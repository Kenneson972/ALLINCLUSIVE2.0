#!/usr/bin/env python3
"""
Script pour corriger les doublons "Information et tarifs" dans les pages villa
"""

import os
import re
import glob

def fix_duplicate_sections(file_path):
    """Supprime les doublons de sections Information et tarifs"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Compter les occurrences de "Information et tarifs"
    count = content.count('Information et tarifs')
    if count <= 1:
        print(f"✅ {os.path.basename(file_path)}: Pas de doublon trouvé")
        return False
    
    print(f"🔍 {os.path.basename(file_path)}: {count} occurrences trouvées")
    
    # Détecter les patterns de duplication
    patterns_to_remove = [
        # Pattern 1: Section complète dupliquée après les styles
        r'<!-- Section Information et tarifs -->\s*<div class="information-tarifs-section"[^>]*>.*?</div>\s*</div>\s*(?=</body>|$)',
        # Pattern 2: Section complète avec styles
        r'<style>.*?\.tarif-card:hover.*?</style>\s*<!-- Section Information et tarifs -->.*?</div>\s*</div>',
    ]
    
    original_content = content
    
    # Essayer de supprimer les doublons avec des patterns spécifiques
    for pattern in patterns_to_remove:
        matches = re.findall(pattern, content, re.DOTALL)
        if len(matches) > 0:
            # Supprimer seulement les occurrences supplémentaires (garder la première)
            for i, match in enumerate(matches[1:], 1):  # Commencer à partir de la 2ème occurrence
                content = content.replace(match, '', 1)
                print(f"  ✂️ Supprimé la {i+1}ème occurrence")
    
    # Vérification finale
    new_count = content.count('Information et tarifs')
    
    if new_count < count:
        # Sauvegarder les changements
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Correction réussie: {count} → {new_count} occurrences")
        return True
    else:
        print(f"  ⚠️ Aucune correction automatique possible")
        return False

def main():
    print("🚀 Correction des doublons 'Information et tarifs' dans les pages villa")
    print("=" * 70)
    
    # Trouver tous les fichiers villa
    villa_files = glob.glob('/app/villa-*.html')
    
    fixed_count = 0
    
    for file_path in sorted(villa_files):
        if fix_duplicate_sections(file_path):
            fixed_count += 1
    
    print("=" * 70)
    print(f"📊 Résumé: {fixed_count}/{len(villa_files)} fichiers corrigés")
    
    if fixed_count > 0:
        print("✅ Corrections terminées avec succès!")
    else:
        print("ℹ️ Aucune correction nécessaire")

if __name__ == "__main__":
    main()