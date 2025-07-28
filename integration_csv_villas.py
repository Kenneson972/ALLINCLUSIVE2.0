#!/usr/bin/env python3
"""
Script d'intégration CSV - KhanelConcept Villas
Intègre les données du CSV dans la base de données en gardant l'interface existante
"""

import asyncio
import json
import re
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration MongoDB
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = 'khanelconcept'

# Données du CSV (extraites du crawl précédent)
CSV_DATA = [
    {
        "nom": "Villa F3 sur Petit Macabou",
        "localisation": "Petit Macabou, Vauclin",
        "type": "F3",
        "capacite": "6 personnes ( jusqu'à 15 personnes en journée )",
        "tarif": "Grandes Vacances: 1550€/semaine, Weekend: 850€ (2 nuits), Noël/Nouvel An: 1690€/semaine",
        "services": "Chambres climatisées, 1 salle de bain avec WC, WC indépendant, salon climatisé avec canapé-lit, sauna, jacuzzi, 2 douches extérieures",
        "description": "Villa avec possibilité d'accueillir 9 invités supplémentaires en journée (9h-20h). Caution: 1500€. Check-in: 16h, Check-out: 11h (possibilité extension jusqu'à 16h selon disponibilité)."
    },
    {
        "nom": "Villa F3 POUR LA BACCHA",
        "localisation": "Petit Macabou",
        "type": "F3",
        "capacite": "6 personnes",
        "tarif": "Août: 1350€/semaine, Juillet: complet",
        "services": "2 chambres climatisées, salon climatisé avec canapé-lit",
        "description": "Possibilité d'accueillir jusqu'à 9 invités entre 9h et 18h. Caution: 1500€ par chèque. Règles strictes concernant le bruit pour respecter le voisinage."
    },
    {
        "nom": "Villa F3 sur le François",
        "localisation": "Hauteurs du Morne Carrière au François",
        "type": "F3",
        "capacite": "4 personnes (maximum 10 invités)",
        "tarif": "Weekend: 800€ (2 nuits), Semaine: 1376€ (7 jours)",
        "services": "Stationnement pour 5 véhicules, enceintes JBL autorisées",
        "description": "Caution: 1000€ (850€ par chèque et 150€ en espèces). Check-in: 16h, Check-out: 11h (option late check-out: +80€). Frais de 50€ par 30 minutes de retard pour la remise des clés. Villa à rendre propre et rangée."
    },
    {
        "nom": "Villa F5 sur Ste Anne",
        "localisation": "Quartier les Anglais, Ste Anne",
        "type": "F5",
        "capacite": "10 personnes ( jusqu'à 15 personnes en journée )",
        "tarif": "Weekend: 1350€ (2 nuits, hors vacances scolaires), Semaine: 2251€ (7 jours)",
        "services": "4 chambres, 4 salles de bain",
        "description": "Possibilité d'accueillir jusqu'à 15 invités de 9h à 19h. Caution: 500€ en espèces + 1500€ en empreinte CB. Facilités de paiement sans frais supplémentaires avec paiement total avant entrée."
    },
    {
        "nom": "Villa F6 au Lamentin",
        "localisation": "Quartier Béleme, Lamentin",
        "type": "F6",
        "capacite": "10 personnes (jusqu'à 20 invités en journée)",
        "tarif": "Weekend: 1500€ (vendredi-dimanche), Weekend 2 nuits: 1200€ (sans invités), Semaine: 2800€ (8 jours), +300€ si fête",
        "services": "Piscine, jacuzzi",
        "description": "Fêtes autorisées de 10h à 19h. Disponibilité vacances: du 1er au 10 juillet et du 25 au 31 août. Check-in: 15h, check-out: 18h. Pénalité retard clés: 150€/30min. Caution: 1000€ (empreinte bancaire). Covoiturage obligatoire."
    },
    {
        "nom": "Villa F6 sur Ste Luce à 1mn de la plage",
        "localisation": "Zac de Pont Café, Ste Luce, à 1mn de la plage Corps de garde",
        "type": "F6",
        "capacite": "10 à 14 personnes",
        "tarif": "Weekend: 1700€, Semaine (8 jours): 2200€ à 2850€",
        "services": "5 appartements (2 F2 duplex et 3 F2), dont un en sous-sol",
        "description": "Check-in: 17h, Check-out: 11h. Caution: 1500€ par chèque + 500€ en espèces (remboursables). Location uniquement à la semaine pendant les vacances scolaires. Facilités de paiement sans frais supplémentaires (tout doit être payé avant l'entrée)."
    },
    {
        "nom": "Villa F3 Bas de villa Trinité Cosmy",
        "localisation": "Cosmy, Trinité",
        "type": "F3 (Bas de villa)",
        "capacite": "5 adultes ou 4 adultes et 2 enfants (jusqu'à 60 invités pour fêtes)",
        "tarif": "Weekend sans invités: 500€, Weekend + Fête: 670€ (10 invités) à 1400€ (60 invités)",
        "services": "2 chambres climatisées, 1 salle de bain, double terrasse, salon, cuisine américaine, piscine privée chauffée",
        "description": "Villa charmante idéale pour séjours entre amis, famille et événements. Environnement calme et relaxant. Horaires fête: 10h-18h ou 14h-22h (départ des invités à partir de 21h). Location à la semaine pendant vacances scolaires (exceptions possibles). Caution: 200€ en espèces + 400€ par chèque."
    },
    {
        "nom": "Bas de villa F3 sur le Robert",
        "localisation": "Pointe Hyacinthe, Le Robert",
        "type": "F3 (Bas de villa)",
        "capacite": "10 personnes",
        "tarif": "Weekend: 900€, Weekend avec fête/invités: +550€, Semaine: 1250€ (basse saison), 1500€ (haute saison)",
        "services": "2 chambres climatisées, location à la journée possible (lundi-jeudi), excursion nautique possible",
        "description": "Enceintes JBL autorisées jusqu'à 22h (DJ et gros systèmes sono interdits). Caution: 1500€ pour la villa + caution pour l'espace piscine. Paiement en plusieurs fois sans frais possible (tout doit être soldé avant l'entrée)."
    },
    {
        "nom": "Villa F7 Baie des Mulets",
        "localisation": "Baie des Mulets, Vauclin",
        "type": "F7 (F5 + F3)",
        "capacite": "16 personnes (F5: 10 personnes + F3: 6 personnes)",
        "tarif": "Base: 2200€/weekend, 4200€/semaine. Fêtes: +330€ (30 invités), +550€ (50 invités), +770€ (80 invités), +1375€ (160 invités)",
        "services": "F5: 4 chambres climatisées + salon avec canapé-lit; F3: salon avec canapé-lit. Parking pour 30 véhicules.",
        "description": "Check-in: 11h, Check-out: 13h (option late check-out 17h30: +150€). Fêtes autorisées de 9h à minuit. Location possible à la journée (lundi-jeudi) selon disponibilité. Caution: 1500€ par chèque ou empreinte bancaire. Paiement possible en plusieurs fois, sans frais, avec solde 72h avant entrée."
    },
    {
        "nom": "Studio Cocooning Lamentin",
        "localisation": "Hauteurs de Morne Pitault, Lamentin",
        "type": "Studio",
        "capacite": "2 personnes",
        "tarif": "À partir de 290€, minimum 2 nuits",
        "services": "Bac à punch privé (petite piscine)",
        "description": "Pas d'invités autorisés. Location uniquement à la semaine pendant les vacances scolaires et haute saison touristique. Check-in: 16h, Check-out: 11h (départ tardif possible selon disponibilité). Paiement en plusieurs fois sans frais possible (tout doit être réglé avant entrée)."
    }
]

