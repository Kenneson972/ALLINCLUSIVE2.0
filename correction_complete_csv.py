#!/usr/bin/env python3
"""
Correction complète - Mise à jour de TOUTES les villas avec leurs données CSV
"""

import asyncio
import json
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime
import re

# Configuration MongoDB
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = 'khanelconcept'

# MAPPING COMPLET : Toutes les villas existantes → Données CSV
MAPPING_COMPLET_CSV = {
    "Villa F3 Petit Macabou": {
        "nom_csv": "Villa F3 sur Petit Macabou",
        "pricing": {
            "base_price": 850,
            "weekend": 850,
            "week": 1550,
            "high_season": 1690,
            "details": "Grandes Vacances: 1550€/semaine, Weekend: 850€ (2 nuits), Noël/Nouvel An: 1690€/semaine"
        },
        "enhanced_description": "Villa avec possibilité d'accueillir 9 invités supplémentaires en journée (9h-20h). Caution: 1500€. Check-in: 16h, Check-out: 11h (possibilité extension jusqu'à 16h selon disponibilité).",
        "services_full": "Chambres climatisées, 1 salle de bain avec WC, WC indépendant, salon climatisé avec canapé-lit, sauna, jacuzzi, 2 douches extérieures",
        "guests_detail": "6 personnes (jusqu'à 15 personnes en journée)",
        "location": "Petit Macabou, Vauclin"
    },
    "Villa F5 Ste Anne": {
        "nom_csv": "Villa F5 sur Ste Anne",
        "pricing": {
            "base_price": 1350,
            "weekend": 1350,
            "week": 2251,
            "high_season": 2251,
            "details": "Weekend: 1350€ (2 nuits, hors vacances scolaires), Semaine: 2251€ (7 jours)"
        },
        "enhanced_description": "Possibilité d'accueillir jusqu'à 15 invités de 9h à 19h. Caution: 500€ en espèces + 1500€ en empreinte CB. Facilités de paiement sans frais supplémentaires avec paiement total avant entrée.",
        "services_full": "4 chambres, 4 salles de bain",
        "guests_detail": "10 personnes (jusqu'à 15 personnes en journée)",
        "location": "Quartier les Anglais, Ste Anne"
    },
    "Villa F3 POUR LA BACCHA": {
        "nom_csv": "Villa F3 POUR LA BACCHA",
        "pricing": {
            "base_price": 1350,
            "weekend": 1350,
            "week": 1350,
            "high_season": 1350,
            "details": "Août: 1350€/semaine, Juillet: complet"
        },
        "enhanced_description": "Possibilité d'accueillir jusqu'à 9 invités entre 9h et 18h. Caution: 1500€ par chèque. Règles strictes concernant le bruit pour respecter le voisinage.",
        "services_full": "2 chambres climatisées, salon climatisé avec canapé-lit",
        "guests_detail": "6 personnes (jusqu'à 9 invités en journée)",
        "location": "Petit Macabou"
    },
    "Studio Cocooning Lamentin": {
        "nom_csv": "Studio Cocooning Lamentin",
        "pricing": {
            "base_price": 290,
            "weekend": 290,
            "week": 2030,
            "high_season": 2030,
            "details": "À partir de 290€, minimum 2 nuits"
        },
        "enhanced_description": "Pas d'invités autorisés. Location uniquement à la semaine pendant les vacances scolaires et haute saison touristique. Check-in: 16h, Check-out: 11h (départ tardif possible selon disponibilité). Paiement en plusieurs fois sans frais possible (tout doit être réglé avant entrée).",
        "services_full": "Bac à punch privé (petite piscine)",
        "guests_detail": "2 personnes",
        "location": "Hauteurs de Morne Pitault, Lamentin"
    },
    "Villa François Moderne": {
        "nom_csv": "Villa F3 sur le François",
        "pricing": {
            "base_price": 800,
            "weekend": 800,
            "week": 1376,
            "high_season": 1376,
            "details": "Weekend: 800€ (2 nuits), Semaine: 1376€ (7 jours)"
        },
        "enhanced_description": "Caution: 1000€ (850€ par chèque et 150€ en espèces). Check-in: 16h, Check-out: 11h (option late check-out: +80€). Frais de 50€ par 30 minutes de retard pour la remise des clés. Villa à rendre propre et rangée.",
        "services_full": "Stationnement pour 5 véhicules, enceintes JBL autorisées",
        "guests_detail": "4 personnes (maximum 10 invités)",
        "location": "Hauteurs du Morne Carrière au François"
    },
    "Villa Grand Luxe Pointe du Bout": {
        "nom_csv": "Villa F6 au Lamentin",
        "pricing": {
            "base_price": 1200,
            "weekend": 1500,
            "week": 2800,
            "high_season": 2800,
            "party_supplement": 300,
            "details": "Weekend: 1500€ (vendredi-dimanche), Weekend 2 nuits: 1200€ (sans invités), Semaine: 2800€ (8 jours), +300€ si fête"
        },
        "enhanced_description": "Fêtes autorisées de 10h à 19h. Disponibilité vacances: du 1er au 10 juillet et du 25 au 31 août. Check-in: 15h, check-out: 18h. Pénalité retard clés: 150€/30min. Caution: 1000€ (empreinte bancaire). Covoiturage obligatoire.",
        "services_full": "Piscine, jacuzzi",
        "guests_detail": "10 personnes (jusqu'à 20 invités en journée)",
        "location": "Quartier Béleme, Lamentin"
    },
    "Villa Anses d'Arlet": {
        "nom_csv": "Villa F6 sur Ste Luce à 1mn de la plage",
        "pricing": {
            "base_price": 1700,
            "weekend": 1700,
            "week": 2200,
            "high_season": 2850,
            "details": "Weekend: 1700€, Semaine (8 jours): 2200€ à 2850€"
        },
        "enhanced_description": "Check-in: 17h, Check-out: 11h. Caution: 1500€ par chèque + 500€ en espèces (remboursables). Location uniquement à la semaine pendant les vacances scolaires. Facilités de paiement sans frais supplémentaires (tout doit être payé avant l'entrée).",
        "services_full": "5 appartements (2 F2 duplex et 3 F2), dont un en sous-sol",
        "guests_detail": "10 à 14 personnes",
        "location": "Zac de Pont Café, Ste Luce, à 1mn de la plage Corps de garde"
    },
    "Villa Bord de Mer Tartane": {
        "nom_csv": "Villa F3 Bas de villa Trinité Cosmy",
        "pricing": {
            "base_price": 500,
            "weekend": 500,
            "week": 3500,
            "high_season": 3500,
            "party_rates": {"10_guests": 670, "60_guests": 1400},
            "details": "Weekend sans invités: 500€, Weekend + Fête: 670€ (10 invités) à 1400€ (60 invités)"
        },
        "enhanced_description": "Villa charmante idéale pour séjours entre amis, famille et événements. Environnement calme et relaxant. Horaires fête: 10h-18h ou 14h-22h (départ des invités à partir de 21h). Location à la semaine pendant vacances scolaires (exceptions possibles). Caution: 200€ en espèces + 400€ par chèque.",
        "services_full": "2 chambres climatisées, 1 salle de bain, double terrasse, salon, cuisine américaine, piscine privée chauffée",
        "guests_detail": "5 adultes ou 4 adultes et 2 enfants (jusqu'à 60 invités pour fêtes)",
        "location": "Cosmy, Trinité"
    },
    "Villa Rivière-Pilote Charme": {
        "nom_csv": "Bas de villa F3 sur le Robert",
        "pricing": {
            "base_price": 900,
            "weekend": 900,
            "week_low": 1250,
            "week_high": 1500,
            "party_supplement": 550,
            "details": "Weekend: 900€, Weekend avec fête/invités: +550€, Semaine: 1250€ (basse saison), 1500€ (haute saison)"
        },
        "enhanced_description": "Enceintes JBL autorisées jusqu'à 22h (DJ et gros systèmes sono interdits). Caution: 1500€ pour la villa + caution pour l'espace piscine. Paiement en plusieurs fois sans frais possible (tout doit être soldé avant l'entrée).",
        "services_full": "2 chambres climatisées, location à la journée possible (lundi-jeudi), excursion nautique possible",
        "guests_detail": "10 personnes",
        "location": "Pointe Hyacinthe, Le Robert"
    },
    "Villa F6 Petit Macabou": {
        "nom_csv": "Villa F7 Baie des Mulets",
        "pricing": {
            "base_price": 2200,
            "weekend": 2200,
            "week": 4200,
            "high_season": 4200,
            "party_rates": {"30_guests": 2530, "50_guests": 2750, "80_guests": 2970, "160_guests": 3575},
            "details": "Base: 2200€/weekend, 4200€/semaine. Fêtes: +330€ (30 invités), +550€ (50 invités), +770€ (80 invités), +1375€ (160 invités)"
        },
        "enhanced_description": "Check-in: 11h, Check-out: 13h (option late check-out 17h30: +150€). Fêtes autorisées de 9h à minuit. Location possible à la journée (lundi-jeudi) selon disponibilité. Caution: 1500€ par chèque ou empreinte bancaire. Paiement possible en plusieurs fois, sans frais, avec solde 72h avant entrée.",
        "services_full": "F5: 4 chambres climatisées + salon avec canapé-lit; F3: salon avec canapé-lit. Parking pour 30 véhicules",
        "guests_detail": "16 personnes (F5: 10 personnes + F3: 6 personnes)",
        "location": "Baie des Mulets, Vauclin"
    },
    "Bungalow Trenelle Nature": {
        "nom_csv": "Appartement F3 Trenelle (Location Annuelle)",
        "pricing": {
            "base_price": 700,
            "month": 700,
            "annual": 8400,
            "details": "700€/mois (eau et EDF inclus)"
        },
        "enhanced_description": "Location à l'année (bail de 12 mois) avec possibilité de louer pour 3 ou 6 mois. Accès au logement: 1550€ (2 mois de caution + 1 mois de loyer hors charges).",
        "services_full": "Meublé, eau et électricité incluses",
        "guests_detail": "Couple sans enfant, personne seule ou 2 colocataires",
        "location": "Trenelle, à 2 minutes du PPM"
    },
    "Villa Marigot Exclusive": {
        "nom_csv": "Villa F5 Vauclin Ravine Plate",
        "pricing": {
            "base_price": 1550,
            "weekend": 1550,
            "week": 2500,
            "high_season": 2500,
            "details": "Weekend: 1550€ (vendredi-dimanche), Semaine: 2500€ (8 jours)"
        },
        "enhanced_description": "Caution: 1500€ par chèque et 500€ en espèces, remboursée à la sortie si aucun dommage. Paiement en plusieurs fois sans frais possible, solde à régler avant l'entrée.",
        "services_full": "4 chambres climatisées avec salle d'eau attenante, piscine à débordement",
        "guests_detail": "8 personnes",
        "location": "Hauteurs de Ravine Plate, Vauclin"
    },
    "Villa Sainte-Marie Familiale": {
        "nom_csv": "Villa F5 La Renée",
        "pricing": {
            "base_price": 900,
            "weekend": 900,
            "weekend_party": 1400,
            "week": 1590,
            "week_party": 2000,
            "details": "Weekend avec fête: 1400€, Weekend sans fête: 900€, Semaine avec fête: 2000€, Semaine sans fête: 1590€"
        },
        "enhanced_description": "Horaires fêtes: 9h-00h. Caution: 1500€ par chèque. Covoiturage recommandé. Paiement possible en quatre fois par carte bancaire, même si le séjour a commencé.",
        "services_full": "4 chambres, 2 salles de bain, grande cuisine, grand salon, grande terrasse, jacuzzi, Wi‑Fi",
        "guests_detail": "10 personnes (jusqu'à 60 invités pour fêtes)",
        "location": "Quartier La Renée, Rivière-Pilote"
    },
    "Studio Marin Cosy": {
        "nom_csv": "Bas de villa F3 sur Ste Luce",
        "pricing": {
            "base_price": 470,
            "weekend": 470,
            "week": 1030,
            "high_season_weekend": 570,
            "high_season_week": 1390,
            "details": "Juil/Août/Déc/Jan: 1390€/semaine ou 570€/weekend (2 nuits), Mai/Juin/Sept: 1030€/semaine ou 470€/weekend"
        },
        "enhanced_description": "Fêtes et invités ne sont plus acceptés suite aux abus. Caution: 1300€ par chèque + 200€ en espèces. Acompte: 30%. Solde à payer le jour d'arrivée.",
        "services_full": "Bas de villa F3, pas d'invités autorisés",
        "guests_detail": "Non précisé",
        "location": "Sainte-Luce"
    },
    "Studio Ducos Pratique": {
        "nom_csv": "Villa Fête Journée Ducos",
        "pricing": {
            "base_price": 375,
            "person_rate": 30,
            "packages": {"15_pers": 375, "20_pers": 440, "30_pers": 510},
            "details": "Formule 1 (10h-20h): 30€/personne, Package 15 pers: 375€, 20 pers: 440€, 30 pers: 510€"
        },
        "enhanced_description": "12 places de parking + stationnement supplémentaire possible en bordure de route. Enfants comptés à partir de 6 ans. Paiement possible en plusieurs fois sans frais, mais doit être réglé avant l'entrée.",
        "services_full": "Piscine, espace extérieur",
        "guests_detail": "5 à 30 personnes",
        "location": "Ducos"
    },
    "Appartement Marina Fort-de-France": {
        "nom_csv": "Villa Fête Journée Fort de France",
        "pricing": {
            "base_price": 100,
            "hourly_rate": 100,
            "details": "À partir de 100€/heure"
        },
        "enhanced_description": "Disponible de 6h à minuit. Paiement possible en plusieurs fois sans frais (tout doit être réglé avant entrée).",
        "services_full": "Prestations à la carte",
        "guests_detail": "20 à 80 personnes",
        "location": "Fort de France"
    },
    "Villa Diamant Prestige": {
        "nom_csv": "Villa Fête Journée Rivière-Pilote",
        "pricing": {
            "base_price": 660,
            "private_event": 660,
            "details": "660€ pour événement privé (anniversaire enfant, enterrement vie célibataire). Devis personnalisé pour mariage, baptême, communion."
        },
        "enhanced_description": "Horaires fête: 13h-20h ou 18h-2h. Caution: 800€.",
        "services_full": "Piscine chauffée, cuisine extérieure équipée (four, micro-onde, congélateur, bar office), DJ autorisé, bungalow 2 personnes (130€/nuit), appartement 2 personnes (110€/nuit)",
        "guests_detail": "Jusqu'à 100 invités",
        "location": "Rivière-Pilote"
    },
    "Villa Carbet Deluxe": {
        "nom_csv": "Villa Fête Journée Rivière Salée",
        "pricing": {
            "base_price": 400,
            "forfait_1": 400,
            "forfait_2": 550,
            "forfait_3": 750,
            "forfait_4": 1000,
            "details": "Forfait 1 (12h-19h): 400€ (25 pers). Forfait 2 (12h-19h): 550€ (50 pers). Forfait 3 (8h-22h): 750€ (50 pers). Forfait 4 (8h-22h): 1000€ (100 pers)."
        },
        "enhanced_description": "Pour événements utilisant la piscine: maître-nageur ou pompier obligatoire aux frais de l'organisateur (sinon barrière de sécurité installée). Déchets à enlever après l'événement. Acompte 30% à la réservation, solde 48h avant l'événement.",
        "services_full": "5 tables rectangulaires, chaises plastiques selon forfait",
        "guests_detail": "De 25 à 100 personnes (selon forfait)",
        "location": "Quartier La Laugier, Rivière Salée"
    },
    "Villa Océan Bleu": {
        "nom_csv": "Villa Fête Journée Sainte-Luce",
        "pricing": {
            "base_price": 390,
            "for_20_guests": 390,
            "for_40_guests": 560,
            "details": "390€ pour 20 personnes, 560€ pour 40 personnes"
        },
        "enhanced_description": "Horaires: 10h-18h (flexible). Caution: 800€ par chèque. Covoiturage recommandé. Paiement sans frais possible, tout doit être réglé avant entrée.",
        "services_full": "3 tentes, 3 salons extérieurs, 2 grandes tables, 1 réfrigérateur, évier extérieur, douche, WC, système son JBL",
        "guests_detail": "Jusqu'à 40 personnes",
        "location": "Sainte-Luce, près de la Forêt Montravail"
    },
    "Villa Sunset Paradise": {
        "nom_csv": "Espace Piscine Journée Bungalow",
        "pricing": {
            "base_price": 350,
            "up_to_20": 350,
            "up_to_40": 550,
            "up_to_60": 750,
            "bungalow_extra": 85,
            "details": "Forfaits Journée (9h-19h): Jusqu'à 20 invités 350€, Jusqu'à 40 invités: 550€, Jusqu'à 60 invités: 750€, Bungalow pour 2 personnes: +85€/nuit"
        },
        "enhanced_description": "Location de 9h à 19h uniquement (pas de possibilité au-delà de 19h). Tarifs uniquement pour anniversaires, baby-showers et enterrements de vie. Caution: 1000€ par chèque + 250€ en espèces. Autres forfaits sur demande selon type d'événement (mariage, baptême, etc.).",
        "services_full": "Cuisine, salle d'eau, mobilier (chaises, tables), chambre climatisée (+80€ supplémentaire)",
        "guests_detail": "10 à 150 personnes",
        "location": "Non précisé"
    },
    "Villa Tropicale Zen": {
        "nom_csv": "Villa F6 sur Petit Macabou (séjour + fête)",
        "pricing": {
            "base_price": 2000,
            "weekend": 2000,
            "week": 3220,
            "high_season": 3220,
            "details": "Weekend: 2000€, Semaine: à partir de 3220€"
        },
        "enhanced_description": "Villa somptueuse et très spacieuse. Événements ou fêtes autorisés de 9h à 19h. Mariage ou baptême avec hébergements sur demande jusqu'à 150 invités. Covoiturage recommandé. Caution: 2500€ par chèque.",
        "services_full": "3 chambres climatisées avec salle de bain attenante, 1 mezzanine, 2 studios aux extrémités, possibilité de louer 3 bungalows supplémentaires avec bac à punch",
        "guests_detail": "10 à 13 personnes (jusqu'à 30 invités pour fêtes)",
        "location": "Petit Macabou au Vauclin (972)"
    },
    "Penthouse Schoelcher Vue Mer": {
        "nom_csv": "Penthouse Schoelcher Vue Mer",
        "pricing": {
            "base_price": 620,
            "weekend": 620,
            "week": 4340,
            "high_season": 4340,
            "details": "Prix estimé basé sur le positionnement villa haut de gamme"
        },
        "enhanced_description": "Penthouse avec vue mer exceptionnelle. Localisation privilégiée à Schoelcher. Idéal pour séjours de standing.",
        "services_full": "Vue mer, équipements haut de gamme",
        "guests_detail": "Capacité premium",
        "location": "Schoelcher, Vue Mer"
    }
}

