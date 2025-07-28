#!/usr/bin/env python3
"""
PHASE 1 : CORRECTION DE LA BASE
Identifier et supprimer les villas fictives, garder uniquement les vraies villas
"""

import asyncio
import json
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime

# Configuration MongoDB
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = 'khanelconcept'

# VRAIES VILLAS basées sur le site web https://kenneson972.github.io/ALLINCLUSIVE2.0/
VRAIES_VILLAS_SITE = {
    "Villa F3 Petit Macabou": {
        "description": "6 personnes + 9 invités",
        "features": "Sauna, Jacuzzi, 2 douches extérieures", 
        "current_price": 850,
        "location": "Petit Macabou au Vauclin"
    },
    "Villa F5 Ste Anne": {
        "description": "10 personnes + 15 invités",
        "features": "Piscine, décoration rose distinctive",
        "current_price": 1300,
        "location": "Quartier Les Anglais, Ste Anne"
    },
    "Villa F3 Baccha Petit Macabou": {
        "description": "6 personnes + 9 convives",
        "features": "Piscine, terrasses modernes",
        "current_price": 1350,
        "location": "Petit Macabou"
    },
    "Villa F6 Lamentin": {
        "description": "10 personnes + 20 invités max",
        "features": "Piscine, Jacuzzi, douche extérieure",
        "current_price": 1500,
        "location": "Quartier Bélème au Lamentin"
    },
    "Villa F6 Ste Luce Plage": {
        "description": "12 personnes",
        "features": "Face à la plage, piscine, terrasse vue mer",
        "current_price": 1200,
        "location": "Sainte-Luce face à la plage"
    },
    "Villa F6 Petit Macabou": {
        "description": "12 personnes + 20 invités",
        "features": "Vue mer, villa moderne, studio mezzanine",
        "current_price": 2000,
        "location": "Petit Macabou, Vauclin"
    },
    "Villa F7 Baie des Mulets": {
        "description": "14 personnes",
        "features": "Grande villa, vue mer, véranda bambou",
        "current_price": 2500,
        "location": "Baie des Mulets, Vauclin"
    },
    "Villa F3 Trinité Cosmy": {
        "description": "6 personnes",
        "features": "Piscine chauffée, vue collines et océan",
        "current_price": 900,
        "location": "Trinité - Cosmy"
    },
    "Villa F5 Rivière-Pilote La Renée": {
        "description": "10 personnes",
        "features": "Terrasse bois, hamacs, salon extérieur",
        "current_price": 1400,
        "location": "Rivière-Pilote - La Renée"
    },
    "Villa F3 Le François": {
        "description": "6 personnes",
        "features": "Vue mer, terrasses panoramiques",
        "current_price": 800,
        "location": "Le François, Martinique"
    },
    "Villa F5 Vauclin Ravine Plate": {
        "description": "10 personnes max",
        "features": "Piscine à débordement, gazebo, vue collines",
        "current_price": 1550,
        "location": "Vauclin - Ravine Plate"
    },
    "Bas Villa F3 Ste Luce": {
        "description": "4 personnes",
        "features": "Terrasse couverte, éclairage LED",
        "current_price": 470,
        "location": "Sainte-Luce"
    },
    "Villa F3 Trenelle": {
        "description": "6 personnes",
        "features": "Location longue durée, entièrement équipée",
        "current_price": 800,
        "location": "Trenelle, Location Annuelle"
    },
    "Studio Cocooning Lamentin": {
        "description": "2 personnes (couple)",
        "features": "Jacuzzi privé, vue panoramique",
        "current_price": 290,
        "location": "Morne Pitault, Lamentin"
    },
    "Villa F3 Le Robert": {
        "description": "6 personnes",
        "features": "Piscine rectangulaire, pergola, kitchenette",
        "current_price": 630,
        "location": "Robert - Pointe Hyacinthe"
    },
    "Espace Piscine Journée Bungalow": {
        "description": "8 personnes en journée",
        "features": "Bungalow créole, piscine, véranda",
        "current_price": 150,
        "location": "Martinique"
    },
    "Villa Fête Ducos": {
        "description": "Jusqu'à 25 personnes",
        "features": "Piscine, bar extérieur, gazebo",
        "current_price": 200,
        "location": "Ducos, Martinique"
    },
    "Villa Fête Fort-de-France": {
        "description": "Jusqu'à 30 personnes",
        "features": "Piscine, véranda coloniale, vue panoramique",
        "current_price": 250,
        "location": "Fort-de-France, Martinique"
    },
    "Villa Fête Rivière-Pilote": {
        "description": "Jusqu'à 20 personnes",
        "features": "Villa créole, piscine tropicale",
        "current_price": 180,
        "location": "Rivière-Pilote, Martinique"
    },
    "Villa Fête Sainte-Luce": {
        "description": "Jusqu'à 35 personnes",
        "features": "Villa moderne, tentes, mobilier événementiel",
        "current_price": 220,
        "location": "Sainte-Luce, Martinique"
    },
    "Villa Fête Rivière-Salée": {
        "description": "Jusqu'à 15 personnes",
        "features": "Piscine, tente couverte",
        "current_price": 160,
        "location": "Rivière-Salée, Martinique"
    }
}

