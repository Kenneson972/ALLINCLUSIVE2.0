#!/usr/bin/env python3
"""
Correction vidéo background sur toutes les pages villa avec la VRAIE vidéo Cloudinary
"""

import os
import re
from pathlib import Path

# URL de la vraie vidéo background de l'index
CORRECT_VIDEO_URL = "https://res.cloudinary.com/ddulasmtz/video/upload/v1752950782/background-video.mp4_qoofsz.mp4"

def fix_video_background_in_file(file_path):
    """Corrige la vidéo background dans un fichier"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Corriger l'URL de la vidéo
        old_video_pattern = r'https://res\.cloudinary\.com/[^"]*\.mp4'
        content = re.sub(old_video_pattern, CORRECT_VIDEO_URL, content)
        
        # 2. S'assurer que la vidéo background est présente
        if 'video-background' not in content:
            print(f"🔧 Ajout vidéo background à {file_path.name}")
            
            # Ajouter après <body>
            video_bg_html = f'''
    <!-- Video Background avec votre vidéo Cloudinary -->
    <div class="video-background">
        <video id="backgroundVideo" autoplay muted loop playsinline preload="metadata" webkit-playsinline>
            <source src="{CORRECT_VIDEO_URL}" type="video/mp4">
            Votre navigateur ne supporte pas la lecture de vidéos HTML5.
        </video>
        <div class="video-overlay"></div>
    </div>'''
            
            content = content.replace('<body', video_bg_html + '\n<body')
        
        # 3. S'assurer que le CSS est correct
        if '.video-background' not in content:
            video_css = f'''
        /* Video Background avec votre vidéo Cloudinary */
        .video-background {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            overflow: hidden;
        }}
        
        .video-background video {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            opacity: 0.7;
        }}
        
        .video-overlay {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.4) 0%, rgba(118, 75, 162, 0.4) 100%);
        }}'''
            
            # Ajouter après le premier style
            content = content.replace('<style>', '<style>' + video_css)
        
        # 4. S'assurer que le JavaScript est correct
        if 'backgroundVideo' not in content:
            video_js = f'''
        // Initialize video background
        function initVideoBackground() {{
            const video = document.getElementById('backgroundVideo');
            if (video) {{
                console.log('🎥 Démarrage vidéo background');
                video.muted = true;
                video.loop = true;
                video.play().catch(e => console.log('Vidéo autoplay bloqué:', e));
                
                // Support mobile
                if (/iPad|iPhone|iPod|Android/i.test(navigator.userAgent)) {{
                    document.addEventListener('touchstart', function() {{
                        video.play().catch(console.log);
                    }}, {{ once: true }});
                }}
            }}
        }}
        
        // Initialiser au chargement
        document.addEventListener('DOMContentLoaded', initVideoBackground);'''
            
            # Ajouter avant </script>
            content = content.replace('</script>', video_js + '\n    </script>')
        
        # Écrire le fichier corrigé
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur sur {file_path.name}: {str(e)}")
        return False

def main():
    print("🎥 CORRECTION VIDÉO BACKGROUND SUR TOUTES LES PAGES VILLA")
    print(f"Vidéo utilisée: {CORRECT_VIDEO_URL}")
    print("=" * 70)
    
    # Trouver toutes les pages villa
    villa_files = []
    for file in Path('/app').glob('villa-*.html'):
        if file.name not in ['villa-details.html', 'villa-template.html']:
            villa_files.append(file)
    
    print(f"📁 {len(villa_files)} pages villa à corriger")
    
    success_count = 0
    for villa_file in villa_files:
        if fix_video_background_in_file(villa_file):
            success_count += 1
            print(f"✅ {villa_file.name}")
        else:
            print(f"❌ {villa_file.name}")
    
    print("\n" + "=" * 70)
    print(f"🎉 TERMINÉ: {success_count}/{len(villa_files)} pages corrigées")
    
    if success_count == len(villa_files):
        print("✅ Vidéo background active sur toutes les pages villa !")
    else:
        print("⚠️ Certaines pages ont des problèmes")

if __name__ == "__main__":
    main()