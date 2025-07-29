#!/usr/bin/env python3
"""
AMÉLIORATION TEXTES ET EMOJIS - PAGES VILLA
Rendre les textes plus lisibles et ajouter des emojis vivants mais équilibrés
"""

import os
import glob
import re

class AmeliorationTextesEmojis:
    def __init__(self):
        self.pages_villa = glob.glob('/app/villa-*.html')
        self.pages_villa = [f for f in self.pages_villa if 'template' not in f and 'backup' not in f]
        
    def get_css_textes_ameliores(self):
        """CSS pour améliorer la lisibilité des textes"""
        return '''
        /* AMÉLIORATION LISIBILITÉ TEXTES GLASSMORPHISM */
        
        /* Textes principaux plus contrastés */
        .info-card .text-gray-800 {
            color: rgba(255, 255, 255, 0.98) !important;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.6) !important;
            font-weight: 700 !important;
            letter-spacing: 0.5px !important;
        }
        
        .info-card .text-gray-700 {
            color: rgba(255, 255, 255, 0.92) !important;
            text-shadow: 0 2px 6px rgba(0, 0, 0, 0.5) !important;
            font-weight: 500 !important;
            line-height: 1.6 !important;
        }
        
        .info-card .text-gray-600 {
            color: rgba(255, 255, 255, 0.88) !important;
            text-shadow: 0 1px 4px rgba(0, 0, 0, 0.4) !important;
            font-weight: 500 !important;
        }
        
        /* Titres de sections plus vibrants */
        .info-card h2 {
            color: rgba(255, 255, 255, 0.98) !important;
            text-shadow: 0 3px 10px rgba(0, 0, 0, 0.7) !important;
            font-weight: 800 !important;
            letter-spacing: 1px !important;
        }
        
        .info-card h3 {
            color: rgba(255, 255, 255, 0.95) !important;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.6) !important;
            font-weight: 700 !important;
            letter-spacing: 0.8px !important;
        }
        
        .info-card h4 {
            color: rgba(255, 255, 255, 0.93) !important;
            text-shadow: 0 2px 6px rgba(0, 0, 0, 0.5) !important;
            font-weight: 600 !important;
        }
        
        /* Numbers avec plus de punch */
        .info-card .text-2xl {
            color: rgba(255, 255, 255, 0.98) !important;
            text-shadow: 0 3px 12px rgba(0, 0, 0, 0.8) !important;
            font-weight: 900 !important;
            font-size: 2.5rem !important;
            letter-spacing: 1px !important;
        }
        
        /* Icônes avec effet glow plus visible */
        .info-card .text-blue-600 {
            color: rgba(255, 255, 255, 0.95) !important;
            text-shadow: 0 0 15px rgba(255, 255, 255, 0.5) !important;
            filter: drop-shadow(0 3px 8px rgba(0, 0, 0, 0.4)) !important;
        }
        
        /* Textes de description plus lisibles */
        .info-card p {
            color: rgba(255, 255, 255, 0.90) !important;
            text-shadow: 0 2px 6px rgba(0, 0, 0, 0.5) !important;
            font-weight: 400 !important;
            line-height: 1.7 !important;
        }
        
        /* Listes avec meilleure lisibilité */
        .info-card ul li {
            color: rgba(255, 255, 255, 0.88) !important;
            text-shadow: 0 1px 4px rgba(0, 0, 0, 0.4) !important;
            font-weight: 500 !important;
            margin-bottom: 8px !important;
        }
        
        /* Prix et tarifs plus visibles */
        .info-card .text-blue-600.font-bold {
            color: rgba(255, 215, 0, 0.95) !important;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.6) !important;
            font-weight: 800 !important;
        }'''
    
    def get_emojis_mapping(self):
        """Mapping des emojis pour différentes sections"""
        return {
            # Titres de sections
            'Description de la villa': '🏡 Description de la villa',
            'Équipements principaux': '⭐ Équipements principaux',
            'Informations et Tarifs': '💰 Informations et Tarifs',
            'Localisation': '📍 Localisation',
            
            # Sous-titres
            'Tarification': '💳 Tarification',
            'Conditions de Location': '📋 Conditions de Location',
            'Réservation et Contact': '📞 Réservation et Contact',
            'Adresse': '🏠 Adresse',
            'Points d\'intérêt à proximité': '🌟 Points d\'intérêt à proximité',
            'Temps de trajet': '🚗 Temps de trajet',
            'Carte de localisation': '🗺️ Carte de localisation',
            
            # Caractéristiques
            'Caractéristiques exceptionnelles': '✨ Caractéristiques exceptionnelles',
            'Terrasses panoramiques avec vue imprenable': '🌅 Terrasses panoramiques avec vue imprenable',
            'Piscine moderne entourée d\'espaces détente': '🏊‍♀️ Piscine moderne entourée d\'espaces détente',
            'Architecture contemporaine soignée': '🏗️ Architecture contemporaine soignée',
            'Chambres modernes climatisées': '❄️ Chambres modernes climatisées',
            
            # Équipements
            'Piscine privée': '🏊‍♀️ Piscine privée',
            'WiFi haut débit': '📶 WiFi haut débit',
            'Climatisation': '❄️ Climatisation',
            'Cuisine équipée': '🍳 Cuisine équipée',
            'Parking privé': '🚗 Parking privé',
            'Jacuzzi': '🛁 Jacuzzi',
            'Sauna': '🧖‍♀️ Sauna',
            'Douche extérieure': '🚿 Douche extérieure',
            'Salle de bain privée': '🛀 Salle de bain privée',
            'Canapé-lit': '🛋️ Canapé-lit',
            'Terrasses modernes': '🏡 Terrasses modernes',
            'Vue panoramique': '👁️ Vue panoramique',
            
            # Quick info labels
            'Voyageurs': '👥 Voyageurs',
            'Chambres': '🛏️ Chambres',
            'Salles de bain': '🚿 Salles de bain',
            'Surface': '📐 Surface',
            
            # Lieux et trajets
            'Plages les plus proches': '🏖️ Plages les plus proches',
            'Commerces et supermarchés': '🛒 Commerces et supermarchés',
            'Restaurants locaux': '🍽️ Restaurants locaux',
            'Stations service': '⛽ Stations service',
            'Aéroport Martinique': '✈️ Aéroport Martinique',
            'Fort-de-France': '🏛️ Fort-de-France',
            'Montagne Pelée': '🌋 Montagne Pelée'
        }
    
    def ameliorer_textes_et_emojis_villa(self, file_path):
        """Améliore les textes et ajoute des emojis à une page villa"""
        nom_fichier = os.path.basename(file_path)
        
        print(f"✨ AMÉLIORATION TEXTES + EMOJIS: {nom_fichier}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # 1. Ajouter le CSS amélioré
            css_ameliore = self.get_css_textes_ameliores()
            
            # Injecter le CSS avant la fermeture </style>
            style_end = contenu.find('</style>')
            if style_end != -1:
                contenu = (
                    contenu[:style_end] + 
                    css_ameliore + 
                    '\n        ' + 
                    contenu[style_end:]
                )
            
            # 2. Remplacer les textes par versions avec emojis
            emojis_map = self.get_emojis_mapping()
            modifications = 0
            
            for texte_original, texte_emoji in emojis_map.items():
                if texte_original in contenu and texte_emoji not in contenu:
                    # Éviter les remplacements dans les balises ou attributs
                    pattern = r'(>[^<]*?)' + re.escape(texte_original) + r'([^<]*?<)'
                    replacement = r'\1' + texte_emoji + r'\2'
                    
                    ancien_contenu = contenu
                    contenu = re.sub(pattern, replacement, contenu)
                    
                    if contenu != ancien_contenu:
                        modifications += 1
            
            # 3. Améliorer quelques phrases spécifiques
            ameliorations_phrases = {
                'Villa moderne avec terrasses panoramiques': '🌟 Villa moderne avec terrasses panoramiques et vue exceptionnelle',
                'Terrasses modernes et piscine': '🏊‍♀️ Terrasses modernes et piscine • 🌺 Idéale pour réunions familiales',
                'Villa.*moderne.': lambda m: f'🏡 {m.group(0)} ✨',
                'Idéale pour réunions familiales': '👨‍👩‍👧‍👦 Idéale pour réunions familiales et moments inoubliables'
            }
            
            for pattern, replacement in ameliorations_phrases.items():
                if callable(replacement):
                    contenu = re.sub(pattern, replacement, contenu)
                else:
                    contenu = contenu.replace(pattern, replacement)
                    modifications += 1
            
            # Sauvegarder
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(contenu)
            
            print(f"  ✅ AMÉLIORATIONS appliquées avec succès")
            print(f"     - CSS lisibilité amélioré")
            print(f"     - {modifications} textes avec emojis")
            print(f"     - Contrastes renforcés")
            print(f"     - Text-shadows optimisés")
            
        except Exception as e:
            print(f"  ❌ Erreur: {e}")
    
    def executer_ameliorations_toutes_villas(self):
        """Applique les améliorations à toutes les pages villa"""
        print("✨ AMÉLIORATION TEXTES + EMOJIS - TOUTES LES PAGES VILLA")
        print("=" * 70)
        print("🎯 Objectifs:")
        print("  1. 👁️ Améliorer la lisibilité des textes sur glassmorphism")
        print("  2. 🎨 Ajouter des emojis vivants mais équilibrés")
        print("  3. 💪 Renforcer les contrastes et text-shadows")
        print("  4. ✨ Rendre l'interface plus dynamique et moderne")
        print(f"📄 {len(self.pages_villa)} pages villa à améliorer")
        print()
        
        succes = 0
        
        for file_path in self.pages_villa:
            if 'template' not in os.path.basename(file_path):
                self.ameliorer_textes_et_emojis_villa(file_path)
                succes += 1
        
        print("\n" + "=" * 70)
        print("✅ AMÉLIORATIONS APPLIQUÉES À TOUTES LES PAGES!")
        
        print("\n🎉 AMÉLIORATIONS FINALES:")
        print("  ✨ LISIBILITÉ: Text-shadows renforcés + contrastes améliorés")
        print("  🎨 EMOJIS: Sections avec emojis pertinents et équilibrés")
        print("  💪 TYPOGRAPHIE: Font-weights renforcés + letter-spacing")
        print("  🌟 VIBRANCY: Couleurs plus éclatantes + effets glow")
        print("  📱 LISIBILITÉ: Textes parfaitement lisibles sur glassmorphism")
        
        print(f"\n🏆 {succes} PAGES VILLA MAINTENANT PLUS VIVANTES ET LISIBLES!")
        
        print("\n🔍 EMOJIS AJOUTÉS:")
        print("  🏡 Description • ⭐ Équipements • 💰 Tarifs • 📍 Localisation")
        print("  👥 Voyageurs • 🛏️ Chambres • 🚿 Salles de bain • 📐 Surface")
        print("  🏊‍♀️ Piscine • 📶 WiFi • ❄️ Climatisation • 🍳 Cuisine")
        print("  🏖️ Plages • 🛒 Commerces • ✈️ Aéroport • 🌋 Montagne Pelée")

if __name__ == "__main__":
    ameliorateur = AmeliorationTextesEmojis()
    ameliorateur.executer_ameliorations_toutes_villas()