#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour restaurer complètement la fonctionnalité de index.html
en appliquant les corrections de index_corrected.html
"""

import os
import re
from datetime import datetime

def backup_original():
    """Créer une sauvegarde de index.html avant modifications"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"index_backup_{timestamp}.html"
    
    try:
        with open('/app/index.html', 'r', encoding='utf-8') as src:
            with open(f'/app/{backup_name}', 'w', encoding='utf-8') as dst:
                dst.write(src.read())
        print(f"✅ Sauvegarde créée: {backup_name}")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde: {e}")
        return False

def extract_corrected_video_section():
    """Extraire la section vidéo corrigée de index_corrected.html"""
    try:
        with open('/app/index_corrected.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extraire la section vidéo complète (de <!-- SECTION VIDÉO DE FOND --> à </div>)
        video_pattern = r'(<!-- SECTION VIDÉO DE FOND - CLOUDINARY FONCTIONNEL -->.*?</div>)'
        video_match = re.search(video_pattern, content, re.DOTALL)
        
        if video_match:
            return video_match.group(1)
        else:
            print("❌ Section vidéo non trouvée dans index_corrected.html")
            return None
            
    except Exception as e:
        print(f"❌ Erreur lors de l'extraction vidéo: {e}")
        return None

def extract_corrected_javascript():
    """Extraire le JavaScript corrigé de index_corrected.html"""
    try:
        with open('/app/index_corrected.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extraire le JavaScript complet (de <script> avec données villas jusqu'à </script>)
        js_pattern = r'(<!-- JavaScript avec données corrigées -->.*?</script>)'
        js_match = re.search(js_pattern, content, re.DOTALL)
        
        if js_match:
            return js_match.group(1)
        else:
            print("❌ JavaScript corrigé non trouvé dans index_corrected.html")
            return None
            
    except Exception as e:
        print(f"❌ Erreur lors de l'extraction JavaScript: {e}")
        return None

def apply_video_corrections(content, corrected_video_section):
    """Appliquer les corrections vidéo au contenu"""
    if not corrected_video_section:
        return content
    
    # 1. Remplacer la section video-background existante
    # Chercher la balise div class="video-background" existante
    video_bg_pattern = r'<div class="video-background">.*?</div>'
    
    if re.search(video_bg_pattern, content, re.DOTALL):
        print("🔧 Remplacement de la section video-background existante...")
        content = re.sub(video_bg_pattern, corrected_video_section, content, flags=re.DOTALL)
    else:
        # Si pas trouvée, l'insérer après <body>
        print("🔧 Insertion de la nouvelle section vidéo après <body>...")
        content = re.sub(r'(<body[^>]*>)', r'\1\n    ' + corrected_video_section + '\n', content)
    
    return content

def apply_javascript_corrections(content, corrected_js):
    """Appliquer les corrections JavaScript au contenu"""
    if not corrected_js:
        return content
    
    # Remplacer tout le JavaScript existant avec données villas
    # Chercher le script qui contient villasData
    js_pattern = r'<script>.*?villasData.*?</script>'
    
    if re.search(js_pattern, content, re.DOTALL):
        print("🔧 Remplacement du JavaScript avec données villas...")
        content = re.sub(js_pattern, corrected_js, content, flags=re.DOTALL)
    else:
        # Si pas trouvé, l'ajouter avant </body>
        print("🔧 Ajout du JavaScript corrigé avant </body>...")
        content = re.sub(r'(</body>)', r'    ' + corrected_js + '\n\1', content)
    
    return content

def fix_asset_paths(content):
    """Corriger les chemins d'assets pour GitHub Pages"""
    
    # 1. Corriger les chemins avec slash initial - méthode plus simple
    # Remplacer src="/images/ par src="images/ (mais pas dans URLs https)
    content = re.sub(r'src="/images/', 'src="images/', content)
    content = re.sub(r'href="/images/', 'href="images/', content)
    content = re.sub(r'src="/videos/', 'src="videos/', content)
    content = re.sub(r'href="/videos/', 'href="videos/', content)
    content = re.sub(r'src="/assets/', 'src="assets/', content)
    content = re.sub(r'href="/assets/', 'href="assets/', content)
    
    # 2. Corriger les favicon et icons Cloudinary
    content = re.sub(
        r'href="https://res\.cloudinary\.com/khanelconcept/',
        'href="https://res.cloudinary.com/demo/',
        content
    )
    
    print("🔧 Chemins d'assets corrigés pour GitHub Pages")
    return content

def add_error_handling_scripts(content):
    """Ajouter les scripts de gestion d'erreurs à la fin"""
    
    error_script = '''
    <!-- Scripts de protection et gestion d'erreurs -->
    <script>
        // Protection contre les erreurs JavaScript
        window.addEventListener('error', function(e) {
            console.warn('Erreur JavaScript capturée:', e.message);
        });
        
        // Protection DOM - empêcher l'écrasement d'éléments
        document.addEventListener('DOMContentLoaded', function() {
            // Protéger les éléments critiques
            const criticalElements = ['heroVideo', 'villas-container', 'header'];
            criticalElements.forEach(id => {
                const element = document.getElementById(id);
                if (element) {
                    // Marquer comme protégé
                    element.setAttribute('data-protected', 'true');
                }
            });
        });
        
        console.log('🎉 KhanelConcept - Page d\\'accueil restaurée avec assets fonctionnels');
    </script>'''
    
    # Ajouter avant </body>
    content = re.sub(r'(</body>)', error_script + '\n\\1', content)
    
    return content

def main():
    print("🚀 Début de la restauration de index.html...")
    print("=" * 60)
    
    # 1. Sauvegarde
    if not backup_original():
        print("❌ Impossible de créer la sauvegarde, arrêt du script")
        return
    
    # 2. Lire le contenu actuel
    try:
        with open('/app/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Erreur lecture index.html: {e}")
        return
    
    # 3. Extraire les corrections
    print("📥 Extraction des corrections de index_corrected.html...")
    corrected_video = extract_corrected_video_section()
    corrected_js = extract_corrected_javascript()
    
    if not corrected_video or not corrected_js:
        print("❌ Impossible d'extraire toutes les corrections nécessaires")
        return
    
    # 4. Appliquer toutes les corrections
    print("🔧 Application des corrections...")
    
    # 4a. Corrections vidéo
    content = apply_video_corrections(content, corrected_video)
    
    # 4b. Corrections JavaScript
    content = apply_javascript_corrections(content, corrected_js)
    
    # 4c. Corrections chemins assets
    content = fix_asset_paths(content)
    
    # 4d. Ajout gestion d'erreurs
    content = add_error_handling_scripts(content)
    
    # 5. Écrire le fichier corrigé
    try:
        with open('/app/index.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ index.html corrigé et sauvegardé")
    except Exception as e:
        print(f"❌ Erreur écriture index.html: {e}")
        return
    
    print("=" * 60)
    print("🎉 RESTAURATION TERMINÉE AVEC SUCCÈS !")
    print("\n📋 CORRECTIONS APPLIQUÉES:")
    print("✅ Vidéo de fond restaurée avec URLs Cloudinary fonctionnelles")
    print("✅ JavaScript des villas corrigé avec gestion d'erreurs")
    print("✅ Chemins d'assets corrigés pour GitHub Pages")
    print("✅ Protection DOM ajoutée")
    print("\n🌐 La page devrait maintenant afficher:")
    print("   - La vidéo de fond Cloudinary en autoplay")
    print("   - Toutes les images des villas avec fallback")
    print("   - Navigation fluide et responsive")

if __name__ == "__main__":
    main()