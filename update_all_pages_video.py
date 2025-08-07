#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour remplacer l'index.html et ajouter le bloc vidéo background
à toutes les pages HTML du site ALLINCLUSIVE2.0
"""

import os
import re
import requests
from datetime import datetime

def backup_file(filepath):
    """Créer une sauvegarde d'un fichier"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.basename(filepath)
    name, ext = os.path.splitext(filename)
    backup_name = f"{name}_backup_video_{timestamp}{ext}"
    backup_path = os.path.join(os.path.dirname(filepath), backup_name)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as src:
            with open(backup_path, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
        print(f"✅ Sauvegarde: {backup_name}")
        return True
    except Exception as e:
        print(f"❌ Erreur sauvegarde {filepath}: {e}")
        return False

def replace_index_html():
    """Remplacer l'index.html actuel par le nouveau fichier fourni"""
    print("🔄 Remplacement de index.html...")
    
    # Sauvegarde de l'ancien index
    if not backup_file('/app/index.html'):
        print("⚠️ Impossible de sauvegarder l'ancien index.html")
        return False
    
    try:
        # Remplacer par le nouveau fichier
        os.rename('/app/new_index.html', '/app/index.html')
        print("✅ index.html remplacé avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur remplacement index.html: {e}")
        return False

def create_poster_image():
    """Créer l'image poster si elle n'existe pas"""
    poster_path = '/app/images/hero-poster.jpg'
    
    if os.path.exists(poster_path):
        print(f"✅ Image poster existe déjà: {poster_path}")
        return True
    
    print("📸 Création de l'image poster manquante...")
    
    # Créer le dossier images s'il n'existe pas
    os.makedirs('/app/images', exist_ok=True)
    
    try:
        # Utiliser une image par défaut (petite image de fallback)
        # Créer une image simple avec Python PIL si disponible, sinon copier une image existante
        sample_images = []
        for root, dirs, files in os.walk('/app/images'):
            for file in files[:3]:  # Prendre les 3 premières images trouvées
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    sample_images.append(os.path.join(root, file))
        
        if sample_images:
            # Copier la première image trouvée comme poster
            import shutil
            shutil.copy2(sample_images[0], poster_path)
            print(f"✅ Image poster créée: {poster_path}")
            return True
        else:
            print("⚠️ Aucune image trouvée pour créer le poster")
            return False
            
    except Exception as e:
        print(f"❌ Erreur création poster: {e}")
        return False

def get_video_block():
    """Retourner le bloc vidéo à insérer"""
    return '''<div class="video-background">
  <video autoplay loop muted playsinline poster="images/hero-poster.jpg">
    <source src="https://res.cloudinary.com/ddulasmtz/video/upload/v1752950782/background-video.webm" type="video/webm">
    Votre navigateur ne supporte pas la vidéo HTML5.
  </video>
  <div class="video-overlay"></div>
</div>'''

def has_video_background(content):
    """Vérifier si le fichier a déjà le bloc vidéo background"""
    return 'class="video-background"' in content or 'video-background' in content

def insert_video_block(filepath):
    """Insérer le bloc vidéo dans un fichier HTML après <body>"""
    print(f"🎬 Traitement: {os.path.basename(filepath)}")
    
    if not os.path.exists(filepath):
        print(f"❌ Fichier non trouvé: {filepath}")
        return False
    
    try:
        # Lire le contenu
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier si le bloc existe déjà
        if has_video_background(content):
            print(f"   ✅ Bloc vidéo déjà présent dans {os.path.basename(filepath)}")
            return True
        
        # Chercher l'ouverture de <body>
        body_pattern = r'(<body[^>]*>)'
        body_match = re.search(body_pattern, content, re.IGNORECASE)
        
        if not body_match:
            print(f"   ❌ Balise <body> non trouvée dans {os.path.basename(filepath)}")
            return False
        
        # Insérer le bloc vidéo juste après <body>
        video_block = get_video_block()
        
        # Insertion après la balise body
        insertion_point = body_match.end()
        new_content = (
            content[:insertion_point] + 
            '\n    ' + video_block + '\n' +
            content[insertion_point:]
        )
        
        # Écrire le nouveau contenu
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"   ✅ Bloc vidéo ajouté à {os.path.basename(filepath)}")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def find_all_html_files():
    """Trouver tous les fichiers HTML dans le projet"""
    html_files = []
    
    for root, dirs, files in os.walk('/app'):
        # Exclure certains dossiers
        dirs[:] = [d for d in dirs if d not in ['node_modules', '__pycache__', '.git', 'backup_phase1_20250729_005829']]
        
        for file in files:
            if file.endswith('.html') and not file.startswith('index_'):
                filepath = os.path.join(root, file)
                html_files.append(filepath)
    
    # Trier par nom pour un affichage ordonné
    html_files.sort()
    return html_files

