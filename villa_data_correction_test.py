#!/usr/bin/env python3
"""
KhanelConcept Villa Data Correction Final Verification Test
Focus: Verify that the villa data correction has been successfully applied

Review Requirements:
1. Confirm exactly 21 villas are now present in the system
2. Check that "Espace Piscine Journée Bungalow" exists with €350 pricing
3. Verify all 3 categories are present: sejour (15), fete (5), piscine (1)
4. Confirm key villa pricing:
   - Villa F3 sur Petit Macabou: €850
   - Villa F5 sur Ste Anne: €1350
   - Villa F6 sur Petit Macabou: €2000
   - Espace Piscine Journée Bungalow: €350
"""

import requests
import json
from datetime import datetime
from collections import Counter

# Backend URL configuration
BACKEND_URL = "https://cfc0e6ef-086c-461a-915c-2319466028f1.preview.emergentagent.com"
API_BASE_URL = f"{BACKEND_URL}/api"

class VillaDataCorrectionTester:
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
        print(f"{status}: {test_name}")
        print(f"   {message}")
        if details:
            print(f"   Details: {details}")
        print()
    
    def test_villa_count_exactly_21(self):
        """Test 1: Confirm exactly 21 villas are present"""
        try:
            response = self.session.get(f"{API_BASE_URL}/villas", timeout=10)
            
            if response.status_code != 200:
                self.log_test("Villa Count (21 villas)", False, 
                            f"Could not retrieve villas - HTTP {response.status_code}")
                return False
            
            villas = response.json()
            villa_count = len(villas)
            
            if villa_count == 21:
                self.log_test("Villa Count (21 villas)", True, 
                            f"✅ PERFECT! Exactly 21 villas found as required", 
                            f"Villa count: {villa_count}")
                return True
            else:
                self.log_test("Villa Count (21 villas)", False, 
                            f"❌ Expected exactly 21 villas, found {villa_count}", 
                            f"Villa count mismatch - correction not applied")
                return False
                
        except Exception as e:
            self.log_test("Villa Count (21 villas)", False, f"Error: {str(e)}")
            return False
    
    def test_espace_piscine_villa_exists(self):
        """Test 2: Check that "Espace Piscine Journée Bungalow" exists with €350 pricing"""
        try:
            response = self.session.get(f"{API_BASE_URL}/villas", timeout=10)
            
            if response.status_code != 200:
                self.log_test("Espace Piscine Villa (€350)", False, 
                            f"Could not retrieve villas - HTTP {response.status_code}")
                return False
            
            villas = response.json()
            
            # Search for Espace Piscine villa
            espace_piscine_villa = None
            for villa in villas:
                villa_name = villa.get("name", "").lower()
                if "espace piscine" in villa_name and "journée" in villa_name:
                    espace_piscine_villa = villa
                    break
            
            if espace_piscine_villa:
                villa_price = espace_piscine_villa.get("price", 0)
                villa_name = espace_piscine_villa.get("name", "")
                
                if villa_price == 350.0:
                    self.log_test("Espace Piscine Villa (€350)", True, 
                                f"✅ FOUND! '{villa_name}' with correct €350 pricing", 
                                f"Villa: {villa_name}, Price: €{villa_price}")
                    return True
                else:
                    self.log_test("Espace Piscine Villa (€350)", False, 
                                f"❌ Found '{villa_name}' but price is €{villa_price}, expected €350", 
                                f"Price correction not applied")
                    return False
            else:
                self.log_test("Espace Piscine Villa (€350)", False, 
                            f"❌ 'Espace Piscine Journée Bungalow' NOT FOUND in database", 
                            f"Villa missing - correction not applied")
                return False
                
        except Exception as e:
            self.log_test("Espace Piscine Villa (€350)", False, f"Error: {str(e)}")
            return False
    
    def test_category_distribution(self):
        """Test 3: Verify all 3 categories are present: sejour (15), fete (5), piscine (1)"""
        try:
            response = self.session.get(f"{API_BASE_URL}/villas", timeout=10)
            
            if response.status_code != 200:
                self.log_test("Category Distribution", False, 
                            f"Could not retrieve villas - HTTP {response.status_code}")
                return False
            
            villas = response.json()
            
            # Count categories
            category_counts = Counter()
            for villa in villas:
                category = villa.get("category", "unknown")
                category_counts[category] += 1
            
            # Expected distribution
            expected_distribution = {
                "sejour": 15,
                "fete": 5,
                "piscine": 1
            }
            
            # Check if all required categories exist
            missing_categories = []
            incorrect_counts = []
            
            for category, expected_count in expected_distribution.items():
                actual_count = category_counts.get(category, 0)
                if actual_count == 0:
                    missing_categories.append(category)
                elif actual_count != expected_count:
                    incorrect_counts.append(f"{category}: {actual_count} (expected {expected_count})")
            
            if not missing_categories and not incorrect_counts:
                self.log_test("Category Distribution", True, 
                            f"✅ PERFECT! All 3 categories with correct distribution", 
                            f"sejour: {category_counts['sejour']}, fete: {category_counts['fete']}, piscine: {category_counts['piscine']}")
                return True
            else:
                issues = []
                if missing_categories:
                    issues.append(f"Missing categories: {missing_categories}")
                if incorrect_counts:
                    issues.append(f"Incorrect counts: {incorrect_counts}")
                
                self.log_test("Category Distribution", False, 
                            f"❌ Category distribution issues found", 
                            f"Issues: {'; '.join(issues)}. Actual: {dict(category_counts)}")
                return False
                
        except Exception as e:
            self.log_test("Category Distribution", False, f"Error: {str(e)}")
            return False
    
    def test_key_villa_pricing(self):
        """Test 4: Confirm key villa pricing"""
        try:
            response = self.session.get(f"{API_BASE_URL}/villas", timeout=10)
            
            if response.status_code != 200:
                self.log_test("Key Villa Pricing", False, 
                            f"Could not retrieve villas - HTTP {response.status_code}")
                return False
            
            villas = response.json()
            
            # Expected key villas with pricing
            expected_villas = {
                "Villa F3 sur Petit Macabou": 850.0,
                "Villa F5 sur Ste Anne": 1350.0,
                "Villa F6 sur Petit Macabou": 2000.0,
                "Espace Piscine Journée Bungalow": 350.0
            }
            
            found_villas = {}
            pricing_issues = []
            
            for villa in villas:
                villa_name = villa.get("name", "")
                villa_price = villa.get("price", 0)
                
                # Check each expected villa with flexible matching
                for expected_name, expected_price in expected_villas.items():
                    if self._villa_name_matches(villa_name, expected_name):
                        found_villas[expected_name] = {
                            "actual_name": villa_name,
                            "actual_price": villa_price,
                            "expected_price": expected_price
                        }
                        
                        if villa_price != expected_price:
                            pricing_issues.append(f"{villa_name}: €{villa_price} (expected €{expected_price})")
            
            # Assessment
            found_count = len(found_villas)
            expected_count = len(expected_villas)
            
            if found_count == expected_count and len(pricing_issues) == 0:
                self.log_test("Key Villa Pricing", True, 
                            f"✅ ALL {expected_count} key villas found with correct pricing", 
                            f"Verified: {list(found_villas.keys())}")
                return True
            else:
                missing_villas = [name for name in expected_villas.keys() if name not in found_villas]
                error_details = []
                if missing_villas:
                    error_details.append(f"Missing: {missing_villas}")
                if pricing_issues:
                    error_details.append(f"Pricing issues: {pricing_issues}")
                
                self.log_test("Key Villa Pricing", False, 
                            f"❌ Found {found_count}/{expected_count} key villas, {len(pricing_issues)} pricing issues", 
                            f"Issues: {'; '.join(error_details)}")
                return False
                
        except Exception as e:
            self.log_test("Key Villa Pricing", False, f"Error: {str(e)}")
            return False
    
    def _villa_name_matches(self, actual_name, expected_name):
        """Helper method to check if villa names match with flexible criteria"""
        actual_lower = actual_name.lower()
        expected_lower = expected_name.lower()
        
        # Direct substring match
        if expected_lower in actual_lower or actual_lower in expected_lower:
            return True
        
        # Extract key components for matching
        actual_parts = set(actual_lower.replace("villa", "").replace("sur", "").split())
        expected_parts = set(expected_lower.replace("villa", "").replace("sur", "").split())
        
        # Check if key parts match (at least 2 common significant parts)
        common_parts = actual_parts & expected_parts
        significant_parts = [p for p in common_parts if len(p) > 2]
        
        return len(significant_parts) >= 2
    
    def test_api_health(self):
        """Test API health before running main tests"""
        try:
            response = self.session.get(f"{API_BASE_URL}/health", timeout=10)
            if response.status_code == 200:
                self.log_test("API Health Check", True, "API is healthy and accessible")
                return True
            else:
                self.log_test("API Health Check", False, f"API health check failed - HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("API Health Check", False, f"API not accessible: {str(e)}")
            return False
    
    def run_final_verification(self):
        """Run the final verification test as requested in review"""
        print("🏖️ KHANELCONCEPT VILLA DATA CORRECTION - FINAL VERIFICATION TEST")
        print("=" * 80)
        print("🎯 Testing villa data correction after CSV integration")
        print(f"📡 API Endpoint: {API_BASE_URL}")
        print("=" * 80)
        
        # Test API health first
        if not self.test_api_health():
            print("❌ API not accessible - stopping verification")
            return False
        
        print("\n🔍 RUNNING VERIFICATION TESTS...")
        print("-" * 50)
        
        # Run all verification tests
        test_results = []
        
        print("1️⃣ Testing villa count (exactly 21 villas)...")
        test_results.append(self.test_villa_count_exactly_21())
        
        print("2️⃣ Testing Espace Piscine villa (€350 pricing)...")
        test_results.append(self.test_espace_piscine_villa_exists())
        
        print("3️⃣ Testing category distribution (sejour:15, fete:5, piscine:1)...")
        test_results.append(self.test_category_distribution())
        
        print("4️⃣ Testing key villa pricing...")
        test_results.append(self.test_key_villa_pricing())
        
        # Final summary
        print("=" * 80)
        print("📊 FINAL VERIFICATION SUMMARY")
        print("=" * 80)
        
        passed_tests = sum(test_results)
        total_tests = len(test_results)
        success_rate = (passed_tests / total_tests) * 100
        
        print(f"✅ Tests Passed: {passed_tests}/{total_tests}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if passed_tests == total_tests:
            print("\n🎉 VILLA DATA CORRECTION SUCCESSFULLY VERIFIED!")
            print("✅ All requirements from the review request have been met:")
            print("   • Exactly 21 villas are present")
            print("   • Espace Piscine Journée Bungalow exists with €350 pricing")
            print("   • All 3 categories are present with correct distribution")
            print("   • Key villa pricing is correct")
            print("\n🚀 The villa data duplication issues and missing villa have been resolved!")
        else:
            print(f"\n❌ VILLA DATA CORRECTION INCOMPLETE!")
            print(f"   {total_tests - passed_tests} out of {total_tests} requirements are not met")
            print("   The villa data correction needs to be completed before deployment")
        
        print("=" * 80)
        
        return passed_tests == total_tests

if __name__ == "__main__":
    tester = VillaDataCorrectionTester()
    success = tester.run_final_verification()
    exit(0 if success else 1)