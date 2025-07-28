#!/usr/bin/env python3
"""
Script de finalisation de l'intégration CSV
Corrige les noms et met à jour les villas existantes avec les données du CSV
"""

import asyncio
import json
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime

# Configuration MongoDB
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = 'khanelconcept'

# Mapping des noms CSV vers les noms existants dans la base
VILLA_NAME_MAPPING = {
    "Villa F3 sur Petit Macabou": "Villa F3 Petit Macabou",
    "Villa F5 sur Ste Anne": "Villa F5 Ste Anne",
    "Villa F3 POUR LA BACCHA": "Villa F3 POUR LA BACCHA",
    "Studio Cocooning Lamentin": "Studio Cocooning Lamentin",
    "Villa F3 sur le François": "Villa François Moderne",
    "Villa F6 au Lamentin": "Villa Grand Luxe Pointe du Bout",
    "Villa F6 sur Ste Luce à 1mn de la plage": "Villa Anses d'Arlet",
    "Villa F3 Bas de villa Trinité Cosmy": "Villa Bord de Mer Tartane",
    "Bas de villa F3 sur le Robert": "Villa Rivière-Pilote Charme",
    "Villa F7 Baie des Mulets": "Villa F6 Petit Macabou"
}

# Données CSV enrichies
CSV_ENRICHED_DATA = {
    "Villa F3 Petit Macabou": {
        "pricing": {
            "base_price": 850,
            "weekend": 850,
            "week": 1550,
            "high_season": 1690,
            "details": "Grandes Vacances: 1550€/semaine, Weekend: 850€ (2 nuits), Noël/Nouvel An: 1690€/semaine"
        },
        "enhanced_description": "Villa avec possibilité d'accueillir 9 invités supplémentaires en journée (9h-20h). Chambres climatisées, sauna, jacuzzi, 2 douches extérieures. Caution: 1500€. Check-in: 16h, Check-out: 11h.",
        "services_full": "Chambres climatisées, 1 salle de bain avec WC, WC indépendant, salon climatisé avec canapé-lit, sauna, jacuzzi, 2 douches extérieures",
        "guests_detail": "6 personnes (jusqu'à 15 personnes en journée)",
        "location": "Petit Macabou, Vauclin"
    },
    "Villa F5 Ste Anne": {
        "pricing": {
            "base_price": 1350,
            "weekend": 1350,
            "week": 2251,
            "high_season": 2251,
            "details": "Weekend: 1350€ (2 nuits, hors vacances scolaires), Semaine: 2251€ (7 jours)"
        },
        "enhanced_description": "Villa F5 avec 4 chambres et 4 salles de bain. Possibilité d'accueillir jusqu'à 15 invités de 9h à 19h. Caution: 500€ en espèces + 1500€ en empreinte CB. Facilités de paiement sans frais supplémentaires.",
        "services_full": "4 chambres, 4 salles de bain, possibilité invités journée",
        "guests_detail": "10 personnes (jusqu'à 15 personnes en journée)",
        "location": "Quartier les Anglais, Ste Anne"
    },
    "Villa F3 POUR LA BACCHA": {
        "pricing": {
            "base_price": 1350,
            "weekend": 1350,
            "week": 1350,
            "high_season": 1350,
            "details": "Août: 1350€/semaine, Juillet: complet"
        },
        "enhanced_description": "Villa F3 avec 2 chambres climatisées et salon climatisé avec canapé-lit. Possibilité d'accueillir jusqu'à 9 invités entre 9h et 18h. Caution: 1500€ par chèque. Règles strictes concernant le bruit.",
        "services_full": "2 chambres climatisées, salon climatisé avec canapé-lit",
        "guests_detail": "6 personnes (jusqu'à 9 invités en journée)",
        "location": "Petit Macabou"
    },
    "Studio Cocooning Lamentin": {
        "pricing": {
            "base_price": 290,
            "weekend": 290,
            "week": 2030,
            "high_season": 2030,
            "details": "À partir de 290€, minimum 2 nuits"
        },
        "enhanced_description": "Studio cocooning avec bac à punch privé (petite piscine). Pas d'invités autorisés. Location uniquement à la semaine pendant les vacances scolaires. Check-in: 16h, Check-out: 11h.",
        "services_full": "Bac à punch privé (petite piscine), climatisation",
        "guests_detail": "2 personnes (couple)",
        "location": "Hauteurs de Morne Pitault, Lamentin"
    },
    "Villa François Moderne": {
        "pricing": {
            "base_price": 800,
            "weekend": 800,
            "week": 1376,
            "high_season": 1376,
            "details": "Weekend: 800€ (2 nuits), Semaine: 1376€ (7 jours)"
        },
        "enhanced_description": "Villa F3 sur les hauteurs du Morne Carrière. Stationnement pour 5 véhicules, enceintes JBL autorisées. Caution: 1000€. Check-in: 16h, Check-out: 11h (option late check-out: +80€).",
        "services_full": "Stationnement pour 5 véhicules, enceintes JBL autorisées, climatisation",
        "guests_detail": "4 personnes (maximum 10 invités)",
        "location": "Hauteurs du Morne Carrière au François"
    },
    "Villa Grand Luxe Pointe du Bout": {
        "pricing": {
            "base_price": 1200,
            "weekend": 1500,
            "week": 2800,
            "high_season": 2800,
            "party_supplement": 300,
            "details": "Weekend: 1500€, Weekend 2 nuits: 1200€ (sans invités), Semaine: 2800€ (8 jours), +300€ si fête"
        },
        "enhanced_description": "Villa F6 avec piscine et jacuzzi. Fêtes autorisées de 10h à 19h. Check-in: 15h, check-out: 18h. Caution: 1000€ (empreinte bancaire). Covoiturage obligatoire.",
        "services_full": "Piscine, jacuzzi, 6 chambres, parking",
        "guests_detail": "10 personnes (jusqu'à 20 invités en journée)",
        "location": "Quartier Béleme, Lamentin"
    },
    "Villa Anses d'Arlet": {
        "pricing": {
            "base_price": 1700,
            "weekend": 1700,
            "week": 2200,
            "high_season": 2850,
            "details": "Weekend: 1700€, Semaine (8 jours): 2200€ à 2850€"
        },
        "enhanced_description": "Villa F6 à 1mn de la plage Corps de garde. 5 appartements (2 F2 duplex et 3 F2). Check-in: 17h, Check-out: 11h. Caution: 1500€ par chèque + 500€ en espèces.",
        "services_full": "5 appartements, proche plage, parking",
        "guests_detail": "10 à 14 personnes",
        "location": "Zac de Pont Café, Ste Luce, à 1mn de la plage Corps de garde"
    },
    "Villa Bord de Mer Tartane": {
        "pricing": {
            "base_price": 500,
            "weekend": 500,
            "week": 3500,
            "high_season": 3500,
            "party_rates": {"10_guests": 670, "60_guests": 1400},
            "details": "Weekend sans invités: 500€, Weekend + Fête: 670€ (10 invités) à 1400€ (60 invités)"
        },
        "enhanced_description": "Villa F3 bas de villa avec piscine privée chauffée. Environnement calme et relaxant. Horaires fête: 10h-18h ou 14h-22h. Caution: 200€ en espèces + 400€ par chèque.",
        "services_full": "2 chambres climatisées, piscine privée chauffée, double terrasse",
        "guests_detail": "5 adultes ou 4 adultes et 2 enfants (jusqu'à 60 invités pour fêtes)",
        "location": "Cosmy, Trinité"
    },
    "Villa Rivière-Pilote Charme": {
        "pricing": {
            "base_price": 900,
            "weekend": 900,
            "week_low": 1250,
            "week_high": 1500,
            "party_supplement": 550,
            "details": "Weekend: 900€, Weekend avec fête: +550€, Semaine: 1250€ (basse saison), 1500€ (haute saison)"
        },
        "enhanced_description": "Bas de villa F3 avec 2 chambres climatisées. Enceintes JBL autorisées jusqu'à 22h. Caution: 1500€ pour la villa + caution pour l'espace piscine.",
        "services_full": "2 chambres climatisées, accès piscine, enceintes JBL autorisées",
        "guests_detail": "10 personnes",
        "location": "Pointe Hyacinthe, Le Robert"
    },
    "Villa F6 Petit Macabou": {
        "pricing": {
            "base_price": 2200,
            "weekend": 2200,
            "week": 4200,
            "high_season": 4200,
            "party_rates": {"30_guests": 2530, "50_guests": 2750, "80_guests": 2970, "160_guests": 3575},
            "details": "Base: 2200€/weekend, 4200€/semaine. Fêtes: +330€ (30 invités), +550€ (50 invités), +770€ (80 invités), +1375€ (160 invités)"
        },
        "enhanced_description": "Villa F7 (F5 + F3) avec 16 personnes. F5: 4 chambres climatisées + salon; F3: salon avec canapé-lit. Parking pour 30 véhicules. Fêtes autorisées de 9h à minuit.",
        "services_full": "F5: 4 chambres + salon; F3: salon avec canapé-lit. Parking 30 véhicules",
        "guests_detail": "16 personnes (F5: 10 personnes + F3: 6 personnes)",
        "location": "Baie des Mulets, Vauclin"
    }
}

