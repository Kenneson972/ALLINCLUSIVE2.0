#!/usr/bin/env python3
"""
Test Premium Villa Features - KhanelConcept
Comprehensive testing of all premium design enhancements, gallery features,
and reservation integration across all 21 villa pages.
"""

import os
import re
import time
import json
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# Test configuration
TEST_CONFIG = {
    'villa_pages_dir': '/app',
    'required_assets': [
        '/app/assets/css/villa-enhanced.css',
        '/app/assets/js/villa-gallery.js', 
        '/app/assets/js/reservation-enhanced.js'
    ],
    'video_url': 'https://res.cloudinary.com/dqz8rw6m2/video/upload/v1733669700/martinique-bg_d0pzjm.mp4',
    'expected_villa_count': 21
}

def print_section(title):
    """Print formatted section header"""
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print('='*60)

def print_test_result(test_name, passed, details=""):
    """Print formatted test result"""
    status = "✅ PASSED" if passed else "❌ FAILED"
    print(f"{status} - {test_name}")
    if details:
        print(f"   📋 {details}")

def find_villa_pages():
    """Find all villa detail pages"""
    villa_pages = []
    villa_dir = Path(TEST_CONFIG['villa_pages_dir'])
    
    for file in villa_dir.glob('villa-*.html'):
        # Exclude template files
        if file.name not in ['villa-details.html', 'villa-template.html']:
            villa_pages.append(file)
    
    return sorted(villa_pages)

def test_required_assets():
    """Test that all premium assets exist and are properly structured"""
    print_section("PREMIUM ASSETS VERIFICATION")
    
    all_assets_exist = True
    
    for asset_path in TEST_CONFIG['required_assets']:
        if os.path.exists(asset_path):
            file_size = os.path.getsize(asset_path)
            print_test_result(
                f"Asset exists: {asset_path}", 
                True, 
                f"Size: {file_size} bytes"
            )
        else:
            print_test_result(f"Asset missing: {asset_path}", False)
            all_assets_exist = False
    
    return all_assets_exist

