#!/usr/bin/env python3
"""
Script pour vérifier et enrichir les données des villas avec les informations manquantes
"""

import os
import re
import json
from pathlib import Path

def analyze_villa_data():
    """Analyse les données des villas dans index.html pour identifier les informations manquantes"""
    
    with open('/app/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraire les données des villas
    villa_pattern = r'const villasData = \[(.*?)\];'
    match = re.search(villa_pattern, content, re.DOTALL)
    
    if not match:
        print("❌ Impossible de trouver les données des villas")
        return
    
    # Analyser chaque villa
    villa_objects = re.findall(r'\{(.*?)\}(?=\s*[,\]])', match.group(1), re.DOTALL)
    
    print(f"🏖️ Analyse de {len(villa_objects)} villas")
    print("=" * 70)
    
    missing_info_count = 0
    placeholder_images = 0
    
    for i, villa_obj in enumerate(villa_objects, 1):
        # Extraire les informations de base
        name_match = re.search(r'name:\s*"([^"]*)"', villa_obj)
        price_match = re.search(r'price:\s*(\d+)', villa_obj)
        image_match = re.search(r'image:\s*"([^"]*)"', villa_obj)
        guests_detail_match = re.search(r'guestsDetail:\s*"([^"]*)"', villa_obj)
        features_match = re.search(r'features:\s*"([^"]*)"', villa_obj)
        description_match = re.search(r'description:\s*"([^"]*)"', villa_obj)
        
        name = name_match.group(1) if name_match else f"Villa {i}"
        price = price_match.group(1) if price_match else "N/A"
        image = image_match.group(1) if image_match else "N/A"
        guests_detail = guests_detail_match.group(1) if guests_detail_match else "N/A"
        features = features_match.group(1) if features_match else "N/A"
        description = description_match.group(1) if description_match else "N/A"
        
        # Analyser les problèmes
        issues = []
        
        # Vérifier les images placeholder
        if 'placeholder_villa' in image:
            issues.append("🖼️ Image placeholder")
            placeholder_images += 1
        
        # Vérifier la description générique
        if description.startswith("Belle villa") and len(description) < 100:
            issues.append("📝 Description générique")
        
        # Vérifier les features basiques
        if features == "Piscine, équipements modernes":
            issues.append("🏊 Features génériques")
        
        # Vérifier les détails d'invités basiques
        if guests_detail.endswith("personnes") and len(guests_detail) < 15:
            issues.append("👥 Détails invités basiques")
        
        if issues:
            print(f"Villa {i:2d}: {name}")
            print(f"         Prix: {price}€ | Image: {os.path.basename(image)}")
            for issue in issues:
                print(f"         ⚠️ {issue}")
            print()
            missing_info_count += 1
    
    print("=" * 70)
    print(f"📊 Résumé:")
    print(f"   • Villas avec informations manquantes: {missing_info_count}/{len(villa_objects)}")
    print(f"   • Images placeholder: {placeholder_images}")
    
    # Recommandations
    if missing_info_count > 0:
        print("\n💡 Recommandations:")
        print("   1. Enrichir les descriptions avec des détails spécifiques")
        print("   2. Ajouter des features détaillées pour chaque villa")
        print("   3. Préciser les détails de capacité (ex: '6 à 10 personnes en journée')")
        print("   4. Remplacer les images placeholder par des vraies photos")

def check_missing_csv_data():
    """Vérifie les informations qui pourraient être manquantes par rapport aux standards CSV"""
    
    expected_fields = [
        'pricing_details',
        'services_full', 
        'guests_detail',
        'csv_integrated',
        'location_details',
        'check_in_time',
        'check_out_time',
        'caution_amount'
    ]
    
    print("\n🔍 Vérification des champs CSV standards")
    print("=" * 50)
    
    with open('/app/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    for field in expected_fields:
        count = content.count(field)
        if count == 0:
            print(f"❌ {field}: Absent")
        elif count < 10:  # Moins de 10 villas ont ce champ
            print(f"⚠️ {field}: Partiel ({count} occurrences)")
        else:
            print(f"✅ {field}: Présent ({count} occurrences)")

def main():
    print("🔬 Analyse des données des villas - Informations manquantes")
    print("=" * 70)
    
    analyze_villa_data()
    check_missing_csv_data()

if __name__ == "__main__":
    main()