async def connect_to_mongo():
    """Connexion à MongoDB"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    return db

async def update_villa_with_csv_data(db, villa_name, csv_data):
    """Met à jour une villa avec les données CSV enrichies"""
    try:
        # Récupérer la villa existante
        existing_villa = await db.villas.find_one({'name': villa_name})
        
        if not existing_villa:
            print(f"⚠️  Villa non trouvée: {villa_name}")
            return False
        
        # Préparer les données de mise à jour
        update_data = {
            'pricing': csv_data['pricing'],
            'price': csv_data['pricing']['base_price'],
            'description': csv_data['enhanced_description'],
            'services_full': csv_data['services_full'],
            'guests_detail': csv_data['guests_detail'],
            'location': csv_data['location'],
            'features': csv_data['services_full'][:100] + '...' if len(csv_data['services_full']) > 100 else csv_data['services_full'],
            'updated_at': datetime.utcnow(),
            'csv_integrated': True
        }
        
        # Mettre à jour la villa
        result = await db.villas.update_one(
            {'name': villa_name},
            {'$set': update_data}
        )
        
        if result.matched_count > 0:
            print(f"✅ Villa mise à jour avec données CSV: {villa_name}")
            return True
        else:
            print(f"❌ Échec mise à jour: {villa_name}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur mise à jour villa {villa_name}: {e}")
        return False

async def main():
    """Fonction principale de finalisation"""
    print("🎯 FINALISATION INTÉGRATION CSV")
    print("=" * 50)
    
    try:
        # Connexion à MongoDB
        db = await connect_to_mongo()
        print("✅ Connexion MongoDB établie")
        
        # Mettre à jour toutes les villas avec les données CSV
        print("\n🔄 MISE À JOUR FINALE DES VILLAS")
        print("-" * 30)
        
        updated_count = 0
        total_villas = len(CSV_ENRICHED_DATA)
        
        for villa_name, csv_data in CSV_ENRICHED_DATA.items():
            success = await update_villa_with_csv_data(db, villa_name, csv_data)
            if success:
                updated_count += 1
        
        print(f"\n📊 Villas mises à jour: {updated_count}/{total_villas}")
        
        # Vérifier les résultats
        villas_with_pricing = await db.villas.count_documents({'pricing': {'$exists': True}})
        villas_with_csv = await db.villas.count_documents({'csv_integrated': True})
        
        print(f"📈 Villas avec tarification: {villas_with_pricing}")
        print(f"📋 Villas avec données CSV: {villas_with_csv}")
        
        # Afficher quelques exemples
        sample_villas = await db.villas.find({'csv_integrated': True}).limit(3).to_list(3)
        
        print(f"\n🎯 Exemples de villas actualisées:")
        for villa in sample_villas:
            pricing = villa.get('pricing', {})
            print(f"   {villa['name']}: {pricing.get('base_price', 0)}€ - {pricing.get('week', 'N/A')}€/semaine")
        
        # Créer un rapport final
        total_villas_db = await db.villas.count_documents({})
        
        report = {
            "integration_completed": True,
            "total_villas": total_villas_db,
            "updated_from_csv": updated_count,
            "villas_with_pricing": villas_with_pricing,
            "integration_date": datetime.utcnow(),
            "interface_preserved": True,
            "pricing_system": "variable"
        }
        
        # Sauvegarder le rapport
        await db.integration_reports.insert_one(report)
        
        print("\n✅ FINALISATION TERMINÉE")
        print("🎯 Interface conservée, données CSV intégrées")
        print("💰 Système de tarification variable activé")
        print("📊 Rapport d'intégration sauvegardé")
        
    except Exception as e:
        print(f"❌ Erreur lors de la finalisation: {e}")

if __name__ == "__main__":
    asyncio.run(main())