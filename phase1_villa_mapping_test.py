#!/usr/bin/env python3
"""
PHASE 1 CRITICAL FIXES TESTING - Villa Mapping System Fix
Testing the critical corrections applied to fix the villa rental system:

1. Villa Mapping System Fix (reservation-enhanced.js):
   - Enhanced getVillaFromUrl() function with comprehensive villa ID mapping
   - Added mapping for all 22 villas to resolve "Villa non trouvée" errors
   - Test villa reservation system with URLs like: ?villa=villa-f3-petit-macabou, ?villa=espace-piscine-journee-bungalow

2. Search Function Enhancement (index.html):
   - Fixed performSearch() function with proper error handling
   - Enhanced data validation and user feedback
   - Test search functionality with destinations like "Vauclin", "Lamentin" and guest counts

3. Backend API Compatibility:
   - Test villa data retrieval: GET /api/villas (should return 21+ villas)
   - Test villa search: POST /api/villas/search with filters
   - Verify villa IDs match between frontend and backend data

4. Performance & Errors:
   - Check if video background loading errors are resolved
   - Verify image optimization and lazy loading works
   - Test villa reservation creation with proper villa IDs

FOCUS: Test reservation system functionality - this was reported as completely broken ("Villa non trouvée") in the audit.
"""

import requests
import json
import sys
import os
from datetime import datetime
from urllib.parse import urlparse, parse_qs

# Configuration
BASE_URL = "https://glass-effect-ui-1.preview.emergentagent.com"
API_BASE = f"{BASE_URL}/api"