def test_villa_page_structure(villa_file):
    """Test individual villa page structure and premium features"""
    try:
        with open(villa_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tests = {
            'video_background': 'video-background' in content and TEST_CONFIG['video_url'] in content,
            'glassmorphism_css': 'villa-enhanced.css' in content,
            'gallery_js': 'villa-gallery.js' in content,
            'glass_header': 'glass-header' in content,
            'photo_slider': 'photo-slider' in content,
            'lightbox_support': 'photo-zoom-overlay' in content,
            'reservation_integration': 'ReservationManager.goToReservation' in content,
            'lazy_loading': 'loading="lazy"' in content,
            'responsive_design': 'viewport' in content,
            'villa_specific_data': 'window.currentVilla' in content
        }
        
        passed_tests = sum(1 for passed in tests.values() if passed)
        total_tests = len(tests)
        
        return {
            'file': villa_file.name,
            'tests': tests,
            'score': passed_tests / total_tests,
            'passed': passed_tests,
            'total': total_tests
        }
        
    except Exception as e:
        return {
            'file': villa_file.name,
            'tests': {},
            'score': 0,
            'error': str(e)
        }

def test_gallery_functionality(villa_file):
    """Test gallery features in villa page"""
    try:
        with open(villa_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count images in gallery
        image_count = len(re.findall(r'<img[^>]*src="[^"]*"[^>]*alt="[^"]*"[^>]*loading="lazy"', content))
        
        # Check for premium gallery features
        gallery_features = {
            'multiple_images': image_count >= 6,
            'zoom_overlay': 'photo-zoom-overlay' in content,
            'lazy_loading': 'loading="lazy"' in content,
            'alt_text': 'alt=' in content and image_count > 0,
            'responsive_images': 'object-fit: cover' in content or 'object-fit:cover' in content
        }
        
        return {
            'file': villa_file.name,
            'image_count': image_count,
            'features': gallery_features,
            'score': sum(1 for f in gallery_features.values() if f) / len(gallery_features)
        }
        
    except Exception as e:
        return {
            'file': villa_file.name,
            'error': str(e),
            'score': 0
        }

def test_reservation_integration(villa_file):
    """Test reservation system integration"""
    try:
        with open(villa_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract villa ID and name for reservation
        villa_id_match = re.search(r"ReservationManager\.goToReservation\('([^']+)'", content)
        villa_name_match = re.search(r"ReservationManager\.goToReservation\('[^']+',\s*'([^']+)'", content)
        
        current_villa_match = re.search(r'window\.currentVilla\s*=\s*\{([^}]+)\}', content, re.DOTALL)
        
        integration_tests = {
            'reservation_button': 'btn-reserve-primary' in content,
            'villa_id_present': villa_id_match is not None,
            'villa_name_present': villa_name_match is not None,
            'current_villa_data': current_villa_match is not None,
            'reservation_link': 'reservation.html' in content,
            'price_data': 'basePrice:' in content or 'price' in content.lower()
        }
        
        villa_data = {}
        if villa_id_match and villa_name_match:
            villa_data = {
                'id': villa_id_match.group(1),
                'name': villa_name_match.group(1)
            }
        
        return {
            'file': villa_file.name,
            'tests': integration_tests,
            'villa_data': villa_data,
            'score': sum(1 for t in integration_tests.values() if t) / len(integration_tests)
        }
        
    except Exception as e:
        return {
            'file': villa_file.name,
            'error': str(e),
            'score': 0
        }

def test_performance_optimization(villa_file):
    """Test performance optimization features"""
    try:
        with open(villa_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        perf_features = {
            'preload_video': 'preload=' in content,
            'lazy_loading_images': content.count('loading="lazy"') >= 3,
            'optimized_video_format': '.mp4' in content,
            'css_optimization': 'villa-enhanced.css' in content,
            'video_fallback': 'video-background-fallback' in content,
            'mobile_optimization': 'webkit-playsinline' in content
        }
        
        file_size = os.path.getsize(villa_file)
        
        return {
            'file': villa_file.name,
            'features': perf_features,
            'file_size_kb': round(file_size / 1024, 2),
            'score': sum(1 for f in perf_features.values() if f) / len(perf_features)
        }
        
    except Exception as e:
        return {
            'file': villa_file.name,
            'error': str(e),
            'score': 0
        }

def test_design_consistency(villa_file):
    """Test glassmorphism design consistency"""
    try:
        with open(villa_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        design_elements = {
            'glass_cards': 'glass-card' in content,
            'hero_section': 'hero-villa' in content,
            'glass_header': 'glass-header' in content,
            'glass_footer': 'glass-footer' in content,
            'villa_enhanced_css': 'villa-enhanced.css' in content,
            'video_background': 'video-background' in content,
            'responsive_meta': 'viewport' in content,
            'proper_title': '<title>' in content and 'Khanel Concept' in content
        }
        
        return {
            'file': villa_file.name,
            'elements': design_elements,
            'score': sum(1 for e in design_elements.values() if e) / len(design_elements)
        }
        
    except Exception as e:
        return {
            'file': villa_file.name,
            'error': str(e),
            'score': 0
        }

def run_comprehensive_test():
    """Run comprehensive test of all premium features"""
    print("🚀 STARTING COMPREHENSIVE PREMIUM VILLA FEATURES TEST")
    print("=" * 80)
    
    # Test 1: Required assets
    assets_ok = test_required_assets()
    
    # Find villa pages
    villa_pages = find_villa_pages()
    print_section(f"VILLA PAGES DISCOVERY")
    print_test_result(
        f"Villa pages found", 
        len(villa_pages) >= TEST_CONFIG['expected_villa_count'],
        f"Found: {len(villa_pages)} pages (Expected: {TEST_CONFIG['expected_villa_count']})"
    )
    
    if not villa_pages:
        print("❌ No villa pages found! Test cannot continue.")
        return
    
    # Test results storage
    test_results = {
        'structure': [],
        'gallery': [],
        'reservation': [],
        'performance': [],
        'design': []
    }
    
    print_section("INDIVIDUAL VILLA PAGES TESTING")
    
    for villa_file in villa_pages:
        print(f"\n🏠 Testing {villa_file.name}...")
        
        # Test structure
        structure_result = test_villa_page_structure(villa_file)
        test_results['structure'].append(structure_result)
        
        # Test gallery
        gallery_result = test_gallery_functionality(villa_file)
        test_results['gallery'].append(gallery_result)
        
        # Test reservation
        reservation_result = test_reservation_integration(villa_file)
        test_results['reservation'].append(reservation_result)
        
        # Test performance
        performance_result = test_performance_optimization(villa_file)
        test_results['performance'].append(performance_result)
        
        # Test design
        design_result = test_design_consistency(villa_file)
        test_results['design'].append(design_result)
        
        # Overall score for this villa
        overall_score = (
            structure_result.get('score', 0) +
            gallery_result.get('score', 0) +
            reservation_result.get('score', 0) +
            performance_result.get('score', 0) +
            design_result.get('score', 0)
        ) / 5
        
        print(f"   📊 Overall Score: {overall_score:.1%}")
    
    # Generate summary report
    print_section("COMPREHENSIVE TEST RESULTS SUMMARY")
    
    categories = {
        'structure': 'Page Structure & Premium Features',
        'gallery': 'Gallery Functionality',
        'reservation': 'Reservation Integration',
        'performance': 'Performance Optimization',
        'design': 'Design Consistency'
    }
    
    overall_scores = []
    
    for category, results in test_results.items():
        if results:
            category_scores = [r.get('score', 0) for r in results if 'score' in r]
            avg_score = sum(category_scores) / len(category_scores) if category_scores else 0
            overall_scores.append(avg_score)
            
            print_test_result(
                categories[category],
                avg_score >= 0.8,
                f"Average Score: {avg_score:.1%} ({len([s for s in category_scores if s >= 0.8])}/{len(category_scores)} pages passed)"
            )
    
    # Final overall score
    final_score = sum(overall_scores) / len(overall_scores) if overall_scores else 0
    
    print_section("FINAL TEST RESULTS")
    print(f"🎯 OVERALL PREMIUM FEATURES SCORE: {final_score:.1%}")
    
    if final_score >= 0.9:
        print("🏆 EXCELLENT! All premium features are working correctly.")
    elif final_score >= 0.8:
        print("✅ GOOD! Most premium features are working correctly.")
    elif final_score >= 0.7:
        print("⚠️  ACCEPTABLE! Some premium features need attention.")
    else:
        print("❌ POOR! Major premium features are missing or broken.")
    
    # Detailed recommendations
    print_section("RECOMMENDATIONS")
    
    # Check for common issues
    structure_scores = [r.get('score', 0) for r in test_results['structure']]
    gallery_scores = [r.get('score', 0) for r in test_results['gallery']]
    reservation_scores = [r.get('score', 0) for r in test_results['reservation']]
    
    if sum(structure_scores) / len(structure_scores) < 0.8:
        print("🔧 Consider checking premium CSS/JS assets and video background implementation")
    
    if sum(gallery_scores) / len(gallery_scores) < 0.8:
        print("🖼️ Consider optimizing gallery functionality and image loading")
    
    if sum(reservation_scores) / len(reservation_scores) < 0.8:
        print("📝 Consider checking reservation integration and URL parameter handling")
    
    print("\n✨ Test completed successfully!")
    
    return {
        'final_score': final_score,
        'total_pages': len(villa_pages),
        'assets_ok': assets_ok,
        'detailed_results': test_results
    }

if __name__ == "__main__":
    try:
        results = run_comprehensive_test()
        
        # Save results to file
        with open('/app/premium_test_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n💾 Detailed results saved to: /app/premium_test_results.json")
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        exit(1)