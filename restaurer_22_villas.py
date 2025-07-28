#!/usr/bin/env python3
"""
Restaurer les 22 vraies villas originales du site
"""

import asyncio
import json
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime

# Configuration MongoDB
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = 'khanelconcept'

async def connect_to_mongo():
    """Connexion à MongoDB"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    return db

async def restaurer_villas_originales():
    """Restaure les 22 villas originales depuis le backup"""
    db = await connect_to_mongo()
    
    print("🔄 RESTAURATION DES 22 VILLAS ORIGINALES")
    print("=" * 45)
    
    try:
        # Lire le backup
        with open('/app/backup_avant_nettoyage.json', 'r') as f:
            backup_villas = json.load(f)
        
        print(f"📋 {len(backup_villas)} villas dans le backup")
        
        # Vider la collection actuelle
        await db.villas.delete_many({})
        print("🗑️  Collection vidée")
        
        # Restaurer toutes les villas du backup
        for villa in backup_villas:
            # Nettoyer l'ID MongoDB
            if '_id' in villa:
                del villa['_id']
            
            # Ajouter un timestamp de restauration
            villa['restored_at'] = datetime.utcnow()
            
            await db.villas.insert_one(villa)
        
        print(f"✅ {len(backup_villas)} villas restaurées")
        
        # Vérifier la restauration
        villas_restaurees = await db.villas.find({}).to_list(None)
        
        print(f"\n📊 VILLAS RESTAURÉES ({len(villas_restaurees)}):")
        for villa in sorted(villas_restaurees, key=lambda x: x['name']):
            print(f"   - {villa['name']}")
        
        return len(villas_restaurees)
        
    except Exception as e:
        print(f"❌ Erreur lors de la restauration: {e}")
        return 0

async def main():
    """Fonction principale"""
    try:
        total_restaurees = await restaurer_villas_originales()
        
        if total_restaurees == 22:
            print(f"\n✅ RESTAURATION RÉUSSIE")
            print(f"🎯 {total_restaurees} vraies villas restaurées")
        else:
            print(f"\n⚠️  RESTAURATION PARTIELLE")
            print(f"🎯 {total_restaurees} villas restaurées")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    asyncio.run(main())