async def connect_to_mongo():
    """Connexion à MongoDB"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    return db

def extract_base_price(tarif_str):
    """Extrait le prix de base d'une chaîne de tarifs"""
    # Chercher le premier prix en euros
    prix_match = re.search(r'(\d+)€', tarif_str)
    if prix_match:
        return int(prix_match.group(1))
    return 500  # Prix par défaut

def extract_guests_count(capacite_str):
    """Extrait le nombre d'invités d'une chaîne de capacité"""
    # Chercher le premier nombre
    guests_match = re.search(r'(\d+)', capacite_str)
    if guests_match:
        return int(guests_match.group(1))
    return 2  # Par défaut

def parse_services_to_amenities(services_str):
    """Convertit les services en amenities"""
    amenities = []
    
    # Mapping des services vers des amenities
    service_mapping = {
        'piscine': 'Piscine',
        'jacuzzi': 'Jacuzzi',
        'climatisé': 'Climatisation',
        'cuisine': 'Cuisine équipée',
        'sauna': 'Sauna',
        'douche': 'Douche extérieure',
        'wifi': 'WiFi',
        'parking': 'Parking',
        'terrasse': 'Terrasse',
        'salle de bain': 'Salle de bain',
        'chambre': 'Chambres',
        'salon': 'Salon',
        'stationnement': 'Parking'
    }
    
    services_lower = services_str.lower()
    for keyword, amenity in service_mapping.items():
        if keyword in services_lower:
            amenities.append(amenity)
    
    # Ajouter WiFi par défaut
    if 'WiFi' not in amenities:
        amenities.append('WiFi')
    
    return amenities

