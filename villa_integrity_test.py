#!/usr/bin/env python3
"""
Villa Data Integrity Analysis for KhanelConcept
Focus: Analyzing villa data for duplications, missing villas, and pricing inconsistencies
"""

import requests
import json
import os
from datetime import datetime
from collections import Counter

# Load environment variables
BACKEND_URL = "https://ebd3cc38-d185-4f99-80ef-7ef3067d8feb.preview.emergentagent.com"
API_BASE_URL = f"{BACKEND_URL}/api"

class VillaDataIntegrityTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        self.villa_data = []
        
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
    
    def test_health_check(self):
        """Test basic API health"""
        try:
            response = self.session.get(f"{API_BASE_URL}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Health Check", True, "API is healthy", data)
                return True
            else:
                self.log_test("Health Check", False, f"Health check failed with status {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Health Check", False, f"Health check error: {str(e)}")
            return False
    
    def retrieve_all_villas(self):
        """Retrieve all villas via GET /api/villas for analysis"""
        try:
            response = self.session.get(f"{API_BASE_URL}/villas", timeout=10)
            
            if response.status_code == 200:
                self.villa_data = response.json()
                villa_count = len(self.villa_data)
                self.log_test("Villa Data Retrieval", True, 
                            f"Successfully retrieved {villa_count} villas from API", 
                            f"Expected: 21 real villas from CSV")
                return True
            else:
                self.log_test("Villa Data Retrieval", False, 
                            f"Failed to retrieve villas - status {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("Villa Data Retrieval", False, f"Error retrieving villas: {str(e)}")
            return False
    
    def analyze_villa_count(self):
        """Analyze total villa count - should be 21 real villas from CSV"""
        if not self.villa_data:
            self.log_test("Villa Count Analysis", False, "No villa data available for analysis")
            return False
        
        villa_count = len(self.villa_data)
        
        if villa_count == 21:
            self.log_test("Villa Count Analysis", True, 
                        f"Perfect! Found exactly 21 villas as expected from CSV integration", 
                        f"Total villas: {villa_count}")
            return True
        elif villa_count > 21:
            self.log_test("Villa Count Analysis", False, 
                        f"Found {villa_count} villas, expected exactly 21 from CSV", 
                        f"Possible duplicate or extra villas present")
            return False
        else:
            self.log_test("Villa Count Analysis", False, 
                        f"Found only {villa_count} villas, expected 21 from CSV", 
                        f"Missing villas detected")
            return False
    
    def analyze_duplicate_villa_names(self):
        """Check for duplicate villa names or similar names"""
        if not self.villa_data:
            self.log_test("Duplicate Names Analysis", False, "No villa data available for analysis")
            return False
        
        villa_names = [villa.get("name", "Unknown") for villa in self.villa_data]
        name_counts = Counter(villa_names)
        
        # Find exact duplicates
        exact_duplicates = {name: count for name, count in name_counts.items() if count > 1}
        
        # Find similar names (basic similarity check)
        similar_names = []
        for i, name1 in enumerate(villa_names):
            for j, name2 in enumerate(villa_names[i+1:], i+1):
                # Check for similar names (same location or similar structure)
                if name1 != name2:
                    name1_words = set(name1.lower().split())
                    name2_words = set(name2.lower().split())
                    common_words = name1_words.intersection(name2_words)
                    
                    # If they share 2+ significant words, flag as similar
                    if len(common_words) >= 2 and any(len(word) > 3 for word in common_words):
                        similar_names.append((name1, name2, list(common_words)))
        
        if exact_duplicates:
            self.log_test("Duplicate Names Analysis", False, 
                        f"Found {len(exact_duplicates)} exact duplicate villa names", 
                        f"Duplicates: {exact_duplicates}")
            return False
        elif similar_names:
            self.log_test("Duplicate Names Analysis", False, 
                        f"Found {len(similar_names)} potentially similar villa names", 
                        f"Similar names: {similar_names[:3]}")  # Show first 3
            return False
        else:
            self.log_test("Duplicate Names Analysis", True, 
                        f"No duplicate or similar villa names found among {len(villa_names)} villas", 
                        f"All villa names are unique")
            return True
    
    def analyze_duplicate_villa_ids(self):
        """Check for duplicate villa IDs"""
        if not self.villa_data:
            self.log_test("Duplicate IDs Analysis", False, "No villa data available for analysis")
            return False
        
        villa_ids = [villa.get("id", "Unknown") for villa in self.villa_data]
        id_counts = Counter(villa_ids)
        
        duplicates = {villa_id: count for villa_id, count in id_counts.items() if count > 1}
        
        if duplicates:
            self.log_test("Duplicate IDs Analysis", False, 
                        f"Found {len(duplicates)} duplicate villa IDs", 
                        f"Duplicate IDs: {duplicates}")
            return False
        else:
            self.log_test("Duplicate IDs Analysis", True, 
                        f"No duplicate villa IDs found among {len(villa_ids)} villas", 
                        f"All villa IDs are unique")
            return True
    
    def search_espace_piscine_villa(self):
        """Specifically look for 'Espace Piscine Journée' villa and verify its pricing (should be €350)"""
        if not self.villa_data:
            self.log_test("Espace Piscine Villa Search", False, "No villa data available for analysis")
            return False
        
        # Search patterns for the villa
        search_patterns = [
            "Espace Piscine Journée Bungalow",
            "Espace Piscine Journée",
            "Espace Piscine",
            "Piscine Journée"
        ]
        
        found_villas = []
        
        for villa in self.villa_data:
            villa_name = villa.get("name", "")
            for pattern in search_patterns:
                if pattern.lower() in villa_name.lower():
                    found_villas.append({
                        "name": villa_name,
                        "id": villa.get("id"),
                        "price": villa.get("price"),
                        "category": villa.get("category"),
                        "location": villa.get("location"),
                        "pattern_matched": pattern
                    })
                    break
        
        if found_villas:
            # Check pricing for found villas
            correct_pricing = []
            incorrect_pricing = []
            
            for villa in found_villas:
                if villa["price"] == 350.0:
                    correct_pricing.append(villa)
                else:
                    incorrect_pricing.append(villa)
            
            if correct_pricing and not incorrect_pricing:
                self.log_test("Espace Piscine Villa Search", True, 
                            f"Found 'Espace Piscine' villa with correct €350 pricing", 
                            f"Villa: {correct_pricing[0]['name']} - €{correct_pricing[0]['price']}")
                return True
            elif incorrect_pricing:
                self.log_test("Espace Piscine Villa Search", False, 
                            f"Found 'Espace Piscine' villa but pricing is incorrect", 
                            f"Expected: €350, Found: €{incorrect_pricing[0]['price']} for {incorrect_pricing[0]['name']}")
                return False
            else:
                self.log_test("Espace Piscine Villa Search", False, 
                            f"Found 'Espace Piscine' villa but no pricing information", 
                            f"Found villas: {[v['name'] for v in found_villas]}")
                return False
        else:
            self.log_test("Espace Piscine Villa Search", False, 
                        "Could not find 'Espace Piscine Journée' villa in the database", 
                        f"Searched patterns: {search_patterns}")
            return False
    
    def analyze_pricing_inconsistencies(self):
        """Look for villas with incorrect pricing or duplicate pricing entries"""
        if not self.villa_data:
            self.log_test("Pricing Inconsistencies Analysis", False, "No villa data available for analysis")
            return False
        
        pricing_issues = []
        price_counts = Counter()
        
        for villa in self.villa_data:
            villa_name = villa.get("name", "Unknown")
            price = villa.get("price")
            
            # Check for missing or invalid pricing
            if price is None:
                pricing_issues.append(f"{villa_name}: Missing price")
            elif not isinstance(price, (int, float)):
                pricing_issues.append(f"{villa_name}: Invalid price type - {type(price)}")
            elif price <= 0:
                pricing_issues.append(f"{villa_name}: Invalid price value - €{price}")
            else:
                price_counts[price] += 1
        
        # Check for suspicious duplicate pricing (same exact price for multiple villas)
        duplicate_prices = {price: count for price, count in price_counts.items() if count > 3}
        
        # Check for pricing that seems inconsistent with villa category/size
        category_price_ranges = {
            "special": (200, 700),    # Studios and small units
            "sejour": (700, 1500),    # Regular villas
            "fete": (1000, 2500),     # Party/event villas
            "piscine": (300, 600)     # Pool day rentals
        }
        
        category_inconsistencies = []
        for villa in self.villa_data:
            villa_name = villa.get("name", "Unknown")
            price = villa.get("price", 0)
            category = villa.get("category", "unknown")
            
            if category in category_price_ranges:
                min_price, max_price = category_price_ranges[category]
                if price < min_price or price > max_price:
                    category_inconsistencies.append(
                        f"{villa_name} ({category}): €{price} outside expected range €{min_price}-{max_price}"
                    )
        
        # Overall assessment
        total_issues = len(pricing_issues) + len(duplicate_prices) + len(category_inconsistencies)
        
        if total_issues == 0:
            self.log_test("Pricing Inconsistencies Analysis", True, 
                        f"No pricing inconsistencies found among {len(self.villa_data)} villas", 
                        f"All villas have valid, reasonable pricing")
            return True
        else:
            issues_summary = []
            if pricing_issues:
                issues_summary.extend(pricing_issues[:3])
            if duplicate_prices:
                issues_summary.append(f"Duplicate prices: {list(duplicate_prices.keys())[:3]}")
            if category_inconsistencies:
                issues_summary.extend(category_inconsistencies[:2])
            
            self.log_test("Pricing Inconsistencies Analysis", False, 
                        f"Found {total_issues} pricing inconsistencies", 
                        f"Issues: {issues_summary}")
            return False
    
    def analyze_villa_categories(self):
        """Check if all villa categories are properly represented (sejour, fete, piscine)"""
        if not self.villa_data:
            self.log_test("Villa Categories Analysis", False, "No villa data available for analysis")
            return False
        
        expected_categories = ["sejour", "fete", "piscine", "special"]
        category_counts = Counter()
        
        for villa in self.villa_data:
            category = villa.get("category", "unknown")
            category_counts[category] += 1
        
        # Check for expected categories
        missing_categories = [cat for cat in expected_categories if category_counts[cat] == 0]
        unexpected_categories = [cat for cat in category_counts.keys() if cat not in expected_categories and cat != "unknown"]
        
        # Specific checks based on review requirements
        issues = []
        
        if missing_categories:
            issues.append(f"Missing categories: {missing_categories}")
        
        if unexpected_categories:
            issues.append(f"Unexpected categories: {unexpected_categories}")
        
        # Check for reasonable distribution
        if category_counts["sejour"] < 10:  # Should have many sejour villas
            issues.append(f"Too few 'sejour' villas: {category_counts['sejour']}")
        
        if category_counts["fete"] < 2:  # Should have some fete villas
            issues.append(f"Too few 'fete' villas: {category_counts['fete']}")
        
        if issues:
            self.log_test("Villa Categories Analysis", False, 
                        f"Category distribution issues found", 
                        f"Issues: {issues}, Distribution: {dict(category_counts)}")
            return False
        else:
            self.log_test("Villa Categories Analysis", True, 
                        f"Villa categories properly represented", 
                        f"Distribution: {dict(category_counts)}")
            return True
    
    def generate_comprehensive_report(self):
        """Generate a comprehensive villa data integrity report"""
        if not self.villa_data:
            self.log_test("Comprehensive Report", False, "No villa data available for report generation")
            return False
        
        print("\n" + "="*80)
        print("🏖️  KHANELCONCEPT VILLA DATA INTEGRITY COMPREHENSIVE REPORT")
        print("="*80)
        
        # Basic statistics
        total_villas = len(self.villa_data)
        print(f"\n📊 BASIC STATISTICS:")
        print(f"   Total Villas Found: {total_villas}")
        print(f"   Expected from CSV: 21")
        print(f"   Status: {'✅ CORRECT' if total_villas == 21 else '❌ INCORRECT'}")
        
        # Villa names sample
        print(f"\n📝 VILLA NAMES SAMPLE (First 10):")
        for i, villa in enumerate(self.villa_data[:10]):
            print(f"   {i+1:2d}. {villa.get('name', 'Unknown')} - €{villa.get('price', 0)} ({villa.get('category', 'unknown')})")
        
        # Category distribution
        category_counts = Counter(villa.get("category", "unknown") for villa in self.villa_data)
        print(f"\n🏷️  CATEGORY DISTRIBUTION:")
        for category, count in category_counts.most_common():
            print(f"   {category:10s}: {count:2d} villas")
        
        # Price range analysis
        prices = [villa.get("price", 0) for villa in self.villa_data if villa.get("price")]
        if prices:
            print(f"\n💰 PRICING ANALYSIS:")
            print(f"   Lowest Price:  €{min(prices)}")
            print(f"   Highest Price: €{max(prices)}")
            print(f"   Average Price: €{sum(prices)/len(prices):.2f}")
        
        # Search for specific villas mentioned in review
        print(f"\n🔍 SPECIFIC VILLA SEARCHES:")
        
        # Espace Piscine search
        espace_piscine_found = False
        for villa in self.villa_data:
            if "espace piscine" in villa.get("name", "").lower():
                espace_piscine_found = True
                print(f"   ✅ Found: {villa['name']} - €{villa.get('price')} ({'✅ CORRECT' if villa.get('price') == 350 else '❌ INCORRECT PRICE'})")
                break
        
        if not espace_piscine_found:
            print(f"   ❌ 'Espace Piscine Journée Bungalow' NOT FOUND")
        
        # Key villas from CSV
        key_villas = ["Villa F3 Petit Macabou", "Villa F5 Ste Anne", "Villa F6 Petit Macabou"]
        print(f"\n🎯 KEY VILLAS FROM CSV:")
        for key_villa in key_villas:
            found = False
            for villa in self.villa_data:
                if key_villa.lower() in villa.get("name", "").lower():
                    found = True
                    print(f"   ✅ {villa['name']} - €{villa.get('price')}")
                    break
            if not found:
                print(f"   ❌ {key_villa} NOT FOUND")
        
        # CSV integration status
        csv_integrated = sum(1 for villa in self.villa_data if villa.get("csv_integrated"))
        print(f"\n📋 CSV INTEGRATION STATUS:")
        print(f"   Villas with CSV flag: {csv_integrated}/{total_villas}")
        print(f"   Integration rate: {(csv_integrated/total_villas)*100:.1f}%")
        
        print("\n" + "="*80)
        
        return True
    
    def run_villa_data_integrity_analysis(self):
        """Run comprehensive villa data integrity analysis as requested in review"""
        print("🏖️ Starting KhanelConcept Villa Data Integrity Analysis")
        print("🎯 Focus: Duplication Issues, Missing Villas, Pricing Inconsistencies")
        print(f"Testing against: {API_BASE_URL}")
        print("=" * 80)
        
        # Test basic connectivity
        if not self.test_health_check():
            print("❌ Health check failed - stopping analysis")
            return False
        
        # Retrieve all villa data
        if not self.retrieve_all_villas():
            print("❌ Failed to retrieve villa data - stopping analysis")
            return False
        
        print("\n🔍 VILLA DATA INTEGRITY ANALYSIS")
        print("-" * 50)
        
        # Core analysis as requested in review
        self.analyze_villa_count()
        self.analyze_duplicate_villa_names()
        self.analyze_duplicate_villa_ids()
        self.search_espace_piscine_villa()
        self.analyze_pricing_inconsistencies()
        self.analyze_villa_categories()
        
        # Generate comprehensive report
        print("\n📊 GENERATING COMPREHENSIVE REPORT")
        print("-" * 40)
        self.generate_comprehensive_report()
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 VILLA DATA INTEGRITY ANALYSIS SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        # Show failed tests
        failed_tests = [result for result in self.test_results if not result["success"]]
        if failed_tests:
            print("\n❌ ISSUES FOUND:")
            for test in failed_tests:
                print(f"  - {test['test']}: {test['message']}")
        else:
            print("\n✅ NO ISSUES FOUND - Villa data integrity is excellent!")
        
        return passed == total

if __name__ == "__main__":
    tester = VillaDataIntegrityTester()
    success = tester.run_villa_data_integrity_analysis()
    
    if success:
        print("\n🎉 Villa data integrity analysis completed successfully!")
    else:
        print("\n⚠️  Issues found in villa data - check details above")