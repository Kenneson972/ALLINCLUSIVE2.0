#!/usr/bin/env python3
"""
Script de mise à jour du système de tarification
Intègre les tarifs variables du CSV dans l'API
"""

import asyncio
import json
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime

# Configuration MongoDB
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = 'khanelconcept'

# Tarifs détaillés par villa (extraits du CSV)
TARIFS_DETAILLES = {
    "Villa F3 sur Petit Macabou": {
        "base_price": 850,
        "weekend": 850,
        "week": 1550,
        "high_season": 1690,
        "details": "Grandes Vacances: 1550€/semaine, Weekend: 850€ (2 nuits), Noël/Nouvel An: 1690€/semaine"
    },
    "Villa F3 POUR LA BACCHA": {
        "base_price": 1350,
        "weekend": 1350,
        "week": 1350,
        "high_season": 1350,
        "details": "Août: 1350€/semaine, Juillet: complet"
    },
    "Villa F3 sur le François": {
        "base_price": 800,
        "weekend": 800,
        "week": 1376,
        "high_season": 1376,
        "details": "Weekend: 800€ (2 nuits), Semaine: 1376€ (7 jours)"
    },
    "Villa F5 sur Ste Anne": {
        "base_price": 1350,
        "weekend": 1350,
        "week": 2251,
        "high_season": 2251,
        "details": "Weekend: 1350€ (2 nuits, hors vacances scolaires), Semaine: 2251€ (7 jours)"
    },
    "Villa F6 au Lamentin": {
        "base_price": 1200,
        "weekend": 1500,
        "week": 2800,
        "high_season": 2800,
        "details": "Weekend: 1500€ (vendredi-dimanche), Weekend 2 nuits: 1200€ (sans invités), Semaine: 2800€ (8 jours), +300€ si fête"
    },
    "Villa F6 sur Ste Luce à 1mn de la plage": {
        "base_price": 1700,
        "weekend": 1700,
        "week": 2200,
        "high_season": 2850,
        "details": "Weekend: 1700€, Semaine (8 jours): 2200€ à 2850€"
    },
    "Villa F3 Bas de villa Trinité Cosmy": {
        "base_price": 500,
        "weekend": 500,
        "week": 3500,
        "high_season": 3500,
        "party_rates": {
            "10_guests": 670,
            "60_guests": 1400
        },
        "details": "Weekend sans invités: 500€, Weekend + Fête: 670€ (10 invités) à 1400€ (60 invités)"
    },
    "Bas de villa F3 sur le Robert": {
        "base_price": 900,
        "weekend": 900,
        "week_low": 1250,
        "week_high": 1500,
        "party_supplement": 550,
        "details": "Weekend: 900€, Weekend avec fête/invités: +550€, Semaine: 1250€ (basse saison), 1500€ (haute saison)"
    },
    "Villa F7 Baie des Mulets": {
        "base_price": 2200,
        "weekend": 2200,
        "week": 4200,
        "high_season": 4200,
        "party_rates": {
            "30_guests": 2530,
            "50_guests": 2750,
            "80_guests": 2970,
            "160_guests": 3575
        },
        "details": "Base: 2200€/weekend, 4200€/semaine. Fêtes: +330€ (30 invités), +550€ (50 invités), +770€ (80 invités), +1375€ (160 invités)"
    },
    "Studio Cocooning Lamentin": {
        "base_price": 290,
        "weekend": 290,
        "week": 2030,
        "high_season": 2030,
        "details": "À partir de 290€, minimum 2 nuits"
    }
}

async def connect_to_mongo():
    """Connexion à MongoDB"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    return db

async def update_villa_pricing(db, villa_name, pricing_data):
    """Met à jour les tarifs d'une villa"""
    try:
        # Créer l'objet de mise à jour
        update_data = {
            'pricing': pricing_data,
            'price': pricing_data['base_price'],  # Prix d'affichage par défaut
            'pricing_updated_at': datetime.utcnow()
        }
        
        # Mettre à jour la villa
        result = await db.villas.update_one(
            {'name': villa_name},
            {'$set': update_data}
        )
        
        if result.matched_count > 0:
            print(f"✅ Tarifs mis à jour: {villa_name}")
            return True
        else:
            print(f"⚠️  Villa non trouvée: {villa_name}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur mise à jour tarifs {villa_name}: {e}")
        return False

async def create_pricing_api_endpoint():
    """Crée les données pour l'endpoint de calcul de prix"""
    
    # Règles de calcul des prix
    pricing_rules = {
        "seasons": {
            "low": {
                "name": "Basse saison",
                "months": [4, 5, 6, 9, 10, 11],
                "multiplier": 1.0
            },
            "high": {
                "name": "Haute saison",
                "months": [7, 8, 12, 1, 2, 3],
                "multiplier": 1.2
            },
            "peak": {
                "name": "Très haute saison",
                "periods": ["2024-12-20/2025-01-05", "2024-07-01/2024-08-31"],
                "multiplier": 1.5
            }
        },
        "duration": {
            "weekend": {"min_nights": 2, "max_nights": 3, "multiplier": 1.0},
            "week": {"min_nights": 7, "max_nights": 14, "multiplier": 0.9},
            "month": {"min_nights": 28, "max_nights": 60, "multiplier": 0.8}
        },
        "party_supplements": {
            "enabled": True,
            "max_guests_standard": 15,
            "supplement_per_guest": 25
        }
    }
    
    return pricing_rules

async def main():
    """Fonction principale de mise à jour des tarifs"""
    print("💰 MISE À JOUR SYSTÈME DE TARIFICATION")
    print("=" * 50)
    
    try:
        # Connexion à MongoDB
        db = await connect_to_mongo()
        print("✅ Connexion MongoDB établie")
        
        # Mettre à jour les tarifs de chaque villa
        print("\n🔄 MISE À JOUR DES TARIFS")
        print("-" * 30)
        
        updated_count = 0
        for villa_name, pricing_data in TARIFS_DETAILLES.items():
            success = await update_villa_pricing(db, villa_name, pricing_data)
            if success:
                updated_count += 1
        
        print(f"\n📊 Villas avec tarifs mis à jour: {updated_count}/{len(TARIFS_DETAILLES)}")
        
        # Créer les règles de tarification
        pricing_rules = await create_pricing_api_endpoint()
        
        # Sauvegarder les règles dans une collection
        await db.pricing_rules.replace_one(
            {'type': 'general'},
            {
                'type': 'general',
                'rules': pricing_rules,
                'updated_at': datetime.utcnow()
            },
            upsert=True
        )
        
        print("✅ Règles de tarification créées")
        
        # Vérifier les résultats
        sample_villas = await db.villas.find({'pricing': {'$exists': True}}).limit(3).to_list(3)
        
        print(f"\n📈 Exemples de villas avec tarifs variables:")
        for villa in sample_villas:
            pricing = villa.get('pricing', {})
            print(f"   {villa['name']}: {pricing.get('base_price', 0)}€ - {pricing.get('week', 0)}€")
        
        print("\n✅ MISE À JOUR TERMINÉE")
        print("🎯 Système de tarification variable opérationnel")
        
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {e}")

if __name__ == "__main__":
    asyncio.run(main())