def determine_category(nom, tarif, capacite):
    """Détermine la catégorie de la villa"""
    nom_lower = nom.lower()
    
    if 'studio' in nom_lower:
        return 'special'
    elif 'fête' in nom_lower or 'journée' in nom_lower:
        return 'fete'
    elif 'location annuelle' in nom_lower:
        return 'special'
    else:
        return 'sejour'

def get_villa_image_path(nom):
    """Génère le chemin d'image basé sur le nom de la villa"""
    # Conversion du nom en nom de dossier
    nom_clean = nom.replace('Villa ', '').replace('Studio ', '').replace('Bas de villa ', '')
    
    # Mapping spécifique pour les noms connus
    image_mapping = {
        'F3 sur Petit Macabou': 'Villa_F3_Petit_Macabou',
        'F3 POUR LA BACCHA': 'Villa_F3_Baccha_Petit_Macabou',
        'F3 sur le François': 'Villa_F3_Le_Francois',
        'F5 sur Ste Anne': 'Villa_F5_Ste_Anne',
        'F6 au Lamentin': 'Villa_F6_Lamentin',
        'F6 sur Ste Luce à 1mn de la plage': 'Villa_F6_Ste_Luce',
        'F3 Bas de villa Trinité Cosmy': 'Villa_F3_Trinite_Cosmy',
        'F3 sur le Robert': 'Villa_F3_Robert_Pointe_Hyacinthe',
        'F7 Baie des Mulets': 'Villa_F7_Baie_des_Mulets_Vauclin',
        'Cocooning Lamentin': 'Studio_Cocooning_Lamentin'
    }
    
    folder_name = image_mapping.get(nom_clean, nom_clean.replace(' ', '_'))
    return f"/images/{folder_name}/01_piscine_exterieur.jpg"

def generate_gallery_paths(nom):
    """Génère les chemins de galerie pour une villa"""
    nom_clean = nom.replace('Villa ', '').replace('Studio ', '').replace('Bas de villa ', '')
    
    # Mapping spécifique pour les galeries
    gallery_mapping = {
        'F3 sur Petit Macabou': 'Villa_F3_Petit_Macabou',
        'F3 POUR LA BACCHA': 'Villa_F3_Baccha_Petit_Macabou',
        'F3 sur le François': 'Villa_F3_Le_Francois',
        'F5 sur Ste Anne': 'Villa_F5_Ste_Anne',
        'F6 au Lamentin': 'Villa_F6_Lamentin',
        'F6 sur Ste Luce à 1mn de la plage': 'Villa_F6_Ste_Luce',
        'F3 Bas de villa Trinité Cosmy': 'Villa_F3_Trinite_Cosmy',
        'F3 sur le Robert': 'Villa_F3_Robert_Pointe_Hyacinthe',
        'F7 Baie des Mulets': 'Villa_F7_Baie_des_Mulets_Vauclin',
        'Cocooning Lamentin': 'Studio_Cocooning_Lamentin'
    }
    
    folder_name = gallery_mapping.get(nom_clean, nom_clean.replace(' ', '_'))
    
    # Générer une galerie type avec les images courantes
    gallery_base = [
        f"/images/{folder_name}/01_piscine_exterieur.jpg",
        f"/images/{folder_name}/02_terrasse_salon_exterieur.jpg",
        f"/images/{folder_name}/03_salle_de_bain_moderne.jpg",
        f"/images/{folder_name}/04_chambre_principale.jpg",
        f"/images/{folder_name}/05_cuisine_equipee.jpg",
        f"/images/{folder_name}/06_vue_panoramique.jpg"
    ]
    
    return gallery_base

