#!/usr/bin/env python3
"""
BACKEND RESERVATION TESTING - KhanelConcept Villa Rental System
================================================================

Test suite for reservation page backend functionality after frontend improvements.
Tests the backend components that support the reservation system.

CONTEXT: Testing backend support for reservation page after corrections to:
- /app/assets/js/reservation-enhanced.js (added complete villa database)
- /app/reservation.html (updated CSS and JavaScript)

TEST SCOPE:
1. Backend Server Status - Verify FastAPI server is running and responsive
2. Static File Serving - Test that reservation.html and reservation-enhanced.js files are served correctly
3. Villa Data Access - Verify the backend can serve villa data and images properly for the reservation system
4. API Health Check - Basic health check of key endpoints that might be used by the reservation page
"""

import asyncio
import aiohttp
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid

class BackendReservationTester:
    def __init__(self):
        # Use internal backend URL for testing
        self.backend_url = "http://localhost:8001"
        self.api_url = f"{self.backend_url}/api"
        self.test_results = []
        self.session = None
        
    async def setup_session(self):
        """Initialize HTTP session"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            connector=aiohttp.TCPConnector(verify_ssl=False)
        )
        
    async def cleanup_session(self):
        """Cleanup HTTP session"""
        if self.session:
            await self.session.close()
            
    def log_test(self, test_name: str, success: bool, details: str = "", data: Any = None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        if details:
            print(f"    {details}")
        if not success and data:
            print(f"    Error data: {data}")
        print()

    async def test_backend_server_status(self):
        """Test 1: Backend Server Status - Verify FastAPI server is running and responsive"""
        print("🔍 TEST 1: Backend Server Status")
        print("=" * 50)
        
        try:
            # Test basic server connectivity
            async with self.session.get(f"{self.backend_url}/") as response:
                if response.status == 200:
                    self.log_test(
                        "Backend Server Connectivity", 
                        True, 
                        f"Server responding on {self.backend_url} with status {response.status}"
                    )
                else:
                    self.log_test(
                        "Backend Server Connectivity", 
                        False, 
                        f"Server returned status {response.status}",
                        {"status": response.status}
                    )
                    
        except Exception as e:
            self.log_test(
                "Backend Server Connectivity", 
                False, 
                f"Failed to connect to backend server: {str(e)}",
                {"error": str(e)}
            )
            
        # Test FastAPI docs endpoint (indicates FastAPI is running)
        try:
            async with self.session.get(f"{self.backend_url}/docs") as response:
                if response.status == 200:
                    self.log_test(
                        "FastAPI Documentation Endpoint", 
                        True, 
                        "FastAPI docs accessible - server is running FastAPI"
                    )
                else:
                    self.log_test(
                        "FastAPI Documentation Endpoint", 
                        False, 
                        f"FastAPI docs returned status {response.status}"
                    )
        except Exception as e:
            self.log_test(
                "FastAPI Documentation Endpoint", 
                False, 
                f"FastAPI docs not accessible: {str(e)}"
            )

    async def test_static_file_serving(self):
        """Test 2: Static File Serving - Test that reservation.html and reservation-enhanced.js are served correctly"""
        print("🔍 TEST 2: Static File Serving")
        print("=" * 50)
        
        # Test reservation.html serving
        try:
            async with self.session.get(f"{self.backend_url}/reservation.html") as response:
                if response.status == 200:
                    content = await response.text()
                    
                    # Check if it's actually HTML content
                    if "<!DOCTYPE html>" in content and "reservation" in content.lower():
                        self.log_test(
                            "Reservation HTML File Serving", 
                            True, 
                            f"reservation.html served correctly ({len(content)} bytes)"
                        )
                        
                        # Check for key reservation elements
                        key_elements = [
                            "KhanelConcept",
                            "reservation",
                            "villa",
                            "form"
                        ]
                        
                        missing_elements = [elem for elem in key_elements if elem.lower() not in content.lower()]
                        
                        if not missing_elements:
                            self.log_test(
                                "Reservation HTML Content Validation", 
                                True, 
                                "All key reservation elements found in HTML"
                            )
                        else:
                            self.log_test(
                                "Reservation HTML Content Validation", 
                                False, 
                                f"Missing elements: {missing_elements}"
                            )
                    else:
                        self.log_test(
                            "Reservation HTML File Serving", 
                            False, 
                            "File served but doesn't appear to be valid HTML reservation page"
                        )
                else:
                    self.log_test(
                        "Reservation HTML File Serving", 
                        False, 
                        f"reservation.html returned status {response.status}"
                    )
        except Exception as e:
            self.log_test(
                "Reservation HTML File Serving", 
                False, 
                f"Failed to serve reservation.html: {str(e)}"
            )
            
        # Test reservation-enhanced.js serving
        try:
            async with self.session.get(f"{self.backend_url}/assets/js/reservation-enhanced.js") as response:
                if response.status == 200:
                    content = await response.text()
                    
                    # Check if it's JavaScript content with villa data
                    if "villaData" in content and "ReservationEnhanced" in content:
                        self.log_test(
                            "Reservation Enhanced JS File Serving", 
                            True, 
                            f"reservation-enhanced.js served correctly ({len(content)} bytes)"
                        )
                        
                        # Check for key JavaScript elements
                        js_elements = [
                            "villaData",
                            "ReservationEnhanced",
                            "handleURLParameters",
                            "updateVillaDisplay"
                        ]
                        
                        missing_js_elements = [elem for elem in js_elements if elem not in content]
                        
                        if not missing_js_elements:
                            self.log_test(
                                "Reservation JS Content Validation", 
                                True, 
                                "All key JavaScript functions found"
                            )
                        else:
                            self.log_test(
                                "Reservation JS Content Validation", 
                                False, 
                                f"Missing JS elements: {missing_js_elements}"
                            )
                            
                        # Check villa database completeness
                        villa_count = content.count("id:")
                        if villa_count >= 10:  # Should have multiple villas
                            self.log_test(
                                "Villa Database in JS", 
                                True, 
                                f"Villa database contains {villa_count} villa entries"
                            )
                        else:
                            self.log_test(
                                "Villa Database in JS", 
                                False, 
                                f"Villa database appears incomplete ({villa_count} entries)"
                            )
                    else:
                        self.log_test(
                            "Reservation Enhanced JS File Serving", 
                            False, 
                            "File served but doesn't appear to be valid reservation JavaScript"
                        )
                else:
                    self.log_test(
                        "Reservation Enhanced JS File Serving", 
                        False, 
                        f"reservation-enhanced.js returned status {response.status}"
                    )
        except Exception as e:
            self.log_test(
                "Reservation Enhanced JS File Serving", 
                False, 
                f"Failed to serve reservation-enhanced.js: {str(e)}"
            )

    async def test_villa_data_access(self):
        """Test 3: Villa Data Access - Verify backend can serve villa data and images properly"""
        print("🔍 TEST 3: Villa Data Access")
        print("=" * 50)
        
        # Test villa API endpoint
        try:
            async with self.session.get(f"{self.api_url}/villas") as response:
                if response.status == 200:
                    villas = await response.json()
                    
                    if isinstance(villas, list) and len(villas) > 0:
                        self.log_test(
                            "Villa API Endpoint", 
                            True, 
                            f"Villa API returned {len(villas)} villas"
                        )
                        
                        # Test villa data structure
                        first_villa = villas[0]
                        required_fields = ["id", "name", "location", "price", "guests", "image"]
                        missing_fields = [field for field in required_fields if field not in first_villa]
                        
                        if not missing_fields:
                            self.log_test(
                                "Villa Data Structure", 
                                True, 
                                "All required villa fields present"
                            )
                        else:
                            self.log_test(
                                "Villa Data Structure", 
                                False, 
                                f"Missing villa fields: {missing_fields}"
                            )
                            
                        # Test specific villas mentioned in reservation-enhanced.js
                        test_villa_ids = [
                            "bas-de-f3-sur-le-robert",
                            "villa-f3-petit-macabou", 
                            "villa-f5-sur-ste-anne"
                        ]
                        
                        found_villas = []
                        for villa in villas:
                            villa_id = str(villa.get("id", "")).lower()
                            villa_name = villa.get("name", "").lower()
                            
                            for test_id in test_villa_ids:
                                if test_id in villa_id or test_id.replace("-", " ") in villa_name:
                                    found_villas.append(test_id)
                                    break
                        
                        if len(found_villas) >= 2:  # At least 2 of the test villas should be found
                            self.log_test(
                                "Key Villa Availability", 
                                True, 
                                f"Found key villas: {found_villas}"
                            )
                        else:
                            self.log_test(
                                "Key Villa Availability", 
                                False, 
                                f"Only found {len(found_villas)} key villas: {found_villas}"
                            )
                            
                    else:
                        self.log_test(
                            "Villa API Endpoint", 
                            False, 
                            "Villa API returned empty or invalid data"
                        )
                else:
                    self.log_test(
                        "Villa API Endpoint", 
                        False, 
                        f"Villa API returned status {response.status}"
                    )
        except Exception as e:
            self.log_test(
                "Villa API Endpoint", 
                False, 
                f"Failed to access villa API: {str(e)}"
            )
            
        # Test villa search functionality
        try:
            search_data = {
                "destination": "Vauclin",
                "guests": 6,
                "category": "sejour"
            }
            
            async with self.session.post(
                f"{self.api_url}/villas/search", 
                json=search_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    search_results = await response.json()
                    
                    if isinstance(search_results, list):
                        self.log_test(
                            "Villa Search Functionality", 
                            True, 
                            f"Villa search returned {len(search_results)} results for Vauclin"
                        )
                    else:
                        self.log_test(
                            "Villa Search Functionality", 
                            False, 
                            "Villa search returned invalid data format"
                        )
                else:
                    self.log_test(
                        "Villa Search Functionality", 
                        False, 
                        f"Villa search returned status {response.status}"
                    )
        except Exception as e:
            self.log_test(
                "Villa Search Functionality", 
                False, 
                f"Failed to test villa search: {str(e)}"
            )
            
        # Test villa image serving
        try:
            # Get a villa with an image
            async with self.session.get(f"{self.api_url}/villas") as response:
                if response.status == 200:
                    villas = await response.json()
                    villa_with_image = None
                    
                    for villa in villas:
                        if villa.get("image") and not villa["image"].startswith("http"):
                            villa_with_image = villa
                            break
                    
                    if villa_with_image:
                        image_path = villa_with_image["image"]
                        if image_path.startswith("./"):
                            image_path = image_path[2:]  # Remove ./
                        
                        async with self.session.get(f"{self.backend_url}/{image_path}") as img_response:
                            if img_response.status == 200:
                                content_type = img_response.headers.get("content-type", "")
                                if "image" in content_type:
                                    self.log_test(
                                        "Villa Image Serving", 
                                        True, 
                                        f"Villa image served correctly (Content-Type: {content_type})"
                                    )
                                else:
                                    self.log_test(
                                        "Villa Image Serving", 
                                        False, 
                                        f"Image served but wrong content type: {content_type}"
                                    )
                            else:
                                self.log_test(
                                    "Villa Image Serving", 
                                    False, 
                                    f"Villa image returned status {img_response.status}"
                                )
                    else:
                        self.log_test(
                            "Villa Image Serving", 
                            False, 
                            "No villa with local image path found for testing"
                        )
        except Exception as e:
            self.log_test(
                "Villa Image Serving", 
                False, 
                f"Failed to test villa image serving: {str(e)}"
            )

    async def test_api_health_check(self):
        """Test 4: API Health Check - Basic health check of key endpoints"""
        print("🔍 TEST 4: API Health Check")
        print("=" * 50)
        
        # Test health endpoint
        try:
            async with self.session.get(f"{self.api_url}/health") as response:
                if response.status == 200:
                    health_data = await response.json()
                    
                    if "status" in health_data and health_data["status"] == "healthy":
                        self.log_test(
                            "API Health Endpoint", 
                            True, 
                            f"API health check passed: {health_data}"
                        )
                    else:
                        self.log_test(
                            "API Health Endpoint", 
                            False, 
                            f"API health check returned unexpected data: {health_data}"
                        )
                else:
                    self.log_test(
                        "API Health Endpoint", 
                        False, 
                        f"Health endpoint returned status {response.status}"
                    )
        except Exception as e:
            self.log_test(
                "API Health Endpoint", 
                False, 
                f"Failed to access health endpoint: {str(e)}"
            )
            
        # Test reservation creation endpoint (without actually creating)
        try:
            # Test with invalid data to check endpoint exists and validates
            invalid_reservation = {
                "villa_id": "test",
                "customer_name": "",  # Invalid - empty
                "customer_email": "invalid-email",  # Invalid format
                "customer_phone": "",
                "checkin_date": "",
                "checkout_date": "",
                "guests_count": 0,
                "total_price": 0
            }
            
            async with self.session.post(
                f"{self.api_url}/reservations",
                json=invalid_reservation,
                headers={"Content-Type": "application/json"}
            ) as response:
                # We expect this to fail validation (400 or 422), which means endpoint exists
                if response.status in [400, 422, 404]:  # 404 if villa not found
                    self.log_test(
                        "Reservation Endpoint Validation", 
                        True, 
                        f"Reservation endpoint exists and validates input (status {response.status})"
                    )
                elif response.status == 200:
                    self.log_test(
                        "Reservation Endpoint Validation", 
                        False, 
                        "Reservation endpoint accepted invalid data - validation may be missing"
                    )
                else:
                    self.log_test(
                        "Reservation Endpoint Validation", 
                        False, 
                        f"Unexpected response from reservation endpoint: {response.status}"
                    )
        except Exception as e:
            self.log_test(
                "Reservation Endpoint Validation", 
                False, 
                f"Failed to test reservation endpoint: {str(e)}"
            )
            
        # Test dashboard stats endpoint (used by admin)
        try:
            async with self.session.get(f"{self.api_url}/stats/dashboard") as response:
                if response.status == 200:
                    stats = await response.json()
                    
                    required_stats = ["total_villas", "total_reservations"]
                    missing_stats = [stat for stat in required_stats if stat not in stats]
                    
                    if not missing_stats:
                        self.log_test(
                            "Dashboard Stats Endpoint", 
                            True, 
                            f"Dashboard stats available: {stats}"
                        )
                    else:
                        self.log_test(
                            "Dashboard Stats Endpoint", 
                            False, 
                            f"Missing dashboard stats: {missing_stats}"
                        )
                else:
                    self.log_test(
                        "Dashboard Stats Endpoint", 
                        False, 
                        f"Dashboard stats returned status {response.status}"
                    )
        except Exception as e:
            self.log_test(
                "Dashboard Stats Endpoint", 
                False, 
                f"Failed to access dashboard stats: {str(e)}"
            )

    async def run_all_tests(self):
        """Run all backend reservation tests"""
        print("🚀 BACKEND RESERVATION TESTING - KhanelConcept")
        print("=" * 60)
        print("Testing backend components that support the reservation system")
        print("after frontend improvements to reservation.html and reservation-enhanced.js")
        print("=" * 60)
        print()
        
        await self.setup_session()
        
        try:
            # Run all test suites
            await self.test_backend_server_status()
            await self.test_static_file_serving()
            await self.test_villa_data_access()
            await self.test_api_health_check()
            
        finally:
            await self.cleanup_session()
            
        # Generate summary
        self.generate_summary()
        
    def generate_summary(self):
        """Generate test summary"""
        print("📊 TEST SUMMARY")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results if t["success"]])
        failed_tests = total_tests - passed_tests
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        print()
        
        if failed_tests > 0:
            print("❌ FAILED TESTS:")
            print("-" * 30)
            for test in self.test_results:
                if not test["success"]:
                    print(f"• {test['test']}: {test['details']}")
            print()
            
        print("✅ PASSED TESTS:")
        print("-" * 30)
        for test in self.test_results:
            if test["success"]:
                print(f"• {test['test']}: {test['details']}")
        print()
        
        # Overall assessment
        if success_rate >= 90:
            print("🎉 EXCELLENT: Backend reservation system is working perfectly!")
        elif success_rate >= 75:
            print("✅ GOOD: Backend reservation system is mostly functional with minor issues.")
        elif success_rate >= 50:
            print("⚠️ MODERATE: Backend reservation system has some issues that need attention.")
        else:
            print("❌ CRITICAL: Backend reservation system has major issues requiring immediate attention.")
            
        print()
        print("🔍 DETAILED RESULTS:")
        print("For detailed test results, check the test_results list in the tester object.")
        
        # Save results to file
        try:
            with open("/app/backend_reservation_test_results.json", "w") as f:
                json.dump({
                    "summary": {
                        "total_tests": total_tests,
                        "passed_tests": passed_tests,
                        "failed_tests": failed_tests,
                        "success_rate": success_rate,
                        "timestamp": datetime.now().isoformat()
                    },
                    "test_results": self.test_results
                }, f, indent=2)
            print("📁 Results saved to: /app/backend_reservation_test_results.json")
        except Exception as e:
            print(f"⚠️ Could not save results to file: {e}")

async def main():
    """Main test execution"""
    tester = BackendReservationTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())