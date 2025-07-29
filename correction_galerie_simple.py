#!/usr/bin/env python3
"""
CORRECTION GALERIES SIMPLIFIÉE - APPROCHE MANUELLE
Corriger le décalage thumbnails et retirer les infos catalogue
"""

import os
import glob

class CorrectionGalerieSimple:
    def __init__(self):
        self.pages_villa = glob.glob('/app/villa-*.html')[:5]  # Test sur 5 pages d'abord
        
    def corriger_javascript_seulement(self, file_path):
        """Corrige seulement le JavaScript pour éviter le décalage"""
        nom_fichier = os.path.basename(file_path)
        
        print(f"🔧 CORRECTION JS: {nom_fichier}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # Remplacer le JavaScript problématique
            ancien_js = '''        // Initialize Swiper
        const swiper = new Swiper('.villa-gallery', {
            slidesPerView: 1,
            spaceBetween: 10,
            loop: true,
            autoplay: {
                delay: 4000,
                disableOnInteraction: false,
            },
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
            },
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
        });

        // Thumbnail navigation
        document.querySelectorAll('.gallery-thumbnails img').forEach((thumb, index) => {
            thumb.addEventListener('click', () => {
                swiper.slideTo(index);
                document.querySelectorAll('.gallery-thumbnails img').forEach(t => t.classList.remove('active'));
                thumb.classList.add('active');
            });
        });'''
            
            nouveau_js = '''        // Initialize Swiper - CORRIGÉ POUR ÉVITER DÉCALAGE
        const swiper = new Swiper('.villa-gallery', {
            slidesPerView: 1,
            spaceBetween: 10,
            loop: false,  // DÉSACTIVÉ pour éviter le décalage
            autoplay: {
                delay: 4000,
                disableOnInteraction: false,
            },
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
            },
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
        });

        // Thumbnail navigation - CORRIGÉ pour synchronisation parfaite
        document.querySelectorAll('.gallery-thumbnails img').forEach((thumb, index) => {
            thumb.addEventListener('click', (e) => {
                e.preventDefault();
                
                // Aller directement à la slide correspondante
                swiper.slideTo(index, 300);
                
                // Mettre à jour les classes active
                document.querySelectorAll('.gallery-thumbnails img').forEach(t => t.classList.remove('active'));
                thumb.classList.add('active');
                
                console.log(`✅ Thumbnail ${index + 1} -> Slide ${index + 1}`);
            });
        });

        // Synchroniser les thumbnails quand on change de slide avec les flèches
        swiper.on('slideChange', function() {
            const activeIndex = swiper.activeIndex;
            
            // Mettre à jour la thumbnail active correspondante
            document.querySelectorAll('.gallery-thumbnails img').forEach((thumb, index) => {
                if (index === activeIndex) {
                    thumb.classList.add('active');
                } else {
                    thumb.classList.remove('active');
                }
            });
            
            console.log(`✅ Slide changed to ${activeIndex + 1}`);
        });'''
            
            # Remplacer le JavaScript
            if ancien_js in contenu:
                contenu = contenu.replace(ancien_js, nouveau_js)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(contenu)
                
                print(f"  ✅ JavaScript CORRIGÉ")
                print(f"     - Loop désactivé (évite décalage)")
                print(f"     - Synchronisation thumbnails améliorée")
                print(f"     - Console logs ajoutés pour debug")
            else:
                print(f"  ⚠️ Ancien JS non trouvé - structure différente")
                
        except Exception as e:
            print(f"  ❌ Erreur: {e}")
    
    def corriger_alt_text_images(self, file_path):
        """Corrige les alt text pour enlever les infos catalogue"""
        nom_fichier = os.path.basename(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # Compter les corrections avant
            corrections = 0
            
            # Remplacer les alt text détaillés par des simples
            # Pour les images de galerie
            lignes = contenu.split('\n')
            nouvelles_lignes = []
            
            for ligne in lignes:
                if 'alt="Villa F3' in ligne or 'alt="Villa F5' in ligne or 'alt="Villa F6' in ligne or 'alt="Villa F7' in ligne or 'alt="Bas de villa' in ligne or 'alt="Studio' in ligne or 'alt="Appartement' in ligne:
                    if 'Image' in ligne:
                        # Extraire le numéro d'image
                        if 'Image 1"' in ligne:
                            ligne = ligne.replace(ligne[ligne.find('alt="'):ligne.find('"', ligne.find('alt="')+5)+1], 'alt="Image 1"')
                        elif 'Image 2"' in ligne:
                            ligne = ligne.replace(ligne[ligne.find('alt="'):ligne.find('"', ligne.find('alt="')+5)+1], 'alt="Image 2"')
                        elif 'Image 3"' in ligne:
                            ligne = ligne.replace(ligne[ligne.find('alt="'):ligne.find('"', ligne.find('alt="')+5)+1], 'alt="Image 3"')
                        elif 'Image 4"' in ligne:
                            ligne = ligne.replace(ligne[ligne.find('alt="'):ligne.find('"', ligne.find('alt="')+5)+1], 'alt="Image 4"')
                        elif 'Image 5"' in ligne:
                            ligne = ligne.replace(ligne[ligne.find('alt="'):ligne.find('"', ligne.find('alt="')+5)+1], 'alt="Image 5"')
                        elif 'Image 6"' in ligne:
                            ligne = ligne.replace(ligne[ligne.find('alt="'):ligne.find('"', ligne.find('alt="')+5)+1], 'alt="Image 6"')
                        elif 'Image 7"' in ligne:
                            ligne = ligne.replace(ligne[ligne.find('alt="'):ligne.find('"', ligne.find('alt="')+5)+1], 'alt="Image 7"')
                        elif 'Image 8"' in ligne:
                            ligne = ligne.replace(ligne[ligne.find('alt="'):ligne.find('"', ligne.find('alt="')+5)+1], 'alt="Image 8"')
                        corrections += 1
                
                # Pour les thumbnails
                elif 'alt="Thumbnail' in ligne:
                    # Garder les thumbnails comme ils sont (déjà simples)
                    pass
                
                nouvelles_lignes.append(ligne)
            
            # Réécrire le fichier
            contenu_corrige = '\n'.join(nouvelles_lignes)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(contenu_corrige)
            
            if corrections > 0:
                print(f"  ✅ Alt text corrigés: {corrections} images")
            
        except Exception as e:
            print(f"  ❌ Erreur alt text: {e}")
    
    def executer_correction_test(self):
        """Test de correction sur quelques pages"""
        print("🧪 TEST CORRECTION GALERIES - 5 PAGES")
        print("=" * 50)
        
        for file_path in self.pages_villa:
            nom_fichier = os.path.basename(file_path)
            print(f"\n🔧 CORRECTION: {nom_fichier}")
            
            # 1. Corriger le JavaScript
            self.corriger_javascript_seulement(file_path)
            
            # 2. Corriger les alt text
            self.corriger_alt_text_images(file_path)
        
        print(f"\n✅ TEST TERMINÉ SUR {len(self.pages_villa)} PAGES")
        print("\n🎯 CORRECTIONS APPLIQUÉES:")
        print("  ✅ Loop Swiper désactivé (évite décalage)")
        print("  ✅ Synchronisation thumbnails améliorée")
        print("  ✅ Alt text simplifiés (sans infos catalogue)")
        print("  ✅ Console logs ajoutés pour debugging")

if __name__ == "__main__":
    correcteur = CorrectionGalerieSimple()
    correcteur.executer_correction_test()