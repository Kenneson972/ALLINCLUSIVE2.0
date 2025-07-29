#!/usr/bin/env python3
"""
Création SIMPLE des 21 vraies villas - Version corrigée
"""

import os
import csv
import re

def get_villa_images(villa_name):
    """Récupère les vraies images d'une villa"""
    
    name_to_folder = {
        'Villa F3 sur Petit Macabou': 'Villa_F3_Petit_Macabou',
        'Villa F3 POUR LA BACCHA': 'Villa_F3_Baccha_Petit_Macabou',
        'Villa F3 sur le François': 'Villa_F3_Le_Francois',
        'Villa F5 sur Ste Anne': 'Villa_F5_Ste_Anne', 
        'Villa F6 au Lamentin': 'Villa_F6_Lamentin',
        'Villa F6 sur Ste Luce à 1mn de la plage': 'Villa_F6_Ste_Luce_Plage',
        'Villa F3 Bas de villa Trinité Cosmy': 'Villa_F3_Trinite_Cosmy',
        'Bas de villa F3 sur le Robert': 'Villa_F3_Robert_Pointe_Hyacinthe',
        'Appartement F3 Trenelle (Location Annuelle)': 'Villa_F3_Trenelle_Location_Annuelle',
        'Villa F5 Vauclin Ravine Plate': 'Villa_F5_Vauclin_Ravine_Plate',
        'Villa F5 La Renée': 'Villa_F5_R_Pilote_La_Renee',
        'Villa F7 Baie des Mulets': 'Villa_F7_Baie_des_Mulets_Vauclin',
        'Bas de villa F3 sur Ste Luce': 'Bas_Villa_F3_Ste_Luce',
        'Studio Cocooning Lamentin': 'Studio_Cocooning_Lamentin',
        'Villa Fête Journée Ducos': 'Villa_Fete_Journee_Ducos',
        'Villa Fête Journée Fort de France': 'Villa_Fete_Journee_Fort_de_France',
        'Villa Fête Journée Rivière-Pilote': 'Villa_Fete_Journee_R_Pilote',
        'Villa Fête Journée Rivière Salée': 'Villa_Fete_Journee_Riviere_Salee',
        'Villa Fête Journée Sainte-Luce': 'Villa_Fete_Journee_Sainte_Luce',
        'Espace Piscine Journée Bungalow': 'Espace_Piscine_Journee_Bungalow',
        'Villa F6 sur Petit Macabou (séjour + fête)': 'Villa_F6_Petit_Macabou'
    }
    
    folder = name_to_folder.get(villa_name, '')
    if not folder:
        return []
    
    image_path = f"/app/images/{folder}"
    images = []
    
    if os.path.exists(image_path):
        for file in sorted(os.listdir(image_path)):
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                images.append(f"./images/{folder}/{file}")
    
    return images

