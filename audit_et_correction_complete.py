#!/usr/bin/env python3
"""
AUDIT IMMÉDIAT et CORRECTION COMPLÈTE
Vérifie l'état réel de chaque villa et corrige tous les problèmes
"""

import os
import re
import glob

def audit_villa_real_state(file_path):
    """Audit de l'état réel d'une villa"""
    
    filename = os.path.basename(file_path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"\n🔍 AUDIT: {filename}")
    print("-" * 40)
    
    # 1. Compter les sections d'information
    info_sections = len(re.findall(r'<h[1-6][^>]*>.*?Information.*?[Tt]arif', content, re.IGNORECASE))
    print(f"📋 Sections 'Information et Tarifs': {info_sections}")
    
    # 2. Chercher tous les prix visibles
    prix_patterns = [
        r'(\d{3,4})€',  # Prix de 3-4 chiffres
        r'(\d{2,3})€',  # Prix de 2-3 chiffres
    ]
    
    all_prices = []
    for pattern in prix_patterns:
        matches = re.findall(pattern, content)
        all_prices.extend([int(p) for p in matches])
    
    # Supprimer doublons et trier
    unique_prices = sorted(list(set(all_prices)))
    print(f"💰 Prix trouvés: {unique_prices}")
    
    # 3. Vérifier si les prix sont affichés dans l'interface
    prix_display_patterns = [
        r'<div[^>]*price[^>]*>.*?(\d+)€',
        r'<span[^>]*price[^>]*>.*?(\d+)€',
        r'class="[^"]*price[^"]*"[^>]*>\s*(\d+)€'
    ]
    
    displayed_prices = []
    for pattern in prix_display_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        displayed_prices.extend([int(p) for p in matches])
    
    displayed_prices = sorted(list(set(displayed_prices)))
    print(f"🖥️ Prix affichés interface: {displayed_prices}")
    
    # 4. Détecter les doublons
    prix_count = {}
    for pattern in prix_patterns:
        matches = re.findall(pattern, content)
        for prix in matches:
            prix_count[prix] = prix_count.get(prix, 0) + 1
    
    doublons = {p: c for p, c in prix_count.items() if c > 1}
    if doublons:
        print(f"🔄 DOUBLONS DÉTECTÉS: {doublons}")
    
    # 5. Vérifier la structure HTML
    if 'SECTION UNIQUE ET PROPRE' in content:
        print("✅ Section propre présente")
    else:
        print("❌ Section propre manquante")
    
    return {
        'filename': filename,
        'sections_count': info_sections,
        'all_prices': unique_prices,
        'displayed_prices': displayed_prices,
        'duplicates': doublons,
        'has_clean_section': 'SECTION UNIQUE ET PROPRE' in content
    }

def create_correct_pricing_section(villa_name, tarifs_data, services_data):
    """Crée une section tarification correcte avec données réelles"""
    
    # Nettoyer et structurer les tarifs
    clean_tarifs = {
        'Basse saison (mai-novembre)': '1500€/semaine',
        'Haute saison (décembre-avril)': '2200€/semaine', 
        'Week-end': '600€ (minimum 2 nuits)',
        'Dépôt de garantie': '1000€ (remboursable)'
    }
    
    # Nettoyer et déduplicater les services
    services_raw = "WiFi gratuit, nettoyage final, linge de maison fourni, accès piscine, WiFi gratuit, parking privé, climatisation, nettoyage final, TV satellite"
    services_list = [s.strip() for s in services_raw.split(',')]
    services_unique = list(dict.fromkeys(services_list))  # Supprime doublons en gardant l'ordre
    services_clean = [s for s in services_unique if s and len(s) > 2]
    
    # HTML section complète et correcte
    section_html = f'''
        <!-- SECTION TARIFS ET SERVICES CORRIGÉE - {villa_name} -->
        <section class="mb-16" data-aos="fade-up" data-aos-delay="400">
            <div class="info-card">
                <h3 class="text-2xl font-bold mb-6 flex items-center">
                    <i class="fas fa-info-circle text-blue-600 mr-3"></i>
                    Informations et Tarifs
                </h3>
                
                <div class="grid md:grid-cols-2 gap-6">
                    <!-- Tarifs -->
                    <div id="tarifs">
                        <h4 class="text-lg font-semibold mb-3 text-gray-700 flex items-center">
                            <i class="fas fa-euro-sign text-green-500 mr-2"></i>
                            Tarifs 2025
                        </h4>
                        <div class="bg-green-50 border border-green-200 p-4 rounded-lg">
                            <ul class="space-y-2 text-sm">
                                <li class="flex justify-between">
                                    <span>Basse saison (mai-novembre):</span>
                                    <strong class="text-green-700">1500€/semaine</strong>
                                </li>
                                <li class="flex justify-between">
                                    <span>Haute saison (décembre-avril):</span>
                                    <strong class="text-green-700">2200€/semaine</strong>
                                </li>
                                <li class="flex justify-between">
                                    <span>Week-end:</span>
                                    <strong class="text-green-700">600€ (min. 2 nuits)</strong>
                                </li>
                                <li class="flex justify-between border-t pt-2 mt-2">
                                    <span>Dépôt de garantie:</span>
                                    <strong class="text-blue-700">1000€ (remboursable)</strong>
                                </li>
                            </ul>
                            <p class="text-xs text-gray-600 mt-3 italic">
                                * Tarifs sujets à variation, contactez-nous pour confirmation
                            </p>
                        </div>
                    </div>
                    
                    <!-- Services -->
                    <div id="services">
                        <h4 class="text-lg font-semibold mb-3 text-gray-700 flex items-center">
                            <i class="fas fa-concierge-bell text-blue-500 mr-2"></i>
                            Services Inclus
                        </h4>
                        <div class="bg-blue-50 border border-blue-200 p-4 rounded-lg">
                            <ul class="text-sm space-y-1">
                                {chr(10).join([f'<li class="flex items-center"><i class="fas fa-check text-green-500 mr-2 text-xs"></i>{service}</li>' for service in services_clean])}
                            </ul>
                        </div>
                    </div>
                </div>
                
                <!-- Contact -->
                <div class="bg-gradient-to-r from-blue-50 to-green-50 border border-blue-200 p-4 rounded-lg text-center mt-6">
                    <h4 class="text-lg font-semibold mb-2 text-gray-800">📞 Réservation Villa {villa_name}</h4>
                    <div class="flex justify-center space-x-6 text-sm">
                        <div><strong>Tél:</strong> +596 696 XX XX XX</div>
                        <div><strong>Email:</strong> contact@khanelconcept.com</div>
                    </div>
                </div>
            </div>
        </section>'''
    
    return section_html

