#!/usr/bin/env python3
"""
Script de nettoyage final pour supprimer les anciennes sections
et ne garder que la section unifiée "Informations Complètes et Tarifs"
"""

import os
import re
import glob

def clean_old_sections(file_path):
    """Supprime toutes les anciennes sections sauf la nouvelle section unifiée"""
    
    filename = os.path.basename(file_path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Compter les sections avant nettoyage
    info_count_before = content.count('Information')
    
    # Patterns pour supprimer les ANCIENNES sections (pas la nouvelle)
    old_patterns = [
        # Ancienne section "Informations et Tarifs Détaillés" (sans "Complètes")
        r'<!-- Informations et Tarifs Détaillés -->.*?</div>\s*</div>',
        # Sections avec h3 "Informations et Tarifs" (pas "Complètes")
        r'<h3[^>]*>.*?<i class="fas fa-info-circle[^>]*></i>\s*Informations et Tarifs\s*</h3>.*?</div>\s*</div>(?!</div>\s*</div>)',
        # Sections orphelines avec tarifs basiques
        r'<div class="mb-6">\s*<h4[^>]*>📋 Tarification</h4>.*?</div>\s*</div>',
        r'<div class="mb-6">\s*<h4[^>]*>📝 Conditions de Location</h4>.*?</div>\s*</div>',
    ]
    
    sections_removed = 0
    
    # Supprimer les anciennes sections
    for pattern in old_patterns:
        matches = re.findall(pattern, content, re.DOTALL)
        for match in matches:
            # S'assurer qu'on ne supprime pas la section unifiée
            if "Informations Complètes et Tarifs" not in match:
                content = content.replace(match, '', 1)
                sections_removed += 1
    
    # Nettoyer les div orphelines vides
    content = re.sub(r'<div[^>]*>\s*</div>', '', content, flags=re.MULTILINE)
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)  # Supprimer les lignes vides multiples
    
    # Compter après nettoyage
    info_count_after = content.count('Information')
    
    if sections_removed > 0:
        # Sauvegarder les changements
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {filename}: {sections_removed} anciennes sections supprimées")
        
        # Vérifier que la section unifiée est toujours présente
        if "Informations Complètes et Tarifs" in content:
            print(f"   ✅ Section unifiée préservée")
        else:
            print(f"   ⚠️ Section unifiée manquante!")
        
        return True
    else:
        print(f"ℹ️ {filename}: Aucune ancienne section trouvée")
        return False

def main():
    print("🧹 NETTOYAGE FINAL - Suppression des anciennes sections")
    print("=" * 60)
    print("OBJECTIF : Garder SEULEMENT la section 'Informations Complètes et Tarifs'")
    print("=" * 60)
    
    villa_files = glob.glob('/app/villa-*.html')
    villa_files = [f for f in villa_files if 'template' not in f and 'details' not in f]
    
    cleaned_count = 0
    
    for file_path in sorted(villa_files):
        if clean_old_sections(file_path):
            cleaned_count += 1
    
    print("=" * 60)
    print(f"🎯 NETTOYAGE TERMINÉ : {cleaned_count}/{len(villa_files)} villas nettoyées")
    print("✅ Chaque villa a maintenant SEULEMENT sa section unifiée avec données CSV")

if __name__ == "__main__":
    main()