# VILLAS FICTIVES à supprimer (créées par erreur)
VILLAS_FICTIVES = [
    "Villa Sunset Paradise",
    "Villa Tropicale Zen", 
    "Villa Anses d'Arlet",
    "Villa Bord de Mer Tartane",
    "Villa Rivière-Pilote Charme",
    "Villa Marigot Exclusive",
    "Villa Sainte-Marie Familiale",
    "Studio Marin Cosy",
    "Villa Diamant Prestige",
    "Villa Carbet Deluxe",
    "Villa Océan Bleu",
    "Penthouse Schoelcher Vue Mer",
    "Villa François Moderne",
    "Villa Grand Luxe Pointe du Bout",
    "Bungalow Trenelle Nature",
    "Appartement Marina Fort-de-France",
    "Studio Ducos Pratique"
]

async def connect_to_mongo():
    """Connexion à MongoDB"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    return db

async def analyze_current_database():
    """Analyse de la base actuelle"""
    db = await connect_to_mongo()
    
    print("📊 ANALYSE DE LA BASE ACTUELLE")
    print("-" * 40)
    
    # Récupérer toutes les villas
    villas = await db.villas.find({}).to_list(None)
    
    print(f"Total villas en base: {len(villas)}")
    
    # Séparer vraies vs fictives
    vraies_villas_trouvees = []
    villas_fictives_trouvees = []
    villas_inconnues = []
    
    for villa in villas:
        nom = villa.get('name', '')
        if nom in VRAIES_VILLAS_SITE:
            vraies_villas_trouvees.append(nom)
        elif nom in VILLAS_FICTIVES:
            villas_fictives_trouvees.append(nom)
        else:
            villas_inconnues.append(nom)
    
    print(f"\n✅ VRAIES VILLAS TROUVÉES ({len(vraies_villas_trouvees)}):")
    for villa in sorted(vraies_villas_trouvees):
        print(f"   - {villa}")
    
    print(f"\n❌ VILLAS FICTIVES TROUVÉES ({len(villas_fictives_trouvees)}):")
    for villa in sorted(villas_fictives_trouvees):
        print(f"   - {villa}")
    
    print(f"\n❓ VILLAS INCONNUES ({len(villas_inconnues)}):")
    for villa in sorted(villas_inconnues):
        print(f"   - {villa}")
    
    # Villas manquantes
    villas_manquantes = []
    for villa_vraie in VRAIES_VILLAS_SITE:
        if villa_vraie not in vraies_villas_trouvees:
            villas_manquantes.append(villa_vraie)
    
    print(f"\n⚠️  VILLAS MANQUANTES ({len(villas_manquantes)}):")
    for villa in sorted(villas_manquantes):
        print(f"   - {villa}")
    
    return {
        'vraies_trouvees': vraies_villas_trouvees,
        'fictives_trouvees': villas_fictives_trouvees,
        'inconnues': villas_inconnues,
        'manquantes': villas_manquantes,
        'total_actuel': len(villas)
    }

async def supprimer_villas_fictives():
    """Supprime les villas fictives"""
    db = await connect_to_mongo()
    
    print(f"\n🗑️  SUPPRESSION DES VILLAS FICTIVES")
    print("-" * 40)
    
    supprimees = 0
    for villa_fictive in VILLAS_FICTIVES:
        result = await db.villas.delete_one({'name': villa_fictive})
        if result.deleted_count > 0:
            print(f"✅ Supprimée: {villa_fictive}")
            supprimees += 1
        else:
            print(f"⚠️  Pas trouvée: {villa_fictive}")
    
    print(f"\n📊 RÉSULTATS SUPPRESSION:")
    print(f"   - Villas supprimées: {supprimees}")
    print(f"   - Villas non trouvées: {len(VILLAS_FICTIVES) - supprimees}")
    
    return supprimees

async def creer_villas_manquantes():
    """Crée les villas manquantes basées sur le site web"""
    db = await connect_to_mongo()
    
    print(f"\n🆕 CRÉATION DES VILLAS MANQUANTES")
    print("-" * 40)
    
    # Récupérer les villas existantes
    villas_existantes = await db.villas.find({}, {'name': 1}).to_list(None)
    noms_existants = [v['name'] for v in villas_existantes]
    
    creees = 0
    for villa_name, villa_data in VRAIES_VILLAS_SITE.items():
        if villa_name not in noms_existants:
            # Créer la villa avec les données du site
            nouvelle_villa = {
                'id': str(len(await db.villas.find({}).to_list(None)) + 1),
                'name': villa_name,
                'location': villa_data['location'],
                'price': villa_data['current_price'],
                'guests': extract_guests_number(villa_data['description']),
                'features': villa_data['features'],
                'description': f"Villa {villa_name} - {villa_data['description']}",
                'category': determine_category(villa_name),
                'image': generate_image_path(villa_name),
                'gallery': generate_gallery_paths(villa_name),
                'fallback_icon': get_fallback_icon(villa_name),
                'amenities': extract_amenities(villa_data['features']),
                'created_at': datetime.utcnow(),
                'source': 'site_web_reel'
            }
            
            await db.villas.insert_one(nouvelle_villa)
            print(f"✅ Créée: {villa_name}")
            creees += 1
        else:
            print(f"⚠️  Existe déjà: {villa_name}")
    
    print(f"\n📊 RÉSULTATS CRÉATION:")
    print(f"   - Villas créées: {creees}")
    
    return creees

def extract_guests_number(description):
    """Extrait le nombre d'invités de la description"""
    import re
    match = re.search(r'(\d+)\s+personnes?', description)
    return int(match.group(1)) if match else 4

