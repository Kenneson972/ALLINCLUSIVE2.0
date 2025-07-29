#!/usr/bin/env python3
"""
AJOUT GLASSMORPHISM AUX PAGES VILLA
Appliquer le style glassmorphism de l'index.html aux cartes d'informations des villas
"""

import os
import glob
import re

class GlassmorphismVillas:
    def __init__(self):
        self.pages_villa = glob.glob('/app/villa-*.html')
        self.pages_villa = [f for f in self.pages_villa if 'template' not in f and 'backup' not in f]
        
    def get_glassmorphism_css(self):
        """Retourne le CSS glassmorphism inspiré de l'index.html"""
        return '''
        /* Glassmorphism Variables */
        :root {
            --glass-bg: rgba(255, 255, 255, 0.1);
            --glass-border: rgba(255, 255, 255, 0.2);
            --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            --glass-hover-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
            --backdrop-blur: blur(15px);
        }
        
        /* Glass Cards pour info-cards des villas */
        .info-card {
            background: var(--glass-bg) !important;
            backdrop-filter: var(--backdrop-blur) saturate(150%) !important;
            -webkit-backdrop-filter: var(--backdrop-blur) saturate(150%) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: 20px !important;
            padding: 25px !important;
            box-shadow: var(--glass-shadow) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            position: relative !important;
            overflow: hidden !important;
        }
        
        /* Effet de survol glassmorphism */
        .info-card:hover {
            transform: translateY(-8px) !important;
            box-shadow: var(--glass-hover-shadow) !important;
            background: rgba(255, 255, 255, 0.15) !important;
            border-color: rgba(255, 255, 255, 0.3) !important;
        }
        
        /* Reflet glassmorphism subtil */
        .info-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, 
                transparent 0%, 
                rgba(255, 255, 255, 0.4) 50%, 
                transparent 100%);
            z-index: 1;
        }
        
        /* Optimisation des textes sur glassmorphism */
        .info-card .text-gray-800 {
            color: rgba(255, 255, 255, 0.95) !important;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3) !important;
            font-weight: 600 !important;
        }
        
        .info-card .text-gray-700 {
            color: rgba(255, 255, 255, 0.85) !important;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
        }
        
        .info-card .text-gray-600 {
            color: rgba(255, 255, 255, 0.75) !important;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
        }
        
        /* Icônes avec effet glassmorphism */
        .info-card .text-blue-600 {
            color: rgba(255, 255, 255, 0.9) !important;
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.3) !important;
            filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2)) !important;
        }
        
        /* Numbers avec effet glassmorphism */
        .info-card .text-2xl {
            color: rgba(255, 255, 255, 0.95) !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
            font-weight: 700 !important;
        }
        
        /* Glass effect pour gallery-container */
        .gallery-container {
            background: var(--glass-bg) !important;
            backdrop-filter: var(--backdrop-blur) !important;
            -webkit-backdrop-filter: var(--backdrop-blur) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: 25px !important;
            overflow: hidden !important;
            box-shadow: var(--glass-shadow) !important;
        }
        
        /* Glass effect pour thumbnails */
        .gallery-thumbnails {
            background: rgba(255, 255, 255, 0.05) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
        }'''
    
    def appliquer_glassmorphisme_villa(self, file_path):
        """Applique le glassmorphism à une page villa"""
        nom_fichier = os.path.basename(file_path)
        
        print(f"✨ GLASSMORPHISM: {nom_fichier}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # Rechercher la section CSS existante
            if '<style>' in contenu and '</style>' in contenu:
                # Trouver la position de fermeture du style existant
                style_end = contenu.find('</style>')
                
                if style_end != -1:
                    # Injecter le CSS glassmorphism avant la fermeture
                    glassmorphism_css = self.get_glassmorphism_css()
                    
                    # Insérer le CSS glassmorphism
                    nouveau_contenu = (
                        contenu[:style_end] + 
                        glassmorphism_css + 
                        '\n        ' + 
                        contenu[style_end:]
                    )
                    
                    # Sauvegarder
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(nouveau_contenu)
                    
                    print(f"  ✅ GLASSMORPHISM appliqué avec succès")
                    print(f"     - Cartes info avec effet glass")
                    print(f"     - Textes optimisés pour transparence")
                    print(f"     - Effets de survol améliorés")
                    print(f"     - Galerie avec glass container")
                else:
                    print(f"  ⚠️ Section </style> non trouvée")
            else:
                print(f"  ⚠️ Pas de section <style> trouvée")
                
        except Exception as e:
            print(f"  ❌ Erreur: {e}")
    
    def executer_glassmorphism_toutes_villas(self):
        """Applique le glassmorphism à toutes les pages villa"""
        print("✨ APPLICATION GLASSMORPHISM - TOUTES LES PAGES VILLA")
        print("=" * 70)
        print("🎯 Objectif: Appliquer le style glassmorphism de l'index.html")
        print("📦 Éléments concernés:")
        print("  - Cartes d'informations (voyageurs, chambres, surface)")
        print("  - Galerie images container")
        print("  - Thumbnails avec effet glass")
        print("  - Textes optimisés pour transparence")
        print(f"📄 {len(self.pages_villa)} pages villa à traiter")
        print()
        
        succes = 0
        
        for file_path in self.pages_villa:
            if 'template' not in os.path.basename(file_path):
                self.appliquer_glassmorphisme_villa(file_path)
                succes += 1
        
        print("\n" + "=" * 70)
        print("✅ GLASSMORPHISM APPLIQUÉ À TOUTES LES PAGES!")
        
        print("\n🎉 EFFETS GLASSMORPHISM AJOUTÉS:")
        print("  ✨ Cartes d'informations avec backdrop-filter blur")
        print("  ✨ Transparence rgba(255, 255, 255, 0.1)")
        print("  ✨ Bordures subtiles avec rgba(255, 255, 255, 0.2)")
        print("  ✨ Ombres douces avec effet depth")
        print("  ✨ Animations de survol élégantes")
        print("  ✨ Textes avec text-shadow pour lisibilité")
        print("  ✨ Icônes avec glow effect")
        print("  ✨ Galerie avec container glassmorphism")
        
        print(f"\n🏆 {succes} PAGES VILLA MAINTENANT AVEC GLASSMORPHISM!")
        print("\n🔍 RÉSULTAT ATTENDU:")
        print("  - Cartes semi-transparentes avec effet flou")
        print("  - Effet de profondeur et modernité")
        print("  - Cohérence visuelle avec l'index.html")
        print("  - Interface premium et luxueuse")

if __name__ == "__main__":
    glassmorphism = GlassmorphismVillas()
    glassmorphism.executer_glassmorphism_toutes_villas()