#!/usr/bin/env python3
"""
Correction FINALE de toutes les pages villa
- Vidéo background corrigée
- Vraies images des villas
- Interface uniforme moderne
"""

import os
import csv
import re
from pathlib import Path

# Mapping correct des villas avec leurs dossiers d'images
VILLA_IMAGE_MAPPING = {
    'villa-f3-petit-macabou': 'Villa_F3_Petit_Macabou',
    'villa-f3-baccha': 'Villa_F3_Baccha_Petit_Macabou', 
    'villa-f3-le-franois': 'Villa_F3_Le_Francois',
    'villa-f5-ste-anne': 'Villa_F5_Ste_Anne',
    'villa-f6-au-lamentin': 'Villa_F6_Lamentin',
    'villa-f6-ste-luce--1mn-de-la-plage': 'Villa_F6_Ste_Luce_Plage',
    'villa-f3-bas-de-trinit-cosmy': 'Villa_F3_Trinite_Cosmy',
    'villa-bas-de-f3-le-robert': 'Villa_F3_Robert_Pointe_Hyacinthe',
    'villa-appartement-f3-trenelle-location-annuelle': 'Villa_F3_Trenelle_Location_Annuelle',
    'villa-f5-vauclin-ravine-plate': 'Villa_F5_Vauclin_Ravine_Plate',
    'villa-f5-la-rene': 'Villa_F5_R_Pilote_La_Renee',
    'villa-f7-baie-des-mulets': 'Villa_F7_Baie_des_Mulets_Vauclin',
    'villa-bas-de-f3-ste-luce': 'Bas_Villa_F3_Ste_Luce',
    'villa-studio-cocooning-lamentin': 'Studio_Cocooning_Lamentin',
    'villa-fte-journe-ducos': 'Villa_Fete_Journee_Ducos',
    'villa-fte-journe-fort-de-france': 'Villa_Fete_Journee_Fort_de_France',
    'villa-fte-journe-rivire-pilote': 'Villa_Fete_Journee_R_Pilote',
    'villa-fte-journe-rivire-sale': 'Villa_Fete_Journee_Riviere_Salee',
    'villa-fte-journe-sainte-luce': 'Villa_Fete_Journee_Sainte_Luce',
    'villa-espace-piscine-journe-bungalow': 'Espace_Piscine_Journee_Bungalow',
    'villa-f6-petit-macabou-sjour--fte': 'Villa_F6_Petit_Macabou'
}

def get_real_images(villa_id):
    """Récupère les vraies images d'une villa"""
    image_folder = VILLA_IMAGE_MAPPING.get(villa_id)
    
    if not image_folder:
        print(f"⚠️ Pas de mapping d'images pour {villa_id}")
        return []
    
    image_path = f"/app/images/{image_folder}"
    images = []
    
    if os.path.exists(image_path):
        for file in sorted(os.listdir(image_path)):
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                images.append(f"./images/{image_folder}/{file}")
        print(f"✅ Trouvé {len(images)} images pour {villa_id}")
    else:
        print(f"❌ Dossier non trouvé: {image_path}")
    
    return images