def get_fallback_icon(nom, type_villa):
    """Génère l'icône de fallback"""
    nom_lower = nom.lower()
    
    if 'studio' in nom_lower:
        return '🏠'
    elif 'f7' in nom_lower or 'baie' in nom_lower:
        return '🏄'
    elif 'piscine' in nom_lower or 'jacuzzi' in nom_lower:
        return '🏊'
    elif 'plage' in nom_lower:
        return '🏖️'
    elif 'trinité' in nom_lower:
        return '🌺'
    else:
        return '🏡'

async def update_villa_from_csv(db, csv_villa):
    """Met à jour une villa avec les données CSV"""
    try:
        # Extraire les informations
        nom = csv_villa['nom']
        prix_base = extract_base_price(csv_villa['tarif'])
        guests_count = extract_guests_count(csv_villa['capacite'])
        amenities = parse_services_to_amenities(csv_villa['services'])
        category = determine_category(nom, csv_villa['tarif'], csv_villa['capacite'])
        image_path = get_villa_image_path(nom)
        gallery_paths = generate_gallery_paths(nom)
        fallback_icon = get_fallback_icon(nom, csv_villa['type'])
        
        # Créer l'objet villa mis à jour
        villa_update = {
            'name': nom,
            'location': csv_villa['localisation'],
            'price': prix_base,
            'guests': guests_count,
            'guests_detail': csv_villa['capacite'],
            'features': csv_villa['services'][:100] + '...' if len(csv_villa['services']) > 100 else csv_villa['services'],
            'category': category,
            'image': image_path,
            'gallery': gallery_paths,
            'fallback_icon': fallback_icon,
            'amenities': amenities,
            'description': csv_villa['description'],
            'pricing_details': csv_villa['tarif'],  # Nouveau champ pour les tarifs détaillés
            'services_full': csv_villa['services'],  # Services complets
            'updated_at': datetime.utcnow()
        }
        
        # Chercher si la villa existe déjà
        existing_villa = await db.villas.find_one({'name': nom})
        
        if existing_villa:
            # Mettre à jour la villa existante
            await db.villas.update_one(
                {'name': nom},
                {'$set': villa_update}
            )
            print(f"✅ Villa mise à jour: {nom}")
        else:
            # Créer une nouvelle villa
            villa_update['id'] = str(len(await db.villas.find({}).to_list(None)) + 1)
            await db.villas.insert_one(villa_update)
            print(f"🆕 Villa créée: {nom}")
            
    except Exception as e:
        print(f"❌ Erreur mise à jour villa {csv_villa['nom']}: {e}")

async def main():
    """Fonction principale d'intégration"""
    print("🏠 INTÉGRATION CSV VILLAS KHANELCONCEPT")
    print("=" * 50)
    
    try:
        # Connexion à MongoDB
        db = await connect_to_mongo()
        print("✅ Connexion MongoDB établie")
        
        # Sauvegarder les données actuelles
        current_villas = await db.villas.find({}).to_list(None)
        print(f"📊 Villas actuelles: {len(current_villas)}")
        
        # Sauvegarder dans un fichier de backup
        with open('/app/backup_villas.json', 'w') as f:
            json.dump(current_villas, f, indent=2, default=str)
        print("💾 Backup créé: /app/backup_villas.json")
        
        # Intégrer les données CSV
        print("\n🔄 MISE À JOUR DES VILLAS")
        print("-" * 30)
        
        for csv_villa in CSV_DATA:
            await update_villa_from_csv(db, csv_villa)
        
        # Vérifier les résultats
        updated_villas = await db.villas.find({}).to_list(None)
        print(f"\n📈 Villas après mise à jour: {len(updated_villas)}")
        
        # Statistiques
        categories = {}
        prix_range = []
        
        for villa in updated_villas:
            cat = villa.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
            prix_range.append(villa.get('price', 0))
        
        print(f"📊 Catégories: {categories}")
        print(f"💰 Prix: {min(prix_range)}€ - {max(prix_range)}€")
        
        print("\n✅ INTÉGRATION TERMINÉE")
        print("🎯 Interface conservée, données actualisées avec CSV")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'intégration: {e}")

if __name__ == "__main__":
    asyncio.run(main())