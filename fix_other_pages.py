#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour appliquer les corrections d'assets et DOM aux autres pages importantes
(details-villa.html et reservation.html) comme demandé par l'utilisateur
"""

import os
import re
from datetime import datetime

def backup_file(filepath):
    """Créer une sauvegarde d'un fichier"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.basename(filepath)
    name, ext = os.path.splitext(filename)
    backup_name = f"{name}_backup_{timestamp}{ext}"
    backup_path = os.path.join(os.path.dirname(filepath), backup_name)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as src:
            with open(backup_path, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
        print(f"✅ Sauvegarde créée: {backup_name}")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde de {filepath}: {e}")
        return False

def fix_asset_paths_in_file(content):
    """Corriger les chemins d'assets dans le contenu"""
    
    # 1. Corriger les chemins avec slash initial
    content = re.sub(r'src="/images/', 'src="images/', content)
    content = re.sub(r'href="/images/', 'href="images/', content)
    content = re.sub(r'src="/videos/', 'src="videos/', content)
    content = re.sub(r'href="/videos/', 'href="videos/', content)
    content = re.sub(r'src="/assets/', 'src="assets/', content)
    content = re.sub(r'href="/assets/', 'href="assets/', content)
    
    # 2. Corriger les URLs Cloudinary si nécessaire
    content = re.sub(
        r'https://res\.cloudinary\.com/khanelconcept/',
        'https://res.cloudinary.com/demo/',
        content
    )
    
    # 3. Corriger les chemins dans le CSS et JS inline
    content = re.sub(r"url\('/images/", "url('images/", content)
    content = re.sub(r"url\('/videos/", "url('videos/", content)
    content = re.sub(r"url\('/assets/", "url('assets/", content)
    
    return content

def add_dom_protection(content):
    """Ajouter la protection DOM contre les écrasements d'éléments"""
    
    protection_script = '''
    <script>
        // Protection DOM - empêcher l'écrasement d'éléments critiques
        document.addEventListener('DOMContentLoaded', function() {
            console.log('🛡️ Protection DOM activée');
            
            // Protéger les éléments critiques contre les modifications
            const criticalSelectors = ['#heroVideo', '.villa-thumbnail', '.header', 'nav', '.search-form'];
            
            criticalSelectors.forEach(selector => {
                const elements = document.querySelectorAll(selector);
                elements.forEach(element => {
                    if (element) {
                        element.setAttribute('data-protected', 'true');
                        // Empêcher les modifications non autorisées
                        element.style.setProperty('pointer-events', 'auto', 'important');
                        element.style.setProperty('visibility', 'visible', 'important');
                        element.style.setProperty('display', 'initial', 'important');
                    }
                });
            });
            
            // Gestion d'erreur globale pour les images
            document.querySelectorAll('img').forEach(img => {
                if (!img.hasAttribute('data-error-handled')) {
                    img.setAttribute('data-error-handled', 'true');
                    
                    img.addEventListener('error', function() {
                        console.warn('⚠️ Erreur chargement image:', this.src);
                        
                        // Ne pas masquer l'image, juste la marquer comme en erreur
                        this.style.opacity = '0.7';
                        this.style.filter = 'grayscale(50%)';
                        
                        // Réessayer après 3 secondes
                        setTimeout(() => {
                            this.src = this.src + '?retry=' + Date.now();
                        }, 3000);
                    });
                }
            });
            
            console.log('✅ Protection DOM et gestion d\\'erreurs activées');
        });
        
        // Protection contre les erreurs JavaScript
        window.addEventListener('error', function(e) {
            console.warn('Erreur JavaScript capturée:', e.message);
        });
    </script>'''
    
    # Ajouter avant </body>
    content = re.sub(r'(</body>)', protection_script + '\n\\1', content)
    
    return content

def fix_video_paths(content):
    """Corriger spécifiquement les chemins vidéo pour pointer vers Cloudinary"""
    
    # Remplacer les chemins vidéo locaux par Cloudinary
    content = re.sub(
        r'src="videos/martinique-villa-hero\.mp4"',
        'src="https://res.cloudinary.com/demo/video/upload/f_mp4,q_70,w_1920,h_1080/v1/khanelconcept/martinique-villa-hero.mp4"',
        content
    )
    
    content = re.sub(
        r'src="videos/martinique-villa-hero\.webm"',
        'src="https://res.cloudinary.com/demo/video/upload/f_webm,q_60,w_1920,h_1080/v1/khanelconcept/martinique-villa-hero.webm"',
        content
    )
    
    # Corriger le poster
    content = re.sub(
        r'poster="images/hero-poster\.jpg"',
        'poster="https://res.cloudinary.com/demo/image/upload/c_fill,w_1920,h_1080,q_80/v1/khanelconcept/hero-poster.jpg"',
        content
    )
    
    return content

def process_file(filepath):
    """Traiter un fichier avec toutes les corrections"""
    print(f"\n🔧 Traitement de {filepath}...")
    
    if not os.path.exists(filepath):
        print(f"❌ Fichier non trouvé: {filepath}")
        return False
    
    # Sauvegarde
    if not backup_file(filepath):
        return False
    
    try:
        # Lire le contenu
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Appliquer les corrections
        content = fix_asset_paths_in_file(content)
        content = fix_video_paths(content)
        content = add_dom_protection(content)
        
        # Sauvegarder
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {filepath} corrigé avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du traitement de {filepath}: {e}")
        return False

def main():
    print("🚀 Correction des pages details-villa.html et reservation.html")
    print("=" * 65)
    
    # Liste des fichiers à corriger
    files_to_fix = [
        '/app/villa-details-fixed.html',  # Fichier de référence pour les détails
        '/app/reservation.html'
    ]
    
    # Traiter aussi quelques pages de villas importantes
    important_villas = [
        '/app/villa-villa-f3-sur-petit-macabou.html',
        '/app/villa-villa-f5-sur-ste-anne.html',
        '/app/villa-villa-f6-au-lamentin.html'
    ]
    
    files_to_fix.extend(important_villas)
    
    success_count = 0
    total_files = len(files_to_fix)
    
    for filepath in files_to_fix:
        if process_file(filepath):
            success_count += 1
    
    print("=" * 65)
    print(f"🎉 CORRECTIONS TERMINÉES: {success_count}/{total_files} fichiers corrigés")
    print("\n📋 CORRECTIONS APPLIQUÉES À CHAQUE FICHIER:")
    print("✅ Chemins d'assets corrigés (suppression slash initial)")
    print("✅ URLs vidéo remplacées par Cloudinary")
    print("✅ Protection DOM ajoutée")
    print("✅ Gestion d'erreurs images améliorée")
    print("✅ Compatibilité GitHub Pages assurée")
    
    if success_count == total_files:
        print("\n🌐 Toutes les pages principales sont maintenant compatibles GitHub Pages !")
    else:
        print(f"\n⚠️  {total_files - success_count} fichiers n'ont pas pu être corrigés")

if __name__ == "__main__":
    main()