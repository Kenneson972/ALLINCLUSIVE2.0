#!/usr/bin/env python3
"""
CORRECTION APPROFONDIE DES BUGS CRITIQUES
Corrections ciblées des problèmes spécifiques détectés
"""

import os
import glob
import re
from datetime import datetime

class CorrectionApprofondie:
    def __init__(self):
        self.pages_villa = glob.glob('/app/villa-*.html')
        self.pages_villa = [f for f in self.pages_villa if 'template' not in f]
        self.corrections_effectuees = []

    def corriger_tailwind_css_erreur(self, contenu, nom_page):
        """Corrige l'erreur Tailwind CSS - remplacer script par link"""
        corrections = 0
        
        # Remplacer le script incorrect par un link correct
        pattern_incorrect = r'<script src="https://cdn\.jsdelivr\.net/npm/tailwindcss@[^"]*"[^>]*></script>'
        if re.search(pattern_incorrect, contenu):
            contenu = re.sub(
                pattern_incorrect,
                '<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">',
                contenu
            )
            corrections += 1
            self.corrections_effectuees.append(f"{nom_page}: Tailwind CSS corrigé (script→link)")
        
        return contenu, corrections

    def corriger_video_cloudinary_alternative(self, contenu, nom_page):
        """Utilise une vidéo background alternative fonctionnelle"""
        corrections = 0
        
        # URLs Cloudinary alternatives
        video_alternatives = [
            "https://res.cloudinary.com/demo/video/upload/v1690876735/background-villa.mp4",
            "https://cdn.pixabay.com/vimeo/540634326/beach-106157.mp4?api_key=default"
        ]
        
        # Remplacer par une URL alternative ou fallback
        cloudinary_pattern = r'<source src="https://res\.cloudinary\.com/[^"]*" type="video/mp4">'
        if re.search(cloudinary_pattern, contenu):
            # Remplacer par un fallback local ou une image statique en cas d'échec
            fallback_html = '''
            <source src="https://cdn.pixabay.com/vimeo/540634326/beach-106157.mp4?api_key=default" type="video/mp4">
            <!-- Fallback image si vidéo échoue -->
            <div class="video-fallback" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; 
                 background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%), 
                 url('https://images.unsplash.com/photo-1520637836862-4d197d17c80a?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80') center/cover; 
                 z-index: -1;"></div>
            '''
            
            contenu = re.sub(cloudinary_pattern, fallback_html, contenu, count=1)
            corrections += 1
            self.corrections_effectuees.append(f"{nom_page}: Vidéo background avec fallback ajoutée")
        
        return contenu, corrections

    def corriger_injection_hamburger(self, contenu, nom_page):
        """Corrige l'injection du menu hamburger qui n'a pas fonctionné"""
        corrections = 0
        
        # Vérifier si le hamburger HTML existe réellement dans le body
        if '.hamburger {' in contenu and 'hamburger span' in contenu:
            # Le CSS est présent, vérifier le HTML
            if '<div class="hamburger">' not in contenu:
                # Le HTML n'a pas été injecté correctement, le faire manuellement
                
                # Trouver un endroit approprié dans le header pour injecter
                header_patterns = [
                    r'(<nav[^>]*>.*?</nav>)',
                    r'(<header[^>]*>.*?</header>)',
                    r'(<div[^>]*class="[^"]*header[^>]*>)',
                    r'(<h1[^>]*>.*?KhanelConcept.*?</h1>)'
                ]
                
                hamburger_html = '''
                <!-- Menu Hamburger Mobile -->
                <div class="hamburger">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
                
                <!-- Menu Mobile -->
                <div class="mobile-menu">
                    <a href="/index.html">🏠 Accueil</a>
                    <a href="/reservation.html">📅 Réserver</a>
                    <a href="/prestataires.html">🛎️ Prestataires</a>
                    <a href="/billetterie.html">🎟️ Billetterie</a>
                    <a href="/mobilier.html">🪑 Mobilier</a>
                    <a href="/excursions.html">🚤 Excursions</a>
                    <a href="/login.html">👤 Connexion</a>
                </div>
                '''
                
                # Essayer d'injecter après le titre ou logo
                for pattern in header_patterns:
                    if re.search(pattern, contenu, re.DOTALL):
                        contenu = re.sub(pattern, r'\1' + hamburger_html, contenu, count=1)
                        corrections += 1
                        self.corrections_effectuees.append(f"{nom_page}: HTML hamburger injecté manuellement")
                        break
                
                # Si aucun pattern trouvé, injecter après <body>
                if corrections == 0:
                    contenu = contenu.replace('<body>', '<body>' + hamburger_html, 1)
                    corrections += 1
                    self.corrections_effectuees.append(f"{nom_page}: HTML hamburger injecté après <body>")
        
        return contenu, corrections

    def ajouter_css_responsive_fix(self, contenu, nom_page):
        """Ajoute des fixes CSS pour améliorer le responsive"""
        corrections = 0
        
        responsive_css = """
        
        /* FIXES RESPONSIVE CRITIQUES */
        @media (max-width: 768px) {
            body {
                font-size: 14px;
            }
            
            .villa-title, h1 {
                font-size: 2rem !important;
                text-align: center;
            }
            
            .info-card {
                margin: 10px !important;
                padding: 15px !important;
            }
            
            .swiper {
                height: 300px !important;
            }
            
            /* Force affichage du hamburger */
            .hamburger {
                display: flex !important;
                position: fixed !important;
                top: 20px !important;
                right: 20px !important;
                z-index: 9999 !important;
                background: rgba(0, 0, 0, 0.7) !important;
                border-radius: 8px !important;
                padding: 10px !important;
            }
            
            /* Cache navigation desktop */
            .desktop-nav, nav:not(.mobile-menu) {
                display: none !important;
            }
        }
        
        /* Force visibilité éléments */
        .mobile-menu, .hamburger {
            visibility: visible !important;
            opacity: 1 !important;
        }
        """
        
        # Injecter avant </style>
        if '</style>' in contenu:
            contenu = contenu.replace('</style>', responsive_css + '</style>')
            corrections += 1
            self.corrections_effectuees.append(f"{nom_page}: CSS responsive fixes ajoutés")
        
        return contenu, corrections

    def corriger_page_approfondie(self, file_path):
        """Applique les corrections approfondies à une page"""
        nom_page = os.path.basename(file_path)
        print(f"🔧 Correction approfondie: {nom_page}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            contenu_original = contenu
            total_corrections = 0
            
            # Corrections spécifiques
            contenu, corrections = self.corriger_tailwind_css_erreur(contenu, nom_page)
            total_corrections += corrections
            
            contenu, corrections = self.corriger_video_cloudinary_alternative(contenu, nom_page)
            total_corrections += corrections
            
            contenu, corrections = self.corriger_injection_hamburger(contenu, nom_page)
            total_corrections += corrections
            
            contenu, corrections = self.ajouter_css_responsive_fix(contenu, nom_page)
            total_corrections += corrections
            
            # Sauvegarder
            if contenu != contenu_original:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(contenu)
                print(f"✅ {nom_page}: {total_corrections} corrections approfondies")
            else:
                print(f"ℹ️ {nom_page}: Aucune correction nécessaire")
                
        except Exception as e:
            print(f"❌ Erreur: {nom_page}: {e}")

    def executer_corrections_approfondies(self):
        """Exécute les corrections approfondies"""
        print("🔥 DÉMARRAGE CORRECTIONS APPROFONDIES")
        print("=" * 50)
        
        for file_path in self.pages_villa[:5]:  # Test sur 5 pages d'abord
            self.corriger_page_approfondie(file_path)
        
        print("\n" + "=" * 50)
        print("✅ CORRECTIONS APPROFONDIES TERMINÉES!")
        print(f"📊 Total corrections: {len(self.corrections_effectuees)}")

if __name__ == "__main__":
    correcteur = CorrectionApprofondie()
    correcteur.executer_corrections_approfondies()