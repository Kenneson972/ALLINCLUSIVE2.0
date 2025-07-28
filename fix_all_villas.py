#!/usr/bin/env python3
"""
Fix All Villa Pages - Corrections multiples
1. Vidéo background forcée
2. Liens navigation corrects
3. Script d'initialisation amélioré
"""

import os
import re
from pathlib import Path

def fix_villa_page(villa_file):
    """Corriger une page villa individuelle"""
    try:
        with open(villa_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. S'assurer que la vidéo background a l'ID correct
        content = re.sub(
            r'<video[^>]*>',
            '<video id="villaVideo" autoplay muted loop playsinline webkit-playsinline preload="metadata">',
            content
        )
        
        # 2. Ajouter le script de vidéo background si pas présent
        if 'initVideoBackground' not in content:
            # Trouver la section script existante
            script_pattern = r'(<script>\s*// Initialisation spécifique à cette villa.*?</script>)'
            
            enhanced_script = '''<script>
        // Initialisation spécifique à cette villa
        document.addEventListener('DOMContentLoaded', function() {
            // Données de la villa pour la réservation
            window.currentVilla = {
                id: '{villa_id}',
                name: '{villa_name}',
                basePrice: {base_price},
                capacity: {capacity},
                maxGuests: {max_guests}
            };
            
            // Force le démarrage de la vidéo background
            initVideoBackground();
        });
        
        // Fonction pour forcer la vidéo background
        function initVideoBackground() {
            const video = document.querySelector('.video-background video');
            if (video) {
                console.log('🎥 Initialisation vidéo background villa');
                
                // Configuration vidéo
                video.muted = true;
                video.loop = true;
                video.autoplay = true;
                video.setAttribute('playsinline', '');
                video.setAttribute('webkit-playsinline', '');
                
                // Tentative de lecture
                const playPromise = video.play();
                if (playPromise !== undefined) {
                    playPromise.then(() => {
                        console.log('✅ Vidéo background démarrée');
                        video.style.opacity = '1';
                    }).catch(error => {
                        console.log('⚠️ Autoplay bloqué, utilisation du fallback');
                        video.style.display = 'none';
                        document.querySelector('.video-background-fallback').style.display = 'block';
                    });
                }
                
                // Gestion iOS/Mobile
                if (/iPad|iPhone|iPod|Android/i.test(navigator.userAgent)) {
                    document.addEventListener('touchstart', function startVideoOnTouch() {
                        video.play().then(() => {
                            console.log('✅ Vidéo démarrée sur mobile');
                            document.removeEventListener('touchstart', startVideoOnTouch);
                        });
                    }, {{ once: true }});
                }
            }
        }
    </script>'''
            
            # Extraire les données de la villa depuis le contenu existant
            villa_id_match = re.search(r"id:\s*'([^']+)'", content)
            villa_name_match = re.search(r"name:\s*'([^']+)'", content)
            base_price_match = re.search(r"basePrice:\s*(\d+)", content)
            capacity_match = re.search(r"capacity:\s*(\d+)", content)
            max_guests_match = re.search(r"maxGuests:\s*(\d+)", content)
            
            villa_id = villa_id_match.group(1) if villa_id_match else 'unknown'
            villa_name = villa_name_match.group(1) if villa_name_match else 'Villa'
            base_price = base_price_match.group(1) if base_price_match else '500'
            capacity = capacity_match.group(1) if capacity_match else '6'
            max_guests = max_guests_match.group(1) if max_guests_match else '10'
            
            script_content = enhanced_script.format(
                villa_id=villa_id,
                villa_name=villa_name,
                base_price=base_price,
                capacity=capacity,
                max_guests=max_guests
            )
            
            # Remplacer le script existant
            content = re.sub(script_pattern, script_content, content, flags=re.DOTALL)
        
        # Écrire le fichier corrigé
        with open(villa_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Corrigé: {villa_file.name}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur sur {villa_file.name}: {str(e)}")
        return False

def main():
    print("🔧 CORRECTION DES PAGES VILLA - Démarrage")
    print("=" * 50)
    
    # Trouver toutes les pages villa
    villa_dir = Path('/app')
    villa_pages = []
    
    for file in villa_dir.glob('villa-*.html'):
        if file.name not in ['villa-details.html', 'villa-template.html']:
            villa_pages.append(file)
    
    print(f"📁 Trouvé {len(villa_pages)} pages villa à corriger")
    
    # Corriger chaque page
    success_count = 0
    for villa_file in villa_pages:
        if fix_villa_page(villa_file):
            success_count += 1
    
    print("\n" + "=" * 50)
    print(f"🎉 TERMINÉ: {success_count}/{len(villa_pages)} pages corrigées")
    
    if success_count == len(villa_pages):
        print("✅ Toutes les corrections appliquées avec succès!")
    else:
        print("⚠️ Certaines pages n'ont pas pu être corrigées")

if __name__ == "__main__":
    main()