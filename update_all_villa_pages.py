#!/usr/bin/env python3
"""
Mise à jour de toutes les pages de villas individuelles avec les données CSV
- Remplace "Tarification" par "Information et tarifs"
- Intègre toutes les données du CSV
- Garde la même interface
"""

import os
import glob
from pathlib import Path

# Mapping des données CSV par nom de villa
VILLA_CSV_DATA = {
    "Villa F3 sur Petit Macabou": {
        "name": "Villa F3 sur Petit Macabou",
        "location": "Petit Macabou, Vauclin",
        "price": 850,
        "guests": "6 personnes (jusqu'à 15 personnes en journée)",
        "pricing": {
            "base": 850,
            "weekend": 850,
            "week": 1550,
            "high_season": 1690,
            "details": "Grandes Vacances: 1550€/semaine, Weekend: 850€ (2 nuits), Noël/Nouvel An: 1690€/semaine"
        },
        "services": "Chambres climatisées, 1 salle de bain avec WC, WC indépendant, salon climatisé avec canapé-lit, sauna, jacuzzi, 2 douches extérieures",
        "description": "Villa avec possibilité d'accueillir 9 invités supplémentaires en journée (9h-20h). Caution: 1500€. Check-in: 16h, Check-out: 11h (possibilité extension jusqu'à 16h selon disponibilité).",
        "file": "villa-f3-petit-macabou.html"
    },
    "Villa F3 POUR LA BACCHA": {
        "name": "Villa F3 POUR LA BACCHA",
        "location": "Petit Macabou",
        "price": 1350,
        "guests": "6 personnes",
        "pricing": {
            "base": 1350,
            "weekend": 1350,
            "week": 1350,
            "high_season": 1350,
            "details": "Août: 1350€/semaine, Juillet: complet"
        },
        "services": "2 chambres climatisées, salon climatisé avec canapé-lit",
        "description": "Possibilité d'accueillir jusqu'à 9 invités entre 9h et 18h. Caution: 1500€ par chèque. Règles strictes concernant le bruit pour respecter le voisinage.",
        "file": "villa-f3-baccha-petit-macabou.html"
    },
    "Villa F3 sur le François": {
        "name": "Villa F3 sur le François",
        "location": "Hauteurs du Morne Carrière au François",
        "price": 800,
        "guests": "4 personnes (maximum 10 invités)",
        "pricing": {
            "base": 800,
            "weekend": 800,
            "week": 1376,
            "high_season": 1376,
            "details": "Weekend: 800€ (2 nuits), Semaine: 1376€ (7 jours)"
        },
        "services": "Stationnement pour 5 véhicules, enceintes JBL autorisées",
        "description": "Caution: 1000€ (850€ par chèque et 150€ en espèces). Check-in: 16h, Check-out: 11h (option late check-out: +80€). Frais de 50€ par 30 minutes de retard pour la remise des clés. Villa à rendre propre et rangée.",
        "file": "villa-f3-le-francois.html"
    },
    "Villa F5 sur Ste Anne": {
        "name": "Villa F5 sur Ste Anne",
        "location": "Quartier les Anglais, Ste Anne",
        "price": 1350,
        "guests": "10 personnes (jusqu'à 15 personnes en journée)",
        "pricing": {
            "base": 1350,
            "weekend": 1350,
            "week": 2251,
            "high_season": 2251,
            "details": "Weekend: 1350€ (2 nuits, hors vacances scolaires), Semaine: 2251€ (7 jours)"
        },
        "services": "4 chambres, 4 salles de bain",
        "description": "Possibilité d'accueillir jusqu'à 15 invités de 9h à 19h. Caution: 500€ en espèces + 1500€ en empreinte CB. Facilités de paiement sans frais supplémentaires avec paiement total avant entrée.",
        "file": "villa-f5-ste-anne.html"
    },
    "Villa F6 au Lamentin": {
        "name": "Villa F6 au Lamentin",
        "location": "Quartier Béleme, Lamentin",
        "price": 1200,
        "guests": "10 personnes (jusqu'à 20 invités en journée)",
        "pricing": {
            "base": 1200,
            "weekend": 1500,
            "week": 2800,
            "high_season": 2800,
            "party_supplement": 300,
            "details": "Weekend: 1500€ (vendredi-dimanche), Weekend 2 nuits: 1200€ (sans invités), Semaine: 2800€ (8 jours), +300€ si fête"
        },
        "services": "Piscine, jacuzzi",
        "description": "Fêtes autorisées de 10h à 19h. Disponibilité vacances: du 1er au 10 juillet et du 25 au 31 août. Check-in: 15h, check-out: 18h. Pénalité retard clés: 150€/30min. Caution: 1000€ (empreinte bancaire). Covoiturage obligatoire.",
        "file": "villa-f6-lamentin.html"
    },
    "Villa F6 sur Ste Luce à 1mn de la plage": {
        "name": "Villa F6 sur Ste Luce à 1mn de la plage",
        "location": "Zac de Pont Café, Ste Luce, à 1mn de la plage Corps de garde",
        "price": 1700,
        "guests": "10 à 14 personnes",
        "pricing": {
            "base": 1700,
            "weekend": 1700,
            "week": 2200,
            "high_season": 2850,
            "details": "Weekend: 1700€, Semaine (8 jours): 2200€ à 2850€"
        },
        "services": "5 appartements (2 F2 duplex et 3 F2), dont un en sous-sol",
        "description": "Check-in: 17h, Check-out: 11h. Caution: 1500€ par chèque + 500€ en espèces (remboursables). Location uniquement à la semaine pendant les vacances scolaires. Facilités de paiement sans frais supplémentaires (tout doit être payé avant l'entrée).",
        "file": "villa-f6-ste-luce-plage.html"
    },
    "Villa F3 Bas de villa Trinité Cosmy": {
        "name": "Villa F3 Bas de villa Trinité Cosmy",
        "location": "Cosmy, Trinité",
        "price": 500,
        "guests": "5 adultes ou 4 adultes et 2 enfants (jusqu'à 60 invités pour fêtes)",
        "pricing": {
            "base": 500,
            "weekend": 500,
            "week": 3500,
            "high_season": 3500,
            "party_rates": "670€ (10 invités) à 1400€ (60 invités)",
            "details": "Weekend sans invités: 500€, Weekend + Fête: 670€ (10 invités) à 1400€ (60 invités)"
        },
        "services": "2 chambres climatisées, 1 salle de bain, double terrasse, salon, cuisine américaine, piscine privée chauffée",
        "description": "Villa charmante idéale pour séjours entre amis, famille et événements. Environnement calme et relaxant. Horaires fête: 10h-18h ou 14h-22h (départ des invités à partir de 21h). Location à la semaine pendant vacances scolaires (exceptions possibles). Caution: 200€ en espèces + 400€ par chèque.",
        "file": "villa-f3-trinite-cosmy.html"
    },
    "Bas de villa F3 sur le Robert": {
        "name": "Bas de villa F3 sur le Robert",
        "location": "Pointe Hyacinthe, Le Robert",
        "price": 900,
        "guests": "10 personnes",
        "pricing": {
            "base": 900,
            "weekend": 900,
            "week_low": 1250,
            "week_high": 1500,
            "party_supplement": 550,
            "details": "Weekend: 900€, Weekend avec fête/invités: +550€, Semaine: 1250€ (basse saison), 1500€ (haute saison)"
        },
        "services": "2 chambres climatisées, location à la journée possible (lundi-jeudi), excursion nautique possible",
        "description": "Enceintes JBL autorisées jusqu'à 22h (DJ et gros systèmes sono interdits). Caution: 1500€ pour la villa + caution pour l'espace piscine. Paiement en plusieurs fois sans frais possible (tout doit être soldé avant l'entrée).",
        "file": "villa-f3-robert-pointe-hyacinthe.html"
    },
    "Appartement F3 Trenelle (Location Annuelle)": {
        "name": "Appartement F3 Trenelle (Location Annuelle)",
        "location": "Trenelle, à 2 minutes du PPM",
        "price": 700,
        "guests": "Couple sans enfant, personne seule ou 2 colocataires",
        "pricing": {
            "base": 700,
            "monthly": 700,
            "annual": 8400,
            "details": "700€/mois (eau et EDF inclus)"
        },
        "services": "Meublé, eau et électricité incluses",
        "description": "Location à l'année (bail de 12 mois) avec possibilité de louer pour 3 ou 6 mois. Accès au logement: 1550€ (2 mois de caution + 1 mois de loyer hors charges).",
        "file": "villa-f3-trenelle-location-annuelle.html"
    },
    "Villa F5 Vauclin Ravine Plate": {
        "name": "Villa F5 Vauclin Ravine Plate",
        "location": "Hauteurs de Ravine Plate, Vauclin",
        "price": 1550,
        "guests": "8 personnes",
        "pricing": {
            "base": 1550,
            "weekend": 1550,
            "week": 2500,
            "high_season": 2500,
            "details": "Weekend: 1550€ (vendredi-dimanche), Semaine: 2500€ (8 jours)"
        },
        "services": "4 chambres climatisées avec salle d'eau attenante, piscine à débordement",
        "description": "Caution: 1500€ par chèque et 500€ en espèces, remboursée à la sortie si aucun dommage. Paiement en plusieurs fois sans frais possible, solde à régler avant l'entrée.",
        "file": "villa-f5-vauclin-ravine-plate.html"
    },
    "Villa F5 La Renée": {
        "name": "Villa F5 La Renée",
        "location": "Quartier La Renée, Rivière-Pilote",
        "price": 900,
        "guests": "10 personnes (jusqu'à 60 invités pour fêtes)",
        "pricing": {
            "base": 900,
            "weekend": 900,
            "weekend_party": 1400,
            "week": 1590,
            "week_party": 2000,
            "details": "Weekend avec fête: 1400€, Weekend sans fête: 900€, Semaine avec fête: 2000€, Semaine sans fête: 1590€"
        },
        "services": "4 chambres, 2 salles de bain, grande cuisine, grand salon, grande terrasse, jacuzzi, Wi‑Fi",
        "description": "Horaires fêtes: 9h-00h. Caution: 1500€ par chèque. Covoiturage recommandé. Paiement possible en quatre fois par carte bancaire, même si le séjour a commencé.",
        "file": "villa-f5-r-pilote-la-renee.html"
    },
    "Villa F7 Baie des Mulets": {
        "name": "Villa F7 Baie des Mulets",
        "location": "Baie des Mulets, Vauclin",
        "price": 2200,
        "guests": "16 personnes (F5: 10 personnes + F3: 6 personnes)",
        "pricing": {
            "base": 2200,
            "weekend": 2200,
            "week": 4200,
            "high_season": 4200,
            "party_rates": "+330€ (30 invités), +550€ (50 invités), +770€ (80 invités), +1375€ (160 invités)",
            "details": "Base: 2200€/weekend, 4200€/semaine. Fêtes: +330€ (30 invités), +550€ (50 invités), +770€ (80 invités), +1375€ (160 invités)"
        },
        "services": "F5: 4 chambres climatisées + salon avec canapé-lit; F3: salon avec canapé-lit. Parking pour 30 véhicules",
        "description": "Check-in: 11h, Check-out: 13h (option late check-out 17h30: +150€). Fêtes autorisées de 9h à minuit. Location possible à la journée (lundi-jeudi) selon disponibilité. Caution: 1500€ par chèque ou empreinte bancaire. Paiement possible en plusieurs fois, sans frais, avec solde 72h avant entrée.",
        "file": "villa-f7-baie-des-mulets-vauclin.html"
    },
    "Studio Cocooning Lamentin": {
        "name": "Studio Cocooning Lamentin",
        "location": "Hauteurs de Morne Pitault, Lamentin",
        "price": 290,
        "guests": "2 personnes",
        "pricing": {
            "base": 290,
            "weekend": 290,
            "week": 2030,
            "high_season": 2030,
            "details": "À partir de 290€, minimum 2 nuits"
        },
        "services": "Bac à punch privé (petite piscine)",
        "description": "Pas d'invités autorisés. Location uniquement à la semaine pendant les vacances scolaires et haute saison touristique. Check-in: 16h, Check-out: 11h (départ tardif possible selon disponibilité). Paiement en plusieurs fois sans frais possible (tout doit être réglé avant entrée).",
        "file": "studio-cocooning-lamentin.html"
    },
    "Villa F6 sur Petit Macabou (séjour + fête)": {
        "name": "Villa F6 sur Petit Macabou (séjour + fête)",
        "location": "Petit Macabou au Vauclin (972)",
        "price": 2000,
        "guests": "10 à 13 personnes (jusqu'à 30 invités pour fêtes)",
        "pricing": {
            "base": 2000,
            "weekend": 2000,
            "week": 3220,
            "high_season": 3220,
            "details": "Weekend: 2000€, Semaine: à partir de 3220€"
        },
        "services": "3 chambres climatisées avec salle de bain attenante, 1 mezzanine, 2 studios aux extrémités, possibilité de louer 3 bungalows supplémentaires avec bac à punch",
        "description": "Villa somptueuse et très spacieuse. Événements ou fêtes autorisés de 9h à 19h. Mariage ou baptême avec hébergements sur demande jusqu'à 150 invités. Covoiturage recommandé. Caution: 2500€ par chèque.",
        "file": "villa-f6-petit-macabou.html"
    },
    "Villa Fête Journée Ducos": {
        "name": "Villa Fête Journée Ducos",
        "location": "Ducos", 
        "price": 375,
        "guests": "5 à 30 personnes",
        "pricing": {
            "base": 375,
            "person_rate": 30,
            "package_15": 375,
            "package_20": 440,
            "package_30": 510,
            "details": "Formule 1 (10h-20h): 30€/personne, Package 15 pers: 375€, 20 pers: 440€, 30 pers: 510€"
        },
        "services": "Piscine, espace extérieur",
        "description": "12 places de parking + stationnement supplémentaire possible en bordure de route. Enfants comptés à partir de 6 ans. Paiement possible en plusieurs fois sans frais, mais doit être réglé avant l'entrée.",
        "file": "villa-fete-journee-ducos.html"
    },
    "Villa Fête Journée Fort de France": {
        "name": "Villa Fête Journée Fort de France", 
        "location": "Fort de France",
        "price": 100,
        "guests": "20 à 80 personnes",
        "pricing": {
            "base": 100,
            "hourly_rate": 100,
            "details": "À partir de 100€/heure"
        },
        "services": "Prestations à la carte",
        "description": "Disponible de 6h à minuit. Paiement possible en plusieurs fois sans frais (tout doit être réglé avant entrée).",
        "file": "villa-fete-journee-fort-de-france.html"
    },
    "Villa Fête Journée Rivière-Pilote": {
        "name": "Villa Fête Journée Rivière-Pilote",
        "location": "Rivière-Pilote",
        "price": 660,
        "guests": "Jusqu'à 100 invités",
        "pricing": {
            "base": 660,
            "private_event": 660,
            "details": "660€ pour événement privé (anniversaire enfant, enterrement vie célibataire). Devis personnalisé pour mariage, baptême, communion."
        },
        "services": "Piscine chauffée, cuisine extérieure équipée (four, micro-onde, congélateur, bar office), DJ autorisé, bungalow 2 personnes (130€/nuit), appartement 2 personnes (110€/nuit)",
        "description": "Horaires fête: 13h-20h ou 18h-2h. Caution: 800€.",
        "file": "villa-fete-journee-r-pilote.html"
    },
    "Villa Fête Journée Rivière Salée": {
        "name": "Villa Fête Journée Rivière Salée",
        "location": "Quartier La Laugier, Rivière Salée",
        "price": 400,
        "guests": "De 25 à 100 personnes (selon forfait)",
        "pricing": {
            "base": 400,
            "forfait_1": 400,
            "forfait_2": 550,
            "forfait_3": 750,
            "forfait_4": 1000,
            "details": "Forfait 1 (12h-19h): 400€ (25 pers). Forfait 2 (12h-19h): 550€ (50 pers). Forfait 3 (8h-22h): 750€ (50 pers). Forfait 4 (8h-22h): 1000€ (100 pers)."
        },
        "services": "5 tables rectangulaires, chaises plastiques selon forfait",
        "description": "Pour événements utilisant la piscine: maître-nageur ou pompier obligatoire aux frais de l'organisateur (sinon barrière de sécurité installée). Déchets à enlever après l'événement. Acompte 30% à la réservation, solde 48h avant l'événement.",
        "file": "villa-fete-journee-riviere-salee.html"
    },
    "Villa Fête Journée Sainte-Luce": {
        "name": "Villa Fête Journée Sainte-Luce",
        "location": "Sainte-Luce, près de la Forêt Montravail",
        "price": 390,
        "guests": "Jusqu'à 40 personnes",
        "pricing": {
            "base": 390,
            "for_20_guests": 390,
            "for_40_guests": 560,
            "details": "390€ pour 20 personnes, 560€ pour 40 personnes"
        },
        "services": "3 tentes, 3 salons extérieurs, 2 grandes tables, 1 réfrigérateur, évier extérieur, douche, WC, système son JBL",
        "description": "Horaires: 10h-18h (flexible). Caution: 800€ par chèque. Covoiturage recommandé. Paiement sans frais possible, tout doit être réglé avant entrée.",
        "file": "villa-fete-journee-sainte-luce.html"
    }
}

