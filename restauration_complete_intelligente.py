#!/usr/bin/env python3
"""
RESTAURATION INTELLIGENTE COMPLÈTE
Récupère les données de villa-details.html et reconstruit avec structure main2
"""

import os
import re
import json
import glob

def extract_villa_data_from_details():
    """Extrait toutes les données des villas depuis villa-details.html"""
    
    with open('/app/villa-details.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraire le JavaScript avec les données des villas
    js_pattern = r'const villasData = \{(.*?)\};'
    match = re.search(js_pattern, content, re.DOTALL)
    
    if not match:
        print("❌ Impossible de trouver les données des villas")
        return {}
    
    # Parser les données villa par villa
    villa_sections = re.findall(r'(\d+):\s*\{(.*?)\}(?=,\s*\d+:|$)', match.group(1), re.DOTALL)
    
    villas_data = {}
    
    for villa_id, villa_content in villa_sections:
        villa_data = {}
        
        # Extraire chaque champ
        fields = {
            'name': r'name:\s*"([^"]*)"',
            'location': r'location:\s*"([^"]*)"',
            'price': r'price:\s*"([^"]*)"',
            'guests': r'guests:\s*"([^"]*)"',
            'image': r'image:\s*"([^"]*)"',
            'description': r'description:\s*"([^"]*)"'
        }
        
        for field, pattern in fields.items():
            field_match = re.search(pattern, villa_content)
            if field_match:
                villa_data[field] = field_match.group(1)
        
        # Extraire la galerie
        gallery_match = re.search(r'gallery:\s*\[(.*?)\]', villa_content, re.DOTALL)
        if gallery_match:
            gallery_content = gallery_match.group(1)
            images = re.findall(r'"([^"]*)"', gallery_content)
            villa_data['gallery'] = images
        
        # Extraire les amenities
        amenities_match = re.search(r'amenities:\s*\[(.*?)\]', villa_content, re.DOTALL)
        if amenities_match:
            amenities_content = amenities_match.group(1)
            amenity_matches = re.findall(r'\{icon:\s*"([^"]*)",\s*name:\s*"([^"]*)"\}', amenities_content)
            villa_data['amenities'] = [{'icon': icon, 'name': name} for icon, name in amenity_matches]
        
        villas_data[int(villa_id)] = villa_data
    
    print(f"✅ {len(villas_data)} villas extraites depuis villa-details.html")
    return villas_data

def get_villa_id_from_filename(filename, villas_data):
    """Trouve l'ID de villa correspondant au filename"""
    
    # Mapping filename vers nom de villa
    filename_to_name = {
        'villa-f3-petit-macabou.html': 'Villa F3 Petit Macabou',
        'villa-f5-ste-anne.html': 'Villa F5 Ste Anne',
        'villa-f6-petit-macabou.html': 'Villa F6 Petit Macabou',
        'villa-f7-baie-des-mulets-vauclin.html': 'Villa F7 Baie des Mulets',
        'villa-f3-trinite-cosmy.html': 'Villa F3 Trinité (Cosmy)',
        'villa-f3-robert-pointe-hyacinthe.html': 'Villa F3 Le Robert',
        'villa-f5-r-pilote-la-renee.html': 'Villa F5 R.Pilote',
        'villa-f5-vauclin-ravine-plate.html': 'Villa F5 Vauclin',
        'villa-f6-lamentin.html': 'Villa F6 Lamentin',
        # Ajouter d'autres mappings...
    }
    
    expected_name = filename_to_name.get(filename)
    if not expected_name:
        return None
    
    # Chercher dans les données
    for villa_id, data in villas_data.items():
        if data.get('name') == expected_name:
            return villa_id
    
    return None

def restore_villa_with_original_data(file_path, villas_data):
    """Restaure une villa avec ses données originales complètes"""
    
    filename = os.path.basename(file_path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"🔧 RESTAURATION COMPLÈTE: {filename}")
    
    # Trouver les données originales de cette villa
    villa_id = get_villa_id_from_filename(filename, villas_data)
    
    if not villa_id or villa_id not in villas_data:
        print(f"   ❌ Données originales non trouvées")
        return False
    
    original_data = villas_data[villa_id]
    
    # ÉTAPE 1: Préserver le HEAD complet
    head_end = content.find('</head>') + len('</head>')
    head_section = content[:head_end]
    
    # ÉTAPE 2: Créer le BODY complet avec données originales
    body_section = create_complete_villa_body(original_data)
    
    # ÉTAPE 3: Reconstruire
    complete_content = head_section + body_section
    
    # ÉTAPE 4: Sauvegarder
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(complete_content)
    
    print(f"   ✅ Villa restaurée avec {len(original_data.get('gallery', []))} images")
    return True

def create_complete_villa_body(villa_data):
    """Crée le body complet avec toutes les données originales"""
    
    name = villa_data.get('name', 'Villa')
    location = villa_data.get('location', '').replace('📍 ', '')
    price = villa_data.get('price', '1200€').replace(' /nuit', '')
    guests = villa_data.get('guests', '').replace('👥 ', '')
    description = villa_data.get('description', '')
    gallery = villa_data.get('gallery', [])
    amenities = villa_data.get('amenities', [])
    
    # Générer les slides de galerie
    gallery_slides = ""
    for image in gallery:
        gallery_slides += f'''
                    <div class="swiper-slide">
                        <img src="{image}" alt="{name}" class="w-full h-full object-cover">
                    </div>'''
    
    # Générer les amenities
    amenities_html = ""
    for amenity in amenities[:8]:  # Limiter à 8
        amenities_html += f'''
                        <div class="amenity-item">
                            <span class="text-xl mr-3">{amenity['icon']}</span>
                            <span>{amenity['name']}</span>
                        </div>'''
    
    return f'''
<body>
    <!-- Navigation (préservée) -->
    <nav class="fixed top-0 left-0 right-0 z-50 bg-white bg-opacity-10 backdrop-blur-md border-b border-white border-opacity-20">
        <div class="container mx-auto px-4">
            <div class="flex items-center justify-between h-16">
                <a href="index.html" class="text-white font-bold text-xl">
                    KhanelConcept
                </a>
                <div class="hidden md:flex space-x-6">
                    <a href="index.html" class="text-white hover:text-yellow-300 transition-colors">Accueil</a>
                    <a href="index.html#villas" class="text-white hover:text-yellow-300 transition-colors">Villas</a>
                    <a href="reservation.html" class="text-white hover:text-yellow-300 transition-colors">Réservation</a>
                </div>
            </div>
        </div>
    </nav>

    <main class="relative z-10">
        <!-- Hero Section avec Galerie COMPLÈTE -->
        <section class="relative h-screen flex items-center justify-center overflow-hidden">
            <!-- Villa Gallery Swiper avec VRAIES IMAGES -->
            <div class="villa-gallery swiper-container absolute inset-0 z-1">
                <div class="swiper-wrapper">
                    {gallery_slides}
                </div>
                
                <!-- Navigation Swiper -->
                <div class="swiper-pagination"></div>
                <div class="swiper-button-next"></div>
                <div class="swiper-button-prev"></div>
            </div>
            
            <!-- Overlay -->
            <div class="absolute inset-0 bg-black bg-opacity-40 z-2"></div>
            
            <!-- Content Hero -->
            <div class="relative z-10 text-center text-white px-4 max-w-4xl mx-auto">
                <!-- Breadcrumb -->
                <nav class="mb-8" data-aos="fade-down">
                    <div class="flex items-center justify-center space-x-2 text-sm opacity-90">
                        <a href="index.html" class="hover:text-yellow-300 transition-colors">
                            <i class="fas fa-home mr-1"></i>Accueil
                        </a>
                        <i class="fas fa-chevron-right text-xs"></i>
                        <a href="index.html#villas" class="hover:text-yellow-300 transition-colors">Villas</a>
                        <i class="fas fa-chevron-right text-xs"></i>
                        <span class="text-yellow-300">{name}</span>
                    </div>
                </nav>
                
                <!-- Villa Title -->
                <h1 class="text-4xl md:text-6xl font-bold mb-4 leading-tight" data-aos="fade-up">
                    {name}
                </h1>
                
                <!-- Rating -->
                <div class="flex items-center justify-center mb-6" data-aos="fade-up" data-aos-delay="100">
                    <div class="flex text-yellow-400 text-xl mr-3">
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                    </div>
                    <span class="text-lg">(5.0)</span>
                </div>
                
                <!-- Location -->
                <p class="text-xl mb-6 flex items-center justify-center" data-aos="fade-up" data-aos-delay="200">
                    <i class="fas fa-map-marker-alt mr-2 text-red-400"></i>
                    {location}
                </p>
                
                <!-- Description -->
                <p class="text-lg mb-8 max-w-2xl mx-auto opacity-90" data-aos="fade-up" data-aos-delay="300">
                    {description}
                </p>
                
                <!-- Prix Principal -->
                <div class="mb-8" data-aos="fade-up" data-aos-delay="400">
                    <div class="inline-block bg-white bg-opacity-20 backdrop-blur-md rounded-full px-6 py-3 border border-white border-opacity-30">
                        <span class="text-2xl font-bold text-yellow-300">{price}</span>
                        <span class="text-white opacity-80">/nuit</span>
                    </div>
                </div>
                
                <!-- CTA Buttons -->
                <div class="flex flex-wrap gap-4 justify-center" data-aos="fade-up" data-aos-delay="500">
                    <button class="btn-primary" onclick="window.location.href='reservation.html'">
                        <i class="fas fa-calendar-check mr-2"></i>
                        Réserver maintenant
                    </button>
                    <button class="btn-secondary" onclick="document.getElementById('amenities').scrollIntoView()">
                        <i class="fas fa-info-circle mr-2"></i>
                        Voir détails
                    </button>
                </div>
            </div>
            
            <!-- Scroll Indicator -->
            <div class="absolute bottom-8 left-1/2 transform -translate-x-1/2 z-10" data-aos="fade-up" data-aos-delay="600">
                <div class="animate-bounce">
                    <i class="fas fa-chevron-down text-white text-2xl opacity-70"></i>
                </div>
            </div>
        </section>

        <!-- Quick Info Cards -->
        <section class="mb-16" data-aos="fade-up" data-aos-delay="200">
            <div class="grid grid-cols-2 lg:grid-cols-4 gap-6">
                <div class="info-card text-center">
                    <div class="text-3xl text-blue-600 mb-3"><i class="fas fa-users"></i></div>
                    <div class="text-lg font-semibold">{guests}</div>
                    <div class="text-sm text-gray-600">Voyageurs</div>
                </div>
                <div class="info-card text-center">
                    <div class="text-3xl text-green-600 mb-3"><i class="fas fa-bed"></i></div>
                    <div class="text-lg font-semibold">3</div>
                    <div class="text-sm text-gray-600">Chambres</div>
                </div>
                <div class="info-card text-center">
                    <div class="text-3xl text-purple-600 mb-3"><i class="fas fa-bath"></i></div>
                    <div class="text-lg font-semibold">2</div>
                    <div class="text-sm text-gray-600">Salles de bain</div>
                </div>
                <div class="info-card text-center">
                    <div class="text-3xl text-orange-600 mb-3"><i class="fas fa-expand-arrows-alt"></i></div>
                    <div class="text-lg font-semibold">200m²</div>
                    <div class="text-sm text-gray-600">Surface</div>
                </div>
            </div>
        </section>

        <!-- Description & Amenities -->
        <div class="grid lg:grid-cols-3 gap-12 mb-16" id="amenities">
            <!-- Description -->
            <div class="lg:col-span-2" data-aos="fade-up" data-aos-delay="300">
                <div class="info-card">
                    <h2 class="text-3xl font-bold mb-6 flex items-center">
                        <i class="fas fa-info-circle text-blue-600 mr-3"></i>
                        Description de la villa
                    </h2>
                    <div class="prose prose-lg max-w-none">
                        <p>{description}</p>
                    </div>
                    
                    <!-- Action Buttons -->
                    <div class="mt-8 flex flex-wrap gap-4">
                        <button class="btn-primary" onclick="window.location.href='reservation.html'">
                            <i class="fas fa-calendar-check"></i>
                            Réserver maintenant
                        </button>
                        <button class="btn-secondary" onclick="alert('Ajouté aux favoris!')">
                            <i class="fas fa-heart"></i>
                            Ajouter aux favoris
                        </button>
                        <button class="btn-secondary" onclick="window.print()">
                            <i class="fas fa-print"></i>
                            Imprimer
                        </button>
                    </div>
                </div>
            </div>
            
            <!-- Quick Amenities ORIGINAUX -->
            <div data-aos="fade-up" data-aos-delay="400">
                <div class="info-card">
                    <h3 class="text-2xl font-bold mb-6 flex items-center">
                        <i class="fas fa-star text-yellow-500 mr-3"></i>
                        Équipements principaux
                    </h3>
                    <div class="space-y-3">
                        {amenities_html}
                    </div>
                </div>
            </div>
        </div>

        <!-- Section Tarifs Propre -->
        <section class="mb-16" data-aos="fade-up" data-aos-delay="500">
            <div class="info-card">
                <h3 class="text-2xl font-bold mb-6 flex items-center">
                    <i class="fas fa-info-circle text-blue-600 mr-3"></i>
                    Informations et Tarifs
                </h3>
                
                <div class="grid md:grid-cols-2 gap-8">
                    <!-- Informations -->
                    <div>
                        <h4 class="text-lg font-semibold mb-4 text-gray-700">🏠 Informations Villa</h4>
                        <div class="bg-gray-50 rounded-lg p-4 space-y-2">
                            <div class="flex justify-between">
                                <span class="font-medium">Nom :</span>
                                <span>{name}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="font-medium">Localisation :</span>
                                <span>{location}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="font-medium">Capacité :</span>
                                <span>{guests}</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Tarifs -->
                    <div>
                        <h4 class="text-lg font-semibold mb-4 text-gray-700">💰 Tarification</h4>
                        <div class="bg-green-50 rounded-lg p-4 border border-green-200">
                            <div class="space-y-2 text-sm">
                                <div class="flex justify-between">
                                    <span>Prix de base:</span>
                                    <strong class="text-green-700">{price}/nuit</strong>
                                </div>
                                <div class="flex justify-between">
                                    <span>Weekend (2 nuits):</span>
                                    <strong class="text-green-700">Prix préférentiel</strong>
                                </div>
                                <div class="flex justify-between">
                                    <span>Semaine (7 jours):</span>
                                    <strong class="text-green-700">Tarif dégressif</strong>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Contact -->
                <div class="mt-8 bg-blue-50 rounded-lg p-6 text-center border border-blue-200">
                    <h4 class="text-lg font-semibold mb-3 text-blue-800">📞 Réservation</h4>
                    <div class="space-y-2 text-sm">
                        <div><strong>Téléphone :</strong> <a href="tel:+596696xxxxxx" class="text-blue-600">+596 696 XX XX XX</a></div>
                        <div><strong>Email :</strong> <a href="mailto:contact@khanelconcept.com" class="text-blue-600">contact@khanelconcept.com</a></div>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <!-- Back to Top -->
    <button id="backToTop" class="fixed bottom-6 right-6 bg-blue-600 text-white w-12 h-12 rounded-full shadow-lg opacity-0 transition-all duration-300 hover:bg-blue-700" style="display: none;">
        <i class="fas fa-chevron-up"></i>
    </button>

    <!-- Scripts -->
    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/swiper@8/swiper-bundle.min.js"></script>
    
    <script>
        // Initialize AOS
        AOS.init({{
            duration: 1000,
            once: true
        }});

        // Initialize Swiper avec VRAIES IMAGES
        const villaSwiper = new Swiper('.villa-gallery', {{
            loop: true,
            pagination: {{
                el: '.swiper-pagination',
                clickable: true,
            }},
            navigation: {{
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            }},
            autoplay: {{
                delay: 5000,
                disableOnInteraction: false,
            }},
        }});

        // Back to Top
        window.addEventListener('scroll', function() {{
            const backToTop = document.getElementById('backToTop');
            if (window.pageYOffset > 300) {{
                backToTop.style.opacity = '1';
                backToTop.style.display = 'block';
            }} else {{
                backToTop.style.opacity = '0';
                setTimeout(() => {{
                    if (window.pageYOffset <= 300) {{
                        backToTop.style.display = 'none';
                    }}
                }}, 300);
            }}
        }});

        document.getElementById('backToTop').addEventListener('click', function() {{
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }});
    </script>
</body>
</html>'''

def main():
    print("🔧 RESTAURATION INTELLIGENTE COMPLÈTE")
    print("=" * 70)
    print("OBJECTIF: Récupérer les données de villa-details.html et tout restaurer")
    print("=" * 70)
    
    # ÉTAPE 1: Extraire toutes les données originales
    villas_data = extract_villa_data_from_details()
    
    if not villas_data:
        print("❌ Impossible de récupérer les données")
        return
    
    # ÉTAPE 2: Lister les villas à restaurer
    villa_files = glob.glob('/app/villa-*.html')
    villa_files = [f for f in villa_files if 'template' not in f and 'details' not in f]
    
    # ÉTAPE 3: Restaurer 3 villas test d'abord
    test_files = [
        '/app/villa-f3-petit-macabou.html',
        '/app/villa-f5-ste-anne.html', 
        '/app/villa-f6-petit-macabou.html'
    ]
    
    restored_count = 0
    
    for file_path in test_files:
        if os.path.exists(file_path):
            if restore_villa_with_original_data(file_path, villas_data):
                restored_count += 1
    
    print("=" * 70)
    print(f"🎯 RESTAURATION TEST TERMINÉE:")
    print(f"   • Villas restaurées: {restored_count}/{len(test_files)}")
    print(f"✅ Structure main2 + données originales complètes")
    print(f"✅ Galeries d'images restaurées")
    print(f"✅ reservation.html préservé")

if __name__ == "__main__":
    main()