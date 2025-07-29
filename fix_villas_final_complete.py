#!/usr/bin/env python3
"""
Corrections finales des pages villa :
1. Ajouter le logo dans le header
2. Optimiser le temps de chargement
3. Corriger l'affichage vide
"""

import os
import re
from pathlib import Path

def fix_villa_page(villa_file):
    """Corrige une page villa individuellement"""
    
    try:
        with open(villa_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"🔧 Correction de {villa_file.name}...")
        
        # 1. AJOUTER LE LOGO DANS LE HEADER
        old_header = r'<a href="./index.html" class="text-2xl font-bold text-yellow-400">🏝️ KhanelConcept</a>'
        new_header = '''<a href="./index.html" class="flex items-center space-x-3 text-yellow-400">
                    <img src="https://customer-assets.emergentagent.com/job_villa-dash/artifacts/vg7ukqf7_logo-khanel-concept-original.png" 
                         alt="Khanel Concept Logo" 
                         class="h-10 w-auto">
                    <span class="text-2xl font-bold">KhanelConcept</span>
                </a>'''
        
        if '🏝️ KhanelConcept</a>' in content:
            content = content.replace(old_header, new_header)
            print(f"  ✅ Logo ajouté au header")
        
        # 2. OPTIMISER LE CHARGEMENT - Ajouter le preloading CSS/JS
        if '<head>' in content and 'preload' not in content:
            preload_links = '''
    <!-- Preload Critical Resources -->
    <link rel="preload" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" as="style">
    <link rel="preload" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js" as="script">
    <link rel="preload" href="https://res.cloudinary.com/ddulasmtz/video/upload/v1752950782/background-video.mp4_qoofsz.mp4" as="video" type="video/mp4">'''
            
            content = content.replace('<head>', '<head>' + preload_links)
            print(f"  ✅ Preload ajouté pour optimisation")
        
        # 3. CORRIGER L'AFFICHAGE VIDE - S'assurer que le main content est visible
        if 'main class=' in content:
            # Ajouter du CSS pour garantir la visibilité
            visibility_css = '''
        /* Force visibility of main content */
        main.container {
            position: relative;
            z-index: 10;
            min-height: 100vh;
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
        }
        
        .info-card {
            display: block !important;
            visibility: visible !important;
        }
        
        .villa-gallery {
            display: block !important;
        }'''
            
            # Ajouter après les styles existants
            content = content.replace('</style>', visibility_css + '\n    </style>')
            print(f"  ✅ CSS de visibilité ajouté")
        
        # 4. OPTIMISER LE JAVASCRIPT - Chargement plus rapide
        if 'document.addEventListener(\'DOMContentLoaded\'' in content:
            # Remplacer par un chargement plus rapide
            content = content.replace(
                'document.addEventListener(\'DOMContentLoaded\', () => {',
                '''// Chargement optimisé
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initializePage);
        } else {
            initializePage();
        }
        
        function initializePage() {'''
            )
            
            # Fermer la fonction
            content = content.replace(
                '});',
                '''        }
        
        // Preload des images critiques
        function preloadCriticalImages() {
            const criticalImages = document.querySelectorAll('.villa-gallery img');
            criticalImages.forEach((img, index) => {
                if (index < 3) { // Preload les 3 premières images
                    const link = document.createElement('link');
                    link.rel = 'preload';
                    link.as = 'image';
                    link.href = img.src;
                    document.head.appendChild(link);
                }
            });
        }
        
        preloadCriticalImages();'''
            )
            print(f"  ✅ JavaScript optimisé")
        
        # 5. AMÉLIORER LA VIDÉO BACKGROUND
        if 'backgroundVideo' in content:
            # S'assurer que la vidéo démarre rapidement
            video_optimization = '''
        // Optimisation vidéo background
        function initVideoBackground() {
            const video = document.getElementById('backgroundVideo');
            if (video) {
                console.log('🎥 Démarrage optimisé vidéo background');
                video.muted = true;
                video.loop = true;
                video.setAttribute('playsinline', '');
                video.setAttribute('webkit-playsinline', '');
                video.setAttribute('preload', 'metadata');
                
                // Démarrage immédiat
                const playPromise = video.play();
                if (playPromise !== undefined) {
                    playPromise.then(() => {
                        console.log('✅ Vidéo démarrée instantanément');
                        video.style.opacity = '1';
                    }).catch(() => {
                        console.log('⚠️ Fallback vidéo');
                        document.querySelector('.video-overlay').style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
                    });
                }
                
                // Support mobile optimisé
                if (/iPad|iPhone|iPod|Android/i.test(navigator.userAgent)) {
                    video.setAttribute('muted', 'muted');
                    video.muted = true;
                    const touchHandler = () => {
                        video.play().catch(console.log);
                        document.removeEventListener('touchstart', touchHandler);
                    };
                    document.addEventListener('touchstart', touchHandler);
                }
            }
        }'''
            
            # Remplacer l'ancienne fonction
            content = re.sub(r'function initVideoBackground\(\) \{[^}]*\}', video_optimization, content, flags=re.DOTALL)
            print(f"  ✅ Vidéo background optimisée")
        
        # Écrire le fichier corrigé
        with open(villa_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {villa_file.name} corrigé avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur sur {villa_file.name}: {str(e)}")
        return False

def main():
    print("🏠 CORRECTIONS FINALES DES PAGES VILLA")
    print("1. Logo dans header")
    print("2. Optimisation chargement") 
    print("3. Correction affichage vide")
    print("=" * 60)
    
    # Trouver toutes les pages villa
    villa_files = []
    for file in Path('/app').glob('villa-*.html'):
        if file.name not in ['villa-details.html', 'villa-template.html']:
            villa_files.append(file)
    
    print(f"📁 {len(villa_files)} pages villa à corriger")
    
    success_count = 0
    for villa_file in villa_files:
        if fix_villa_page(villa_file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"🎉 TERMINÉ: {success_count}/{len(villa_files)} pages corrigées")
    
    if success_count == len(villa_files):
        print("✅ Toutes les corrections appliquées !")
        print("🏠 Pages villa optimisées avec logo et chargement rapide")
    else:
        print("⚠️ Certaines pages ont des problèmes")

if __name__ == "__main__":
    main()