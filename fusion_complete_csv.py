#!/usr/bin/env python3
"""
Script pour fusionner les sections et enrichir avec les données CSV complètes
FUSION : Informations et Tarifs + Services inclus + Informations importantes = UNE SEULE SECTION
"""

import csv
import os
import re
import glob
from pathlib import Path

def load_csv_data():
    """Charge les données du CSV et les structure par nom de villa"""
    
    csv_data = {}
    
    with open('/app/Catalogue_Villas_Khanel_Concept_Complet_Final.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            if row['Nom de la Villa']:  # Ignorer les lignes vides
                villa_name = row['Nom de la Villa'].strip()
                csv_data[villa_name] = {
                    'nom': villa_name,
                    'localisation': row['Localisation'],
                    'type': row['Type (F3, F5, etc.)'],
                    'capacite': row['Capacité (personnes)'],
                    'tarif': row['Tarif'],
                    'services': row['Options/Services'],
                    'description': row['Description']
                }
    
    print(f"📊 CSV chargé : {len(csv_data)} villas trouvées")
    return csv_data

def map_villa_file_to_csv(filename, csv_data):
    """Fait correspondre un fichier villa à ses données CSV"""
    
    # Correspondances manuelles entre noms de fichiers et noms CSV
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
    
    csv_name = file_to_csv_mapping.get(filename)
    if csv_name and csv_name in csv_data:
        return csv_data[csv_name]
    
    return None

def create_unified_section(villa_data, filename):
    """Crée UNE section unifiée complète avec toutes les données CSV"""
    
    if not villa_data:
        return ""
    
    villa_name = villa_data['nom']
    
    # Structure HTML unifiée avec TOUTES les informations
    unified_section = f'''
            <!-- SECTION UNIFIÉE : Information, Tarifs, Services et Conditions (depuis CSV) -->
            <div data-aos="fade-up" data-aos-delay="500">
                <div class="info-card">
                    <h3 class="text-2xl font-bold mb-6 flex items-center">
                        <i class="fas fa-info-circle text-blue-600 mr-3"></i>
                        Informations Complètes et Tarifs
                    </h3>
                    
                    <!-- Informations générales -->
                    <div class="mb-6">
                        <h4 class="text-xl font-semibold mb-3 text-gray-700">🏠 Informations Générales</h4>
                        <div class="bg-gray-50 p-4 rounded-lg space-y-2">
                            <div class="flex justify-between">
                                <span><strong>Nom :</strong></span>
                                <span class="font-semibold">{villa_data['nom']}</span>
                            </div>
                            <div class="flex justify-between">
                                <span><strong>Localisation :</strong></span>
                                <span class="font-semibold">{villa_data['localisation']}</span>
                            </div>
                            <div class="flex justify-between">
                                <span><strong>Type :</strong></span>
                                <span class="font-semibold">{villa_data['type']}</span>
                            </div>
                            <div class="flex justify-between">
                                <span><strong>Capacité :</strong></span>
                                <span class="font-semibold">{villa_data['capacite']}</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Tarifs détaillés -->
                    <div class="mb-6">
                        <h4 class="text-xl font-semibold mb-3 text-gray-700">💰 Tarification Détaillée</h4>
                        <div class="bg-blue-50 p-4 rounded-lg">
                            <div class="text-sm space-y-1">
                                {villa_data['tarif'].replace(', ', '<br>• ').replace('€', '€<br>• ') if villa_data['tarif'] else 'Tarifs sur demande'}
                            </div>
                        </div>
                    </div>
                    
                    <!-- Services et équipements -->
                    <div class="mb-6">
                        <h4 class="text-xl font-semibold mb-3 text-gray-700">🔧 Services et Équipements Inclus</h4>
                        <div class="bg-green-50 p-4 rounded-lg">
                            <div class="text-sm">
                                {villa_data['services'].replace(', ', '<br>• ') if villa_data['services'] else 'Services standards inclus'}
                            </div>
                        </div>
                    </div>
                    
                    <!-- Informations importantes et conditions -->
                    <div class="mb-6">
                        <h4 class="text-xl font-semibold mb-3 text-gray-700">⚠️ Informations Importantes et Conditions</h4>
                        <div class="bg-yellow-50 p-4 rounded-lg">
                            <div class="text-sm leading-relaxed">
                                {villa_data['description'].replace('. ', '.<br>• ') if villa_data['description'] else 'Conditions standards appliquées'}
                            </div>
                        </div>
                    </div>
                    
                    <!-- Contact et Réservation -->
                    <div class="bg-blue-50 p-4 rounded-lg">
                        <h4 class="text-xl font-semibold mb-2 text-blue-800">📞 Réservation et Contact</h4>
                        <p class="text-sm text-blue-700 mb-3">{villa_name}</p>
                        <div class="space-y-1 text-sm">
                            <p><strong>Téléphone :</strong> +596 696 XX XX XX</p>
                            <p><strong>Email :</strong> contact@khanelconcept.com</p>
                            <p><strong>Réservation en ligne :</strong> Disponible 24h/7j</p>
                        </div>
                    </div>
                </div>
            </div>'''
    
    return unified_section

def process_villa_file(file_path, csv_data):
    """Traite un fichier villa : supprime les sections multiples et crée la section unifiée"""
    
    filename = os.path.basename(file_path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Trouver les données CSV correspondantes
    villa_data = map_villa_file_to_csv(filename, csv_data)
    
    if not villa_data:
        print(f"⚠️ {filename}: Aucune correspondance CSV trouvée")
        return False
    
    print(f"✅ {filename}: Correspondance trouvée - {villa_data['nom']}")
    
    # Supprimer TOUTES les sections existantes (multiples sections)
    patterns_to_remove = [
        # Section "Informations et Tarifs Détaillés"
        r'<!-- Informations et Tarifs Détaillés -->.*?</div>\s*</div>',
        # Sections avec h3 "Informations et Tarifs"
        r'<h3[^>]*>.*?Informations et Tarifs.*?</h3>.*?(?=<h3|</div>\s*</div>|<section)',
        # Sections "Services inclus"
        r'<h4[^>]*>.*?Services inclus.*?</h4>.*?(?=<h4|<h3|</div>\s*</div>)',
        # Sections "Informations importantes"
        r'<h4[^>]*>.*?Informations importantes.*?</h4>.*?(?=<h4|<h3|</div>\s*</div>)',
    ]
    
    sections_removed = 0
    for pattern in patterns_to_remove:
        matches = re.findall(pattern, content, re.DOTALL)
        for match in matches:
            content = content.replace(match, '', 1)
            sections_removed += 1
    
    # Créer la section unifiée
    unified_section = create_unified_section(villa_data, filename)
    
    # Trouver le bon endroit pour insérer la section
    insertion_patterns = [
        (r'(</div>\s*</div>\s*</section>)', f'\\1{unified_section}'),  # Après une section
        (r'(</div>\s*</div>\s*<section)', f'\\1{unified_section}\\2'),  # Entre sections
        (r'(</div>\s*</div>\s*)(<script)', f'\\1{unified_section}\\2'),  # Avant les scripts
    ]
    
    inserted = False
    for pattern, replacement in insertion_patterns:
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, replacement, content, count=1, flags=re.DOTALL)
            inserted = True
            break
    
    if not inserted:
        # Fallback : insérer avant les scripts
        script_pos = content.find('<script')
        if script_pos > -1:
            content = content[:script_pos] + unified_section + '\n' + content[script_pos:]
            inserted = True
    
    if inserted:
        # Sauvegarder les modifications
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ {sections_removed} sections supprimées, 1 section unifiée créée")
        return True
    else:
        print(f"  ❌ Impossible d'insérer la section unifiée")
        return False

def main():
    print("🔧 FUSION COMPLÈTE : Sections + Enrichissement CSV")
    print("=" * 60)
    print("OBJECTIF : UNE seule section complète par villa avec TOUTES les données CSV")
    print("=" * 60)
    
    # Charger les données CSV
    csv_data = load_csv_data()
    
    # Traiter tous les fichiers villa
    villa_files = glob.glob('/app/villa-*.html')
    villa_files = [f for f in villa_files if 'template' not in f and 'details' not in f]
    
    processed_count = 0
    
    for file_path in sorted(villa_files):
        if process_villa_file(file_path, csv_data):
            processed_count += 1
    
    print("=" * 60)
    print(f"🎯 FUSION TERMINÉE : {processed_count}/{len(villa_files)} villas enrichies")
    print("✅ Chaque villa a maintenant UNE section complète avec toutes les données CSV")

if __name__ == "__main__":
    main()