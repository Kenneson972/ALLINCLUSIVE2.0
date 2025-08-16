#!/usr/bin/env python3
"""
Additional comprehensive test for reservation creation and admin functionality
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
BACKEND_URL = "https://web-a11y-upgrade.preview.emergentagent.com"
API_BASE_URL = f"{BACKEND_URL}/api"

def test_reservation_creation():
    """Test creating a reservation and then viewing it via admin"""
    session = requests.Session()
    
    print("🧪 Testing Reservation Creation and Admin View")
    
    # Step 1: Create a test reservation
    reservation_data = {
        "villa_id": "1",
        "customer_name": "Marie Dubois",
        "customer_email": "marie.dubois@example.com",
        "customer_phone": "+596 696 12 34 56",
        "checkin_date": "2025-08-15",
        "checkout_date": "2025-08-22",
        "guests_count": 4,
        "message": "Réservation pour vacances en famille",
        "total_price": 5950.0
    }
    
    try:
        response = session.post(f"{API_BASE_URL}/reservations", json=reservation_data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Reservation created successfully: {result['reservation_id']}")
            reservation_id = result['reservation_id']
            
            # Step 2: Login as admin
            login_data = {"username": "admin", "password": "khanelconcept2025"}
            login_response = session.post(f"{API_BASE_URL}/admin/login", json=login_data, timeout=10)
            
            if login_response.status_code == 200:
                print("✅ Admin login successful")
                
                # Step 3: Check admin reservations
                admin_reservations = session.get(f"{API_BASE_URL}/admin/reservations", timeout=10)
                
                if admin_reservations.status_code == 200:
                    reservations = admin_reservations.json()
                    print(f"✅ Admin can view reservations: {len(reservations)} found")
                    
                    # Find our test reservation
                    test_reservation = next((r for r in reservations if r['id'] == reservation_id), None)
                    if test_reservation:
                        print(f"✅ Test reservation found in admin view: {test_reservation['customer_name']}")
                        
                        # Step 4: Test dashboard stats update
                        stats_response = session.get(f"{API_BASE_URL}/stats/dashboard", timeout=10)
                        if stats_response.status_code == 200:
                            stats = stats_response.json()
                            print(f"✅ Dashboard stats updated: {stats['total_reservations']} total reservations")
                            return True
                        else:
                            print("❌ Dashboard stats failed")
                            return False
                    else:
                        print("❌ Test reservation not found in admin view")
                        return False
                else:
                    print("❌ Admin reservations view failed")
                    return False
            else:
                print("❌ Admin login failed")
                return False
        else:
            print(f"❌ Reservation creation failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
        return False

def test_villa_details():
    """Test individual villa details endpoint"""
    session = requests.Session()
    
    try:
        # Test getting a specific villa
        response = session.get(f"{API_BASE_URL}/villas/1", timeout=10)
        
        if response.status_code == 200:
            villa = response.json()
            print(f"✅ Villa details endpoint working: {villa['name']}")
            
            # Check required fields
            required_fields = ["id", "name", "location", "price", "guests", "features", "category", "image", "gallery"]
            missing_fields = [field for field in required_fields if field not in villa]
            
            if not missing_fields:
                print("✅ Villa data structure complete")
                return True
            else:
                print(f"❌ Villa missing fields: {missing_fields}")
                return False
        else:
            print(f"❌ Villa details failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Villa details error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔍 Running Additional Backend Tests")
    print("=" * 50)
    
    # Test villa details
    villa_test = test_villa_details()
    
    # Test reservation flow
    reservation_test = test_reservation_creation()
    
    print("\n" + "=" * 50)
    print("📊 ADDITIONAL TEST RESULTS")
    print("=" * 50)
    
    if villa_test and reservation_test:
        print("🎉 All additional tests passed!")
    else:
        print("⚠️ Some additional tests failed")
        
    print(f"Villa Details Test: {'✅ PASS' if villa_test else '❌ FAIL'}")
    print(f"Reservation Flow Test: {'✅ PASS' if reservation_test else '❌ FAIL'}")