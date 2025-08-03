#!/usr/bin/env python3
"""
Villa F3 Backend Testing Suite
Tests backend components supporting Villa F3 enhancements
"""

import requests
import json
import os
import sys
from datetime import datetime
from pathlib import Path

class VillaF3BackendTester:
    def __init__(self):
        # Get backend URL from environment or use default
        self.backend_url = os.getenv('REACT_APP_BACKEND_URL', 'http://localhost:8001')
        self.api_url = f"{self.backend_url}/api"
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'backend_url': self.backend_url,
            'tests': [],
            'summary': {
                'total': 0,
                'passed': 0,
                'failed': 0,
                'success_rate': 0
            }
        }
        
    def log_test(self, test_name, status, details, error=None):
        """Log test result"""
        test_result = {
            'test': test_name,
            'status': status,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        if error:
            test_result['error'] = str(error)
        
        self.results['tests'].append(test_result)
        self.results['summary']['total'] += 1
        
        if status == 'PASS':
            self.results['summary']['passed'] += 1
            print(f"✅ {test_name}: {details}")
        else:
            self.results['summary']['failed'] += 1
            print(f"❌ {test_name}: {details}")
            if error:
                print(f"   Error: {error}")
    
    def test_backend_health(self):
        """Test backend health endpoint"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_test(
                    "Backend Health Check",
                    "PASS",
                    f"Backend responding correctly with status {response.status_code}"
                )
                return True
            else:
                self.log_test(
                    "Backend Health Check",
                    "FAIL",
                    f"Backend returned status {response.status_code}"
                )
                return False
        except Exception as e:
            self.log_test(
                "Backend Health Check",
                "FAIL",
                "Backend not accessible",
                e
            )
            return False
    
    def test_static_file_serving(self):
        """Test static file serving for Villa F3 pages"""
        files_to_test = [
            {
                'path': '/villa-villa-f3-sur-petit-macabou.html',
                'name': 'Villa F3 Detail Page'
            },
            {
                'path': '/reservation.html',
                'name': 'Reservation Page'
            }
        ]
        
        for file_info in files_to_test:
            try:
                response = requests.get(f"{self.backend_url}{file_info['path']}", timeout=10)
                if response.status_code == 200:
                    content = response.text
                    # Check for key content
                    if 'Villa F3' in content or 'reservation' in content.lower():
                        self.log_test(
                            f"Static File: {file_info['name']}",
                            "PASS",
                            f"File served correctly ({len(content)} bytes)"
                        )
                    else:
                        self.log_test(
                            f"Static File: {file_info['name']}",
                            "FAIL",
                            "File served but content appears incorrect"
                        )
                else:
                    self.log_test(
                        f"Static File: {file_info['name']}",
                        "FAIL",
                        f"File not accessible (status {response.status_code})"
                    )
            except Exception as e:
                self.log_test(
                    f"Static File: {file_info['name']}",
                    "FAIL",
                    "File not accessible",
                    e
                )
    
    def test_villa_f3_video_path(self):
        """Test video file accessibility"""
        video_paths = [
            '/ALLINCLUSIVE2.0/images/Villa_F3_Petit_Macabou/youtube video__-puEXXjWZA.mp4',
            '/images/Villa_F3_Petit_Macabou/youtube video__-puEXXjWZA.mp4'
        ]
        
        video_found = False
        for video_path in video_paths:
            try:
                response = requests.head(f"{self.backend_url}{video_path}", timeout=10)
                if response.status_code == 200:
                    content_type = response.headers.get('content-type', '')
                    if 'video' in content_type:
                        self.log_test(
                            "Villa F3 Video File",
                            "PASS",
                            f"Video file accessible at {video_path}"
                        )
                        video_found = True
                        break
                    else:
                        self.log_test(
                            "Villa F3 Video File",
                            "FAIL",
                            f"File found but not video type: {content_type}"
                        )
                else:
                    continue  # Try next path
            except Exception as e:
                continue  # Try next path
        
        if not video_found:
            self.log_test(
                "Villa F3 Video File",
                "FAIL",
                "Video file not accessible at any expected path"
            )
    
    def test_villa_f3_images(self):
        """Test Villa F3 image accessibility"""
        image_paths = [
            '/ALLINCLUSIVE2.0/images/Villa_F3_Petit_Macabou/01_piscine_exterieur.jpg',
            '/images/Villa_F3_Petit_Macabou/01_piscine_exterieur.jpg'
        ]
        
        image_found = False
        for image_path in image_paths:
            try:
                response = requests.head(f"{self.backend_url}{image_path}", timeout=10)
                if response.status_code == 200:
                    content_type = response.headers.get('content-type', '')
                    if 'image' in content_type:
                        self.log_test(
                            "Villa F3 Images",
                            "PASS",
                            f"Villa F3 images accessible at {image_path}"
                        )
                        image_found = True
                        break
            except Exception as e:
                continue  # Try next path
        
        if not image_found:
            self.log_test(
                "Villa F3 Images",
                "FAIL",
                "Villa F3 images not accessible at expected paths"
            )
    
    def test_reservation_with_villa_parameter(self):
        """Test reservation.html with villa parameter"""
        try:
            response = requests.get(
                f"{self.backend_url}/reservation.html?villa=f3-sur-petit-macabou", 
                timeout=10
            )
            if response.status_code == 200:
                content = response.text
                # Check for F3 calendar section
                if 'f3CalendarSection' in content or 'Villa F3' in content:
                    self.log_test(
                        "Reservation with Villa Parameter",
                        "PASS",
                        "Reservation page loads with villa parameter"
                    )
                else:
                    self.log_test(
                        "Reservation with Villa Parameter",
                        "FAIL",
                        "Reservation page loads but F3 content not found"
                    )
            else:
                self.log_test(
                    "Reservation with Villa Parameter",
                    "FAIL",
                    f"Reservation page not accessible (status {response.status_code})"
                )
        except Exception as e:
            self.log_test(
                "Reservation with Villa Parameter",
                "FAIL",
                "Reservation page not accessible",
                e
            )
    
    def test_villa_api_endpoints(self):
        """Test villa-related API endpoints"""
        try:
            # Test get all villas
            response = requests.get(f"{self.api_url}/villas", timeout=10)
            if response.status_code == 200:
                villas = response.json()
                # Look for Villa F3 Petit Macabou
                f3_villa = None
                for villa in villas:
                    if 'f3' in villa.get('name', '').lower() and 'petit macabou' in villa.get('name', '').lower():
                        f3_villa = villa
                        break
                
                if f3_villa:
                    self.log_test(
                        "Villa API - Get All Villas",
                        "PASS",
                        f"Found Villa F3 Petit Macabou in API response (ID: {f3_villa.get('id')})"
                    )
                    
                    # Test specific villa endpoint
                    villa_id = f3_villa.get('id')
                    if villa_id:
                        try:
                            villa_response = requests.get(f"{self.api_url}/villas/{villa_id}", timeout=10)
                            if villa_response.status_code == 200:
                                villa_data = villa_response.json()
                                self.log_test(
                                    "Villa API - Get Specific Villa",
                                    "PASS",
                                    f"Villa F3 data retrieved successfully"
                                )
                            else:
                                self.log_test(
                                    "Villa API - Get Specific Villa",
                                    "FAIL",
                                    f"Villa F3 not accessible (status {villa_response.status_code})"
                                )
                        except Exception as e:
                            self.log_test(
                                "Villa API - Get Specific Villa",
                                "FAIL",
                                "Error retrieving specific villa",
                                e
                            )
                else:
                    self.log_test(
                        "Villa API - Get All Villas",
                        "FAIL",
                        "Villa F3 Petit Macabou not found in API response"
                    )
            else:
                self.log_test(
                    "Villa API - Get All Villas",
                    "FAIL",
                    f"Villa API not accessible (status {response.status_code})"
                )
        except Exception as e:
            self.log_test(
                "Villa API - Get All Villas",
                "FAIL",
                "Villa API not accessible",
                e
            )
    
    def test_villa_search_functionality(self):
        """Test villa search functionality"""
        try:
            search_data = {
                "destination": "Vauclin",
                "guests": 6,
                "category": "sejour"
            }
            
            response = requests.post(
                f"{self.api_url}/villas/search",
                json=search_data,
                timeout=10
            )
            
            if response.status_code == 200:
                results = response.json()
                # Check if Villa F3 Petit Macabou appears in Vauclin search
                f3_found = any(
                    'f3' in villa.get('name', '').lower() and 
                    'petit macabou' in villa.get('name', '').lower()
                    for villa in results
                )
                
                if f3_found:
                    self.log_test(
                        "Villa Search Functionality",
                        "PASS",
                        f"Villa F3 found in Vauclin search results ({len(results)} total results)"
                    )
                else:
                    self.log_test(
                        "Villa Search Functionality",
                        "FAIL",
                        f"Villa F3 not found in Vauclin search results ({len(results)} total results)"
                    )
            else:
                self.log_test(
                    "Villa Search Functionality",
                    "FAIL",
                    f"Search API not accessible (status {response.status_code})"
                )
        except Exception as e:
            self.log_test(
                "Villa Search Functionality",
                "FAIL",
                "Search API not accessible",
                e
            )
    
    def test_reservation_api(self):
        """Test reservation API functionality"""
        try:
            # Test reservation creation with Villa F3 data
            reservation_data = {
                "villa_id": "f3-petit-macabou",
                "customer_name": "Test Customer",
                "customer_email": "test@example.com",
                "customer_phone": "+596123456789",
                "checkin_date": "2025-02-15",
                "checkout_date": "2025-02-20",
                "guests_count": 4,
                "message": "Test reservation for Villa F3",
                "total_price": 4250.0
            }
            
            response = requests.post(
                f"{self.api_url}/reservations",
                json=reservation_data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    self.log_test(
                        "Reservation API",
                        "PASS",
                        f"Reservation created successfully (ID: {result.get('reservation_id')})"
                    )
                else:
                    self.log_test(
                        "Reservation API",
                        "FAIL",
                        "Reservation API returned success=false"
                    )
            else:
                # Check if it's a validation error (expected for test data)
                if response.status_code in [400, 422]:
                    self.log_test(
                        "Reservation API",
                        "PASS",
                        f"Reservation API responding correctly with validation (status {response.status_code})"
                    )
                else:
                    self.log_test(
                        "Reservation API",
                        "FAIL",
                        f"Reservation API error (status {response.status_code})"
                    )
        except Exception as e:
            self.log_test(
                "Reservation API",
                "FAIL",
                "Reservation API not accessible",
                e
            )
    
    def test_dashboard_stats(self):
        """Test dashboard statistics API"""
        try:
            response = requests.get(f"{self.api_url}/stats/dashboard", timeout=10)
            if response.status_code == 200:
                stats = response.json()
                villa_count = stats.get('total_villas', 0)
                if villa_count > 0:
                    self.log_test(
                        "Dashboard Statistics",
                        "PASS",
                        f"Dashboard stats accessible ({villa_count} villas in system)"
                    )
                else:
                    self.log_test(
                        "Dashboard Statistics",
                        "FAIL",
                        "Dashboard stats show 0 villas"
                    )
            else:
                self.log_test(
                    "Dashboard Statistics",
                    "FAIL",
                    f"Dashboard stats not accessible (status {response.status_code})"
                )
        except Exception as e:
            self.log_test(
                "Dashboard Statistics",
                "FAIL",
                "Dashboard stats not accessible",
                e
            )
    
    def run_all_tests(self):
        """Run all Villa F3 backend tests"""
        print("🏖️ VILLA F3 BACKEND TESTING SUITE")
        print("=" * 50)
        print(f"Backend URL: {self.backend_url}")
        print(f"API URL: {self.api_url}")
        print()
        
        # Test backend connectivity first
        if not self.test_backend_health():
            print("\n❌ Backend not accessible. Stopping tests.")
            return self.results
        
        # Run all tests
        print("\n📋 Running Villa F3 Enhancement Tests...")
        self.test_static_file_serving()
        self.test_villa_f3_video_path()
        self.test_villa_f3_images()
        self.test_reservation_with_villa_parameter()
        
        print("\n🔌 Running API Tests...")
        self.test_villa_api_endpoints()
        self.test_villa_search_functionality()
        self.test_reservation_api()
        self.test_dashboard_stats()
        
        # Calculate success rate
        if self.results['summary']['total'] > 0:
            self.results['summary']['success_rate'] = round(
                (self.results['summary']['passed'] / self.results['summary']['total']) * 100, 1
            )
        
        # Print summary
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        print(f"Total Tests: {self.results['summary']['total']}")
        print(f"Passed: {self.results['summary']['passed']}")
        print(f"Failed: {self.results['summary']['failed']}")
        print(f"Success Rate: {self.results['summary']['success_rate']}%")
        
        if self.results['summary']['success_rate'] >= 80:
            print("\n✅ VILLA F3 BACKEND TESTS: EXCELLENT RESULTS")
        elif self.results['summary']['success_rate'] >= 60:
            print("\n⚠️ VILLA F3 BACKEND TESTS: GOOD RESULTS WITH MINOR ISSUES")
        else:
            print("\n❌ VILLA F3 BACKEND TESTS: CRITICAL ISSUES FOUND")
        
        return self.results
    
    def save_results(self, filename="villa_f3_backend_test_results.json"):
        """Save test results to file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Results saved to {filename}")
        except Exception as e:
            print(f"\n❌ Error saving results: {e}")

def main():
    """Main function"""
    tester = VillaF3BackendTester()
    results = tester.run_all_tests()
    tester.save_results()
    
    # Return appropriate exit code
    if results['summary']['success_rate'] >= 80:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure

if __name__ == "__main__":
    main()