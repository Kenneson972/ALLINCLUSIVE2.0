#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script complémentaire pour ajouter les assets bg-video.css et bg-video.js
aux pages critiques même si elles ont déjà des éléments vidéo background
"""

import os
import re

def add_bg_video_assets_to_critical_pages():
    """Ajouter les assets bg-video aux pages critiques"""
    
    critical_pages = [
        '/app/index.html',
        '/app/reservation.html'
    ]
    
    cache_bust = '?v=20250807'
    css_link = f'<link rel="stylesheet" href="assets/css/bg-video.css{cache_bust}">'
    js_link = f'<script defer src="assets/js/bg-video.js{cache_bust}"></script>'
    
    for page_path in critical_pages:
        if not os.path.exists(page_path):
            print(f"❌ Page non trouvée: {page_path}")
            continue
        
        filename = os.path.basename(page_path)
        print(f"🔧 Traitement: {filename}")
        
        try:
            # Lire le contenu
            with open(page_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier si les assets sont déjà présents
            has_bg_css = 'bg-video.css' in content
            has_bg_js = 'bg-video.js' in content
            
            if has_bg_css and has_bg_js:
                print(f"   ✅ Assets déjà présents")
                continue
            
            # Créer sauvegarde
            backup_path = page_path.replace('.html', '_backup_critical.html')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   💾 Sauvegarde: {os.path.basename(backup_path)}")
            
            # Ajouter les assets manquants
            new_content = content
            
            if not has_bg_css:
                if '</head>' in content:
                    new_content = new_content.replace('</head>', f'    {css_link}\\n</head>')
                    print(f"   ✅ CSS ajouté")
            
            if not has_bg_js:
                if '</head>' in content:
                    new_content = new_content.replace('</head>', f'    {js_link}\\n</head>')
                    print(f"   ✅ JS ajouté")
            
            # Sauvegarder
            with open(page_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"   ✅ {filename} mis à jour")
            
        except Exception as e:
            print(f"   ❌ Erreur: {e}")

def main():
    print("🔧 AJOUT ASSETS BG-VIDEO AUX PAGES CRITIQUES")
    print("=" * 50)
    
    add_bg_video_assets_to_critical_pages()
    
    print("\\n✅ Traitement terminé")

if __name__ == "__main__":
    main()