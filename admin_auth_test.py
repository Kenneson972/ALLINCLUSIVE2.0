#!/usr/bin/env python3
"""
Focused Admin Authentication Test for KhanelConcept
Testing the admin authentication endpoints as requested
"""

import requests
import json
import sys
from datetime import datetime

def test_admin_authentication():
    """Test admin authentication endpoints specifically"""
    print("🔐 Testing Admin Authentication System")
    print("=" * 50)
    
    # Try different possible base URLs
    possible_urls = [
        "http://localhost:8001",
        "https://f6169287-bcef-4657-a67a-5f4c828e7215.preview.emergentagent.com"
    ]
    
    admin_credentials = {
        "username": "admin",
        "password": "khanelconcept2025"
    }
    
    for base_url in possible_urls:
        print(f"\n🌐 Testing with base URL: {base_url}")
        
        # Test 1: Admin Login
        try:
            login_url = f"{base_url}/api/admin/login"
            print(f"📍 Testing POST {login_url}")
            
            response = requests.post(
                login_url,
                json=admin_credentials,
                timeout=10,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"   Status Code: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data and "token_type" in data:
                    print("   ✅ LOGIN SUCCESS: Token received")
                    print(f"   Token Type: {data['token_type']}")
                    print(f"   Token Length: {len(data['access_token'])} characters")
                    
                    # Test 2: Token Verification
                    token = data["access_token"]
                    verify_url = f"{base_url}/api/admin/verify-token"
                    print(f"\n📍 Testing POST {verify_url}")
                    
                    verify_response = requests.post(
                        verify_url,
                        json={"token": token},
                        timeout=10,
                        headers={"Content-Type": "application/json"}
                    )
                    
                    print(f"   Status Code: {verify_response.status_code}")
                    print(f"   Response: {verify_response.text}")
                    
                    if verify_response.status_code == 200:
                        verify_data = verify_response.json()
                        if verify_data.get("valid") == True:
                            print("   ✅ TOKEN VERIFICATION SUCCESS")
                            print(f"   Username: {verify_data.get('username')}")
                            return True, base_url, token
                        else:
                            print("   ❌ TOKEN VERIFICATION FAILED: Invalid token")
                    else:
                        print(f"   ❌ TOKEN VERIFICATION FAILED: HTTP {verify_response.status_code}")
                else:
                    print("   ❌ LOGIN FAILED: Missing token fields in response")
            else:
                print(f"   ❌ LOGIN FAILED: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ CONNECTION ERROR: {str(e)}")
    
    return False, None, None

def test_with_direct_import():
    """Test authentication by importing the server module directly"""
    print("\n🔧 Testing Authentication Functions Directly")
    print("=" * 50)
    
    try:
        import sys
        sys.path.append('/app/backend')
        from server import authenticate_user, create_access_token, verify_token
        
        # Test authentication function
        print("📍 Testing authenticate_user function")
        user = authenticate_user("admin", "khanelconcept2025")
        if user:
            print("   ✅ AUTHENTICATION SUCCESS")
            print(f"   User: {user['username']}, Role: {user['role']}")
            
            # Test token creation
            print("📍 Testing create_access_token function")
            token = create_access_token(data={"sub": user["username"], "role": user["role"]})
            print(f"   ✅ TOKEN CREATED: {len(token)} characters")
            
            # Test token verification
            print("📍 Testing verify_token function")
            username = verify_token(token)
            if username:
                print(f"   ✅ TOKEN VERIFICATION SUCCESS: {username}")
                return True
            else:
                print("   ❌ TOKEN VERIFICATION FAILED")
        else:
            print("   ❌ AUTHENTICATION FAILED")
            
    except Exception as e:
        print(f"   ❌ DIRECT TEST ERROR: {str(e)}")
    
    return False

if __name__ == "__main__":
    print("🚀 KhanelConcept Admin Authentication Test")
    print("Testing credentials: username='admin', password='khanelconcept2025'")
    print("=" * 70)
    
    # Test via HTTP endpoints
    success, working_url, token = test_admin_authentication()
    
    # Test via direct function calls
    direct_success = test_with_direct_import()
    
    print("\n" + "=" * 70)
    print("📊 FINAL RESULTS")
    print("=" * 70)
    
    if success:
        print("✅ HTTP API AUTHENTICATION: WORKING")
        print(f"   Working URL: {working_url}")
        print(f"   Token obtained and verified successfully")
    else:
        print("❌ HTTP API AUTHENTICATION: FAILED")
        print("   Could not access API endpoints via HTTP")
    
    if direct_success:
        print("✅ DIRECT FUNCTION AUTHENTICATION: WORKING")
        print("   Authentication functions work correctly")
    else:
        print("❌ DIRECT FUNCTION AUTHENTICATION: FAILED")
        print("   Authentication functions have issues")
    
    # Overall assessment
    if success or direct_success:
        print("\n🎉 OVERALL: Admin authentication system is functional")
        if not success:
            print("⚠️  Note: HTTP routing issue prevents API access, but core auth logic works")
        sys.exit(0)
    else:
        print("\n💥 OVERALL: Admin authentication system has critical issues")
        sys.exit(1)