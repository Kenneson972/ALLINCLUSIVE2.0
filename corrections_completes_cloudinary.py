#!/usr/bin/env python3
"""
CORRECTIONS COMPLÈTES AVEC VIDÉO CLOUDINARY
Application de TOUTES les corrections identifiées
"""

import os
import re
from datetime import datetime

class CorrectionsCompletesCloudinary:
    def __init__(self):
        self.page_test = '/app/villa-villa-f3-sur-petit-macabou.html'
        self.corrections_appliquees = []
    
    def correction_1_tailwind_css(self):
        """Correction 1: Tailwind CSS - remplacer script par link"""
        print("🔧 CORRECTION 1: TAILWIND CSS (SCRIPT → LINK)")
        
        try:
            with open(self.page_test, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # Remplacer script Tailwind par link correct
            pattern_script = r'<script src="https://cdn\.jsdelivr\.net/npm/tailwindcss@[^"]*"[^>]*></script>'
            link_correct = '<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">'
            
            if re.search(pattern_script, contenu):
                contenu = re.sub(pattern_script, link_correct, contenu)
                
                with open(self.page_test, 'w', encoding='utf-8') as f:
                    f.write(contenu)
                    
                print("✅ Tailwind CSS: script remplacé par link")
                self.corrections_appliquees.append("Tailwind CSS: Erreur MIME corrigée")
            else:
                print("ℹ️ Script Tailwind non trouvé (déjà corrigé)")
                
        except Exception as e:
            print(f"❌ Erreur correction Tailwind: {e}")
    
    def correction_2_hamburger_html(self):
        """Correction 2: Ajouter HTML hamburger dans le DOM"""
        print("🔧 CORRECTION 2: HAMBURGER HTML")
        
        try:
            with open(self.page_test, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # Vérifier si le hamburger HTML existe déjà
            if '<div class="hamburger">' not in contenu:
                # HTML hamburger complet
                hamburger_html = '''
                
    <!-- Menu Hamburger Mobile - Injection directe -->
    <div class="hamburger" id="mobileMenuToggle">
        <span></span>
        <span></span>
        <span></span>
    </div>
    
    <!-- Menu Mobile -->
    <div class="mobile-menu" id="mobileMenu">
        <a href="/index.html">🏠 Accueil</a>
        <a href="/reservation.html?villa=villa-f3-sur-petit-macabou">📅 Réserver cette villa</a>
        <a href="/prestataires.html">🛎️ Prestataires</a>
        <a href="/billetterie.html">🎟️ Billetterie</a>
        <a href="/login.html">👤 Connexion</a>
    </div>

'''
                
                # Injecter après <body>
                contenu = contenu.replace('<body', hamburger_html + '<body', 1)
                
                # JavaScript hamburger renforcé
                js_hamburger = '''
                
    // JavaScript Hamburger - Renforcé
    document.addEventListener('DOMContentLoaded', function() {
        console.log('🍔 Init hamburger menu');
        
        const hamburger = document.getElementById('mobileMenuToggle');
        const mobileMenu = document.getElementById('mobileMenu');
        
        if (hamburger && mobileMenu) {
            console.log('✅ Hamburger elements found');
            
            hamburger.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('🔄 Hamburger clicked');
                
                // Toggle class active
                mobileMenu.classList.toggle('active');
                hamburger.classList.toggle('active');
                
                console.log('Menu active:', mobileMenu.classList.contains('active'));
            });
            
            // Fermer menu si clic sur lien
            mobileMenu.addEventListener('click', function(e) {
                if (e.target.tagName === 'A') {
                    mobileMenu.classList.remove('active');
                    hamburger.classList.remove('active');
                }
            });
        } else {
            console.error('❌ Hamburger elements not found');
        }
    });

'''
                
                # Injecter JavaScript avant </body>
                contenu = contenu.replace('</body>', f'<script>{js_hamburger}</script></body>')
                
                with open(self.page_test, 'w', encoding='utf-8') as f:
                    f.write(contenu)
                    
                print("✅ HTML hamburger ajouté dans le DOM")
                print("✅ JavaScript hamburger renforcé avec IDs")
                self.corrections_appliquees.append("Hamburger: HTML + JS ajoutés")
            else:
                print("ℹ️ HTML hamburger déjà présent")
                
        except Exception as e:
            print(f"❌ Erreur correction hamburger: {e}")
    
    def correction_3_elements_caches(self):
        """Correction 3: Corriger éléments cachés"""
        print("🔧 CORRECTION 3: ÉLÉMENTS CACHÉS")
        
        try:
            with open(self.page_test, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # CSS pour forcer l'affichage
            css_affichage = '''
            
/* CORRECTION AFFICHAGE - Forcer visibilité */
main, section, .container, .villa-title, .info-card {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
}

/* Hamburger mobile - Forcer affichage sur mobile */
@media (max-width: 768px) {
    .hamburger {
        display: flex !important;
        position: fixed !important;
        top: 20px !important;
        right: 20px !important;
        z-index: 9999 !important;
        background: rgba(0, 0, 0, 0.8) !important;
        padding: 12px !important;
        border-radius: 8px !important;
        cursor: pointer !important;
    }
    
    .mobile-menu {
        position: fixed !important;
        top: 70px !important;
        left: 0 !important;
        right: 0 !important;
        background: rgba(15, 25, 50, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        padding: 20px !important;
        z-index: 9998 !important;
        display: none !important;
    }
    
    .mobile-menu.active {
        display: block !important;
    }
    
    .mobile-menu a {
        display: block !important;
        color: white !important;
        text-decoration: none !important;
        padding: 15px 0 !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Cacher navigation desktop sur mobile */
    nav .flex.space-x-6 {
        display: none !important;
    }
}

@media (min-width: 769px) {
    .hamburger {
        display: none !important;
    }
    
    .mobile-menu {
        display: none !important;
    }
}

'''
            
            # Injecter le CSS
            contenu = contenu.replace('</style>', css_affichage + '</style>')
            
            with open(self.page_test, 'w', encoding='utf-8') as f:
                f.write(contenu)
                
            print("✅ CSS affichage forcé ajouté")
            print("✅ Media queries hamburger améliorées")
            self.corrections_appliquees.append("Affichage: CSS forcé et media queries")
            
        except Exception as e:
            print(f"❌ Erreur correction affichage: {e}")
    
    def correction_4_breakpoints_responsive(self):
        """Correction 4: Améliorer breakpoints responsive"""
        print("🔧 CORRECTION 4: BREAKPOINTS RESPONSIVE")
        
        try:
            with open(self.page_test, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # CSS responsive complet
            css_responsive = '''
            
/* BREAKPOINTS RESPONSIVE COMPLETS */

/* Mobile Small (320px - 480px) */
@media (max-width: 480px) {
    .container {
        padding: 0 15px !important;
    }
    
    h1, .villa-title {
        font-size: 1.8rem !important;
    }
    
    .info-card {
        margin: 10px 0 !important;
        padding: 15px !important;
    }
}

/* Mobile Large (481px - 768px) */
@media (min-width: 481px) and (max-width: 768px) {
    .container {
        padding: 0 20px !important;
    }
    
    h1, .villa-title {
        font-size: 2.2rem !important;
    }
}

/* Tablet (769px - 1024px) */
@media (min-width: 769px) and (max-width: 1024px) {
    .container {
        max-width: 95% !important;
    }
    
    .info-card {
        padding: 25px !important;
    }
}

/* Desktop (1025px+) */
@media (min-width: 1025px) {
    .container {
        max-width: 1200px !important;
    }
}

'''
            
            # Injecter le CSS responsive
            contenu = contenu.replace('</style>', css_responsive + '</style>')
            
            with open(self.page_test, 'w', encoding='utf-8') as f:
                f.write(contenu)
                
            print("✅ Breakpoints responsive complets ajoutés")
            self.corrections_appliquees.append("Responsive: Breakpoints complets")
            
        except Exception as e:
            print(f"❌ Erreur correction breakpoints: {e}")
    
    def executer_toutes_corrections(self):
        """Exécute toutes les corrections"""
        print("🎯 APPLICATION DE TOUTES LES CORRECTIONS")
        print("=" * 60)
        print(f"📄 Page: {self.page_test}")
        print()
        
        # Créer sauvegarde
        backup_file = f"{self.page_test}.backup_complet_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.system(f"cp '{self.page_test}' '{backup_file}'")
        print(f"💾 Sauvegarde: {backup_file}")
        print()
        
        # Appliquer toutes les corrections
        self.correction_1_tailwind_css()
        print()
        
        self.correction_2_hamburger_html()
        print()
        
        self.correction_3_elements_caches()
        print()
        
        self.correction_4_breakpoints_responsive()
        print()
        
        # Rapport final
        print("=" * 60)
        print("✅ TOUTES LES CORRECTIONS APPLIQUÉES!")
        print(f"📊 Total: {len(self.corrections_appliquees)} corrections")
        print()
        
        if self.corrections_appliquees:
            print("🔧 CORRECTIONS RÉALISÉES:")
            for i, correction in enumerate(self.corrections_appliquees, 1):
                print(f"  {i}. {correction}")
        
        print()
        print("🎯 PRÊT POUR TEST FINAL AVEC VIDÉO CLOUDINARY")

if __name__ == "__main__":
    corrections = CorrectionsCompletesCloudinary()
    corrections.executer_toutes_corrections()