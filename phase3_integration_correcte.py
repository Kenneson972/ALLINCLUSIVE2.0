#!/usr/bin/env python3
"""
PHASE 3 : INTÉGRATION CORRECTE
Intégrer les données CSV dans les 6 vraies villas
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime

# Configuration MongoDB
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = 'khanelconcept'

# MAPPING CORRECT POUR LES 6 VRAIES VILLAS
MAPPING_6_VILLAS = {
    "Villa F3 Petit Macabou": {
        "csv_name": "Villa F3 sur Petit Macabou",
        "pricing": {
            "base_price": 850,
            "weekend": 850,
            "week": 1550,
            "high_season": 1690,
            "details": "Grandes Vacances: 1550€/semaine, Weekend: 850€ (2 nuits), Noël/Nouvel An: 1690€/semaine"
        },
        "description": "Villa avec possibilité d'accueillir 9 invités supplémentaires en journée (9h-20h). Caution: 1500€. Check-in: 16h, Check-out: 11h (possibilité extension jusqu'à 16h selon disponibilité).",
        "services": "Chambres climatisées, 1 salle de bain avec WC, WC indépendant, salon climatisé avec canapé-lit, sauna, jacuzzi, 2 douches extérieures",
        "guests": "6 personnes (jusqu'à 15 personnes en journée)",
        "location": "Petit Macabou, Vauclin"
    },
    "Villa F5 Ste Anne": {
        "csv_name": "Villa F5 sur Ste Anne",
        "pricing": {
            "base_price": 1350,
            "weekend": 1350,
            "week": 2251,
            "high_season": 2251,
            "details": "Weekend: 1350€ (2 nuits, hors vacances scolaires), Semaine: 2251€ (7 jours)"
        },
        "description": "Possibilité d'accueillir jusqu'à 15 invités de 9h à 19h. Caution: 500€ en espèces + 1500€ en empreinte CB. Facilités de paiement sans frais supplémentaires avec paiement total avant entrée.",
        "services": "4 chambres, 4 salles de bain",
        "guests": "10 personnes (jusqu'à 15 personnes en journée)",
        "location": "Quartier les Anglais, Ste Anne"
    },
    "Villa F3 POUR LA BACCHA": {
        "csv_name": "Villa F3 POUR LA BACCHA",
        "pricing": {
            "base_price": 1350,
            "weekend": 1350,
            "week": 1350,
            "high_season": 1350,
            "details": "Août: 1350€/semaine, Juillet: complet"
        },
        "description": "Possibilité d'accueillir jusqu'à 9 invités entre 9h et 18h. Caution: 1500€ par chèque. Règles strictes concernant le bruit pour respecter le voisinage.",
        "services": "2 chambres climatisées, salon climatisé avec canapé-lit",
        "guests": "6 personnes (jusqu'à 9 invités en journée)",
        "location": "Petit Macabou"
    },
    "Studio Cocooning Lamentin": {
        "csv_name": "Studio Cocooning Lamentin",
        "pricing": {
            "base_price": 290,
            "weekend": 290,
            "week": 2030,
            "high_season": 2030,
            "details": "À partir de 290€, minimum 2 nuits"
        },
        "description": "Pas d'invités autorisés. Location uniquement à la semaine pendant les vacances scolaires et haute saison touristique. Check-in: 16h, Check-out: 11h (départ tardif possible selon disponibilité). Paiement en plusieurs fois sans frais possible (tout doit être réglé avant entrée).",
        "services": "Bac à punch privé (petite piscine)",
        "guests": "2 personnes",
        "location": "Hauteurs de Morne Pitault, Lamentin"
    },
    "Villa F6 Petit Macabou": {
        "csv_name": "Villa F6 sur Petit Macabou (séjour + fête)",
        "pricing": {
            "base_price": 2000,
            "weekend": 2000,
            "week": 3220,
            "high_season": 3220,
            "details": "Weekend: 2000€, Semaine: à partir de 3220€"
        },
        "description": "Villa somptueuse et très spacieuse. Événements ou fêtes autorisés de 9h à 19h. Mariage ou baptême avec hébergements sur demande jusqu'à 150 invités. Covoiturage recommandé. Caution: 2500€ par chèque.",
        "services": "3 chambres climatisées avec salle de bain attenante, 1 mezzanine, 2 studios aux extrémités, possibilité de louer 3 bungalows supplémentaires avec bac à punch",
        "guests": "10 à 13 personnes (jusqu'à 30 invités pour fêtes)",
        "location": "Petit Macabou au Vauclin (972)"
    },
    "Espace Piscine Journée Bungalow": {
        "csv_name": "Espace Piscine Journée Bungalow",
        "pricing": {
            "base_price": 350,
            "up_to_20": 350,
            "up_to_40": 550,
            "up_to_60": 750,
            "bungalow_extra": 85,
            "details": "Forfaits Journée (9h-19h): Jusqu'à 20 invités 350€, Jusqu'à 40 invités: 550€, Jusqu'à 60 invités: 750€, Bungalow pour 2 personnes: +85€/nuit"
        },
        "description": "Location de 9h à 19h uniquement (pas de possibilité au-delà de 19h). Tarifs uniquement pour anniversaires, baby-showers et enterrements de vie. Caution: 1000€ par chèque + 250€ en espèces. Autres forfaits sur demande selon type d'événement (mariage, baptême, etc.).",
        "services": "Cuisine, salle d'eau, mobilier (chaises, tables), chambre climatisée (+80€ supplémentaire)",
        "guests": "10 à 150 personnes",
        "location": "Martinique"
    }
}

async def connect_to_mongo():
    """Connexion à MongoDB"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    return db

