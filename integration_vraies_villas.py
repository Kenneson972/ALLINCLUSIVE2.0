#!/usr/bin/env python3
"""
Intégration correcte des vraies villas avec les données CSV
Basé sur le vrai site https://kenneson972.github.io/ALLINCLUSIVE2.0/
"""

import asyncio
import json
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime

# Configuration MongoDB
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = 'khanelconcept'

# MAPPING CORRECT basé sur les vraies villas du site
VRAIES_VILLAS_MAPPING = {
    "Villa F3 Petit Macabou": {
        "csv_name": "Villa F3 sur Petit Macabou",
        "current_price": 850,
        "csv_pricing": {
            "base_price": 850,
            "weekend": 850,
            "week": 1550,
            "high_season": 1690,
            "christmas": 1690,
            "details": "Grandes Vacances: 1550€/semaine, Weekend: 850€ (2 nuits), Noël/Nouvel An: 1690€/semaine"
        },
        "csv_description": "Villa avec possibilité d'accueillir 9 invités supplémentaires en journée (9h-20h). Caution: 1500€. Check-in: 16h, Check-out: 11h (possibilité extension jusqu'à 16h selon disponibilité).",
        "csv_services": "Chambres climatisées, 1 salle de bain avec WC, WC indépendant, salon climatisé avec canapé-lit, sauna, jacuzzi, 2 douches extérieures",
        "csv_guests": "6 personnes (jusqu'à 15 personnes en journée)",
        "csv_location": "Petit Macabou, Vauclin"
    },
    "Villa F5 Ste Anne": {
        "csv_name": "Villa F5 sur Ste Anne",
        "current_price": 1300,
        "csv_pricing": {
            "base_price": 1350,
            "weekend": 1350,
            "week": 2251,
            "high_season": 2251,
            "details": "Weekend: 1350€ (2 nuits, hors vacances scolaires), Semaine: 2251€ (7 jours)"
        },
        "csv_description": "Possibilité d'accueillir jusqu'à 15 invités de 9h à 19h. Caution: 500€ en espèces + 1500€ en empreinte CB. Facilités de paiement sans frais supplémentaires avec paiement total avant entrée.",
        "csv_services": "4 chambres, 4 salles de bain",
        "csv_guests": "10 personnes (jusqu'à 15 personnes en journée)",
        "csv_location": "Quartier les Anglais, Ste Anne"
    },
    "Villa F3 Baccha Petit Macabou": {
        "csv_name": "Villa F3 POUR LA BACCHA",
        "current_price": 1350,
        "csv_pricing": {
            "base_price": 1350,
            "weekend": 1350,
            "week": 1350,
            "high_season": 1350,
            "july": "complet",
            "details": "Août: 1350€/semaine, Juillet: complet"
        },
        "csv_description": "Possibilité d'accueillir jusqu'à 9 invités entre 9h et 18h. Caution: 1500€ par chèque. Règles strictes concernant le bruit pour respecter le voisinage.",
        "csv_services": "2 chambres climatisées, salon climatisé avec canapé-lit",
        "csv_guests": "6 personnes (jusqu'à 9 invités en journée)",
        "csv_location": "Petit Macabou"
    },
    "Villa F6 Lamentin": {
        "csv_name": "Villa F6 au Lamentin",
        "current_price": 1500,
        "csv_pricing": {
            "base_price": 1200,
            "weekend": 1500,
            "weekend_2nights": 1200,
            "week": 2800,
            "party_supplement": 300,
            "details": "Weekend: 1500€ (vendredi-dimanche), Weekend 2 nuits: 1200€ (sans invités), Semaine: 2800€ (8 jours), +300€ si fête"
        },
        "csv_description": "Fêtes autorisées de 10h à 19h. Disponibilité vacances: du 1er au 10 juillet et du 25 au 31 août. Check-in: 15h, check-out: 18h. Pénalité retard clés: 150€/30min. Caution: 1000€ (empreinte bancaire). Covoiturage obligatoire.",
        "csv_services": "Piscine, jacuzzi",
        "csv_guests": "10 personnes (jusqu'à 20 invités en journée)",
        "csv_location": "Quartier Béleme, Lamentin"
    },
    "Villa F6 Ste Luce Plage": {
        "csv_name": "Villa F6 sur Ste Luce à 1mn de la plage",
        "current_price": 1200,
        "csv_pricing": {
            "base_price": 1700,
            "weekend": 1700,
            "week": 2200,
            "high_season": 2850,
            "details": "Weekend: 1700€, Semaine (8 jours): 2200€ à 2850€"
        },
        "csv_description": "Check-in: 17h, Check-out: 11h. Caution: 1500€ par chèque + 500€ en espèces (remboursables). Location uniquement à la semaine pendant les vacances scolaires. Facilités de paiement sans frais supplémentaires (tout doit être payé avant l'entrée).",
        "csv_services": "5 appartements (2 F2 duplex et 3 F2), dont un en sous-sol",
        "csv_guests": "10 à 14 personnes",
        "csv_location": "Zac de Pont Café, Ste Luce, à 1mn de la plage Corps de garde"
    },
    "Villa F6 Petit Macabou": {
        "csv_name": "Villa F6 sur Petit Macabou (séjour + fête)",
        "current_price": 2000,
        "csv_pricing": {
            "base_price": 2000,
            "weekend": 2000,
            "week": 3220,
            "high_season": 3220,
            "details": "Weekend: 2000€, Semaine: à partir de 3220€"
        },
        "csv_description": "Villa somptueuse et très spacieuse. Événements ou fêtes autorisés de 9h à 19h. Mariage ou baptême avec hébergements sur demande jusqu'à 150 invités. Covoiturage recommandé. Caution: 2500€ par chèque.",
        "csv_services": "3 chambres climatisées avec salle de bain attenante, 1 mezzanine, 2 studios aux extrémités, possibilité de louer 3 bungalows supplémentaires avec bac à punch",
        "csv_guests": "10 à 13 personnes (jusqu'à 30 invités pour fêtes)",
        "csv_location": "Petit Macabou au Vauclin (972)"
    },
    "Villa F7 Baie des Mulets": {
        "csv_name": "Villa F7 Baie des Mulets",
        "current_price": 2500,
        "csv_pricing": {
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
        "csv_description": "Check-in: 11h, Check-out: 13h (option late check-out 17h30: +150€). Fêtes autorisées de 9h à minuit. Location possible à la journée (lundi-jeudi) selon disponibilité. Caution: 1500€ par chèque ou empreinte bancaire. Paiement possible en plusieurs fois, sans frais, avec solde 72h avant entrée.",
        "csv_services": "F5: 4 chambres climatisées + salon avec canapé-lit; F3: salon avec canapé-lit. Parking pour 30 véhicules",
        "csv_guests": "16 personnes (F5: 10 personnes + F3: 6 personnes)",
        "csv_location": "Baie des Mulets, Vauclin"
    },
    "Villa F3 Trinité Cosmy": {
        "csv_name": "Villa F3 Bas de villa Trinité Cosmy",
        "current_price": 900,
        "csv_pricing": {
            "base_price": 500,
            "weekend": 500,
            "week": 3500,
            "party_rates": {
                "10_guests": 670,
                "60_guests": 1400
            },
            "details": "Weekend sans invités: 500€, Weekend + Fête: 670€ (10 invités) à 1400€ (60 invités)"
        },
        "csv_description": "Villa charmante idéale pour séjours entre amis, famille et événements. Environnement calme et relaxant. Horaires fête: 10h-18h ou 14h-22h (départ des invités à partir de 21h). Location à la semaine pendant vacances scolaires (exceptions possibles). Caution: 200€ en espèces + 400€ par chèque.",
        "csv_services": "2 chambres climatisées, 1 salle de bain, double terrasse, salon, cuisine américaine, piscine privée chauffée",
        "csv_guests": "5 adultes ou 4 adultes et 2 enfants (jusqu'à 60 invités pour fêtes)",
        "csv_location": "Cosmy, Trinité"
    },
    "Villa F5 Rivière-Pilote La Renée": {
        "csv_name": "Villa F5 La Renée",
        "current_price": 1400,
        "csv_pricing": {
            "base_price": 900,
            "weekend": 900,
            "weekend_party": 1400,
            "week": 1590,
            "week_party": 2000,
            "details": "Weekend avec fête: 1400€, Weekend sans fête: 900€, Semaine avec fête: 2000€, Semaine sans fête: 1590€"
        },
        "csv_description": "Horaires fêtes: 9h-00h. Caution: 1500€ par chèque. Covoiturage recommandé. Paiement possible en quatre fois par carte bancaire, même si le séjour a commencé.",
        "csv_services": "4 chambres, 2 salles de bain, grande cuisine, grand salon, grande terrasse, jacuzzi, Wi‑Fi",
        "csv_guests": "10 personnes (jusqu'à 60 invités pour fêtes)",
        "csv_location": "Quartier La Renée, Rivière-Pilote"
    },
    "Villa F3 Le François": {
        "csv_name": "Villa F3 sur le François",
        "current_price": 800,
        "csv_pricing": {
            "base_price": 800,
            "weekend": 800,
            "week": 1376,
            "high_season": 1376,
            "details": "Weekend: 800€ (2 nuits), Semaine: 1376€ (7 jours)"
        },
        "csv_description": "Caution: 1000€ (850€ par chèque et 150€ en espèces). Check-in: 16h, Check-out: 11h (option late check-out: +80€). Frais de 50€ par 30 minutes de retard pour la remise des clés. Villa à rendre propre et rangée.",
        "csv_services": "Stationnement pour 5 véhicules, enceintes JBL autorisées",
        "csv_guests": "4 personnes (maximum 10 invités)",
        "csv_location": "Hauteurs du Morne Carrière au François"
    },
    "Villa F5 Vauclin Ravine Plate": {
        "csv_name": "Villa F5 Vauclin Ravine Plate",
        "current_price": 1550,
        "csv_pricing": {
            "base_price": 1550,
            "weekend": 1550,
            "week": 2500,
            "high_season": 2500,
            "details": "Weekend: 1550€ (vendredi-dimanche), Semaine: 2500€ (8 jours)"
        },
        "csv_description": "Caution: 1500€ par chèque et 500€ en espèces, remboursée à la sortie si aucun dommage. Paiement en plusieurs fois sans frais possible, solde à régler avant l'entrée.",
        "csv_services": "4 chambres climatisées avec salle d'eau attenante, piscine à débordement",
        "csv_guests": "8 personnes",
        "csv_location": "Hauteurs de Ravine Plate, Vauclin"
    },
    "Bas Villa F3 Ste Luce": {
        "csv_name": "Bas de villa F3 sur Ste Luce",
        "current_price": 470,
        "csv_pricing": {
            "base_price": 470,
            "weekend_low": 470,
            "week_low": 1030,
            "weekend_high": 570,
            "week_high": 1390,
            "details": "Juil/Août/Déc/Jan: 1390€/semaine ou 570€/weekend (2 nuits), Mai/Juin/Sept: 1030€/semaine ou 470€/weekend"
        },
        "csv_description": "Fêtes et invités ne sont plus acceptés suite aux abus. Caution: 1300€ par chèque + 200€ en espèces. Acompte: 30%. Solde à payer le jour d'arrivée.",
        "csv_services": "Bas de villa F3, pas d'invités autorisés",
        "csv_guests": "4 personnes",
        "csv_location": "Sainte-Luce"
    },
    "Villa F3 Trenelle": {
        "csv_name": "Appartement F3 Trenelle (Location Annuelle)",
        "current_price": 800,
        "csv_pricing": {
            "base_price": 700,
            "monthly": 700,
            "annual": 8400,
            "details": "700€/mois (eau et EDF inclus)"
        },
        "csv_description": "Location à l'année (bail de 12 mois) avec possibilité de louer pour 3 ou 6 mois. Accès au logement: 1550€ (2 mois de caution + 1 mois de loyer hors charges).",
        "csv_services": "Meublé, eau et électricité incluses",
        "csv_guests": "Couple sans enfant, personne seule ou 2 colocataires",
        "csv_location": "Trenelle, à 2 minutes du PPM"
    },
    "Studio Cocooning Lamentin": {
        "csv_name": "Studio Cocooning Lamentin",
        "current_price": 290,
        "csv_pricing": {
            "base_price": 290,
            "weekend": 290,
            "week": 2030,
            "high_season": 2030,
            "details": "À partir de 290€, minimum 2 nuits"
        },
        "csv_description": "Pas d'invités autorisés. Location uniquement à la semaine pendant les vacances scolaires et haute saison touristique. Check-in: 16h, Check-out: 11h (départ tardif possible selon disponibilité). Paiement en plusieurs fois sans frais possible (tout doit être réglé avant entrée).",
        "csv_services": "Bac à punch privé (petite piscine)",
        "csv_guests": "2 personnes",
        "csv_location": "Hauteurs de Morne Pitault, Lamentin"
    },
    "Villa F3 Le Robert": {
        "csv_name": "Bas de villa F3 sur le Robert",
        "current_price": 630,
        "csv_pricing": {
            "base_price": 900,
            "weekend": 900,
            "week_low": 1250,
            "week_high": 1500,
            "party_supplement": 550,
            "details": "Weekend: 900€, Weekend avec fête/invités: +550€, Semaine: 1250€ (basse saison), 1500€ (haute saison)"
        },
        "csv_description": "Enceintes JBL autorisées jusqu'à 22h (DJ et gros systèmes sono interdits). Caution: 1500€ pour la villa + caution pour l'espace piscine. Paiement en plusieurs fois sans frais possible (tout doit être soldé avant l'entrée).",
        "csv_services": "2 chambres climatisées, location à la journée possible (lundi-jeudi), excursion nautique possible",
        "csv_guests": "10 personnes",
        "csv_location": "Pointe Hyacinthe, Le Robert"
    },
    "Espace Piscine Journée Bungalow": {
        "csv_name": "Espace Piscine Journée Bungalow",
        "current_price": 150,
        "csv_pricing": {
            "base_price": 350,
            "up_to_20": 350,
            "up_to_40": 550,
            "up_to_60": 750,
            "bungalow_extra": 85,
            "details": "Forfaits Journée (9h-19h): Jusqu'à 20 invités 350€, Jusqu'à 40 invités: 550€, Jusqu'à 60 invités: 750€, Bungalow pour 2 personnes: +85€/nuit"
        },
        "csv_description": "Location de 9h à 19h uniquement (pas de possibilité au-delà de 19h). Tarifs uniquement pour anniversaires, baby-showers et enterrements de vie. Caution: 1000€ par chèque + 250€ en espèces. Autres forfaits sur demande selon type d'événement (mariage, baptême, etc.).",
        "csv_services": "Cuisine, salle d'eau, mobilier (chaises, tables), chambre climatisée (+80€ supplémentaire)",
        "csv_guests": "10 à 150 personnes",
        "csv_location": "Martinique"
    },
    "Villa Fête Ducos": {
        "csv_name": "Villa Fête Journée Ducos",
        "current_price": 200,
        "csv_pricing": {
            "base_price": 375,
            "person_rate": 30,
            "formula_1": {"15_pers": 375, "20_pers": 440, "30_pers": 510},
            "formula_2": {"15_pers": 260, "20_pers": 300, "30_pers": 375},
            "details": "Formule 1 (10h-20h): 30€/personne, Package 15 pers: 375€, 20 pers: 440€, 30 pers: 510€. Formule 2 (13h-18h): 20€/personne, Package 15 pers: 260€, 20 pers: 300€, 30 pers: 375€."
        },
        "csv_description": "12 places de parking + stationnement supplémentaire possible en bordure de route. Enfants comptés à partir de 6 ans. Paiement possible en plusieurs fois sans frais, mais doit être réglé avant l'entrée.",
        "csv_services": "Piscine, espace extérieur",
        "csv_guests": "5 à 30 personnes",
        "csv_location": "Ducos"
    },
    "Villa Fête Fort-de-France": {
        "csv_name": "Villa Fête Journée Fort de France",
        "current_price": 250,
        "csv_pricing": {
            "base_price": 100,
            "hourly_rate": 100,
            "details": "À partir de 100€/heure"
        },
        "csv_description": "Disponible de 6h à minuit. Paiement possible en plusieurs fois sans frais (tout doit être réglé avant entrée).",
        "csv_services": "Prestations à la carte",
        "csv_guests": "20 à 80 personnes",
        "csv_location": "Fort de France"
    },
    "Villa Fête Rivière-Pilote": {
        "csv_name": "Villa Fête Journée Rivière-Pilote",
        "current_price": 180,
        "csv_pricing": {
            "base_price": 660,
            "private_event": 660,
            "bungalow": 130,
            "apartment": 110,
            "details": "660€ pour événement privé (anniversaire enfant, enterrement vie célibataire). Devis personnalisé pour mariage, baptême, communion."
        },
        "csv_description": "Horaires fête: 13h-20h ou 18h-2h. Caution: 800€.",
        "csv_services": "Piscine chauffée, cuisine extérieure équipée (four, micro-onde, congélateur, bar office), DJ autorisé, bungalow 2 personnes (130€/nuit), appartement 2 personnes (110€/nuit)",
        "csv_guests": "Jusqu'à 100 invités",
        "csv_location": "Rivière-Pilote"
    },
    "Villa Fête Sainte-Luce": {
        "csv_name": "Villa Fête Journée Sainte-Luce",
        "current_price": 220,
        "csv_pricing": {
            "base_price": 390,
            "for_20_guests": 390,
            "for_40_guests": 560,
            "details": "390€ pour 20 personnes, 560€ pour 40 personnes"
        },
        "csv_description": "Horaires: 10h-18h (flexible). Caution: 800€ par chèque. Covoiturage recommandé. Paiement sans frais possible, tout doit être réglé avant entrée.",
        "csv_services": "3 tentes, 3 salons extérieurs, 2 grandes tables, 1 réfrigérateur, évier extérieur, douche, WC, système son JBL",
        "csv_guests": "Jusqu'à 40 personnes",
        "csv_location": "Sainte-Luce, près de la Forêt Montravail"
    },
    "Villa Fête Rivière-Salée": {
        "csv_name": "Villa Fête Journée Rivière Salée",
        "current_price": 160,
        "csv_pricing": {
            "base_price": 400,
            "forfait_1": 400,
            "forfait_2": 550,
            "forfait_3": 750,
            "forfait_4": 1000,
            "details": "Forfait 1 (12h-19h): 400€ (25 pers). Forfait 2 (12h-19h): 550€ (50 pers). Forfait 3 (8h-22h): 750€ (50 pers). Forfait 4 (8h-22h): 1000€ (100 pers)."
        },
        "csv_description": "Pour événements utilisant la piscine: maître-nageur ou pompier obligatoire aux frais de l'organisateur (sinon barrière de sécurité installée). Déchets à enlever après l'événement. Acompte 30% à la réservation, solde 48h avant l'événement.",
        "csv_services": "5 tables rectangulaires, chaises plastiques selon forfait",
        "csv_guests": "De 25 à 100 personnes (selon forfait)",
        "csv_location": "Quartier La Laugier, Rivière Salée"
    }
}

async def connect_to_mongo():
    """Connexion à MongoDB"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    return db

async def update_real_villa_with_csv(db, villa_name, villa_data):
    """Met à jour une vraie villa avec ses données CSV"""
    try:
        # Chercher la villa par nom
        existing_villa = await db.villas.find_one({'name': villa_name})
        
        if not existing_villa:
            print(f"⚠️  Villa non trouvée: {villa_name}")
            return False
        
        # Créer l'objet de mise à jour
        update_data = {
            'price': villa_data['csv_pricing']['base_price'],
            'pricing_details': villa_data['csv_pricing'],
            'description': villa_data['csv_description'],
            'services_full': villa_data['csv_services'],
            'guests_detail': villa_data['csv_guests'],
            'location': villa_data['csv_location'],
            'features': villa_data['csv_services'][:100] + '...' if len(villa_data['csv_services']) > 100 else villa_data['csv_services'],
            'updated_at': datetime.utcnow(),
            'csv_integrated': True,
            'csv_source': villa_data['csv_name'],
            'old_price': villa_data['current_price']
        }
        
        # Mettre à jour la villa
        result = await db.villas.update_one(
            {'name': villa_name},
            {'$set': update_data}
        )
        
        if result.matched_count > 0:
            print(f"✅ Villa mise à jour: {villa_name}")
            print(f"   Prix: {villa_data['current_price']}€ → {villa_data['csv_pricing']['base_price']}€")
            print(f"   Source CSV: {villa_data['csv_name']}")
            return True
        else:
            print(f"❌ Échec mise à jour: {villa_name}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur villa {villa_name}: {e}")
        return False

async def main():
    """Fonction principale d'intégration des vraies villas"""
    print("🏠 INTÉGRATION CORRECTE DES VRAIES VILLAS AVEC DONNÉES CSV")
    print("=" * 70)
    
    try:
        # Connexion à MongoDB
        db = await connect_to_mongo()
        print("✅ Connexion MongoDB établie")
        
        # Vérifier le nombre actuel de villas
        current_count = await db.villas.count_documents({})
        print(f"📊 Villas actuelles: {current_count}")
        
        # Récupérer les noms des villas actuelles
        villas = await db.villas.find({}, {'name': 1}).to_list(None)
        villa_names = [villa['name'] for villa in villas]
        
        print(f"📋 Villas dans la base:")
        for name in sorted(villa_names):
            print(f"   - {name}")
        
        # Mise à jour des vraies villas avec données CSV
        print(f"\n🔄 MISE À JOUR DES VRAIES VILLAS AVEC DONNÉES CSV")
        print("-" * 60)
        
        updated_count = 0
        not_found_count = 0
        total_mapped = len(VRAIES_VILLAS_MAPPING)
        
        for villa_name, villa_data in VRAIES_VILLAS_MAPPING.items():
            if villa_name in villa_names:
                success = await update_real_villa_with_csv(db, villa_name, villa_data)
                if success:
                    updated_count += 1
            else:
                print(f"⚠️  Villa non trouvée dans la base: {villa_name}")
                not_found_count += 1
        
        print(f"\n📊 RÉSULTATS DE L'INTÉGRATION:")
        print(f"   - Villas mises à jour: {updated_count}")
        print(f"   - Villas non trouvées: {not_found_count}")
        print(f"   - Total mappées: {total_mapped}")
        
        # Vérifier les résultats
        csv_integrated = await db.villas.count_documents({'csv_integrated': True})
        print(f"   - Villas avec CSV intégré: {csv_integrated}")
        
        # Exemples de villas mises à jour
        examples = await db.villas.find(
            {'csv_integrated': True}, 
            {'name': 1, 'price': 1, 'old_price': 1, 'csv_source': 1}
        ).limit(5).to_list(5)
        
        print(f"\n🎯 EXEMPLES DE VILLAS MISES À JOUR:")
        for villa in examples:
            old_price = villa.get('old_price', 'N/A')
            new_price = villa.get('price', 'N/A')
            csv_source = villa.get('csv_source', 'N/A')
            print(f"   {villa['name']}: {old_price}€ → {new_price}€ (← {csv_source})")
        
        # Rapport final
        report = {
            "integration_type": "vraies_villas",
            "date": datetime.utcnow(),
            "total_villas_in_db": current_count,
            "villas_mapped": total_mapped,
            "villas_updated": updated_count,
            "villas_not_found": not_found_count,
            "success_rate": (updated_count / total_mapped) * 100,
            "csv_integrated_count": csv_integrated
        }
        
        await db.vraies_villas_integration_report.insert_one(report)
        
        print(f"\n✅ INTÉGRATION TERMINÉE")
        print(f"🎯 Taux de réussite: {report['success_rate']:.1f}%")
        print(f"📊 Rapport sauvegardé dans la base")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'intégration: {e}")

if __name__ == "__main__":
    asyncio.run(main())