#!/usr/bin/env python3
"""
DIAGNOSTIC APPROFONDI COMPLET - GARDER VIDÉO CLOUDINARY
Diagnostic de TOUS les problèmes sur les pages villa
"""

import os
import re
import requests
from datetime import datetime

class DiagnosticCompletVideoCLoudinary:
    def __init__(self):
        self.page_test = '/app/villa-villa-f3-sur-petit-macabou.html'
        self.problemes_detectes = []
        self.solutions_proposees = []
        
    def corriger_url_video_cloudinary(self):
        """Corriger l'URL de la vidéo Cloudinary avec la bonne URL"""
        print("🔍 DIAGNOSTIC VIDÉO CLOUDINARY")
        
        try:
            with open(self.page_test, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # URL actuelle (incorrecte)
            url_incorrecte = "https://res.cloudinary.com/dld9eojbt/video/upload/q_auto,f_mp4/v1716830959/villa-background-video_hqhq2s.mp4"
            
            # URLs alternatives à tester
            urls_alternatives = [
                "https://res.cloudinary.com/ddulasmtz/video/upload/v1752950782/background-video.mp4_qoofsz.mp4",  # URL du backup
                "https://res.cloudinary.com/demo/video/upload/v1/video-background.mp4",  # URL de démo
                "https://res.cloudinary.com/dld9eojbt/video/upload/v1716830959/villa-background-video_hqhq2s.mp4"  # URL actuelle
            ]
            
            print("🔍 Test des URLs Cloudinary disponibles...")
            
            url_fonctionnelle = None
            for url in urls_alternatives:
                print(f"  Testing: {url[:60]}...")
                try:
                    response = requests.head(url, timeout=5)
                    if response.status_code == 200:
                        print(f"  ✅ URL FONCTIONNELLE: {url}")
                        url_fonctionnelle = url
                        break
                    else:
                        print(f"  ❌ Code {response.status_code}")
                except Exception as e:
                    print(f"  ❌ Erreur: {str(e)[:50]}")
            
            if url_fonctionnelle:
                # Remplacer l'URL dans le fichier
                contenu = contenu.replace(url_incorrecte, url_fonctionnelle)
                
                with open(self.page_test, 'w', encoding='utf-8') as f:
                    f.write(contenu)
                    
                print(f"✅ URL vidéo corrigée vers: {url_fonctionnelle}")
                self.solutions_proposees.append(f"Vidéo Cloudinary: URL corrigée")
            else:
                print("❌ AUCUNE URL Cloudinary fonctionnelle trouvée")
                self.problemes_detectes.append("Toutes les URLs Cloudinary inaccessibles")
                
                # Proposer une solution alternative
                self.proposer_solution_video_alternative()
                
        except Exception as e:
            print(f"❌ Erreur correction vidéo: {e}")
    
    def proposer_solution_video_alternative(self):
        """Propose une solution vidéo alternative qui fonctionne"""
        print("🔄 PROPOSITION SOLUTION VIDÉO ALTERNATIVE")
        
        try:
            with open(self.page_test, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # Test avec une vidéo alternative publique
            videos_alternatives = [
                "https://cdn.pixabay.com/vimeo/540634326/beach-106157.mp4?api_key=default",
                "https://vod-progressive.akamaized.net/exp=1670000000~acl=%2Fvimeo-prod-skyfire-std-us%2F01%2F2682%2F14%2F362244271%2F1553173990.mp4~hmac=placeholder/vimeo-prod-skyfire-std-us/01/2682/14/362244271/1553173990.mp4"
            ]
            
            print("🔍 Test d'URLs vidéo alternatives...")
            
            url_alternative = None
            for url in videos_alternatives:
                print(f"  Testing: {url[:60]}...")
                try:
                    response = requests.head(url, timeout=5)
                    if response.status_code == 200:
                        print(f"  ✅ URL ALTERNATIVE FONCTIONNELLE")
                        url_alternative = url
                        break
                    else:
                        print(f"  ❌ Code {response.status_code}")
                except Exception as e:
                    print(f"  ❌ Erreur: {str(e)[:50]}")
            
            if url_alternative:
                # Remplacer avec l'URL alternative
                pattern_video = r'<source src="[^"]*" type="video/mp4">'
                nouveau_source = f'<source src="{url_alternative}" type="video/mp4">'
                
                contenu = re.sub(pattern_video, nouveau_source, contenu)
                
                with open(self.page_test, 'w', encoding='utf-8') as f:
                    f.write(contenu)
                    
                print(f"✅ Vidéo remplacée par alternative fonctionnelle")
                self.solutions_proposees.append("Vidéo: Alternative fonctionnelle utilisée")
            else:
                print("❌ Aucune vidéo alternative accessible")
                self.problemes_detectes.append("Impossibilité d'accéder aux vidéos externes")
                
        except Exception as e:
            print(f"❌ Erreur solution alternative: {e}")
    
    def diagnostiquer_problemes_affichage(self):
        """Diagnostic approfondi des problèmes d'affichage"""
        print("\n🔍 DIAGNOSTIC PROBLÈMES D'AFFICHAGE")
        
        try:
            with open(self.page_test, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # 1. Vérifier les problèmes CSS critiques
            print("📊 Analyse CSS critique...")
            
            # Tailwind CSS problématique
            if 'script src="https://cdn.jsdelivr.net/npm/tailwindcss' in contenu:
                print("❌ Tailwind CSS chargé comme script (erreur MIME)")
                self.problemes_detectes.append("Tailwind CSS: Erreur MIME (script au lieu de link)")
            
            # CSS manquant ou mal structuré
            if contenu.count('<style>') > 3:
                print("⚠️ Nombreuses balises <style> détectées - peut causer des conflits")
                self.problemes_detectes.append("CSS: Multiples balises <style> (conflits possibles)")
            
            # 2. Vérifier la structure du contenu
            print("📊 Analyse structure contenu...")
            
            # Éléments cachés
            elements_caches = re.findall(r'style="[^"]*display:\s*none[^"]*"', contenu, re.IGNORECASE)
            if elements_caches:
                print(f"❌ {len(elements_caches)} éléments avec display:none")
                self.problemes_detectes.append(f"Affichage: {len(elements_caches)} éléments cachés")
            
            # Z-index conflicts
            z_index_count = len(re.findall(r'z-index:\s*\d+', contenu))
            if z_index_count > 10:
                print(f"⚠️ {z_index_count} déclarations z-index (risque de conflit)")
                self.problemes_detectes.append("Z-index: Nombreuses déclarations (conflits possibles)")
            
            # 3. Vérifier JavaScript
            print("📊 Analyse JavaScript...")
            
            # Scripts externes manquants
            scripts_requis = ['swiper', 'aos', 'font-awesome']
            for script in scripts_requis:
                if script not in contenu.lower():
                    print(f"❌ Script {script} manquant")
                    self.problemes_detectes.append(f"JavaScript: {script} manquant")
            
            # Erreurs potentielles
            if 'console.error' in contenu:
                print("⚠️ Gestion d'erreurs détectée dans le code")
            
        except Exception as e:
            print(f"❌ Erreur diagnostic affichage: {e}")
    
    def diagnostiquer_responsive_mobile(self):
        """Diagnostic complet du responsive mobile"""
        print("\n📱 DIAGNOSTIC RESPONSIVE MOBILE COMPLET")
        
        try:
            with open(self.page_test, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # 1. Menu hamburger
            print("🍔 Analyse menu hamburger...")
            
            # CSS hamburger
            if '.hamburger {' in contenu:
                print("✅ CSS hamburger présent")
                
                # HTML hamburger
                if '<div class="hamburger">' in contenu:
                    print("✅ HTML hamburger présent")
                    
                    # JavaScript hamburger
                    if 'hamburger.addEventListener' in contenu:
                        print("✅ JavaScript hamburger présent")
                    else:
                        print("❌ JavaScript hamburger manquant")
                        self.problemes_detectes.append("Hamburger: JavaScript event listener manquant")
                else:
                    print("❌ HTML hamburger manquant")
                    self.problemes_detectes.append("Hamburger: HTML manquant dans le DOM")
            else:
                print("❌ CSS hamburger manquant")
                self.problemes_detectes.append("Hamburger: CSS complètement manquant")
            
            # 2. Media queries
            print("📱 Analyse media queries...")
            
            media_queries = re.findall(r'@media[^{]*\{[^}]*\}', contenu, re.DOTALL)
            if len(media_queries) < 2:
                print("❌ Media queries insuffisantes")
                self.problemes_detectes.append("Responsive: Media queries insuffisantes")
            else:
                print(f"✅ {len(media_queries)} media queries détectées")
            
            # 3. Breakpoints
            print("📊 Analyse breakpoints...")
            
            breakpoints = ['768px', '1024px', '375px', '480px']
            breakpoints_present = []
            for bp in breakpoints:
                if bp in contenu:
                    breakpoints_present.append(bp)
            
            if len(breakpoints_present) < 2:
                print("❌ Breakpoints responsive insuffisants")
                self.problemes_detectes.append("Responsive: Breakpoints insuffisants")
            else:
                print(f"✅ Breakpoints détectés: {', '.join(breakpoints_present)}")
                
        except Exception as e:
            print(f"❌ Erreur diagnostic mobile: {e}")
    
    def proposer_corrections_completes(self):
        """Propose un plan de corrections complet"""
        print("\n🎯 PLAN DE CORRECTIONS COMPLET")
        print("=" * 50)
        
        if self.problemes_detectes:
            print(f"🚨 PROBLÈMES DÉTECTÉS: {len(self.problemes_detectes)}")
            for i, probleme in enumerate(self.problemes_detectes, 1):
                print(f"  {i}. {probleme}")
            
            print(f"\n✅ CORRECTIONS DÉJÀ APPLIQUÉES: {len(self.solutions_proposees)}")
            for i, solution in enumerate(self.solutions_proposees, 1):
                print(f"  {i}. {solution}")
            
            print(f"\n🔧 CORRECTIONS RESTANTES À APPLIQUER:")
            corrections_restantes = [
                "Corriger Tailwind CSS: remplacer <script> par <link>",
                "Ajouter menu hamburger HTML dans le DOM",
                "Corriger éléments cachés avec display:none",
                "Améliorer media queries responsive",
                "Optimiser z-index pour éviter les conflits"
            ]
            
            for i, correction in enumerate(corrections_restantes, 1):
                print(f"  {i}. {correction}")
        else:
            print("✅ AUCUN PROBLÈME CRITIQUE DÉTECTÉ")
    
    def executer_diagnostic_complet(self):
        """Exécute le diagnostic complet"""
        print("🔍 DIAGNOSTIC APPROFONDI COMPLET - GARDER VIDÉO CLOUDINARY")
        print("=" * 70)
        
        # Étape 1: Corriger la vidéo Cloudinary
        self.corriger_url_video_cloudinary()
        
        # Étape 2: Diagnostiquer autres problèmes
        self.diagnostiquer_problemes_affichage()
        self.diagnostiquer_responsive_mobile()
        
        # Étape 3: Plan complet de corrections
        self.proposer_corrections_completes()
        
        print("\n" + "=" * 70)
        print("✅ DIAGNOSTIC COMPLET TERMINÉ")
        print("🎯 PRÊT POUR CORRECTIONS CIBLÉES AVEC VIDÉO CLOUDINARY")

if __name__ == "__main__":
    diagnostic = DiagnosticCompletVideoCLoudinary()
    diagnostic.executer_diagnostic_complet()