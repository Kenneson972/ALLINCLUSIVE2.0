#!/usr/bin/env python3
"""
Member Authentication and Management System Testing for KhanelConcept
Testing all new member endpoints and integration features
"""

import requests
import json
import uuid
from datetime import datetime, timedelta
import time

# Use the same backend URL as the existing test
BACKEND_URL = "https://cfc0e6ef-086c-461a-915c-2319466028f1.preview.emergentagent.com"
API_BASE_URL = f"{BACKEND_URL}/api"

class MemberSystemTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        self.test_member_id = None
        self.test_member_token = None
        self.test_member_email = None
        
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
    
    def test_member_registration(self):
        """Test member registration with full data"""
        try:
            # Generate unique test data
            unique_id = str(uuid.uuid4())[:8]
            test_data = {
                "firstName": "Marie-Claire",
                "lastName": "Dubois",
                "email": f"marie.dubois.{unique_id}@martinique.fr",
                "phone": "+596696123456",
                "password": "MonMotDePasse2025!",
                "birthDate": "1985-03-15",
                "nationality": "Française",
                "acceptTerms": True
            }
            
            response = self.session.post(
                f"{API_BASE_URL}/members/register",
                json=test_data,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "member" in data and "token" in data:
                    member = data["member"]
                    # Store for later tests
                    self.test_member_id = member["id"]
                    self.test_member_token = data["token"]
                    self.test_member_email = member["email"]
                    
                    # Verify member data
                    expected_fields = ["id", "firstName", "lastName", "email", "phone", "level", "points"]
                    missing_fields = [field for field in expected_fields if field not in member]
                    
                    if missing_fields:
                        self.log_test("Member Registration", False, 
                                    f"Missing member fields: {missing_fields}", member)
                        return False
                    
                    # Check initial values
                    if member["level"] == "Découvreur" and member["points"] == 100:
                        self.log_test("Member Registration", True, 
                                    f"Member registered successfully with welcome bonus", 
                                    f"Member: {member['firstName']} {member['lastName']}, Level: {member['level']}, Points: {member['points']}")
                        return True
                    else:
                        self.log_test("Member Registration", False, 
                                    f"Incorrect initial values - Level: {member['level']}, Points: {member['points']}")
                        return False
                else:
                    self.log_test("Member Registration", False, 
                                "Registration response missing required fields", data)
                    return False
            else:
                self.log_test("Member Registration", False, 
                            f"Registration failed with status {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("Member Registration", False, f"Registration error: {str(e)}")
            return False
    
    def test_member_login(self):
        """Test member login with email/password"""
        if not self.test_member_email:
            self.log_test("Member Login", False, "No test member email available")
            return False
            
        try:
            login_data = {
                "email": self.test_member_email,
                "password": "MonMotDePasse2025!",
                "remember": True
            }
            
            response = self.session.post(
                f"{API_BASE_URL}/members/login",
                json=login_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "member" in data and "token" in data:
                    member = data["member"]
                    token = data["token"]
                    
                    # Update token for future tests
                    self.test_member_token = token
                    
                    # Verify login response
                    if member["email"] == self.test_member_email and "password" not in member:
                        self.log_test("Member Login", True, 
                                    "Member login successful", 
                                    f"Member: {member['firstName']} {member['lastName']}")
                        return True
                    else:
                        self.log_test("Member Login", False, 
                                    "Login response contains password or wrong email", member)
                        return False
                else:
                    self.log_test("Member Login", False, 
                                "Login response missing required fields", data)
                    return False
            else:
                self.log_test("Member Login", False, 
                            f"Login failed with status {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("Member Login", False, f"Login error: {str(e)}")
            return False
    
    def test_member_token_verification(self):
        """Test token verification for members"""
        if not self.test_member_token:
            self.log_test("Member Token Verification", False, "No test member token available")
            return False
            
        try:
            token_data = {
                "token": self.test_member_token
            }
            
            response = self.session.post(
                f"{API_BASE_URL}/members/verify-token",
                json=token_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("valid") and "member" in data:
                    member = data["member"]
                    if member["id"] == self.test_member_id:
                        self.log_test("Member Token Verification", True, 
                                    "Token verification successful", 
                                    f"Verified member: {member['firstName']} {member['lastName']}")
                        return True
                    else:
                        self.log_test("Member Token Verification", False, 
                                    "Token verification returned wrong member")
                        return False
                else:
                    self.log_test("Member Token Verification", False, 
                                "Token verification response invalid", data)
                    return False
            else:
                self.log_test("Member Token Verification", False, 
                            f"Token verification failed with status {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("Member Token Verification", False, f"Token verification error: {str(e)}")
            return False
    
    def test_member_profile_retrieval(self):
        """Test profile retrieval"""
        if not self.test_member_id:
            self.log_test("Member Profile Retrieval", False, "No test member ID available")
            return False
            
        try:
            response = self.session.get(
                f"{API_BASE_URL}/members/profile/{self.test_member_id}",
                timeout=10
            )
            
            if response.status_code == 200:
                profile = response.json()
                expected_fields = ["id", "firstName", "lastName", "email", "phone", "level", "points"]
                missing_fields = [field for field in expected_fields if field not in profile]
                
                if missing_fields:
                    self.log_test("Member Profile Retrieval", False, 
                                f"Profile missing fields: {missing_fields}", profile)
                    return False
                
                if "password" in profile:
                    self.log_test("Member Profile Retrieval", False, 
                                "Profile contains password field (security issue)")
                    return False
                
                self.log_test("Member Profile Retrieval", True, 
                            "Profile retrieved successfully", 
                            f"Profile for: {profile['firstName']} {profile['lastName']}")
                return True
            else:
                self.log_test("Member Profile Retrieval", False, 
                            f"Profile retrieval failed with status {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("Member Profile Retrieval", False, f"Profile retrieval error: {str(e)}")
            return False
    
    def test_member_profile_update(self):
        """Test profile update"""
        if not self.test_member_id:
            self.log_test("Member Profile Update", False, "No test member ID available")
            return False
            
        try:
            update_data = {
                "phone": "+596696789012",
                "nationality": "Franco-Martiniquaise",
                "preferences": {
                    "notifications": {
                        "email": True,
                        "sms": True,
                        "push": False
                    },
                    "language": "fr"
                }
            }
            
            response = self.session.put(
                f"{API_BASE_URL}/members/profile/{self.test_member_id}",
                json=update_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "member" in data:
                    updated_member = data["member"]
                    
                    # Verify updates
                    if (updated_member["phone"] == update_data["phone"] and 
                        updated_member["nationality"] == update_data["nationality"]):
                        self.log_test("Member Profile Update", True, 
                                    "Profile updated successfully", 
                                    f"Updated phone: {updated_member['phone']}")
                        return True
                    else:
                        self.log_test("Member Profile Update", False, 
                                    "Profile update did not apply correctly", updated_member)
                        return False
                else:
                    self.log_test("Member Profile Update", False, 
                                "Profile update response invalid", data)
                    return False
            else:
                self.log_test("Member Profile Update", False, 
                            f"Profile update failed with status {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("Member Profile Update", False, f"Profile update error: {str(e)}")
            return False
    
    def test_member_reservations(self):
        """Test member reservations retrieval"""
        if not self.test_member_id:
            self.log_test("Member Reservations", False, "No test member ID available")
            return False
            
        try:
            response = self.session.get(
                f"{API_BASE_URL}/members/{self.test_member_id}/reservations",
                timeout=10
            )
            
            if response.status_code == 200:
                reservations = response.json()
                if isinstance(reservations, list):
                    self.log_test("Member Reservations", True, 
                                f"Member reservations retrieved successfully - {len(reservations)} reservations", 
                                f"Reservations count: {len(reservations)}")
                    return True
                else:
                    self.log_test("Member Reservations", False, 
                                "Reservations response is not a list", type(reservations))
                    return False
            else:
                self.log_test("Member Reservations", False, 
                            f"Reservations retrieval failed with status {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("Member Reservations", False, f"Reservations retrieval error: {str(e)}")
            return False
    
    def test_member_loyalty_info(self):
        """Test loyalty points and level info"""
        if not self.test_member_id:
            self.log_test("Member Loyalty Info", False, "No test member ID available")
            return False
            
        try:
            response = self.session.get(
                f"{API_BASE_URL}/members/{self.test_member_id}/loyalty",
                timeout=10
            )
            
            if response.status_code == 200:
                loyalty = response.json()
                expected_fields = ["member_id", "current_points", "current_level", "level_benefits", 
                                 "next_level", "points_to_next", "total_earned", "transactions"]
                missing_fields = [field for field in expected_fields if field not in loyalty]
                
                if missing_fields:
                    self.log_test("Member Loyalty Info", False, 
                                f"Loyalty info missing fields: {missing_fields}", loyalty)
                    return False
                
                # Verify loyalty levels
                if loyalty["current_level"] in ["Découvreur", "Explorateur", "Aventurier", "Légende"]:
                    self.log_test("Member Loyalty Info", True, 
                                f"Loyalty info retrieved successfully", 
                                f"Level: {loyalty['current_level']}, Points: {loyalty['current_points']}, Next: {loyalty['next_level']}")
                    return True
                else:
                    self.log_test("Member Loyalty Info", False, 
                                f"Invalid loyalty level: {loyalty['current_level']}")
                    return False
            else:
                self.log_test("Member Loyalty Info", False, 
                            f"Loyalty info retrieval failed with status {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("Member Loyalty Info", False, f"Loyalty info error: {str(e)}")
            return False
    
    def test_member_notifications(self):
        """Test notifications retrieval"""
        if not self.test_member_id:
            self.log_test("Member Notifications", False, "No test member ID available")
            return False
            
        try:
            response = self.session.get(
                f"{API_BASE_URL}/members/{self.test_member_id}/notifications",
                timeout=10
            )
            
            if response.status_code == 200:
                notifications = response.json()
                if isinstance(notifications, list):
                    # Should have at least welcome notification
                    if len(notifications) >= 1:
                        notification = notifications[0]
                        expected_fields = ["id", "memberId", "type", "title", "message", "isRead", "createdAt"]
                        missing_fields = [field for field in expected_fields if field not in notification]
                        
                        if missing_fields:
                            self.log_test("Member Notifications", False, 
                                        f"Notification missing fields: {missing_fields}", notification)
                            return False
                        
                        self.log_test("Member Notifications", True, 
                                    f"Notifications retrieved successfully - {len(notifications)} notifications", 
                                    f"Latest: {notification['title']}")
                        return True
                    else:
                        self.log_test("Member Notifications", True, 
                                    "Notifications endpoint working (no notifications yet)", 
                                    f"Notifications count: {len(notifications)}")
                        return True
                else:
                    self.log_test("Member Notifications", False, 
                                "Notifications response is not a list", type(notifications))
                    return False
            else:
                self.log_test("Member Notifications", False, 
                            f"Notifications retrieval failed with status {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("Member Notifications", False, f"Notifications error: {str(e)}")
            return False
    
    def test_member_wishlist_retrieval(self):
        """Test wishlist functionality"""
        if not self.test_member_id:
            self.log_test("Member Wishlist Retrieval", False, "No test member ID available")
            return False
            
        try:
            response = self.session.get(
                f"{API_BASE_URL}/members/{self.test_member_id}/wishlist",
                timeout=10
            )
            
            if response.status_code == 200:
                wishlist = response.json()
                if isinstance(wishlist, list):
                    self.log_test("Member Wishlist Retrieval", True, 
                                f"Wishlist retrieved successfully - {len(wishlist)} items", 
                                f"Wishlist items: {len(wishlist)}")
                    return True
                else:
                    self.log_test("Member Wishlist Retrieval", False, 
                                "Wishlist response is not a list", type(wishlist))
                    return False
            else:
                self.log_test("Member Wishlist Retrieval", False, 
                            f"Wishlist retrieval failed with status {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("Member Wishlist Retrieval", False, f"Wishlist retrieval error: {str(e)}")
            return False
    
    def test_add_villa_to_wishlist(self):
        """Test adding villa to wishlist"""
        if not self.test_member_id:
            self.log_test("Add Villa to Wishlist", False, "No test member ID available")
            return False
            
        try:
            # Use villa ID "1" (Villa F3 Petit Macabou)
            villa_id = "1"
            
            response = self.session.post(
                f"{API_BASE_URL}/members/{self.test_member_id}/wishlist",
                params={"villa_id": villa_id},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Add Villa to Wishlist", True, 
                                "Villa added to wishlist successfully", 
                                f"Added villa ID: {villa_id}")
                    return True
                else:
                    self.log_test("Add Villa to Wishlist", False, 
                                "Wishlist add response indicates failure", data)
                    return False
            else:
                self.log_test("Add Villa to Wishlist", False, 
                            f"Add to wishlist failed with status {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("Add Villa to Wishlist", False, f"Add to wishlist error: {str(e)}")
            return False
    
    def test_member_stats(self):
        """Test member statistics"""
        try:
            response = self.session.get(
                f"{API_BASE_URL}/members/stats",
                timeout=10
            )
            
            if response.status_code == 200:
                stats = response.json()
                expected_fields = ["total_members", "new_members_month", "level_distribution"]
                missing_fields = [field for field in expected_fields if field not in stats]
                
                if missing_fields:
                    self.log_test("Member Statistics", False, 
                                f"Stats missing fields: {missing_fields}", stats)
                    return False
                
                if stats["total_members"] >= 1:  # Should have at least our test member
                    self.log_test("Member Statistics", True, 
                                "Member statistics retrieved successfully", 
                                f"Total members: {stats['total_members']}")
                    return True
                else:
                    self.log_test("Member Statistics", False, 
                                f"Unexpected member count: {stats['total_members']}")
                    return False
            else:
                self.log_test("Member Statistics", False, 
                            f"Member stats failed with status {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("Member Statistics", False, f"Member stats error: {str(e)}")
            return False
    
    def test_reservation_loyalty_integration(self):
        """Test that new reservations automatically add loyalty points for members"""
        if not self.test_member_email:
            self.log_test("Reservation Loyalty Integration", False, "No test member email available")
            return False
            
        try:
            # Create a reservation for the member
            reservation_data = {
                "villa_id": "1",
                "customer_name": "Marie-Claire Dubois",
                "customer_email": self.test_member_email,
                "customer_phone": "+596696123456",
                "checkin_date": "2025-02-15",
                "checkout_date": "2025-02-22",
                "guests_count": 4,
                "message": "Test reservation for loyalty integration",
                "total_price": 850.0
            }
            
            response = self.session.post(
                f"{API_BASE_URL}/reservations",
                json=reservation_data,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("points_earned", 0) > 0:
                    points_earned = data["points_earned"]
                    
                    # Wait a moment for the points to be processed
                    time.sleep(2)
                    
                    # Check loyalty points were added
                    loyalty_response = self.session.get(
                        f"{API_BASE_URL}/members/{self.test_member_id}/loyalty",
                        timeout=10
                    )
                    
                    if loyalty_response.status_code == 200:
                        loyalty = loyalty_response.json()
                        # Should have initial 100 points + reservation points
                        expected_points = 100 + int(reservation_data["total_price"])
                        
                        if loyalty["current_points"] >= expected_points:
                            self.log_test("Reservation Loyalty Integration", True, 
                                        f"Reservation automatically added {points_earned} loyalty points", 
                                        f"Total points: {loyalty['current_points']}")
                            return True
                        else:
                            self.log_test("Reservation Loyalty Integration", False, 
                                        f"Points not added correctly - Expected: {expected_points}, Got: {loyalty['current_points']}")
                            return False
                    else:
                        self.log_test("Reservation Loyalty Integration", False, 
                                    "Could not verify loyalty points after reservation")
                        return False
                else:
                    self.log_test("Reservation Loyalty Integration", False, 
                                "Reservation created but no points earned", data)
                    return False
            else:
                self.log_test("Reservation Loyalty Integration", False, 
                            f"Reservation creation failed with status {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("Reservation Loyalty Integration", False, f"Reservation loyalty integration error: {str(e)}")
            return False
    
    def test_loyalty_level_progression(self):
        """Test loyalty level progression (Découvreur → Explorateur → Aventurier → Légende)"""
        if not self.test_member_id:
            self.log_test("Loyalty Level Progression", False, "No test member ID available")
            return False
            
        try:
            # Get current loyalty info
            response = self.session.get(
                f"{API_BASE_URL}/members/{self.test_member_id}/loyalty",
                timeout=10
            )
            
            if response.status_code == 200:
                loyalty = response.json()
                current_level = loyalty["current_level"]
                current_points = loyalty["current_points"]
                next_level = loyalty["next_level"]
                points_to_next = loyalty["points_to_next"]
                
                # Verify level progression logic
                level_progression = ["Découvreur", "Explorateur", "Aventurier", "Légende"]
                
                if current_level in level_progression:
                    current_index = level_progression.index(current_level)
                    
                    # Check if next level is correct
                    if current_index < len(level_progression) - 1:
                        expected_next = level_progression[current_index + 1]
                        if next_level == expected_next:
                            self.log_test("Loyalty Level Progression", True, 
                                        f"Loyalty level progression working correctly", 
                                        f"Current: {current_level} ({current_points} pts) → Next: {next_level} ({points_to_next} pts needed)")
                            return True
                        else:
                            self.log_test("Loyalty Level Progression", False, 
                                        f"Incorrect next level - Expected: {expected_next}, Got: {next_level}")
                            return False
                    else:
                        # Already at max level
                        if next_level is None:
                            self.log_test("Loyalty Level Progression", True, 
                                        f"Member at maximum level (Légende)", 
                                        f"Current: {current_level} ({current_points} pts)")
                            return True
                        else:
                            self.log_test("Loyalty Level Progression", False, 
                                        f"Max level member should have next_level=None, got: {next_level}")
                            return False
                else:
                    self.log_test("Loyalty Level Progression", False, 
                                f"Invalid current level: {current_level}")
                    return False
            else:
                self.log_test("Loyalty Level Progression", False, 
                            f"Could not retrieve loyalty info for progression test")
                return False
                
        except Exception as e:
            self.log_test("Loyalty Level Progression", False, f"Loyalty level progression error: {str(e)}")
            return False
    
    def test_notification_system_integration(self):
        """Test notification system when creating reservations for members"""
        if not self.test_member_id:
            self.log_test("Notification System Integration", False, "No test member ID available")
            return False
            
        try:
            # Get current notification count
            initial_response = self.session.get(
                f"{API_BASE_URL}/members/{self.test_member_id}/notifications",
                timeout=10
            )
            
            if initial_response.status_code != 200:
                self.log_test("Notification System Integration", False, 
                            "Could not get initial notifications")
                return False
            
            initial_notifications = initial_response.json()
            initial_count = len(initial_notifications)
            
            # Create another reservation to trigger notification
            reservation_data = {
                "villa_id": "2",
                "customer_name": "Marie-Claire Dubois",
                "customer_email": self.test_member_email,
                "customer_phone": "+596696123456",
                "checkin_date": "2025-03-10",
                "checkout_date": "2025-03-17",
                "guests_count": 6,
                "message": "Test reservation for notification integration",
                "total_price": 1300.0
            }
            
            response = self.session.post(
                f"{API_BASE_URL}/reservations",
                json=reservation_data,
                timeout=15
            )
            
            if response.status_code == 200:
                # Wait for notification to be created
                time.sleep(3)
                
                # Check for new notifications
                new_response = self.session.get(
                    f"{API_BASE_URL}/members/{self.test_member_id}/notifications",
                    timeout=10
                )
                
                if new_response.status_code == 200:
                    new_notifications = new_response.json()
                    new_count = len(new_notifications)
                    
                    if new_count > initial_count:
                        # Check if the latest notification is about the reservation
                        latest_notification = new_notifications[0]  # Should be sorted by createdAt desc
                        
                        if (latest_notification["type"] == "reservation" and 
                            "réservation" in latest_notification["message"].lower()):
                            self.log_test("Notification System Integration", True, 
                                        f"Reservation notification created successfully", 
                                        f"Notification: {latest_notification['title']}")
                            return True
                        else:
                            self.log_test("Notification System Integration", False, 
                                        f"New notification is not about reservation", latest_notification)
                            return False
                    else:
                        self.log_test("Notification System Integration", False, 
                                    f"No new notification created - Count: {initial_count} → {new_count}")
                        return False
                else:
                    self.log_test("Notification System Integration", False, 
                                "Could not retrieve notifications after reservation")
                    return False
            else:
                self.log_test("Notification System Integration", False, 
                            f"Reservation creation failed for notification test")
                return False
                
        except Exception as e:
            self.log_test("Notification System Integration", False, f"Notification system integration error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all member system tests"""
        print("🌴 Starting KhanelConcept Member Authentication & Management System Tests")
        print(f"Testing against: {API_BASE_URL}")
        print("=" * 80)
        
        # Test member registration and authentication
        print("\n👤 Testing Member Registration & Authentication...")
        if not self.test_member_registration():
            print("❌ Member registration failed - stopping member tests")
            return False
        
        self.test_member_login()
        self.test_member_token_verification()
        
        # Test member profile and data
        print("\n📋 Testing Member Profile & Data...")
        self.test_member_profile_retrieval()
        self.test_member_profile_update()
        
        # Test member features
        print("\n🎯 Testing Member Features...")
        self.test_member_reservations()
        self.test_member_loyalty_info()
        self.test_member_notifications()
        self.test_member_wishlist_retrieval()
        self.test_add_villa_to_wishlist()
        self.test_member_stats()
        
        # Test integration features
        print("\n🔗 Testing Integration Features...")
        self.test_reservation_loyalty_integration()
        self.test_loyalty_level_progression()
        self.test_notification_system_integration()
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 MEMBER SYSTEM TEST SUMMARY")
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
        else:
            print("\n🎉 All member system tests passed!")
        
        return passed == total

if __name__ == "__main__":
    tester = MemberSystemTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All member authentication and management tests passed!")
    else:
        print("\n⚠️  Some member system tests failed - check details above")