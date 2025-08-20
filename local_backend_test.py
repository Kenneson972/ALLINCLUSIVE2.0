#!/usr/bin/env python3
"""
Local Backend API Testing Suite for KhanelConcept
Tests backend running on localhost:8001
"""

import requests
import json
import sys
from datetime import datetime
import time

class LocalBackendTester:
    def __init__(self, base_url="http://localhost:8001"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name, success, message="", response_data=None):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}: PASS - {message}")
        else:
            print(f"❌ {name}: FAIL - {message}")
        
        self.test_results.append({
            "test": name,
            "success": success,
            "message": message,
            "response_data": response_data,
            "timestamp": datetime.now().isoformat()
        })

    def test_basic_connectivity(self):
        """Test basic backend connectivity"""
        print("\n🔍 Testing Basic Connectivity...")
        
        endpoints_to_test = [
            ("/api/v1/health", "V1 Health Check"),
            ("/api/health", "Health Check"),
            ("/api/v1/villas", "V1 Villas"),
            ("/api/villas", "Villas API")
        ]
        
        for endpoint, name in endpoints_to_test:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                if response.status_code == 200:
                    self.log_test(name, True, f"Status: {response.status_code}")
                    if endpoint == "/api/villas":
                        try:
                            data = response.json()
                            self.log_test(f"{name} Data", True, f"Found {len(data)} villas")
                        except:
                            self.log_test(f"{name} Data", False, "Invalid JSON response")
                else:
                    self.log_test(name, False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(name, False, f"Error: {str(e)}")

    def test_static_file_serving(self):
        """Test static file serving"""
        print("\n📁 Testing Static File Serving...")
        
        # Test if the main index.html is served
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            if response.status_code == 200:
                self.log_test("Static Index", True, "Index page served")
            else:
                self.log_test("Static Index", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Static Index", False, f"Error: {str(e)}")

    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting Local Backend API Tests...")
        print(f"Testing against: {self.base_url}")
        print("=" * 50)
        
        start_time = time.time()
        
        # Run test suites
        self.test_basic_connectivity()
        self.test_static_file_serving()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Print summary
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        print(f"Duration: {duration:.2f} seconds")
        
        return self.tests_passed == self.tests_run

def main():
    """Main test execution"""
    tester = LocalBackendTester()
    
    # Run tests
    success = tester.run_all_tests()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())