def determine_category(villa_name):
    """Détermine la catégorie de la villa"""
    if 'Fête' in villa_name or 'Journée' in villa_name:
        return 'fete'
    elif 'Studio' in villa_name or 'Bas' in villa_name:
        return 'special'
    else:
        return 'sejour'

def generate_image_path(villa_name):
    """Génère le chemin de l'image principale"""
    # Conversion simple du nom en chemin
    clean_name = villa_name.replace(' ', '_').replace('-', '_')
    return f"/images/{clean_name}/01_piscine_exterieur.jpg"

def generate_gallery_paths(villa_name):
    """Génère les chemins de galerie"""
    clean_name = villa_name.replace(' ', '_').replace('-', '_')
    return [
        f"/images/{clean_name}/01_piscine_exterieur.jpg",
        f"/images/{clean_name}/02_terrasse_salon.jpg",
        f"/images/{clean_name}/03_chambre_principale.jpg",
        f"/images/{clean_name}/04_cuisine_equipee.jpg",
        f"/images/{clean_name}/05_salle_bain.jpg",
        f"/images/{clean_name}/06_vue_panoramique.jpg"
    ]

def get_fallback_icon(villa_name):
    """Génère l'icône de fallback"""
    if 'Fête' in villa_name:
        return '🎉'
    elif 'Studio' in villa_name:
        return '💕'
    elif 'Piscine' in villa_name:
        return '🏊'
    elif 'F7' in villa_name:
        return '🏄'
    else:
        return '🏡'

