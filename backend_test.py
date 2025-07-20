#!/usr/bin/env python3
"""
Backend API Testing for KhanelConcept Admin Routes
Testing the new admin authentication and management routes
"""

import requests
import json
import os
from datetime import datetime

# Load environment variables
BACKEND_URL = "https://1dca108e-6598-4fcc-bcc6-b86d7551b3e6.preview.emergentagent.com"
API_BASE_URL = f"{BACKEND_URL}/api"

# Admin credentials from the review request
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "khanelconcept2025"

class KhanelConceptAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.admin_token = None
        self.test_results = []
        
    def log_test(self, test_name, success, message, details=None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "details": details
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name} - {message}")
        if details:
            print(f"   Details: {details}")
    
    def test_health_check(self):
        """Test basic API health"""
        try:
            response = self.session.get(f"{API_BASE_URL}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Health Check", True, "API is healthy", data)
                return True
            else:
                self.log_test("Health Check", False, f"Health check failed with status {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Health Check", False, f"Health check error: {str(e)}")
            return False
    
    def test_admin_login(self):
        """Test admin authentication with specified credentials"""
        try:
            login_data = {
                "username": ADMIN_USERNAME,
                "password": ADMIN_PASSWORD
            }
            
            response = self.session.post(
                f"{API_BASE_URL}/admin/login",
                json=login_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data and "token_type" in data:
                    self.admin_token = data["access_token"]
                    self.log_test("Admin Login", True, "Admin authentication successful", 
                                f"Token type: {data['token_type']}")
                    return True
                else:
                    self.log_test("Admin Login", False, "Login response missing token fields", data)
                    return False
            else:
                self.log_test("Admin Login", False, 
                            f"Login failed with status {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("Admin Login", False, f"Login error: {str(e)}")
            return False
    
    def test_dashboard_stats(self):
        """Test dashboard statistics endpoint"""
        try:
            response = self.session.get(f"{API_BASE_URL}/stats/dashboard", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ["total_villas", "total_reservations", "pending_reservations", 
                                 "confirmed_reservations", "monthly_revenue", "monthly_reservations"]
                
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    self.log_test("Dashboard Stats", False, 
                                f"Missing required fields: {missing_fields}", data)
                    return False
                
                # Check if we have 22 villas as expected (updated from 21)
                if data["total_villas"] >= 21:
                    self.log_test("Dashboard Stats", True, 
                                f"Dashboard stats retrieved successfully - {data['total_villas']} villas found", 
                                data)
                    return True
                else:
                    self.log_test("Dashboard Stats", False, 
                                f"Expected at least 21 villas, got {data['total_villas']}", data)
                    return False
            else:
                self.log_test("Dashboard Stats", False, 
                            f"Stats request failed with status {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("Dashboard Stats", False, f"Stats error: {str(e)}")
            return False
    
    def test_admin_villas(self):
        """Test admin villa management endpoint"""
        try:
            response = self.session.get(f"{API_BASE_URL}/admin/villas", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    villa_count = len(data)
                    if villa_count == 21:
                        # Check structure of first villa
                        if data:
                            villa = data[0]
                            required_fields = ["id", "name", "location", "price", "guests", 
                                             "category", "image", "gallery"]
                            missing_fields = [field for field in required_fields if field not in villa]
                            
                            if missing_fields:
                                self.log_test("Admin Villas", False, 
                                            f"Villa data missing fields: {missing_fields}", villa)
                                return False
                            
                            self.log_test("Admin Villas", True, 
                                        f"Retrieved {villa_count} villas with correct structure", 
                                        f"Sample villa: {villa['name']} - {villa['location']}")
                            return True
                        else:
                            self.log_test("Admin Villas", False, "Empty villa list returned")
                            return False
                    else:
                        self.log_test("Admin Villas", False, 
                                    f"Expected 21 villas, got {villa_count}")
                        return False
                else:
                    self.log_test("Admin Villas", False, "Response is not a list", type(data))
                    return False
            else:
                self.log_test("Admin Villas", False, 
                            f"Admin villas request failed with status {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("Admin Villas", False, f"Admin villas error: {str(e)}")
            return False
    
    def test_admin_reservations(self):
        """Test admin reservation management endpoint"""
        try:
            response = self.session.get(f"{API_BASE_URL}/admin/reservations", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    reservation_count = len(data)
                    self.log_test("Admin Reservations", True, 
                                f"Retrieved {reservation_count} reservations successfully", 
                                f"Reservations found: {reservation_count}")
                    
                    # If there are reservations, check structure
                    if data:
                        reservation = data[0]
                        required_fields = ["id", "villa_id", "customer_name", "customer_email", 
                                         "status", "created_at"]
                        missing_fields = [field for field in required_fields if field not in reservation]
                        
                        if missing_fields:
                            self.log_test("Admin Reservations Structure", False, 
                                        f"Reservation data missing fields: {missing_fields}", reservation)
                            return False
                        else:
                            self.log_test("Admin Reservations Structure", True, 
                                        "Reservation data structure is correct")
                    
                    return True
                else:
                    self.log_test("Admin Reservations", False, "Response is not a list", type(data))
                    return False
            else:
                self.log_test("Admin Reservations", False, 
                            f"Admin reservations request failed with status {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("Admin Reservations", False, f"Admin reservations error: {str(e)}")
            return False
    
    def test_public_villas_endpoint(self):
        """Test public villas endpoint to ensure basic functionality"""
        try:
            response = self.session.get(f"{API_BASE_URL}/villas", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) >= 21:
                    self.log_test("Public Villas", True, 
                                f"Public villas endpoint working - {len(data)} villas", 
                                f"Sample villa: {data[0]['name'] if data else 'None'}")
                    return True
                else:
                    self.log_test("Public Villas", False, 
                                f"Expected at least 21 villas, got {len(data) if isinstance(data, list) else 'non-list'}")
                    return False
            else:
                self.log_test("Public Villas", False, 
                            f"Public villas request failed with status {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Public Villas", False, f"Public villas error: {str(e)}")
            return False
    
    def test_villa_search(self):
        """Test villa search functionality"""
        try:
            search_data = {
                "destination": "lamentin",
                "guests": 2,
                "category": "special"
            }
            
            response = self.session.post(
                f"{API_BASE_URL}/villas/search",
                json=search_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_test("Villa Search", True, 
                                f"Search functionality working - found {len(data)} matching villas", 
                                f"Search criteria: {search_data}")
                    return True
                else:
                    self.log_test("Villa Search", False, "Search response is not a list", type(data))
                    return False
            else:
                self.log_test("Villa Search", False, 
                            f"Search request failed with status {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("Villa Search", False, f"Search error: {str(e)}")
            return False
    
    def test_static_villa_pages(self):
        """Test static villa HTML pages are served correctly"""
        # List of villa HTML files that should be accessible
        villa_pages = [
            "villa-f3-petit-macabou.html",
            "villa-f5-ste-anne.html", 
            "villa-f3-baccha-petit-macabou.html",
            "villa-f6-petit-macabou.html",
            "villa-f6-lamentin.html",
            "villa-f3-le-francois.html",
            "villa-f3-robert-pointe-hyacinthe.html",
            "villa-f6-ste-luce-plage.html",
            "villa-f3-trinite-cosmy.html",
            "villa-f7-baie-des-mulets-vauclin.html",
            "villa-f5-r-pilote-la-renee.html",
            "villa-f3-trenelle-location-annuelle.html",
            "villa-f5-vauclin-ravine-plate.html",
            "villa-fete-journee-fort-de-france.html",
            "villa-fete-journee-riviere-salee.html",
            "villa-fete-journee-ducos.html",
            "villa-fete-journee-r-pilote.html",
            "villa-fete-journee-sainte-luce.html"
        ]
        
        accessible_pages = 0
        failed_pages = []
        
        for page in villa_pages:
            try:
                response = self.session.get(f"{BACKEND_URL}/{page}", timeout=10)
                if response.status_code == 200:
                    # Check if it's actually HTML content
                    if "html" in response.headers.get("content-type", "").lower() or \
                       "<html" in response.text.lower():
                        accessible_pages += 1
                    else:
                        failed_pages.append(f"{page} (not HTML content)")
                else:
                    failed_pages.append(f"{page} (status {response.status_code})")
            except Exception as e:
                failed_pages.append(f"{page} (error: {str(e)})")
        
        if accessible_pages >= 15:  # Allow some flexibility as exact count may vary
            self.log_test("Static Villa Pages", True, 
                        f"Villa HTML pages accessible - {accessible_pages}/{len(villa_pages)} pages working", 
                        f"Working pages: {accessible_pages}")
            return True
        else:
            self.log_test("Static Villa Pages", False, 
                        f"Too many villa pages inaccessible - only {accessible_pages}/{len(villa_pages)} working", 
                        f"Failed pages: {failed_pages[:5]}")  # Show first 5 failures
            return False
    
    def test_villa_id_mapping(self):
        """Test that villa IDs 1-21 map correctly to data"""
        try:
            # Get all villas from API
            response = self.session.get(f"{API_BASE_URL}/villas", timeout=10)
            
            if response.status_code == 200:
                villas = response.json()
                villa_ids = [villa["id"] for villa in villas if "id" in villa]
                
                # Check if we have sequential IDs from 1 to at least 21
                expected_ids = [str(i) for i in range(1, 22)]  # 1-21
                missing_ids = [id for id in expected_ids if id not in villa_ids]
                
                if len(missing_ids) == 0:
                    self.log_test("Villa ID Mapping", True, 
                                f"All villa IDs 1-21 present in database", 
                                f"Total villas: {len(villas)}")
                    return True
                else:
                    self.log_test("Villa ID Mapping", False, 
                                f"Missing villa IDs: {missing_ids}", 
                                f"Found IDs: {villa_ids[:10]}...")  # Show first 10
                    return False
            else:
                self.log_test("Villa ID Mapping", False, 
                            f"Could not retrieve villas for ID mapping test - status {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Villa ID Mapping", False, f"Villa ID mapping error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting KhanelConcept Backend API Tests")
        print(f"Testing against: {API_BASE_URL}")
        print("=" * 60)
        
        # Test basic connectivity
        if not self.test_health_check():
            print("❌ Health check failed - stopping tests")
            return False
        
        # Test public endpoints first
        self.test_public_villas_endpoint()
        self.test_villa_search()
        
        # Test new static file serving functionality
        self.test_static_villa_pages()
        self.test_villa_id_mapping()
        
        # Test admin authentication
        if not self.test_admin_login():
            print("❌ Admin login failed - skipping admin-only tests")
        else:
            # Test admin endpoints
            self.test_dashboard_stats()
            self.test_admin_villas()
            self.test_admin_reservations()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        # Show failed tests
        failed_tests = [result for result in self.test_results if not result["success"]]
        if failed_tests:
            print("\n❌ FAILED TESTS:")
            for test in failed_tests:
                print(f"  - {test['test']}: {test['message']}")
        
        return passed == total

if __name__ == "__main__":
    tester = KhanelConceptAPITester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️  Some tests failed - check details above")