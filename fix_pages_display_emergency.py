#!/usr/bin/env python3
"""
CORRECTION URGENTE - Pages villa avec contenu invisible
"""

import os
import re
from pathlib import Path

def fix_display_issue(file_path):
    """Corriger le problème d'affichage du contenu"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"🔧 Correction affichage pour {file_path.name}...")
        
        # 1. FORCER L'AFFICHAGE DU CONTENU AVEC CSS
        css_fix = '''
        /* FORCE DISPLAY - Correction urgente */
        main.container {
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
            position: relative !important;
            z-index: 100 !important;
        }
        
        .gallery-container,
        .villa-gallery,
        .swiper,
        .swiper-wrapper,
        .swiper-slide,
        .info-card,
        section {
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
        }
        
        .swiper-slide {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        
        /* S'assurer que AOS n'interfère pas */
        [data-aos] {
            opacity: 1 !important;
            transform: none !important;
        }'''
        
        # Ajouter ce CSS avant </style>
        if '</style>' in content:
            content = content.replace('</style>', css_fix + '\n    </style>')
        
        # 2. SIMPLIFIER LE JAVASCRIPT - Supprimer AOS qui peut causer des problèmes
        content = content.replace('data-aos="fade-up"', '')
        content = content.replace('data-aos-delay="300"', '')
        content = content.replace('data-aos-delay="400"', '')
        content = content.replace('data-aos-delay="600"', '')
        
        # 3. CORRIGER L'INITIALISATION JAVASCRIPT
        js_fix = '''
        // CORRECTION URGENTE - Affichage forcé
        document.addEventListener("DOMContentLoaded", function() {
            console.log("🔧 Correction affichage démarrée");
            
            // Forcer l'affichage de tous les éléments
            const elementsToShow = [
                'main', '.gallery-container', '.villa-gallery', 
                '.info-card', '.swiper', '.swiper-wrapper', '.swiper-slide'
            ];
            
            elementsToShow.forEach(selector => {
                const elements = document.querySelectorAll(selector);
                elements.forEach(el => {
                    el.style.display = 'block';
                    el.style.visibility = 'visible';
                    el.style.opacity = '1';
                });
            });
            
            // Initialiser Swiper avec configuration simple
            setTimeout(() => {
                if (typeof Swiper !== 'undefined') {
                    new Swiper('.villa-gallery', {
                        loop: true,
                        autoplay: { delay: 5000 },
                        pagination: { el: '.swiper-pagination', clickable: true },
                        navigation: { 
                            nextEl: '.swiper-button-next', 
                            prevEl: '.swiper-button-prev' 
                        }
                    });
                    console.log("✅ Swiper initialisé");
                }
            }, 500);
            
            // Video background simple
            const video = document.getElementById('backgroundVideo');
            if (video) {
                video.play().catch(() => console.log("Video autoplay bloqué"));
            }
            
            console.log("✅ Correction affichage terminée");
        });'''
        
        # Remplacer le JavaScript existant par le nouveau
        content = re.sub(
            r'<script>.*?</script>',
            f'<script>{js_fix}</script>',
            content,
            flags=re.DOTALL
        )
        
        # Écrire le fichier corrigé
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ {file_path.name} corrigé pour l'affichage")
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur sur {file_path.name}: {str(e)}")
        return False

def main():
    print("🚨 CORRECTION URGENTE - AFFICHAGE PAGES VILLA")
    print("=" * 60)
    
    # Corriger toutes les pages villa
    villa_files = []
    for file in Path('/app').glob('villa-*.html'):
        if file.name not in ['villa-details.html', 'villa-template.html', 'villa-template-clean.html']:
            villa_files.append(file)
    
    print(f"🔧 Correction de {len(villa_files)} pages villa...")
    
    success_count = 0
    for villa_file in villa_files:
        if fix_display_issue(villa_file):
            success_count += 1
    
    print(f"\n✅ CORRECTION TERMINÉE: {success_count}/{len(villa_files)} pages corrigées")
    
    if success_count == len(villa_files):
        print("🎉 Toutes les pages villa devraient maintenant afficher leur contenu !")
    else:
        print("⚠️ Certaines pages ont encore des problèmes")

if __name__ == "__main__":
    main()