def create_information_tarifs_section(villa_data):
    """Crée la section 'Information et tarifs' en remplacement de 'Tarification'"""
    
    pricing = villa_data["pricing"]
    
    # Construction des cartes de tarifs
    tarif_cards = []
    
    # Prix de base
    tarif_cards.append(f"""
                <div class="tarif-card" style="background: rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 1.5rem; text-align: center; transition: all 0.3s ease; border: 1px solid rgba(255, 255, 255, 0.2);">
                    <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
                        <i class="fas fa-calendar-day" style="color: #4facfe; margin-right: 0.5rem;"></i>
                        <span style="color: white; font-weight: 600;">Base</span>
                    </div>
                    <div style="font-size: 1.8rem; font-weight: bold; color: #4facfe; margin-bottom: 0.5rem;">{pricing['base']}€</div>
                    <div style="color: rgba(255, 255, 255, 0.7); font-size: 0.9rem;">par nuit</div>
                </div>""")
    
    # Weekend
    weekend_price = pricing.get('weekend', pricing['base'])
    tarif_cards.append(f"""
                <div class="tarif-card" style="background: rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 1.5rem; text-align: center; transition: all 0.3s ease; border: 1px solid rgba(255, 255, 255, 0.2);">
                    <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
                        <i class="fas fa-calendar-week" style="color: #00f5ff; margin-right: 0.5rem;"></i>
                        <span style="color: white; font-weight: 600;">Weekend</span>
                    </div>
                    <div style="font-size: 1.8rem; font-weight: bold; color: #00f5ff; margin-bottom: 0.5rem;">{weekend_price}€</div>
                    <div style="color: rgba(255, 255, 255, 0.7); font-size: 0.9rem;">2-3 nuits</div>
                </div>""")
    
    # Semaine
    week_price = pricing.get('week', pricing.get('week_low', pricing.get('monthly', pricing['base'])))
    tarif_cards.append(f"""
                <div class="tarif-card" style="background: rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 1.5rem; text-align: center; transition: all 0.3s ease; border: 1px solid rgba(255, 255, 255, 0.2);">
                    <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
                        <i class="fas fa-calendar-alt" style="color: #10b981; margin-right: 0.5rem;"></i>
                        <span style="color: white; font-weight: 600;">Semaine</span>
                    </div>
                    <div style="font-size: 1.8rem; font-weight: bold; color: #10b981; margin-bottom: 0.5rem;">{week_price}€</div>
                    <div style="color: rgba(255, 255, 255, 0.7); font-size: 0.9rem;">7 jours</div>
                </div>""")
    
    # Haute saison (si différente)
    high_season_price = pricing.get('high_season', pricing.get('week_high', week_price))
    if high_season_price != week_price:
        tarif_cards.append(f"""
                <div class="tarif-card" style="background: rgba(255, 215, 0, 0.2); border-radius: 15px; padding: 1.5rem; text-align: center; transition: all 0.3s ease; border: 1px solid rgba(255, 215, 0, 0.3);">
                    <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
                        <i class="fas fa-star" style="color: #ffd700; margin-right: 0.5rem;"></i>
                        <span style="color: white; font-weight: 600;">Haute saison</span>
                    </div>
                    <div style="font-size: 1.8rem; font-weight: bold; color: #ffd700; margin-bottom: 0.5rem;">{high_season_price}€</div>
                    <div style="color: rgba(255, 255, 255, 0.7); font-size: 0.9rem;">Juillet/Août/Décembre</div>
                </div>""")
    
    # Section complète
    section = f"""
    <!-- Section Information et tarifs -->
    <div class="information-tarifs-section" style="margin: 2rem 0;">
        <div class="glass-card" style="padding: 2rem; border-radius: 20px; background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2);">
            <h3 style="color: white; font-size: 1.5rem; font-weight: bold; margin-bottom: 1.5rem; display: flex; align-items: center;">
                <i class="fas fa-info-circle" style="margin-right: 0.75rem; color: #4facfe;"></i>
                Information et tarifs
            </h3>
            
            <!-- Informations générales -->
            <div style="background: rgba(255, 255, 255, 0.05); padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem;">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
                    <div>
                        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                            <i class="fas fa-users" style="color: #4facfe; margin-right: 0.5rem;"></i>
                            <span style="color: white; font-weight: 600;">Capacité</span>
                        </div>
                        <span style="color: rgba(255, 255, 255, 0.9);">{villa_data['guests']}</span>
                    </div>
                    <div>
                        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                            <i class="fas fa-map-marker-alt" style="color: #4facfe; margin-right: 0.5rem;"></i>
                            <span style="color: white; font-weight: 600;">Localisation</span>
                        </div>
                        <span style="color: rgba(255, 255, 255, 0.9);">{villa_data['location']}</span>
                    </div>
                </div>
                
                <!-- Services -->
                <div style="margin-top: 1rem;">
                    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                        <i class="fas fa-concierge-bell" style="color: #4facfe; margin-right: 0.5rem;"></i>
                        <span style="color: white; font-weight: 600;">Services inclus</span>
                    </div>
                    <span style="color: rgba(255, 255, 255, 0.9);">{villa_data['services']}</span>
                </div>
                
                <!-- Description -->
                <div style="margin-top: 1rem;">
                    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                        <i class="fas fa-file-alt" style="color: #4facfe; margin-right: 0.5rem;"></i>
                        <span style="color: white; font-weight: 600;">Informations importantes</span>
                    </div>
                    <span style="color: rgba(255, 255, 255, 0.9); font-size: 0.9rem; line-height: 1.4;">{villa_data['description']}</span>
                </div>
            </div>
            
            <!-- Grille des tarifs -->
            <div class="tarifs-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
                {''.join(tarif_cards)}
            </div>
            
            <!-- Détails des tarifs -->
            <div style="background: rgba(255, 255, 255, 0.05); padding: 1rem; border-radius: 10px;">
                <div style="display: flex; align-items: flex-start;">
                    <i class="fas fa-euro-sign" style="color: #4facfe; margin-right: 0.5rem; margin-top: 0.2rem;"></i>
                    <span style="color: rgba(255, 255, 255, 0.9); font-size: 0.9rem; line-height: 1.4;">{pricing['details']}</span>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Styles pour hover effects -->
    <style>
        .tarif-card:hover {{
            background: rgba(255, 255, 255, 0.15) !important;
            transform: translateY(-3px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}
        
        @media (max-width: 768px) {{
            .tarifs-grid {{
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)) !important;
            }}
            
            .tarif-card {{
                padding: 1rem !important;
            }}
            
            .tarif-card > div:nth-child(2) {{
                font-size: 1.4rem !important;
            }}
        }}
    </style>"""
    
    return section

