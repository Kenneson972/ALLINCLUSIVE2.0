#!/usr/bin/env python3
"""
AUDIT ULTRA-COMPLET ET EXHAUSTIF
Analyse chaque prix, chaque villa, chaque doublon - TOUT EN DÉTAIL
"""

import os
import re
import glob
import csv
from urllib.parse import urlparse

def load_csv_reference():
    """Charge TOUTES les données CSV avec vérification"""
    print("📊 Chargement du CSV de référence...")
    
    csv_data = {}
    try:
        with open('/app/Catalogue_Villas_Khanel_Concept_Complet_Final.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, 1):
                if row['Nom de la Villa']:
                    csv_data[row['Nom de la Villa']] = row
                    print(f"   {i}. CSV: {row['Nom de la Villa']}")
        
        print(f"✅ {len(csv_data)} villas chargées depuis le CSV")
        return csv_data
    except Exception as e:
        print(f"❌ Erreur chargement CSV: {e}")
        return {}

def extract_all_prices_detailed(content, filename):
    """Extrait TOUS les prix avec leur contexte exact"""
    
    # Patterns très détaillés pour capturer tous les prix
    price_patterns = [
        (r'(\d+)€/nuit', 'par nuit'),
        (r'(\d+)€/jour', 'par jour'),
        (r'(\d+)€/semaine', 'par semaine'),
        (r'(\d+)€\s*\(\s*\d+\s*nuits?\)', 'weekend'),
        (r'Weekend[^:]*:\s*(\d+)€', 'weekend'),
        (r'Semaine[^:]*:\s*(\d+)€', 'semaine'),
        (r'Base[^:]*:\s*(\d+)€', 'base'),
        (r'Prix[^:]*:\s*(\d+)€', 'prix'),
        (r'Caution[^:]*:\s*(\d+)€', 'caution'),
        (r'(\d+)€\s*en espèces', 'espèces'),
        (r'(\d+)€\s*par chèque', 'chèque'),
        (r'Juillet[^:]*:\s*(\d+)€', 'juillet'),
        (r'Août[^:]*:\s*(\d+)€', 'août'),
        (r'Noël[^:]*:\s*(\d+)€', 'noël'),
        (r'(\d+)€\s*\(\s*\d+\s*jours?\)', 'séjour'),
        (r'>(\d+)€<', 'prix affiché'),
        (r'(\d+)€(?!\s*\d)', 'général')
    ]
    
    all_prices = []
    
    for pattern, context in price_patterns:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            price = int(match.group(1))
            # Extraire le contexte environnant
            start = max(0, match.start() - 50)
            end = min(len(content), match.end() + 50)
            surrounding = content[start:end].replace('\n', ' ').strip()
            
            all_prices.append({
                'prix': price,
                'contexte': context,
                'environnement': surrounding,
                'position': match.start()
            })
    
    return all_prices

def analyze_villa_comprehensively(file_path, csv_data):
    """Analyse COMPLÈTE d'une villa - tout en détail"""
    
    filename = os.path.basename(file_path)
    villa_name = filename.replace('.html', '').replace('-', ' ').title()
    
    print(f"\n🔍 ANALYSE EXHAUSTIVE: {filename}")
    print("-" * 50)
    
    # Vérifier que le fichier existe et est accessible
    if not os.path.exists(file_path):
        print(f"❌ FICHIER INEXISTANT: {file_path}")
        return {'errors': ['Fichier inexistant']}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ ERREUR LECTURE: {e}")
        return {'errors': [f'Erreur lecture: {e}']}
    
    analysis = {
        'filename': filename,
        'file_size': len(content),
        'errors': [],
        'warnings': [],
        'sections': [],
        'prices': [],
        'csv_match': None,
        'duplicates': []
    }
    
    # 1. CORRESPONDANCE CSV
    file_to_csv = {
        'villa-f3-petit-macabou.html': 'Villa F3 sur Petit Macabou',
        'villa-f3-baccha-petit-macabou.html': 'Villa F3 POUR LA BACCHA',
        'villa-f3-le-francois.html': 'Villa F3 sur le François',
        'villa-f5-ste-anne.html': 'Villa F5 sur Ste Anne',
        'villa-f6-lamentin.html': 'Villa F6 au Lamentin',
        'villa-f6-ste-luce-plage.html': 'Villa F6 sur Ste Luce à 1mn de la plage',
        'villa-f3-trinite-cosmy.html': 'Villa F3 Bas de villa Trinité Cosmy',
        'villa-f3-robert-pointe-hyacinthe.html': 'Bas de villa F3 sur le Robert',
        'villa-f3-trenelle-location-annuelle.html': 'Appartement F3 Trenelle (Location Annuelle)',
        'villa-f5-vauclin-ravine-plate.html': 'Villa F5 Vauclin Ravine Plate',
        'villa-f5-r-pilote-la-renee.html': 'Villa F5 La Renée',
        'villa-f7-baie-des-mulets-vauclin.html': 'Villa F7 Baie des Mulets',
        'villa-f6-petit-macabou.html': 'Villa F6 sur Petit Macabou (séjour + fête)',
        'villa-fete-journee-ducos.html': 'Villa Fête Journée Ducos',
        'villa-fete-journee-fort-de-france.html': 'Villa Fête Journée Fort de France',
        'villa-fete-journee-r-pilote.html': 'Villa Fête Journée Rivière-Pilote',
        'villa-fete-journee-riviere-salee.html': 'Villa Fête Journée Rivière Salée',
        'villa-fete-journee-sainte-luce.html': 'Villa Fête Journée Sainte-Luce'
    }
    
    csv_name = file_to_csv.get(filename)
    if csv_name and csv_name in csv_data:
        analysis['csv_match'] = csv_data[csv_name]
        print(f"✅ Correspondance CSV: {csv_name}")
    else:
        analysis['errors'].append(f"Aucune correspondance CSV pour {filename}")
        print(f"❌ AUCUNE CORRESPONDANCE CSV")
    
    # 2. ANALYSE DU TITRE
    title_match = re.search(r'<title>(.*?)</title>', content)
    if title_match:
        print(f"📄 Titre: {title_match.group(1)}")
    else:
        analysis['errors'].append("Titre manquant")
    
    # 3. SECTIONS D'INFORMATION
    info_sections = re.findall(r'<h[1-6][^>]*>.*?(?:Information|Tarif).*?</h[1-6]>', content, re.IGNORECASE)
    analysis['sections'] = info_sections
    print(f"📋 Sections d'information trouvées: {len(info_sections)}")
    
    for i, section in enumerate(info_sections, 1):
        print(f"   {i}. {section.strip()}")
        if i > 1:
            analysis['duplicates'].append(f"Section {i}: {section.strip()}")
    
    # 4. ANALYSE EXHAUSTIVE DES PRIX
    all_prices = extract_all_prices_detailed(content, filename)
    analysis['prices'] = all_prices
    
    print(f"💰 TOUS LES PRIX TROUVÉS ({len(all_prices)}):")
    
    # Grouper les prix par valeur
    price_groups = {}
    for price_info in all_prices:
        prix = price_info['prix']
        if prix not in price_groups:
            price_groups[prix] = []
        price_groups[prix].append(price_info)
    
    for prix, occurrences in sorted(price_groups.items()):
        print(f"   {prix}€ ({len(occurrences)} fois):")
        for occ in occurrences[:3]:  # Limiter à 3 exemples
            context_short = occ['environnement'][:60] + "..." if len(occ['environnement']) > 60 else occ['environnement']
            print(f"      → {occ['contexte']}: {context_short}")
        if len(occurrences) > 3:
            print(f"      ... et {len(occurrences) - 3} autres occurrences")
    
    # 5. DÉTECTION DES DOUBLONS DE PRIX
    duplicated_prices = {prix: occs for prix, occs in price_groups.items() if len(occs) > 1}
    if duplicated_prices:
        analysis['warnings'].append(f"{len(duplicated_prices)} prix en double")
        print(f"⚠️ DOUBLONS DE PRIX DÉTECTÉS:")
        for prix, occs in duplicated_prices.items():
            print(f"   {prix}€ répété {len(occs)} fois")
    
    # 6. VÉRIFICATION CSV vs RÉALITÉ
    if analysis['csv_match']:
        csv_tarif = analysis['csv_match']['Tarif']
        csv_prices = re.findall(r'(\d+)', csv_tarif)
        csv_prices = [int(p) for p in csv_prices]
        
        found_prices = list(price_groups.keys())
        
        print(f"📊 COMPARAISON CSV:")
        print(f"   Prix CSV attendus: {csv_prices}")
        print(f"   Prix trouvés: {found_prices}")
        
        missing_csv_prices = [p for p in csv_prices if p not in found_prices]
        extra_prices = [p for p in found_prices if p not in csv_prices]
        
        if missing_csv_prices:
            analysis['errors'].append(f"Prix CSV manquants: {missing_csv_prices}")
            print(f"   ❌ Prix CSV manquants: {missing_csv_prices}")
        
        if extra_prices:
            analysis['warnings'].append(f"Prix supplémentaires: {extra_prices}")
            print(f"   ⚠️ Prix supplémentaires: {extra_prices}")
    
    # 7. RÉSUMÉ DE L'ANALYSE
    print(f"\n📊 RÉSUMÉ {filename}:")
    print(f"   • Taille fichier: {analysis['file_size']} caractères")
    print(f"   • Sections info: {len(analysis['sections'])}")
    print(f"   • Prix uniques: {len(price_groups)}")
    print(f"   • Prix doublons: {len(duplicated_prices)}")
    print(f"   • Erreurs: {len(analysis['errors'])}")
    print(f"   • Avertissements: {len(analysis['warnings'])}")
    
    return analysis

def comprehensive_audit():
    """Audit ULTRA-COMPLET de toutes les villas"""
    
    print("🚀 AUDIT ULTRA-COMPLET ET EXHAUSTIF")
    print("=" * 80)
    print("Analyse détaillée de chaque prix, chaque villa, chaque doublon")
    print("=" * 80)
    
    # Charger les données CSV
    csv_data = load_csv_reference()
    
    # Lister tous les fichiers villa
    villa_files = glob.glob('/app/villa-*.html')
    villa_files = [f for f in villa_files if 'template' not in f and 'details' not in f]
    
    print(f"\n🏠 VILLAS À AUDITER ({len(villa_files)}):")
    for i, file_path in enumerate(villa_files, 1):
        print(f"   {i}. {os.path.basename(file_path)}")
    
    print("\n" + "=" * 80)
    
    # Analyser chaque villa en détail
    all_analyses = []
    critical_errors = 0
    total_warnings = 0
    
    for file_path in sorted(villa_files):
        analysis = analyze_villa_comprehensively(file_path, csv_data)
        all_analyses.append(analysis)
        
        critical_errors += len(analysis.get('errors', []))
        total_warnings += len(analysis.get('warnings', []))
    
    # RAPPORT FINAL ULTRA-DÉTAILLÉ
    print("\n" + "=" * 80)
    print("📋 RAPPORT FINAL ULTRA-DÉTAILLÉ")
    print("=" * 80)
    
    print(f"🏠 Villas auditées: {len(all_analyses)}")
    print(f"❌ Erreurs critiques: {critical_errors}")
    print(f"⚠️ Avertissements: {total_warnings}")
    
    # Villas avec erreurs critiques
    critical_villas = [a for a in all_analyses if a.get('errors')]
    if critical_villas:
        print(f"\n🚨 VILLAS AVEC ERREURS CRITIQUES ({len(critical_villas)}):")
        for analysis in critical_villas:
            print(f"   • {analysis['filename']}:")
            for error in analysis['errors']:
                print(f"     ❌ {error}")
    
    # Villas avec doublons
    duplicate_villas = [a for a in all_analyses if a.get('duplicates')]
    if duplicate_villas:
        print(f"\n🔄 VILLAS AVEC DOUBLONS ({len(duplicate_villas)}):")
        for analysis in duplicate_villas:
            print(f"   • {analysis['filename']}:")
            for duplicate in analysis['duplicates']:
                print(f"     🔄 {duplicate}")
    
    # Villas avec prix multiples suspects
    suspicious_prices = [a for a in all_analyses if len(set(p['prix'] for p in a.get('prices', []))) > 8]
    if suspicious_prices:
        print(f"\n💰 VILLAS AVEC TROP DE PRIX DIFFÉRENTS ({len(suspicious_prices)}):")
        for analysis in suspicious_prices:
            prices = set(p['prix'] for p in analysis.get('prices', []))
            print(f"   • {analysis['filename']}: {len(prices)} prix différents")
            print(f"     {sorted(list(prices))}")
    
    # CONCLUSION
    print(f"\n🎯 CONCLUSION:")
    if critical_errors == 0 and total_warnings == 0:
        print("🎉 PARFAIT ! Aucun problème détecté.")
    elif critical_errors == 0:
        print(f"✅ ACCEPTABLE - Seulement {total_warnings} avertissements mineurs.")
    else:
        print(f"🚨 ACTION REQUISE - {critical_errors} erreurs critiques à corriger.")
    
    return all_analyses

if __name__ == "__main__":
    comprehensive_audit()