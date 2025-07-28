#!/usr/bin/env python3
"""
PHASE 1 CORRECTION : Corriger l'erreur d'ID dupliqué
"""

import asyncio
import json
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime
import uuid

# Configuration MongoDB
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = 'khanelconcept'

# VRAIES VILLAS manquantes (suite à l'erreur)
VILLAS_MANQUANTES = [
    "Villa Fête Rivière-Salée"
]

async def connect_to_mongo():
    """Connexion à MongoDB"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    return db

async def corriger_ids_dupliques():
    """Corrige les IDs dupliqués en utilisant des UUID"""
    db = await connect_to_mongo()
    
    print("🔧 CORRECTION DES IDS DUPLIQUÉS")
    print("-" * 35)
    
    # Récupérer toutes les villas
    villas = await db.villas.find({}).to_list(None)
    
    # Mettre à jour chaque villa avec un ID unique
    for villa in villas:
        new_id = str(uuid.uuid4())[:8]  # ID court et unique
        await db.villas.update_one(
            {'_id': villa['_id']},
            {'$set': {'id': new_id}}
        )
    
    print(f"✅ IDs corrigés pour {len(villas)} villas")

async def creer_villas_manquantes_fixe():
    """Crée les villas manquantes avec IDs uniques"""
    db = await connect_to_mongo()
    
    print("🆕 CRÉATION DES VILLAS MANQUANTES (AVEC IDS UNIQUES)")
    print("-" * 55)
    
    # Récupérer les villas existantes
    villas_existantes = await db.villas.find({}, {'name': 1}).to_list(None)
    noms_existants = [v['name'] for v in villas_existantes]
    
    # Données de la villa manquante
    villa_data = {
        "Villa Fête Rivière-Salée": {
            "description": "Jusqu'à 15 personnes",
            "features": "Piscine, tente couverte",
            "current_price": 160,
            "location": "Rivière-Salée, Martinique"
        }
    }
    
    creees = 0
    for villa_name, data in villa_data.items():
        if villa_name not in noms_existants:
            nouvelle_villa = {
                'id': str(uuid.uuid4())[:8],  # ID unique
                'name': villa_name,
                'location': data['location'],
                'price': data['current_price'],
                'guests': extract_guests_number(data['description']),
                'features': data['features'],
                'description': f"Villa {villa_name} - {data['description']}",
                'category': 'fete',
                'image': f"/images/{villa_name.replace(' ', '_')}/01_piscine_exterieur.jpg",
                'gallery': [
                    f"/images/{villa_name.replace(' ', '_')}/01_piscine_exterieur.jpg",
                    f"/images/{villa_name.replace(' ', '_')}/02_terrasse_salon.jpg",
                    f"/images/{villa_name.replace(' ', '_')}/03_vue_panoramique.jpg"
                ],
                'fallback_icon': '⛺',
                'amenities': ['Piscine', 'Tente couverte', 'WiFi', 'Parking'],
                'created_at': datetime.utcnow(),
                'source': 'site_web_reel'
            }
            
            await db.villas.insert_one(nouvelle_villa)
            print(f"✅ Créée: {villa_name}")
            creees += 1
    
    return creees

def extract_guests_number(description):
    """Extrait le nombre d'invités"""
    import re
    match = re.search(r'(\d+)\s+personnes?', description)
    return int(match.group(1)) if match else 4

async def verifier_villas_finales():
    """Vérifie l'état final des villas"""
    db = await connect_to_mongo()
    
    print("\n📊 VÉRIFICATION FINALE")
    print("-" * 25)
    
    villas = await db.villas.find({}).to_list(None)
    
    print(f"Total villas: {len(villas)}")
    
    # Lister toutes les villas
    print("\n📋 VILLAS DANS LA BASE:")
    for villa in sorted(villas, key=lambda x: x['name']):
        print(f"   - {villa['name']} (ID: {villa['id']})")
    
    return len(villas)

async def main():
    """Fonction principale de correction"""
    print("🔧 PHASE 1 - CORRECTION FINALE")
    print("=" * 35)
    
    try:
        # Corriger les IDs dupliqués
        await corriger_ids_dupliques()
        
        # Créer les villas manquantes
        creees = await creer_villas_manquantes_fixe()
        
        # Vérifier l'état final
        total_final = await verifier_villas_finales()
        
        print(f"\n✅ PHASE 1 TERMINÉE")
        print(f"🎯 {total_final} villas dans la base")
        print(f"📊 {creees} villas créées lors de cette correction")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    asyncio.run(main())