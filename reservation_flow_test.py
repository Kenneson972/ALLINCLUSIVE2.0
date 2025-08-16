#!/usr/bin/env python3
"""
Reservation Flow Testing for KhanelConcept
Testing the complete reservation flow including URL parameters and villa data transmission
"""

import requests
import json
from datetime import datetime

# Production URL
BACKEND_URL = "https://web-a11y-upgrade.preview.emergentagent.com"
API_BASE_URL = f"{BACKEND_URL}/api"

class ReservationFlowTester:
    def __init__(self):
        self.session = requests.Session()
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
    
    def test_villa_data_for_reservation(self):
        """Test that villa data is available for reservation page"""
        try:
            # Test specific villas mentioned in the review request
            test_villas = [
                {"name": "Villa F3", "expected_price": 850, "expected_location": "Vauclin"},
                {"name": "Villa F5", "expected_price": 1300, "expected_location": "Ste Anne"},
                {"name": "Villa F3 POUR LA BACCHA", "expected_price": 1350, "expected_location": "Petit Macabou"}
            ]
            
            # Get all villas
            response = self.session.get(f"{API_BASE_URL}/villas", timeout=10)
            
            if response.status_code == 200:
                villas = response.json()
                villa_dict = {villa["name"]: villa for villa in villas}
                
                found_villas = 0
                for test_villa in test_villas:
                    villa_name = test_villa["name"]
                    if villa_name in villa_dict:
                        villa = villa_dict[villa_name]
                        found_villas += 1
                        
                        # Verify price and location data
                        price_match = villa["price"] == test_villa["expected_price"]
                        location_match = test_villa["expected_location"].lower() in villa["location"].lower()
                        
                        if price_match and location_match:
                            self.log_test(f"Villa Data - {villa_name}", True, 
                                        f"Villa data correct: €{villa['price']}, {villa['location']}")
                        else:
                            self.log_test(f"Villa Data - {villa_name}", False, 
                                        f"Data mismatch - Price: {villa['price']} (expected {test_villa['expected_price']}), Location: {villa['location']}")
                
                if found_villas == len(test_villas):
                    self.log_test("Villa Data Availability", True, 
                                f"All {found_villas} test villas found with correct data")
                    return True
                else:
                    self.log_test("Villa Data Availability", False, 
                                f"Only {found_villas}/{len(test_villas)} test villas found")
                    return False
            else:
                self.log_test("Villa Data Availability", False, 
                            f"Failed to retrieve villas - status {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Villa Data Availability", False, f"Error: {str(e)}")
            return False
    
    def test_reservation_creation(self):
        """Test reservation creation with realistic data"""
        try:
            # Create a realistic reservation
            reservation_data = {
                "villa_id": "1",  # Villa F3 Petit Macabou
                "customer_name": "Marie Dubois",
                "customer_email": "marie.dubois@email.com",
                "customer_phone": "0696123456",
                "checkin_date": "2025-08-15",
                "checkout_date": "2025-08-22",
                "guests_count": 4,
                "message": "Réservation pour vacances en famille",
                "total_price": 5950.0  # 7 nights * 850€
            }
            
            response = self.session.post(
                f"{API_BASE_URL}/reservations",
                json=reservation_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "reservation_id" in data:
                    self.log_test("Reservation Creation", True, 
                                f"Reservation created successfully - ID: {data['reservation_id']}", 
                                f"Villa: {data.get('villa_name', 'Unknown')}")
                    return data["reservation_id"]
                else:
                    self.log_test("Reservation Creation", False, 
                                "Reservation response missing required fields", data)
                    return None
            else:
                self.log_test("Reservation Creation", False, 
                            f"Reservation failed - status {response.status_code}", 
                            response.text)
                return None
                
        except Exception as e:
            self.log_test("Reservation Creation", False, f"Error: {str(e)}")
            return None
    
    def test_static_pages_accessibility(self):
        """Test that key static pages are accessible"""
        try:
            # Test key pages mentioned in the review request
            test_pages = [
                "index.html",
                "reservation.html", 
                "villa-f3-petit-macabou.html"
            ]
            
            accessible_pages = 0
            for page in test_pages:
                try:
                    response = self.session.get(f"{BACKEND_URL}/{page}", timeout=10)
                    if response.status_code == 200:
                        # Check if it's HTML content
                        if "html" in response.headers.get("content-type", "").lower() or \
                           "<html" in response.text.lower():
                            accessible_pages += 1
                            self.log_test(f"Page Access - {page}", True, "Page accessible and contains HTML")
                        else:
                            self.log_test(f"Page Access - {page}", False, "Page accessible but not HTML content")
                    else:
                        self.log_test(f"Page Access - {page}", False, f"Page not accessible - status {response.status_code}")
                except Exception as e:
                    self.log_test(f"Page Access - {page}", False, f"Error accessing page: {str(e)}")
            
            if accessible_pages == len(test_pages):
                self.log_test("Static Pages Accessibility", True, 
                            f"All {accessible_pages} key pages accessible")
                return True
            else:
                self.log_test("Static Pages Accessibility", False, 
                            f"Only {accessible_pages}/{len(test_pages)} pages accessible")
                return False
                
        except Exception as e:
            self.log_test("Static Pages Accessibility", False, f"Error: {str(e)}")
            return False
    
    def test_villa_images_mapping(self):
        """Test that villa images are properly mapped"""
        try:
            # Get villas and check image paths
            response = self.session.get(f"{API_BASE_URL}/villas", timeout=10)
            
            if response.status_code == 200:
                villas = response.json()
                
                # Check specific villas mentioned in review request
                villa_image_tests = [
                    {"name": "Villa F3 Petit Macabou", "expected_path": "Villa_F3_Petit_Macabou"},
                    {"name": "Villa F5 Ste Anne", "expected_path": "Villa_F5_Ste_Anne"},
                    {"name": "Villa F3 POUR LA BACCHA", "expected_path": "Villa_F3_Baccha_Petit_Macabou"}
                ]
                
                correct_mappings = 0
                for test in villa_image_tests:
                    villa = next((v for v in villas if v["name"] == test["name"]), None)
                    if villa:
                        image_path = villa.get("image", "")
                        gallery = villa.get("gallery", [])
                        
                        # Check if expected path is in image or gallery
                        path_found = (test["expected_path"] in image_path or 
                                    any(test["expected_path"] in img for img in gallery))
                        
                        if path_found:
                            correct_mappings += 1
                            self.log_test(f"Image Mapping - {test['name']}", True, 
                                        f"Correct image path found: {test['expected_path']}")
                        else:
                            self.log_test(f"Image Mapping - {test['name']}", False, 
                                        f"Expected path '{test['expected_path']}' not found in {image_path}")
                    else:
                        self.log_test(f"Image Mapping - {test['name']}", False, "Villa not found")
                
                if correct_mappings == len(villa_image_tests):
                    self.log_test("Villa Images Mapping", True, 
                                f"All {correct_mappings} villa image mappings correct")
                    return True
                else:
                    self.log_test("Villa Images Mapping", False, 
                                f"Only {correct_mappings}/{len(villa_image_tests)} mappings correct")
                    return False
            else:
                self.log_test("Villa Images Mapping", False, 
                            f"Failed to retrieve villas - status {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Villa Images Mapping", False, f"Error: {str(e)}")
            return False
    
    def run_reservation_flow_tests(self):
        """Run all reservation flow tests"""
        print("🏖️ Starting KhanelConcept Reservation Flow Tests")
        print(f"Testing against: {BACKEND_URL}")
        print("=" * 60)
        
        # Test villa data availability for reservation page
        self.test_villa_data_for_reservation()
        
        # Test reservation creation functionality
        reservation_id = self.test_reservation_creation()
        
        # Test static pages accessibility
        self.test_static_pages_accessibility()
        
        # Test villa image mappings
        self.test_villa_images_mapping()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 RESERVATION FLOW TEST SUMMARY")
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
    tester = ReservationFlowTester()
    success = tester.run_reservation_flow_tests()
    
    if success:
        print("\n🎉 All reservation flow tests passed!")
    else:
        print("\n⚠️  Some reservation flow tests failed - check details above")