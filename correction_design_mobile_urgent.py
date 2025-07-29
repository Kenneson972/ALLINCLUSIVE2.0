#!/usr/bin/env python3
"""
CORRECTION URGENTE DESIGN MOBILE VILLA - REFONTE COMPLÈTE
Correction de l'interface mobile "dégueulasse" identifiée par l'utilisateur
"""

import os
import glob
import re
from datetime import datetime

class CorrectionDesignMobileUrgent:
    def __init__(self):
        self.pages_villa = glob.glob('/app/villa-*.html')
        self.pages_villa = [f for f in self.pages_villa if 'template' not in f and 'backup' not in f]
        
    def corriger_design_mobile_page(self, file_path):
        """Correction urgente du design mobile catastrophique"""
        nom_page = os.path.basename(file_path)
        print(f"🚨 CORRECTION URGENTE MOBILE: {nom_page}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            contenu_original = contenu
            
            # CSS MOBILE COMPLÈTEMENT REFAIT
            css_mobile_propre = '''

/* =====================================================
   CORRECTION URGENTE DESIGN MOBILE - INTERFACE PROPRE
   ===================================================== */

@media (max-width: 768px) {
    /* Reset mobile complet */
    * {
        box-sizing: border-box;
    }
    
    body {
        margin: 0 !important;
        padding: 0 !important;
        overflow-x: hidden !important;
        font-size: 14px !important;
        line-height: 1.4 !important;
    }
    
    /* LOGO KHANEL - Taille réduite mobile */
    .logo, h1[onclick*="showSection"] {
        font-size: 1.5rem !important;
        margin: 10px 0 !important;
        padding: 5px !important;
        text-align: center !important;
        background: rgba(0, 0, 0, 0.7) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 10px !important;
        max-width: 200px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    
    /* TITRE VILLA - Clean et lisible */
    .villa-title, main h1, main h2 {
        font-size: 1.4rem !important;
        color: white !important;
        text-align: center !important;
        margin: 15px 10px !important;
        padding: 10px !important;
        background: rgba(0, 0, 0, 0.6) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 12px !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8) !important;
        font-weight: 600 !important;
        line-height: 1.3 !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    /* CONTENEUR PRINCIPAL MOBILE */
    main {
        padding: 10px !important;
        margin: 0 !important;
        position: relative !important;
        z-index: 10 !important;
        min-height: 100vh !important;
    }
    
    /* CARDS INFO - Design propre mobile */
    .info-card {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 15px !important;
        padding: 15px !important;
        margin: 10px 5px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
        color: #333 !important;
        font-size: 13px !important;
        line-height: 1.5 !important;
    }
    
    .info-card h3 {
        font-size: 1.1rem !important;
        margin: 0 0 8px 0 !important;
        color: #2563eb !important;
        font-weight: 600 !important;
    }
    
    .info-card p, .info-card li {
        margin: 5px 0 !important;
        font-size: 13px !important;
        color: #444 !important;
    }
    
    /* GALERIE MOBILE - Refonte complète */
    .swiper, .gallery-container {
        background: rgba(0, 0, 0, 0.8) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 15px !important;
        padding: 15px !important;
        margin: 15px 5px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.4) !important;
        height: auto !important;
        min-height: 200px !important;
    }
    
    .swiper-wrapper {
        height: 200px !important;
    }
    
    .swiper-slide {
        height: 200px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    .swiper-slide img {
        width: 100% !important;
        height: 200px !important;
        object-fit: cover !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5) !important;
    }
    
    /* Navigation Swiper mobile */
    .swiper-button-next, .swiper-button-prev {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 50% !important;
        width: 35px !important;
        height: 35px !important;
        margin-top: -17px !important;
    }
    
    .swiper-button-next:after, .swiper-button-prev:after {
        font-size: 14px !important;
        color: #333 !important;
        font-weight: bold !important;
    }
    
    .swiper-pagination {
        bottom: -35px !important;
    }
    
    .swiper-pagination-bullet {
        background: rgba(255, 255, 255, 0.7) !important;
        opacity: 1 !important;
    }
    
    .swiper-pagination-bullet-active {
        background: #3b82f6 !important;
    }
    
    /* BOUTONS MOBILE - Clean */
    .btn, .reservation-btn, button {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 20px !important;
        font-size: 14px !important;
        margin: 10px 5px !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
        text-decoration: none !important;
        display: inline-block !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
        font-weight: 600 !important;
    }
    
    .btn:hover, .reservation-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* MENU HAMBURGER - Position fixe propre */
    .hamburger {
        position: fixed !important;
        top: 15px !important;
        right: 15px !important;
        z-index: 9999 !important;
        background: rgba(0, 0, 0, 0.9) !important;
        backdrop-filter: blur(15px) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
        padding: 10px !important;
        width: 45px !important;
        height: 45px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        cursor: pointer !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5) !important;
    }
    
    .hamburger span {
        display: block !important;
        width: 20px !important;
        height: 2px !important;
        background: white !important;
        margin: 2px 0 !important;
        border-radius: 1px !important;
        transition: all 0.3s ease !important;
    }
    
    /* MENU MOBILE - Overlay propre */
    .mobile-menu {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        background: rgba(15, 25, 50, 0.98) !important;
        backdrop-filter: blur(25px) !important;
        padding: 80px 20px 20px !important;
        z-index: 9998 !important;
        display: none !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .mobile-menu.active {
        display: block !important;
    }
    
    .mobile-menu a {
        display: block !important;
        color: white !important;
        text-decoration: none !important;
        padding: 15px 0 !important;
        font-size: 18px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
        transition: all 0.3s ease !important;
        text-align: left !important;
    }
    
    .mobile-menu a:hover {
        color: #3b82f6 !important;
        padding-left: 15px !important;
        background: rgba(59, 130, 246, 0.1) !important;
        border-radius: 8px !important;
    }
    
    /* SPACING MOBILE GÉNÉRAL */
    section {
        margin: 15px 0 !important;
        padding: 0 5px !important;
    }
    
    /* RESPONSIVE IMAGES */
    img {
        max-width: 100% !important;
        height: auto !important;
    }
    
    /* TEXTE LISIBLE */
    p, li, span {
        font-size: 13px !important;
        line-height: 1.5 !important;
        margin: 8px 0 !important;
    }
}

/* Tablet adjustments */
@media (min-width: 481px) and (max-width: 768px) {
    .villa-title, main h1 {
        font-size: 1.6rem !important;
    }
    
    .info-card {
        padding: 20px !important;
        margin: 15px 10px !important;
    }
    
    .swiper-slide img {
        height: 250px !important;
    }
}

'''
            
            # Injecter le nouveau CSS mobile
            if '</style>' in contenu:
                # Remplacer l'ancien CSS mobile s'il existe
                if 'CORRECTION URGENTE DESIGN MOBILE' in contenu:
                    # Remplacer l'ancien
                    pattern = r'/\* ={50,}\s*CORRECTION URGENTE DESIGN MOBILE.*?\*/'
                    contenu = re.sub(pattern, '', contenu, flags=re.DOTALL)
                
                contenu = contenu.replace('</style>', css_mobile_propre + '</style>')
                print("  ✅ CSS mobile propre injecté")
            
            # JavaScript pour optimiser l'affichage mobile
            js_mobile_propre = '''

// JavaScript Mobile Optimisé - Interface Propre
document.addEventListener('DOMContentLoaded', function() {
    console.log('📱 Optimisation mobile interface propre');
    
    // Détecter mobile
    if (window.innerWidth <= 768) {
        console.log('📱 Mode mobile - Optimisations appliquées');
        
        // Optimiser le logo
        const logo = document.querySelector('.logo, h1[onclick]');
        if (logo) {
            logo.style.fontSize = '1.5rem';
            logo.style.padding = '5px';
            logo.style.margin = '10px auto';
            logo.style.maxWidth = '200px';
            logo.style.textAlign = 'center';
        }
        
        // Optimiser le titre villa
        const villaTitle = document.querySelector('.villa-title, main h1, main h2');
        if (villaTitle) {
            villaTitle.style.fontSize = '1.4rem';
            villaTitle.style.margin = '15px 10px';
            villaTitle.style.padding = '10px';
            villaTitle.style.textAlign = 'center';
        }
        
        // Réinitialiser Swiper pour mobile si existe
        if (typeof Swiper !== 'undefined') {
            setTimeout(() => {
                const swiperContainer = document.querySelector('.swiper');
                if (swiperContainer) {
                    console.log('🔄 Réinitialisation Swiper mobile');
                    
                    // Nouvelle config mobile optimisée
                    const swiper = new Swiper('.swiper', {
                        slidesPerView: 1,
                        spaceBetween: 10,
                        loop: false,
                        autoplay: {
                            delay: 3000,
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
                        on: {
                            init: function() {
                                console.log('✅ Swiper mobile optimisé initialisé');
                            }
                        }
                    });
                }
            }, 1000);
        }
        
        // Menu hamburger optimisé
        const hamburger = document.querySelector('.hamburger, #mobileMenuToggle');
        const mobileMenu = document.querySelector('.mobile-menu, #mobileMenu');
        
        if (hamburger && mobileMenu) {
            console.log('✅ Menu mobile optimisé activé');
            
            hamburger.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                mobileMenu.classList.toggle('active');
                hamburger.classList.toggle('active');
                
                console.log('🔄 Menu toggle:', mobileMenu.classList.contains('active'));
            });
            
            // Fermer menu sur clic extérieur
            document.addEventListener('click', function(e) {
                if (!hamburger.contains(e.target) && !mobileMenu.contains(e.target)) {
                    mobileMenu.classList.remove('active');
                    hamburger.classList.remove('active');
                }
            });
        }
        
        // Lazy loading optimisé
        const images = document.querySelectorAll('img');
        images.forEach(img => {
            img.loading = 'lazy';
            img.style.transition = 'opacity 0.3s ease';
        });
        
        // Smooth scroll
        document.documentElement.style.scrollBehavior = 'smooth';
    }
});

'''
            
            # Injecter le JavaScript mobile
            if 'Interface Propre' not in contenu:
                contenu = contenu.replace('</body>', f'<script>{js_mobile_propre}</script></body>')
                print("  ✅ JavaScript mobile propre ajouté")
            
            # Sauvegarder
            if contenu != contenu_original:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(contenu)
                print("  ✅ Design mobile corrigé!")
            else:
                print("  ℹ️ Déjà optimisé")
                
        except Exception as e:
            print(f"  ❌ Erreur: {e}")
    
    def executer_correction_urgente(self):
        """Correction urgente du design mobile sur toutes les pages"""
        print("🚨 CORRECTION URGENTE DESIGN MOBILE - TOUTES LES PAGES VILLA")
        print("=" * 70)
        print("📱 Correction de l'interface mobile 'dégueulasse'")
        print(f"🔧 {len(self.pages_villa)} pages à corriger")
        print()
        
        for file_path in self.pages_villa:
            self.corriger_design_mobile_page(file_path)
        
        print("\n" + "=" * 70)
        print("✅ CORRECTION URGENTE MOBILE TERMINÉE!")
        
        print("\n🎯 CORRECTIONS APPLIQUÉES:")
        print("  1. ✅ Logo KHANEL redimensionné (1.5rem)")
        print("  2. ✅ Titre villa repositionné et lisible")
        print("  3. ✅ Galerie photos réorganisée (200px height)")
        print("  4. ✅ Cards info avec background blanc lisible")
        print("  5. ✅ Menu hamburger repositionné proprement")
        print("  6. ✅ Buttons et interactions optimisées")
        print("  7. ✅ Responsive breakpoints ajustés")
        
        print("\n📱 L'INTERFACE MOBILE DEVRAIT MAINTENANT ÊTRE PROPRE!")

if __name__ == "__main__":
    correcteur = CorrectionDesignMobileUrgent()
    correcteur.executer_correction_urgente()