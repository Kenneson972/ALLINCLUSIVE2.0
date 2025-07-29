#!/usr/bin/env python3
"""
DIAGNOSTIC MANUEL APPROFONDI - PAGE VILLA F3 PETIT MACABOU
Option A: Diagnostic page par page avec corrections ciblées
"""

import os
import re
from datetime import datetime

class DiagnosticManuelApprofondi:
    def __init__(self):
        self.page_test = '/app/villa-villa-f3-sur-petit-macabou.html'
        self.problemes_detectes = []
        self.corrections_a_appliquer = []
        
    def diagnostic_complet_page(self):
        """Effectue un diagnostic complet de la page test"""
        print("🔍 DIAGNOSTIC MANUEL APPROFONDI - VILLA F3 PETIT MACABOU")
        print("=" * 60)
        
        try:
            with open(self.page_test, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            self.analyser_structure_html(contenu)
            self.analyser_css_styles(contenu)
            self.analyser_javascript(contenu)
            self.analyser_assets_externes(contenu)
            self.analyser_responsive_mobile(contenu)
            
            self.generer_rapport_diagnostique()
            self.proposer_corrections_ciblees()
            
        except Exception as e:
            print(f"❌ Erreur lors du diagnostic: {e}")
    
    def analyser_structure_html(self, contenu):
        """Analyse la structure HTML de base"""
        print("📋 ANALYSE STRUCTURE HTML")
        
        # DOCTYPE et meta tags
        if '<!DOCTYPE html>' in contenu:
            print("✅ DOCTYPE HTML5 présent")
        else:
            self.problemes_detectes.append("DOCTYPE HTML5 manquant")
            
        if 'charset="UTF-8"' in contenu:
            print("✅ Meta charset UTF-8 présent")
        else:
            self.problemes_detectes.append("Meta charset manquant")
            
        # Structure du body
        if '<main' in contenu:
            print("✅ Élément <main> présent")
        else:
            print("⚠️ Élément <main> manquant - peut affecter l'accessibilité")
            
        # Navigation
        if '<nav' in contenu:
            print("✅ Navigation présente")
        else:
            self.problemes_detectes.append("Navigation manquante")
            
        # Vérifier si le contenu principal est visible
        style_display_none = re.findall(r'style="[^"]*display:\s*none', contenu, re.IGNORECASE)
        if style_display_none:
            print(f"⚠️ {len(style_display_none)} éléments avec display:none détectés")
            self.problemes_detectes.append(f"Éléments cachés: {style_display_none}")
        
        print()
    
    def analyser_css_styles(self, contenu):
        """Analyse les styles CSS"""
        print("🎨 ANALYSE CSS STYLES")
        
        # Vérifier le CSS glassmorphism
        if 'backdrop-filter' in contenu:
            print("✅ CSS glassmorphism (backdrop-filter) présent")
        else:
            print("❌ CSS glassmorphism manquant")
            self.problemes_detectes.append("Effets glassmorphism manquants")
            
        # Vérifier Tailwind CSS
        tailwind_patterns = [
            'cdn.tailwindcss.com',
            'tailwindcss@',
            'script.*tailwind'
        ]
        
        tailwind_trouve = False
        for pattern in tailwind_patterns:
            if re.search(pattern, contenu, re.IGNORECASE):
                if 'script.*tailwind.*css' in pattern and re.search(pattern, contenu):
                    print("❌ Tailwind CSS chargé comme script (erreur MIME)")
                    self.problemes_detectes.append("Tailwind CSS: erreur MIME type (script au lieu de link)")
                    self.corrections_a_appliquer.append("Corriger Tailwind CSS: remplacer <script> par <link>")
                else:
                    print("✅ Tailwind CSS détecté")
                tailwind_trouve = True
                break
                
        if not tailwind_trouve:
            print("⚠️ Tailwind CSS non détecté")
            
        # Vérifier les media queries mobile
        if '@media' in contenu and '768px' in contenu:
            print("✅ Media queries responsive présentes")
        else:
            print("⚠️ Media queries mobile manquantes ou incomplètes")
            self.problemes_detectes.append("Media queries responsive insuffisantes")
            
        print()
    
    def analyser_javascript(self, contenu):
        """Analyse le JavaScript"""
        print("⚙️ ANALYSE JAVASCRIPT")
        
        # Vérifier les scripts essentiels
        scripts_essentiels = {
            'Swiper': 'swiper',
            'AOS': 'aos',
            'Font Awesome': 'font-awesome'
        }
        
        for nom, pattern in scripts_essentiels.items():
            if pattern in contenu.lower():
                print(f"✅ {nom} détecté")
            else:
                print(f"⚠️ {nom} manquant")
                
        # Vérifier les fonctions personnalisées
        if 'addEventListener' in contenu:
            print("✅ Event listeners personnalisés présents")
        else:
            print("⚠️ Pas d'event listeners détectés")
            
        # Vérifier les erreurs JS potentielles
        if 'querySelector' in contenu:
            print("✅ DOM manipulation présente")
        else:
            print("⚠️ Pas de DOM manipulation détectée")
            
        print()
    
    def analyser_assets_externes(self, contenu):
        """Analyse les assets externes (vidéo, logo, etc.)"""
        print("🌐 ANALYSE ASSETS EXTERNES")
        
        # Vidéo Cloudinary
        video_patterns = [
            r'cloudinary\.com/[^"]*\.mp4',
            r'background-video[^"]*\.mp4'
        ]
        
        video_trouve = False
        for pattern in video_patterns:
            matches = re.findall(pattern, contenu)
            if matches:
                print(f"🎥 Vidéo détectée: {matches[0]}")
                video_trouve = True
                # Problème connu avec cette URL
                if 'dld9eojbt' in matches[0]:
                    print("❌ URL vidéo Cloudinary problématique (ERR_BLOCKED_BY_ORB)")
                    self.problemes_detectes.append("Vidéo Cloudinary inaccessible")
                    self.corrections_a_appliquer.append("Remplacer vidéo Cloudinary par alternative fonctionnelle")
                break
                
        if not video_trouve:
            print("❌ Aucune vidéo background détectée")
            self.problemes_detectes.append("Vidéo background manquante")
            
        # Logo
        logo_patterns = [
            r'customer-assets\.emergentagent\.com[^"]*\.png',
            r'logo[^"]*\.png'
        ]
        
        logo_trouve = False
        for pattern in logo_patterns:
            matches = re.findall(pattern, contenu)
            if matches:
                print(f"🖼️ Logo détecté: {matches[0]}")
                logo_trouve = True
                # Vérifier si c'est le logo problématique
                if 'job_villa-dash' in matches[0]:
                    print("❌ URL logo problématique")
                    self.problemes_detectes.append("Logo inaccessible")
                    self.corrections_a_appliquer.append("Corriger URL du logo")
                break
                
        if not logo_trouve:
            print("❌ Logo non détecté")
            self.problemes_detectes.append("Logo manquant")
            
        print()
    
    def analyser_responsive_mobile(self, contenu):
        """Analyse la compatibilité mobile"""
        print("📱 ANALYSE RESPONSIVE MOBILE")
        
        # Menu hamburger
        hamburger_elements = [
            '.hamburger',
            'hamburger',
            'menu-toggle',
            'mobile-menu'
        ]
        
        hamburger_css_present = False
        hamburger_html_present = False
        
        for element in hamburger_elements:
            if element in contenu:
                print(f"✅ Élément hamburger CSS trouvé: {element}")
                hamburger_css_present = True
                break
                
        if '<div class="hamburger">' in contenu:
            print("✅ HTML hamburger présent")
            hamburger_html_present = True
        else:
            print("❌ HTML hamburger manquant")
            
        if hamburger_css_present and not hamburger_html_present:
            print("⚠️ CSS hamburger présent mais HTML manquant")
            self.problemes_detectes.append("Menu hamburger: CSS présent mais HTML manquant")
            self.corrections_a_appliquer.append("Ajouter HTML hamburger dans le DOM")
        elif not hamburger_css_present:
            print("❌ Menu hamburger complètement manquant")
            self.problemes_detectes.append("Menu hamburger mobile absent")
            self.corrections_a_appliquer.append("Implémenter menu hamburger complet")
            
        # Viewport meta
        if 'viewport' in contenu:
            print("✅ Meta viewport présent")
        else:
            print("❌ Meta viewport manquant")
            self.problemes_detectes.append("Meta viewport manquant")
            
        print()
    
    def generer_rapport_diagnostique(self):
        """Génère un rapport détaillé des problèmes détectés"""
        print("📊 RAPPORT DIAGNOSTIC")
        print("=" * 40)
        
        if self.problemes_detectes:
            print(f"🚨 PROBLÈMES DÉTECTÉS ({len(self.problemes_detectes)}):")
            for i, probleme in enumerate(self.problemes_detectes, 1):
                print(f"  {i}. {probleme}")
        else:
            print("✅ Aucun problème majeur détecté")
            
        print()
        
        if self.corrections_a_appliquer:
            print(f"🔧 CORRECTIONS À APPLIQUER ({len(self.corrections_a_appliquer)}):")
            for i, correction in enumerate(self.corrections_a_appliquer, 1):
                print(f"  {i}. {correction}")
        else:
            print("ℹ️ Aucune correction nécessaire")
            
        print()
    
    def proposer_corrections_ciblees(self):
        """Propose des corrections spécifiques et ciblées"""
        print("🎯 PLAN DE CORRECTIONS CIBLÉES")
        print("=" * 40)
        
        if self.corrections_a_appliquer:
            print("ORDRE DE PRIORITÉ:")
            
            # Priorité 1: Assets critiques
            priorite1 = [c for c in self.corrections_a_appliquer if 'vidéo' in c.lower() or 'logo' in c.lower()]
            if priorite1:
                print("\n🔥 PRIORITÉ 1 - ASSETS CRITIQUES:")
                for correction in priorite1:
                    print(f"  • {correction}")
            
            # Priorité 2: Navigation mobile
            priorite2 = [c for c in self.corrections_a_appliquer if 'hamburger' in c.lower() or 'mobile' in c.lower()]
            if priorite2:
                print("\n📱 PRIORITÉ 2 - NAVIGATION MOBILE:")
                for correction in priorite2:
                    print(f"  • {correction}")
            
            # Priorité 3: CSS/JS
            priorite3 = [c for c in self.corrections_a_appliquer if 'css' in c.lower() or 'tailwind' in c.lower()]
            if priorite3:
                print("\n🎨 PRIORITÉ 3 - CSS/FRAMEWORK:")
                for correction in priorite3:
                    print(f"  • {correction}")
                    
        print("\n🚀 PRÊT POUR CORRECTIONS MANUELLES CIBLÉES")
        print("=" * 60)

if __name__ == "__main__":
    diagnostic = DiagnosticManuelApprofondi()
    diagnostic.diagnostic_complet_page()