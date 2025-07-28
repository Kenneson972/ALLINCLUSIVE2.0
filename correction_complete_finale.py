#!/usr/bin/env python3
"""
CORRECTION COMPLÈTE des problèmes détectés :
1. Supprimer DÉFINITIVEMENT toutes les anciennes sections
2. Garder SEULEMENT la nouvelle section unifiée avec CSV 
3. Nettoyer les prix incohérents
"""

import os
import re
import glob
import csv

def load_csv_data():
    """Charge les données CSV propres"""
    csv_data = {}
    
    file_to_csv_mapping = {
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
    
    with open('/app/Catalogue_Villas_Khanel_Concept_Complet_Final.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Nom de la Villa']:
                csv_data[row['Nom de la Villa']] = row
    
    return csv_data, file_to_csv_mapping

def clean_villa_completely(file_path, csv_data, mapping):
    """Nettoie complètement une villa et recrée SEULEMENT la section CSV"""
    
    filename = os.path.basename(file_path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Trouver les données CSV
    csv_name = mapping.get(filename)
    if not csv_name or csv_name not in csv_data:
        print(f"❌ {filename}: Aucune correspondance CSV")
        return False
    
    villa_data = csv_data[csv_name]
    
    # SUPPRIMER TOUTES les sections d'information existantes
    patterns_to_remove = [
        # Toute section avec "Informations" et "Tarifs"
        r'<div[^>]*>\s*<div class="info-card">.*?<h3[^>]*>.*?Information.*?Tarif.*?</h3>.*?</div>\s*</div>',
        # Sections avec commentaire
        r'<!-- SECTION UNIFIÉE.*?</div>\s*</div>',
        r'<!-- Section Information.*?</div>\s*</div>',
        r'<!-- Informations et Tarifs.*?</div>\s*</div>',
        # Sections orphelines
        r'<h3[^>]*>.*?Information.*?Tarif.*?</h3>.*?(?=<section|<script|</main|</body)',
        r'<h4[^>]*>.*?Tarification.*?</h4>.*?(?=<h[34]|<section|<script)',
        r'<div class="bg-gray-50 p-4 rounded-lg space-y-2">.*?</div>',
        r'<div class="bg-blue-50 p-4 rounded-lg">.*?</div>',
        r'<div class="bg-green-50 p-4 rounded-lg">.*?</div>',
        r'<div class="bg-yellow-50 p-4 rounded-lg">.*?</div>'
    ]
    
    sections_removed = 0
    for pattern in patterns_to_remove:
        while True:
            match = re.search(pattern, content, re.DOTALL)
            if not match:
                break
            content = content.replace(match.group(0), '', 1)
            sections_removed += 1
            if sections_removed > 10:  # Sécurité pour éviter boucle infinie
                break
    
    # Créer UNE SEULE section propre et complète
    clean_section = f'''
        <!-- SECTION UNIQUE ET COMPLÈTE - Données CSV -->
        <section class="mb-16" data-aos="fade-up" data-aos-delay="400">
            <div class="info-card">
                <h3 class="text-2xl font-bold mb-6 flex items-center">
                    <i class="fas fa-info-circle text-blue-600 mr-3"></i>
                    Informations et Tarifs Complets
                </h3>
                
                <!-- Villa Information -->
                <div class="grid md:grid-cols-2 gap-6 mb-6">
                    <div>
                        <h4 class="text-lg font-semibold mb-3 text-gray-700 flex items-center">
                            <i class="fas fa-home text-blue-500 mr-2"></i>
                            Informations Villa
                        </h4>
                        <div class="space-y-2 text-sm">
                            <div><strong>Nom :</strong> {villa_data['Nom de la Villa']}</div>
                            <div><strong>Localisation :</strong> {villa_data['Localisation']}</div>
                            <div><strong>Type :</strong> {villa_data['Type (F3, F5, etc.)']}</div>
                            <div><strong>Capacité :</strong> {villa_data['Capacité (personnes)']}</div>
                        </div>
                    </div>
                    
                    <div>
                        <h4 class="text-lg font-semibold mb-3 text-gray-700 flex items-center">
                            <i class="fas fa-euro-sign text-green-500 mr-2"></i>
                            Tarification
                        </h4>
                        <div class="bg-green-50 p-3 rounded text-sm">
                            {villa_data['Tarif'].replace(', ', '<br>• ').replace('€', '€<br>• ') if villa_data['Tarif'] else 'Tarifs sur demande'}
                        </div>
                    </div>
                </div>
                
                <!-- Services -->
                <div class="mb-6">
                    <h4 class="text-lg font-semibold mb-3 text-gray-700 flex items-center">
                        <i class="fas fa-concierge-bell text-purple-500 mr-2"></i>
                        Services et Équipements
                    </h4>
                    <div class="bg-purple-50 p-3 rounded text-sm">
                        {villa_data['Options/Services'].replace(', ', '<br>• ') if villa_data['Options/Services'] else 'Services standards'}
                    </div>
                </div>
                
                <!-- Conditions importantes -->
                <div class="mb-6">
                    <h4 class="text-lg font-semibold mb-3 text-gray-700 flex items-center">
                        <i class="fas fa-exclamation-triangle text-orange-500 mr-2"></i>
                        Conditions et Informations Importantes
                    </h4>
                    <div class="bg-orange-50 p-3 rounded text-sm leading-relaxed">
                        {villa_data['Description'].replace('. ', '.<br>• ') if villa_data['Description'] else 'Conditions standards'}
                    </div>
                </div>
                
                <!-- Contact -->
                <div class="bg-blue-50 p-4 rounded-lg text-center">
                    <h4 class="text-lg font-semibold mb-2 text-blue-800">Réservation et Contact</h4>
                    <div class="space-y-1 text-sm">
                        <p><strong>Téléphone :</strong> +596 696 XX XX XX</p>
                        <p><strong>Email :</strong> contact@khanelconcept.com</p>
                        <p><strong>Réservation :</strong> Disponible 24h/24</p>
                    </div>
                </div>
            </div>
        </section>'''
    
    # Trouver où insérer la section (après les équipements, avant la localisation)
    insertion_patterns = [
        (r'(</section>\s*)(<!-- Location -->|<section[^>]*>.*?Localisation)', f'\\1{clean_section}\\2'),
        (r'(</div>\s*</div>\s*)(</main>)', f'\\1{clean_section}\\2'),
        (r'(</section>\s*)(<script)', f'\\1{clean_section}\\2')
    ]
    
    inserted = False
    for pattern, replacement in insertion_patterns:
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, replacement, content, count=1, flags=re.DOTALL)
            inserted = True
            break
    
    if not inserted:
        # Fallback: avant </body>
        content = content.replace('</body>', f'{clean_section}\n</body>')
        inserted = True
    
    if inserted:
        # Nettoyer le HTML (espaces multiples, lignes vides)
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        content = re.sub(r'<div[^>]*>\s*</div>', '', content)
        
        # Sauvegarder
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {filename}: {sections_removed} sections supprimées, 1 section propre créée")
        return True
    else:
        print(f"❌ {filename}: Impossible d'insérer la section")
        return False

def main():
    print("🔧 CORRECTION COMPLÈTE - Suppression définitive des doublons")
    print("=" * 60)
    print("Action: Supprimer TOUTES les sections existantes et recréer UNE section propre")
    print("=" * 60)
    
    csv_data, mapping = load_csv_data()
    
    villa_files = glob.glob('/app/villa-*.html')
    villa_files = [f for f in villa_files if 'template' not in f and 'details' not in f]
    
    corrected_count = 0
    
    for file_path in sorted(villa_files):
        if clean_villa_completely(file_path, csv_data, mapping):
            corrected_count += 1
    
    print("=" * 60)
    print(f"🎯 CORRECTION TERMINÉE : {corrected_count}/{len(villa_files)} villas corrigées")
    print("✅ Chaque villa a maintenant UNE SEULE section propre avec prix cohérents")

if __name__ == "__main__":
    main()