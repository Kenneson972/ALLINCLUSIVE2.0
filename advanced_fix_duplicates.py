#!/usr/bin/env python3
"""
Script avancé pour supprimer les doublons des sections "Information et tarifs"
"""

import os
import re
import glob

def remove_duplicate_info_sections(file_path):
    """Supprime les sections Information et tarifs dupliquées"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Compter les occurrences
    count = content.count('Information et tarifs')
    if count <= 1:
        return False, f"Pas de doublon trouvé"
    
    # Identifier et supprimer les sections en double à la fin du fichier
    # Pattern pour détecter les sections dupliquées après le </script>
    
    # Chercher la position du dernier </script> avant </body>
    script_end_pattern = r'</script>\s*(?=(?:.*?</body>))'
    script_matches = list(re.finditer(script_end_pattern, content, re.DOTALL))
    
    if not script_matches:
        return False, "Impossible de localiser la fin des scripts"
    
    last_script_end = script_matches[-1].end()
    
    # Tout après le dernier </script> mais avant </body>
    after_scripts = content[last_script_end:]
    before_scripts = content[:last_script_end]
    
    # Supprimer toutes les sections "Information et tarifs" après les scripts
    # Pattern pour capturer une section complète
    section_pattern = r'<!-- Section Information et tarifs -->.*?</div>\s*</div>(?:\s*</div>)?'
    
    # Compter les sections dans after_scripts
    sections_after = re.findall(section_pattern, after_scripts, re.DOTALL)
    
    if len(sections_after) > 0:
        # Supprimer toutes les sections après les scripts
        cleaned_after = re.sub(section_pattern, '', after_scripts, flags=re.DOTALL)
        
        # Nettoyer les styles orphelins aussi
        style_pattern = r'<style>.*?\.tarif-card:hover.*?</style>'
        cleaned_after = re.sub(style_pattern, '', cleaned_after, flags=re.DOTALL)
        
        # Reconstruire le contenu
        new_content = before_scripts + cleaned_after
        
        # Vérifier le résultat
        new_count = new_content.count('Information et tarifs')
        
        if new_count < count:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, f"Supprimé {count - new_count} sections ({count} → {new_count})"
    
    return False, "Aucune section supprimable trouvée"

def main():
    print("🔧 Suppression avancée des doublons 'Information et tarifs'")
    print("=" * 60)
    
    villa_files = glob.glob('/app/villa-*.html')
    villa_files = [f for f in villa_files if 'template' not in f and 'details' not in f]
    
    fixed_count = 0
    
    for file_path in sorted(villa_files):
        filename = os.path.basename(file_path)
        success, message = remove_duplicate_info_sections(file_path)
        
        if success:
            print(f"✅ {filename}: {message}")
            fixed_count += 1
        else:
            print(f"ℹ️ {filename}: {message}")
    
    print("=" * 60)
    print(f"📊 Résumé: {fixed_count}/{len(villa_files)} fichiers corrigés")

if __name__ == "__main__":
    main()