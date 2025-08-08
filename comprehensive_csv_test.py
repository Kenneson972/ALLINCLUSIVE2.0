#!/usr/bin/env python3
"""
Comprehensive CSV Integration Testing for KhanelConcept Villa Data
Testing the complete CSV integration for 22 villas as requested in the review
"""

import requests
import json
import os
from datetime import datetime

# Load backend URL
BACKEND_URL = "https://f6169287-bcef-4657-a67a-5f4c828e7215.preview.emergentagent.com"
API_BASE_URL = f"{BACKEND_URL}/api"

class ComprehensiveCSVTester:
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
    
    def get_all_villas(self):
        """Get all villas from API"""
        try:
            response = self.session.get(f"{API_BASE_URL}/villas", timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to get villas: HTTP {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Error getting villas: {str(e)}")
            return []
    
    def test_22_villas_updated(self):
        """Test that all 22 villas have been updated with CSV data"""
        villas = self.get_all_villas()
        
        if len(villas) != 22:
            self.log_test("22 Villas Count", False, 
                        f"Expected 22 villas, got {len(villas)}")
            return False, villas
        
        # Check for csv_updated flag
        csv_updated_count = 0
        for villa in villas:
            if villa.get("csv_updated", False):
                csv_updated_count += 1
        
        if csv_updated_count == 22:
            self.log_test("22 Villas Updated", True,
                        f"All 22 villas have csv_updated: true",
                        f"CSV updated count: {csv_updated_count}/22")
        else:
            self.log_test("22 Villas Updated", False,
                        f"Only {csv_updated_count}/22 villas have csv_updated: true")
        
        return True, villas
    
    def test_espace_piscine_mapping(self, villas):
        """Test specific mapping: Espace Piscine → Villa Sunset Paradise (price 350€)"""
        villa_sunset_paradise = None
        
        # Look for Villa Sunset Paradise
        for villa in villas:
            if "Villa Sunset Paradise" in villa.get("name", ""):
                villa_sunset_paradise = villa
                break
        
        if not villa_sunset_paradise:
            self.log_test("Espace Piscine Mapping", False,
                        "Villa Sunset Paradise not found in database")
            return False
        
        # Check price (should be 350€ instead of 950€)
        current_price = villa_sunset_paradise.get("price", 0)
        expected_price = 350.0
        
        if current_price == expected_price:
            price_correct = True
            price_msg = f"Price correctly updated to €{current_price}"
        else:
            price_correct = False
            price_msg = f"Price incorrect: expected €{expected_price}, got €{current_price}"
        
        # Check services
        features = villa_sunset_paradise.get("features", "")
        services_full = villa_sunset_paradise.get("services_full", "")
        expected_services = "Cuisine, salle d'eau, mobilier (chaises, tables), chambre climatisée"
        
        # Check if expected services are present
        services_content = f"{features} {services_full}".lower()
        service_keywords = ["cuisine", "salle d'eau", "mobilier", "chambre climatisée"]
        services_found = [keyword for keyword in service_keywords if keyword.lower() in services_content]
        
        services_correct = len(services_found) >= 2  # At least 2 services should be found
        
        # Check csv_updated flag
        csv_updated = villa_sunset_paradise.get("csv_updated", False)
        
        # Overall assessment
        if price_correct and services_correct and csv_updated:
            self.log_test("Espace Piscine Mapping", True,
                        f"Villa Sunset Paradise correctly mapped from Espace Piscine",
                        {
                            "price": price_msg,
                            "services_found": services_found,
                            "csv_updated": csv_updated,
                            "villa_data": {
                                "name": villa_sunset_paradise.get("name"),
                                "price": current_price,
                                "features": features,
                                "services_full": services_full
                            }
                        })
            return True
        else:
            issues = []
            if not price_correct:
                issues.append(price_msg)
            if not services_correct:
                issues.append(f"Services incomplete: found {services_found}")
            if not csv_updated:
                issues.append("csv_updated flag missing")
            
            self.log_test("Espace Piscine Mapping", False,
                        f"Villa Sunset Paradise mapping issues: {'; '.join(issues)}",
                        {
                            "current_price": current_price,
                            "expected_price": expected_price,
                            "services_found": services_found,
                            "csv_updated": csv_updated
                        })
            return False
    
    def test_key_villa_prices(self, villas):
        """Test prices for key villas mentioned in review"""
        key_villas = {
            "Villa F3 Petit Macabou": 850.0,
            "Villa F5 Ste Anne": 1350.0,
            "Villa F6 Petit Macabou": 2200.0
        }
        
        results = {}
        all_correct = True
        
        for expected_name, expected_price in key_villas.items():
            villa_found = False
            
            for villa in villas:
                villa_name = villa.get("name", "")
                if expected_name in villa_name:
                    villa_found = True
                    current_price = villa.get("price", 0)
                    
                    if current_price == expected_price:
                        results[expected_name] = f"✅ €{current_price} (correct)"
                    else:
                        results[expected_name] = f"❌ €{current_price} (expected €{expected_price})"
                        all_correct = False
                    break
            
            if not villa_found:
                results[expected_name] = "❌ Villa not found"
                all_correct = False
        
        if all_correct:
            self.log_test("Key Villa Prices", True,
                        "All key villa prices are correct",
                        results)
        else:
            self.log_test("Key Villa Prices", False,
                        "Some villa prices are incorrect",
                        results)
        
        return all_correct
    
    def test_villa_mappings(self, villas):
        """Test villa name mappings mentioned in review"""
        expected_mappings = {
            "Studio Ducos Pratique": "Villa Fête Journée Ducos",
            "Villa Carbet Deluxe": "Villa Fête Journée Rivière Salée",
            "Appartement Marina Fort-de-France": "Villa Fête Journée Fort de France"
        }
        
        villa_names = [villa.get("name", "") for villa in villas]
        mapping_results = {}
        all_mappings_found = True
        
        for original_name, csv_name in expected_mappings.items():
            # Check if either original or CSV name exists
            original_found = any(original_name in name for name in villa_names)
            csv_found = any(csv_name in name for name in villa_names)
            
            if original_found or csv_found:
                mapping_results[original_name] = f"✅ Found (mapped to {csv_name})"
            else:
                mapping_results[original_name] = f"❌ Neither original nor CSV name found"
                all_mappings_found = False
        
        if all_mappings_found:
            self.log_test("Villa Name Mappings", True,
                        "All expected villa name mappings found",
                        mapping_results)
        else:
            self.log_test("Villa Name Mappings", False,
                        "Some villa name mappings missing",
                        mapping_results)
        
        return all_mappings_found
    
    def test_csv_data_presence(self, villas):
        """Test that villas have CSV-specific data fields"""
        csv_fields = ["services_full", "guests_detail", "csv_updated"]
        villas_with_csv_data = 0
        
        for villa in villas:
            csv_fields_present = sum(1 for field in csv_fields if villa.get(field))
            if csv_fields_present >= 2:  # At least 2 CSV fields
                villas_with_csv_data += 1
        
        csv_rate = (villas_with_csv_data / len(villas)) * 100
        
        if csv_rate >= 90:  # At least 90% should have CSV data
            self.log_test("CSV Data Presence", True,
                        f"CSV data present in {csv_rate:.1f}% of villas",
                        f"Villas with CSV data: {villas_with_csv_data}/{len(villas)}")
            return True
        else:
            self.log_test("CSV Data Presence", False,
                        f"CSV data only in {csv_rate:.1f}% of villas",
                        f"Expected at least 90%, got {csv_rate:.1f}%")
            return False
    
    def test_api_consistency(self):
        """Test that different API endpoints return consistent data"""
        endpoints = [
            ("/villas", "Public Villas"),
            ("/admin/villas", "Admin Villas"),
            ("/stats/dashboard", "Dashboard Stats")
        ]
        
        results = {}
        all_consistent = True
        
        for endpoint, name in endpoints:
            try:
                response = self.session.get(f"{API_BASE_URL}{endpoint}", timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if endpoint == "/stats/dashboard":
                        villa_count = data.get("total_villas", 0)
                    else:
                        villa_count = len(data) if isinstance(data, list) else 0
                    
                    if villa_count == 22:
                        results[name] = f"✅ {villa_count} villas"
                    else:
                        results[name] = f"❌ {villa_count} villas (expected 22)"
                        all_consistent = False
                else:
                    results[name] = f"❌ HTTP {response.status_code}"
                    all_consistent = False
                    
            except Exception as e:
                results[name] = f"❌ Error: {str(e)}"
                all_consistent = False
        
        if all_consistent:
            self.log_test("API Consistency", True,
                        "All API endpoints return consistent villa count",
                        results)
        else:
            self.log_test("API Consistency", False,
                        "API endpoints return inconsistent data",
                        results)
        
        return all_consistent
    
    def run_comprehensive_tests(self):
        """Run all comprehensive CSV integration tests"""
        print("🏖️ Starting Comprehensive CSV Integration Testing for KhanelConcept")
        print("🎯 Focus: Verify 22 villas updated, Espace Piscine mapping, and API consistency")
        print(f"Testing against: {API_BASE_URL}")
        print("=" * 80)
        
        # Step 1: Test villa count and get data
        print("\n📊 STEP 1: VILLA COUNT AND CSV FLAGS")
        print("-" * 40)
        success, villas = self.test_22_villas_updated()
        
        if not success or not villas:
            print("❌ Cannot proceed without villa data")
            return False
        
        # Step 2: Test Espace Piscine mapping (main concern)
        print("\n🎯 STEP 2: ESPACE PISCINE → VILLA SUNSET PARADISE")
        print("-" * 50)
        self.test_espace_piscine_mapping(villas)
        
        # Step 3: Test key villa prices
        print("\n💰 STEP 3: KEY VILLA PRICES")
        print("-" * 30)
        self.test_key_villa_prices(villas)
        
        # Step 4: Test villa mappings
        print("\n🔄 STEP 4: VILLA NAME MAPPINGS")
        print("-" * 35)
        self.test_villa_mappings(villas)
        
        # Step 5: Test CSV data presence
        print("\n📋 STEP 5: CSV DATA PRESENCE")
        print("-" * 30)
        self.test_csv_data_presence(villas)
        
        # Step 6: Test API consistency
        print("\n🔍 STEP 6: API CONSISTENCY")
        print("-" * 25)
        self.test_api_consistency()
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE CSV INTEGRATION TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        # Critical findings
        print(f"\n🎯 CRITICAL FINDINGS:")
        
        # Check Espace Piscine mapping
        espace_test = next((r for r in self.test_results if r["test"] == "Espace Piscine Mapping"), None)
        if espace_test:
            if espace_test["success"]:
                print("  ✅ Espace Piscine → Villa Sunset Paradise mapping WORKING")
            else:
                print("  ❌ Espace Piscine → Villa Sunset Paradise mapping FAILED")
        
        # Check API consistency
        api_test = next((r for r in self.test_results if r["test"] == "API Consistency"), None)
        if api_test:
            if api_test["success"]:
                print("  ✅ API returns consistent updated data")
            else:
                print("  ❌ API NOT returning consistent data")
        
        # Show failed tests
        failed_tests = [result for result in self.test_results if not result["success"]]
        if failed_tests:
            print("\n❌ FAILED TESTS:")
            for test in failed_tests:
                print(f"  - {test['test']}: {test['message']}")
        
        return passed == total

if __name__ == "__main__":
    tester = ComprehensiveCSVTester()
    success = tester.run_comprehensive_tests()
    
    if success:
        print("\n🎉 All CSV integration tests passed!")
        print("✅ The correction_complete_csv.py script worked correctly")
    else:
        print("\n⚠️  Some CSV integration tests failed")
        print("❌ Issues found with CSV integration or API data consistency")