def update_villa_page(file_path, villa_data):
    """Met à jour une page de villa avec les nouvelles données"""
    
    if not os.path.exists(file_path):
        print(f"❌ Fichier {file_path} non trouvé")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Chercher et remplacer la section Tarification
        import re
        
        # Pattern pour trouver la section Tarification existante
        tarification_pattern = r'<!-- Section Tarification -->.*?</style>'
        
        # Remplacer par la nouvelle section Information et tarifs
        new_section = create_information_tarifs_section(villa_data)
        
        if re.search(tarification_pattern, content, re.DOTALL):
            content = re.sub(tarification_pattern, new_section, content, flags=re.DOTALL)
            print(f"✅ Remplacement de 'Tarification' par 'Information et tarifs' dans {os.path.basename(file_path)}")
        else:
            # Si pas de section Tarification, ajouter avant </body>
            body_end = content.rfind('</body>')
            if body_end != -1:
                content = content[:body_end] + new_section + '\n\n' + content[body_end:]
                print(f"✅ Ajout de 'Information et tarifs' dans {os.path.basename(file_path)}")
            else:
                print(f"⚠️ Impossible de trouver </body> dans {os.path.basename(file_path)}")
                return False
        
        # Sauvegarder le fichier modifié
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour de {file_path}: {e}")
        return False

