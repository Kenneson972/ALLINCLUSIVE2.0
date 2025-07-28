#!/usr/bin/env python3
"""
Backend API Testing for KhanelConcept Admin Routes
Testing the new admin authentication and management routes
"""

import requests
import json
import os
from datetime import datetime

# Load environment variables
BACKEND_URL = "https://2dc70b52-37ed-4f34-9403-c7388838f79e.preview.emergentagent.com"
API_BASE_URL = f"{BACKEND_URL}/api"

# Admin credentials from the review request
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "khanelconcept2025"

class KhanelConceptAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.admin_token = None
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
    
    def test_admin_login(self):
        """Test admin authentication with specified credentials"""
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
                    self.log_test("Admin Login", True, "Admin authentication successful", 
                                f"Token type: {data['token_type']}")
                    return True
                else:
                    self.log_test("Admin Login", False, "Login response missing token fields", data)
                    return False
            else:
                self.log_test("Admin Login", False, 
                            f"Login failed with status {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("Admin Login", False, f"Login error: {str(e)}")
            return False
    
    def test_dashboard_stats(self):
        """Test dashboard statistics endpoint"""
        try:
            response = self.session.get(f"{API_BASE_URL}/stats/dashboard", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ["total_villas", "total_reservations", "pending_reservations", 
                                 "confirmed_reservations", "monthly_revenue", "monthly_reservations"]
                
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    self.log_test("Dashboard Stats", False, 
                                f"Missing required fields: {missing_fields}", data)
                    return False
                
                # Check if we have 22 villas as expected (updated from 21)
                if data["total_villas"] >= 21:
                    self.log_test("Dashboard Stats", True, 
                                f"Dashboard stats retrieved successfully - {data['total_villas']} villas found", 
                                data)
                    return True
                else:
                    self.log_test("Dashboard Stats", False, 
                                f"Expected at least 21 villas, got {data['total_villas']}", data)
                    return False
            else:
                self.log_test("Dashboard Stats", False, 
                            f"Stats request failed with status {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("Dashboard Stats", False, f"Stats error: {str(e)}")
            return False
    
    def test_admin_villas(self):
        """Test admin villa management endpoint"""
        try:
            response = self.session.get(f"{API_BASE_URL}/admin/villas", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    villa_count = len(data)
                    if villa_count >= 21:
                        # Check structure of first villa
                        if data:
                            villa = data[0]
                            required_fields = ["id", "name", "location", "price", "guests", 
                                             "category", "image", "gallery"]
                            missing_fields = [field for field in required_fields if field not in villa]
                            
                            if missing_fields:
                                self.log_test("Admin Villas", False, 
                                            f"Villa data missing fields: {missing_fields}", villa)
                                return False
                            
                            self.log_test("Admin Villas", True, 
                                        f"Retrieved {villa_count} villas with correct structure", 
                                        f"Sample villa: {villa['name']} - {villa['location']}")
                            return True
                        else:
                            self.log_test("Admin Villas", False, "Empty villa list returned")
                            return False
                    else:
                        self.log_test("Admin Villas", False, 
                                    f"Expected at least 21 villas, got {villa_count}")
                        return False
                else:
                    self.log_test("Admin Villas", False, "Response is not a list", type(data))
                    return False
            else:
                self.log_test("Admin Villas", False, 
                            f"Admin villas request failed with status {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("Admin Villas", False, f"Admin villas error: {str(e)}")
            return False
    
    def test_admin_reservations(self):
        """Test admin reservation management endpoint"""
        try:
            response = self.session.get(f"{API_BASE_URL}/admin/reservations", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    reservation_count = len(data)
                    self.log_test("Admin Reservations", True, 
                                f"Retrieved {reservation_count} reservations successfully", 
                                f"Reservations found: {reservation_count}")
                    
                    # If there are reservations, check structure
                    if data:
                        reservation = data[0]
                        required_fields = ["id", "villa_id", "customer_name", "customer_email", 
                                         "status", "created_at"]
                        missing_fields = [field for field in required_fields if field not in reservation]
                        
                        if missing_fields:
                            self.log_test("Admin Reservations Structure", False, 
                                        f"Reservation data missing fields: {missing_fields}", reservation)
                            return False
                        else:
                            self.log_test("Admin Reservations Structure", True, 
                                        "Reservation data structure is correct")
                    
                    return True
                else:
                    self.log_test("Admin Reservations", False, "Response is not a list", type(data))
                    return False
            else:
                self.log_test("Admin Reservations", False, 
                            f"Admin reservations request failed with status {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("Admin Reservations", False, f"Admin reservations error: {str(e)}")
            return False
    
    def test_public_villas_endpoint(self):
        """Test public villas endpoint to ensure basic functionality"""
        try:
            response = self.session.get(f"{API_BASE_URL}/villas", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) >= 21:
                    self.log_test("Public Villas", True, 
                                f"Public villas endpoint working - {len(data)} villas", 
                                f"Sample villa: {data[0]['name'] if data else 'None'}")
                    return True
                else:
                    self.log_test("Public Villas", False, 
                                f"Expected at least 21 villas, got {len(data) if isinstance(data, list) else 'non-list'}")
                    return False
            else:
                self.log_test("Public Villas", False, 
                            f"Public villas request failed with status {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Public Villas", False, f"Public villas error: {str(e)}")
            return False
    
    def test_villa_search(self):
        """Test villa search functionality"""
        try:
            search_data = {
                "destination": "lamentin",
                "guests": 2,
                "category": "special"
            }
            
            response = self.session.post(
                f"{API_BASE_URL}/villas/search",
                json=search_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_test("Villa Search", True, 
                                f"Search functionality working - found {len(data)} matching villas", 
                                f"Search criteria: {search_data}")
                    return True
                else:
                    self.log_test("Villa Search", False, "Search response is not a list", type(data))
                    return False
            else:
                self.log_test("Villa Search", False, 
                            f"Search request failed with status {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("Villa Search", False, f"Search error: {str(e)}")
            return False
    
    def test_static_villa_pages(self):
        """Test static villa HTML pages are served correctly"""
        # List of villa HTML files that should be accessible
        villa_pages = [
            "villa-f3-petit-macabou.html",
            "villa-f5-ste-anne.html", 
            "villa-f3-baccha-petit-macabou.html",
            "villa-f6-petit-macabou.html",
            "villa-f6-lamentin.html",
            "villa-f3-le-francois.html",
            "villa-f3-robert-pointe-hyacinthe.html",
            "villa-f6-ste-luce-plage.html",
            "villa-f3-trinite-cosmy.html",
            "villa-f7-baie-des-mulets-vauclin.html",
            "villa-f5-r-pilote-la-renee.html",
            "villa-f3-trenelle-location-annuelle.html",
            "villa-f5-vauclin-ravine-plate.html",
            "villa-fete-journee-fort-de-france.html",
            "villa-fete-journee-riviere-salee.html",
            "villa-fete-journee-ducos.html",
            "villa-fete-journee-r-pilote.html",
            "villa-fete-journee-sainte-luce.html"
        ]
        
        accessible_pages = 0
        failed_pages = []
        
        # Test using localhost since external URL has routing issues for static files
        local_backend_url = "http://localhost:8001"
        
        for page in villa_pages:
            try:
                response = self.session.get(f"{local_backend_url}/{page}", timeout=10)
                if response.status_code == 200:
                    # Check if it's actually HTML content
                    if "html" in response.headers.get("content-type", "").lower() or \
                       "<html" in response.text.lower():
                        accessible_pages += 1
                    else:
                        failed_pages.append(f"{page} (not HTML content)")
                else:
                    failed_pages.append(f"{page} (status {response.status_code})")
            except Exception as e:
                failed_pages.append(f"{page} (error: {str(e)})")
        
        if accessible_pages >= 15:  # Allow some flexibility as exact count may vary
            self.log_test("Static Villa Pages", True, 
                        f"Villa HTML pages accessible via backend - {accessible_pages}/{len(villa_pages)} pages working", 
                        f"Working pages: {accessible_pages}")
            return True
        else:
            self.log_test("Static Villa Pages", False, 
                        f"Too many villa pages inaccessible - only {accessible_pages}/{len(villa_pages)} working", 
                        f"Failed pages: {failed_pages[:5]}")  # Show first 5 failures
            return False
    
    def test_ios_video_background_support(self):
        """Test iOS background video support implementation"""
        # Test key pages that should have iOS video support
        test_pages = [
            "index.html",
            "reservation.html", 
            "villa-f3-petit-macabou.html"
        ]
        
        local_backend_url = "http://localhost:8001"
        ios_features_found = 0
        missing_features = []
        
        for page in test_pages:
            try:
                response = self.session.get(f"{local_backend_url}/{page}", timeout=10)
                if response.status_code == 200:
                    content = response.text.lower()
                    
                    # Check for iOS-specific video attributes
                    ios_checks = {
                        'video_id': 'id="backgroundvideo"' in content,
                        'webkit_playsinline': 'webkit-playsinline' in content,
                        'preload_metadata': 'preload="metadata"' in content,
                        'ios_function': 'initbackgroundvideoios' in content,
                        'ios_detection': '/ipad|iphone|ipod/' in content,
                        'cloudinary_video': 'cloudinary.com' in content and 'background-video' in content
                    }
                    
                    page_features = sum(ios_checks.values())
                    ios_features_found += page_features
                    
                    if page_features >= 4:  # At least 4 out of 6 features should be present
                        self.log_test(f"iOS Video Support - {page}", True, 
                                    f"iOS video features found: {page_features}/6", 
                                    f"Features: {[k for k, v in ios_checks.items() if v]}")
                    else:
                        missing = [k for k, v in ios_checks.items() if not v]
                        missing_features.extend(missing)
                        self.log_test(f"iOS Video Support - {page}", False, 
                                    f"Missing iOS features: {len(missing)}/6", 
                                    f"Missing: {missing}")
                else:
                    self.log_test(f"iOS Video Support - {page}", False, 
                                f"Page not accessible - status {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"iOS Video Support - {page}", False, 
                            f"Error accessing page: {str(e)}")
        
        # Overall assessment
        expected_features = len(test_pages) * 4  # Minimum 4 features per page
        if ios_features_found >= expected_features:
            self.log_test("iOS Video Background System", True, 
                        f"iOS video background support properly implemented", 
                        f"Total features found: {ios_features_found}")
            return True
        else:
            self.log_test("iOS Video Background System", False, 
                        f"iOS video support incomplete - {ios_features_found} features found, expected at least {expected_features}", 
                        f"Common missing features: {list(set(missing_features))}")
            return False
    
    def test_javascript_ios_functions(self):
        """Test that iOS-specific JavaScript functions are present and don't cause errors"""
        test_pages = ["index.html", "villa-f3-petit-macabou.html"]
        local_backend_url = "http://localhost:8001"
        
        js_functions_found = 0
        
        for page in test_pages:
            try:
                response = self.session.get(f"{local_backend_url}/{page}", timeout=10)
                if response.status_code == 200:
                    content = response.text
                    
                    # Check for iOS-specific JavaScript functions
                    js_checks = {
                        'initBackgroundVideoiOS': 'function initBackgroundVideoiOS()' in content,
                        'iOS_detection': 'navigator.userAgent' in content and 'iPad|iPhone|iPod' in content,
                        'webkit_playsinline_attr': "setAttribute('webkit-playsinline'" in content,
                        'touch_event_listeners': 'touchstart' in content,
                        'video_play_promise': 'video.play().catch' in content
                    }
                    
                    found_functions = sum(js_checks.values())
                    js_functions_found += found_functions
                    
                    if found_functions >= 3:  # At least 3 key functions should be present
                        self.log_test(f"JavaScript iOS Functions - {page}", True, 
                                    f"iOS JavaScript functions found: {found_functions}/5", 
                                    f"Functions: {[k for k, v in js_checks.items() if v]}")
                    else:
                        missing = [k for k, v in js_checks.items() if not v]
                        self.log_test(f"JavaScript iOS Functions - {page}", False, 
                                    f"Missing iOS JavaScript functions: {len(missing)}/5", 
                                    f"Missing: {missing}")
                else:
                    self.log_test(f"JavaScript iOS Functions - {page}", False, 
                                f"Page not accessible - status {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"JavaScript iOS Functions - {page}", False, 
                            f"Error checking JavaScript: {str(e)}")
        
        # Overall JavaScript assessment
        if js_functions_found >= 6:  # At least 3 functions per page
            self.log_test("iOS JavaScript Implementation", True, 
                        f"iOS JavaScript functions properly implemented", 
                        f"Total functions found: {js_functions_found}")
            return True
        else:
            self.log_test("iOS JavaScript Implementation", False, 
                        f"iOS JavaScript implementation incomplete - {js_functions_found} functions found")
            return False
    
    def test_villa_id_mapping(self):
        """Test that villa IDs 1-21 map correctly to data"""
        try:
            # Get all villas from API
            response = self.session.get(f"{API_BASE_URL}/villas", timeout=10)
            
            if response.status_code == 200:
                villas = response.json()
                villa_ids = [villa["id"] for villa in villas if "id" in villa]
                
                # Check if we have sequential IDs from 1 to at least 21
                expected_ids = [str(i) for i in range(1, 22)]  # 1-21
                missing_ids = [id for id in expected_ids if id not in villa_ids]
                
                if len(missing_ids) == 0:
                    self.log_test("Villa ID Mapping", True, 
                                f"All villa IDs 1-21 present in database", 
                                f"Total villas: {len(villas)}")
                    return True
                else:
                    self.log_test("Villa ID Mapping", False, 
                                f"Missing villa IDs: {missing_ids}", 
                                f"Found IDs: {villa_ids[:10]}...")  # Show first 10
                    return False
            else:
                self.log_test("Villa ID Mapping", False, 
                            f"Could not retrieve villas for ID mapping test - status {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Villa ID Mapping", False, f"Villa ID mapping error: {str(e)}")
            return False
    
    def test_villa_gallery_integrity(self):
        """Test villa galleries for information image removal - MAIN FOCUS"""
        try:
            response = self.session.get(f"{API_BASE_URL}/villas", timeout=10)
            
            if response.status_code != 200:
                self.log_test("Villa Gallery Integrity", False, 
                            f"Could not retrieve villas - status {response.status_code}")
                return False
            
            villas = response.json()
            
            # Information/catalogue image patterns to check for
            info_image_patterns = [
                "informations_catalogue",
                "tarifs_conditions", 
                "informations_tarifs",
                "catalogue",
                "tarifs",
                "conditions",
                "informations",
                "info_",
                "pricing",
                "rates"
            ]
            
            total_villas = len(villas)
            clean_galleries = 0
            problematic_villas = []
            
            for villa in villas:
                villa_name = villa.get("name", "Unknown")
                villa_id = villa.get("id", "Unknown")
                gallery = villa.get("gallery", [])
                
                # Check each image in gallery for information patterns
                info_images_found = []
                for image_path in gallery:
                    image_name = image_path.lower()
                    for pattern in info_image_patterns:
                        if pattern in image_name:
                            info_images_found.append(image_path)
                            break
                
                if info_images_found:
                    problematic_villas.append({
                        "id": villa_id,
                        "name": villa_name,
                        "info_images": info_images_found
                    })
                else:
                    clean_galleries += 1
            
            # Test specific villas mentioned in review
            villa_f6_found = False
            villa_f7_found = False
            
            for villa in villas:
                if "F6 Petit Macabou" in villa.get("name", ""):
                    villa_f6_found = True
                    gallery = villa.get("gallery", [])
                    expected_images = ["01_vue_aerienne_nuit.jpg", "10_vue_aerienne_jour.jpg"]
                    forbidden_images = ["11_informations_catalogue.jpg"]
                    
                    has_expected = any(expected in str(gallery) for expected in expected_images)
                    has_forbidden = any(forbidden in str(gallery) for forbidden in forbidden_images)
                    
                    if has_forbidden:
                        self.log_test("Villa F6 Petit Macabou Gallery", False,
                                    f"Contains forbidden information images", 
                                    f"Gallery: {gallery}")
                    elif has_expected or len(gallery) > 0:
                        self.log_test("Villa F6 Petit Macabou Gallery", True,
                                    f"Gallery clean with {len(gallery)} legitimate images",
                                    f"Sample images: {gallery[:3]}")
                    else:
                        self.log_test("Villa F6 Petit Macabou Gallery", False,
                                    "Gallery is empty")
                
                if "F7 Baie des Mulets" in villa.get("name", ""):
                    villa_f7_found = True
                    gallery = villa.get("gallery", [])
                    expected_images = ["salon_canape_angle_gris.jpg", "veranda_salle_a_manger_bambou.jpg"]
                    forbidden_images = ["tarifs_conditions_F7.jpg"]
                    
                    has_expected = any(expected in str(gallery) for expected in expected_images)
                    has_forbidden = any(forbidden in str(gallery) for forbidden in forbidden_images)
                    
                    if has_forbidden:
                        self.log_test("Villa F7 Baie des Mulets Gallery", False,
                                    f"Contains forbidden information images",
                                    f"Gallery: {gallery}")
                    elif has_expected or len(gallery) > 0:
                        self.log_test("Villa F7 Baie des Mulets Gallery", True,
                                    f"Gallery clean with {len(gallery)} legitimate images",
                                    f"Sample images: {gallery[:3]}")
                    else:
                        self.log_test("Villa F7 Baie des Mulets Gallery", False,
                                    "Gallery is empty")
            
            # Overall gallery integrity assessment
            if len(problematic_villas) == 0:
                self.log_test("Villa Gallery Integrity - Overall", True,
                            f"All {total_villas} villa galleries are clean - no information images found",
                            f"Clean galleries: {clean_galleries}/{total_villas}")
                success = True
            else:
                self.log_test("Villa Gallery Integrity - Overall", False,
                            f"{len(problematic_villas)} villas still contain information images",
                            f"Problematic villas: {[v['name'] for v in problematic_villas[:3]]}")
                success = False
            
            # Log specific villa findings
            if not villa_f6_found:
                self.log_test("Villa F6 Petit Macabou Search", False,
                            "Villa F6 Petit Macabou not found in villa list")
            
            if not villa_f7_found:
                self.log_test("Villa F7 Baie des Mulets Search", False,
                            "Villa F7 Baie des Mulets not found in villa list")
            
            return success
            
        except Exception as e:
            self.log_test("Villa Gallery Integrity", False, f"Error testing gallery integrity: {str(e)}")
            return False
    
    def test_villa_data_structure_consistency(self):
        """Test that all villa data structures are correct and consistent"""
        try:
            response = self.session.get(f"{API_BASE_URL}/villas", timeout=10)
            
            if response.status_code != 200:
                self.log_test("Villa Data Structure", False,
                            f"Could not retrieve villas - status {response.status_code}")
                return False
            
            villas = response.json()
            
            required_fields = ["id", "name", "location", "price", "guests", "category", "image", "gallery"]
            optional_fields = ["guests_detail", "features", "fallback_icon", "amenities", "description"]
            
            structure_issues = []
            gallery_issues = []
            
            for villa in villas:
                villa_name = villa.get("name", f"Villa ID {villa.get('id', 'Unknown')}")
                
                # Check required fields
                missing_fields = [field for field in required_fields if field not in villa]
                if missing_fields:
                    structure_issues.append(f"{villa_name}: missing {missing_fields}")
                
                # Check gallery structure
                gallery = villa.get("gallery", [])
                if not isinstance(gallery, list):
                    gallery_issues.append(f"{villa_name}: gallery is not a list")
                elif len(gallery) == 0:
                    gallery_issues.append(f"{villa_name}: gallery is empty")
                else:
                    # Check gallery image paths
                    for image_path in gallery:
                        if not isinstance(image_path, str):
                            gallery_issues.append(f"{villa_name}: non-string image path")
                        elif not image_path.startswith("/images/"):
                            gallery_issues.append(f"{villa_name}: invalid image path format")
            
            # Assessment
            total_issues = len(structure_issues) + len(gallery_issues)
            
            if total_issues == 0:
                self.log_test("Villa Data Structure Consistency", True,
                            f"All {len(villas)} villas have consistent data structure",
                            f"Required fields present, galleries properly formatted")
                return True
            else:
                issues_summary = []
                if structure_issues:
                    issues_summary.extend(structure_issues[:3])
                if gallery_issues:
                    issues_summary.extend(gallery_issues[:3])
                
                self.log_test("Villa Data Structure Consistency", False,
                            f"{total_issues} data structure issues found",
                            f"Sample issues: {issues_summary}")
                return False
                
        except Exception as e:
            self.log_test("Villa Data Structure Consistency", False, 
                        f"Error testing data structure: {str(e)}")
            return False
    
    def test_admin_analytics_overview(self):
        """Test admin analytics overview endpoint"""
        if not self.admin_token:
            self.log_test("Admin Analytics Overview", False, "No admin token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = self.session.get(
                f"{API_BASE_URL}/admin/analytics/overview", 
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ["total_villas", "total_members", "total_reservations", 
                                 "monthly_revenue", "conversion_rate", "recent_activity"]
                
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    self.log_test("Admin Analytics Overview", False, 
                                f"Missing required analytics fields: {missing_fields}", data)
                    return False
                
                self.log_test("Admin Analytics Overview", True, 
                            f"Analytics overview retrieved successfully", 
                            f"Revenue: €{data.get('monthly_revenue', 0)}, Conversion: {data.get('conversion_rate', 0)}%")
                return True
            elif response.status_code == 401:
                self.log_test("Admin Analytics Overview", False, 
                            "Analytics endpoint requires admin authentication", 
                            "Unauthorized access properly blocked")
                return False
            else:
                self.log_test("Admin Analytics Overview", False, 
                            f"Analytics request failed with status {response.status_code}", 
                            response.text)
                return False
                
        except Exception as e:
            self.log_test("Admin Analytics Overview", False, f"Analytics error: {str(e)}")
            return False

    def test_admin_verify_token(self):
        """Test admin token verification endpoint"""
        if not self.admin_token:
            self.log_test("Admin Token Verification", False, "No admin token available")
            return False
            
        try:
            token_data = {"token": self.admin_token}
            response = self.session.post(
                f"{API_BASE_URL}/admin/verify-token",
                json=token_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("valid") and data.get("username"):
                    self.log_test("Admin Token Verification", True, 
                                f"Token verification successful for user: {data['username']}")
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

    def test_csv_integration_verification(self):
        """Test that 21 villas CSV integration is working correctly"""
        try:
            response = self.session.get(f"{API_BASE_URL}/villas", timeout=10)
            
            if response.status_code != 200:
                self.log_test("CSV Integration Verification", False, 
                            f"Could not retrieve villas - status {response.status_code}")
                return False
            
            villas = response.json()
            
            # Check for exactly 21 villas as mentioned in review
            if len(villas) != 21:
                self.log_test("CSV Integration Verification", False, 
                            f"Expected exactly 21 villas from CSV, found {len(villas)}")
                return False
            
            # Check for CSV integration flags and data
            csv_integrated_count = 0
            pricing_details_count = 0
            
            for villa in villas:
                if villa.get("csv_integrated"):
                    csv_integrated_count += 1
                if villa.get("pricing_details"):
                    pricing_details_count += 1
            
            # Verify specific villas mentioned in review
            key_villas = {
                "Villa F3 Petit Macabou": 850.0,
                "Villa F5 Ste Anne": 1350.0, 
                "Villa F6 Petit Macabou": 2200.0
            }
            
            found_key_villas = 0
            for villa in villas:
                villa_name = villa.get("name", "")
                for key_name, expected_price in key_villas.items():
                    if key_name in villa_name:
                        found_key_villas += 1
                        if villa.get("price") != expected_price:
                            self.log_test("CSV Integration - Key Villa Pricing", False,
                                        f"{key_name} has price {villa.get('price')}, expected {expected_price}")
                            return False
            
            if found_key_villas == len(key_villas):
                self.log_test("CSV Integration Verification", True,
                            f"21 villas CSV integration verified successfully",
                            f"CSV integrated: {csv_integrated_count}, Pricing details: {pricing_details_count}")
                return True
            else:
                self.log_test("CSV Integration Verification", False,
                            f"Only found {found_key_villas}/{len(key_villas)} key villas from CSV")
                return False
                
        except Exception as e:
            self.log_test("CSV Integration Verification", False, f"CSV integration test error: {str(e)}")
            return False
        """Test villa search functionality and verify returned galleries are clean"""
        try:
            # Test different search filters
            search_tests = [
                {"destination": "Vauclin", "expected_min": 1},
                {"guests": 6, "expected_min": 1},
                {"category": "sejour", "expected_min": 1},
                {"destination": "Lamentin", "guests": 2, "expected_min": 1}
            ]
            
            all_searches_passed = True
            
            for search_data in search_tests:
                expected_min = search_data.pop("expected_min")
                
                response = self.session.post(
                    f"{API_BASE_URL}/villas/search",
                    json=search_data,
                    timeout=10
                )
                
                if response.status_code == 200:
                    results = response.json()
                    
                    if len(results) >= expected_min:
                        # Check galleries in search results
                        gallery_clean = True
                        info_patterns = ["informations_", "tarifs_", "catalogue"]
                        
                        for villa in results:
                            gallery = villa.get("gallery", [])
                            for image_path in gallery:
                                if any(pattern in image_path.lower() for pattern in info_patterns):
                                    gallery_clean = False
                                    break
                            if not gallery_clean:
                                break
                        
                        if gallery_clean:
                            self.log_test(f"Villa Search - {search_data}", True,
                                        f"Found {len(results)} villas with clean galleries",
                                        f"Search criteria: {search_data}")
                        else:
                            self.log_test(f"Villa Search - {search_data}", False,
                                        f"Search results contain information images",
                                        f"Found {len(results)} villas but galleries not clean")
                            all_searches_passed = False
                    else:
                        self.log_test(f"Villa Search - {search_data}", False,
                                    f"Expected at least {expected_min} results, got {len(results)}")
                        all_searches_passed = False
                else:
                    self.log_test(f"Villa Search - {search_data}", False,
                                f"Search failed with status {response.status_code}")
                    all_searches_passed = False
            
            return all_searches_passed
            
        except Exception as e:
            self.log_test("Villa Search with Gallery Verification", False,
                        f"Error testing search: {str(e)}")
            return False

    def run_all_tests(self):
        """Run comprehensive admin dashboard endpoint tests for AllInclusive 2.0"""
        print("🏖️ Starting KhanelConcept Admin Dashboard Testing for AllInclusive 2.0")
        print("🎯 Focus: Admin Authentication & Dashboard Endpoints Verification")
        print(f"Testing against: {API_BASE_URL}")
        print("=" * 70)
        
        # Test basic connectivity
        if not self.test_health_check():
            print("❌ Health check failed - stopping tests")
            return False
        
        # MAIN FOCUS: Admin Dashboard Tests
        print("\n🔐 ADMIN AUTHENTICATION TESTS (PRIMARY FOCUS)")
        print("-" * 50)
        admin_login_success = self.test_admin_login()
        if admin_login_success:
            self.test_admin_verify_token()
        
        print("\n📊 ADMIN DASHBOARD ENDPOINTS TESTS")
        print("-" * 40)
        self.test_dashboard_stats()
        self.test_admin_villas()
        self.test_admin_reservations()
        
        # Test analytics if available
        print("\n📈 ADMIN ANALYTICS TESTS")
        print("-" * 25)
        if admin_login_success:
            self.test_admin_analytics_overview()
        
        # Test CSV integration as mentioned in review
        print("\n📋 CSV INTEGRATION VERIFICATION")
        print("-" * 30)
        self.test_csv_integration_verification()
        
        # Test basic villa endpoints to ensure system integrity
        print("\n🏖️ VILLA SYSTEM INTEGRITY TESTS")
        print("-" * 35)
        self.test_public_villas_endpoint()
        self.test_villa_search()
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 ADMIN DASHBOARD TESTING SUMMARY")
        print("=" * 70)
        
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
        
        # Special focus on admin dashboard results
        admin_tests = [r for r in self.test_results if "Admin" in r["test"] or "Dashboard" in r["test"]]
        if admin_tests:
            print(f"\n🎯 ADMIN DASHBOARD FOCUS RESULTS:")
            for test in admin_tests:
                status = "✅" if test["success"] else "❌"
                print(f"  {status} {test['test']}: {test['message']}")
        
        return passed == total

if __name__ == "__main__":
    tester = KhanelConceptAPITester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️  Some tests failed - check details above")