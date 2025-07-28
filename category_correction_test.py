#!/usr/bin/env python3
"""
Category Correction Verification Test for KhanelConcept
Focus: Quick verification after category correction as requested in review

Requirements from review request:
1. Confirm exactly 21 villas are present
2. Check that "Espace Piscine Journée Bungalow" exists with €350 pricing and is now in 'fete' category (not 'piscine')
3. Verify only 2 categories are present: sejour and fete (no 'piscine' category)
4. Confirm the distribution: sejour (15), fete (6)
"""

import requests
import json
from datetime import datetime
from collections import Counter

# Load backend URL from environment
BACKEND_URL = "https://cfc0e6ef-086c-461a-915c-2319466028f1.preview.emergentagent.com"
API_BASE_URL = f"{BACKEND_URL}/api"

class CategoryCorrectionTester:
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
                self.log_test("Villa Count (21)", False, 
                            f"Could not retrieve villas - status {response.status_code}")
                return False
            
            villas = response.json()
            villa_count = len(villas)
            
            if villa_count == 21:
                self.log_test("Villa Count (21)", True, 
                            f"✅ PERFECT! Exactly 21 villas found as required")
                return True
            else:
                self.log_test("Villa Count (21)", False, 
                            f"❌ Expected exactly 21 villas, found {villa_count}")
                return False
                
        except Exception as e:
            self.log_test("Villa Count (21)", False, f"Error: {str(e)}")
            return False
    
    def test_espace_piscine_in_fete_category(self):
        """Test 2: Check that "Espace Piscine Journée Bungalow" exists with €350 pricing and is in 'fete' category"""
        try:
            response = self.session.get(f"{API_BASE_URL}/villas", timeout=10)
            
            if response.status_code != 200:
                self.log_test("Espace Piscine in Fete Category", False, 
                            f"Could not retrieve villas - status {response.status_code}")
                return False
            
            villas = response.json()
            
            # Search for Espace Piscine villa
            espace_piscine_patterns = [
                "Espace Piscine Journée Bungalow",
                "Espace Piscine Journée",
                "Espace Piscine"
            ]
            
            found_villa = None
            for villa in villas:
                villa_name = villa.get("name", "")
                for pattern in espace_piscine_patterns:
                    if pattern.lower() in villa_name.lower():
                        found_villa = villa
                        break
                if found_villa:
                    break
            
            if not found_villa:
                self.log_test("Espace Piscine in Fete Category", False, 
                            f"❌ 'Espace Piscine Journée Bungalow' NOT FOUND in database")
                return False
            
            # Check price
            villa_price = found_villa.get("price", 0)
            if villa_price != 350.0:
                self.log_test("Espace Piscine in Fete Category", False, 
                            f"❌ Found '{found_villa['name']}' but price is €{villa_price}, expected €350")
                return False
            
            # Check category
            villa_category = found_villa.get("category", "")
            if villa_category != "fete":
                self.log_test("Espace Piscine in Fete Category", False, 
                            f"❌ Found '{found_villa['name']}' with €350 but category is '{villa_category}', expected 'fete'")
                return False
            
            self.log_test("Espace Piscine in Fete Category", True, 
                        f"✅ PERFECT! '{found_villa['name']}' found with €350 pricing in 'fete' category")
            return True
                
        except Exception as e:
            self.log_test("Espace Piscine in Fete Category", False, f"Error: {str(e)}")
            return False
    
    def test_only_sejour_and_fete_categories(self):
        """Test 3: Verify only 2 categories are present: sejour and fete (no 'piscine' category)"""
        try:
            response = self.session.get(f"{API_BASE_URL}/villas", timeout=10)
            
            if response.status_code != 200:
                self.log_test("Only Sejour and Fete Categories", False, 
                            f"Could not retrieve villas - status {response.status_code}")
                return False
            
            villas = response.json()
            
            # Count categories
            categories = {}
            for villa in villas:
                category = villa.get("category", "unknown")
                categories[category] = categories.get(category, 0) + 1
            
            # Check categories
            found_categories = set(categories.keys())
            expected_categories = {"sejour", "fete"}
            
            # Check if only sejour and fete are present
            if found_categories == expected_categories:
                self.log_test("Only Sejour and Fete Categories", True, 
                            f"✅ PERFECT! Only 2 categories present: sejour and fete (no 'piscine')")
                return True
            elif "piscine" in found_categories:
                self.log_test("Only Sejour and Fete Categories", False, 
                            f"❌ 'piscine' category still exists! Found categories: {list(found_categories)}")
                return False
            else:
                self.log_test("Only Sejour and Fete Categories", False, 
                            f"❌ Unexpected categories found: {list(found_categories)}, expected only: sejour, fete")
                return False
                
        except Exception as e:
            self.log_test("Only Sejour and Fete Categories", False, f"Error: {str(e)}")
            return False
    
    def test_category_distribution_15_6(self):
        """Test 4: Confirm the distribution: sejour (15), fete (6)"""
        try:
            response = self.session.get(f"{API_BASE_URL}/villas", timeout=10)
            
            if response.status_code != 200:
                self.log_test("Category Distribution (15,6)", False, 
                            f"Could not retrieve villas - status {response.status_code}")
                return False
            
            villas = response.json()
            
            # Count categories
            categories = {}
            for villa in villas:
                category = villa.get("category", "unknown")
                categories[category] = categories.get(category, 0) + 1
            
            # Check distribution
            sejour_count = categories.get("sejour", 0)
            fete_count = categories.get("fete", 0)
            
            if sejour_count == 15 and fete_count == 6:
                self.log_test("Category Distribution (15,6)", True, 
                            f"✅ PERFECT! Distribution matches: sejour (15), fete (6)")
                return True
            else:
                self.log_test("Category Distribution (15,6)", False, 
                            f"❌ Expected sejour (15), fete (6) but found sejour ({sejour_count}), fete ({fete_count})")
                return False
                
        except Exception as e:
            self.log_test("Category Distribution (15,6)", False, f"Error: {str(e)}")
            return False
    
    def test_comprehensive_category_correction(self):
        """Comprehensive test combining all category correction requirements"""
        try:
            response = self.session.get(f"{API_BASE_URL}/villas", timeout=10)
            
            if response.status_code != 200:
                self.log_test("Comprehensive Category Correction", False, 
                            f"Could not retrieve villas - status {response.status_code}")
                return False
            
            villas = response.json()
            
            # Analysis
            analysis = {
                "total_villas": len(villas),
                "categories": {},
                "espace_piscine_found": False,
                "espace_piscine_details": None
            }
            
            for villa in villas:
                # Category analysis
                category = villa.get("category", "unknown")
                analysis["categories"][category] = analysis["categories"].get(category, 0) + 1
                
                # Espace Piscine detection
                villa_name = villa.get("name", "").lower()
                if "espace piscine" in villa_name:
                    analysis["espace_piscine_found"] = True
                    analysis["espace_piscine_details"] = {
                        "name": villa.get("name"),
                        "price": villa.get("price"),
                        "category": villa.get("category")
                    }
            
            # Check all requirements
            requirements_met = []
            
            # Requirement 1: Exactly 21 villas
            req1 = analysis["total_villas"] == 21
            requirements_met.append(("Exactly 21 villas", req1))
            
            # Requirement 2: Espace Piscine in fete with €350
            req2 = (analysis["espace_piscine_found"] and 
                   analysis["espace_piscine_details"] and
                   analysis["espace_piscine_details"]["price"] == 350.0 and
                   analysis["espace_piscine_details"]["category"] == "fete")
            requirements_met.append(("Espace Piscine in fete with €350", req2))
            
            # Requirement 3: Only sejour and fete categories
            req3 = set(analysis["categories"].keys()) == {"sejour", "fete"}
            requirements_met.append(("Only sejour and fete categories", req3))
            
            # Requirement 4: Distribution sejour (15), fete (6)
            req4 = (analysis["categories"].get("sejour", 0) == 15 and 
                   analysis["categories"].get("fete", 0) == 6)
            requirements_met.append(("Distribution sejour(15), fete(6)", req4))
            
            # Overall assessment
            all_met = all(req[1] for req in requirements_met)
            met_count = sum(1 for req in requirements_met if req[1])
            
            if all_met:
                self.log_test("Comprehensive Category Correction", True, 
                            f"✅ ALL 4 category correction requirements met perfectly!", 
                            f"Analysis: {analysis}")
                return True
            else:
                failed_reqs = [req[0] for req in requirements_met if not req[1]]
                self.log_test("Comprehensive Category Correction", False, 
                            f"❌ {met_count}/4 requirements met. Failed: {failed_reqs}", 
                            f"Analysis: {analysis}")
                return False
                
        except Exception as e:
            self.log_test("Comprehensive Category Correction", False, f"Error: {str(e)}")
            return False
    
    def run_category_correction_verification(self):
        """Run the category correction verification tests"""
        print("🏖️ KhanelConcept Category Correction Verification")
        print("🎯 Quick verification after category correction")
        print(f"Testing against: {API_BASE_URL}")
        print("=" * 60)
        
        print("\n🔍 CATEGORY CORRECTION VERIFICATION TESTS")
        print("-" * 45)
        
        # Run all tests
        test1 = self.test_villa_count_exactly_21()
        test2 = self.test_espace_piscine_in_fete_category()
        test3 = self.test_only_sejour_and_fete_categories()
        test4 = self.test_category_distribution_15_6()
        test5 = self.test_comprehensive_category_correction()
        
        # Summary
        print("=" * 60)
        print("📊 CATEGORY CORRECTION VERIFICATION SUMMARY")
        print("=" * 60)
        
        main_tests = [test1, test2, test3, test4]
        passed = sum(main_tests)
        total = len(main_tests)
        
        print(f"📋 MAIN VERIFICATION TESTS:")
        print(f"   1. Villa Count (21): {'✅ PASS' if test1 else '❌ FAIL'}")
        print(f"   2. Espace Piscine in Fete: {'✅ PASS' if test2 else '❌ FAIL'}")
        print(f"   3. Only Sejour & Fete: {'✅ PASS' if test3 else '❌ FAIL'}")
        print(f"   4. Distribution (15,6): {'✅ PASS' if test4 else '❌ FAIL'}")
        print(f"   5. Comprehensive: {'✅ PASS' if test5 else '❌ FAIL'}")
        
        print(f"\n📊 OVERALL RESULTS:")
        print(f"   Passed: {passed}/{total}")
        print(f"   Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print(f"\n🎉 SUCCESS! Category correction was applied successfully!")
            print(f"   ✅ All requirements from user feedback have been met")
            return True
        else:
            print(f"\n⚠️  ISSUES FOUND! Category correction needs attention")
            print(f"   ❌ {total - passed} requirement(s) not met")
            return False

def main():
    """Main function to run the category correction verification"""
    tester = CategoryCorrectionTester()
    success = tester.run_category_correction_verification()
    
    if success:
        print("\n✅ Category correction verification completed successfully!")
    else:
        print("\n❌ Category correction verification found issues!")
    
    return success

if __name__ == "__main__":
    main()