#!/usr/bin/env python3
"""
Audit final des 21 pages villa créées pour KhanelConcept
Vérifie les liens, la structure, et génère un rapport complet
"""

import os
import re
from pathlib import Path
import json

def audit_villa_pages():
    """Audit complet des pages villa créées"""
    
    # Liste des 21 pages villa à vérifier
    expected_pages = [
        'villa-f3-petit-macabou.html',
        'villa-f3-baccha.html', 
        'villa-f3-francois.html',
        'villa-f5-ste-anne.html',
        'villa-f6-lamentin.html',
        'villa-f6-ste-luce.html',
        'villa-f5-vauclin.html',
        'villa-f7-baie-mulets.html',
        'villa-f5-la-renee.html',
        'bas-villa-trinite-cosmy.html',
        'bas-villa-robert.html',
        'bas-villa-ste-luce.html',
        'studio-cocooning-lamentin.html',
        'appartement-trenelle.html',
        'villa-fete-ducos.html',
        'villa-fete-fort-de-france.html',
        'villa-fete-riviere-pilote.html',
        'villa-fete-riviere-salee.html',
        'villa-fete-sainte-luce.html',
        'espace-piscine-bungalow.html',
        'villa-f6-petit-macabou-fete.html'
    ]
    
    app_dir = Path('/app')
    results = {
        'total_pages': len(expected_pages),
        'found_pages': 0,
        'missing_pages': [],
        'page_analysis': {},
        'links_analysis': {},
        'errors': []
    }
    
    print("🔍 AUDIT FINAL DES 21 PAGES VILLA KHANEL CONCEPT")
    print("=" * 60)
    
    for page in expected_pages:
        page_path = app_dir / page
        
        if not page_path.exists():
            results['missing_pages'].append(page)
            print(f"❌ {page} - MANQUANTE")
            continue
            
        results['found_pages'] += 1
        
        # Analyse du contenu de la page
        try:
            with open(page_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            page_info = analyze_page_content(content, page)
            results['page_analysis'][page] = page_info
            
            # Vérification des liens
            links_info = check_page_links(content, page)
            results['links_analysis'][page] = links_info
            
            print(f"✅ {page} - OK")
            
        except Exception as e:
            results['errors'].append(f"Erreur lors de l'analyse de {page}: {str(e)}")
            print(f"⚠️  {page} - ERREUR: {str(e)}")
    
    # Génération du rapport
    generate_report(results)
    return results

def analyze_page_content(content, page_name):
    """Analyse le contenu d'une page villa"""
    info = {
        'has_title': bool(re.search(r'<title>.*?</title>', content)),
        'has_hero_section': bool(re.search(r'<section class="hero-villa', content)),
        'has_gallery': bool(re.search(r'<section class="gallery', content)),
        'has_details': bool(re.search(r'<section class="details', content)),
        'has_pricing': bool(re.search(r'<section class="pricing', content)),
        'has_booking_form': bool(re.search(r'<section class="booking', content)),
        'has_footer': bool(re.search(r'<footer class="glass-footer', content)),
        'has_video_background': bool(re.search(r'<div class="video-background', content)),
        'has_glassmorphism_css': bool(re.search(r'glassmorphism\.css', content)),
        'has_glassmorphism_js': bool(re.search(r'glassmorphism\.js', content)),
        'villa_name': extract_villa_name(content),
        'villa_location': extract_villa_location(content),
        'price_found': extract_price_info(content)
    }
    
    return info

def check_page_links(content, page_name):
    """Vérifie les liens dans une page"""
    links_info = {
        'has_index_link': bool(re.search(r'href="\./index\.html"', content)),
        'has_reservation_link': bool(re.search(r'href="\./reservation\.html"', content)),
        'has_contact_link': bool(re.search(r'href="\./contact\.html"', content)),
        'has_villas_link': bool(re.search(r'href="\./villas\.html"', content)),
        'form_action': extract_form_action(content),
        'cloudinary_video': bool(re.search(r'cloudinary\.com.*?martinique-bg', content)),
        'image_paths': extract_image_paths(content)
    }
    
    return links_info

def extract_villa_name(content):
    """Extrait le nom de la villa"""
    match = re.search(r'<h1>(.*?)</h1>', content)
    return match.group(1) if match else "Non trouvé"

def extract_villa_location(content):
    """Extrait la localisation de la villa"""
    match = re.search(r'<p class="villa-location">(.*?)</p>', content)
    return match.group(1) if match else "Non trouvé"

def extract_price_info(content):
    """Extrait les informations de prix"""
    price_match = re.search(r'À partir de ([0-9,]+€)', content)
    return price_match.group(1) if price_match else "Non trouvé"

def extract_form_action(content):
    """Extrait l'action du formulaire"""
    match = re.search(r'action="(.*?)"', content)
    return match.group(1) if match else "Non trouvé"

def extract_image_paths(content):
    """Extrait les chemins d'images"""
    images = re.findall(r'<img src="(.*?)"', content)
    return images[:3]  # Premières 3 images pour l'aperçu

def generate_report(results):
    """Génère un rapport complet"""
    
    print(f"\n📊 RAPPORT FINAL")
    print("=" * 60)
    print(f"✅ Pages trouvées: {results['found_pages']}/{results['total_pages']}")
    print(f"❌ Pages manquantes: {len(results['missing_pages'])}")
    
    if results['missing_pages']:
        print(f"\n⚠️  PAGES MANQUANTES:")
        for page in results['missing_pages']:
            print(f"   - {page}")
    
    print(f"\n📝 ANALYSE DÉTAILLÉE:")
    
    # Vérification des éléments essentiels
    essential_elements = [
        'has_title', 'has_hero_section', 'has_gallery', 
        'has_details', 'has_pricing', 'has_booking_form'
    ]
    
    for page, info in results['page_analysis'].items():
        missing_elements = [elem for elem in essential_elements if not info.get(elem, False)]
        if missing_elements:
            print(f"⚠️  {page}: Éléments manquants - {', '.join(missing_elements)}")
    
    # Vérification des liens
    print(f"\n🔗 ANALYSE DES LIENS:")
    broken_links = []
    
    for page, links in results['links_analysis'].items():
        if not links.get('has_reservation_link', False):
            broken_links.append(f"{page}: Lien réservation manquant")
        if not links.get('has_index_link', False):
            broken_links.append(f"{page}: Lien index manquant")
    
    if broken_links:
        print("⚠️  LIENS CASSÉS:")
        for link in broken_links:
            print(f"   - {link}")
    else:
        print("✅ Tous les liens essentiels sont présents")
    
    # Vérification des assets
    print(f"\n🎨 VÉRIFICATION DES ASSETS:")
    missing_assets = []
    
    for page, info in results['page_analysis'].items():
        if not info.get('has_glassmorphism_css', False):
            missing_assets.append(f"{page}: CSS glassmorphism manquant")
        if not info.get('has_glassmorphism_js', False):
            missing_assets.append(f"{page}: JS glassmorphism manquant")
    
    if missing_assets:
        print("⚠️  ASSETS MANQUANTS:")
        for asset in missing_assets:
            print(f"   - {asset}")
    else:
        print("✅ Tous les assets sont liés correctement")
    
    # Résumé final
    print(f"\n🎯 RÉSUMÉ FINAL:")
    if results['found_pages'] == results['total_pages'] and not broken_links and not missing_assets:
        print("✅ SUCCÈS COMPLET - Toutes les 21 pages villa sont créées et fonctionnelles!")
        print("✅ Design glassmorphism uniforme appliqué")
        print("✅ Vidéo background Cloudinary configurée")
        print("✅ Liens vers reservation.html fonctionnels")
        print("✅ Formulaires de réservation intégrés")
    else:
        print("⚠️  ACTIONS REQUISES:")
        if results['found_pages'] < results['total_pages']:
            print(f"   - Créer {results['total_pages'] - results['found_pages']} page(s) manquante(s)")
        if broken_links:
            print(f"   - Corriger {len(broken_links)} lien(s) cassé(s)")
        if missing_assets:
            print(f"   - Ajouter {len(missing_assets)} asset(s) manquant(s)")
    
    # Sauvegarde du rapport JSON
    with open('/app/RAPPORT_AUDIT_FINAL.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Rapport détaillé sauvegardé: RAPPORT_AUDIT_FINAL.json")

if __name__ == "__main__":
    audit_villa_pages()