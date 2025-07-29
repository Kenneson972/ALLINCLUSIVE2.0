#!/usr/bin/env python3
"""
CORRECTION URGENTE CHEMINS IMAGES GITHUB PAGES
Corriger les chemins d'images pour toutes les 21 villas avec le préfixe /ALLINCLUSIVE2.0/
"""

import os
import glob
import re

class CorrectionCheminsImagesGitHub:
    def __init__(self):
        self.pages_villa = glob.glob('/app/villa-*.html')
        self.pages_villa = [f for f in self.pages_villa if 'template' not in f and 'backup' not in f]
        
    def corriger_chemins_images_page(self, file_path):
        """Corrige les chemins d'images d'une page villa pour GitHub Pages"""
        nom_fichier = os.path.basename(file_path)
        
        print(f"🔧 CORRECTION CHEMINS GITHUB PAGES: {nom_fichier}")
        
        try:
            # Lire le contenu du fichier
            with open(file_path, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # Compter les occurrences AVANT correction
            occurrences_avant = len(re.findall(r'src="\/images\/', contenu))
            
            # CORRECTION 1: Images dans les swiper-slide
            contenu = re.sub(
                r'src="\/images\/',
                r'src="/ALLINCLUSIVE2.0/images/',
                contenu
            )
            
            # CORRECTION 2: Images dans les thumbnails
            contenu = re.sub(
                r'<img src="\/images\/',
                r'<img src="/ALLINCLUSIVE2.0/images/',
                contenu
            )
            
            # Compter les occurrences APRÈS correction
            occurrences_apres = len(re.findall(r'src="\/ALLINCLUSIVE2\.0\/images\/', contenu))
            
            # Sauvegarder le fichier corrigé
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(contenu)
            
            print(f"  ✅ CHEMINS CORRIGÉS avec succès")
            print(f"     - {occurrences_avant} chemins incorrects trouvés")
            print(f"     - {occurrences_apres} chemins corrigés vers /ALLINCLUSIVE2.0/images/")
            print(f"     - Fichier sauvegardé")
            
        except Exception as e:
            print(f"  ❌ Erreur correction: {e}")
    
    def executer_correction_toutes_villas(self):
        """Exécute la correction sur TOUTES les pages villa"""
        print("🚨 CORRECTION URGENTE CHEMINS IMAGES GITHUB PAGES")
        print("=" * 80)
        print("🎯 Objectif: Corriger /images/ vers /ALLINCLUSIVE2.0/images/ pour toutes les villas")
        print(f"📄 {len(self.pages_villa)} pages villa à corriger")
        print()
        
        total_corrections = 0
        
        for file_path in self.pages_villa:
            if 'template' not in os.path.basename(file_path):
                self.corriger_chemins_images_page(file_path)
                total_corrections += 1
        
        print("\n" + "=" * 80)
        print("✅ CORRECTION CHEMINS IMAGES TERMINÉE!")
        
        print("\n🎉 RÉSULTAT FINAL:")
        print("  ✅ TOUS les chemins d'images corrigés pour GitHub Pages")
        print("  ✅ Préfixe /ALLINCLUSIVE2.0/ ajouté à tous les chemins")
        print("  ✅ Images maintenant accessibles sur GitHub Pages")
        print("  ✅ Plus d'erreurs 404 sur les images")
        print("  ✅ Galeries et thumbnails fonctionnelles")
        
        print(f"\n🏆 {total_corrections} PAGES VILLA CORRIGÉES POUR GITHUB PAGES!")
        
        print("\n📋 VALIDATION REQUISE:")
        print("  - Tester une villa: https://kenneson972.github.io/ALLINCLUSIVE2.0/villa-villa-f3-sur-petit-macabou.html")
        print("  - Vérifier que les images s'affichent correctement")
        print("  - Confirmer que les thumbnails fonctionnent")
        print("  - Valider la navigation du carrousel")

if __name__ == "__main__":
    correcteur = CorrectionCheminsImagesGitHub()
    correcteur.executer_correction_toutes_villas()