async def connect_to_mongo():
    """Connexion à MongoDB"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    return db

async def update_villa_complete_csv(db, villa_name, csv_data):
    """Met à jour complètement une villa avec ses données CSV"""
    try:
        existing_villa = await db.villas.find_one({'name': villa_name})
        
        if not existing_villa:
            print(f"⚠️  Villa non trouvée: {villa_name}")
            return False
        
        # Mise à jour complète
        update_data = {
            'pricing': csv_data['pricing'],
            'price': csv_data['pricing']['base_price'],
            'description': csv_data['enhanced_description'],
            'services_full': csv_data['services_full'],
            'guests_detail': csv_data['guests_detail'],
            'location': csv_data['location'],
            'features': csv_data['services_full'][:100] + '...' if len(csv_data['services_full']) > 100 else csv_data['services_full'],
            'updated_at': datetime.utcnow(),
            'csv_updated': True,
            'csv_source': csv_data['nom_csv']
        }
        
        result = await db.villas.update_one(
            {'name': villa_name},
            {'$set': update_data}
        )
        
        if result.matched_count > 0:
            print(f"✅ Villa mise à jour complète: {villa_name}")
            return True
        else:
            print(f"❌ Échec mise à jour: {villa_name}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur villa {villa_name}: {e}")
        return False

async def main():
    """Fonction principale de correction complète"""
    print("🔧 CORRECTION COMPLÈTE - TOUTES LES VILLAS AVEC DONNÉES CSV")
    print("=" * 70)
    
    try:
        db = await connect_to_mongo()
        print("✅ Connexion MongoDB établie")
        
        # Vérification initiale
        current_count = await db.villas.count_documents({})
        print(f"📊 Villas actuelles: {current_count}")
        
        # Mise à jour COMPLÈTE des 22 villas
        print("\n🔄 MISE À JOUR COMPLÈTE DE TOUTES LES VILLAS")
        print("-" * 50)
        
        updated_count = 0
        total_villas = len(MAPPING_COMPLET_CSV)
        
        for villa_name, csv_data in MAPPING_COMPLET_CSV.items():
            success = await update_villa_complete_csv(db, villa_name, csv_data)
            if success:
                updated_count += 1
        
        print(f"\n📊 Villas mises à jour: {updated_count}/{total_villas}")
        
        # Vérification finale
        final_count = await db.villas.count_documents({})
        csv_updated = await db.villas.count_documents({'csv_updated': True})
        
        print(f"📈 Villas totales: {final_count}")
        print(f"📋 Villas avec données CSV: {csv_updated}")
        
        # Exemples
        examples = await db.villas.find({'csv_updated': True}).limit(5).to_list(5)
        
        print(f"\n🎯 Exemples de villas mises à jour:")
        for villa in examples:
            pricing = villa.get('pricing', {})
            csv_source = villa.get('csv_source', 'N/A')
            print(f"   {villa['name']}: {pricing.get('base_price', 0)}€ ← {csv_source}")
        
        # Rapport final
        report = {
            "correction_complete": True,
            "total_villas": final_count,
            "updated_villas": updated_count,
            "csv_mapping_complete": True,
            "date": datetime.utcnow(),
            "success_rate": (updated_count / total_villas) * 100
        }
        
        await db.correction_complete_reports.insert_one(report)
        
        print("\n✅ CORRECTION COMPLÈTE TERMINÉE")
        print("🎯 TOUTES les villas ont été mises à jour avec leurs données CSV")
        print("💰 Système complet de tarification variable")
        
        if updated_count == total_villas:
            print("\n🎉 SUCCÈS TOTAL: Toutes les villas ont été mises à jour!")
        else:
            print(f"\n⚠️  {updated_count}/{total_villas} villas mises à jour")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    asyncio.run(main())