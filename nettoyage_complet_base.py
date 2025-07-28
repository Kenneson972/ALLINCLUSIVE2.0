#!/usr/bin/env python3
"""
NETTOYAGE COMPLET DE LA BASE
Supprimer toutes les villas fictives et ne garder que les vraies villas du site
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime

# Configuration MongoDB
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = 'khanelconcept'

# VRAIES VILLAS (exactement celles du site web)
VRAIES_VILLAS_EXACTES = [
    "Villa F3 Petit Macabou",
    "Villa F5 Ste Anne", 
    "Villa F3 POUR LA BACCHA",
    "Studio Cocooning Lamentin",
    "Villa F6 Petit Macabou",
    "Espace Piscine Journée Bungalow"
]

# TOUTES LES AUTRES SONT FICTIVES
TOUTES_VILLAS_FICTIVES = [
    "Appartement Marina Fort-de-France",
    "Bungalow Trenelle Nature",
    "Penthouse Schoelcher Vue Mer",
    "Studio Ducos Pratique",
    "Studio Marin Cosy",
    "Villa Anses d'Arlet",
    "Villa Bord de Mer Tartane",
    "Villa Carbet Deluxe",
    "Villa Diamant Prestige",
    "Villa François Moderne",
    "Villa Grand Luxe Pointe du Bout",
    "Villa Marigot Exclusive",
    "Villa Océan Bleu",
    "Villa Rivière-Pilote Charme",
    "Villa Sainte-Marie Familiale",
    "Villa Sunset Paradise",
    "Villa Tropicale Zen",
    "Villa Fête Rivière-Salée"
]

async def connect_to_mongo():
    """Connexion à MongoDB"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    return db

async def analyser_base_actuelle():
    """Analyse de la base actuelle"""
    db = await connect_to_mongo()
    
    print("📊 ANALYSE DE LA BASE ACTUELLE")
    print("-" * 35)
    
    villas = await db.villas.find({}).to_list(None)
    noms_villas = [villa['name'] for villa in villas]
    
    print(f"Total villas: {len(villas)}")
    
    vraies_trouvees = []
    fictives_trouvees = []
    
    for nom in noms_villas:
        if nom in VRAIES_VILLAS_EXACTES:
            vraies_trouvees.append(nom)
        else:
            fictives_trouvees.append(nom)
    
    print(f"\n✅ VRAIES VILLAS TROUVÉES ({len(vraies_trouvees)}):")
    for villa in sorted(vraies_trouvees):
        print(f"   - {villa}")
    
    print(f"\n❌ VILLAS FICTIVES TROUVÉES ({len(fictives_trouvees)}):")
    for villa in sorted(fictives_trouvees):
        print(f"   - {villa}")
    
    return vraies_trouvees, fictives_trouvees

async def supprimer_toutes_villas_fictives():
    """Supprime toutes les villas fictives"""
    db = await connect_to_mongo()
    
    print("\n🗑️  SUPPRESSION DE TOUTES LES VILLAS FICTIVES")
    print("-" * 45)
    
    # Supprimer toutes les villas qui ne sont pas dans la liste des vraies villas
    result = await db.villas.delete_many({
        'name': {'$nin': VRAIES_VILLAS_EXACTES}
    })
    
    print(f"✅ {result.deleted_count} villas fictives supprimées")
    
    return result.deleted_count

async def verifier_resultats():
    """Vérifie les résultats après nettoyage"""
    db = await connect_to_mongo()
    
    print("\n📊 VÉRIFICATION APRÈS NETTOYAGE")
    print("-" * 35)
    
    villas_restantes = await db.villas.find({}).to_list(None)
    
    print(f"Villas restantes: {len(villas_restantes)}")
    
    for villa in sorted(villas_restantes, key=lambda x: x['name']):
        print(f"   - {villa['name']}")
    
    return len(villas_restantes)

async def main():
    """Fonction principale de nettoyage"""
    print("🧹 NETTOYAGE COMPLET DE LA BASE")
    print("=" * 40)
    
    try:
        # Analyser la base actuelle
        vraies, fictives = await analyser_base_actuelle()
        
        # Créer backup avant suppression
        db = await connect_to_mongo()
        backup_villas = await db.villas.find({}).to_list(None)
        
        with open('/app/backup_avant_nettoyage.json', 'w') as f:
            import json
            json.dump(backup_villas, f, indent=2, default=str)
        
        print(f"\n💾 Backup créé: /app/backup_avant_nettoyage.json")
        
        # Supprimer toutes les villas fictives
        supprimees = await supprimer_toutes_villas_fictives()
        
        # Vérifier les résultats
        villas_finales = await verifier_resultats()
        
        print(f"\n📊 RÉSULTATS DU NETTOYAGE:")
        print(f"   - Villas au début: {len(backup_villas)}")
        print(f"   - Villas supprimées: {supprimees}")
        print(f"   - Villas restantes: {villas_finales}")
        print(f"   - Objectif: {len(VRAIES_VILLAS_EXACTES)} vraies villas")
        
        # Rapport
        rapport = {
            'operation': 'nettoyage_complet',
            'date': datetime.utcnow(),
            'villas_initiales': len(backup_villas),
            'villas_supprimees': supprimees,
            'villas_finales': villas_finales,
            'objectif': len(VRAIES_VILLAS_EXACTES),
            'success': villas_finales == len(VRAIES_VILLAS_EXACTES)
        }
        
        await db.nettoyage_complet_report.insert_one(rapport)
        
        if villas_finales == len(VRAIES_VILLAS_EXACTES):
            print(f"\n✅ NETTOYAGE TERMINÉ AVEC SUCCÈS")
            print(f"🎯 Base propre avec {len(VRAIES_VILLAS_EXACTES)} vraies villas")
        else:
            print(f"\n⚠️  NETTOYAGE TERMINÉ AVEC AVERTISSEMENT")
            print(f"🎯 {villas_finales} villas au lieu de {len(VRAIES_VILLAS_EXACTES)} attendues")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    asyncio.run(main())