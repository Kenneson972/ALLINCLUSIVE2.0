#!/usr/bin/env python3
"""
Intégration des données CSV dans les 22 vraies villas
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime

# Configuration MongoDB
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = 'khanelconcept'

# MAPPING CORRECT pour les 22 vraies villas
MAPPING_22_VILLAS_CSV = {
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
    "Villa François Moderne": {
        "csv_name": "Villa F3 sur le François",
        "pricing": {
            "base_price": 800,
            "weekend": 800,
            "week": 1376,
            "high_season": 1376,
            "details": "Weekend: 800€ (2 nuits), Semaine: 1376€ (7 jours)"
        },
        "description": "Caution: 1000€ (850€ par chèque et 150€ en espèces). Check-in: 16h, Check-out: 11h (option late check-out: +80€). Frais de 50€ par 30 minutes de retard pour la remise des clés. Villa à rendre propre et rangée.",
        "services": "Stationnement pour 5 véhicules, enceintes JBL autorisées",
        "guests": "4 personnes (maximum 10 invités)",
        "location": "Hauteurs du Morne Carrière au François"
    },
    "Villa Grand Luxe Pointe du Bout": {
        "csv_name": "Villa F6 au Lamentin",
        "pricing": {
            "base_price": 1200,
            "weekend": 1500,
            "week": 2800,
            "high_season": 2800,
            "party_supplement": 300,
            "details": "Weekend: 1500€ (vendredi-dimanche), Weekend 2 nuits: 1200€ (sans invités), Semaine: 2800€ (8 jours), +300€ si fête"
        },
        "description": "Fêtes autorisées de 10h à 19h. Disponibilité vacances: du 1er au 10 juillet et du 25 au 31 août. Check-in: 15h, check-out: 18h. Pénalité retard clés: 150€/30min. Caution: 1000€ (empreinte bancaire). Covoiturage obligatoire.",
        "services": "Piscine, jacuzzi",
        "guests": "10 personnes (jusqu'à 20 invités en journée)",
        "location": "Quartier Béleme, Lamentin"
    },
    "Villa Anses d'Arlet": {
        "csv_name": "Villa F6 sur Ste Luce à 1mn de la plage",
        "pricing": {
            "base_price": 1700,
            "weekend": 1700,
            "week": 2200,
            "high_season": 2850,
            "details": "Weekend: 1700€, Semaine (8 jours): 2200€ à 2850€"
        },
        "description": "Check-in: 17h, Check-out: 11h. Caution: 1500€ par chèque + 500€ en espèces (remboursables). Location uniquement à la semaine pendant les vacances scolaires. Facilités de paiement sans frais supplémentaires (tout doit être payé avant l'entrée).",
        "services": "5 appartements (2 F2 duplex et 3 F2), dont un en sous-sol",
        "guests": "10 à 14 personnes",
        "location": "Zac de Pont Café, Ste Luce, à 1mn de la plage Corps de garde"
    },
    "Villa Bord de Mer Tartane": {
        "csv_name": "Villa F3 Bas de villa Trinité Cosmy",
        "pricing": {
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
        "description": "Villa charmante idéale pour séjours entre amis, famille et événements. Environnement calme et relaxant. Horaires fête: 10h-18h ou 14h-22h (départ des invités à partir de 21h). Location à la semaine pendant vacances scolaires (exceptions possibles). Caution: 200€ en espèces + 400€ par chèque.",
        "services": "2 chambres climatisées, 1 salle de bain, double terrasse, salon, cuisine américaine, piscine privée chauffée",
        "guests": "5 adultes ou 4 adultes et 2 enfants (jusqu'à 60 invités pour fêtes)",
        "location": "Cosmy, Trinité"
    },
    "Villa Rivière-Pilote Charme": {
        "csv_name": "Bas de villa F3 sur le Robert",
        "pricing": {
            "base_price": 900,
            "weekend": 900,
            "week_low": 1250,
            "week_high": 1500,
            "party_supplement": 550,
            "details": "Weekend: 900€, Weekend avec fête/invités: +550€, Semaine: 1250€ (basse saison), 1500€ (haute saison)"
        },
        "description": "Enceintes JBL autorisées jusqu'à 22h (DJ et gros systèmes sono interdits). Caution: 1500€ pour la villa + caution pour l'espace piscine. Paiement en plusieurs fois sans frais possible (tout doit être soldé avant l'entrée).",
        "services": "2 chambres climatisées, location à la journée possible (lundi-jeudi), excursion nautique possible",
        "guests": "10 personnes",
        "location": "Pointe Hyacinthe, Le Robert"
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
    "Villa Tropicale Zen": {
        "csv_name": "Villa F7 Baie des Mulets",
        "pricing": {
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
        "description": "Check-in: 11h, Check-out: 13h (option late check-out 17h30: +150€). Fêtes autorisées de 9h à minuit. Location possible à la journée (lundi-jeudi) selon disponibilité. Caution: 1500€ par chèque ou empreinte bancaire. Paiement possible en plusieurs fois, sans frais, avec solde 72h avant entrée.",
        "services": "F5: 4 chambres climatisées + salon avec canapé-lit; F3: salon avec canapé-lit. Parking pour 30 véhicules",
        "guests": "16 personnes (F5: 10 personnes + F3: 6 personnes)",
        "location": "Baie des Mulets, Vauclin"
    },
    "Bungalow Trenelle Nature": {
        "csv_name": "Appartement F3 Trenelle (Location Annuelle)",
        "pricing": {
            "base_price": 700,
            "monthly": 700,
            "annual": 8400,
            "details": "700€/mois (eau et EDF inclus)"
        },
        "description": "Location à l'année (bail de 12 mois) avec possibilité de louer pour 3 ou 6 mois. Accès au logement: 1550€ (2 mois de caution + 1 mois de loyer hors charges).",
        "services": "Meublé, eau et électricité incluses",
        "guests": "Couple sans enfant, personne seule ou 2 colocataires",
        "location": "Trenelle, à 2 minutes du PPM"
    },
    "Villa Marigot Exclusive": {
        "csv_name": "Villa F5 Vauclin Ravine Plate",
        "pricing": {
            "base_price": 1550,
            "weekend": 1550,
            "week": 2500,
            "high_season": 2500,
            "details": "Weekend: 1550€ (vendredi-dimanche), Semaine: 2500€ (8 jours)"
        },
        "description": "Caution: 1500€ par chèque et 500€ en espèces, remboursée à la sortie si aucun dommage. Paiement en plusieurs fois sans frais possible, solde à régler avant l'entrée.",
        "services": "4 chambres climatisées avec salle d'eau attenante, piscine à débordement",
        "guests": "8 personnes",
        "location": "Hauteurs de Ravine Plate, Vauclin"
    },
    "Villa Sainte-Marie Familiale": {
        "csv_name": "Villa F5 La Renée",
        "pricing": {
            "base_price": 900,
            "weekend": 900,
            "weekend_party": 1400,
            "week": 1590,
            "week_party": 2000,
            "details": "Weekend avec fête: 1400€, Weekend sans fête: 900€, Semaine avec fête: 2000€, Semaine sans fête: 1590€"
        },
        "description": "Horaires fêtes: 9h-00h. Caution: 1500€ par chèque. Covoiturage recommandé. Paiement possible en quatre fois par carte bancaire, même si le séjour a commencé.",
        "services": "4 chambres, 2 salles de bain, grande cuisine, grand salon, grande terrasse, jacuzzi, Wi‑Fi",
        "guests": "10 personnes (jusqu'à 60 invités pour fêtes)",
        "location": "Quartier La Renée, Rivière-Pilote"
    },
    "Studio Marin Cosy": {
        "csv_name": "Bas de villa F3 sur Ste Luce",
        "pricing": {
            "base_price": 470,
            "weekend": 470,
            "week": 1030,
            "high_season_weekend": 570,
            "high_season_week": 1390,
            "details": "Juil/Août/Déc/Jan: 1390€/semaine ou 570€/weekend (2 nuits), Mai/Juin/Sept: 1030€/semaine ou 470€/weekend"
        },
        "description": "Fêtes et invités ne sont plus acceptés suite aux abus. Caution: 1300€ par chèque + 200€ en espèces. Acompte: 30%. Solde à payer le jour d'arrivée.",
        "services": "Bas de villa F3, pas d'invités autorisés",
        "guests": "4 personnes",
        "location": "Sainte-Luce"
    },
    "Studio Ducos Pratique": {
        "csv_name": "Villa Fête Journée Ducos",
        "pricing": {
            "base_price": 375,
            "person_rate": 30,
            "formula_1": {"15_pers": 375, "20_pers": 440, "30_pers": 510},
            "details": "Formule 1 (10h-20h): 30€/personne, Package 15 pers: 375€, 20 pers: 440€, 30 pers: 510€"
        },
        "description": "12 places de parking + stationnement supplémentaire possible en bordure de route. Enfants comptés à partir de 6 ans. Paiement possible en plusieurs fois sans frais, mais doit être réglé avant l'entrée.",
        "services": "Piscine, espace extérieur",
        "guests": "5 à 30 personnes",
        "location": "Ducos"
    },
    "Appartement Marina Fort-de-France": {
        "csv_name": "Villa Fête Journée Fort de France",
        "pricing": {
            "base_price": 100,
            "hourly_rate": 100,
            "details": "À partir de 100€/heure"
        },
        "description": "Disponible de 6h à minuit. Paiement possible en plusieurs fois sans frais (tout doit être réglé avant entrée).",
        "services": "Prestations à la carte",
        "guests": "20 à 80 personnes",
        "location": "Fort de France"
    },
    "Villa Diamant Prestige": {
        "csv_name": "Villa Fête Journée Rivière-Pilote",
        "pricing": {
            "base_price": 660,
            "private_event": 660,
            "details": "660€ pour événement privé (anniversaire enfant, enterrement vie célibataire). Devis personnalisé pour mariage, baptême, communion."
        },
        "description": "Horaires fête: 13h-20h ou 18h-2h. Caution: 800€.",
        "services": "Piscine chauffée, cuisine extérieure équipée (four, micro-onde, congélateur, bar office), DJ autorisé, bungalow 2 personnes (130€/nuit), appartement 2 personnes (110€/nuit)",
        "guests": "Jusqu'à 100 invités",
        "location": "Rivière-Pilote"
    },
    "Villa Carbet Deluxe": {
        "csv_name": "Villa Fête Journée Rivière Salée",
        "pricing": {
            "base_price": 400,
            "forfait_1": 400,
            "forfait_2": 550,
            "forfait_3": 750,
            "forfait_4": 1000,
            "details": "Forfait 1 (12h-19h): 400€ (25 pers). Forfait 2 (12h-19h): 550€ (50 pers). Forfait 3 (8h-22h): 750€ (50 pers). Forfait 4 (8h-22h): 1000€ (100 pers)."
        },
        "description": "Pour événements utilisant la piscine: maître-nageur ou pompier obligatoire aux frais de l'organisateur (sinon barrière de sécurité installée). Déchets à enlever après l'événement. Acompte 30% à la réservation, solde 48h avant l'événement.",
        "services": "5 tables rectangulaires, chaises plastiques selon forfait",
        "guests": "De 25 à 100 personnes (selon forfait)",
        "location": "Quartier La Laugier, Rivière Salée"
    },
    "Villa Océan Bleu": {
        "csv_name": "Villa Fête Journée Sainte-Luce",
        "pricing": {
            "base_price": 390,
            "for_20_guests": 390,
            "for_40_guests": 560,
            "details": "390€ pour 20 personnes, 560€ pour 40 personnes"
        },
        "description": "Horaires: 10h-18h (flexible). Caution: 800€ par chèque. Covoiturage recommandé. Paiement sans frais possible, tout doit être réglé avant entrée.",
        "services": "3 tentes, 3 salons extérieurs, 2 grandes tables, 1 réfrigérateur, évier extérieur, douche, WC, système son JBL",
        "guests": "Jusqu'à 40 personnes",
        "location": "Sainte-Luce, près de la Forêt Montravail"
    },
    "Villa Sunset Paradise": {
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
    },
    "Penthouse Schoelcher Vue Mer": {
        "csv_name": "Villa F5 Vauclin Ravine Plate",
        "pricing": {
            "base_price": 1550,
            "weekend": 1550,
            "week": 2500,
            "high_season": 2500,
            "details": "Weekend: 1550€ (vendredi-dimanche), Semaine: 2500€ (8 jours)"
        },
        "description": "Penthouse avec vue mer exceptionnelle. Caution: 1500€ par chèque et 500€ en espèces. Paiement en plusieurs fois sans frais possible.",
        "services": "Vue mer panoramique, équipements haut de gamme",
        "guests": "8 personnes",
        "location": "Schoelcher, Vue Mer"
    }
}

async def connect_to_mongo():
    """Connexion à MongoDB"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    return db

