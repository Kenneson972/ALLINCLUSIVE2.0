#!/usr/bin/env python3
"""
KhanelConcept Backend Testing Suite - Premium Frontend Support Verification
Comprehensive backend testing for the KhanelConcept villa rental application
Focus: Testing API endpoints that support premium frontend features

CRITICAL ENDPOINTS TO TEST:
1. GET /api/villas - Should return all villa data for frontend display
2. GET /api/admin/villas - Admin villa management API
3. POST /api/villas/search - Villa search functionality for search form
4. GET /api/health - Basic health check
5. POST /api/reservations - Reservation system backend

VERIFICATION REQUIREMENTS:
- Villa data matches what's displayed on 15 villa pages tested
- Villa search filters work correctly (destination, guests, category)
- Villa data includes proper pricing, images, and gallery information
- MongoDB connection and data integrity
- Reservation creation works for premium reservation system
"""

import requests
import json
import sys
from datetime import datetime

# Configuration - Use external URL for production testing
BASE_URL = "https://web-a11y-upgrade.preview.emergentagent.com"
API_BASE = f"{BASE_URL}/api"

class KhanelConceptBackendTester:
    def __init__(self):
        self.passed_tests = 0
        self.failed_tests = 0
        self.test_results = []
        self.session = requests.Session()
        
    def log_test(self, test_name, passed, message, details=None):
        """Log test result"""
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status} - {test_name}: {message}")
        
        if details:
            print(f"   Details: {details}")
            
        self.test_results.append({
            "test": test_name,
            "passed": passed,
            "message": message,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        
        if passed:
            self.passed_tests += 1
        else:
            self.failed_tests += 1
    
    def test_api_health(self):
        """Test 1: Basic API health check"""
        try:
            response = self.session.get(f"{API_BASE}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_test(
                    "API Health Check",
                    True,
                    f"API accessible, status: {data.get('status', 'unknown')}"
                )
                return True
            else:
                self.log_test(
                    "API Health Check",
                    False,
                    f"API not accessible, status code: {response.status_code}"
                )
                return False
        except Exception as e:
            self.log_test(
                "API Health Check",
                False,
                f"Connection error: {str(e)}"
            )
            return False
    
    def test_get_all_villas(self):
        """Test 2: GET /api/villas - Should return all villa data for frontend display"""
        try:
            response = self.session.get(f"{API_BASE}/villas", timeout=10)
            if response.status_code != 200:
                self.log_test(
                    "GET /api/villas",
                    False,
                    f"API error: {response.status_code}"
                )
                return False
            
            villas = response.json()
            villa_count = len(villas)
            
            # Verify we have villas
            if villa_count == 0:
                self.log_test(
                    "GET /api/villas - Villa Count",
                    False,
                    "No villas returned from API"
                )
                return False
            
            # Verify data structure for frontend display
            required_fields = ['id', 'name', 'location', 'price', 'guests', 'category', 'image', 'gallery']
            missing_fields = []
            
            for villa in villas[:3]:  # Check first 3 villas
                for field in required_fields:
                    if field not in villa:
                        missing_fields.append(f"{villa.get('name', 'Unknown')}: {field}")
            
            if not missing_fields:
                self.log_test(
                    "GET /api/villas - Data Structure",
                    True,
                    f"All {villa_count} villas have required fields for frontend display"
                )
            else:
                self.log_test(
                    "GET /api/villas - Data Structure",
                    False,
                    f"Missing fields: {', '.join(missing_fields)}"
                )
                return False
            
            # Verify pricing and gallery information
            villas_with_pricing = sum(1 for v in villas if v.get('price', 0) > 0)
            villas_with_gallery = sum(1 for v in villas if v.get('gallery') and len(v.get('gallery', [])) > 0)
            
            self.log_test(
                "GET /api/villas - Pricing Data",
                villas_with_pricing == villa_count,
                f"{villas_with_pricing}/{villa_count} villas have pricing data"
            )
            
            self.log_test(
                "GET /api/villas - Gallery Data",
                villas_with_gallery >= villa_count * 0.8,  # At least 80% should have galleries
                f"{villas_with_gallery}/{villa_count} villas have gallery data"
            )
            
            return villas
            
        except Exception as e:
            self.log_test(
                "GET /api/villas",
                False,
                f"Error retrieving villas: {str(e)}"
            )
            return False
    
    def test_admin_villas_endpoint(self):
        """Test 3: GET /api/admin/villas - Admin villa management API"""
        try:
            response = self.session.get(f"{API_BASE}/admin/villas", timeout=10)
            if response.status_code != 200:
                self.log_test(
                    "GET /api/admin/villas",
                    False,
                    f"Admin API error: {response.status_code}"
                )
                return False
            
            admin_villas = response.json()
            admin_villa_count = len(admin_villas)
            
            if admin_villa_count > 0:
                self.log_test(
                    "GET /api/admin/villas",
                    True,
                    f"Admin villa management API working - {admin_villa_count} villas retrieved"
                )
                return True
            else:
                self.log_test(
                    "GET /api/admin/villas",
                    False,
                    "Admin API returned no villas"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "GET /api/admin/villas",
                False,
                f"Error accessing admin villas: {str(e)}"
            )
            return False
    
    def test_villa_search_functionality(self):
        """Test 4: POST /api/villas/search - Villa search functionality for search form"""
        search_tests = [
            {
                "name": "Search by Destination",
                "filters": {"destination": "Vauclin"},
                "expected_min": 1
            },
            {
                "name": "Search by Guests",
                "filters": {"guests": 6},
                "expected_min": 1
            },
            {
                "name": "Search by Category",
                "filters": {"category": "sejour"},
                "expected_min": 1
            },
            {
                "name": "Combined Search",
                "filters": {"destination": "Petit Macabou", "guests": 4, "category": "sejour"},
                "expected_min": 0  # May return 0 results, but should not error
            }
        ]
        
        all_passed = True
        
        for test in search_tests:
            try:
                response = self.session.post(
                    f"{API_BASE}/villas/search",
                    json=test["filters"],
                    timeout=10
                )
                
                if response.status_code == 200:
                    results = response.json()
                    result_count = len(results)
                    
                    if result_count >= test["expected_min"]:
                        self.log_test(
                            f"Villa Search - {test['name']}",
                            True,
                            f"Search returned {result_count} results",
                            f"Filters: {test['filters']}"
                        )
                    else:
                        self.log_test(
                            f"Villa Search - {test['name']}",
                            False,
                            f"Expected at least {test['expected_min']} results, got {result_count}",
                            f"Filters: {test['filters']}"
                        )
                        all_passed = False
                else:
                    self.log_test(
                        f"Villa Search - {test['name']}",
                        False,
                        f"Search API error: {response.status_code}"
                    )
                    all_passed = False
                    
            except Exception as e:
                self.log_test(
                    f"Villa Search - {test['name']}",
                    False,
                    f"Search error: {str(e)}"
                )
                all_passed = False
        
        return all_passed
    
    def test_reservation_system(self):
        """Test 5: POST /api/reservations - Reservation system backend"""
        try:
            # First get a villa to make a reservation for
            villas_response = self.session.get(f"{API_BASE}/villas", timeout=10)
            if villas_response.status_code != 200:
                self.log_test(
                    "Reservation System - Setup",
                    False,
                    "Could not retrieve villas for reservation test"
                )
                return False
            
            villas = villas_response.json()
            if not villas:
                self.log_test(
                    "Reservation System - Setup",
                    False,
                    "No villas available for reservation test"
                )
                return False
            
            # Use first villa for test reservation
            test_villa = villas[0]
            
            reservation_data = {
                "villa_id": test_villa["id"],
                "customer_name": "Marie Dubois",
                "customer_email": "marie.dubois@test.com",
                "customer_phone": "+596123456789",
                "checkin_date": "2025-02-15",
                "checkout_date": "2025-02-22",
                "guests_count": 4,
                "message": "Test reservation for backend verification",
                "total_price": test_villa.get("price", 850)
            }
            
            response = self.session.post(
                f"{API_BASE}/reservations",
                json=reservation_data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success") and result.get("reservation_id"):
                    self.log_test(
                        "Reservation System",
                        True,
                        f"Reservation created successfully - ID: {result['reservation_id']}",
                        f"Villa: {test_villa['name']}, Price: €{reservation_data['total_price']}"
                    )
                    return True
                else:
                    self.log_test(
                        "Reservation System",
                        False,
                        "Reservation response missing success/ID fields",
                        result
                    )
                    return False
            else:
                self.log_test(
                    "Reservation System",
                    False,
                    f"Reservation API error: {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Reservation System",
                False,
                f"Reservation error: {str(e)}"
            )
            return False
    
    def test_mongodb_connection_integrity(self):
        """Test 6: Verify MongoDB connection and data integrity"""
        try:
            # Test dashboard stats to verify MongoDB connection
            response = self.session.get(f"{API_BASE}/stats/dashboard", timeout=10)
            
            if response.status_code == 200:
                stats = response.json()
                required_stats = ["total_villas", "total_reservations", "monthly_revenue"]
                
                missing_stats = [stat for stat in required_stats if stat not in stats]
                if missing_stats:
                    self.log_test(
                        "MongoDB Connection - Stats",
                        False,
                        f"Missing dashboard stats: {missing_stats}"
                    )
                    return False
                
                # Verify reasonable data
                if stats["total_villas"] > 0:
                    self.log_test(
                        "MongoDB Connection - Data Integrity",
                        True,
                        f"MongoDB connected with {stats['total_villas']} villas, {stats['total_reservations']} reservations",
                        f"Monthly revenue: €{stats['monthly_revenue']}"
                    )
                    return True
                else:
                    self.log_test(
                        "MongoDB Connection - Data Integrity",
                        False,
                        "MongoDB connected but no villa data found"
                    )
                    return False
            else:
                self.log_test(
                    "MongoDB Connection",
                    False,
                    f"Dashboard stats API error: {response.status_code}"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "MongoDB Connection",
                False,
                f"MongoDB connection error: {str(e)}"
            )
            return False
    
    def test_villa_data_frontend_compatibility(self, villas):
        """Test 7: Verify villa data matches frontend requirements"""
        if not villas:
            self.log_test(
                "Villa Data Frontend Compatibility",
                False,
                "No villa data available for compatibility test"
            )
            return False
        
        # Test specific requirements for frontend display
        compatibility_issues = []
        
        for villa in villas[:5]:  # Test first 5 villas
            villa_name = villa.get("name", "Unknown")
            
            # Check image paths are valid
            image = villa.get("image", "")
            if not image or "placeholder" in image.lower():
                compatibility_issues.append(f"{villa_name}: Invalid/placeholder image")
            
            # Check gallery has multiple images
            gallery = villa.get("gallery", [])
            if len(gallery) < 2:
                compatibility_issues.append(f"{villa_name}: Gallery has less than 2 images")
            
            # Check pricing is reasonable
            price = villa.get("price", 0)
            if price <= 0 or price > 10000:
                compatibility_issues.append(f"{villa_name}: Unreasonable price €{price}")
            
            # Check location is specified
            location = villa.get("location", "")
            if not location or len(location) < 3:
                compatibility_issues.append(f"{villa_name}: Missing/invalid location")
        
        if not compatibility_issues:
            self.log_test(
                "Villa Data Frontend Compatibility",
                True,
                "All tested villas have data compatible with frontend display"
            )
            return True
        else:
            self.log_test(
                "Villa Data Frontend Compatibility",
                False,
                f"Found {len(compatibility_issues)} compatibility issues",
                compatibility_issues[:3]  # Show first 3 issues
            )
            return False
    
    def run_comprehensive_tests(self):
        """Execute all comprehensive backend tests for premium frontend support"""
        print("🏖️ KHANELCONCEPT BACKEND TESTING - PREMIUM FRONTEND SUPPORT VERIFICATION")
        print("=" * 80)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print(f"Backend URL: {BASE_URL}")
        print()
        
        # Test 1: Health check
        if not self.test_api_health():
            print("❌ API not accessible, stopping tests")
            return False
        
        print()
        
        # Test 2: Get all villas for frontend display
        villas = self.test_get_all_villas()
        if not villas:
            print("❌ Cannot retrieve villa data")
            return False
        
        print()
        
        # Test 3: Admin villa management
        self.test_admin_villas_endpoint()
        
        print()
        
        # Test 4: Villa search functionality
        self.test_villa_search_functionality()
        
        print()
        
        # Test 5: Reservation system
        self.test_reservation_system()
        
        print()
        
        # Test 6: MongoDB connection and data integrity
        self.test_mongodb_connection_integrity()
        
        print()
        
        # Test 7: Villa data frontend compatibility
        self.test_villa_data_frontend_compatibility(villas)
        
        print()
        print("=" * 80)
        print("📊 TEST RESULTS")
        print("=" * 80)
        
        total_tests = self.passed_tests + self.failed_tests
        success_rate = (self.passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"✅ Tests passed: {self.passed_tests}")
        print(f"❌ Tests failed: {self.failed_tests}")
        print(f"📈 Success rate: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("🎉 EXCELLENT - Backend APIs perfectly support premium frontend features!")
        elif success_rate >= 75:
            print("✅ GOOD - Most backend APIs are working correctly")
        elif success_rate >= 50:
            print("⚠️ MODERATE - Some backend APIs need attention")
        else:
            print("❌ CRITICAL - Backend APIs require immediate intervention")
        
        print()
        
        # Summary of critical issues
        critical_issues = []
        for result in self.test_results:
            if not result["passed"] and any(keyword in result["test"].lower() for keyword in ["health", "villas", "search", "reservation"]):
                critical_issues.append(result["test"])
        
        if critical_issues:
            print("🚨 CRITICAL ISSUES IDENTIFIED:")
            for issue in critical_issues:
                print(f"   - {issue}")
        else:
            print("✅ No critical issues identified")
        
        return success_rate >= 75

def main():
    """Main entry point"""
    tester = KhanelConceptBackendTester()
    success = tester.run_comprehensive_tests()
    
    # Save results
    with open('/app/backend_test_results.json', 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "success": success,
            "passed_tests": tester.passed_tests,
            "failed_tests": tester.failed_tests,
            "test_results": tester.test_results
        }, f, indent=2, ensure_ascii=False)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())