def create_simple_villa(villa_name, localisation, villa_type, capacity, tarif, services, description):
    """Crée une page villa simple mais complète"""
    
    # ID de fichier
    villa_id = villa_name.lower().replace(' ', '-').replace('villa-', '').replace('(', '').replace(')', '').replace('à', 'a')
    villa_id = re.sub(r'[^a-z0-9-]', '', villa_id)
    villa_id = f"villa-{villa_id}"
    
    # Prix de base
    price_match = re.search(r'(\d+)€', tarif)
    base_price = price_match.group(1) if price_match else '500'
    
    # Images réelles
    images = get_villa_images(villa_name)
    if not images:
        images = ["https://images.unsplash.com/photo-1564013799919-ab600027ffc6?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80"]
    
    # Galerie Swiper
    gallery_slides = ""
    for i, img in enumerate(images):
        gallery_slides += f'<div class="swiper-slide"><img src="{img}" alt="{villa_name} - Image {i+1}" loading="lazy"></div>'
    
    # Thumbnails
    gallery_thumbnails = ""
    for i, img in enumerate(images):
        active = "active" if i == 0 else ""
        gallery_thumbnails += f'<img src="{img}" alt="Thumbnail {i+1}" class="w-20 h-15 object-cover rounded cursor-pointer {active}" onclick="swiper.slideToLoop({i})">'
    
    html_content = f'''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{villa_name} - {localisation} | KhanelConcept</title>
    
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.tailwindcss.com"></script>
    
    <style>
        body {{ 
            font-family: 'Inter', sans-serif; 
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); 
            color: white; 
            position: relative;
        }}
        
        .video-background {{ 
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -2; overflow: hidden; 
        }}
        .video-background video {{ 
            width: 100%; height: 100%; object-fit: cover; opacity: 0.8; 
        }}
        .video-overlay {{ 
            position: absolute; top: 0; left: 0; width: 100%; height: 100%; 
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.7) 0%, rgba(30, 41, 59, 0.7) 100%); 
        }}
        
        .glass-card {{ 
            background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(20px); 
            border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 20px; 
        }}
        
        .info-card {{ 
            background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); 
            border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 15px; 
            padding: 2rem; margin-bottom: 1.5rem; transition: all 0.3s ease; 
        }}
        
        .glass-header {{ 
            background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(20px); 
            border-bottom: 1px solid rgba(255, 255, 255, 0.2); position: fixed; 
            top: 0; left: 0; right: 0; z-index: 1000; padding: 1rem 2rem; 
        }}
        
        .villa-gallery {{ border-radius: 20px; overflow: hidden; height: 500px; }}
        .villa-gallery .swiper-slide img {{ width: 100%; height: 500px; object-fit: cover; }}
        
        .gallery-thumbnails {{ 
            background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 0 0 20px 20px; 
            display: flex; gap: 1rem; overflow-x: auto; 
        }}
        
        .btn-primary {{ 
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%); color: white; 
            padding: 1rem 2rem; border-radius: 12px; font-weight: 600; text-decoration: none;
            display: inline-flex; align-items: center; gap: 0.5rem; 
        }}
        
        .btn-secondary {{ 
            background: rgba(255, 255, 255, 0.1); color: white; padding: 1rem 1.5rem; 
            border-radius: 12px; text-decoration: none; display: inline-flex; 
            align-items: center; gap: 0.5rem; border: 1px solid rgba(255, 255, 255, 0.2); 
        }}
        
        @media (max-width: 768px) {{ 
            .villa-gallery {{ height: 300px; }}
            .villa-gallery .swiper-slide img {{ height: 300px; }}
        }}
    </style>
</head>

<body>
    <!-- Background Video -->
    <div class="video-background">
        <video id="backgroundVideo" autoplay muted loop playsinline preload="metadata" webkit-playsinline>
            <source src="https://res.cloudinary.com/dqz8rw6m2/video/upload/v1733669700/martinique-bg_d0pzjm.mp4" type="video/mp4">
        </video>
        <div class="video-overlay"></div>
    </div>
    
    <!-- Navigation -->
    <header class="glass-header">
        <nav class="flex justify-between items-center max-w-7xl mx-auto">
            <a href="./index.html" class="text-xl font-bold text-yellow-600">🏝️ KhanelConcept</a>
            <div class="flex space-x-6">
                <a href="./index.html" class="text-white hover:text-yellow-400">Nos Villas</a>
                <a href="./reservation.html" class="text-white hover:text-yellow-400">Réserver</a>
                <a href="./login.html" class="text-white hover:text-yellow-400">Connexion</a>
            </div>
        </nav>
    </header>

    <main class="container mx-auto px-6 py-12 mt-20">
        <!-- Title -->
        <section class="text-center mb-12">
            <h1 class="text-5xl font-bold mb-4 bg-gradient-to-r from-white to-yellow-400 bg-clip-text text-transparent">
                {villa_name}
            </h1>
            <p class="text-xl text-gray-300 mb-4">
                <i class="fas fa-map-marker-alt text-red-400 mr-2"></i>{localisation}
            </p>
            <div class="flex justify-center items-center gap-6 text-lg flex-wrap">
                <span class="bg-blue-600/30 px-4 py-2 rounded-full">
                    <i class="fas fa-users mr-2"></i>{capacity}
                </span>
                <span class="bg-green-600/30 px-4 py-2 rounded-full">
                    <i class="fas fa-tag mr-2"></i>À partir de {base_price}€
                </span>
                <span class="bg-purple-600/30 px-4 py-2 rounded-full">
                    <i class="fas fa-home mr-2"></i>{villa_type}
                </span>
            </div>
        </section>
        
        <!-- Gallery -->
        <section class="mb-16">
            <div class="max-w-6xl mx-auto">
                <div class="swiper villa-gallery mb-0">
                    <div class="swiper-wrapper">{gallery_slides}</div>
                    <div class="swiper-pagination"></div>
                    <div class="swiper-button-next"></div>
                    <div class="swiper-button-prev"></div>
                </div>
                <div class="gallery-thumbnails">{gallery_thumbnails}</div>
            </div>
        </section>

        <!-- Content -->
        <div class="grid lg:grid-cols-3 gap-12">
            <div class="lg:col-span-2">
                <div class="info-card">
                    <h2 class="text-3xl font-bold mb-6 text-blue-400">
                        <i class="fas fa-info-circle mr-3"></i>Description
                    </h2>
                    <div class="text-gray-200 mb-6">{description}</div>
                    
                    <div class="mt-8 p-6 bg-gradient-to-r from-blue-600/20 to-purple-600/20 rounded-2xl">
                        <h3 class="text-2xl font-bold mb-4 text-yellow-400">
                            <i class="fas fa-euro-sign mr-2"></i>Tarification
                        </h3>
                        <div class="text-gray-200 whitespace-pre-line">{tarif}</div>
                    </div>
                    
                    <div class="mt-8 flex flex-wrap gap-4">
                        <a href="./reservation.html?villa={villa_id}" class="btn-primary">
                            <i class="fas fa-calendar-check"></i>Réserver
                        </a>
                        <a href="./index.html" class="btn-secondary">
                            <i class="fas fa-arrow-left"></i>Retour
                        </a>
                    </div>
                </div>
            </div>
            
            <div>
                <div class="info-card">
                    <h3 class="text-2xl font-bold mb-6 text-yellow-500">
                        <i class="fas fa-star mr-3"></i>Services & Équipements
                    </h3>
                    <div class="text-gray-200 whitespace-pre-line">{services}</div>
                </div>
            </div>
        </div>
    </main>

    <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
    <script>
        // Video background
        function initVideoBackground() {{
            const video = document.getElementById('backgroundVideo');
            if (video) {{
                console.log('🎥 Démarrage vidéo background');
                video.play().catch(e => console.log('Vidéo autoplay bloqué'));
            }}
        }}

        // Swiper
        const swiper = new Swiper('.villa-gallery', {{
            loop: true,
            autoplay: {{ delay: 5000 }},
            pagination: {{ el: '.swiper-pagination', clickable: true }},
            navigation: {{ nextEl: '.swiper-button-next', prevEl: '.swiper-button-prev' }},
            effect: 'fade'
        }});

        document.addEventListener('DOMContentLoaded', initVideoBackground);
        
        window.currentVilla = {{
            id: '{villa_id}',
            name: '{villa_name}',
            basePrice: {base_price}
        }};
    </script>
</body>
</html>'''
    
    return villa_id, html_content

