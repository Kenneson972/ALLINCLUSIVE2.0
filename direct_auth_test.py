#!/usr/bin/env python3
"""
Direct Authentication Function Test
"""

import sys
import os
sys.path.append('/app/backend')
os.chdir('/app/backend')

try:
    from server import authenticate_user, create_access_token, verify_token, ADMIN_USERS
    
    print("🔐 Testing Admin Authentication Functions Directly")
    print("=" * 50)
    
    # Check admin users data
    print("📋 Admin Users Configuration:")
    for username, user_data in ADMIN_USERS.items():
        print(f"   Username: {username}")
        print(f"   Role: {user_data['role']}")
        print(f"   Has Password Hash: {'hashed_password' in user_data}")
    
    # Test authentication function
    print("\n📍 Testing authenticate_user function")
    user = authenticate_user("admin", "khanelconcept2025")
    if user:
        print("   ✅ AUTHENTICATION SUCCESS")
        print(f"   User: {user['username']}, Role: {user['role']}")
        
        # Test token creation
        print("\n📍 Testing create_access_token function")
        token = create_access_token(data={"sub": user["username"], "role": user["role"]})
        print(f"   ✅ TOKEN CREATED: {len(token)} characters")
        print(f"   Token preview: {token[:50]}...")
        
        # Test token verification
        print("\n📍 Testing verify_token function")
        username = verify_token(token)
        if username:
            print(f"   ✅ TOKEN VERIFICATION SUCCESS: {username}")
            print("\n🎉 ALL AUTHENTICATION FUNCTIONS WORKING CORRECTLY")
        else:
            print("   ❌ TOKEN VERIFICATION FAILED")
    else:
        print("   ❌ AUTHENTICATION FAILED")
        
        # Test with wrong password
        print("\n📍 Testing with wrong password")
        wrong_user = authenticate_user("admin", "wrongpassword")
        if not wrong_user:
            print("   ✅ CORRECTLY REJECTED wrong password")
        else:
            print("   ❌ INCORRECTLY ACCEPTED wrong password")

except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()