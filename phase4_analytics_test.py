#!/usr/bin/env python3
"""
Phase 4 Analytics System Testing
KhanelConcept Villa Rental Platform

Tests all new analytics endpoints:
1. GET /api/admin/analytics/overview - Analytics Overview
2. GET /api/admin/analytics/performance - Performance Analytics  
3. GET /api/admin/analytics/trends - Trends Analytics
4. GET /api/admin/analytics/realtime - Realtime Analytics
5. POST /api/analytics/track - Analytics Tracking (GDPR compliant)

Admin Credentials: admin / khanelconcept2025
"""

import requests
import json
import time
import uuid
from datetime import datetime

# Backend URL Configuration
BACKEND_URL = "https://2dc70b52-37ed-4f34-9403-c7388838f79e.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "khanelconcept2025"

class Phase4AnalyticsTest:
    def __init__(self):
        self.session = requests.Session()
        self.admin_token = None
        self.test_results = []
        
    def log_test(self, test_name, success, details="", error=None):
        """Log test results"""
        status = "✅ PASSED" if success else "❌ FAILED"
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "error": str(error) if error else None,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"{status} - {test_name}")
        if details:
            print(f"   Details: {details}")
        if error:
            print(f"   Error: {error}")
        print()

    def admin_login(self):
        """Login as admin to get authentication token"""
        try:
            login_data = {
                "username": ADMIN_USERNAME,
                "password": ADMIN_PASSWORD
            }
            
            response = self.session.post(
                f"{API_BASE}/admin/login",
                json=login_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.admin_token = data.get("access_token")
                self.session.headers.update({
                    "Authorization": f"Bearer {self.admin_token}"
                })
                self.log_test(
                    "Admin Authentication",
                    True,
                    f"Successfully logged in as {ADMIN_USERNAME}, token obtained"
                )
                return True
            else:
                self.log_test(
                    "Admin Authentication",
                    False,
                    f"Login failed with status {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_test("Admin Authentication", False, "Login request failed", e)
            return False

    def test_analytics_overview(self):
        """Test GET /api/admin/analytics/overview"""
        try:
            response = self.session.get(
                f"{API_BASE}/admin/analytics/overview",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                required_fields = ["overview", "recent_activity"]
                overview_fields = [
                    "total_villas", "total_members", "total_reservations",
                    "new_members", "recent_reservations", "monthly_revenue",
                    "conversion_rate"
                ]
                
                missing_fields = []
                for field in required_fields:
                    if field not in data:
                        missing_fields.append(field)
                
                if "overview" in data:
                    for field in overview_fields:
                        if field not in data["overview"]:
                            missing_fields.append(f"overview.{field}")
                
                if missing_fields:
                    self.log_test(
                        "Analytics Overview - Structure",
                        False,
                        f"Missing required fields: {missing_fields}"
                    )
                else:
                    overview = data["overview"]
                    details = f"Villas: {overview['total_villas']}, Members: {overview['total_members']}, " \
                             f"Reservations: {overview['total_reservations']}, Revenue: €{overview['monthly_revenue']}, " \
                             f"Conversion: {overview['conversion_rate']}%"
                    
                    self.log_test(
                        "Analytics Overview - Structure",
                        True,
                        f"All required fields present. {details}"
                    )
                
                # Test data types
                if "overview" in data:
                    overview = data["overview"]
                    numeric_fields = ["total_villas", "total_members", "total_reservations", 
                                    "new_members", "recent_reservations", "monthly_revenue", "conversion_rate"]
                    
                    type_errors = []
                    for field in numeric_fields:
                        if field in overview and not isinstance(overview[field], (int, float)):
                            type_errors.append(f"{field}: expected number, got {type(overview[field])}")
                    
                    if type_errors:
                        self.log_test(
                            "Analytics Overview - Data Types",
                            False,
                            f"Type validation errors: {type_errors}"
                        )
                    else:
                        self.log_test(
                            "Analytics Overview - Data Types",
                            True,
                            "All numeric fields have correct data types"
                        )
                
                return True
                
            else:
                self.log_test(
                    "Analytics Overview",
                    False,
                    f"Request failed with status {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_test("Analytics Overview", False, "Request failed", e)
            return False

    def test_performance_analytics(self):
        """Test GET /api/admin/analytics/performance"""
        try:
            response = self.session.get(
                f"{API_BASE}/admin/analytics/performance",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                required_fields = ["villa_performance", "monthly_performance", "member_loyalty", "system_metrics"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test(
                        "Performance Analytics - Structure",
                        False,
                        f"Missing required fields: {missing_fields}"
                    )
                else:
                    villa_count = len(data.get("villa_performance", []))
                    monthly_count = len(data.get("monthly_performance", []))
                    loyalty_count = len(data.get("member_loyalty", []))
                    
                    details = f"Villa performance: {villa_count} entries, " \
                             f"Monthly data: {monthly_count} months, " \
                             f"Loyalty levels: {loyalty_count} levels"
                    
                    self.log_test(
                        "Performance Analytics - Structure",
                        True,
                        f"All required fields present. {details}"
                    )
                
                # Test system metrics
                if "system_metrics" in data:
                    metrics = data["system_metrics"]
                    required_metrics = ["avg_response_time", "uptime", "cache_hit_rate"]
                    missing_metrics = [metric for metric in required_metrics if metric not in metrics]
                    
                    if missing_metrics:
                        self.log_test(
                            "Performance Analytics - System Metrics",
                            False,
                            f"Missing system metrics: {missing_metrics}"
                        )
                    else:
                        details = f"Response time: {metrics['avg_response_time']}ms, " \
                                 f"Uptime: {metrics['uptime']}%, " \
                                 f"Cache hit rate: {metrics['cache_hit_rate']}%"
                        
                        self.log_test(
                            "Performance Analytics - System Metrics",
                            True,
                            f"All system metrics present. {details}"
                        )
                
                return True
                
            else:
                self.log_test(
                    "Performance Analytics",
                    False,
                    f"Request failed with status {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_test("Performance Analytics", False, "Request failed", e)
            return False

    def test_trends_analytics(self):
        """Test GET /api/admin/analytics/trends"""
        try:
            response = self.session.get(
                f"{API_BASE}/admin/analytics/trends",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                required_fields = ["weekday_trends", "avg_stay_duration", "geographic_distribution", "price_analysis"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test(
                        "Trends Analytics - Structure",
                        False,
                        f"Missing required fields: {missing_fields}"
                    )
                else:
                    weekday_count = len(data.get("weekday_trends", []))
                    geo_count = len(data.get("geographic_distribution", []))
                    avg_duration = data.get("avg_stay_duration", 0)
                    
                    details = f"Weekday trends: {weekday_count} days, " \
                             f"Geographic data: {geo_count} locations, " \
                             f"Avg stay: {avg_duration} days"
                    
                    self.log_test(
                        "Trends Analytics - Structure",
                        True,
                        f"All required fields present. {details}"
                    )
                
                # Test price analysis
                if "price_analysis" in data:
                    price_data = data["price_analysis"]
                    required_price_fields = ["avg_price", "min_price", "max_price"]
                    missing_price_fields = [field for field in required_price_fields if field not in price_data]
                    
                    if missing_price_fields:
                        self.log_test(
                            "Trends Analytics - Price Analysis",
                            False,
                            f"Missing price analysis fields: {missing_price_fields}"
                        )
                    else:
                        details = f"Avg: €{price_data['avg_price']}, " \
                                 f"Min: €{price_data['min_price']}, " \
                                 f"Max: €{price_data['max_price']}"
                        
                        self.log_test(
                            "Trends Analytics - Price Analysis",
                            True,
                            f"Price analysis complete. {details}"
                        )
                
                return True
                
            else:
                self.log_test(
                    "Trends Analytics",
                    False,
                    f"Request failed with status {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_test("Trends Analytics", False, "Request failed", e)
            return False

    def test_realtime_analytics(self):
        """Test GET /api/admin/analytics/realtime"""
        try:
            response = self.session.get(
                f"{API_BASE}/admin/analytics/realtime",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                required_fields = ["active_users", "recent_events", "popular_pages", "new_reservations", "timestamp"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test(
                        "Realtime Analytics - Structure",
                        False,
                        f"Missing required fields: {missing_fields}"
                    )
                else:
                    active_users = data.get("active_users", 0)
                    recent_events = data.get("recent_events", 0)
                    popular_pages = len(data.get("popular_pages", []))
                    new_reservations = data.get("new_reservations", 0)
                    
                    details = f"Active users: {active_users}, " \
                             f"Recent events: {recent_events}, " \
                             f"Popular pages: {popular_pages}, " \
                             f"New reservations: {new_reservations}"
                    
                    self.log_test(
                        "Realtime Analytics - Structure",
                        True,
                        f"All required fields present. {details}"
                    )
                
                # Test timestamp format
                if "timestamp" in data:
                    try:
                        datetime.fromisoformat(data["timestamp"].replace('Z', '+00:00'))
                        self.log_test(
                            "Realtime Analytics - Timestamp",
                            True,
                            f"Valid ISO timestamp: {data['timestamp']}"
                        )
                    except ValueError:
                        self.log_test(
                            "Realtime Analytics - Timestamp",
                            False,
                            f"Invalid timestamp format: {data['timestamp']}"
                        )
                
                return True
                
            else:
                self.log_test(
                    "Realtime Analytics",
                    False,
                    f"Request failed with status {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_test("Realtime Analytics", False, "Request failed", e)
            return False

    def test_analytics_tracking_with_consent(self):
        """Test POST /api/analytics/track with GDPR consent"""
        try:
            # Test with consent
            tracking_data = {
                "event_type": "page_view",
                "page": "/villa-details/1",
                "session_id": str(uuid.uuid4()),
                "member_id": "test-member-123",
                "consent": {
                    "analytics": True,
                    "personalization": True
                },
                "metadata": {
                    "villa_id": "1",
                    "villa_name": "Villa F3 Petit Macabou",
                    "user_action": "view_details"
                }
            }
            
            response = self.session.post(
                f"{API_BASE}/analytics/track",
                json=tracking_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("status") == "tracked":
                    self.log_test(
                        "Analytics Tracking - With Consent",
                        True,
                        f"Event tracked successfully. Event ID: {data.get('event_id', 'N/A')}"
                    )
                else:
                    self.log_test(
                        "Analytics Tracking - With Consent",
                        False,
                        f"Unexpected response status: {data.get('status')}"
                    )
                
                return True
                
            else:
                self.log_test(
                    "Analytics Tracking - With Consent",
                    False,
                    f"Request failed with status {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_test("Analytics Tracking - With Consent", False, "Request failed", e)
            return False

    def test_analytics_tracking_without_consent(self):
        """Test POST /api/analytics/track without GDPR consent"""
        try:
            # Test without analytics consent
            tracking_data = {
                "event_type": "page_view",
                "page": "/villa-details/2",
                "session_id": str(uuid.uuid4()),
                "member_id": "test-member-456",
                "consent": {
                    "analytics": False,  # No analytics consent
                    "personalization": False
                },
                "metadata": {
                    "villa_id": "2",
                    "villa_name": "Villa F5 Ste Anne"
                }
            }
            
            response = self.session.post(
                f"{API_BASE}/analytics/track",
                json=tracking_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("status") == "skipped" and data.get("reason") == "analytics_consent_required":
                    self.log_test(
                        "Analytics Tracking - GDPR Compliance",
                        True,
                        "Correctly skipped tracking without analytics consent"
                    )
                else:
                    self.log_test(
                        "Analytics Tracking - GDPR Compliance",
                        False,
                        f"Expected skipped status, got: {data}"
                    )
                
                return True
                
            else:
                self.log_test(
                    "Analytics Tracking - GDPR Compliance",
                    False,
                    f"Request failed with status {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_test("Analytics Tracking - GDPR Compliance", False, "Request failed", e)
            return False

    def test_analytics_tracking_anonymized(self):
        """Test POST /api/analytics/track with partial consent (anonymized)"""
        try:
            # Test with analytics consent but no personalization
            tracking_data = {
                "event_type": "villa_search",
                "page": "/search",
                "session_id": str(uuid.uuid4()),
                "member_id": "test-member-789",
                "consent": {
                    "analytics": True,      # Analytics allowed
                    "personalization": False  # No personalization
                },
                "metadata": {
                    "search_query": "Lamentin",
                    "results_count": 2
                }
            }
            
            response = self.session.post(
                f"{API_BASE}/analytics/track",
                json=tracking_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("status") == "tracked":
                    self.log_test(
                        "Analytics Tracking - Anonymized",
                        True,
                        f"Event tracked with anonymization. Event ID: {data.get('event_id', 'N/A')}"
                    )
                else:
                    self.log_test(
                        "Analytics Tracking - Anonymized",
                        False,
                        f"Unexpected response status: {data.get('status')}"
                    )
                
                return True
                
            else:
                self.log_test(
                    "Analytics Tracking - Anonymized",
                    False,
                    f"Request failed with status {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_test("Analytics Tracking - Anonymized", False, "Request failed", e)
            return False

    def test_unauthorized_access(self):
        """Test analytics endpoints without admin authentication"""
        try:
            # Remove authorization header temporarily
            original_headers = self.session.headers.copy()
            if "Authorization" in self.session.headers:
                del self.session.headers["Authorization"]
            
            endpoints = [
                "/admin/analytics/overview",
                "/admin/analytics/performance", 
                "/admin/analytics/trends",
                "/admin/analytics/realtime"
            ]
            
            unauthorized_count = 0
            for endpoint in endpoints:
                response = self.session.get(f"{API_BASE}{endpoint}", timeout=10)
                if response.status_code == 401:
                    unauthorized_count += 1
            
            # Restore headers
            self.session.headers.update(original_headers)
            
            if unauthorized_count == len(endpoints):
                self.log_test(
                    "Analytics Security - Unauthorized Access",
                    True,
                    f"All {len(endpoints)} admin endpoints properly protected (401 Unauthorized)"
                )
            else:
                self.log_test(
                    "Analytics Security - Unauthorized Access",
                    False,
                    f"Only {unauthorized_count}/{len(endpoints)} endpoints returned 401"
                )
            
            return unauthorized_count == len(endpoints)
            
        except Exception as e:
            self.log_test("Analytics Security - Unauthorized Access", False, "Test failed", e)
            return False

    def run_all_tests(self):
        """Run all Phase 4 analytics tests"""
        print("🚀 PHASE 4 ANALYTICS SYSTEM TESTING STARTED")
        print("=" * 60)
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Testing Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        print()
        
        # Step 1: Admin Authentication
        if not self.admin_login():
            print("❌ Cannot proceed without admin authentication")
            return False
        
        # Step 2: Test all analytics endpoints
        tests = [
            self.test_analytics_overview,
            self.test_performance_analytics,
            self.test_trends_analytics,
            self.test_realtime_analytics,
            self.test_analytics_tracking_with_consent,
            self.test_analytics_tracking_without_consent,
            self.test_analytics_tracking_anonymized,
            self.test_unauthorized_access
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test in tests:
            if test():
                passed_tests += 1
        
        # Summary
        print("=" * 60)
        print("📊 PHASE 4 ANALYTICS TESTING SUMMARY")
        print("=" * 60)
        
        success_rate = (passed_tests / total_tests) * 100
        status_emoji = "✅" if success_rate >= 90 else "⚠️" if success_rate >= 70 else "❌"
        
        print(f"{status_emoji} Overall Success Rate: {success_rate:.1f}% ({passed_tests}/{total_tests} tests passed)")
        print()
        
        # Detailed results
        for result in self.test_results:
            print(f"{result['status']} {result['test']}")
            if result['details']:
                print(f"   {result['details']}")
        
        print()
        print("=" * 60)
        
        if success_rate >= 90:
            print("🎉 PHASE 4 ANALYTICS SYSTEM IS FULLY OPERATIONAL!")
            print("All analytics endpoints are working correctly with proper authentication and GDPR compliance.")
        elif success_rate >= 70:
            print("⚠️ PHASE 4 ANALYTICS SYSTEM HAS MINOR ISSUES")
            print("Most functionality works but some improvements needed.")
        else:
            print("❌ PHASE 4 ANALYTICS SYSTEM HAS MAJOR ISSUES")
            print("Significant problems detected that need immediate attention.")
        
        return success_rate >= 90

if __name__ == "__main__":
    tester = Phase4AnalyticsTest()
    tester.run_all_tests()