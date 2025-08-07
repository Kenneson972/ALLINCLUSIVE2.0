#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour analyser l'index.html fonctionnel remis par l'utilisateur
et appliquer SEULEMENT les corrections nécessaires aux autres pages HTML
en respectant exactement la même structure qui fonctionne
"""

import os
import re
from datetime import datetime

def backup_file(filepath):
    """Créer une sauvegarde d'un fichier"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.basename(filepath)
    name, ext = os.path.splitext(filename)
    backup_name = f"{name}_backup_correct_{timestamp}{ext}"
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

def analyze_working_index():
    """Analyser l'index.html qui fonctionne pour extraire les patterns corrects"""
    print("🔍 Analyse de l'index.html fonctionnel...")
    
    try:
        with open('/app/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        patterns = {
            'video_structure': None,
            'asset_paths': [],
            'css_structure': None
        }
        
        # Extraire la structure vidéo qui fonctionne
        video_match = re.search(r'<!-- Vidéo Optimisée avec Support Moderne -->.*?</video>', content, re.DOTALL)
        if video_match:
            patterns['video_structure'] = video_match.group(0)
            print("✅ Structure vidéo trouvée")
        
        # Analyser les chemins d'assets qui fonctionnent
        asset_patterns = re.findall(r'(?:src|href)="([^"]*(?:images|videos|assets)[^"]*)"', content)
        patterns['asset_paths'] = asset_patterns
        print(f"✅ {len(asset_patterns)} chemins d'assets analysés")
        
        # Analyser les chemins utilisés
        relative_paths = [p for p in asset_patterns if not p.startswith('http') and not p.startswith('/')]
        absolute_paths = [p for p in asset_patterns if p.startswith('/')]
        
        print(f"   - Chemins relatifs (corrects): {len(relative_paths)}")
        print(f"   - Chemins absolus (à corriger): {len(absolute_paths)}")
        
        if relative_paths:
            print(f"   - Exemple chemin correct: {relative_paths[0]}")
        
        return patterns
        
    except Exception as e:
        print(f"❌ Erreur analyse index.html: {e}")
        return None

def fix_paths_like_index(content):
    """
    Corriger les chemins d'assets pour qu'ils soient comme dans l'index fonctionnel
    SEULEMENT les corrections de chemins, pas de modification de structure
    """
    print("🔧 Correction des chemins d'assets...")
    
    original_content = content
    corrections = 0
    
    # 1. Corriger SEULEMENT les chemins qui commencent par /
    # Remplacer src="/images/ par src="images/
    if 'src="/images/' in content:
        content = re.sub(r'src="/images/', 'src="images/', content)
        corrections += content.count('src="images/') - original_content.count('src="images/')
        
    if 'href="/images/' in content:
        content = re.sub(r'href="/images/', 'href="images/', content)
        corrections += 1
        
    if 'src="/videos/' in content:
        content = re.sub(r'src="/videos/', 'src="videos/', content)
        corrections += 1
        
    if 'href="/videos/' in content:
        content = re.sub(r'href="/videos/', 'href="videos/', content)
        corrections += 1
        
    if 'src="/assets/' in content:
        content = re.sub(r'src="/assets/', 'src="assets/', content)
        corrections += 1
        
    if 'href="/assets/' in content:
        content = re.sub(r'href="/assets/', 'href="assets/', content)
        corrections += 1
    
    # 2. Corriger aussi les chemins dans le CSS inline
    if "url('/images/" in content:
        content = re.sub(r"url\('/images/", "url('images/", content)
        corrections += 1
        
    if "url('/videos/" in content:
        content = re.sub(r"url\('/videos/", "url('videos/", content)
        corrections += 1
        
    if "url('/assets/" in content:
        content = re.sub(r"url\('/assets/", "url('assets/", content)
        corrections += 1
    
    print(f"   - {corrections} corrections de chemins appliquées")
    return content

