#!/usr/bin/env python3
"""
Ajouter Espace Piscine Journée Bungalow
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime
import uuid

# Configuration MongoDB
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = 'khanelconcept'

async def connect_to_mongo():
    """Connexion à MongoDB"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    return db

async def ajouter_espace_piscine():
    """Ajoute Espace Piscine Journée Bungalow"""
    db = await connect_to_mongo()
    
    print("🏊 AJOUT DE ESPACE PISCINE JOURNÉE BUNGALOW")
    print("-" * 45)
    
    # Vérifier si elle existe déjà
    existing = await db.villas.find_one({'name': 'Espace Piscine Journée Bungalow'})
    if existing:
        print("⚠️  Villa déjà présente")
        return
    
    # Créer la villa
    villa_espace_piscine = {
        'id': str(uuid.uuid4())[:8],
        'name': 'Espace Piscine Journée Bungalow',
        'location': 'Martinique',
        'price': 150,
        'guests': 8,
        'guests_detail': '8 personnes en journée',
        'features': 'Bungalow créole, piscine, véranda',
        'description': 'Espace piscine avec bungalow créole authentique. Idéal pour événements en journée.',
        'category': 'fete',
        'image': '/images/Espace_Piscine_Journee_Bungalow/01_piscine_exterieur.jpg',
        'gallery': [
            '/images/Espace_Piscine_Journee_Bungalow/01_piscine_exterieur.jpg',
            '/images/Espace_Piscine_Journee_Bungalow/02_bungalow_creole.jpg',
            '/images/Espace_Piscine_Journee_Bungalow/03_veranda.jpg',
            '/images/Espace_Piscine_Journee_Bungalow/04_espace_detente.jpg',
            '/images/Espace_Piscine_Journee_Bungalow/05_vue_ensemble.jpg',
            '/images/Espace_Piscine_Journee_Bungalow/06_terrasse.jpg'
        ],
        'fallback_icon': '🏊',
        'amenities': ['Piscine', 'Bungalow', 'Véranda', 'Terrasse', 'Parking', 'WiFi'],
        'created_at': datetime.utcnow(),
        'source': 'site_web_reel'
    }
    
    # Insérer la villa
    await db.villas.insert_one(villa_espace_piscine)
    print("✅ Espace Piscine Journée Bungalow ajouté")

async def verifier_total():
    """Vérifie le total final"""
    db = await connect_to_mongo()
    
    villas = await db.villas.find({}).to_list(None)
    
    print(f"\n📊 TOTAL FINAL: {len(villas)} villas")
    
    for villa in sorted(villas, key=lambda x: x['name']):
        print(f"   - {villa['name']}")
    
    return len(villas)

async def main():
    """Fonction principale"""
    try:
        await ajouter_espace_piscine()
        total = await verifier_total()
        
        if total == 6:
            print(f"\n✅ SUCCÈS: {total} vraies villas dans la base")
        else:
            print(f"\n⚠️  ATTENTION: {total} villas au lieu de 6")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    asyncio.run(main())