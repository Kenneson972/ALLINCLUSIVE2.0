#!/usr/bin/env python3
"""
Mise à niveau ULTRA-SMOOTH de toutes les pages villa
Applique le design premium basé sur l'interface index.html
"""

import os
import re
from pathlib import Path

class VillaPremiumUpgrader:
    def __init__(self):
        self.villa_pages = [
            'villa-f3-petit-macabou.html',
            'villa-f3-baccha.html', 
            'villa-f3-francois.html',
            'villa-f5-ste-anne.html',
            'villa-f6-lamentin.html',
            'villa-f6-ste-luce.html',
            'villa-f5-vauclin.html',
            'villa-f7-baie-mulets.html',
            'villa-f5-la-renee.html',
            'bas-villa-trinite-cosmy.html',
            'bas-villa-robert.html',
            'bas-villa-ste-luce.html',
            'studio-cocooning-lamentin.html',
            'appartement-trenelle.html',
            'villa-fete-ducos.html',
            'villa-fete-fort-de-france.html',
            'villa-fete-riviere-pilote.html',
            'villa-fete-riviere-salee.html',
            'villa-fete-sainte-luce.html',
            'espace-piscine-bungalow.html',
            'villa-f6-petit-macabou-fete.html'
        ]
        
        self.villa_data = self.get_villa_data()

    def get_villa_data(self):
        """Données des villas pour la réservation"""
        return {
            'villa-f3-petit-macabou': {
                'name': 'Villa F3 sur Petit Macabou',
                'basePrice': 850,
                'capacity': 6,
                'maxGuests': 15
            },
            'villa-f3-baccha': {
                'name': 'Villa F3 POUR LA BACCHA',
                'basePrice': 1350,
                'capacity': 6,
                'maxGuests': 9
            },
            'villa-f3-francois': {
                'name': 'Villa F3 sur le François',
                'basePrice': 800,
                'capacity': 4,
                'maxGuests': 10
            },
            'villa-f5-ste-anne': {
                'name': 'Villa F5 sur Ste Anne',
                'basePrice': 1350,
                'capacity': 10,
                'maxGuests': 15
            },
            'villa-f6-lamentin': {
                'name': 'Villa F6 au Lamentin',
                'basePrice': 1200,
                'capacity': 10,
                'maxGuests': 20
            },
            'villa-f6-ste-luce': {
                'name': 'Villa F6 sur Ste Luce à 1mn de la plage',
                'basePrice': 1700,
                'capacity': 14,
                'maxGuests': 14
            },
            'villa-f5-vauclin': {
                'name': 'Villa F5 Vauclin Ravine Plate',
                'basePrice': 1550,
                'capacity': 8,
                'maxGuests': 8
            },
            'villa-f7-baie-mulets': {
                'name': 'Villa F7 Baie des Mulets',
                'basePrice': 2200,
                'capacity': 16,
                'maxGuests': 160
            },
            'villa-f5-la-renee': {
                'name': 'Villa F5 La Renée',
                'basePrice': 900,
                'capacity': 10,
                'maxGuests': 60
            },
            'bas-villa-trinite-cosmy': {
                'name': 'Bas de villa F3 Trinité Cosmy',
                'basePrice': 500,
                'capacity': 5,
                'maxGuests': 60
            },
            'bas-villa-robert': {
                'name': 'Bas de villa F3 sur le Robert',
                'basePrice': 900,
                'capacity': 10,
                'maxGuests': 10
            },
            'bas-villa-ste-luce': {
                'name': 'Bas de villa F3 sur Ste Luce',
                'basePrice': 470,
                'capacity': 6,
                'maxGuests': 6
            },
            'studio-cocooning-lamentin': {
                'name': 'Studio Cocooning Lamentin',
                'basePrice': 290,
                'capacity': 2,
                'maxGuests': 2
            },
            'appartement-trenelle': {
                'name': 'Appartement F3 Trenelle',
                'basePrice': 700,
                'capacity': 3,
                'maxGuests': 3
            },
            'villa-fete-ducos': {
                'name': 'Villa Fête Journée Ducos',
                'basePrice': 20,
                'capacity': 30,
                'maxGuests': 30
            },
            'villa-fete-fort-de-france': {
                'name': 'Villa Fête Journée Fort de France',
                'basePrice': 100,
                'capacity': 80,
                'maxGuests': 80
            },
            'villa-fete-riviere-pilote': {
                'name': 'Villa Fête Journée Rivière-Pilote',
                'basePrice': 660,
                'capacity': 100,
                'maxGuests': 100
            },
            'villa-fete-riviere-salee': {
                'name': 'Villa Fête Journée Rivière Salée',
                'basePrice': 400,
                'capacity': 100,
                'maxGuests': 100
            },
            'villa-fete-sainte-luce': {
                'name': 'Villa Fête Journée Sainte-Luce',
                'basePrice': 390,
                'capacity': 40,
                'maxGuests': 40
            },
            'espace-piscine-bungalow': {
                'name': 'Espace Piscine Journée Bungalow',
                'basePrice': 350,
                'capacity': 150,
                'maxGuests': 150
            },
            'villa-f6-petit-macabou-fete': {
                'name': 'Villa F6 sur Petit Macabou (séjour + fête)',
                'basePrice': 2000,
                'capacity': 13,
                'maxGuests': 150
            }
        }

    def upgrade_page(self, page_path):
        """Met à niveau une page villa avec le design premium"""
        
        if not page_path.exists():
            print(f"❌ {page_path.name} - Fichier non trouvé")
            return False
            
        try:
            with open(page_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            villa_id = page_path.stem
            villa_info = self.villa_data.get(villa_id, {})
            
            # 1. Mise à jour du HEAD avec assets premium
            content = self.update_head(content)
            
            # 2. Mise à jour vidéo background
            content = self.update_video_background(content)
            
            # 3. Mise à jour galerie photos
            content = self.update_gallery(content)
            
            # 4. Suppression formulaire et ajout boutons réservation
            content = self.update_reservation_section(content, villa_id, villa_info)
            
            # 5. Mise à jour JavaScript
            content = self.update_javascript(content, villa_id, villa_info)
            
            # Sauvegarder
            with open(page_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"✅ {page_path.name} - Mise à niveau réussie")
            return True
            
        except Exception as e:
            print(f"❌ {page_path.name} - Erreur: {str(e)}")
            return False

    def update_head(self, content):
        """Met à jour la section HEAD avec assets premium"""
        
        # Remplacer le CSS glassmorphism par villa-enhanced
        content = re.sub(
            r'<link rel="stylesheet" href="\./assets/css/glassmorphism\.css">',
            '''    <link rel="stylesheet" href="./assets/css/villa-enhanced.css">
    <link rel="preload" href="https://res.cloudinary.com/dqz8rw6m2/video/upload/v1733669700/martinique-bg_d0pzjm.mp4" as="video" type="video/mp4">''',
            content
        )
        
        # Ajouter meta description si absente
        if '<meta name="description"' not in content:
            content = re.sub(
                r'(<meta name="viewport"[^>]*>)',
                r'\1\n    <meta name="description" content="Villa de luxe en Martinique avec design premium et réservation en ligne sécurisée.">',
                content
            )
        
        return content

    def update_video_background(self, content):
        """Met à jour la vidéo background avec version premium"""
        
        old_video = r'''    <!-- Video Background \(identique index\) -->
    <div class="video-background">
        <video autoplay muted loop>
            <source src="https://res\.cloudinary\.com/dqz8rw6m2/video/upload/v1733669700/martinique-bg_d0pzjm\.mp4" type="video/mp4">
        </video>
    </div>'''
        
        new_video = '''    <!-- Video Background Premium -->
    <div class="video-background">
        <video autoplay muted loop playsinline webkit-playsinline preload="metadata">
            <source src="https://res.cloudinary.com/dqz8rw6m2/video/upload/v1733669700/martinique-bg_d0pzjm.mp4" type="video/mp4">
        </video>
    </div>
    
    <!-- Fallback Background -->
    <div class="video-background-fallback"></div>'''
        
        content = re.sub(old_video, new_video, content, flags=re.MULTILINE)
        
        return content

    def update_gallery(self, content):
        """Met à jour la galerie avec version premium interactive"""
        
        # Chercher la galerie existante
        gallery_match = re.search(r'<section class="gallery glass-card">(.*?)</section>', content, re.DOTALL)
        
        if not gallery_match:
            return content
            
        gallery_content = gallery_match.group(1)
        
        # Extraire les images
        img_pattern = r'<img src="([^"]*)" alt="([^"]*)"[^>]*>'
        images = re.findall(img_pattern, gallery_content)
        
        if not images:
            return content
            
        # Créer la nouvelle galerie premium
        new_gallery_items = []
        for img_src, img_alt in images:
            new_gallery_items.append(f'''                <div class="photo-item">
                    <img src="{img_src}" alt="{img_alt}" loading="lazy">
                    <div class="photo-zoom-overlay">🔍 Cliquer pour agrandir</div>
                </div>''')
        
        new_gallery = f'''<section class="gallery glass-card">
            <h2>Galerie Photos</h2>
            <div class="photo-slider">
{chr(10).join(new_gallery_items)}
            </div>
        </section>'''
        
        content = re.sub(r'<section class="gallery glass-card">.*?</section>', new_gallery, content, flags=re.DOTALL)
        
        return content

    def update_reservation_section(self, content, villa_id, villa_info):
        """Remplace le formulaire par des boutons réservation premium"""
        
        villa_name = villa_info.get('name', 'Villa')
        
        new_reservation = f'''        <!-- Réservation Premium -->
        <section class="booking glass-card">
            <h2>Réservation</h2>
            <div class="reservation-buttons">
                <a href="javascript:void(0)" 
                   class="btn-reserve-primary" 
                   onclick="ReservationManager.goToReservation('{villa_id}', '{villa_name}')">
                    🏨 Réserver maintenant
                </a>
                <a href="./reservation.html" class="btn-reserve-secondary">
                    📋 Voir toutes les villas
                </a>
            </div>
            <p style="text-align: center; margin-top: 1rem; color: var(--text-secondary);">
                Réservation sécurisée • Confirmation immédiate • Assistance 24/7
            </p>
        </section>'''
        
        # Remplacer toute la section booking
        content = re.sub(
            r'        <!-- Formulaire Réservation -->.*?</section>',
            new_reservation,
            content,
            flags=re.DOTALL
        )
        
        return content

    def update_javascript(self, content, villa_id, villa_info):
        """Met à jour le JavaScript avec villa-gallery.js premium"""
        
        new_js = f'''    <script src="./assets/js/villa-gallery.js"></script>
    <script>
        // Initialisation spécifique à cette villa
        document.addEventListener('DOMContentLoaded', function() {{
            // Données de la villa pour la réservation
            window.currentVilla = {{
                id: '{villa_id}',
                name: '{villa_info.get("name", "Villa")}',
                basePrice: {villa_info.get("basePrice", 0)},
                capacity: {villa_info.get("capacity", 0)},
                maxGuests: {villa_info.get("maxGuests", 0)}
            }};
        }});
    </script>'''
        
        # Remplacer l'ancien JavaScript
        content = re.sub(
            r'    <script src="\./assets/js/glassmorphism\.js"></script>',
            new_js,
            content
        )
        
        return content

    def upgrade_all_pages(self):
        """Met à niveau toutes les pages villa"""
        
        print("🚀 MISE À NIVEAU ULTRA-SMOOTH DES PAGES VILLA")
        print("=" * 60)
        print("Basé sur l'interface premium de l'index.html")
        print()
        
        successful_upgrades = 0
        failed_upgrades = 0
        
        for page_name in self.villa_pages:
            page_path = Path(f'/app/{page_name}')
            
            if self.upgrade_page(page_path):
                successful_upgrades += 1
            else:
                failed_upgrades += 1
        
        print(f"\n📊 RÉSULTATS DE LA MISE À NIVEAU:")
        print(f"✅ Réussies: {successful_upgrades}")
        print(f"❌ Échouées: {failed_upgrades}")
        
        if successful_upgrades == len(self.villa_pages):
            print(f"\n🎉 SUCCÈS COMPLET!")
            print("✨ Toutes les pages villa sont maintenant ULTRA-SMOOTH")
            print("🎨 Design premium basé sur l'index.html appliqué")
            print("🖼️ Galerie photos interactive avec lightbox")
            print("📱 Navigation tactile et responsive")
            print("🎥 Vidéo background optimisée")
            print("🔗 Boutons réservation premium intégrés")
            print("\n🏆 Les 21 pages villa sont prêtes pour une expérience premium!")
        else:
            print(f"\n⚠️ ATTENTION: {failed_upgrades} page(s) n'ont pas pu être mises à niveau")
        
        return successful_upgrades == len(self.villa_pages)

if __name__ == "__main__":
    upgrader = VillaPremiumUpgrader()
    upgrader.upgrade_all_pages()