def fix_video_paths_minimal(content):
    """
    Corriger SEULEMENT les chemins vidéo cassés pour pointer vers des chemins relatifs
    comme dans l'index fonctionnel
    """
    print("🎬 Correction des chemins vidéo...")
    
    corrections = 0
    
    # Si on trouve des URLs Cloudinary cassées, les remplacer par les chemins relatifs corrects
    if 'cloudinary.com' in content and 'martinique-villa-hero' in content:
        # Remplacer par la structure exacte qui fonctionne dans index.html
        content = re.sub(
            r'src="https://[^"]*cloudinary[^"]*martinique-villa-hero\.webm"',
            'src="videos/martinique-villa-hero.webm"',
            content
        )
        content = re.sub(
            r'src="https://[^"]*cloudinary[^"]*martinique-villa-hero\.mp4"',
            'src="videos/martinique-villa-hero.mp4"',
            content
        )
        corrections += 2
        
    # Corriger les posters aussi
    if 'cloudinary.com' in content and 'hero-poster' in content:
        content = re.sub(
            r'poster="https://[^"]*cloudinary[^"]*hero-poster[^"]*"',
            'poster="images/hero-poster.jpg"',
            content
        )
        corrections += 1
    
    if corrections > 0:
        print(f"   - {corrections} chemins vidéo corrigés")
    else:
        print("   - Aucune correction vidéo nécessaire")
        
    return content

def minimal_fix_file(filepath):
    """
    Appliquer SEULEMENT les corrections minimales nécessaires
    pour que le fichier fonctionne comme l'index
    """
    print(f"\n🔧 Correction minimale: {os.path.basename(filepath)}")
    
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
        
        original_size = len(content)
        
        # Appliquer SEULEMENT les corrections nécessaires
        content = fix_paths_like_index(content)
        content = fix_video_paths_minimal(content)
        
        # Vérifier qu'on n'a pas cassé le fichier
        if len(content) < original_size * 0.9:
            print(f"⚠️ Fichier trop réduit, annulation pour {filepath}")
            return False
        
        # Sauvegarder
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {os.path.basename(filepath)} corrigé")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    print("🚀 CORRECTION MINIMALE DES PAGES HTML")
    print("Basée sur l'analyse de l'index.html fonctionnel remis par l'utilisateur")
    print("=" * 70)
    
    # 1. Analyser l'index fonctionnel
    patterns = analyze_working_index()
    if not patterns:
        print("❌ Impossible d'analyser l'index.html")
        return
    
    print("\n📋 STRATÉGIE DE CORRECTION:")
    print("- Corriger SEULEMENT les chemins d'assets (/ vers chemins relatifs)")
    print("- Corriger les URLs vidéo cassées vers chemins relatifs")
    print("- PRÉSERVER toute la structure existante")
    print("- Aucune modification majeure du code")
    
    # 2. Liste des fichiers à corriger avec prudence
    files_to_fix = [
        '/app/reservation.html',
        '/app/villa-villa-f3-sur-petit-macabou.html'
    ]
    
    # Ajouter quelques autres villas importantes si elles existent
    other_villas = [
        '/app/villa-villa-f5-sur-ste-anne.html',
        '/app/villa-villa-f6-au-lamentin.html'
    ]
    
    for villa in other_villas:
        if os.path.exists(villa):
            files_to_fix.append(villa)
    
    print(f"\n🎯 Fichiers à corriger: {len(files_to_fix)}")
    for f in files_to_fix:
        print(f"   - {os.path.basename(f)}")
    
    # 3. Appliquer les corrections minimales
    success_count = 0
    
    for filepath in files_to_fix:
        if minimal_fix_file(filepath):
            success_count += 1
    
    # 4. Résumé
    print("\n" + "=" * 70)
    print(f"🎉 CORRECTIONS TERMINÉES: {success_count}/{len(files_to_fix)} fichiers")
    
    if success_count == len(files_to_fix):
        print("\n✅ TOUTES LES PAGES CORRIGÉES AVEC SUCCÈS")
        print("📋 Corrections appliquées:")
        print("   - Chemins d'assets corrigés (/ vers relatifs)")
        print("   - Chemins vidéo normalisés")
        print("   - Structure originale préservée")
        print("\n🌐 Les pages devraient maintenant fonctionner comme l'index.html")
    else:
        failed = len(files_to_fix) - success_count
        print(f"\n⚠️ {failed} fichier(s) non corrigé(s)")
    
    print("\n💡 NOTE: L'index.html original a été préservé intact")

if __name__ == "__main__":
    main()