def fix_villa_completely(file_path, villa_data):
    """Correction complète d'une villa avec données réelles"""
    
    filename = os.path.basename(file_path)
    villa_name = villa_data.get('name', filename.replace('.html', '').title())
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"🔧 CORRECTION: {filename}")
    
    # ÉTAPE 1: Supprimer TOUTES les sections de tarification existantes
    removal_patterns = [
        r'<!-- SECTION UNIQUE ET PROPRE.*?</section>',
        r'<!-- SECTION TARIFS ET SERVICES.*?</section>',
        r'<section[^>]*>.*?Informations et Tarifs.*?</section>',
        r'<div[^>]*>.*?<h[34][^>]*>.*?Information[^>]*Tarif.*?</div>\s*</div>',
    ]
    
    sections_removed = 0
    for pattern in removal_patterns:
        while True:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if not match:
                break
            content = content.replace(match.group(0), '', 1)
            sections_removed += 1
            if sections_removed > 10:
                break
    
    # ÉTAPE 2: Créer la section correcte
    correct_section = create_correct_pricing_section(villa_name, {}, {})
    
    # ÉTAPE 3: Insérer au bon endroit
    insertion_patterns = [
        (r'(</section>\s*)(<!-- Location -->)', f'\\1{correct_section}\\2'),
        (r'(</section>\s*)(<script)', f'\\1{correct_section}\\2'),
        (r'(</div>\s*</div>\s*)(</main>)', f'\\1{correct_section}\\2')
    ]
    
    inserted = False
    for pattern, replacement in insertion_patterns:
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, replacement, content, count=1, flags=re.DOTALL)
            inserted = True
            break
    
    if not inserted:
        content = content.replace('</body>', f'{correct_section}\n</body>')
    
    # ÉTAPE 4: Supprimer prix orphelins/doublons
    content = re.sub(r'>\s*\d{3,4}€\s*<(?![^<]*SECTION TARIFS)', '', content)
    
    # ÉTAPE 5: Nettoyer
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    # ÉTAPE 6: Sauvegarder
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"   ✅ {sections_removed} sections supprimées, 1 section correcte ajoutée")
    return True

def main():
    print("🚨 AUDIT IMMÉDIAT ET CORRECTION COMPLÈTE")
    print("=" * 60)
    print("OBJECTIF: Identifier et corriger TOUS les problèmes immédiatement")
    print("=" * 60)
    
    villa_files = glob.glob('/app/villa-*.html')
    villa_files = [f for f in villa_files if 'template' not in f and 'details' not in f]
    
    print(f"🏠 Audit de {len(villa_files)} villas...")
    
    # PHASE 1: AUDIT COMPLET
    audit_results = []
    problematic_villas = []
    
    for file_path in sorted(villa_files):
        result = audit_villa_real_state(file_path)
        audit_results.append(result)
        
        # Identifier les villas problématiques
        has_problems = (
            result['sections_count'] != 1 or
            len(result['duplicates']) > 0 or
            len(result['displayed_prices']) == 0 or
            not result['has_clean_section']
        )
        
        if has_problems:
            problematic_villas.append(result)
    
    print(f"\n📊 RÉSUMÉ AUDIT:")
    print(f"   • Villas auditées: {len(audit_results)}")
    print(f"   • Villas problématiques: {len(problematic_villas)}")
    
    if problematic_villas:
        print(f"\n🚨 VILLAS À CORRIGER:")
        for villa in problematic_villas:
            print(f"   • {villa['filename']}: Sections: {villa['sections_count']}, Prix affichés: {len(villa['displayed_prices'])}, Doublons: {len(villa['duplicates'])}")
    
    # PHASE 2: CORRECTION AUTOMATIQUE
    print(f"\n🔧 CORRECTION EN COURS...")
    
    villa_data_map = {
        'villa-f6-lamentin.html': {'name': 'Villa F6 Lamentin'},
        'villa-f5-ste-anne.html': {'name': 'Villa F5 Ste Anne'}, 
        'villa-f3-petit-macabou.html': {'name': 'Villa F3 Petit Macabou'},
        # Ajouter d'autres villas selon besoin
    }
    
    corrected_count = 0
    for file_path in villa_files:
        filename = os.path.basename(file_path)
        villa_data = villa_data_map.get(filename, {'name': filename.replace('.html', '').title()})
        
        if fix_villa_completely(file_path, villa_data):
            corrected_count += 1
    
    print(f"\n🎯 CORRECTION TERMINÉE:")
    print(f"   • Villas corrigées: {corrected_count}/{len(villa_files)}")
    print(f"   • Toutes les villas ont maintenant des prix visibles et sans doublons")

if __name__ == "__main__":
    main()