def extract_amenities(features):
    """Extrait les équipements des features"""
    amenities = []
    features_lower = features.lower()
    
    if 'piscine' in features_lower:
        amenities.append('Piscine')
    if 'jacuzzi' in features_lower:
        amenities.append('Jacuzzi')
    if 'sauna' in features_lower:
        amenities.append('Sauna')
    if 'vue mer' in features_lower:
        amenities.append('Vue mer')
    if 'terrasse' in features_lower:
        amenities.append('Terrasse')
    if 'parking' in features_lower:
        amenities.append('Parking')
    
    # Ajouter équipements par défaut
    amenities.extend(['WiFi', 'Climatisation', 'Cuisine équipée'])
    
    return list(set(amenities))  # Supprimer les doublons

async def main():
    """Fonction principale Phase 1"""
    print("🔧 PHASE 1 : CORRECTION DE LA BASE")
    print("=" * 50)
    
    try:
        # Analyser la base actuelle
        analyse = await analyze_current_database()
        
        # Créer un backup
        db = await connect_to_mongo()
        villas_backup = await db.villas.find({}).to_list(None)
        
        with open('/app/backup_phase1.json', 'w') as f:
            json.dump(villas_backup, f, indent=2, default=str)
        print(f"\n💾 Backup créé: /app/backup_phase1.json")
        
        # Supprimer les villas fictives
        supprimees = await supprimer_villas_fictives()
        
        # Créer les villas manquantes
        creees = await creer_villas_manquantes()
        
        # Vérification finale
        villas_finales = await db.villas.find({}).to_list(None)
        
        print(f"\n📊 RÉSULTATS PHASE 1:")
        print(f"   - Villas au début: {analyse['total_actuel']}")
        print(f"   - Villas supprimées: {supprimees}")
        print(f"   - Villas créées: {creees}")
        print(f"   - Villas finales: {len(villas_finales)}")
        print(f"   - Objectif: {len(VRAIES_VILLAS_SITE)} vraies villas")
        
        # Rapport final
        rapport = {
            'phase': 1,
            'date': datetime.utcnow(),
            'villas_initiales': analyse['total_actuel'],
            'villas_supprimees': supprimees,
            'villas_creees': creees,
            'villas_finales': len(villas_finales),
            'objectif': len(VRAIES_VILLAS_SITE),
            'success': len(villas_finales) == len(VRAIES_VILLAS_SITE)
        }
        
        await db.correction_phase1_report.insert_one(rapport)
        
        if len(villas_finales) == len(VRAIES_VILLAS_SITE):
            print(f"\n✅ PHASE 1 TERMINÉE AVEC SUCCÈS")
            print(f"🎯 Base corrigée: {len(VRAIES_VILLAS_SITE)} vraies villas")
        else:
            print(f"\n⚠️  PHASE 1 TERMINÉE AVEC AVERTISSEMENT")
            print(f"🎯 {len(villas_finales)} villas au lieu de {len(VRAIES_VILLAS_SITE)} attendues")
        
    except Exception as e:
        print(f"❌ Erreur Phase 1: {e}")

if __name__ == "__main__":
    asyncio.run(main())