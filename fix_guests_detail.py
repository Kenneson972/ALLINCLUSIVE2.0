#!/usr/bin/env python3
"""
Correction du champ guests_detail manquant
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os

# Configuration MongoDB
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = 'khanelconcept'

async def connect_to_mongo():
    """Connexion à MongoDB"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    return db

async def fix_guests_detail():
    """Ajoute le champ guests_detail manquant"""
    db = await connect_to_mongo()
    
    print("🔧 CORRECTION DU CHAMP GUESTS_DETAIL")
    print("-" * 40)
    
    # Récupérer toutes les villas sans guests_detail
    villas_sans_guests_detail = await db.villas.find({
        'guests_detail': {'$exists': False}
    }).to_list(None)
    
    print(f"Villas sans guests_detail: {len(villas_sans_guests_detail)}")
    
    # Corriger chaque villa
    for villa in villas_sans_guests_detail:
        guests_count = villa.get('guests', 4)
        villa_name = villa.get('name', '')
        
        # Générer guests_detail basé sur le nom et le nombre d'invités
        if 'Fête' in villa_name:
            guests_detail = f"Jusqu'à {guests_count} personnes"
        elif 'Studio' in villa_name:
            guests_detail = f"{guests_count} personnes (couple)"
        elif 'Bas' in villa_name:
            guests_detail = f"{guests_count} personnes"
        else:
            guests_detail = f"{guests_count} personnes"
        
        # Mettre à jour la villa
        await db.villas.update_one(
            {'_id': villa['_id']},
            {'$set': {'guests_detail': guests_detail}}
        )
        
        print(f"✅ Corrigé: {villa_name} → {guests_detail}")
    
    print(f"\n📊 {len(villas_sans_guests_detail)} villas corrigées")

async def main():
    """Fonction principale"""
    try:
        await fix_guests_detail()
        print("\n✅ CORRECTION TERMINÉE")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    asyncio.run(main())