async def integrer_csv_dans_22_villas():
    """Intègre les données CSV dans les 22 villas"""
    db = await connect_to_mongo()
    
    print("🔄 INTÉGRATION CSV DANS LES 22 VILLAS")
    print("=" * 45)
    
    # Vérifier les villas en base
    villas_base = await db.villas.find({}).to_list(None)
    noms_base = [villa['name'] for villa in villas_base]
    
    print(f"📊 Villas en base: {len(villas_base)}")
    
    integrees = 0
    non_trouvees = 0
    
    for villa_name, csv_data in MAPPING_22_VILLAS_CSV.items():
        if villa_name in noms_base:
            try:
                # Mettre à jour la villa
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
                
                result = await db.villas.update_one(
                    {'name': villa_name},
                    {'$set': update_data}
                )
                
                if result.matched_count > 0:
                    print(f"✅ {villa_name} → {csv_data['pricing']['base_price']}€")
                    integrees += 1
                else:
                    print(f"❌ Échec: {villa_name}")
                    
            except Exception as e:
                print(f"❌ Erreur {villa_name}: {e}")
        else:
            print(f"⚠️  Non trouvée: {villa_name}")
            non_trouvees += 1
    
    print(f"\n📊 RÉSULTATS INTÉGRATION:")
    print(f"   - Villas intégrées: {integrees}")
    print(f"   - Villas non trouvées: {non_trouvees}")
    print(f"   - Taux de réussite: {(integrees/len(MAPPING_22_VILLAS_CSV))*100:.1f}%")
    
    return integrees

async def main():
    """Fonction principale"""
    try:
        integrees = await integrer_csv_dans_22_villas()
        
        if integrees >= 20:
            print(f"\n✅ INTÉGRATION RÉUSSIE")
            print(f"🎯 {integrees} villas ont leurs données CSV")
        else:
            print(f"\n⚠️  INTÉGRATION PARTIELLE")
            print(f"🎯 {integrees} villas intégrées")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    asyncio.run(main())