def main():
    print("🏠 CRÉATION SIMPLE DES 21 VRAIES VILLAS")
    print("=" * 50)
    
    csv_file = '/app/Catalogue_Villas_Khanel_Concept_Complet_Final.csv'
    created_villas = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for i, row in enumerate(reader, 1):
            villa_name = row.get('Nom de la Villa', '').strip()
            if villa_name and i <= 21:
                try:
                    localisation = row.get('Localisation', '').strip()
                    villa_type = row.get('Type (F3, F5, etc.)', '').strip()
                    capacity = row.get('Capacité (personnes)', '').strip()
                    tarif = row.get('Tarif', '').strip()
                    services = row.get('Options/Services', '').strip()
                    description = row.get('Description', '').strip()
                    
                    villa_id, html_content = create_simple_villa(
                        villa_name, localisation, villa_type, capacity, 
                        tarif, services, description
                    )
                    
                    filename = f"/app/{villa_id}.html"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    
                    created_villas.append(villa_name)
                    print(f"✅ Villa {i}: {villa_id}.html - {villa_name}")
                    
                except Exception as e:
                    print(f"❌ Erreur Villa {i}: {str(e)}")
    
    print(f"\n🎉 TERMINÉ: {len(created_villas)}/21 villas créées !")

if __name__ == "__main__":
    main()