#!/usr/bin/env python3
"""
CORRECTIONS MANUELLES CIBLÉES - VILLA F3 PETIT MACABOU
Application des corrections identifiées par le diagnostic
"""

import os
import re
from datetime import datetime

class CorrectionsManuellesCiblees:
    def __init__(self):
        self.page_test = '/app/villa-villa-f3-sur-petit-macabou.html'
        self.corrections_appliquees = []
        
    def appliquer_correction_priorite1_video(self):
        """PRIORITÉ 1: Remplacer la vidéo Cloudinary par une alternative fonctionnelle"""
        print("🔥 PRIORITÉ 1: CORRECTION VIDÉO BACKGROUND")
        
        try:
            with open(self.page_test, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # Remplacer la vidéo Cloudinary problématique par une alternative
            video_alternative = """
            <!-- Alternative fonctionnelle: Gradient animé + image background -->
            <div class="video-fallback" style="
                position: absolute; 
                top: 0; 
                left: 0; 
                width: 100%; 
                height: 100%; 
                background: 
                    linear-gradient(45deg, rgba(59, 130, 246, 0.3) 0%, rgba(147, 51, 234, 0.3) 50%, rgba(236, 72, 153, 0.3) 100%),
                    linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%),
                    url('https://images.unsplash.com/photo-1520637736862-4d197d17c80a?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80') center/cover;
                animation: backgroundAnimation 20s ease-in-out infinite;
                z-index: -2;
            "></div>
            <style>
                @keyframes backgroundAnimation {
                    0%, 100% { 
                        background-position: 0% 50%;
                        filter: brightness(0.7) contrast(1.1) saturate(1.2);
                    }
                    50% { 
                        background-position: 100% 50%;
                        filter: brightness(0.8) contrast(1.2) saturate(1.3);
                    }
                }
            </style>
            """
            
            # Remplacer la section vidéo complète
            video_pattern = r'<div class="video-background">.*?</div>'
            contenu = re.sub(video_pattern, video_alternative, contenu, flags=re.DOTALL)
            
            # Sauvegarder
            with open(self.page_test, 'w', encoding='utf-8') as f:
                f.write(contenu)
                
            print("✅ Vidéo Cloudinary remplacée par background animé fonctionnel")
            self.corrections_appliquees.append("Vidéo background: Cloudinary → Gradient animé + image")
            
        except Exception as e:
            print(f"❌ Erreur correction vidéo: {e}")
    
    def appliquer_correction_priorite2_hamburger(self):
        """PRIORITÉ 2: Ajouter le HTML hamburger dans le DOM"""
        print("📱 PRIORITÉ 2: CORRECTION MENU HAMBURGER")
        
        try:
            with open(self.page_test, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # HTML du menu hamburger à injecter
            hamburger_html = '''
            <!-- Menu Hamburger Mobile (injection ciblée) -->
            <div class="hamburger" style="position: fixed; top: 20px; right: 20px; z-index: 9999; display: none;">
                <span></span>
                <span></span>
                <span></span>
            </div>
            
            <!-- Menu Mobile -->
            <div class="mobile-menu" style="display: none; position: fixed; top: 70px; left: 0; right: 0; z-index: 9998;">
                <a href="/index.html">🏠 Accueil</a>
                <a href="/reservation.html?villa=villa-f3-sur-petit-macabou">📅 Réserver</a>
                <a href="/prestataires.html">🛎️ Prestataires</a>
                <a href="/billetterie.html">🎟️ Billetterie</a>
                <a href="/login.html">👤 Connexion</a>
            </div>
            '''
            
            # Injecter après la balise <body>
            contenu = contenu.replace('<body', hamburger_html + '\n<body', 1)
            
            # Améliorer le CSS hamburger pour forcer l'affichage
            css_amelioration = """
            
            /* CORRECTION HAMBURGER - Affichage forcé */
            @media (max-width: 768px) {
                .hamburger {
                    display: flex !important;
                    visibility: visible !important;
                    opacity: 1 !important;
                    background: rgba(0, 0, 0, 0.8) !important;
                    padding: 10px !important;
                    border-radius: 8px !important;
                }
                
                .mobile-menu.active {
                    display: block !important;
                    visibility: visible !important;
                    opacity: 1 !important;
                    background: rgba(15, 25, 50, 0.95) !important;
                    backdrop-filter: blur(20px) !important;
                    padding: 20px !important;
                }
                
                /* Cacher navigation desktop sur mobile */
                nav .flex.space-x-6 {
                    display: none !important;
                }
            }
            """
            
            # Injecter le CSS amélioré
            contenu = contenu.replace('</style>', css_amelioration + '</style>')
            
            # JavaScript amélioré pour le hamburger
            js_amelioration = """
            
            // CORRECTION HAMBURGER - JavaScript renforcé
            document.addEventListener('DOMContentLoaded', function() {
                console.log('🔧 Correction hamburger initialisée');
                
                const hamburger = document.querySelector('.hamburger');
                const mobileMenu = document.querySelector('.mobile-menu');
                
                if (hamburger && mobileMenu) {
                    console.log('✅ Éléments hamburger trouvés');
                    
                    hamburger.addEventListener('click', function(e) {
                        e.preventDefault();
                        e.stopPropagation();
                        
                        console.log('🔄 Toggle menu mobile');
                        mobileMenu.classList.toggle('active');
                        
                        // Animation des barres
                        const spans = hamburger.querySelectorAll('span');
                        if (mobileMenu.classList.contains('active')) {
                            spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                            spans[1].style.opacity = '0';
                            spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
                        } else {
                            spans.forEach(span => {
                                span.style.transform = 'none';
                                span.style.opacity = '1';
                            });
                        }
                    });
                    
                    // Fermer au clic sur un lien
                    mobileMenu.querySelectorAll('a').forEach(link => {
                        link.addEventListener('click', function() {
                            mobileMenu.classList.remove('active');
                            hamburger.querySelectorAll('span').forEach(span => {
                                span.style.transform = 'none';
                                span.style.opacity = '1';
                            });
                        });
                    });
                } else {
                    console.error('❌ Éléments hamburger non trouvés');
                }
            });
            """
            
            # Injecter le JavaScript avant </body>
            contenu = contenu.replace('</body>', f'<script>{js_amelioration}</script></body>')
            
            # Sauvegarder
            with open(self.page_test, 'w', encoding='utf-8') as f:
                f.write(contenu)
                
            print("✅ Menu hamburger HTML ajouté dans le DOM")
            print("✅ CSS hamburger amélioré avec affichage forcé")
            print("✅ JavaScript hamburger renforcé")
            self.corrections_appliquees.append("Menu hamburger: HTML + CSS + JS ajoutés et renforcés")
            
        except Exception as e:
            print(f"❌ Erreur correction hamburger: {e}")
    
    def correction_bonus_elements_caches(self):
        """BONUS: Corriger les éléments cachés avec display:none"""
        print("🎨 BONUS: CORRECTION ÉLÉMENTS CACHÉS")
        
        try:
            with open(self.page_test, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # Ajouter CSS pour forcer l'affichage des éléments principaux
            css_affichage_force = """
            
            /* CORRECTION AFFICHAGE - Forcer la visibilité */
            main, .container, section, .villa-title, .info-card, .gallery-container {
                display: block !important;
                visibility: visible !important;
                opacity: 1 !important;
            }
            
            /* Assurer que le contenu principal est au-dessus */
            main {
                position: relative !important;
                z-index: 100 !important;
            }
            
            /* S'assurer que les cards glassmorphism sont visibles */
            .info-card {
                background: rgba(255, 255, 255, 0.1) !important;
                backdrop-filter: blur(20px) !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
                border-radius: 20px !important;
                padding: 20px !important;
                margin: 20px 0 !important;
            }
            """
            
            # Injecter le CSS
            contenu = contenu.replace('</style>', css_affichage_force + '</style>')
            
            # Sauvegarder
            with open(self.page_test, 'w', encoding='utf-8') as f:
                f.write(contenu)
                
            print("✅ CSS affichage forcé ajouté")
            self.corrections_appliquees.append("Affichage: CSS forcé pour la visibilité des éléments")
            
        except Exception as e:
            print(f"❌ Erreur correction affichage: {e}")
    
    def executer_corrections_completes(self):
        """Exécute toutes les corrections dans l'ordre de priorité"""
        print("🎯 DÉMARRAGE CORRECTIONS MANUELLES CIBLÉES")
        print("=" * 60)
        print(f"📄 Page cible: {self.page_test}")
        print()
        
        # Créer une sauvegarde avant corrections
        backup_file = f"{self.page_test}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.system(f"cp '{self.page_test}' '{backup_file}'")
        print(f"💾 Sauvegarde créée: {backup_file}")
        print()
        
        # Appliquer les corrections par priorité
        self.appliquer_correction_priorite1_video()
        print()
        
        self.appliquer_correction_priorite2_hamburger()
        print()
        
        self.correction_bonus_elements_caches()
        print()
        
        # Rapport final
        print("=" * 60)
        print("✅ CORRECTIONS MANUELLES TERMINÉES!")
        print(f"📊 Total corrections appliquées: {len(self.corrections_appliquees)}")
        print()
        
        if self.corrections_appliquees:
            print("🔧 CORRECTIONS APPLIQUÉES:")
            for i, correction in enumerate(self.corrections_appliquees, 1):
                print(f"  {i}. {correction}")
        
        print()
        print("🎯 PRÊT POUR TEST DE VALIDATION")
        print("=" * 60)

if __name__ == "__main__":
    corrections = CorrectionsManuellesCiblees()
    corrections.executer_corrections_completes()