def main():
    print("🚀 MISE À JOUR COMPLÈTE - ALLINCLUSIVE2.0")
    print("Remplacer index.html + Ajouter bloc vidéo à toutes les pages")
    print("=" * 70)
    
    # 1. Remplacer index.html
    print("\n📋 ÉTAPE 1: Remplacement de index.html")
    if not replace_index_html():
        print("❌ Impossible de remplacer index.html, arrêt du script")
        return
    
    # 2. Créer l'image poster si nécessaire
    print("\n📋 ÉTAPE 2: Vérification image poster")
    create_poster_image()
    
    # 3. Trouver tous les fichiers HTML
    print("\n📋 ÉTAPE 3: Recherche des fichiers HTML")
    html_files = find_all_html_files()
    
    # Filtrer pour exclure index.html (déjà traité)
    html_files = [f for f in html_files if not f.endswith('/index.html')]
    
    print(f"📁 {len(html_files)} fichiers HTML trouvés (hors index.html)")
    
    # Afficher la liste des fichiers
    for f in html_files[:10]:  # Afficher les 10 premiers
        print(f"   - {os.path.basename(f)}")
    
    if len(html_files) > 10:
        print(f"   ... et {len(html_files) - 10} autres")
    
    # 4. Demander confirmation
    print(f"\n📋 ÉTAPE 4: Ajout du bloc vidéo")
    print("Bloc vidéo à insérer:")
    print("─" * 50)
    print(get_video_block())
    print("─" * 50)
    
    # 5. Traiter tous les fichiers
    success_count = 0
    
    for filepath in html_files:
        # Créer une sauvegarde avant modification
        backup_file(filepath)
        
        if insert_video_block(filepath):
            success_count += 1
    
    # 6. Résumé final
    print("\n" + "=" * 70)
    print(f"🎉 MISE À JOUR TERMINÉE")
    print(f"📊 Résultats:")
    print(f"   ✅ index.html remplacé avec succès")
    print(f"   📸 Image poster: {'Créée' if not os.path.exists('/app/images/hero-poster.jpg') else 'Vérifiée'}")
    print(f"   🎬 Bloc vidéo ajouté: {success_count}/{len(html_files)} pages")
    
    if success_count == len(html_files):
        print(f"\n🌟 TOUTES LES PAGES ONT ÉTÉ MISES À JOUR AVEC SUCCÈS!")
        print(f"Le bloc vidéo background s'affichera maintenant sur toutes les pages du site.")
    else:
        failed = len(html_files) - success_count
        print(f"\n⚠️ {failed} page(s) n'ont pas pu être mises à jour")
    
    print(f"\n💡 RAPPEL:")
    print(f"   - CSS .video-background conservé intact")
    print(f"   - Aucune duplication de bloc existant")
    print(f"   - Image poster: images/hero-poster.jpg")
    print(f"   - Vidéo: https://res.cloudinary.com/ddulasmtz/video/upload/v1752950782/background-video.webm")

if __name__ == "__main__":
    main()