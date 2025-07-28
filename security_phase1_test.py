#!/usr/bin/env python3
"""
PHASE 1 - SÉCURITÉ CRITIQUE Testing for KhanelConcept
Testing the newly implemented security features:
1. Admin 2FA System
2. Member Email Verification 
3. Security Logging and Credentials
"""

import requests
import json
import os
import time
import random
import string
from datetime import datetime

# Load backend URL from environment or use default
BACKEND_URL = "https://f0dc2e11-c7f8-4f89-86b8-00ffc3281185.preview.emergentagent.com"
API_BASE_URL = f"{BACKEND_URL}/api"

# Admin credentials from environment variables (Phase 1 security improvement)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "khanelconcept2025"

class SecurityPhase1Tester:
    def __init__(self):
        self.session = requests.Session()
        self.admin_token = None
        self.test_results = []
        self.test_member_email = None
        self.test_member_data = None
        
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
    
    def generate_test_email(self):
        """Generate unique test email"""
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"test.security.{random_suffix}@example.com"
    
    def generate_strong_password(self):
        """Generate a strong password for testing"""
        return "SecureTest2025!"
    
    # ========== ADMIN 2FA SYSTEM TESTS ==========
    
    def test_admin_login_without_2fa(self):
        """Test admin login without 2FA (should work initially)"""
        try:
            login_data = {
                "username": ADMIN_USERNAME,
                "password": ADMIN_PASSWORD
            }
            
            response = self.session.post(
                f"{API_BASE_URL}/admin/login",
                json=login_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data and "token_type" in data:
                    self.admin_token = data["access_token"]
                    self.log_test("Admin Login (No 2FA)", True, 
                                "Admin login successful without 2FA", 
                                f"Token type: {data['token_type']}")
                    return True
                else:
                    self.log_test("Admin Login (No 2FA)", False, 
                                "Login response missing token fields", data)
                    return False
            else:
                self.log_test("Admin Login (No 2FA)", False, 
                            f"Login failed with status {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("Admin Login (No 2FA)", False, f"Login error: {str(e)}")
            return False
    
    def test_2fa_status_check(self):
        """Test 2FA status endpoint"""
        try:
            response = self.session.get(f"{API_BASE_URL}/admin/2fa-status", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "enabled" in data and "configured" in data:
                    self.log_test("2FA Status Check", True, 
                                f"2FA status retrieved - Enabled: {data['enabled']}, Configured: {data['configured']}", 
                                data)
                    return True, data
                else:
                    self.log_test("2FA Status Check", False, 
                                "Status response missing required fields", data)
                    return False, None
            else:
                self.log_test("2FA Status Check", False, 
                            f"Status check failed with status {response.status_code}", 
                            response.text)
                return False, None
                
        except Exception as e:
            self.log_test("2FA Status Check", False, f"Status check error: {str(e)}")
            return False, None
    
    def test_2fa_setup(self):
        """Test 2FA setup process"""
        try:
            setup_data = {
                "password": ADMIN_PASSWORD
            }
            
            response = self.session.post(
                f"{API_BASE_URL}/admin/setup-2fa",
                json=setup_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ["qr_code", "secret", "message"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("2FA Setup", False, 
                                f"Setup response missing fields: {missing_fields}", data)
                    return False, None
                
                # Verify QR code format
                if data["qr_code"].startswith("data:image/png;base64,"):
                    self.log_test("2FA Setup", True, 
                                "2FA setup successful - QR code and secret generated", 
                                f"Secret length: {len(data['secret'])}")
                    return True, data["secret"]
                else:
                    self.log_test("2FA Setup", False, 
                                "Invalid QR code format", data["qr_code"][:50])
                    return False, None
            else:
                self.log_test("2FA Setup", False, 
                            f"Setup failed with status {response.status_code}", 
                            response.text)
                return False, None
                
        except Exception as e:
            self.log_test("2FA Setup", False, f"Setup error: {str(e)}")
            return False, None
    
    def test_2fa_enable_with_invalid_code(self):
        """Test 2FA enable with invalid TOTP code"""
        try:
            enable_data = {
                "totp_code": "123456"  # Invalid code
            }
            
            response = self.session.post(
                f"{API_BASE_URL}/admin/enable-2fa",
                json=enable_data,
                timeout=10
            )
            
            if response.status_code == 400:
                self.log_test("2FA Enable (Invalid Code)", True, 
                            "2FA enable correctly rejected invalid code", 
                            response.json().get("detail", "No detail"))
                return True
            else:
                self.log_test("2FA Enable (Invalid Code)", False, 
                            f"Expected 400 error, got {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("2FA Enable (Invalid Code)", False, f"Enable test error: {str(e)}")
            return False
    
    def test_2fa_disable_without_setup(self):
        """Test 2FA disable without proper setup"""
        try:
            disable_data = {
                "password": ADMIN_PASSWORD,
                "totp_code": "123456"
            }
            
            response = self.session.post(
                f"{API_BASE_URL}/admin/disable-2fa",
                json=disable_data,
                timeout=10
            )
            
            # Should fail because 2FA is not properly enabled
            if response.status_code in [400, 401]:
                self.log_test("2FA Disable (Not Setup)", True, 
                            "2FA disable correctly rejected - not properly setup", 
                            response.json().get("detail", "No detail"))
                return True
            else:
                self.log_test("2FA Disable (Not Setup)", False, 
                            f"Expected 400/401 error, got {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("2FA Disable (Not Setup)", False, f"Disable test error: {str(e)}")
            return False
    
    def test_admin_token_verification(self):
        """Test admin token verification"""
        if not self.admin_token:
            self.log_test("Admin Token Verification", False, "No admin token available")
            return False
        
        try:
            token_data = {
                "token": self.admin_token
            }
            
            response = self.session.post(
                f"{API_BASE_URL}/admin/verify-token",
                json=token_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("valid") and data.get("username") == ADMIN_USERNAME:
                    self.log_test("Admin Token Verification", True, 
                                "Admin token verification successful", 
                                f"Username: {data['username']}")
                    return True
                else:
                    self.log_test("Admin Token Verification", False, 
                                "Token verification response invalid", data)
                    return False
            else:
                self.log_test("Admin Token Verification", False, 
                            f"Token verification failed with status {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("Admin Token Verification", False, f"Token verification error: {str(e)}")
            return False
    
    # ========== MEMBER EMAIL VERIFICATION TESTS ==========
    
    def test_member_registration_with_verification(self):
        """Test member registration creates unverified account"""
        try:
            self.test_member_email = self.generate_test_email()
            self.test_member_data = {
                "firstName": "Marie-Claire",
                "lastName": "Dubois",
                "email": self.test_member_email,
                "phone": "+596123456789",
                "password": self.generate_strong_password(),
                "birthDate": "1985-03-15",
                "acceptTerms": True
            }
            
            response = self.session.post(
                f"{API_BASE_URL}/members/register",
                json=self.test_member_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if (data.get("success") and 
                    data.get("verification_required") and 
                    "member" in data):
                    
                    member = data["member"]
                    if (not member.get("isVerified", True) and 
                        not member.get("isActive", True)):
                        
                        self.log_test("Member Registration (Unverified)", True, 
                                    "Member registration successful - account unverified", 
                                    f"Email: {self.test_member_email}, Verified: {member.get('isVerified')}")
                        return True
                    else:
                        self.log_test("Member Registration (Unverified)", False, 
                                    "Member account should be unverified initially", 
                                    f"Verified: {member.get('isVerified')}, Active: {member.get('isActive')}")
                        return False
                else:
                    self.log_test("Member Registration (Unverified)", False, 
                                "Registration response missing required fields", data)
                    return False
            else:
                self.log_test("Member Registration (Unverified)", False, 
                            f"Registration failed with status {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("Member Registration (Unverified)", False, f"Registration error: {str(e)}")
            return False
    
    def test_member_login_blocked_unverified(self):
        """Test member login is blocked for unverified email"""
        if not self.test_member_email or not self.test_member_data:
            self.log_test("Member Login (Blocked Unverified)", False, "No test member data available")
            return False
        
        try:
            login_data = {
                "email": self.test_member_email,
                "password": self.test_member_data["password"]
            }
            
            response = self.session.post(
                f"{API_BASE_URL}/members/login",
                json=login_data,
                timeout=10
            )
            
            if response.status_code == 401:
                error_detail = response.json().get("detail", "")
                if "non vérifié" in error_detail.lower() or "not verified" in error_detail.lower():
                    self.log_test("Member Login (Blocked Unverified)", True, 
                                "Login correctly blocked for unverified email", 
                                f"Error: {error_detail}")
                    return True
                else:
                    self.log_test("Member Login (Blocked Unverified)", False, 
                                "Wrong error message for unverified login", 
                                f"Error: {error_detail}")
                    return False
            else:
                self.log_test("Member Login (Blocked Unverified)", False, 
                            f"Expected 401 error, got {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("Member Login (Blocked Unverified)", False, f"Login test error: {str(e)}")
            return False
    
    def test_email_verification_with_invalid_code(self):
        """Test email verification with invalid code"""
        if not self.test_member_email:
            self.log_test("Email Verification (Invalid Code)", False, "No test member email available")
            return False
        
        try:
            verification_data = {
                "email": self.test_member_email,
                "verification_code": "123456"  # Invalid code
            }
            
            response = self.session.post(
                f"{API_BASE_URL}/members/verify-email",
                json=verification_data,
                timeout=10
            )
            
            if response.status_code == 400:
                error_detail = response.json().get("detail", "")
                if "invalide" in error_detail.lower() or "invalid" in error_detail.lower():
                    self.log_test("Email Verification (Invalid Code)", True, 
                                "Email verification correctly rejected invalid code", 
                                f"Error: {error_detail}")
                    return True
                else:
                    self.log_test("Email Verification (Invalid Code)", False, 
                                "Wrong error message for invalid code", 
                                f"Error: {error_detail}")
                    return False
            else:
                self.log_test("Email Verification (Invalid Code)", False, 
                            f"Expected 400 error, got {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("Email Verification (Invalid Code)", False, f"Verification test error: {str(e)}")
            return False
    
    def test_resend_verification_email(self):
        """Test resending verification email"""
        if not self.test_member_email:
            self.log_test("Resend Verification Email", False, "No test member email available")
            return False
        
        try:
            resend_data = {
                "email": self.test_member_email
            }
            
            response = self.session.post(
                f"{API_BASE_URL}/members/resend-verification",
                json=resend_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Resend Verification Email", True, 
                                "Verification email resend successful", 
                                data.get("message", "No message"))
                    return True
                else:
                    self.log_test("Resend Verification Email", False, 
                                "Resend response indicates failure", data)
                    return False
            else:
                self.log_test("Resend Verification Email", False, 
                            f"Resend failed with status {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("Resend Verification Email", False, f"Resend error: {str(e)}")
            return False
    
    # ========== SECURITY IMPROVEMENTS TESTS ==========
    
    def test_security_headers(self):
        """Test security headers are present"""
        try:
            response = self.session.get(f"{API_BASE_URL}/health", timeout=10)
            
            required_headers = {
                "X-Content-Type-Options": "nosniff",
                "X-Frame-Options": "DENY", 
                "X-XSS-Protection": "1; mode=block",
                "Strict-Transport-Security": "max-age=31536000; includeSubDomains"
            }
            
            missing_headers = []
            present_headers = {}
            
            for header, expected_value in required_headers.items():
                actual_value = response.headers.get(header)
                if actual_value:
                    present_headers[header] = actual_value
                    if expected_value not in actual_value:
                        missing_headers.append(f"{header} (wrong value: {actual_value})")
                else:
                    missing_headers.append(header)
            
            if not missing_headers:
                self.log_test("Security Headers", True, 
                            "All required security headers present", 
                            present_headers)
                return True
            else:
                self.log_test("Security Headers", False, 
                            f"Missing or incorrect security headers: {missing_headers}", 
                            present_headers)
                return False
                
        except Exception as e:
            self.log_test("Security Headers", False, f"Security headers test error: {str(e)}")
            return False
    
    def test_rate_limiting_protection(self):
        """Test rate limiting protection"""
        try:
            # Make multiple rapid requests to test rate limiting
            rapid_requests = 0
            rate_limited = False
            
            for i in range(65):  # Try to exceed 60 requests per minute limit
                response = self.session.get(f"{API_BASE_URL}/health", timeout=5)
                rapid_requests += 1
                
                if response.status_code == 429:
                    rate_limited = True
                    break
                
                # Small delay to avoid overwhelming
                time.sleep(0.01)
            
            if rate_limited:
                self.log_test("Rate Limiting Protection", True, 
                            f"Rate limiting activated after {rapid_requests} requests", 
                            "429 Too Many Requests received")
                return True
            else:
                self.log_test("Rate Limiting Protection", False, 
                            f"No rate limiting detected after {rapid_requests} requests", 
                            "Rate limiting may not be working")
                return False
                
        except Exception as e:
            self.log_test("Rate Limiting Protection", False, f"Rate limiting test error: {str(e)}")
            return False
    
    def test_path_traversal_protection(self):
        """Test path traversal attack protection"""
        try:
            # Test various path traversal payloads
            traversal_payloads = [
                "../../../etc/passwd",
                "..%2F..%2F..%2Fetc%2Fpasswd",
                "....//....//....//etc/passwd",
                "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd"
            ]
            
            blocked_attacks = 0
            
            for payload in traversal_payloads:
                try:
                    response = self.session.get(f"{API_BASE_URL}/{payload}", timeout=5)
                    
                    if response.status_code == 400:
                        blocked_attacks += 1
                    elif response.status_code == 200 and "root:" in response.text:
                        # This would be a serious vulnerability
                        self.log_test("Path Traversal Protection", False, 
                                    f"Path traversal attack succeeded with payload: {payload}", 
                                    "System files accessible!")
                        return False
                        
                except requests.exceptions.RequestException:
                    # Connection errors are acceptable for blocked requests
                    blocked_attacks += 1
            
            if blocked_attacks >= len(traversal_payloads) * 0.8:  # At least 80% blocked
                self.log_test("Path Traversal Protection", True, 
                            f"Path traversal protection working - {blocked_attacks}/{len(traversal_payloads)} attacks blocked", 
                            "System protected against directory traversal")
                return True
            else:
                self.log_test("Path Traversal Protection", False, 
                            f"Insufficient path traversal protection - only {blocked_attacks}/{len(traversal_payloads)} attacks blocked", 
                            "Security vulnerability detected")
                return False
                
        except Exception as e:
            self.log_test("Path Traversal Protection", False, f"Path traversal test error: {str(e)}")
            return False
    
    def test_password_strength_validation(self):
        """Test password strength validation in member registration"""
        try:
            weak_passwords = [
                "123456",
                "password", 
                "admin",
                "123",
                "qwerty",
                "abc123"
            ]
            
            rejected_passwords = 0
            
            for weak_password in weak_passwords:
                test_email = self.generate_test_email()
                registration_data = {
                    "firstName": "Test",
                    "lastName": "User",
                    "email": test_email,
                    "phone": "+596123456789",
                    "password": weak_password,
                    "acceptTerms": True
                }
                
                response = self.session.post(
                    f"{API_BASE_URL}/members/register",
                    json=registration_data,
                    timeout=10
                )
                
                if response.status_code == 422:  # Validation error
                    error_detail = response.json().get("detail", [])
                    if any("password" in str(error).lower() for error in error_detail):
                        rejected_passwords += 1
                
                # Small delay between attempts
                time.sleep(0.1)
            
            if rejected_passwords >= len(weak_passwords) * 0.8:  # At least 80% rejected
                self.log_test("Password Strength Validation", True, 
                            f"Password validation working - {rejected_passwords}/{len(weak_passwords)} weak passwords rejected", 
                            "Strong password policy enforced")
                return True
            else:
                self.log_test("Password Strength Validation", False, 
                            f"Weak password validation insufficient - only {rejected_passwords}/{len(weak_passwords)} passwords rejected", 
                            "Password policy needs strengthening")
                return False
                
        except Exception as e:
            self.log_test("Password Strength Validation", False, f"Password validation test error: {str(e)}")
            return False
    
    def test_brute_force_protection(self):
        """Test brute force protection on member login"""
        try:
            # Create a test member first (if not already created)
            if not self.test_member_email:
                self.test_member_registration_with_verification()
            
            if not self.test_member_email:
                self.log_test("Brute Force Protection", False, "No test member available")
                return False
            
            # Attempt multiple failed logins
            failed_attempts = 0
            blocked = False
            
            for i in range(7):  # Try 7 failed attempts
                login_data = {
                    "email": self.test_member_email,
                    "password": "WrongPassword123!"
                }
                
                response = self.session.post(
                    f"{API_BASE_URL}/members/login",
                    json=login_data,
                    timeout=10
                )
                
                failed_attempts += 1
                
                if response.status_code == 429:  # Too Many Requests
                    blocked = True
                    break
                
                # Small delay between attempts
                time.sleep(0.5)
            
            if blocked:
                self.log_test("Brute Force Protection", True, 
                            f"Brute force protection activated after {failed_attempts} failed attempts", 
                            "Account temporarily locked")
                return True
            else:
                self.log_test("Brute Force Protection", False, 
                            f"No brute force protection detected after {failed_attempts} failed attempts", 
                            "Brute force protection may be insufficient")
                return False
                
        except Exception as e:
            self.log_test("Brute Force Protection", False, f"Brute force test error: {str(e)}")
            return False
    
    def run_all_security_tests(self):
        """Run all Phase 1 security tests"""
        print("🔒 Starting KhanelConcept PHASE 1 - SÉCURITÉ CRITIQUE Tests")
        print("🎯 Focus: Admin 2FA, Member Email Verification, Security Improvements")
        print(f"Testing against: {API_BASE_URL}")
        print("=" * 80)
        
        # Test basic connectivity
        try:
            response = self.session.get(f"{API_BASE_URL}/health", timeout=10)
            if response.status_code != 200:
                print("❌ API health check failed - stopping tests")
                return False
            print("✅ API connectivity confirmed")
        except Exception as e:
            print(f"❌ API connectivity failed: {e}")
            return False
        
        # ADMIN 2FA SYSTEM TESTS
        print("\n🔐 ADMIN 2FA SYSTEM TESTS")
        print("-" * 40)
        self.test_admin_login_without_2fa()
        self.test_2fa_status_check()
        self.test_2fa_setup()
        self.test_2fa_enable_with_invalid_code()
        self.test_2fa_disable_without_setup()
        self.test_admin_token_verification()
        
        # MEMBER EMAIL VERIFICATION TESTS
        print("\n📧 MEMBER EMAIL VERIFICATION TESTS")
        print("-" * 40)
        self.test_member_registration_with_verification()
        self.test_member_login_blocked_unverified()
        self.test_email_verification_with_invalid_code()
        self.test_resend_verification_email()
        
        # SECURITY IMPROVEMENTS TESTS
        print("\n🛡️ SECURITY IMPROVEMENTS TESTS")
        print("-" * 40)
        self.test_security_headers()
        self.test_rate_limiting_protection()
        self.test_path_traversal_protection()
        self.test_password_strength_validation()
        self.test_brute_force_protection()
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 PHASE 1 SECURITY TEST SUMMARY")
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
            print("\n❌ FAILED TESTS:")
            for test in failed_tests:
                print(f"  - {test['test']}: {test['message']}")
        
        # Show passed tests summary
        passed_tests = [result for result in self.test_results if result["success"]]
        if passed_tests:
            print(f"\n✅ PASSED TESTS ({len(passed_tests)}):")
            for test in passed_tests:
                print(f"  - {test['test']}: {test['message']}")
        
        # Security assessment
        security_score = (passed / total) * 100
        print(f"\n🔒 SECURITY ASSESSMENT:")
        if security_score >= 90:
            print(f"🟢 EXCELLENT SECURITY ({security_score:.1f}%) - Phase 1 implementation successful")
        elif security_score >= 75:
            print(f"🟡 GOOD SECURITY ({security_score:.1f}%) - Minor improvements needed")
        elif security_score >= 50:
            print(f"🟠 MODERATE SECURITY ({security_score:.1f}%) - Several issues need attention")
        else:
            print(f"🔴 POOR SECURITY ({security_score:.1f}%) - Critical issues require immediate attention")
        
        return passed == total

if __name__ == "__main__":
    tester = SecurityPhase1Tester()
    success = tester.run_all_security_tests()
    
    if success:
        print("\n🎉 All Phase 1 security tests passed!")
    else:
        print("\n⚠️  Some security tests failed - check details above")