#!/usr/bin/env python3
"""
KhanelConcept Villa Data Integration Testing
Focus: Testing villa data integration as requested in review request

CRITICAL TESTING AREAS:
1. Villa API Endpoints - Test that all villa endpoints return correct integrated data
2. CSV Data Integration - Verify villa data from CSV has been properly integrated
3. Image Serving - Test villa images are served correctly from /app/images/
4. Villa Detail Consistency - Check villa detail pages have accurate data
5. Database Integrity - Verify villa database contains correct integrated data

SPECIFIC ENDPOINTS TO TEST:
- GET /api/villas (should return all 21+ villas with integrated data)
- GET /api/admin/villas (admin villa management)
- Villa search functionality
- Villa-specific data retrieval
"""

import requests
import json
import sys
from datetime import datetime

# Configuration - Use external URL for production testing
BASE_URL = "https://static-site-restore.preview.emergentagent.com"
API_BASE = f"{BASE_URL}/api"

class VillaIntegrationTester:
    def __init__(self):
        self.passed_tests = 0
        self.failed_tests = 0
        self.test_results = []
        self.admin_token = None
        
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
        """Test API health and connectivity"""
        try:
            response = requests.get(f"{API_BASE}/health", timeout=10)
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
    
    def test_admin_authentication(self):
        """Test admin authentication for protected endpoints"""
        try:
            login_data = {
                "username": "admin",
                "password": "khanelconcept2025"
            }
            
            response = requests.post(f"{API_BASE}/admin/login", json=login_data, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data:
                    self.admin_token = data["access_token"]
                    self.log_test(
                        "Admin Authentication",
                        True,
                        "Admin login successful, token obtained"
                    )
                    return True
                else:
                    self.log_test(
                        "Admin Authentication",
                        False,
                        "Login response missing access token"
                    )
                    return False
            else:
                self.log_test(
                    "Admin Authentication",
                    False,
                    f"Admin login failed: {response.status_code}"
                )
                return False
        except Exception as e:
            self.log_test(
                "Admin Authentication",
                False,
                f"Authentication error: {str(e)}"
            )
            return False
    
    def test_villa_api_endpoints(self):
        """Test 1: Villa API Endpoints - GET /api/villas returns all villas with integrated data"""
        try:
            response = requests.get(f"{API_BASE}/villas", timeout=10)
            if response.status_code != 200:
                self.log_test(
                    "Villa API Endpoints",
                    False,
                    f"API error: {response.status_code}"
                )
                return False
            
            villas = response.json()
            villa_count = len(villas)
            
            # Check if we have 21+ villas as expected
            if villa_count >= 21:
                self.log_test(
                    "Villa API Endpoints - Count",
                    True,
                    f"Found {villa_count} villas (expected 21+)"
                )
            else:
                self.log_test(
                    "Villa API Endpoints - Count",
                    False,
                    f"Only {villa_count} villas found (expected 21+)"
                )
                return False
            
            # Verify data structure
            required_fields = ['id', 'name', 'location', 'price', 'guests', 'category', 'image', 'gallery']
            missing_fields = []
            
            for villa in villas[:3]:  # Check first 3 villas
                for field in required_fields:
                    if field not in villa:
                        missing_fields.append(f"{villa.get('name', 'Unknown')}: {field}")
            
            if not missing_fields:
                self.log_test(
                    "Villa API Endpoints - Data Structure",
                    True,
                    "All required fields present in villa data"
                )
            else:
                self.log_test(
                    "Villa API Endpoints - Data Structure",
                    False,
                    f"Missing fields: {', '.join(missing_fields)}"
                )
            
            return villas
            
        except Exception as e:
            self.log_test(
                "Villa API Endpoints",
                False,
                f"Error retrieving villas: {str(e)}"
            )
            return False
    
    def test_csv_data_integration(self, villas):
        """Test 2: CSV Data Integration - Verify villa data from CSV has been properly integrated"""
        if not villas:
            self.log_test(
                "CSV Data Integration",
                False,
                "No villa data available for testing"
            )
            return False
        
        # Check for CSV integration indicators
        csv_integrated_count = 0
        pricing_details_count = 0
        services_full_count = 0
        guests_detail_count = 0
        
        for villa in villas:
            # Check csv_integrated flag
            if villa.get('csv_integrated'):
                csv_integrated_count += 1
            
            # Check pricing_details from CSV
            if villa.get('pricing_details') and isinstance(villa.get('pricing_details'), dict):
                pricing_details_count += 1
            
            # Check services_full from CSV
            if villa.get('services_full'):
                services_full_count += 1
            
            # Check guests_detail from CSV
            if villa.get('guests_detail'):
                guests_detail_count += 1
        
        total_villas = len(villas)
        
        # Test CSV integration flags
        if csv_integrated_count >= total_villas * 0.8:  # At least 80%
            self.log_test(
                "CSV Data Integration - Flags",
                True,
                f"{csv_integrated_count}/{total_villas} villas have csv_integrated flag"
            )
        else:
            self.log_test(
                "CSV Data Integration - Flags",
                False,
                f"Only {csv_integrated_count}/{total_villas} villas have csv_integrated flag"
            )
        
        # Test pricing details integration
        if pricing_details_count >= total_villas * 0.7:  # At least 70%
            self.log_test(
                "CSV Data Integration - Pricing Details",
                True,
                f"{pricing_details_count}/{total_villas} villas have pricing_details"
            )
        else:
            self.log_test(
                "CSV Data Integration - Pricing Details",
                False,
                f"Only {pricing_details_count}/{total_villas} villas have pricing_details"
            )
        
        return csv_integrated_count >= total_villas * 0.8
    
    def test_admin_villa_management(self):
        """Test 3: Admin Villa Management - GET /api/admin/villas"""
        if not self.admin_token:
            self.log_test(
                "Admin Villa Management",
                False,
                "No admin token available for testing"
            )
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = requests.get(f"{API_BASE}/admin/villas", headers=headers, timeout=10)
            
            if response.status_code != 200:
                self.log_test(
                    "Admin Villa Management",
                    False,
                    f"Admin villa endpoint error: {response.status_code}"
                )
                return False
            
            admin_villas = response.json()
            
            if len(admin_villas) >= 21:
                self.log_test(
                    "Admin Villa Management",
                    True,
                    f"Admin endpoint returns {len(admin_villas)} villas with proper structure"
                )
                return True
            else:
                self.log_test(
                    "Admin Villa Management",
                    False,
                    f"Admin endpoint only returns {len(admin_villas)} villas (expected 21+)"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Admin Villa Management",
                False,
                f"Error testing admin villas: {str(e)}"
            )
            return False
    
    def test_villa_search_functionality(self):
        """Test 4: Villa Search Functionality"""
        try:
            # Test search by destination
            search_data = {"destination": "Vauclin"}
            response = requests.post(f"{API_BASE}/villas/search", json=search_data, timeout=10)
            
            if response.status_code == 200:
                vauclin_results = response.json()
                self.log_test(
                    "Villa Search - Destination",
                    True,
                    f"Destination search working: found {len(vauclin_results)} villas in Vauclin"
                )
            else:
                self.log_test(
                    "Villa Search - Destination",
                    False,
                    f"Destination search failed: {response.status_code}"
                )
                return False
            
            # Test search by guests
            search_data = {"guests": 6}
            response = requests.post(f"{API_BASE}/villas/search", json=search_data, timeout=10)
            
            if response.status_code == 200:
                guest_results = response.json()
                self.log_test(
                    "Villa Search - Guests",
                    True,
                    f"Guest search working: found {len(guest_results)} villas for 6+ guests"
                )
            else:
                self.log_test(
                    "Villa Search - Guests",
                    False,
                    f"Guest search failed: {response.status_code}"
                )
                return False
            
            # Test search by category
            search_data = {"category": "sejour"}
            response = requests.post(f"{API_BASE}/villas/search", json=search_data, timeout=10)
            
            if response.status_code == 200:
                category_results = response.json()
                self.log_test(
                    "Villa Search - Category",
                    True,
                    f"Category search working: found {len(category_results)} 'sejour' villas"
                )
            else:
                self.log_test(
                    "Villa Search - Category",
                    False,
                    f"Category search failed: {response.status_code}"
                )
                return False
            
            return True
            
        except Exception as e:
            self.log_test(
                "Villa Search Functionality",
                False,
                f"Error testing search: {str(e)}"
            )
            return False
    
    def test_villa_detail_consistency(self, villas):
        """Test 5: Villa Detail Consistency - Check key villas have accurate data"""
        if not villas:
            self.log_test(
                "Villa Detail Consistency",
                False,
                "No villa data available for testing"
            )
            return False
        
        # Test key villas mentioned in previous tests
        key_villas_to_check = [
            {"pattern": "F3", "location": "Petit Macabou", "expected_price": 850},
            {"pattern": "F5", "location": "Ste Anne", "expected_price": 1350},
            {"pattern": "F6", "location": "Petit Macabou", "expected_price": 2000},
            {"pattern": "Espace Piscine", "location": "", "expected_price": 350}
        ]
        
        found_key_villas = 0
        pricing_matches = 0
        
        for key_villa in key_villas_to_check:
            found = False
            for villa in villas:
                villa_name = villa.get('name', '').lower()
                villa_location = villa.get('location', '').lower()
                villa_price = villa.get('price', 0)
                
                if (key_villa["pattern"].lower() in villa_name and 
                    (not key_villa["location"] or key_villa["location"].lower() in villa_location)):
                    found = True
                    found_key_villas += 1
                    
                    if villa_price == key_villa["expected_price"]:
                        pricing_matches += 1
                        self.log_test(
                            f"Villa Detail - {key_villa['pattern']}",
                            True,
                            f"Found with correct price: €{villa_price}"
                        )
                    else:
                        self.log_test(
                            f"Villa Detail - {key_villa['pattern']}",
                            False,
                            f"Price mismatch: €{villa_price} (expected €{key_villa['expected_price']})"
                        )
                    break
            
            if not found:
                self.log_test(
                    f"Villa Detail - {key_villa['pattern']}",
                    False,
                    "Key villa not found in database"
                )
        
        # Overall consistency check
        if found_key_villas >= 3 and pricing_matches >= 2:
            self.log_test(
                "Villa Detail Consistency - Overall",
                True,
                f"Found {found_key_villas}/4 key villas, {pricing_matches} with correct pricing"
            )
            return True
        else:
            self.log_test(
                "Villa Detail Consistency - Overall",
                False,
                f"Only found {found_key_villas}/4 key villas, {pricing_matches} with correct pricing"
            )
            return False
    
    def test_database_integrity(self):
        """Test 6: Database Integrity - Verify villa database contains correct integrated data"""
        try:
            # Test dashboard stats
            stats_response = requests.get(f"{API_BASE}/stats/dashboard", timeout=10)
            if stats_response.status_code == 200:
                stats = stats_response.json()
                total_villas_stats = stats.get('total_villas', 0)
                
                if total_villas_stats >= 21:
                    self.log_test(
                        "Database Integrity - Stats",
                        True,
                        f"Dashboard stats show {total_villas_stats} villas"
                    )
                else:
                    self.log_test(
                        "Database Integrity - Stats",
                        False,
                        f"Dashboard stats show only {total_villas_stats} villas (expected 21+)"
                    )
                    return False
            else:
                self.log_test(
                    "Database Integrity - Stats",
                    False,
                    f"Dashboard stats endpoint failed: {stats_response.status_code}"
                )
                return False
            
            return True
            
        except Exception as e:
            self.log_test(
                "Database Integrity",
                False,
                f"Error testing database integrity: {str(e)}"
            )
            return False
    
    def run_comprehensive_villa_integration_tests(self):
        """Run all villa data integration tests"""
        print("🏖️ KHANELCONCEPT VILLA DATA INTEGRATION TESTING")
        print("=" * 80)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print(f"Backend URL: {BASE_URL}")
        print()
        
        # Test 0: Health check
        if not self.test_api_health():
            print("❌ API not accessible, stopping tests")
            return False
        
        print()
        
        # Test admin authentication
        if not self.test_admin_authentication():
            print("⚠️ Admin authentication failed, some tests will be skipped")
        
        print()
        
        # Test 1: Villa API Endpoints
        villas = self.test_villa_api_endpoints()
        if not villas:
            print("❌ Cannot retrieve villa data, stopping tests")
            return False
        
        print()
        
        # Test 2: CSV Data Integration
        self.test_csv_data_integration(villas)
        
        print()
        
        # Test 3: Admin Villa Management
        self.test_admin_villa_management()
        
        print()
        
        # Test 4: Villa Search Functionality
        self.test_villa_search_functionality()
        
        print()
        
        # Test 5: Villa Detail Consistency
        self.test_villa_detail_consistency(villas)
        
        print()
        
        # Test 6: Database Integrity
        self.test_database_integrity()
        
        print()
        print("=" * 80)
        print("📊 VILLA DATA INTEGRATION TEST RESULTS")
        print("=" * 80)
        
        total_tests = self.passed_tests + self.failed_tests
        success_rate = (self.passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"✅ Tests passed: {self.passed_tests}")
        print(f"❌ Tests failed: {self.failed_tests}")
        print(f"📈 Success rate: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("🎉 EXCELLENT - Villa data integration is working perfectly!")
        elif success_rate >= 75:
            print("✅ GOOD - Most villa integration features are working")
        elif success_rate >= 50:
            print("⚠️ MODERATE - Some villa integration issues need attention")
        else:
            print("❌ CRITICAL - Villa data integration needs immediate attention")
        
        print()
        
        # Summary of critical issues
        critical_issues = []
        for result in self.test_results:
            if not result["passed"] and any(keyword in result["test"].lower() 
                                          for keyword in ["villa api", "csv data", "database integrity"]):
                critical_issues.append(result["test"])
        
        if critical_issues:
            print("🚨 CRITICAL ISSUES IDENTIFIED:")
            for issue in critical_issues:
                print(f"   - {issue}")
        else:
            print("✅ No critical villa integration issues identified")
        
        return success_rate >= 75

def main():
    """Main entry point"""
    tester = VillaIntegrationTester()
    success = tester.run_comprehensive_villa_integration_tests()
    
    # Save results
    with open('/app/villa_integration_test_results.json', 'w', encoding='utf-8') as f:
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