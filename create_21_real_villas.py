#!/usr/bin/env python3
"""
Création des 21 VRAIES villas selon le CSV avec les VRAIES photos
Fini l'embrouille, on fait ça proprement !
"""

import os
import csv
import re
from pathlib import Path

def get_villa_images(villa_name):
    """Récupère les vraies images d'une villa"""
    
    # Mapping exact des noms avec leurs dossiers d'images
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
    
    folder = name_to_folder.get(villa_name)
    if not folder:
        print(f"❌ Pas de mapping pour: {villa_name}")
        return []
    
    image_path = f"/app/images/{folder}"
    images = []
    
    if os.path.exists(image_path):
        for file in sorted(os.listdir(image_path)):
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                images.append(f"./images/{folder}/{file}")
    
    print(f"✅ {villa_name}: {len(images)} images trouvées")
    return images

def create_villa_html(villa_data):
    """Crée le HTML d'une villa avec vraies photos et vidéo background"""
    
    villa_name = villa_data['Nom de la Villa'].strip()
    localisation = villa_data['Localisation'].strip()
    villa_type = villa_data['Type (F3, F5, etc.)'].strip()
    capacity = villa_data['Capacité (personnes)'].strip()
    tarif = villa_data['Tarif'].strip()
    services = villa_data['Options/Services'].strip()
    description = villa_data['Description'].strip()
    
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
        gallery_slides += f'''
        <div class="swiper-slide">
            <img src="{img}" alt="{villa_name} - Image {i+1}" loading="lazy">
        </div>'''
    
    # Thumbnails
    gallery_thumbnails = ""
    for i, img in enumerate(images):
        active = "active" if i == 0 else ""
        gallery_thumbnails += f'''
        <img src="{img}" alt="Thumbnail {i+1}" class="w-20 h-15 object-cover rounded cursor-pointer {active}" onclick="swiper.slideToLoop({i}); updateActiveThumbnail({i})">'''
    
    # HTML complet
    html_content = f'''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{villa_name} - {localisation} | KhanelConcept Martinique</title>
    <meta name="description" content="{villa_name} à {localisation} - Villa de luxe {capacity}. Prix à partir de {base_price}€. Réservation en ligne sécurisée.">
    
    <!-- Swiper CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css">
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- AOS Animation -->
    <link rel="stylesheet" href="https://unpkg.com/aos@2.3.1/dist/aos.css">
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <style>
        :root {{
            --primary-blue: #1e40af;
            --primary-gold: #d97706;
            --glass-bg: rgba(255, 255, 255, 0.1);
            --glass-border: rgba(255, 255, 255, 0.2);
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            min-height: 100vh;
            color: white;
            position: relative;
        }}
        
        /* Video Background */
        .video-background {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -2;
            overflow: hidden;
        }}
        
        .video-background video {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            opacity: 0.8;
        }}
        
        .video-overlay {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.7) 0%, rgba(30, 41, 59, 0.7) 100%);
        }}
        
        /* Glassmorphism Components */
        .glass-card {{
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}
        
        .info-card {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            transition: all 0.3s ease;
        }}
        
        .info-card:hover {{
            background: rgba(255, 255, 255, 0.1);
            transform: translateY(-2px);
        }}
        
        /* Header */
        .glass-header {{
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--glass-border);
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            padding: 1rem 2rem;
        }}
        
        .nav-brand {{
            font-size: 1.5rem;
            font-weight: bold;
            color: var(--primary-gold);
            text-decoration: none;
        }}
        
        .nav-link {{
            color: white;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s ease;
        }}
        
        .nav-link:hover {{
            color: var(--primary-gold);
        }}
        
        /* Gallery */
        .villa-gallery {{
            border-radius: 20px;
            overflow: hidden;
            height: 500px;
        }}
        
        .villa-gallery .swiper-slide img {{
            width: 100%;
            height: 500px;
            object-fit: cover;
        }}
        
        .gallery-thumbnails {{
            background: rgba(255, 255, 255, 0.1);
            padding: 1rem;
            border-radius: 0 0 20px 20px;
            display: flex;
            gap: 1rem;
            overflow-x: auto;
        }}
        
        .gallery-thumbnails img {{
            min-width: 80px;
            height: 60px;
            opacity: 0.6;
            border: 2px solid transparent;
            transition: all 0.3s ease;
        }}
        
        .gallery-thumbnails img.active {{
            opacity: 1;
            border-color: var(--primary-gold);
        }}
        
        /* Buttons */
        .btn-primary {{
            background: linear-gradient(135deg, var(--primary-blue) 0%, #3b82f6 100%);
            color: white;
            padding: 1rem 2rem;
            border-radius: 12px;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.3s ease;
            text-decoration: none;
        }}
        
        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(59, 130, 246, 0.4);
        }}
        
        .btn-secondary {{
            background: rgba(255, 255, 255, 0.1);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            font-weight: 500;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.3s ease;
            text-decoration: none;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .btn-secondary:hover {{
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
        }}
        
        @media (max-width: 768px) {{
            .villa-gallery {{
                height: 300px;
            }}
            
            .villa-gallery .swiper-slide img {{
                height: 300px;
            }}
        }}
    </style>
</head>

<body data-aos-easing="ease" data-aos-duration="1000" data-aos-delay="0">
    <!-- Background Video -->
    <div class="video-background">
        <video id="backgroundVideo" autoplay muted loop playsinline preload="metadata" webkit-playsinline>
            <source src="https://res.cloudinary.com/dqz8rw6m2/video/upload/v1733669700/martinique-bg_d0pzjm.mp4" type="video/mp4">
            Votre navigateur ne supporte pas la lecture de vidéos HTML5.
        </video>
        <div class="video-overlay"></div>
    </div>
    
    <!-- Navigation -->
    <header class="glass-header">
        <nav class="flex justify-between items-center max-w-7xl mx-auto">
            <a href="./index.html" class="nav-brand">🏝️ KhanelConcept</a>
            <div class="flex space-x-8">
                <a href="./index.html" class="nav-link">Nos Villas</a>
                <a href="./reservation.html" class="nav-link">Réserver</a>
                <a href="./login.html" class="nav-link">Connexion</a>
            </div>
        </nav>
    </header>

    <!-- Main Content -->
    <main class="container mx-auto px-6 py-12 mt-20">
        
        <!-- Villa Title -->
        <section class="text-center mb-12" data-aos="fade-up">
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
        
        <!-- Gallery Section -->
        <section class="mb-16" data-aos="fade-up">
            <div class="max-w-6xl mx-auto">
                <!-- Main Swiper Gallery -->
                <div class="swiper villa-gallery mb-0">
                    <div class="swiper-wrapper">{gallery_slides}
                    </div>
                    <div class="swiper-pagination"></div>
                    <div class="swiper-button-next"></div>
                    <div class="swiper-button-prev"></div>
                </div>
                
                <!-- Thumbnails -->
                <div class="gallery-thumbnails">{gallery_thumbnails}
                </div>
            </div>
        </section>

        <!-- Description & Details -->
        <div class="grid lg:grid-cols-3 gap-12 mb-16">
            <!-- Description -->
            <div class="lg:col-span-2" data-aos="fade-up" data-aos-delay="300">
                <div class="info-card">
                    <h2 class="text-3xl font-bold mb-6 flex items-center">
                        <i class="fas fa-info-circle text-blue-600 mr-3"></i>
                        Description de la villa
                    </h2>
                    <div class="prose prose-lg max-w-none text-gray-200 mb-6">
                        {description}
                    </div>
                    
                    <!-- Pricing Info -->
                    <div class="mt-8 p-6 bg-gradient-to-r from-blue-600/20 to-purple-600/20 rounded-2xl border border-blue-400/30">
                        <h3 class="text-2xl font-bold mb-4 text-yellow-400">
                            <i class="fas fa-euro-sign mr-2"></i>Tarification
                        </h3>
                        <div class="text-gray-200 whitespace-pre-line">
                            {tarif}
                        </div>
                    </div>
                    
                    <!-- Action Buttons -->
                    <div class="mt-8 flex flex-wrap gap-4">
                        <a href="./reservation.html?villa={villa_id}" class="btn-primary">
                            <i class="fas fa-calendar-check"></i>
                            Réserver maintenant
                        </a>
                        <a href="./index.html" class="btn-secondary">
                            <i class="fas fa-arrow-left"></i>
                            Voir toutes les villas
                        </a>
                        <button class="btn-secondary" onclick="window.print()">
                            <i class="fas fa-print"></i>
                            Imprimer
                        </button>
                    </div>
                </div>
            </div>
            
            <!-- Amenities -->
            <div data-aos="fade-up" data-aos-delay="400">
                <div class="info-card">
                    <h3 class="text-2xl font-bold mb-6 flex items-center">
                        <i class="fas fa-star text-yellow-500 mr-3"></i>
                        Équipements & Services
                    </h3>
                    <div class="text-gray-200 whitespace-pre-line">
                        {services}
                    </div>
                </div>
            </div>
        </div>
    </main>

    <!-- Scripts -->
    <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
    
    <script>
        // Initialize AOS
        AOS.init({{
            duration: 1000,
            once: true
        }});

        // Initialize video background
        function initVideoBackground() {{
            const video = document.getElementById('backgroundVideo');
            if (video) {{
                console.log('🎥 Initialisation vidéo background');
                video.muted = true;
                video.loop = true;
                video.autoplay = true;
                video.setAttribute('playsinline', '');
                video.setAttribute('webkit-playsinline', '');
                
                const playPromise = video.play();
                if (playPromise !== undefined) {{
                    playPromise.then(() => {{
                        console.log('✅ Vidéo background démarrée');
                        video.style.opacity = '1';
                    }}).catch(error => {{
                        console.log('⚠️ Autoplay bloqué:', error);
                    }});
                }}
                
                // Support mobile
                if (/iPad|iPhone|iPod|Android/i.test(navigator.userAgent)) {{
                    document.addEventListener('touchstart', function() {{
                        video.play().catch(console.log);
                    }}, {{ once: true }});
                }}
            }}
        }}

        // Swiper Gallery
        const swiper = new Swiper('.villa-gallery', {{
            loop: true,
            autoplay: {{
                delay: 5000,
                disableOnInteraction: false,
            }},
            pagination: {{
                el: '.swiper-pagination',
                clickable: true,
            }},
            navigation: {{
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            }},
            effect: 'fade',
            fadeEffect: {{
                crossFade: true
            }}
        }});

        // Update active thumbnail
        function updateActiveThumbnail(index) {{
            const thumbnails = document.querySelectorAll('.gallery-thumbnails img');
            thumbnails.forEach(t => t.classList.remove('active'));
            if (thumbnails[index]) {{
                thumbnails[index].classList.add('active');
            }}
        }}

        // Swiper slide change event
        swiper.on('slideChange', () => {{
            const realIndex = swiper.realIndex;
            updateActiveThumbnail(realIndex);
        }});

        // Initialize on page load
        document.addEventListener('DOMContentLoaded', () => {{
            initVideoBackground();
        }});

        // Villa data for reservation
        window.currentVilla = {{
            id: '{villa_id}',
            name: '{villa_name}',
            basePrice: {base_price},
            capacity: '{capacity}',
            location: '{localisation}'
        }};
    </script>
</body>
</html>'''
    
    return villa_id, html_content