def main():
    """Fonction principale"""
    print("🏖️ MISE À JOUR DE TOUTES LES PAGES DE VILLAS")
    print("📋 Remplacement de 'Tarification' par 'Information et tarifs'")
    print("=" * 60)
    
    updated_count = 0
    total_pages = 0
    
    # Trouver toutes les pages de villas
    villa_files = glob.glob("/app/villa-*.html")
    villa_files = [f for f in villa_files if not f.endswith('villa-details.html') and not f.endswith('villa-template.html')]
    
    print(f"📊 {len(villa_files)} pages de villas trouvées")
    
    for file_path in villa_files:
        filename = os.path.basename(file_path)
        total_pages += 1
        
        # Trouver les données correspondantes
        villa_data = None
        for name, data in VILLA_CSV_DATA.items():
            if data['file'] == filename:
                villa_data = data
                break
        
        if villa_data:
            if update_villa_page(file_path, villa_data):
                updated_count += 1
                print(f"  💎 {villa_data['name']} - Prix: {villa_data['price']}€")
            else:
                print(f"  ❌ Échec de mise à jour: {filename}")
        else:
            print(f"  ⚠️ Données CSV non trouvées pour: {filename}")
    
    print(f"\n🎉 Mise à jour terminée !")
    print(f"✅ {updated_count} pages mises à jour sur {total_pages}")
    print(f"📌 Toutes les sections 'Tarification' ont été remplacées par 'Information et tarifs'")

if __name__ == "__main__":
    main()