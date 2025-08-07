#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour FORCER l'ajout des assets bg-video.css et bg-video.js 
sur TOUTES les pages importantes, même si elles ont déjà des éléments vidéo
"""

import os
import glob

def force_add_bg_video_assets():
    """Forcer l'ajout des assets sur toutes les pages importantes"""
    
    cache_bust = '?v=20250807'
    
    # Pages à traiter absolument
    important_patterns = [
        '/app/*.html',
        '/app/villa-*.html',
        '/app/*villa*.html'
    ]
    
    all_files = []
    for pattern in important_patterns:
        all_files.extend(glob.glob(pattern))
    
    # Supprimer doublons et trier
    all_files = sorted(list(set(all_files)))
    
    # Exclure les backups et fichiers temporaires
    important_files = [f for f in all_files if not any(x in f for x in ['backup', 'min.html', 'test', 'example', 'fixed', 'corrected'])]
    
    print(f"🔧 Pages importantes à traiter: {len(important_files)}")
    
    success_count = 0
    
    for filepath in important_files:
        filename = os.path.basename(filepath)
        print(f"🎬 {filename}...", end=" ")
        
        try:
            # Lire le contenu
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Calculer le prefix selon la profondeur
            relative_path = os.path.relpath(filepath, '/app')
            depth = len(relative_path.split(os.sep)) - 1
            prefix = "../" * depth if depth > 0 else ""
            
            # Créer les liens
            css_link = f'<link rel="stylesheet" href="{prefix}assets/css/bg-video.css{cache_bust}">'
            js_link = f'<script defer src="{prefix}assets/js/bg-video.js{cache_bust}"></script>'
            
            # Vérifier si déjà présents
            has_css = 'bg-video.css' in content
            has_js = 'bg-video.js' in content
            
            if has_css and has_js:
                print("déjà OK")
                success_count += 1
                continue
            
            # Créer sauvegarde
            backup_path = filepath.replace('.html', '_backup_force.html')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Ajouter les assets manquants
            new_content = content
            
            if not has_css and '</head>' in content:
                new_content = new_content.replace('</head>', f'    {css_link}\\n</head>')
            
            if not has_js and '</head>' in content:
                new_content = new_content.replace('</head>', f'    {js_link}\\n</head>')
            
            # Sauvegarder
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ ajouté")
            success_count += 1
            
        except Exception as e:
            print(f"❌ {e}")
    
    print(f"\\n📊 Résultat: {success_count}/{len(important_files)} pages traitées")
    return success_count

def main():
    print("🚀 FORÇAGE ASSETS BG-VIDEO SUR TOUTES LES PAGES IMPORTANTES")
    print("=" * 60)
    
    force_add_bg_video_assets()
    
    print("\\n✅ Traitement terminé")

if __name__ == "__main__":
    main()