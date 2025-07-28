#!/usr/bin/env python3
"""
Script pour supprimer les sections "Information et tarifs UNIFIÉE" 
ajoutées par erreur et garder seulement les sections principales
"""

import os
import re
import glob

def clean_duplicate_sections(file_path):
    """Supprime les sections UNIFIÉE ajoutées par erreur"""
    
    filename = os.path.basename(file_path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Compter les sections avant nettoyage
    initial_count = content.count('Information et tarifs')
    
    # Pattern pour supprimer la section UNIFIÉE ajoutée par mon script
    pattern_unifie = r'<!-- Section Information et tarifs UNIFIÉE -->.*?</div>\s*</div>'
    
    # Supprimer cette section
    new_content = re.sub(pattern_unifie, '', content, flags=re.DOTALL)
    
    # Vérifier si des changements ont été effectués
    final_count = new_content.count('Information et tarifs')
    
    if final_count < initial_count:
        # Sauvegarder les changements
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ {filename}: Section UNIFIÉE supprimée ({initial_count} → {final_count})")
        return True
    else:
        print(f"ℹ️ {filename}: Aucune section UNIFIÉE trouvée")
        return False

def main():
    print("🧹 Nettoyage des sections 'Information et tarifs UNIFIÉE' ajoutées par erreur")
    print("=" * 70)
    
    villa_files = glob.glob('/app/villa-*.html')
    villa_files = [f for f in villa_files if 'template' not in f and 'details' not in f]
    
    cleaned_count = 0
    
    for file_path in sorted(villa_files):
        if clean_duplicate_sections(file_path):
            cleaned_count += 1
    
    print("=" * 70)
    print(f"🎯 Nettoyage terminé : {cleaned_count}/{len(villa_files)} pages nettoyées")
    print("✅ Les pages villa ont maintenant seulement leur section principale 'Informations et Tarifs Détaillés'")

if __name__ == "__main__":
    main()