def fix_villa_page(villa_file):
    """Corrige une page villa avec vraies images et vidéo background"""
    
    try:
        with open(villa_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extraire l'ID de la villa du nom de fichier
        villa_id = villa_file.stem
        
        # 1. CORRIGER LA VIDÉO BACKGROUND
        # Vérifier si la vidéo background existe
        if 'video-background' not in content:
            print(f"🔧 Ajout vidéo background pour {villa_id}")
            # Ajouter après <body>
            video_bg = '''
    <!-- Background Video Cloudinary -->
    <div class="video-background">
        <video id="backgroundVideo" autoplay muted loop playsinline preload="metadata" webkit-playsinline>
            <source src="https://res.cloudinary.com/dqz8rw6m2/video/upload/v1733669700/martinique-bg_d0pzjm.mp4" type="video/mp4">
            Votre navigateur ne supporte pas la lecture de vidéos HTML5.
        </video>
        <div class="video-overlay"></div>
    </div>'''
            
            content = content.replace('<body', video_bg + '\n<body')
        
        # 2. CORRIGER LE CSS DE LA VIDÉO BACKGROUND
        if '.video-background' not in content:
            print(f"🔧 Ajout CSS vidéo background pour {villa_id}")
            video_css = '''
        /* Video Background */
        .video-background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -2;
            overflow: hidden;
        }
        
        .video-background video {
            width: 100%;
            height: 100%;
            object-fit: cover;
            opacity: 0.7;
        }
        
        .video-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.8) 0%, rgba(30, 41, 59, 0.8) 100%);
        }'''
            
            # Ajouter après le :root
            content = content.replace('body {', video_css + '\n\n        body {')
        
        # 3. CORRIGER LES IMAGES AVEC LES VRAIES PHOTOS
        real_images = get_real_images(villa_id)
        
        if real_images:
            print(f"🖼️ Remplacement images pour {villa_id}")
            
            # Remplacer les slides Swiper
            gallery_slides = ""
            for i, img in enumerate(real_images):
                gallery_slides += f'''
        <div class="swiper-slide">
            <img src="{img}" alt="{villa_id} - Image {i+1}" loading="lazy">
        </div>'''
            
            # Remplacer les thumbnails
            gallery_thumbnails = ""
            for i, img in enumerate(real_images):
                active_class = "active" if i == 0 else ""
                gallery_thumbnails += f'''
        <img src="{img}" alt="Thumbnail {i+1}" class="{active_class}" onclick="openModal(this.src, {i})">'''
            
            # Remplacer dans le contenu
            # Pattern pour trouver les slides existants
            slides_pattern = r'<div class="swiper-wrapper">.*?</div>'
            content = re.sub(slides_pattern, f'<div class="swiper-wrapper">{gallery_slides}\n                    </div>', content, flags=re.DOTALL)
            
            # Pattern pour trouver les thumbnails
            thumbs_pattern = r'<div class="gallery-thumbnails[^>]*>.*?</div>'
            content = re.sub(thumbs_pattern, f'<div class="gallery-thumbnails">{gallery_thumbnails}\n                </div>', content, flags=re.DOTALL)
        
        # 4. CORRIGER LE SCRIPT D'INITIALISATION VIDÉO
        if 'initVideoBackground' not in content:
            print(f"🔧 Ajout script vidéo pour {villa_id}")
            video_script = '''
        // Initialize video background
        function initVideoBackground() {
            const video = document.getElementById('backgroundVideo');
            if (video) {
                console.log('🎥 Initialisation vidéo background');
                video.muted = true;
                video.loop = true;
                video.autoplay = true;
                video.setAttribute('playsinline', '');
                video.setAttribute('webkit-playsinline', '');
                
                const playPromise = video.play();
                if (playPromise !== undefined) {
                    playPromise.then(() => {
                        console.log('✅ Vidéo background démarrée');
                        video.style.opacity = '1';
                    }).catch(error => {
                        console.log('⚠️ Autoplay bloqué:', error);
                    });
                }
                
                // Support mobile
                if (/iPad|iPhone|iPod|Android/i.test(navigator.userAgent)) {
                    document.addEventListener('touchstart', function() {
                        video.play().catch(console.log);
                    }, { once: true });
                }
            }
        }'''
            
            # Ajouter avant document.addEventListener('DOMContentLoaded'
            content = content.replace("document.addEventListener('DOMContentLoaded', () => {", 
                                    video_script + "\n\n        document.addEventListener('DOMContentLoaded', () => {\n            initVideoBackground();")
        
        # 5. S'ASSURER QUE LE BODY A LE BON BACKGROUND
        if 'body {' in content and 'background:' not in content:
            content = content.replace('body {', '''body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            min-height: 100vh;
            color: white;''')
        
        # Écrire le fichier corrigé
        with open(villa_file, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ {villa_id} corrigé avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur sur {villa_file}: {str(e)}")
        return False

def main():
    print("🔧 CORRECTION FINALE DE TOUTES LES PAGES VILLA")
    print("- Vidéo background activée")
    print("- Vraies images des villas") 
    print("- Interface uniforme moderne")
    print("=" * 60)
    
    # Trouver toutes les pages villa
    villa_pages = []
    for file in Path('/app').glob('villa-*.html'):
        if file.name not in ['villa-details.html', 'villa-template.html']:
            villa_pages.append(file)
    
    print(f"📁 {len(villa_pages)} pages villa à corriger")
    
    success_count = 0
    for villa_file in villa_pages:
        if fix_villa_page(villa_file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"🎉 TERMINÉ: {success_count}/{len(villa_pages)} pages corrigées")
    
    if success_count == len(villa_pages):
        print("✅ Toutes les corrections appliquées !")
        print("🎥 Vidéo background active sur toutes les pages")
        print("🖼️ Vraies images utilisées pour chaque villa")
    else:
        print("⚠️ Certaines pages ont des problèmes")

if __name__ == "__main__":
    main()