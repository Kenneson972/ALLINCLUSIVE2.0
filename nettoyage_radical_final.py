#!/usr/bin/env python3
"""
NETTOYAGE RADICAL ET DÉFINITIF
Supprime TOUS les doublons de prix et sections multiples
Crée UNE seule section propre avec prix CSV uniques
"""

import os
import re
import glob
import csv

def radical_cleanup(file_path):
    """Nettoyage radical d'une villa - Supprime TOUT et recrée proprement"""
    
    filename = os.path.basename(file_path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Correspondance CSV
    file_to_csv = {
        'villa-f3-petit-macabou.html': ('Villa F3 sur Petit Macabou', ['1550€/semaine', '850€ (2 nuits)', '1690€/semaine']),
        'villa-f3-baccha-petit-macabou.html': ('Villa F3 POUR LA BACCHA', ['1350€/semaine']),
        'villa-f3-le-francois.html': ('Villa F3 sur le François', ['800€ (2 nuits)', '1376€ (7 jours)']),
        'villa-f5-ste-anne.html': ('Villa F5 sur Ste Anne', ['1350€ (2 nuits)', '2251€ (7 jours)']),
        'villa-f6-lamentin.html': ('Villa F6 au Lamentin', ['1500€ (weekend)', '1200€ (2 nuits)', '2800€ (8 jours)']),
        'villa-f6-ste-luce-plage.html': ('Villa F6 sur Ste Luce à 1mn de la plage', ['1700€ (weekend)', '2200€ à 2850€ (8 jours)']),
        'villa-f3-trinite-cosmy.html': ('Villa F3 Bas de villa Trinité Cosmy', ['500€ (weekend)', '670€ à 1400€ (fête)']),
        'villa-f3-robert-pointe-hyacinthe.html': ('Bas de villa F3 sur le Robert', ['900€ (weekend)', '1250€ (semaine)']),
        'villa-f3-trenelle-location-annuelle.html': ('Appartement F3 Trenelle', ['700€/mois']),
        'villa-f5-vauclin-ravine-plate.html': ('Villa F5 Vauclin Ravine Plate', ['1550€ (weekend)', '2500€ (8 jours)']),
        'villa-f5-r-pilote-la-renee.html': ('Villa F5 La Renée', ['1400€ (weekend fête)', '900€ (weekend)', '2000€ (semaine fête)']),
        'villa-f7-baie-des-mulets-vauclin.html': ('Villa F7 Baie des Mulets', ['2200€/weekend', '4200€/semaine']),
        'villa-f6-petit-macabou.html': ('Villa F6 sur Petit Macabou', ['2000€ (weekend)', 'à partir de 3220€ (semaine)']),
        'villa-fete-journee-ducos.html': ('Villa Fête Journée Ducos', ['30€/personne', '375€ (15 pers)', '440€ (20 pers)']),
        'villa-fete-journee-fort-de-france.html': ('Villa Fête Journée Fort de France', ['À partir de 100€/heure']),
        'villa-fete-journee-r-pilote.html': ('Villa Fête Journée Rivière-Pilote', ['660€ (événement privé)']),
        'villa-fete-journee-riviere-salee.html': ('Villa Fête Journée Rivière Salée', ['400€ (25 pers)', '550€ (50 pers)', '1000€ (100 pers)']),
        'villa-fete-journee-sainte-luce.html': ('Villa Fête Journée Sainte-Luce', ['390€ (20 pers)', '560€ (40 pers)'])
    }
    
    villa_info = file_to_csv.get(filename)
    if not villa_info:
        print(f"❌ {filename}: Aucune correspondance trouvée")
        return False
    
    villa_name, clean_prices = villa_info
    
    print(f"🧹 {filename}: Nettoyage radical...")
    print(f"   Villa: {villa_name}")
    print(f"   Prix propres: {clean_prices}")
    
    # ÉTAPE 1: Supprimer TOUTES les sections d'information existantes
    content_before = content
    
    # Patterns exhaustifs pour supprimer TOUT
    removal_patterns = [
        # Toutes les sections avec "Information" et "Tarif"
        r'<!-- SECTION UNIQUE ET COMPLÈTE.*?</section>',
        r'<section[^>]*>.*?<h3[^>]*>.*?Information.*?Tarif.*?</h3>.*?</section>',
        r'<div[^>]*>.*?<h3[^>]*>.*?Information.*?Tarif.*?</h3>.*?</div>\s*</div>',
        r'<div[^>]*>.*?<h4[^>]*>.*?Information.*?Tarif.*?</h4>.*?</div>\s*</div>',
        # Sections de prix spécifiques
        r'<h4[^>]*>.*?Tarification.*?</h4>.*?(?=<h[34]|<section|<script)',
        r'<h5[^>]*>.*?Tarifs.*?</h5>.*?(?=<h[345]|<section|<script)',
        # Divs avec classes de prix
        r'<div class="bg-[^"]*-50 p-[34] rounded[^>]*>.*?</div>',
        r'<div[^>]*tarif[^>]*>.*?</div>',
    ]
    
    sections_removed = 0
    for pattern in removal_patterns:
        while True:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if not match:
                break
            content = content.replace(match.group(0), '', 1)
            sections_removed += 1
            if sections_removed > 20:  # Sécurité
                break
    
    # ÉTAPE 2: Créer UNE section ultra-propre
    clean_section = f'''
        <!-- SECTION UNIQUE ET PROPRE - {villa_name} -->
        <section class="mb-16" data-aos="fade-up" data-aos-delay="400">
            <div class="info-card">
                <h3 class="text-2xl font-bold mb-6 flex items-center">
                    <i class="fas fa-info-circle text-blue-600 mr-3"></i>
                    Informations et Tarifs
                </h3>
                
                <div class="grid md:grid-cols-2 gap-6">
                    <!-- Informations Villa -->
                    <div>
                        <h4 class="text-lg font-semibold mb-3 text-gray-700">🏠 {villa_name}</h4>
                        <div class="bg-gray-50 p-3 rounded text-sm">
                            Voir détails ci-dessus pour capacité, équipements et services.
                        </div>
                    </div>
                    
                    <!-- Tarifs -->
                    <div>
                        <h4 class="text-lg font-semibold mb-3 text-gray-700">💰 Tarification</h4>
                        <div class="bg-blue-50 p-3 rounded text-sm space-y-1">
                            {('<br>'.join([f'• {price}' for price in clean_prices]))}
                        </div>
                    </div>
                </div>
                
                <!-- Contact -->
                <div class="bg-green-50 p-4 rounded-lg text-center mt-6">
                    <h4 class="text-lg font-semibold mb-2 text-green-800">📞 Réservation</h4>
                    <p class="text-sm"><strong>Tél :</strong> +596 696 XX XX XX</p>
                    <p class="text-sm"><strong>Email :</strong> contact@khanelconcept.com</p>
                </div>
            </div>
        </section>'''
    
    # ÉTAPE 3: Insérer la section propre au bon endroit
    insertion_patterns = [
        (r'(</section>\s*)(<!-- Location -->)', f'\\1{clean_section}\\2'),
        (r'(</section>\s*)(<script)', f'\\1{clean_section}\\2'),
        (r'(</div>\s*</div>\s*)(</main>)', f'\\1{clean_section}\\2')
    ]
    
    inserted = False
    for pattern, replacement in insertion_patterns:
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, replacement, content, count=1, flags=re.DOTALL)
            inserted = True
            break
    
    if not inserted:
        # Fallback
        content = content.replace('</body>', f'{clean_section}\n</body>')
    
    # ÉTAPE 4: Supprimer les prix orphelins dans le reste du HTML
    # (Garder seulement ceux dans notre section propre)
    price_patterns_to_clean = [
        r'<span[^>]*>\s*\d+€[^<]*</span>(?![^<]*SECTION UNIQUE)',
        r'>\s*\d+€\s*<(?![^<]*SECTION UNIQUE)',
        r'Prix[^:]*:\s*\d+€(?![^<]*SECTION UNIQUE)',
    ]
    
    for pattern in price_patterns_to_clean:
        content = re.sub(pattern, '', content, flags=re.IGNORECASE)
    
    # ÉTAPE 5: Nettoyer le HTML
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    content = re.sub(r'<div[^>]*>\s*</div>', '', content)
    
    # ÉTAPE 6: Sauvegarder
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"   ✅ {sections_removed} sections supprimées, 1 section propre créée")
    return True

def main():
    print("🚨 NETTOYAGE RADICAL ET DÉFINITIF")
    print("=" * 60)
    print("SUPPRESSION de TOUS les doublons et sections multiples")
    print("CRÉATION d'UNE seule section propre par villa")
    print("=" * 60)
    
    villa_files = glob.glob('/app/villa-*.html')
    villa_files = [f for f in villa_files if 'template' not in f and 'details' not in f]
    
    cleaned_count = 0
    
    for file_path in sorted(villa_files):
        if radical_cleanup(file_path):
            cleaned_count += 1
    
    print("=" * 60)
    print(f"🎯 NETTOYAGE RADICAL TERMINÉ : {cleaned_count}/{len(villa_files)} villas")
    print("✅ CHAQUE villa a maintenant UNE section propre sans doublons")

if __name__ == "__main__":
    main()