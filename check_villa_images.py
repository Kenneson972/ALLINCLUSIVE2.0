#!/usr/bin/env python3
"""
Script pour vérifier la validité de toutes les images des villas
"""

import os
import re
import json

def check_image_exists(image_path):
    """Vérifie si un fichier image existe"""
    # Convertir le chemin relatif en chemin absolu
    if image_path.startswith('./'):
        abs_path = '/app' + image_path[1:]  # Supprimer le . du début
    else:
        abs_path = '/app/' + image_path
    
    return os.path.exists(abs_path)

def extract_villa_images():
    """Extrait toutes les images des villas depuis index.html"""
    
    with open('/app/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Trouver la section des données des villas
    villa_pattern = r'const villasData = \[(.*?)\];'
    match = re.search(villa_pattern, content, re.DOTALL)
    
    if not match:
        print("❌ Impossible de trouver les données des villas")
        return
    
    # Extraire toutes les images
    image_pattern = r'image:\s*"([^"]+)"'
    gallery_pattern = r'gallery:\s*\[(.*?)\]'
    
    all_images = []
    
    # Images principales
    main_images = re.findall(image_pattern, match.group(1))
    all_images.extend(main_images)
    
    # Images de galerie
    gallery_matches = re.findall(gallery_pattern, match.group(1), re.DOTALL)
    for gallery_match in gallery_matches:
        # Extraire chaque image de la galerie
        gallery_images = re.findall(r'"([^"]+)"', gallery_match)
        all_images.extend(gallery_images)
    
    return list(set(all_images))  # Supprimer les doublons

def main():
    print("🔍 Vérification de la validité des images des villas")
    print("=" * 60)
    
    images = extract_villa_images()
    
    if not images:
        print("❌ Aucune image trouvée")
        return
    
    missing_images = []
    valid_images = []
    
    for image in images:
        if check_image_exists(image):
            valid_images.append(image)
        else:
            missing_images.append(image)
    
    print(f"📊 Résultats :")
    print(f"   • Images valides : {len(valid_images)}")
    print(f"   • Images manquantes : {len(missing_images)}")
    
    if missing_images:
        print(f"\n❌ Images manquantes à corriger :")
        for i, img in enumerate(missing_images, 1):
            print(f"   {i}. {img}")
            
        # Suggérer des corrections
        print(f"\n💡 Suggestions de correction :")
        for img in missing_images:
            # Essayer de trouver des alternatives
            folder = os.path.dirname(img.replace('./', '/app/'))
            if os.path.exists(folder):
                available_images = [f for f in os.listdir(folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
                if available_images:
                    print(f"   {img} → Utiliser : {available_images[0]}")
                else:
                    print(f"   {img} → Aucune image disponible dans le dossier")
            else:
                print(f"   {img} → Dossier inexistant")
    else:
        print(f"\n✅ Toutes les images sont valides !")

if __name__ == "__main__":
    main()