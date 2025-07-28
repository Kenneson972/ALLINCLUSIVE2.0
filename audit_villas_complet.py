#!/usr/bin/env python3
"""
Audit complet de toutes les pages villa - Détection des problèmes
Prix incohérents, doublons, informations manquantes, etc.
"""

import os
import re
import glob
import csv

def load_csv_reference():
    """Charge les données CSV de référence"""
    csv_data = {}
    with open('/app/Catalogue_Villas_Khanel_Concept_Complet_Final.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Nom de la Villa']:
                csv_data[row['Nom de la Villa']] = row
    return csv_data

def extract_villa_info(file_path):
    """Extrait toutes les informations d'une page villa"""
    
    filename = os.path.basename(file_path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraction des informations
    info = {
        'filename': filename,
        'title': '',
        'prix_affiches': [],
        'sections_info': 0,
        'capacite': '',
        'localisation': '',
        'services': '',
        'problemes': []
    }
    
    # Titre de la page
    title_match = re.search(r'<title>(.*?)</title>', content)
    if title_match:
        info['title'] = title_match.group(1)
    
    # Compter les sections d'information
    info['sections_info'] = len(re.findall(r'Information.*[Tt]arif', content))
    
    # Extraire tous les prix mentionnés
    prix_patterns = [
        r'(\d+)€',
        r'Prix[^:]*:\s*(\d+)€',
        r'Weekend[^:]*:\s*(\d+)€',
        r'Semaine[^:]*:\s*(\d+)€',
        r'Base[^:]*:\s*(\d+)€'
    ]
    
    for pattern in prix_patterns:
        matches = re.findall(pattern, content)
        info['prix_affiches'].extend([int(p) for p in matches])
    
    # Supprimer les doublons et trier
    info['prix_affiches'] = sorted(list(set(info['prix_affiches'])))
    
    # Extraire la capacité
    capacite_match = re.search(r'(\d+\s*(?:à|personnes)[^<.]*)', content)
    if capacite_match:
        info['capacite'] = capacite_match.group(1)
    
    # Extraire la localisation
    location_patterns = [
        r'<strong>Localisation\s*:\s*</strong>[^<]*<span[^>]*>(.*?)</span>',
        r'Localisation[^:]*:\s*([^<\n]*)',
        r'<i class="fas fa-map-marker-alt[^>]*></i>[^<]*([A-Z][^<\n]{10,})'
    ]
    
    for pattern in location_patterns:
        match = re.search(pattern, content)
        if match:
            info['localisation'] = match.group(1).strip()
            break
    
    return info

def detect_problems(villa_info, csv_data):
    """Détecte les problèmes dans une villa"""
    
    problems = []
    
    # Problème 1: Sections multiples
    if villa_info['sections_info'] > 1:
        problems.append(f"🔄 {villa_info['sections_info']} sections d'information (devrait être 1)")
    
    # Problème 2: Prix incohérents ou manquants
    if not villa_info['prix_affiches']:
        problems.append("💰 Aucun prix trouvé")
    elif len(villa_info['prix_affiches']) > 6:
        problems.append(f"💰 Trop de prix différents ({len(villa_info['prix_affiches'])}): {villa_info['prix_affiches']}")
    
    # Problème 3: Prix suspects (trop élevés ou trop bas)
    if villa_info['prix_affiches']:
        min_prix = min(villa_info['prix_affiches'])
        max_prix = max(villa_info['prix_affiches'])
        
        if min_prix < 50:
            problems.append(f"💰 Prix suspect trop bas: {min_prix}€")
        if max_prix > 5000:
            problems.append(f"💰 Prix suspect trop élevé: {max_prix}€")
        if max_prix - min_prix > 3000:
            problems.append(f"💰 Écart de prix énorme: {min_prix}€ à {max_prix}€")
    
    # Problème 4: Informations manquantes
    if not villa_info['capacite']:
        problems.append("👥 Capacité manquante")
    if not villa_info['localisation']:
        problems.append("📍 Localisation manquante")
    
    # Problème 5: Titre de page générique
    if not villa_info['title'] or 'Villa' not in villa_info['title']:
        problems.append(f"📄 Titre de page problématique: '{villa_info['title']}'")
    
    return problems

def audit_villa_page(file_path, csv_data):
    """Audit complet d'une page villa"""
    
    villa_info = extract_villa_info(file_path)
    problems = detect_problems(villa_info, csv_data)
    
    return villa_info, problems

def main():
    print("🔍 AUDIT COMPLET DES PAGES VILLA")
    print("=" * 60)
    print("Recherche: Prix incohérents, doublons, informations manquantes")
    print("=" * 60)
    
    # Charger les données CSV de référence
    csv_data = load_csv_reference()
    
    # Auditer tous les fichiers villa
    villa_files = glob.glob('/app/villa-*.html')
    villa_files = [f for f in villa_files if 'template' not in f and 'details' not in f]
    
    total_problems = 0
    critical_villas = []
    
    for file_path in sorted(villa_files):
        villa_info, problems = audit_villa_page(file_path, csv_data)
        
        print(f"\n📋 {villa_info['filename']}")
        print(f"   📄 Titre: {villa_info['title']}")
        print(f"   💰 Prix trouvés: {villa_info['prix_affiches']}")
        print(f"   👥 Capacité: {villa_info['capacite']}")
        print(f"   📍 Localisation: {villa_info['localisation']}")
        print(f"   🔄 Sections info: {villa_info['sections_info']}")
        
        if problems:
            print(f"   ❌ PROBLÈMES DÉTECTÉS:")
            for problem in problems:
                print(f"      • {problem}")
            total_problems += len(problems)
            critical_villas.append(villa_info['filename'])
        else:
            print(f"   ✅ Aucun problème détecté")
    
    print("\n" + "=" * 60)
    print(f"📊 RÉSUMÉ DE L'AUDIT")
    print(f"   • Villas auditées: {len(villa_files)}")
    print(f"   • Problèmes détectés: {total_problems}")
    print(f"   • Villas avec problèmes: {len(critical_villas)}")
    
    if critical_villas:
        print(f"\n🚨 VILLAS NÉCESSITANT UNE CORRECTION:")
        for villa in critical_villas:
            print(f"   • {villa}")
    else:
        print(f"\n✅ Toutes les villas sont conformes!")

if __name__ == "__main__":
    main()