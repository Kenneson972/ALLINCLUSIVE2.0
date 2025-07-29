#!/usr/bin/env python3
"""
Diagnostic test to see what's actually in the database
"""

import requests
import json
from collections import Counter

BACKEND_URL = "https://34d42641-f91e-4f6d-9f2c-608b166de7b9.preview.emergentagent.com"
API_BASE_URL = f"{BACKEND_URL}/api"

def diagnostic_check():
    try:
        response = requests.get(f"{API_BASE_URL}/villas", timeout=10)
        
        if response.status_code != 200:
            print(f"❌ Could not retrieve villas - HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return
        
        villas = response.json()
        print(f"✅ Successfully retrieved {len(villas)} villas")
        print()
        
        # Count categories
        categories = Counter()
        for villa in villas:
            category = villa.get("category", "unknown")
            categories[category] += 1
        
        print("📊 CATEGORY DISTRIBUTION:")
        for category, count in categories.items():
            print(f"   {category}: {count}")
        print()
        
        # Look for Espace Piscine
        print("🔍 SEARCHING FOR ESPACE PISCINE VILLA:")
        espace_found = False
        for villa in villas:
            villa_name = villa.get("name", "").lower()
            if "espace piscine" in villa_name:
                espace_found = True
                print(f"   ✅ FOUND: {villa['name']}")
                print(f"      Price: €{villa.get('price', 0)}")
                print(f"      Category: {villa.get('category', 'unknown')}")
                print(f"      ID: {villa.get('id', 'unknown')}")
                break
        
        if not espace_found:
            print("   ❌ Espace Piscine villa NOT FOUND")
        print()
        
        # Check key villas
        print("🎯 KEY VILLAS CHECK:")
        key_villas = {
            "Villa F3 sur Petit Macabou": 850.0,
            "Villa F5 sur Ste Anne": 1350.0,
            "Villa F6 sur Petit Macabou": 2000.0
        }
        
        for expected_name, expected_price in key_villas.items():
            found = False
            for villa in villas:
                villa_name = villa.get("name", "")
                if any(part in villa_name.lower() for part in expected_name.lower().split()):
                    found = True
                    actual_price = villa.get("price", 0)
                    status = "✅" if actual_price == expected_price else "❌"
                    print(f"   {status} {villa_name}: €{actual_price} (expected €{expected_price})")
                    break
            
            if not found:
                print(f"   ❌ {expected_name}: NOT FOUND")
        print()
        
        # Show all villa names for reference
        print("📋 ALL VILLA NAMES:")
        for i, villa in enumerate(villas, 1):
            name = villa.get("name", "Unknown")
            price = villa.get("price", 0)
            category = villa.get("category", "unknown")
            print(f"   {i:2d}. {name} - €{price} ({category})")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    diagnostic_check()