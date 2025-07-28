#!/usr/bin/env python3
"""
Intégration des 21 vraies villas à partir du CSV
Supprime tous les noms fictifs et intègre les données exactes du CSV
"""

import asyncio
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# Données exactes du CSV
VILLAS_CSV_DATA = [
    {
        "id": "1",
        "name": "Villa F3 sur Petit Macabou",
        "location": "Petit Macabou, Vauclin",
        "type": "F3",
        "guests": 6,
        "guests_detail": "6 personnes (jusqu'à 15 personnes en journée)",
        "price": 850.0,
        "features": "Chambres climatisées, 1 salle de bain avec WC, WC indépendant, salon climatisé avec canapé-lit, sauna, jacuzzi, 2 douches extérieures",
        "description": "Villa avec possibilité d'accueillir 9 invités supplémentaires en journée (9h-20h). Caution: 1500€. Check-in: 16h, Check-out: 11h (possibilité extension jusqu'à 16h selon disponibilité).",
        "category": "sejour",
        "image": "/images/Villa_F3_Petit_Macabou/01_piscine_exterieur.jpg",
        "gallery": [
            "/images/Villa_F3_Petit_Macabou/01_piscine_exterieur.jpg",
            "/images/Villa_F3_Petit_Macabou/02_terrasse_salon_exterieur.jpg",
            "/images/Villa_F3_Petit_Macabou/03_salle_de_bain_moderne.jpg",
            "/images/Villa_F3_Petit_Macabou/04_chambre_principale.jpg",
            "/images/Villa_F3_Petit_Macabou/05_cuisine_equipee.jpg",
            "/images/Villa_F3_Petit_Macabou/07_sauna_detente.jpg",
            "/images/Villa_F3_Petit_Macabou/08_douche_exterieure.jpg"
        ],
        "pricing_details": {
            "base_price": 850,
            "weekend": 850,
            "week": 1550,
            "high_season": 1690,
            "details": "Grandes Vacances: 1550€/semaine, Weekend: 850€ (2 nuits), Noël/Nouvel An: 1690€/semaine"
        },
        "services_full": "Chambres climatisées, 1 salle de bain avec WC, WC indépendant, salon climatisé avec canapé-lit, sauna, jacuzzi, 2 douches extérieures"
    },
    {
        "id": "2",
        "name": "Villa F3 POUR LA BACCHA",
        "location": "Petit Macabou",
        "type": "F3",
        "guests": 6,
        "guests_detail": "6 personnes",
        "price": 1350.0,
        "features": "2 chambres climatisées, salon climatisé avec canapé-lit",
        "description": "Possibilité d'accueillir jusqu'à 9 invités entre 9h et 18h. Caution: 1500€ par chèque. Règles strictes concernant le bruit pour respecter le voisinage.",
        "category": "sejour",
        "image": "/images/Villa_F3_Baccha_Petit_Macabou/01_facade_villa.jpg",
        "gallery": [
            "/images/Villa_F3_Baccha_Petit_Macabou/01_facade_villa.jpg",
            "/images/Villa_F3_Baccha_Petit_Macabou/02_piscine_principale.jpg",
            "/images/Villa_F3_Baccha_Petit_Macabou/03_terrasse_couverte.jpg",
            "/images/Villa_F3_Baccha_Petit_Macabou/04_chambre_climatisee.jpg",
            "/images/Villa_F3_Baccha_Petit_Macabou/05_salon_interieur.jpg"
        ],
        "pricing_details": {
            "base_price": 1350,
            "weekend": 1350,
            "week": 1350,
            "high_season": 1350,
            "details": "Août: 1350€/semaine, Juillet: complet"
        },
        "services_full": "2 chambres climatisées, salon climatisé avec canapé-lit"
    },
    {
        "id": "3",
        "name": "Villa F3 sur le François",
        "location": "Hauteurs du Morne Carrière au François",
        "type": "F3",
        "guests": 4,
        "guests_detail": "4 personnes (maximum 10 invités)",
        "price": 800.0,
        "features": "Stationnement pour 5 véhicules, enceintes JBL autorisées",
        "description": "Caution: 1000€ (850€ par chèque et 150€ en espèces). Check-in: 16h, Check-out: 11h (option late check-out: +80€). Frais de 50€ par 30 minutes de retard pour la remise des clés. Villa à rendre propre et rangée.",
        "category": "sejour",
        "image": "/images/Villa_F3_Le_Francois/01_vue_generale.jpg",
        "gallery": [
            "/images/Villa_F3_Le_Francois/01_vue_generale.jpg",
            "/images/Villa_F3_Le_Francois/02_piscine_vue_mer.jpg",
            "/images/Villa_F3_Le_Francois/03_terrasse_panoramique.jpg",
            "/images/Villa_F3_Le_Francois/04_salon_moderne.jpg",
            "/images/Villa_F3_Le_Francois/05_chambre_principale.jpg"
        ],
        "pricing_details": {
            "base_price": 800,
            "weekend": 800,
            "week": 1376,
            "high_season": 1376,
            "details": "Weekend: 800€ (2 nuits), Semaine: 1376€ (7 jours)"
        },
        "services_full": "Stationnement pour 5 véhicules, enceintes JBL autorisées"
    },
    {
        "id": "4",
        "name": "Villa F5 sur Ste Anne",
        "location": "Quartier les Anglais, Ste Anne",
        "type": "F5",
        "guests": 10,
        "guests_detail": "10 personnes (jusqu'à 15 personnes en journée)",
        "price": 1350.0,
        "features": "4 chambres, 4 salles de bain",
        "description": "Possibilité d'accueillir jusqu'à 15 invités de 9h à 19h. Caution: 500€ en espèces + 1500€ en empreinte CB. Facilités de paiement sans frais supplémentaires avec paiement total avant entrée.",
        "category": "sejour",
        "image": "/images/Villa_F5_Ste_Anne/01_piscine_principale.jpg",
        "gallery": [
            "/images/Villa_F5_Ste_Anne/01_piscine_principale.jpg",
            "/images/Villa_F5_Ste_Anne/02_piscine_vue_aerienne.jpg",
            "/images/Villa_F5_Ste_Anne/03_facade_villa_rose.jpg",
            "/images/Villa_F5_Ste_Anne/04_terrasse_salon_exterieur.jpg",
            "/images/Villa_F5_Ste_Anne/05_salon_interieur_moderne.jpg"
        ],
        "pricing_details": {
            "base_price": 1350,
            "weekend": 1350,
            "week": 2251,
            "high_season": 2251,
            "details": "Weekend: 1350€ (2 nuits, hors vacances scolaires), Semaine: 2251€ (7 jours)"
        },
        "services_full": "4 chambres, 4 salles de bain"
    },
    {
        "id": "5",
        "name": "Villa F6 au Lamentin",
        "location": "Quartier Béleme, Lamentin",
        "type": "F6",
        "guests": 10,
        "guests_detail": "10 personnes (jusqu'à 20 invités en journée)",
        "price": 1200.0,
        "features": "Piscine, jacuzzi",
        "description": "Fêtes autorisées de 10h à 19h. Disponibilité vacances: du 1er au 10 juillet et du 25 au 31 août. Check-in: 15h, check-out: 18h. Pénalité retard clés: 150€/30min. Caution: 1000€ (empreinte bancaire). Covoiturage obligatoire.",
        "category": "sejour",
        "image": "/images/Villa_F6_Lamentin/01_piscine_jacuzzi.jpg",
        "gallery": [
            "/images/Villa_F6_Lamentin/01_piscine_jacuzzi.jpg",
            "/images/Villa_F6_Lamentin/02_vue_generale_villa.jpg",
            "/images/Villa_F6_Lamentin/03_terrasse_exterieure.jpg",
            "/images/Villa_F6_Lamentin/04_salon_spacieux.jpg",
            "/images/Villa_F6_Lamentin/05_chambre_climatisee.jpg"
        ],
        "pricing_details": {
            "base_price": 1200,
            "weekend": 1500,
            "week": 2800,
            "high_season": 2800,
            "party_supplement": 300,
            "details": "Weekend: 1500€ (vendredi-dimanche), Weekend 2 nuits: 1200€ (sans invités), Semaine: 2800€ (8 jours), +300€ si fête"
        },
        "services_full": "Piscine, jacuzzi"
    },
    {
        "id": "6",
        "name": "Villa F6 sur Ste Luce à 1mn de la plage",
        "location": "Zac de Pont Café, Ste Luce, à 1mn de la plage Corps de garde",
        "type": "F6",
        "guests": 12,
        "guests_detail": "10 à 14 personnes",
        "price": 1700.0,
        "features": "5 appartements (2 F2 duplex et 3 F2), dont un en sous-sol",
        "description": "Check-in: 17h, Check-out: 11h. Caution: 1500€ par chèque + 500€ en espèces (remboursables). Location uniquement à la semaine pendant les vacances scolaires. Facilités de paiement sans frais supplémentaires (tout doit être payé avant l'entrée).",
        "category": "sejour",
        "image": "/images/Villa_F6_Ste_Luce_Plage/01_facade_proche_plage.jpg",
        "gallery": [
            "/images/Villa_F6_Ste_Luce_Plage/01_facade_proche_plage.jpg",
            "/images/Villa_F6_Ste_Luce_Plage/02_appartements_duplex.jpg",
            "/images/Villa_F6_Ste_Luce_Plage/03_terrasse_vue_mer.jpg",
            "/images/Villa_F6_Ste_Luce_Plage/04_salon_moderne.jpg",
            "/images/Villa_F6_Ste_Luce_Plage/05_cuisine_equipee.jpg"
        ],
        "pricing_details": {
            "base_price": 1700,
            "weekend": 1700,
            "week": 2200,
            "high_season": 2850,
            "details": "Weekend: 1700€, Semaine (8 jours): 2200€ à 2850€"
        },
        "services_full": "5 appartements (2 F2 duplex et 3 F2), dont un en sous-sol"
    },
    {
        "id": "7",
        "name": "Villa F3 Bas de villa Trinité Cosmy",
        "location": "Cosmy, Trinité",
        "type": "F3",
        "guests": 5,
        "guests_detail": "5 adultes ou 4 adultes et 2 enfants (jusqu'à 60 invités pour fêtes)",
        "price": 500.0,
        "features": "2 chambres climatisées, 1 salle de bain, double terrasse, salon, cuisine américaine, piscine privée chauffée",
        "description": "Villa charmante idéale pour séjours entre amis, famille et événements. Environnement calme et relaxant. Horaires fête: 10h-18h ou 14h-22h (départ des invités à partir de 21h). Location à la semaine pendant vacances scolaires (exceptions possibles). Caution: 200€ en espèces + 400€ par chèque.",
        "category": "sejour",
        "image": "/images/Villa_F3_Trinite_Cosmy/01_piscine_chauffee.jpg",
        "gallery": [
            "/images/Villa_F3_Trinite_Cosmy/01_piscine_chauffee.jpg",
            "/images/Villa_F3_Trinite_Cosmy/02_double_terrasse.jpg",
            "/images/Villa_F3_Trinite_Cosmy/03_salon_cuisine_americaine.jpg",
            "/images/Villa_F3_Trinite_Cosmy/04_chambre_climatisee.jpg",
            "/images/Villa_F3_Trinite_Cosmy/05_salle_de_bain_moderne.jpg"
        ],
        "pricing_details": {
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
        "services_full": "2 chambres climatisées, 1 salle de bain, double terrasse, salon, cuisine américaine, piscine privée chauffée"
    },
    {
        "id": "8",
        "name": "Bas de villa F3 sur le Robert",
        "location": "Pointe Hyacinthe, Le Robert",
        "type": "F3",
        "guests": 10,
        "guests_detail": "10 personnes",
        "price": 900.0,
        "features": "2 chambres climatisées, location à la journée possible (lundi-jeudi), excursion nautique possible",
        "description": "Enceintes JBL autorisées jusqu'à 22h (DJ et gros systèmes sono interdits). Caution: 1500€ pour la villa + caution pour l'espace piscine. Paiement en plusieurs fois sans frais possible (tout doit être soldé avant l'entrée).",
        "category": "sejour",
        "image": "/images/Villa_F3_Robert_Pointe_Hyacinthe/01_vue_mer_robert.jpg",
        "gallery": [
            "/images/Villa_F3_Robert_Pointe_Hyacinthe/01_vue_mer_robert.jpg",
            "/images/Villa_F3_Robert_Pointe_Hyacinthe/02_terrasse_vue_mer.jpg",
            "/images/Villa_F3_Robert_Pointe_Hyacinthe/03_salon_moderne.jpg",
            "/images/Villa_F3_Robert_Pointe_Hyacinthe/04_chambre_climatisee.jpg",
            "/images/Villa_F3_Robert_Pointe_Hyacinthe/05_cuisine_equipee.jpg"
        ],
        "pricing_details": {
            "base_price": 900,
            "weekend": 900,
            "week_low": 1250,
            "week_high": 1500,
            "party_supplement": 550,
            "details": "Weekend: 900€, Weekend avec fête/invités: +550€, Semaine: 1250€ (basse saison), 1500€ (haute saison)"
        },
        "services_full": "2 chambres climatisées, location à la journée possible (lundi-jeudi), excursion nautique possible"
    },
    {
        "id": "9",
        "name": "Appartement F3 Trenelle (Location Annuelle)",
        "location": "Trenelle, à 2 minutes du PPM",
        "type": "F3",
        "guests": 2,
        "guests_detail": "Couple sans enfant, personne seule ou 2 colocataires",
        "price": 700.0,
        "features": "Meublé, eau et électricité incluses",
        "description": "Location à l'année (bail de 12 mois) avec possibilité de louer pour 3 ou 6 mois. Accès au logement: 1550€ (2 mois de caution + 1 mois de loyer hors charges).",
        "category": "sejour",
        "image": "/images/Villa_F3_Trenelle_Location_Annuelle/01_appartement_meuble.jpg",
        "gallery": [
            "/images/Villa_F3_Trenelle_Location_Annuelle/01_appartement_meuble.jpg",
            "/images/Villa_F3_Trenelle_Location_Annuelle/02_salon_moderne.jpg",
            "/images/Villa_F3_Trenelle_Location_Annuelle/03_cuisine_equipee.jpg",
            "/images/Villa_F3_Trenelle_Location_Annuelle/04_chambre_principale.jpg",
            "/images/Villa_F3_Trenelle_Location_Annuelle/05_salle_de_bain.jpg"
        ],
        "pricing_details": {
            "base_price": 700,
            "monthly": 700,
            "annual": 8400,
            "details": "700€/mois (eau et EDF inclus)"
        },
        "services_full": "Meublé, eau et électricité incluses"
    },
    {
        "id": "10",
        "name": "Villa F5 Vauclin Ravine Plate",
        "location": "Hauteurs de Ravine Plate, Vauclin",
        "type": "F5",
        "guests": 8,
        "guests_detail": "8 personnes",
        "price": 1550.0,
        "features": "4 chambres climatisées avec salle d'eau attenante, piscine à débordement",
        "description": "Caution: 1500€ par chèque et 500€ en espèces, remboursée à la sortie si aucun dommage. Paiement en plusieurs fois sans frais possible, solde à régler avant l'entrée.",
        "category": "sejour",
        "image": "/images/Villa_F5_Vauclin_Ravine_Plate/01_piscine_debordement.jpg",
        "gallery": [
            "/images/Villa_F5_Vauclin_Ravine_Plate/01_piscine_debordement.jpg",
            "/images/Villa_F5_Vauclin_Ravine_Plate/02_vue_panoramique.jpg",
            "/images/Villa_F5_Vauclin_Ravine_Plate/03_terrasse_vue_mer.jpg",
            "/images/Villa_F5_Vauclin_Ravine_Plate/04_chambre_suite.jpg",
            "/images/Villa_F5_Vauclin_Ravine_Plate/05_salon_moderne.jpg"
        ],
        "pricing_details": {
            "base_price": 1550,
            "weekend": 1550,
            "week": 2500,
            "high_season": 2500,
            "details": "Weekend: 1550€ (vendredi-dimanche), Semaine: 2500€ (8 jours)"
        },
        "services_full": "4 chambres climatisées avec salle d'eau attenante, piscine à débordement"
    },
    {
        "id": "11",
        "name": "Villa F5 La Renée",
        "location": "Quartier La Renée, Rivière-Pilote",
        "type": "F5",
        "guests": 10,
        "guests_detail": "10 personnes (jusqu'à 60 invités pour fêtes)",
        "price": 900.0,
        "features": "4 chambres, 2 salles de bain, grande cuisine, grand salon, grande terrasse, jacuzzi, Wi‑Fi",
        "description": "Horaires fêtes: 9h-00h. Caution: 1500€ par chèque. Covoiturage recommandé. Paiement possible en quatre fois par carte bancaire, même si le séjour a commencé.",
        "category": "sejour",
        "image": "/images/Villa_F5_R_Pilote_La_Renee/01_villa_spacieuse.jpg",
        "gallery": [
            "/images/Villa_F5_R_Pilote_La_Renee/01_villa_spacieuse.jpg",
            "/images/Villa_F5_R_Pilote_La_Renee/02_jacuzzi_terrasse.jpg",
            "/images/Villa_F5_R_Pilote_La_Renee/03_grande_cuisine.jpg",
            "/images/Villa_F5_R_Pilote_La_Renee/04_salon_spacieux.jpg",
            "/images/Villa_F5_R_Pilote_La_Renee/05_chambre_principale.jpg"
        ],
        "pricing_details": {
            "base_price": 900,
            "weekend": 900,
            "weekend_party": 1400,
            "week": 1590,
            "week_party": 2000,
            "details": "Weekend avec fête: 1400€, Weekend sans fête: 900€, Semaine avec fête: 2000€, Semaine sans fête: 1590€"
        },
        "services_full": "4 chambres, 2 salles de bain, grande cuisine, grand salon, grande terrasse, jacuzzi, Wi‑Fi"
    },
    {
        "id": "12",
        "name": "Villa F7 Baie des Mulets",
        "location": "Baie des Mulets, Vauclin",
        "type": "F7",
        "guests": 16,
        "guests_detail": "16 personnes (F5: 10 personnes + F3: 6 personnes)",
        "price": 2200.0,
        "features": "F5: 4 chambres climatisées + salon avec canapé-lit; F3: salon avec canapé-lit. Parking pour 30 véhicules",
        "description": "Check-in: 11h, Check-out: 13h (option late check-out 17h30: +150€). Fêtes autorisées de 9h à minuit. Location possible à la journée (lundi-jeudi) selon disponibilité. Caution: 1500€ par chèque ou empreinte bancaire. Paiement possible en plusieurs fois, sans frais, avec solde 72h avant entrée.",
        "category": "sejour",
        "image": "/images/Villa_F7_Baie_des_Mulets_Vauclin/01_vue_generale_f7.jpg",
        "gallery": [
            "/images/Villa_F7_Baie_des_Mulets_Vauclin/01_vue_generale_f7.jpg",
            "/images/Villa_F7_Baie_des_Mulets_Vauclin/02_piscine_spacieuse.jpg",
            "/images/Villa_F7_Baie_des_Mulets_Vauclin/03_terrasse_panoramique.jpg",
            "/images/Villa_F7_Baie_des_Mulets_Vauclin/04_salon_f5.jpg",
            "/images/Villa_F7_Baie_des_Mulets_Vauclin/05_parking_30_vehicules.jpg",
            "/images/Villa_F7_Baie_des_Mulets_Vauclin/06_chambre_climatisee.jpg"
        ],
        "pricing_details": {
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
        "services_full": "F5: 4 chambres climatisées + salon avec canapé-lit; F3: salon avec canapé-lit. Parking pour 30 véhicules"
    },
    {
        "id": "13",
        "name": "Bas de villa F3 sur Ste Luce",
        "location": "Sainte-Luce",
        "type": "F3",
        "guests": 4,
        "guests_detail": "4 personnes",
        "price": 470.0,
        "features": "Bas de villa F3, pas d'invités autorisés",
        "description": "Fêtes et invités ne sont plus acceptés suite aux abus. Caution: 1300€ par chèque + 200€ en espèces. Acompte: 30%. Solde à payer le jour d'arrivée.",
        "category": "sejour",
        "image": "/images/Bas_Villa_F3_Ste_Luce/01_bas_villa_ste_luce.jpg",
        "gallery": [
            "/images/Bas_Villa_F3_Ste_Luce/01_bas_villa_ste_luce.jpg",
            "/images/Bas_Villa_F3_Ste_Luce/02_terrasse_privee.jpg",
            "/images/Bas_Villa_F3_Ste_Luce/03_salon_cosy.jpg",
            "/images/Bas_Villa_F3_Ste_Luce/04_chambre_calme.jpg",
            "/images/Bas_Villa_F3_Ste_Luce/05_cuisine_equipee.jpg"
        ],
        "pricing_details": {
            "base_price": 470,
            "weekend": 470,
            "week": 1030,
            "high_season_weekend": 570,
            "high_season_week": 1390,
            "details": "Juil/Août/Déc/Jan: 1390€/semaine ou 570€/weekend (2 nuits), Mai/Juin/Sept: 1030€/semaine ou 470€/weekend"
        },
        "services_full": "Bas de villa F3, pas d'invités autorisés"
    },
    {
        "id": "14",
        "name": "Studio Cocooning Lamentin",
        "location": "Hauteurs de Morne Pitault, Lamentin",
        "type": "Studio",
        "guests": 2,
        "guests_detail": "2 personnes",
        "price": 290.0,
        "features": "Bac à punch privé (petite piscine)",
        "description": "Pas d'invités autorisés. Location uniquement à la semaine pendant les vacances scolaires et haute saison touristique. Check-in: 16h, Check-out: 11h (départ tardif possible selon disponibilité). Paiement en plusieurs fois sans frais possible (tout doit être réglé avant entrée).",
        "category": "sejour",
        "image": "/images/Studio_Cocooning_Lamentin/01_studio_cocooning.jpg",
        "gallery": [
            "/images/Studio_Cocooning_Lamentin/01_studio_cocooning.jpg",
            "/images/Studio_Cocooning_Lamentin/02_bac_punch_prive.jpg",
            "/images/Studio_Cocooning_Lamentin/03_interieur_cosy.jpg",
            "/images/Studio_Cocooning_Lamentin/04_coin_nuit.jpg",
            "/images/Studio_Cocooning_Lamentin/05_kitchenette.jpg"
        ],
        "pricing_details": {
            "base_price": 290,
            "weekend": 290,
            "week": 2030,
            "high_season": 2030,
            "details": "À partir de 290€, minimum 2 nuits"
        },
        "services_full": "Bac à punch privé (petite piscine)"
    },
    {
        "id": "15",
        "name": "Villa Fête Journée Ducos",
        "location": "Ducos",
        "type": "Location journée",
        "guests": 15,
        "guests_detail": "5 à 30 personnes",
        "price": 375.0,
        "features": "Piscine, espace extérieur",
        "description": "12 places de parking + stationnement supplémentaire possible en bordure de route. Enfants comptés à partir de 6 ans. Paiement possible en plusieurs fois sans frais, mais doit être réglé avant l'entrée.",
        "category": "fete",
        "image": "/images/Villa_Fete_Journee_Ducos/01_espace_fete_ducos.jpg",
        "gallery": [
            "/images/Villa_Fete_Journee_Ducos/01_espace_fete_ducos.jpg",
            "/images/Villa_Fete_Journee_Ducos/02_piscine_fete.jpg",
            "/images/Villa_Fete_Journee_Ducos/03_espace_exterieur.jpg",
            "/images/Villa_Fete_Journee_Ducos/04_parking_multiple.jpg"
        ],
        "pricing_details": {
            "base_price": 375,
            "person_rate": 30,
            "formula_1": {
                "15_pers": 375,
                "20_pers": 440,
                "30_pers": 510
            },
            "details": "Formule 1 (10h-20h): 30€/personne, Package 15 pers: 375€, 20 pers: 440€, 30 pers: 510€"
        },
        "services_full": "Piscine, espace extérieur"
    },
    {
        "id": "16",
        "name": "Villa Fête Journée Fort de France",
        "location": "Fort de France",
        "type": "Location journée",
        "guests": 50,
        "guests_detail": "20 à 80 personnes",
        "price": 100.0,
        "features": "Prestations à la carte",
        "description": "Disponible de 6h à minuit. Paiement possible en plusieurs fois sans frais (tout doit être réglé avant entrée).",
        "category": "fete",
        "image": "/images/Villa_Fete_Journee_Fort_de_France/01_espace_fete_fdf.jpg",
        "gallery": [
            "/images/Villa_Fete_Journee_Fort_de_France/01_espace_fete_fdf.jpg",
            "/images/Villa_Fete_Journee_Fort_de_France/02_prestations_carte.jpg",
            "/images/Villa_Fete_Journee_Fort_de_France/03_espace_modulable.jpg"
        ],
        "pricing_details": {
            "base_price": 100,
            "hourly_rate": 100,
            "details": "À partir de 100€/heure"
        },
        "services_full": "Prestations à la carte"
    },
    {
        "id": "17",
        "name": "Villa Fête Journée Rivière-Pilote",
        "location": "Rivière-Pilote",
        "type": "Location journée",
        "guests": 100,
        "guests_detail": "Jusqu'à 100 invités",
        "price": 660.0,
        "features": "Piscine chauffée, cuisine extérieure équipée (four, micro-onde, congélateur, bar office), DJ autorisé, bungalow 2 personnes (130€/nuit), appartement 2 personnes (110€/nuit)",
        "description": "Horaires fête: 13h-20h ou 18h-2h. Caution: 800€.",
        "category": "fete",
        "image": "/images/Villa_Fete_Journee_R_Pilote/01_piscine_chauffee_fete.jpg",
        "gallery": [
            "/images/Villa_Fete_Journee_R_Pilote/01_piscine_chauffee_fete.jpg",
            "/images/Villa_Fete_Journee_R_Pilote/02_cuisine_exterieure.jpg",
            "/images/Villa_Fete_Journee_R_Pilote/03_espace_dj.jpg",
            "/images/Villa_Fete_Journee_R_Pilote/04_bungalow_hebergement.jpg"
        ],
        "pricing_details": {
            "base_price": 660,
            "private_event": 660,
            "details": "660€ pour événement privé (anniversaire enfant, enterrement vie célibataire). Devis personnalisé pour mariage, baptême, communion."
        },
        "services_full": "Piscine chauffée, cuisine extérieure équipée (four, micro-onde, congélateur, bar office), DJ autorisé, bungalow 2 personnes (130€/nuit), appartement 2 personnes (110€/nuit)"
    },
    {
        "id": "18",
        "name": "Villa Fête Journée Rivière Salée",
        "location": "Quartier La Laugier, Rivière Salée",
        "type": "Location journée",
        "guests": 50,
        "guests_detail": "De 25 à 100 personnes (selon forfait)",
        "price": 400.0,
        "features": "5 tables rectangulaires, chaises plastiques selon forfait",
        "description": "Pour événements utilisant la piscine: maître-nageur ou pompier obligatoire aux frais de l'organisateur (sinon barrière de sécurité installée). Déchets à enlever après l'événement. Acompte 30% à la réservation, solde 48h avant l'événement.",
        "category": "fete",
        "image": "/images/Villa_Fete_Journee_Riviere_Salee/01_espace_modulable.jpg",
        "gallery": [
            "/images/Villa_Fete_Journee_Riviere_Salee/01_espace_modulable.jpg",
            "/images/Villa_Fete_Journee_Riviere_Salee/02_tables_exterieures.jpg",
            "/images/Villa_Fete_Journee_Riviere_Salee/03_piscine_securisee.jpg"
        ],
        "pricing_details": {
            "base_price": 400,
            "forfait_1": 400,
            "forfait_2": 550,
            "forfait_3": 750,
            "forfait_4": 1000,
            "details": "Forfait 1 (12h-19h): 400€ (25 pers). Forfait 2 (12h-19h): 550€ (50 pers). Forfait 3 (8h-22h): 750€ (50 pers). Forfait 4 (8h-22h): 1000€ (100 pers)."
        },
        "services_full": "5 tables rectangulaires, chaises plastiques selon forfait"
    },
    {
        "id": "19",
        "name": "Villa Fête Journée Sainte-Luce",
        "location": "Sainte-Luce, près de la Forêt Montravail",
        "type": "Location journée",
        "guests": 30,
        "guests_detail": "Jusqu'à 40 personnes",
        "price": 390.0,
        "features": "3 tentes, 3 salons extérieurs, 2 grandes tables, 1 réfrigérateur, évier extérieur, douche, WC, système son JBL",
        "description": "Horaires: 10h-18h (flexible). Caution: 800€ par chèque. Covoiturage recommandé. Paiement sans frais possible, tout doit être réglé avant entrée.",
        "category": "fete",
        "image": "/images/Villa_Fete_Journee_Sainte_Luce/01_tentes_exterieures.jpg",
        "gallery": [
            "/images/Villa_Fete_Journee_Sainte_Luce/01_tentes_exterieures.jpg",
            "/images/Villa_Fete_Journee_Sainte_Luce/02_salons_exterieurs.jpg",
            "/images/Villa_Fete_Journee_Sainte_Luce/03_equipements_complets.jpg"
        ],
        "pricing_details": {
            "base_price": 390,
            "for_20_guests": 390,
            "for_40_guests": 560,
            "details": "390€ pour 20 personnes, 560€ pour 40 personnes"
        },
        "services_full": "3 tentes, 3 salons extérieurs, 2 grandes tables, 1 réfrigérateur, évier extérieur, douche, WC, système son JBL"
    },
    {
        "id": "20",
        "name": "Espace Piscine Journée Bungalow",
        "location": "Martinique",
        "type": "Location journée",
        "guests": 100,
        "guests_detail": "10 à 150 personnes",
        "price": 350.0,
        "features": "Cuisine, salle d'eau, mobilier (chaises, tables), chambre climatisée (+80€ supplémentaire)",
        "description": "Location de 9h à 19h uniquement (pas de possibilité au-delà de 19h). Tarifs uniquement pour anniversaires, baby-showers et enterrements de vie. Caution: 1000€ par chèque + 250€ en espèces. Autres forfaits sur demande selon type d'événement (mariage, baptême, etc.).",
        "category": "fete",
        "image": "/images/Espace_Piscine_Journee_Bungalow/01_espace_piscine.jpg",
        "gallery": [
            "/images/Espace_Piscine_Journee_Bungalow/01_espace_piscine.jpg",
            "/images/Espace_Piscine_Journee_Bungalow/02_bungalow_hebergement.jpg",
            "/images/Espace_Piscine_Journee_Bungalow/03_cuisine_equipee.jpg",
            "/images/Espace_Piscine_Journee_Bungalow/04_mobilier_fete.jpg"
        ],
        "pricing_details": {
            "base_price": 350,
            "up_to_20": 350,
            "up_to_40": 550,
            "up_to_60": 750,
            "bungalow_extra": 85,
            "details": "Forfaits Journée (9h-19h): Jusqu'à 20 invités 350€, Jusqu'à 40 invités: 550€, Jusqu'à 60 invités: 750€, Bungalow pour 2 personnes: +85€/nuit"
        },
        "services_full": "Cuisine, salle d'eau, mobilier (chaises, tables), chambre climatisée (+80€ supplémentaire)"
    },
    {
        "id": "21",
        "name": "Villa F6 sur Petit Macabou (séjour + fête)",
        "location": "Petit Macabou au Vauclin (972)",
        "type": "F6",
        "guests": 12,
        "guests_detail": "10 à 13 personnes (jusqu'à 30 invités pour fêtes)",
        "price": 2000.0,
        "features": "3 chambres climatisées avec salle de bain attenante, 1 mezzanine, 2 studios aux extrémités, possibilité de louer 3 bungalows supplémentaires avec bac à punch",
        "description": "Villa somptueuse et très spacieuse. Événements ou fêtes autorisés de 9h à 19h. Mariage ou baptême avec hébergements sur demande jusqu'à 150 invités. Covoiturage recommandé. Caution: 2500€ par chèque.",
        "category": "sejour",
        "image": "/images/Villa_F6_Petit_Macabou/01_villa_somptueuse.jpg",
        "gallery": [
            "/images/Villa_F6_Petit_Macabou/01_villa_somptueuse.jpg",
            "/images/Villa_F6_Petit_Macabou/02_mezzanine_spacieuse.jpg",
            "/images/Villa_F6_Petit_Macabou/03_studios_exterieurs.jpg",
            "/images/Villa_F6_Petit_Macabou/04_bungalows_additionnels.jpg",
            "/images/Villa_F6_Petit_Macabou/05_terrasse_panoramique.jpg",
            "/images/Villa_F6_Petit_Macabou/06_salle_de_bain_moderne.jpg",
            "/images/Villa_F6_Petit_Macabou/07_chambre_climatisee.jpg"
        ],
        "pricing_details": {
            "base_price": 2000,
            "weekend": 2000,
            "week": 3220,
            "high_season": 3220,
            "details": "Weekend: 2000€, Semaine: à partir de 3220€"
        },
        "services_full": "3 chambres climatisées avec salle de bain attenante, 1 mezzanine, 2 studios aux extrémités, possibilité de louer 3 bungalows supplémentaires avec bac à punch"
    }
]

async def integrate_21_real_villas():
    """Intègre les 21 vraies villas du CSV dans la base de données"""
    
    # Connexion à MongoDB
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017/')
    client = AsyncIOMotorClient(mongo_url)
    db = client.khanelconcept
    collection = db.villas
    
    print("🔄 Connexion à MongoDB...")
    
    # Supprimer toutes les villas existantes (nettoyage complet)
    result = await collection.delete_many({})
    print(f"🗑️ Supprimé {result.deleted_count} villas existantes")
    
    # Insérer les 21 vraies villas
    inserted_count = 0
    for villa_data in VILLAS_CSV_DATA:
        # Ajouter les champs additionnels requis
        villa_data.update({
            "fallback_icon": "🏖️",
            "amenities": ["Piscine", "WiFi", "Climatisation"],
            "available_dates": [],
            "csv_integrated": True,
            "csv_source": "Catalogue_Villas_Khanel_Concept_Complet_Final.csv",
            "csv_updated": datetime.now().isoformat(),
            "integration_date": datetime.now().isoformat()
        })
        
        # Insérer la villa
        result = await collection.insert_one(villa_data)
        if result.inserted_id:
            inserted_count += 1
            print(f"✅ Villa {villa_data['id']}: {villa_data['name']} - Intégrée")
        else:
            print(f"❌ Erreur lors de l'insertion de {villa_data['name']}")
    
    print(f"\n🎉 Intégration terminée !")
    print(f"📊 {inserted_count} villas intégrées sur 21 prévues")
    
    # Vérification finale
    total_villas = await collection.count_documents({})
    print(f"🔍 Vérification: {total_villas} villas dans la base de données")
    
    # Afficher quelques exemples
    print("\n📋 Exemples de villas intégrées:")
    async for villa in collection.find({}).limit(5):
        print(f"  - {villa['name']} (Prix: {villa['price']}€, Capacité: {villa['guests']} pers)")
    
    client.close()
    return inserted_count

async def main():
    """Fonction principale"""
    print("🏖️ INTÉGRATION DES 21 VRAIES VILLAS KHANELCONCEPT")
    print("=" * 60)
    
    try:
        result = await integrate_21_real_villas()
        print(f"\n✅ Succès ! {result} villas intégrées correctement")
        print("📌 L'onglet tarification existant affichera maintenant les données CSV")
        
    except Exception as e:
        print(f"\n❌ Erreur durant l'intégration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())