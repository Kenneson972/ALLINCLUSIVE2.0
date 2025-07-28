#!/usr/bin/env python3
"""
Script pour corriger la catégorie de Espace Piscine Journée Bungalow
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def fix_category():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['khanelconcept']
    collection = db['villas']
    
    print("🔧 CORRECTION DE LA CATÉGORIE ESPACE PISCINE")
    print("-" * 50)
    
    # Changer la catégorie de 'piscine' vers 'fete' pour Espace Piscine Journée Bungalow
    result = await collection.update_one(
        {'name': 'Espace Piscine Journée Bungalow'},
        {'$set': {'category': 'fete'}}
    )
    
    if result.modified_count > 0:
        print('✅ Catégorie changée: Espace Piscine Journée Bungalow -> fete')
    else:
        print('❌ Villa non trouvée ou déjà dans la bonne catégorie')
    
    # Vérifier les nouvelles catégories
    categories = await collection.distinct('category')
    print(f'✅ Catégories après correction: {sorted(categories)}')
    
    # Compter par catégorie avec une approche simple
    villas = await collection.find({}, {'category': 1}).to_list(None)
    category_counts = {}
    for villa in villas:
        cat = villa.get('category', 'unknown')
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    print('📊 Répartition par catégorie:')
    for cat, count in sorted(category_counts.items()):
        print(f'  {cat}: {count} villas')
    
    # Vérifier la villa Espace Piscine
    espace_villa = await collection.find_one({'name': 'Espace Piscine Journée Bungalow'})
    if espace_villa:
        print(f"✅ Villa trouvée: {espace_villa['name']} - €{espace_villa['price']} (catégorie: {espace_villa['category']})")
    
    client.close()
    print("\n🎉 CORRECTION TERMINÉE")

if __name__ == "__main__":
    asyncio.run(fix_category())