#!/usr/bin/env python3
"""
Final Verification Test - KhanelConcept Villa Data Correction
Testing all requirements from the review request
"""

import requests
import json
from collections import Counter

# Backend URL
BACKEND_URL = "https://11d55026-8d04-4554-bff9-4cc57e14d1b2.preview.emergentagent.com"

def main():
    print("🌴 KHANELCONCEPT VILLA DATA CORRECTION - FINAL VERIFICATION")
    print("=" * 70)
    print("Testing all requirements from review request...")
    print()
    
    try:
        # Get all villas
        response = requests.get(f"{BACKEND_URL}/api/villas", timeout=10)
        if response.status_code != 200:
            print(f"❌ API Error: {response.status_code}")
            return False
        
        villas = response.json()
        
        # Test results
        tests_passed = 0
        total_tests = 5
        
        # 1. Confirm exactly 21 villas
        print("1️⃣ TESTING: Exactly 21 villas present")
        if len(villas) == 21:
            print("   ✅ SUCCESS: Found exactly 21 villas")
            tests_passed += 1
        else:
            print(f"   ❌ FAILED: Found {len(villas)} villas, expected 21")
        print()
        
        # 2. Check Espace Piscine villa
        print("2️⃣ TESTING: Espace Piscine Journée Bungalow exists with €350 and 'piscine' category")
        espace_piscine = None
        for villa in villas:
            if "Espace Piscine Journée Bungalow" in villa.get("name", ""):
                espace_piscine = villa
                break
        
        if espace_piscine:
            price_ok = espace_piscine['price'] == 350.0
            category_ok = espace_piscine['category'] == 'piscine'
            
            if price_ok and category_ok:
                print(f"   ✅ SUCCESS: Found '{espace_piscine['name']}' with €350 pricing and 'piscine' category")
                tests_passed += 1
            else:
                print(f"   ❌ FAILED: Price: €{espace_piscine['price']} (expected €350), Category: '{espace_piscine['category']}' (expected 'piscine')")
        else:
            print("   ❌ FAILED: Espace Piscine Journée Bungalow not found")
        print()
        
        # 3. Verify category distribution
        print("3️⃣ TESTING: Category distribution - sejour (15), fete (5), piscine (1)")
        categories = [villa.get("category", "unknown") for villa in villas]
        category_counts = Counter(categories)
        
        expected = {"sejour": 15, "fete": 5, "piscine": 1}
        category_ok = True
        
        for cat, expected_count in expected.items():
            actual_count = category_counts.get(cat, 0)
            if actual_count != expected_count:
                category_ok = False
                break
        
        if category_ok:
            print(f"   ✅ SUCCESS: Category distribution correct - {dict(category_counts)}")
            tests_passed += 1
        else:
            print(f"   ❌ FAILED: Category distribution - {dict(category_counts)}, expected {expected}")
        print()
        
        # 4. Check key villa pricing
        print("4️⃣ TESTING: Key villa pricing verification")
        key_villas = {
            "Villa F3 sur Petit Macabou": 850.0,
            "Villa F5 sur Ste Anne": 1350.0,
            "Villa F6 sur Petit Macabou": 2000.0,
            "Espace Piscine Journée Bungalow": 350.0
        }
        
        pricing_ok = True
        pricing_results = []
        
        for villa_name, expected_price in key_villas.items():
            found = False
            for villa in villas:
                if villa_name in villa.get("name", ""):
                    actual_price = villa['price']
                    if actual_price == expected_price:
                        pricing_results.append(f"   ✅ {villa_name}: €{actual_price}")
                    else:
                        pricing_results.append(f"   ❌ {villa_name}: €{actual_price} (expected €{expected_price})")
                        pricing_ok = False
                    found = True
                    break
            
            if not found:
                pricing_results.append(f"   ❌ {villa_name}: NOT FOUND")
                pricing_ok = False
        
        if pricing_ok:
            print("   ✅ SUCCESS: All key villa pricing correct")
            tests_passed += 1
        else:
            print("   ❌ FAILED: Key villa pricing issues")
        
        for result in pricing_results:
            print(result)
        print()
        
        # 5. Check csv_integrated flags
        print("5️⃣ TESTING: CSV integrated flags set for all villas")
        csv_integrated_count = sum(1 for villa in villas if villa.get("csv_integrated", False))
        
        if csv_integrated_count == 21:
            print(f"   ✅ SUCCESS: All {csv_integrated_count}/21 villas have csv_integrated=true")
            tests_passed += 1
        else:
            print(f"   ❌ FAILED: Only {csv_integrated_count}/21 villas have csv_integrated=true")
        print()
        
        # Final summary
        print("=" * 70)
        print("📊 FINAL VERIFICATION SUMMARY")
        print("=" * 70)
        print(f"Tests Passed: {tests_passed}/{total_tests}")
        print(f"Success Rate: {(tests_passed/total_tests)*100:.1f}%")
        print()
        
        if tests_passed == total_tests:
            print("🎉 VILLA DATA CORRECTION SUCCESSFULLY VERIFIED!")
            print("✅ All requirements from review request have been met:")
            print("   • Exactly 21 villas present")
            print("   • Espace Piscine Journée Bungalow exists with €350 pricing and 'piscine' category")
            print("   • Category distribution correct: sejour (15), fete (5), piscine (1)")
            print("   • Key villa pricing verified")
            print("   • CSV integration flags set for all villas")
            print()
            print("The villa data duplication issues and missing 'Espace Piscine' villa have been successfully resolved.")
            return True
        else:
            print("❌ VILLA DATA CORRECTION VERIFICATION FAILED!")
            print("Some requirements are not yet met.")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)