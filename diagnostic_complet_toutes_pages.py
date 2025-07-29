#!/usr/bin/env python3
"""
DIAGNOSTIC ET CORRECTIONS SUR TOUTES LES 21 PAGES VILLA
Extension du diagnostic approfondi à toutes les pages
"""

import os
import glob
import re
import requests
from datetime import datetime

class DiagnosticCompletToutesPages:
    def __init__(self):
        self.pages_villa = glob.glob('/app/villa-*.html')
        self.pages_villa = [f for f in self.pages_villa if 'template' not in f and 'backup' not in f]
        self.rapport_global = {}
        self.corrections_par_page = {}
        
    def diagnostiquer_page_villa(self, file_path):
        """Diagnostic complet d'une page villa spécifique"""
        nom_page = os.path.basename(file_path)
        print(f"🔍 DIAGNOSTIC: {nom_page}")
        
        problemes = []
        corrections_necessaires = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # 1. Vidéo Cloudinary
            if 'cloudinary.com' in contenu:
                if 'dld9eojbt' in contenu:
                    print("  🎥 Vidéo Cloudinary URL problématique détectée")
                    problemes.append("Vidéo Cloudinary URL incorrecte")
                    corrections_necessaires.append("corriger_video_cloudinary")
                elif 'ddulasmtz' in contenu:
                    print("  ✅ Vidéo Cloudinary URL correcte")
                else:
                    print("  ⚠️ URL Cloudinary non reconnue")
            else:
                print("  ❌ Pas de vidéo Cloudinary")
                problemes.append("Vidéo Cloudinary manquante")
                corrections_necessaires.append("ajouter_video_cloudinary")
            
            # 2. Tailwind CSS
            if 'script.*tailwindcss' in contenu and 'link.*tailwindcss' not in contenu:
                print("  ❌ Tailwind CSS en script (erreur MIME)")
                problemes.append("Tailwind CSS erreur MIME")
                corrections_necessaires.append("corriger_tailwind_css")
            elif 'tailwindcss' in contenu:
                print("  ✅ Tailwind CSS OK")
            else:
                print("  ❌ Tailwind CSS manquant")
                problemes.append("Tailwind CSS manquant")
                corrections_necessaires.append("ajouter_tailwind_css")
            
            # 3. Menu Hamburger
            hamburger_css = '.hamburger {' in contenu
            hamburger_html = '<div class="hamburger">' in contenu or '<div class="hamburger"' in contenu
            hamburger_js = 'hamburger.addEventListener' in contenu or 'mobileMenuToggle' in contenu
            
            if hamburger_css and hamburger_html and hamburger_js:
                print("  ✅ Menu hamburger complet")
            elif hamburger_css and not hamburger_html:
                print("  ⚠️ CSS hamburger présent, HTML manquant")
                problemes.append("Hamburger HTML manquant")
                corrections_necessaires.append("ajouter_hamburger_html")
            elif not hamburger_css:
                print("  ❌ Menu hamburger complètement manquant")
                problemes.append("Menu hamburger manquant")
                corrections_necessaires.append("ajouter_hamburger_complet")
            
            # 4. Éléments cachés
            elements_caches = len(re.findall(r'display:\s*none', contenu))
            if elements_caches > 0:
                print(f"  ⚠️ {elements_caches} éléments avec display:none")
                problemes.append(f"{elements_caches} éléments cachés")
                corrections_necessaires.append("corriger_elements_caches")
            else:
                print("  ✅ Pas d'éléments cachés détectés")
            
            # 5. Media queries responsive
            media_queries = len(re.findall(r'@media', contenu))
            if media_queries < 2:
                print(f"  ❌ Seulement {media_queries} media queries")
                problemes.append("Media queries insuffisantes")
                corrections_necessaires.append("ajouter_breakpoints_responsive")
            else:
                print(f"  ✅ {media_queries} media queries détectées")
            
            # 6. Navigation réservation
            villa_id = nom_page.replace('villa-', '').replace('.html', '')
            if f'reservation.html?villa={villa_id}' in contenu:
                print("  ✅ Navigation réservation avec paramètres")
            elif 'reservation.html' in contenu:
                print("  ⚠️ Navigation réservation sans paramètres")
                problemes.append("Navigation réservation incomplète")
                corrections_necessaires.append("corriger_navigation_reservation")
            else:
                print("  ❌ Pas de navigation réservation")
                problemes.append("Navigation réservation manquante")
                corrections_necessaires.append("ajouter_navigation_reservation")
            
            # Enregistrer les résultats
            self.rapport_global[nom_page] = {
                'problemes': problemes,
                'corrections_necessaires': corrections_necessaires,
                'score': max(0, 100 - (len(problemes) * 15))
            }
            
            print(f"  📊 Score: {self.rapport_global[nom_page]['score']}/100")
            print()
            
        except Exception as e:
            print(f"  ❌ Erreur diagnostic: {e}")
            self.rapport_global[nom_page] = {
                'problemes': [f"Erreur lecture: {e}"],
                'corrections_necessaires': [],
                'score': 0
            }
    
    def appliquer_corrections_page(self, file_path):
        """Applique les corrections nécessaires à une page"""
        nom_page = os.path.basename(file_path)
        corrections_necessaires = self.rapport_global[nom_page]['corrections_necessaires']
        
        if not corrections_necessaires:
            print(f"ℹ️ {nom_page}: Aucune correction nécessaire")
            return
        
        print(f"🔧 CORRECTIONS: {nom_page}")
        corrections_appliquees = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            contenu_original = contenu
            
            # Appliquer chaque correction nécessaire
            for correction in corrections_necessaires:
                if correction == "corriger_video_cloudinary":
                    # URL correcte de la vidéo Cloudinary
                    url_correcte = "https://res.cloudinary.com/ddulasmtz/video/upload/v1752950782/background-video.mp4_qoofsz.mp4"
                    url_incorrecte = "https://res.cloudinary.com/dld9eojbt/video/upload/q_auto,f_mp4/v1716830959/villa-background-video_hqhq2s.mp4"
                    
                    if url_incorrecte in contenu:
                        contenu = contenu.replace(url_incorrecte, url_correcte)
                        corrections_appliquees.append("Vidéo Cloudinary URL corrigée")
                
                elif correction == "corriger_tailwind_css":
                    # Remplacer script Tailwind par link
                    pattern_script = r'<script src="https://cdn\.jsdelivr\.net/npm/tailwindcss@[^"]*"[^>]*></script>'
                    link_correct = '<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">'
                    
                    if re.search(pattern_script, contenu):
                        contenu = re.sub(pattern_script, link_correct, contenu)
                        corrections_appliquees.append("Tailwind CSS script→link")
                
                elif correction == "ajouter_hamburger_html":
                    # Ajouter HTML hamburger si manquant
                    if '<div class="hamburger">' not in contenu:
                        villa_id = nom_page.replace('villa-', '').replace('.html', '')
                        hamburger_html = f'''
    <!-- Menu Hamburger Mobile -->
    <div class="hamburger" id="mobileMenuToggle">
        <span></span>
        <span></span>
        <span></span>
    </div>
    
    <!-- Menu Mobile -->
    <div class="mobile-menu" id="mobileMenu">
        <a href="/index.html">🏠 Accueil</a>
        <a href="/reservation.html?villa={villa_id}">📅 Réserver cette villa</a>
        <a href="/prestataires.html">🛎️ Prestataires</a>
        <a href="/billetterie.html">🎟️ Billetterie</a>
        <a href="/login.html">👤 Connexion</a>
    </div>

'''
                        contenu = contenu.replace('<body', hamburger_html + '<body', 1)
                        corrections_appliquees.append("HTML hamburger ajouté")
                
                elif correction == "corriger_elements_caches":
                    # CSS pour forcer l'affichage
                    css_affichage = '''

/* CORRECTION AFFICHAGE - Forcer visibilité */
main, section, .container, .villa-title, .info-card {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
}

/* Hamburger mobile responsive */
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
    
    nav .flex.space-x-6 {
        display: none !important;
    }
}

'''
                    if '</style>' in contenu:
                        contenu = contenu.replace('</style>', css_affichage + '</style>')
                        corrections_appliquees.append("CSS affichage forcé")
                
                elif correction == "ajouter_breakpoints_responsive":
                    # Breakpoints responsive complets
                    css_responsive = '''

/* BREAKPOINTS RESPONSIVE COMPLETS */
@media (max-width: 480px) {
    .container { padding: 0 15px !important; }
    h1, .villa-title { font-size: 1.8rem !important; }
    .info-card { margin: 10px 0 !important; padding: 15px !important; }
}

@media (min-width: 481px) and (max-width: 768px) {
    .container { padding: 0 20px !important; }
    h1, .villa-title { font-size: 2.2rem !important; }
}

@media (min-width: 769px) and (max-width: 1024px) {
    .container { max-width: 95% !important; }
    .info-card { padding: 25px !important; }
}

@media (min-width: 1025px) {
    .container { max-width: 1200px !important; }
}

'''
                    if '</style>' in contenu:
                        contenu = contenu.replace('</style>', css_responsive + '</style>')
                        corrections_appliquees.append("Breakpoints responsive")
                
                # Ajouter JavaScript hamburger si nécessaire
                if "ajouter_hamburger" in correction and 'mobileMenuToggle' not in contenu:
                    js_hamburger = '''

// JavaScript Hamburger
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.getElementById('mobileMenuToggle');
    const mobileMenu = document.getElementById('mobileMenu');
    
    if (hamburger && mobileMenu) {
        hamburger.addEventListener('click', function(e) {
            e.preventDefault();
            mobileMenu.classList.toggle('active');
            hamburger.classList.toggle('active');
        });
        
        mobileMenu.addEventListener('click', function(e) {
            if (e.target.tagName === 'A') {
                mobileMenu.classList.remove('active');
                hamburger.classList.remove('active');
            }
        });
    }
});

'''
                    contenu = contenu.replace('</body>', f'<script>{js_hamburger}</script></body>')
                    corrections_appliquees.append("JavaScript hamburger")
            
            # Sauvegarder si des modifications ont été apportées
            if contenu != contenu_original:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(contenu)
                
                print(f"  ✅ {len(corrections_appliquees)} corrections appliquées")
                self.corrections_par_page[nom_page] = corrections_appliquees
            else:
                print(f"  ℹ️ Aucune modification nécessaire")
                
        except Exception as e:
            print(f"  ❌ Erreur corrections: {e}")
    
    def generer_rapport_final(self):
        """Génère un rapport final complet"""
        rapport_file = f"/app/RAPPORT_DIAGNOSTIC_TOUTES_PAGES_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        # Calculer les statistiques
        total_pages = len(self.rapport_global)
        pages_parfaites = len([p for p in self.rapport_global.values() if p['score'] == 100])
        pages_problemes = len([p for p in self.rapport_global.values() if p['score'] < 80])
        score_moyen = sum([p['score'] for p in self.rapport_global.values()]) / total_pages
        
        with open(rapport_file, 'w', encoding='utf-8') as f:
            f.write(f"""# RAPPORT DIAGNOSTIC COMPLET - TOUTES LES PAGES VILLA
## Option A: Diagnostic Manuel Approfondi sur {total_pages} Pages

**Date:** {datetime.now().strftime('%d %B %Y %H:%M')}
**Pages analysées:** {total_pages} pages villa
**Score moyen:** {score_moyen:.1f}/100

---

## 📊 STATISTIQUES GLOBALES

- **Pages parfaites (100/100):** {pages_parfaites}
- **Pages avec problèmes (<80/100):** {pages_problemes}
- **Total corrections appliquées:** {sum([len(c) for c in self.corrections_par_page.values()])}

---

## 📋 DÉTAIL PAR PAGE

""")
            
            for nom_page, donnees in self.rapport_global.items():
                f.write(f"### {nom_page}\n")
                f.write(f"**Score:** {donnees['score']}/100\n\n")
                
                if donnees['problemes']:
                    f.write("**Problèmes détectés:**\n")
                    for probleme in donnees['problemes']:
                        f.write(f"- {probleme}\n")
                else:
                    f.write("✅ Aucun problème détecté\n")
                
                if nom_page in self.corrections_par_page:
                    f.write("\n**Corrections appliquées:**\n")
                    for correction in self.corrections_par_page[nom_page]:
                        f.write(f"- {correction}\n")
                
                f.write("\n---\n\n")
        
        print(f"📄 Rapport final généré: {rapport_file}")
        return rapport_file
    
    def executer_diagnostic_complet_toutes_pages(self):
        """Exécute le diagnostic et les corrections sur toutes les pages"""
        print("🎯 DIAGNOSTIC COMPLET SUR TOUTES LES PAGES VILLA")
        print("=" * 70)
        print(f"📋 {len(self.pages_villa)} pages villa à analyser")
        print()
        
        # Phase 1: Diagnostic de toutes les pages
        print("🔍 PHASE 1: DIAGNOSTIC DE TOUTES LES PAGES")
        print("-" * 50)
        for file_path in self.pages_villa:
            self.diagnostiquer_page_villa(file_path)
        
        # Phase 2: Application des corrections
        print("🔧 PHASE 2: APPLICATION DES CORRECTIONS")
        print("-" * 50)
        for file_path in self.pages_villa:
            self.appliquer_corrections_page(file_path)
        
        # Phase 3: Rapport final
        print("\n📊 PHASE 3: GÉNÉRATION DU RAPPORT FINAL")
        print("-" * 50)
        rapport_file = self.generer_rapport_final()
        
        print("\n" + "=" * 70)
        print("✅ DIAGNOSTIC COMPLET DE TOUTES LES PAGES TERMINÉ!")
        print(f"📄 Rapport: {rapport_file}")
        print("=" * 70)

if __name__ == "__main__":
    diagnostic = DiagnosticCompletToutesPages()
    diagnostic.executer_diagnostic_complet_toutes_pages()