def main():
    print("🏠 CRÉATION DES 21 VRAIES VILLAS")
    print("Avec vraies photos et vidéo background qui fonctionne !")
    print("=" * 60)
    
    # Lire le CSV
    csv_file = '/app/Catalogue_Villas_Khanel_Concept_Complet_Final.csv'
    created_villas = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for i, row in enumerate(reader, 1):
            villa_name = row.get('Nom de la Villa', '').strip()
            if villa_name:
                try:
                    villa_id, html_content = create_villa_html(row)
                    
                    # Écrire le fichier
                    filename = f"/app/{villa_id}.html"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    
                    created_villas.append({{
                        'id': villa_id,
                        'name': villa_name,
                        'file': filename
                    }})
                    
                    print(f"✅ Villa {i}: {villa_id}.html - {villa_name}")
                    
                except Exception as e:
                    print(f"❌ Erreur Villa {i} ({villa_name}): {str(e)}")
            
            # Arrêter après 21 villas
            if i >= 21:
                break
    
    print("\n" + "=" * 60)
    print(f"🎉 TERMINÉ: {len(created_villas)}/21 villas créées avec VRAIES PHOTOS !")
    
    # Vérification
    print("\nVillas créées:")
    for villa in created_villas:
        print(f"  • {villa['file']} - {villa['name']}")

if __name__ == "__main__":
    main()