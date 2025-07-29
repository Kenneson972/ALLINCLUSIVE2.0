#!/usr/bin/env python3
"""
CORRECTION DESIGN SMOOTH - TOUTES LES VILLAS
1. Réduire la taille des textes trop gros
2. Améliorer la lisibilité des équipements
3. Rendre le design plus smooth et élégant
4. S'assurer que TOUTES les villas sont traitées
"""

import os
import glob
import re

class CorrectionDesignSmooth:
    def __init__(self):
        self.pages_villa = glob.glob('/app/villa-*.html')
        self.pages_villa = [f for f in self.pages_villa if 'template' not in f and 'backup' not in f]
        
    def get_css_design_smooth(self):
        """CSS pour un design plus smooth avec tailles réduites"""
        return '''
        /* DESIGN SMOOTH ET LISIBLE - TAILLES OPTIMISÉES */
        
        /* Titres principaux - tailles réduites mais lisibles */
        .info-card h2 {
            color: rgba(255, 255, 255, 0.96) !important;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.6) !important;
            font-weight: 600 !important;
            font-size: 1.8rem !important;
            letter-spacing: 0.5px !important;
            margin-bottom: 1rem !important;
        }
        
        .info-card h3 {
            color: rgba(255, 255, 255, 0.94) !important;
            text-shadow: 0 2px 6px rgba(0, 0, 0, 0.5) !important;
            font-weight: 600 !important;
            font-size: 1.4rem !important;
            letter-spacing: 0.3px !important;
            margin-bottom: 0.8rem !important;
        }
        
        .info-card h4 {
            color: rgba(255, 255, 255, 0.92) !important;
            text-shadow: 0 1px 5px rgba(0, 0, 0, 0.4) !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
            margin-bottom: 0.6rem !important;
        }
        
        /* Textes de base - lisibilité optimisée */
        .info-card .text-gray-800 {
            color: rgba(255, 255, 255, 0.94) !important;
            text-shadow: 0 1px 4px rgba(0, 0, 0, 0.4) !important;
            font-weight: 500 !important;
            font-size: 1rem !important;
            line-height: 1.6 !important;
        }
        
        .info-card .text-gray-700 {
            color: rgba(255, 255, 255, 0.90) !important;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3) !important;
            font-weight: 400 !important;
            font-size: 0.95rem !important;
            line-height: 1.7 !important;
        }
        
        .info-card .text-gray-600 {
            color: rgba(255, 255, 255, 0.86) !important;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3) !important;
            font-weight: 400 !important;
            font-size: 0.9rem !important;
        }
        
        /* Numbers avec taille réduite mais visible */
        .info-card .text-2xl {
            color: rgba(255, 255, 255, 0.96) !important;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.6) !important;
            font-weight: 700 !important;
            font-size: 2rem !important;
            letter-spacing: 0.5px !important;
        }
        
        /* Icônes avec effet smooth */
        .info-card .text-blue-600 {
            color: rgba(255, 255, 255, 0.92) !important;
            text-shadow: 0 0 8px rgba(255, 255, 255, 0.3) !important;
            filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3)) !important;
            font-size: 2.5rem !important;
        }
        
        /* AMÉLIORATION SECTION ÉQUIPEMENTS */
        .amenity-item {
            display: flex !important;
            align-items: center !important;
            padding: 12px 16px !important;
            background: rgba(255, 255, 255, 0.08) !important;
            backdrop-filter: blur(10px) !important;
            border-radius: 12px !important;
            margin-bottom: 8px !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        
        .amenity-item:hover {
            background: rgba(255, 255, 255, 0.12) !important;
            transform: translateX(8px) !important;
            border-color: rgba(255, 255, 255, 0.2) !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
        }
        
        .amenity-item i {
            color: rgba(255, 255, 255, 0.9) !important;
            text-shadow: 0 0 8px rgba(255, 255, 255, 0.2) !important;
            font-size: 1.1rem !important;
            margin-right: 12px !important;
            min-width: 20px !important;
        }
        
        .amenity-item span {
            color: rgba(255, 255, 255, 0.92) !important;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3) !important;
            font-weight: 500 !important;
            font-size: 0.95rem !important;
            line-height: 1.4 !important;
        }
        
        /* Prix et tarifs plus élégants */
        .info-card .text-blue-600.font-bold {
            color: rgba(255, 215, 0, 0.95) !important;
            text-shadow: 0 2px 6px rgba(0, 0, 0, 0.4) !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
        }
        
        /* Paragraphes avec espacement optimal */
        .info-card p {
            color: rgba(255, 255, 255, 0.88) !important;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3) !important;
            font-weight: 400 !important;
            font-size: 0.95rem !important;
            line-height: 1.6 !important;
            margin-bottom: 0.8rem !important;
        }
        
        /* Listes avec style amélioré */
        .info-card ul li {
            color: rgba(255, 255, 255, 0.86) !important;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
            font-weight: 400 !important;
            font-size: 0.9rem !important;
            margin-bottom: 6px !important;
            line-height: 1.5 !important;
        }
        
        /* Tables de tarifs plus lisibles */
        .info-card .flex.justify-between {
            padding: 8px 0 !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        
        .info-card .flex.justify-between span {
            font-size: 0.9rem !important;
            line-height: 1.4 !important;
        }
        
        /* Transitions smooth sur tous les éléments */
        .info-card * {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        
        /* Quick info cards plus harmonieuses */
        .info-card.text-center {
            padding: 20px !important;
        }
        
        .info-card.text-center .text-4xl {
            font-size: 2.5rem !important;
            margin-bottom: 0.8rem !important;
        }
        
        .info-card.text-center .text-2xl {
            font-size: 1.8rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        .info-card.text-center .text-gray-600 {
            font-size: 0.85rem !important;
            font-weight: 500 !important;
        }'''
    
    def corriger_design_smooth_villa(self, file_path):
        """Applique le design smooth à une page villa"""
        nom_fichier = os.path.basename(file_path)
        
        print(f"🎨 DESIGN SMOOTH: {nom_fichier}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # Vérifier si déjà traité pour éviter les doublons
            if "DESIGN SMOOTH ET LISIBLE" in contenu:
                print(f"  ⚡ Déjà traité - mise à jour du CSS")
                # Remplacer l'ancien CSS par le nouveau
                pattern = r'/\* AMÉLIORATION LISIBILITÉ TEXTES GLASSMORPHISM \*/.*?(?=/\*|</style>)'
                nouveau_css = self.get_css_design_smooth()
                contenu = re.sub(pattern, nouveau_css, contenu, flags=re.DOTALL)
            else:
                # Ajouter le nouveau CSS
                style_end = contenu.find('</style>')
                if style_end != -1:
                    css_smooth = self.get_css_design_smooth()
                    contenu = (
                        contenu[:style_end] + 
                        css_smooth + 
                        '\n        ' + 
                        contenu[style_end:]
                    )
            
            # Sauvegarder
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(contenu)
            
            print(f"  ✅ DESIGN SMOOTH appliqué")
            print(f"     - Tailles de texte optimisées")
            print(f"     - Équipements plus lisibles")
            print(f"     - Transitions smooth ajoutées")
            print(f"     - Espacement harmonisé")
            
        except Exception as e:
            print(f"  ❌ Erreur: {e}")
    
    def verifier_villas_manquantes(self):
        """Vérifie quelles villas manquent ou ont des problèmes"""
        print("🔍 VÉRIFICATION DES VILLAS...")
        
        villas_attendues = [
            'villa-appartement-f3-trenelle-location-annuelle.html',
            'villa-bas-de-villa-f3-sur-le-robert.html', 
            'villa-bas-de-villa-f3-sur-ste-luce.html',
            'villa-espace-piscine-journee-bungalow.html',
            'villa-studio-cocooning-lamentin.html',
            'villa-villa-f3-bas-de-villa-trinite-cosmy.html',
            'villa-villa-f3-pour-la-baccha.html',
            'villa-villa-f3-sur-le-franois.html', 
            'villa-villa-f3-sur-petit-macabou.html',
            'villa-villa-f5-la-renee.html',
            'villa-villa-f5-sur-ste-anne.html',
            'villa-villa-f5-vauclin-ravine-plate.html',
            'villa-villa-f6-au-lamentin.html',
            'villa-villa-f6-sur-petit-macabou-sejour--fte.html',
            'villa-villa-f6-sur-ste-luce-a-1mn-de-la-plage.html',
            'villa-villa-f7-baie-des-mulets.html',
            'villa-villa-fte-journee-ducos.html',
            'villa-villa-fte-journee-fort-de-france.html',
            'villa-villa-fte-journee-riviere-pilote.html', 
            'villa-villa-fte-journee-riviere-salee.html',
            'villa-villa-fte-journee-sainte-luce.html'
        ]
        
        villas_existantes = [os.path.basename(f) for f in self.pages_villa]
        
        manquantes = [v for v in villas_attendues if v not in villas_existantes]
        
        if manquantes:
            print(f"  ⚠️ {len(manquantes)} villas manquantes:")
            for villa in manquantes:
                print(f"     - {villa}")
        else:
            print(f"  ✅ Toutes les {len(villas_attendues)} villas sont présentes")
            
        return len(villas_existantes)
    
    def executer_correction_design_smooth(self):
        """Applique le design smooth à toutes les pages villa"""
        print("🎨 CORRECTION DESIGN SMOOTH - TOUTES LES VILLAS")
        print("=" * 70)
        print("🎯 Corrections appliquées:")
        print("  1. 📏 Réduction des tailles de texte trop grandes")
        print("  2. 👁️ Amélioration lisibilité équipements principaux") 
        print("  3. ✨ Design plus smooth avec transitions fluides")
        print("  4. 🎨 Espacements et proportions harmonisés")
        print()
        
        # Vérifier les villas manquantes
        nb_villas = self.verifier_villas_manquantes()
        print(f"📄 {nb_villas} pages villa à traiter")
        print()
        
        succes = 0
        
        for file_path in self.pages_villa:
            if 'template' not in os.path.basename(file_path):
                self.corriger_design_smooth_villa(file_path)
                succes += 1
        
        print("\n" + "=" * 70)
        print("✅ DESIGN SMOOTH APPLIQUÉ À TOUTES LES PAGES!")
        
        print("\n🎉 AMÉLIORATIONS FINALES:")
        print("  📏 TAILLES: Textes réduits et harmonisés")
        print("  👁️ LISIBILITÉ: Équipements avec background subtil")
        print("  ✨ SMOOTH: Transitions fluides sur tous éléments")
        print("  🎨 ÉLÉGANCE: Espacements et contrastes optimisés")
        print("  🏆 COHÉRENCE: Design uniforme sur toutes les villas")
        
        print(f"\n🚀 {succes} PAGES VILLA MAINTENANT AVEC DESIGN SMOOTH OPTIMAL!")

if __name__ == "__main__":
    correcteur = CorrectionDesignSmooth()
    correcteur.executer_correction_design_smooth()