async def verifier_villas_base():
    """Vérifie les villas dans la base"""
    db = await connect_to_mongo()
    
    print("📊 VÉRIFICATION DES VILLAS EN BASE")
    print("-" * 40)
    
    villas = await db.villas.find({}).to_list(None)
    noms_villas = [villa['name'] for villa in villas]
    
    print(f"Villas en base: {len(villas)}")
    for nom in sorted(noms_villas):
        print(f"   - {nom}")
    
    return noms_villas

async def integrer_donnees_csv():
    """Intègre les données CSV dans chaque villa"""
    db = await connect_to_mongo()
    
    print("\n🔄 INTÉGRATION DES DONNÉES CSV")
    print("-" * 35)
    
    integrees = 0
    
    for villa_name, csv_data in MAPPING_6_VILLAS.items():
        try:
            # Chercher la villa
            villa = await db.villas.find_one({'name': villa_name})
            
            if not villa:
                print(f"❌ Villa non trouvée: {villa_name}")
                continue
            
            # Préparer les données de mise à jour
            update_data = {
                'price': csv_data['pricing']['base_price'],
                'pricing_details': csv_data['pricing'],
                'description': csv_data['description'],
                'services_full': csv_data['services'],
                'guests_detail': csv_data['guests'],
                'location': csv_data['location'],
                'features': csv_data['services'][:100] + '...' if len(csv_data['services']) > 100 else csv_data['services'],
                'csv_integrated': True,
                'csv_source': csv_data['csv_name'],
                'updated_at': datetime.utcnow()
            }
            
            # Mettre à jour la villa
            result = await db.villas.update_one(
                {'name': villa_name},
                {'$set': update_data}
            )
            
            if result.matched_count > 0:
                print(f"✅ {villa_name}")
                print(f"   Prix: {villa.get('price', 'N/A')}€ → {csv_data['pricing']['base_price']}€")
                print(f"   Source: {csv_data['csv_name']}")
                integrees += 1
            else:
                print(f"❌ Échec mise à jour: {villa_name}")
                
        except Exception as e:
            print(f"❌ Erreur {villa_name}: {e}")
    
    return integrees

async def verifier_integration():
    """Vérifie que l'intégration a fonctionné"""
    db = await connect_to_mongo()
    
    print(f"\n📊 VÉRIFICATION DE L'INTÉGRATION")
    print("-" * 35)
    
    # Compter les villas avec CSV intégré
    villas_avec_csv = await db.villas.count_documents({'csv_integrated': True})
    
    print(f"Villas avec CSV intégré: {villas_avec_csv}")
    
    # Afficher les détails
    villas = await db.villas.find({'csv_integrated': True}).to_list(None)
    
    for villa in sorted(villas, key=lambda x: x['name']):
        pricing = villa.get('pricing_details', {})
        print(f"   {villa['name']}: {pricing.get('base_price', 'N/A')}€")
    
    return villas_avec_csv

async def verifier_api():
    """Vérifie que l'API retourne les bonnes données"""
    print(f"\n🔍 VÉRIFICATION API")
    print("-" * 20)
    
    try:
        import requests
        response = requests.get("https://cfc0e6ef-086c-461a-915c-2319466028f1.preview.emergentagent.com/api/villas")
        
        if response.status_code == 200:
            villas = response.json()
            print(f"✅ API fonctionne: {len(villas)} villas")
            
            # Vérifier quelques villas
            for villa in villas[:3]:
                pricing = villa.get('pricing_details')
                if pricing:
                    print(f"   {villa['name']}: {pricing.get('base_price', 'N/A')}€ (CSV ✅)")
                else:
                    print(f"   {villa['name']}: {villa.get('price', 'N/A')}€ (CSV ❌)")
            
            return True
        else:
            print(f"❌ API erreur: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur API: {e}")
        return False

async def main():
    """Fonction principale Phase 3"""
    print("🔧 PHASE 3 : INTÉGRATION CORRECTE")
    print("=" * 40)
    
    try:
        # Vérifier les villas en base
        villas_base = await verifier_villas_base()
        
        if len(villas_base) != 6:
            print(f"⚠️  Attention: {len(villas_base)} villas au lieu de 6")
        
        # Intégrer les données CSV
        integrees = await integrer_donnees_csv()
        
        # Vérifier l'intégration
        villas_avec_csv = await verifier_integration()
        
        # Vérifier l'API
        api_ok = await verifier_api()
        
        # Rapport final
        db = await connect_to_mongo()
        rapport = {
            'phase': 3,
            'date': datetime.utcnow(),
            'villas_en_base': len(villas_base),
            'villas_integrees': integrees,
            'villas_avec_csv': villas_avec_csv,
            'api_functional': api_ok,
            'success': integrees == 6 and villas_avec_csv == 6
        }
        
        await db.integration_phase3_report.insert_one(rapport)
        
        print(f"\n📊 RÉSULTATS PHASE 3:")
        print(f"   - Villas en base: {len(villas_base)}")
        print(f"   - Villas intégrées: {integrees}")
        print(f"   - Villas avec CSV: {villas_avec_csv}")
        print(f"   - API fonctionnelle: {'✅' if api_ok else '❌'}")
        
        if integrees == 6 and villas_avec_csv == 6:
            print(f"\n✅ PHASE 3 TERMINÉE AVEC SUCCÈS")
            print(f"🎯 Toutes les villas ont leurs données CSV intégrées")
        else:
            print(f"\n⚠️  PHASE 3 TERMINÉE AVEC AVERTISSEMENT")
            print(f"🎯 {integrees}/{6} villas intégrées")
        
    except Exception as e:
        print(f"❌ Erreur Phase 3: {e}")

if __name__ == "__main__":
    asyncio.run(main())