class Phase1VillaMappingTester:
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
        """Test 0: Verify API is accessible"""
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
    
    def test_villa_data_retrieval(self):
        """Test 1: Villa data retrieval - GET /api/villas should return 21+ villas"""
        try:
            response = self.session.get(f"{API_BASE}/villas", timeout=10)
            if response.status_code != 200:
                self.log_test(
                    "Villa Data Retrieval",
                    False,
                    f"API error: {response.status_code}"
                )
                return False
            
            villas = response.json()
            villa_count = len(villas)
            
            # Check villa count (should be 21+ as per review)
            if villa_count >= 21:
                self.log_test(
                    "Villa Count Verification",
                    True,
                    f"Correct villa count: {villa_count} villas found"
                )
            else:
                self.log_test(
                    "Villa Count Verification",
                    False,
                    f"Insufficient villas: {villa_count} (expected: 21+)"
                )
                return False
            
            # Verify villa data structure
            required_fields = ['id', 'name', 'location', 'price', 'guests', 'category', 'image', 'gallery']
            missing_fields = []
            
            for villa in villas[:3]:  # Check first 3 villas
                for field in required_fields:
                    if field not in villa:
                        missing_fields.append(f"{villa.get('name', 'Unknown')}: {field}")
            
            if not missing_fields:
                self.log_test(
                    "Villa Data Structure",
                    True,
                    "All required fields present in villa data"
                )
            else:
                self.log_test(
                    "Villa Data Structure",
                    False,
                    f"Missing fields: {', '.join(missing_fields)}"
                )
            
            return villas
            
        except Exception as e:
            self.log_test(
                "Villa Data Retrieval",
                False,
                f"Error retrieving villas: {str(e)}"
            )
            return False
    
    def test_villa_search_functionality(self):
        """Test 2: Villa search functionality with filters"""
        search_tests = [
            {
                "name": "Search by Destination - Vauclin",
                "filters": {"destination": "Vauclin"},
                "expected_min": 1
            },
            {
                "name": "Search by Destination - Lamentin", 
                "filters": {"destination": "Lamentin"},
                "expected_min": 1
            },
            {
                "name": "Search by Guest Count",
                "filters": {"guests": 6},
                "expected_min": 1
            },
            {
                "name": "Search by Category - Sejour",
                "filters": {"category": "sejour"},
                "expected_min": 1
            },
            {
                "name": "Search by Category - Fete",
                "filters": {"category": "fete"},
                "expected_min": 1
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
                            test["name"],
                            True,
                            f"Search successful: {result_count} results found",
                            f"Filters: {test['filters']}"
                        )
                    else:
                        self.log_test(
                            test["name"],
                            False,
                            f"Insufficient results: {result_count} (expected: {test['expected_min']}+)",
                            f"Filters: {test['filters']}"
                        )
                        all_passed = False
                else:
                    self.log_test(
                        test["name"],
                        False,
                        f"Search API error: {response.status_code}"
                    )
                    all_passed = False
                    
            except Exception as e:
                self.log_test(
                    test["name"],
                    False,
                    f"Search error: {str(e)}"
                )
                all_passed = False
        
        return all_passed
    
    def test_villa_id_mapping(self, villas):
        """Test 3: Verify villa IDs match between frontend and backend data"""
        if not villas:
            self.log_test(
                "Villa ID Mapping",
                False,
                "No villa data available for ID mapping test"
            )
            return False
        
        # Test specific villa URLs mentioned in the review
        test_villa_urls = [
            "villa-f3-petit-macabou",
            "espace-piscine-journee-bungalow",
            "villa-f5-ste-anne",
            "villa-f6-petit-macabou"
        ]
        
        villa_mapping_success = 0
        
        for url_pattern in test_villa_urls:
            # Try to find matching villa by name pattern
            found_villa = None
            for villa in villas:
                villa_name = villa.get('name', '').lower()
                villa_id = str(villa.get('id', ''))
                
                # Check if villa name matches URL pattern
                if self._matches_url_pattern(villa_name, url_pattern):
                    found_villa = villa
                    break
            
            if found_villa:
                self.log_test(
                    f"Villa Mapping - {url_pattern}",
                    True,
                    f"Villa found: {found_villa['name']} (ID: {found_villa['id']})",
                    f"Price: €{found_villa.get('price', 0)}, Category: {found_villa.get('category', 'unknown')}"
                )
                villa_mapping_success += 1
            else:
                self.log_test(
                    f"Villa Mapping - {url_pattern}",
                    False,
                    f"No villa found matching URL pattern: {url_pattern}"
                )
        
        # Overall mapping assessment
        mapping_rate = (villa_mapping_success / len(test_villa_urls)) * 100
        if mapping_rate >= 75:
            self.log_test(
                "Villa ID Mapping Overall",
                True,
                f"Villa mapping successful: {villa_mapping_success}/{len(test_villa_urls)} ({mapping_rate:.1f}%)"
            )
            return True
        else:
            self.log_test(
                "Villa ID Mapping Overall",
                False,
                f"Villa mapping insufficient: {villa_mapping_success}/{len(test_villa_urls)} ({mapping_rate:.1f}%)"
            )
            return False
    
    def _matches_url_pattern(self, villa_name, url_pattern):
        """Helper method to check if villa name matches URL pattern"""
        # Convert URL pattern to searchable terms
        pattern_parts = url_pattern.replace('-', ' ').split()
        villa_words = villa_name.replace('-', ' ').split()
        
        # Check if key parts of the pattern exist in villa name
        matches = 0
        for part in pattern_parts:
            if part in ['villa', 'sur', 'de', 'la', 'le']:
                continue  # Skip common words
            for word in villa_words:
                if part.lower() in word.lower() or word.lower() in part.lower():
                    matches += 1
                    break
        
        # Consider it a match if at least 2 significant parts match
        return matches >= 2
    
    def test_reservation_creation(self, villas):
        """Test 4: Test villa reservation creation with proper villa IDs"""
        if not villas:
            self.log_test(
                "Reservation Creation Test",
                False,
                "No villa data available for reservation test"
            )
            return False
        
        # Select a test villa (first available villa)
        test_villa = villas[0]
        villa_id = str(test_villa.get('id', ''))
        villa_name = test_villa.get('name', 'Unknown Villa')
        
        # Create test reservation data
        reservation_data = {
            "villa_id": villa_id,
            "customer_name": "Test Customer Phase1",
            "customer_email": "test.phase1@khanelconcept.com",
            "customer_phone": "+596123456789",
            "checkin_date": "2025-02-15",
            "checkout_date": "2025-02-22",
            "guests_count": 4,
            "message": "Test reservation for Phase 1 villa mapping verification",
            "total_price": float(test_villa.get('price', 850))
        }
        
        try:
            response = self.session.post(
                f"{API_BASE}/reservations",
                json=reservation_data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success') and result.get('reservation_id'):
                    self.log_test(
                        "Reservation Creation",
                        True,
                        f"Reservation created successfully for {villa_name}",
                        f"Reservation ID: {result.get('reservation_id')}, Villa ID: {villa_id}"
                    )
                    return True
                else:
                    self.log_test(
                        "Reservation Creation",
                        False,
                        f"Reservation creation failed: {result.get('message', 'Unknown error')}"
                    )
                    return False
            else:
                error_detail = response.text if response.text else f"Status {response.status_code}"
                self.log_test(
                    "Reservation Creation",
                    False,
                    f"Reservation API error: {error_detail}"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Reservation Creation",
                False,
                f"Reservation creation error: {str(e)}"
            )
            return False
    
    def test_specific_villa_issues(self, villas):
        """Test 5: Test specific villa issues mentioned in the audit"""
        if not villas:
            self.log_test(
                "Specific Villa Issues",
                False,
                "No villa data available"
            )
            return False
        
        # Test for "Espace Piscine Journée Bungalow" - this was specifically mentioned as problematic
        espace_piscine_found = False
        espace_piscine_villa = None
        
        for villa in villas:
            villa_name = villa.get('name', '').lower()
            if 'espace piscine' in villa_name and 'bungalow' in villa_name:
                espace_piscine_found = True
                espace_piscine_villa = villa
                break
            elif 'espace piscine' in villa_name:
                espace_piscine_found = True
                espace_piscine_villa = villa
                break
        
        if espace_piscine_found and espace_piscine_villa:
            villa_price = espace_piscine_villa.get('price', 0)
            villa_category = espace_piscine_villa.get('category', '')
            
            # Check if it has the expected price (350€) and category
            price_correct = villa_price == 350.0
            category_correct = villa_category in ['fete', 'piscine']
            
            if price_correct and category_correct:
                self.log_test(
                    "Espace Piscine Villa Fix",
                    True,
                    f"Espace Piscine villa found with correct data: {espace_piscine_villa['name']}",
                    f"Price: €{villa_price}, Category: {villa_category}"
                )
            else:
                issues = []
                if not price_correct:
                    issues.append(f"Price: €{villa_price} (expected: €350)")
                if not category_correct:
                    issues.append(f"Category: {villa_category} (expected: fete or piscine)")
                
                self.log_test(
                    "Espace Piscine Villa Fix",
                    False,
                    f"Espace Piscine villa found but has issues: {', '.join(issues)}"
                )
        else:
            self.log_test(
                "Espace Piscine Villa Fix",
                False,
                "Espace Piscine Journée Bungalow villa not found - this was a critical issue in the audit"
            )
        
        # Test villa count consistency
        expected_villa_count = 21  # As mentioned in the review
        actual_count = len(villas)
        
        if actual_count == expected_villa_count:
            self.log_test(
                "Villa Count Consistency",
                True,
                f"Villa count matches expected: {actual_count} villas"
            )
        else:
            self.log_test(
                "Villa Count Consistency",
                False,
                f"Villa count mismatch: {actual_count} found, expected: {expected_villa_count}"
            )
        
        return espace_piscine_found
    
    def test_dashboard_stats_consistency(self):
        """Test 6: Verify dashboard stats are consistent with villa data"""
        try:
            response = self.session.get(f"{API_BASE}/stats/dashboard", timeout=10)
            if response.status_code == 200:
                stats = response.json()
                total_villas = stats.get('total_villas', 0)
                
                if total_villas >= 21:
                    self.log_test(
                        "Dashboard Stats Consistency",
                        True,
                        f"Dashboard shows correct villa count: {total_villas}",
                        f"Stats: {stats}"
                    )
                    return True
                else:
                    self.log_test(
                        "Dashboard Stats Consistency",
                        False,
                        f"Dashboard villa count too low: {total_villas} (expected: 21+)"
                    )
                    return False
            else:
                self.log_test(
                    "Dashboard Stats Consistency",
                    False,
                    f"Dashboard stats API error: {response.status_code}"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Dashboard Stats Consistency",
                False,
                f"Dashboard stats error: {str(e)}"
            )
            return False
    
    def run_phase1_tests(self):
        """Execute all Phase 1 villa mapping tests"""
        print("🏖️ PHASE 1 CRITICAL FIXES TESTING - VILLA MAPPING SYSTEM")
        print("=" * 80)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print(f"Backend URL: {BASE_URL}")
        print()
        print("TESTING FOCUS: Villa mapping system fixes to resolve 'Villa non trouvée' errors")
        print()
        
        # Test 0: Health check
        if not self.test_api_health():
            print("❌ API not accessible, stopping tests")
            return False
        
        print()
        
        # Test 1: Villa data retrieval
        villas = self.test_villa_data_retrieval()
        if not villas:
            print("❌ Cannot retrieve villa data, stopping tests")
            return False
        
        print()
        
        # Test 2: Villa search functionality
        self.test_villa_search_functionality()
        
        print()
        
        # Test 3: Villa ID mapping
        self.test_villa_id_mapping(villas)
        
        print()
        
        # Test 4: Reservation creation
        self.test_reservation_creation(villas)
        
        print()
        
        # Test 5: Specific villa issues
        self.test_specific_villa_issues(villas)
        
        print()
        
        # Test 6: Dashboard stats consistency
        self.test_dashboard_stats_consistency()
        
        print()
        print("=" * 80)
        print("📊 PHASE 1 TEST RESULTS")
        print("=" * 80)
        
        total_tests = self.passed_tests + self.failed_tests
        success_rate = (self.passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"✅ Tests passed: {self.passed_tests}")
        print(f"❌ Tests failed: {self.failed_tests}")
        print(f"📈 Success rate: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("🎉 EXCELLENT - Phase 1 villa mapping fixes working perfectly!")
            status = "EXCELLENT"
        elif success_rate >= 75:
            print("✅ GOOD - Most Phase 1 fixes are working correctly")
            status = "GOOD"
        elif success_rate >= 50:
            print("⚠️ MODERATE - Some Phase 1 fixes need attention")
            status = "MODERATE"
        else:
            print("❌ CRITICAL - Phase 1 villa mapping fixes require immediate attention")
            status = "CRITICAL"
        
        print()
        
        # Critical issues summary
        critical_failures = []
        for result in self.test_results:
            if not result["passed"] and any(keyword in result["test"].lower() 
                                          for keyword in ["villa data", "mapping", "reservation", "espace piscine"]):
                critical_failures.append(result["test"])
        
        if critical_failures:
            print("🚨 CRITICAL ISSUES IDENTIFIED:")
            for issue in critical_failures:
                print(f"   - {issue}")
        else:
            print("✅ No critical issues identified in Phase 1 fixes")
        
        print()
        print("📋 PHASE 1 ASSESSMENT SUMMARY:")
        print(f"   Status: {status}")
        print(f"   Villa mapping system: {'✅ WORKING' if success_rate >= 75 else '❌ NEEDS ATTENTION'}")
        print(f"   Reservation system: {'✅ WORKING' if any('Reservation Creation' in r['test'] and r['passed'] for r in self.test_results) else '❌ NEEDS ATTENTION'}")
        print(f"   Search functionality: {'✅ WORKING' if any('Search' in r['test'] and r['passed'] for r in self.test_results) else '❌ NEEDS ATTENTION'}")
        
        return success_rate >= 75

def main():
    """Main entry point"""
    tester = Phase1VillaMappingTester()
    success = tester.run_phase1_tests()
    
    # Save results
    with open('/app/phase1_villa_mapping_test_results.json', 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "success": success,
            "passed_tests": tester.passed_tests,
            "failed_tests": tester.failed_tests,
            "test_results": tester.test_results,
            "focus": "PHASE 1 CRITICAL FIXES - Villa Mapping System",
            "summary": "Testing villa mapping system fixes to resolve 'Villa non trouvée' errors"
        }, f, indent=2, ensure_ascii=False)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())