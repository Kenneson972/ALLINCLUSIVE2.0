#!/usr/bin/env python3
"""
Générateur automatique de pages détails pour les 21 villas KhanelConcept
Génère des pages HTML complètes avec galeries photos et informations détaillées
"""

import os
import json
from pathlib import Path

def discover_villa_images(folder_name):
    """Découvre automatiquement les images disponibles dans un dossier de villa"""
    images_path = Path("/app/images") / folder_name
    if not images_path.exists():
        return []
    
    # Extensions d'images supportées
    image_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    
    # Trouver toutes les images dans le dossier
    images = []
    for file in sorted(images_path.glob('*')):
        if file.is_file() and file.suffix.lower() in image_extensions:
            # Exclure les fichiers d'information catalogue
            if 'information' not in file.name.lower() and 'catalogue' not in file.name.lower():
                images.append(f"./images/{folder_name}/{file.name}")
    
    return images

# Données des 21 villas
villas_data = [
    {
        "id": "villa-f3-petit-macabou",
        "name": "Villa F3 Petit Macabou", 
        "location": "Petit Macabou au Vauclin",
        "price": 850,
        "capacity": "6 + 9",
        "bedrooms": 3,
        "bathrooms": 2,
        "surface": 120,
        "tagline": "Villa de luxe avec sauna, jacuzzi et 2 douches extérieures",
        "folder": "Villa_F3_Petit_Macabou",
        "main_features": ["Sauna", "Jacuzzi", "Piscine", "2 douches extérieures"],
        "description": """
        <p><strong>Découvrez la Villa F3 Petit Macabou, un véritable havre de paix pour votre séjour en Martinique.</strong></p>
        <p>Cette magnifique villa moderne située au cœur du Vauclin vous offre une expérience de détente unique avec ses équipements haut de gamme. Conçue pour accueillir confortablement 6 personnes avec la possibilité de recevoir jusqu'à 9 invités supplémentaires, elle est parfaite pour les familles ou les groupes d'amis en quête d'authenticité et de luxe.</p>
        <p><strong>Les atouts exclusifs de cette villa :</strong><br>
        • Un sauna privatif pour des moments de relaxation absolue<br>
        • Un jacuzzi pour profiter des soirées tropicales<br>
        • Deux douches extérieures pour un contact privilégié avec la nature<br>
        • Une piscine privée entourée d'une terrasse spacieuse</p>
        """
    },
    {
        "id": "villa-f5-ste-anne",
        "name": "Villa F5 Ste Anne",
        "location": "Quartier Les Anglais, Ste Anne", 
        "price": 1300,
        "capacity": "10 + 15",
        "bedrooms": 5,
        "bathrooms": 3,
        "surface": 200,
        "tagline": "Villa distinctive avec décoration rose et grande piscine",
        "folder": "Villa_F5_Ste_Anne",
        "main_features": ["Piscine", "Décoration unique", "Grande terrasse", "Vue panoramique"],
        "description": """
        <p><strong>Villa F5 Ste Anne - Une villa exceptionnelle au design distinctif.</strong></p>
        <p>Située dans le quartier résidentiel des Anglais à Sainte-Anne, cette magnifique villa F5 se distingue par sa façade rose caractéristique et ses espaces généreux. Parfaitement adaptée aux grands groupes, elle peut accueillir jusqu'à 10 personnes avec la possibilité de recevoir 15 invités supplémentaires.</p>
        <p><strong>Points forts de la villa :</strong><br>
        • Architecture créole modernisée avec façade rose distinctive<br>
        • Grande piscine avec vue panoramique<br>
        • Espaces de réception spacieux pour grands groupes<br>
        • Cuisine moderne entièrement équipée</p>
        """
    },
    {
        "id": "villa-f3-baccha-petit-macabou",
        "name": "Villa F3 POUR LA BACCHA",
        "location": "Petit Macabou",
        "price": 1350,
        "capacity": "6 + 9", 
        "bedrooms": 3,
        "bathrooms": 2,
        "surface": 140,
        "tagline": "Villa moderne avec terrasses panoramiques",
        "folder": "Villa_F3_Baccha_Petit_Macabou",
        "main_features": ["Piscine", "Terrasses modernes", "Vue panoramique", "Design contemporain"],
        "description": """
        <p><strong>Villa F3 POUR LA BACCHA - Modernité et élégance au cœur du Petit Macabou.</strong></p>
        <p>Cette villa contemporaine offre un cadre exceptionnel avec ses terrasses modernes et sa piscine à débordement. Conçue pour 6 personnes avec la possibilité d'accueillir 9 convives supplémentaires, elle allie confort et raffinement.</p>
        <p><strong>Caractéristiques exceptionnelles :</strong><br>
        • Terrasses panoramiques avec vue imprenable<br>
        • Piscine moderne entourée d'espaces détente<br>
        • Architecture contemporaine soignée<br>
        • Chambres modernes climatisées</p>
        """
    },
    {
        "id": "studio-cocooning-lamentin",
        "name": "Studio Cocooning Lamentin", 
        "location": "Le Lamentin",
        "price": 450,
        "capacity": "2 + 2",
        "bedrooms": 1,
        "bathrooms": 1,
        "surface": 50,
        "tagline": "Studio moderne avec jacuzzi privatif",
        "folder": "Studio_Cocooning_Lamentin",
        "main_features": ["Jacuzzi", "Terrasse privée", "Cuisine équipée", "Design moderne"],
        "description": """
        <p><strong>Studio Cocooning Lamentin - L'intimité et le confort pour deux.</strong></p>
        <p>Ce studio design au Lamentin est l'écrin parfait pour un séjour romantique ou un voyage d'affaires. Avec son jacuzzi privatif et sa terrasse, il offre tout le confort moderne dans un espace optimisé.</p>
        <p><strong>Points forts du studio :</strong><br>
        • Jacuzzi privatif sur terrasse couverte<br>
        • Cuisine ouverte entièrement équipée<br>
        • Décoration moderne et soignée<br>
        • Emplacement stratégique au Lamentin</p>
        """
    },
    {
        "id": "villa-f6-lamentin", 
        "name": "Villa F6 Lamentin",
        "location": "Le Lamentin",
        "price": 1800,
        "capacity": "12 + 20",
        "bedrooms": 6,
        "bathrooms": 4,
        "surface": 300,
        "tagline": "Grande villa avec piscine et jacuzzi pour grands groupes",
        "folder": "Villa_F6_Lamentin", 
        "main_features": ["Piscine", "Jacuzzi", "Grande capacité", "Espaces multiples"],
        "description": """
        <p><strong>Villa F6 Lamentin - La villa idéale pour les grandes réunions de famille.</strong></p>
        <p>Cette spacieuse villa F6 au Lamentin est conçue pour accueillir de grands groupes avec tout le confort nécessaire. Jusqu'à 12 personnes peuvent y séjourner avec la possibilité de recevoir 20 invités supplémentaires.</p>
        <p><strong>Équipements exceptionnels :</strong><br>
        • Piscine avec jacuzzi intégré<br>
        • 6 chambres spacieuses et climatisées<br>
        • Espaces de vie multiples pour tous<br>
        • Grande cuisine professionnelle</p>
        """
    },
    {
        "id": "villa-f5-vauclin-ravine-plate",
        "name": "Villa F5 Vauclin Ravine Plate", 
        "location": "Vauclin - Ravine Plate",
        "price": 1200,
        "capacity": "10 + 12",
        "bedrooms": 5,
        "bathrooms": 3,
        "surface": 180,
        "tagline": "Villa moderne avec piscine à débordement et vue panoramique",
        "folder": "Villa_F5_Vauclin_Ravine_Plate",
        "main_features": ["Piscine débordement", "Vue panoramique", "Design moderne", "Terrasse gazebo"],
        "description": """
        <p><strong>Villa F5 Vauclin Ravine Plate - Luxe et panorama exceptionnel.</strong></p>
        <p>Perchée sur les hauteurs de Ravine Plate au Vauclin, cette villa moderne offre une vue panoramique époustouflante. Sa piscine à débordement et ses terrasses en font un lieu d'exception pour 10 personnes.</p>
        <p><strong>Atouts majeurs :</strong><br>
        • Piscine à débordement avec vue panoramique<br>
        • Terrasse gazebo pour moments privilégiés<br>
        • Salon étage avec poutres apparentes<br>
        • Cuisine équipée haut de gamme</p>
        """
    },
    {
        "id": "villa-f6-petit-macabou",
        "name": "Villa F6 Petit Macabou",
        "location": "Petit Macabou au Vauclin", 
        "price": 1600,
        "capacity": "12 + 15",
        "bedrooms": 6,
        "bathrooms": 4,
        "surface": 250,
        "tagline": "Grande villa familiale avec vue aérienne spectaculaire",
        "folder": "Villa_F6_Petit_Macabou",
        "main_features": ["Vue aérienne", "Grande piscine", "6 chambres", "Terrasse couverte"],
        "description": """
        <p><strong>Villa F6 Petit Macabou - L'excellence pour les grands séjours familiaux.</strong></p>
        <p>Cette imposante villa F6 au Petit Macabou offre des prestations haut de gamme pour accueillir jusqu'à 12 personnes. Ses vues aériennes spectaculaires et ses équipements complets en font une destination de choix.</p>
        <p><strong>Prestations de luxe :</strong><br>
        • Vue aérienne panoramique jour et nuit<br>
        • Grande piscine avec terrasse aménagée<br>
        • 6 chambres avec climatisation individuelle<br>
        • Espaces de vie généreux et lumineux</p>
        """
    },
    {
        "id": "villa-f3-le-francois",
        "name": "Villa F3 Le François",
        "location": "Le François", 
        "price": 900,
        "capacity": "6 + 8",
        "bedrooms": 3,
        "bathrooms": 2,
        "surface": 130,
        "tagline": "Villa colorée avec vue mer et terrasse panoramique",
        "folder": "Villa_F3_Le_Francois",
        "main_features": ["Vue mer", "Terrasse panoramique", "Décoration colorée", "Piscine privée"],
        "description": """
        <p><strong>Villa F3 Le François - Couleurs tropicales et vue mer.</strong></p>
        <p>Située au François, cette villa F3 séduit par sa décoration colorée et sa vue imprenable sur la mer. Parfaite pour 6 personnes, elle offre un cadre authentiquement martiniquais avec tout le confort moderne.</p>
        <p><strong>Charme créole moderne :</strong><br>
        • Vue mer depuis la terrasse panoramique<br>
        • Décoration colorée style tropical<br>
        • Chambres climatisées aux couleurs vives<br>
        • Piscine avec salon extérieur détente</p>
        """
    },
    {
        "id": "bas-villa-f3-ste-luce",
        "name": "Bas Villa F3 Ste Luce",
        "location": "Sainte-Luce", 
        "price": 750,
        "capacity": "6 + 6",
        "bedrooms": 3,
        "bathrooms": 2,
        "surface": 110,
        "tagline": "Villa moderne avec éclairage LED et terrasse lounge",
        "folder": "Bas_Villa_F3_Ste_Luce",
        "main_features": ["Éclairage LED", "Terrasse lounge", "Design moderne", "Proche plages"],
        "description": """
        <p><strong>Bas Villa F3 Ste Luce - Modernité et confort près des plages.</strong></p>
        <p>Cette villa moderne à Sainte-Luce allie design contemporain et proximité des plus belles plages. Son système d'éclairage LED et ses espaces lounge en font un lieu tendance pour 6 personnes.</p>
        <p><strong>Style contemporain :</strong><br>
        • Éclairage LED d'ambiance dans tous les espaces<br>
        • Terrasse lounge avec mobilier design<br>
        • Salon TV avec éclairage moderne<br>
        • Proche des plages de Sainte-Luce</p>
        """
    },
    {
        "id": "villa-f3-trinite-cosmy",
        "name": "Villa F3 Trinité Cosmy",
        "location": "La Trinité - Cosmy", 
        "price": 950,
        "capacity": "6 + 8",
        "bedrooms": 3,
        "bathrooms": 2,
        "surface": 125,
        "tagline": "Villa avec piscine chauffée et vue panoramique océan",
        "folder": "Villa_F3_Trinite_Cosmy",
        "main_features": ["Piscine chauffée", "Vue océan", "Terrasse couverte", "Collines"],
        "description": """
        <p><strong>Villa F3 Trinité Cosmy - Piscine chauffée et panorama océan.</strong></p>
        <p>Nichée sur les hauteurs de Cosmy à La Trinité, cette villa offre une vue panoramique sur l'océan et les collines. Sa piscine chauffée permet de profiter des baignades toute l'année.</p>
        <p><strong>Vue exceptionnelle :</strong><br>
        • Piscine chauffée avec vue collines<br>
        • Panorama océan depuis la terrasse<br>
        • Cuisine américaine ouverte jaune et bois<br>
        • Chambres aux couleurs tropicales</p>
        """
    },
    {
        "id": "villa-f7-baie-des-mulets-vauclin",
        "name": "Villa F7 Baie des Mulets Vauclin",
        "location": "Baie des Mulets - Vauclin", 
        "price": 2000,
        "capacity": "14 + 20",
        "bedrooms": 7,
        "bathrooms": 5,
        "surface": 350,
        "tagline": "Villa exceptionnelle 7 chambres avec véranda bambou",
        "folder": "Villa_F7_Baie_des_Mulets_Vauclin",
        "main_features": ["7 chambres", "Véranda bambou", "Grande capacité", "Coin détente"],
        "description": """
        <p><strong>Villa F7 Baie des Mulets - L'excellence pour très grands groupes.</strong></p>
        <p>Cette villa F7 exceptionnelle à la Baie des Mulets est notre plus grande propriété, pouvant accueillir jusqu'à 14 personnes. Ses 7 chambres et ses espaces généreux en font le choix idéal pour les grands événements familiaux.</p>
        <p><strong>Prestations maximales :</strong><br>
        • 7 chambres spacieuses et climatisées<br>
        • Véranda bambou authentique<br>
        • Coin détente avec fauteuils suspendus<br>
        • Cuisine moderne blanche équipée pro</p>
        """
    },
    {
        "id": "villa-f6-ste-luce-plage",
        "name": "Villa F6 Ste Luce Plage",
        "location": "Sainte-Luce près plage", 
        "price": 1500,
        "capacity": "12 + 15",
        "bedrooms": 6,
        "bathrooms": 4,
        "surface": 220,
        "tagline": "Villa avec poutres apparentes proche des plages",
        "folder": "Villa_F6_Ste_Luce_Plage",
        "main_features": ["Proche plage", "Poutres apparentes", "Vue aérienne", "6 chambres"],
        "description": """
        <p><strong>Villa F6 Ste Luce Plage - Le charme créole près des plages.</strong></p>
        <p>Cette villa F6 à Sainte-Luce combine l'authenticité créole avec ses poutres apparentes et la proximité des magnifiques plages de la commune. Idéale pour 12 personnes en quête de détente balnéaire.</p>
        <p><strong>Charme créole :</strong><br>
        • Poutres apparentes traditionnelles<br>
        • Vue aérienne sur la piscine<br>
        • Proximité immédiate des plages<br>
        • 6 chambres avec caractère créole</p>
        """
    },
    {
        "id": "villa-f3-robert-pointe-hyacinthe",
        "name": "Villa F3 Robert Pointe Hyacinthe",
        "location": "Le Robert - Pointe Hyacinthe", 
        "price": 800,
        "capacity": "6 + 8",
        "bedrooms": 3,
        "bathrooms": 2,
        "surface": 115,
        "tagline": "Villa avec piscine rectangulaire et pergola kitchenette",
        "folder": "Villa_F3_Robert_Pointe_Hyacinthe",
        "main_features": ["Piscine rectangulaire", "Pergola kitchenette", "Cuisine ouverte", "TV salon"],
        "description": """
        <p><strong>Villa F3 Robert Pointe Hyacinthe - Confort moderne au Robert.</strong></p>
        <p>Située à la Pointe Hyacinthe au Robert, cette villa F3 moderne offre une piscine rectangulaire et une pergola avec kitchenette extérieure. Parfaite pour allier détente et convivialité pour 6 personnes.</p>
        <p><strong>Espaces optimisés :</strong><br>
        • Piscine rectangulaire moderne<br>
        • Pergola couverte avec kitchenette<br>
        • Cuisine ouverte sur salon TV<br>
        • Terrasse couverte pour repas extérieurs</p>
        """
    },
    {
        "id": "villa-f5-r-pilote-la-renee",
        "name": "Villa F5 R-Pilote La Renée",
        "location": "Rivière-Pilote - La Renée", 
        "price": 1150,
        "capacity": "10 + 12",
        "bedrooms": 5,
        "bathrooms": 3,
        "surface": 175,
        "tagline": "Villa avec terrasse bois et hamacs entre palmiers",
        "folder": "Villa_F5_R_Pilote_La_Renee",
        "main_features": ["Terrasse bois", "Hamacs", "Palmiers", "Salon cuir"],
        "description": """
        <p><strong>Villa F5 R-Pilote La Renée - Détente tropicale authentique.</strong></p>
        <p>Cette villa F5 à La Renée offre une ambiance tropicale unique avec sa terrasse en bois, ses hamacs suspendus entre les palmiers. Le cadre idéal pour se déconnecter avec 10 personnes maximum.</p>
        <p><strong>Ambiance tropicale :</strong><br>
        • Terrasse bois avec piscine et palmiers<br>
        • Hamacs pour sieste tropicale<br>
        • Salon cuir noir avec plafond vert<br>
        • Cuisine bois clair équipée</p>
        """
    },
    {
        "id": "villa-f3-trenelle-location-annuelle",
        "name": "Villa F3 Trenelle Location Annuelle",
        "location": "Trenelle", 
        "price": 650,
        "capacity": "6",
        "bedrooms": 3,
        "bathrooms": 2,
        "surface": 100,
        "tagline": "Villa pour location longue durée avec espaces optimisés",
        "folder": "Villa_F3_Trenelle_Location_Annuelle",
        "main_features": ["Location annuelle", "Cuisine équipée", "Salon TV", "Espaces optimisés"],
        "description": """
        <p><strong>Villa F3 Trenelle - Idéale pour séjours longue durée.</strong></p>
        <p>Cette villa F3 à Trenelle est spécialement conçue pour les locations de longue durée. Tous les équipements nécessaires au quotidien sont présents pour un confort optimal de 6 personnes.</p>
        <p><strong>Confort longue durée :</strong><br>
        • Cuisine entièrement équipée avec évier double<br>
        • Salon télévision confortable<br>
        • Espaces de rangement optimisés<br>
        • Espace détente intérieur</p>
        """
    },
    # Villas pour fêtes et journées spéciales
    {
        "id": "villa-fete-journee-fort-de-france",
        "name": "Villa Fête Journée Fort-de-France",
        "location": "Fort-de-France", 
        "price": 2500,
        "capacity": "50",
        "bedrooms": 4,
        "bathrooms": 3,
        "surface": 400,
        "tagline": "Espace événementiel avec piscine et colonnes coloniales",
        "folder": "Villa_Fete_Journee_Fort_de_France",
        "main_features": ["Événements", "Piscine panoramique", "Colonnes coloniales", "Statues Bouddha"],
        "description": """
        <p><strong>Villa Fête Journée Fort-de-France - L'excellence pour vos événements.</strong></p>
        <p>Cet espace événementiel exceptionnel à Fort-de-France peut accueillir jusqu'à 50 personnes pour vos fêtes, mariages et célébrations. Architecture coloniale et équipements modernes se conjuguent parfaitement.</p>
        <p><strong>Cadre exceptionnel :</strong><br>
        • Piscine avec vue panoramique et statues Bouddha<br>
        • Véranda à arches coloniales authentiques<br>
        • Cuisine moderne équipée pour traiteur<br>
        • Allée de palmiers d'entrée majestueuse</p>
        """
    },
    {
        "id": "villa-fete-journee-sainte-luce",
        "name": "Villa Fête Journée Sainte-Luce",
        "location": "Sainte-Luce", 
        "price": 2000,
        "capacity": "40",
        "bedrooms": 3,
        "bathrooms": 2,
        "surface": 300,
        "tagline": "Villa moderne pour événements avec tentes et animations",
        "folder": "Villa_Fete_Journee_Sainte_Luce",
        "main_features": ["Événements", "Tentes blanches", "Animation fête", "Villa contemporaine"],
        "description": """
        <p><strong>Villa Fête Journée Sainte-Luce - Modernité pour vos célébrations.</strong></p>
        <p>Cette villa contemporaine à Sainte-Luce est équipée pour accueillir 40 personnes lors de vos événements. Les tentes blanches et les aménagements permettent tous types de célébrations.</p>
        <p><strong>Équipements événementiels :</strong><br>
        • Tentes blanches avec mobilier de réception<br>
        • Décorations pour anniversaires et fêtes<br>
        • Piscine avec aménagements spéciaux<br>
        • Toilettes extérieures pour grands groupes</p>
        """
    },
    {
        "id": "villa-fete-journee-ducos",
        "name": "Villa Fête Journée Ducos",
        "location": "Ducos", 
        "price": 1800,
        "capacity": "35",
        "bedrooms": 3,
        "bathrooms": 2,
        "surface": 250,
        "tagline": "Espace fête avec bar extérieur et salon rotin",
        "folder": "Villa_Fete_Journee_Ducos",
        "main_features": ["Bar extérieur", "Gazebo", "Salon rotin", "Jouets gonflables"],
        "description": """
        <p><strong>Villa Fête Journée Ducos - Ambiance festive garantie.</strong></p>
        <p>Cette propriété à Ducos est spécialement aménagée pour les fêtes et événements familiaux. Avec son bar extérieur sous gazebo et ses multiples espaces, elle accueille 35 personnes dans une ambiance décontractée.</p>
        <p><strong>Espaces festifs :</strong><br>
        • Bar extérieur sous gazebo équipé<br>
        • Piscine avec jouets gonflables<br>
        • Salon rotin sur terrasse couverte<br>
        • Jardin avec parasols et espaces détente</p>
        """
    },
    {
        "id": "villa-fete-journee-r-pilote",
        "name": "Villa Fête Journée R-Pilote",
        "location": "Rivière-Pilote", 
        "price": 2200,
        "capacity": "45",
        "bedrooms": 4,
        "bathrooms": 3,
        "surface": 320,
        "tagline": "Villa créole pour événements avec piscine tropicale",
        "folder": "Villa_Fete_Journee_R_Pilote",
        "main_features": ["Style créole", "Piscine tropicale", "Terrasse pierre", "Cuisine moderne"],
        "description": """
        <p><strong>Villa Fête Journée R-Pilote - Authenticité créole pour vos événements.</strong></p>
        <p>Cette magnifique villa créole à Rivière-Pilote combine authenticité et modernité pour accueillir 45 personnes. Sa piscine tropicale et ses terrasses en pierre naturelle créent une ambiance unique.</p>
        <p><strong>Charme créole événementiel :</strong><br>
        • Piscine tropicale avec vue panoramique<br>
        • Terrasse en pierre naturelle<br>
        • Villa créole authentique rénovée<br>
        • Cuisine moderne équipée pour traiteur</p>
        """
    },
    {
        "id": "villa-fete-journee-riviere-salee",
        "name": "Villa Fête Journée Rivière-Salée",
        "location": "Rivière-Salée", 
        "price": 1500,
        "capacity": "30",
        "bedrooms": 2,
        "bathrooms": 2,
        "surface": 200,
        "tagline": "Espace événementiel avec piscine et tente couverte",
        "folder": "Villa_Fete_Journee_Riviere_Salee",
        "main_features": ["Piscine", "Tente couverte", "Forfaits événements", "Espace modulable"],
        "description": """
        <p><strong>Villa Fête Journée Rivière-Salée - Solutions événementielles flexibles.</strong></p>
        <p>Cet espace à Rivière-Salée propose des solutions modulables pour vos événements de 30 personnes. La tente couverte et les forfaits sur mesure s'adaptent à tous vos besoins festifs.</p>
        <p><strong>Formules événementielles :</strong><br>
        • Piscine avec tente de réception couverte<br>
        • Forfaits personnalisables selon événement<br>
        • Aménagements modulables<br>
        • Tarifs attractifs pour associations</p>
        """
    },
    {
        "id": "espace-piscine-journee-bungalow",
        "name": "Espace Piscine Journée Bungalow",
        "location": "Emplacement privilégié", 
        "price": 800,
        "capacity": "15",
        "bedrooms": 1,
        "bathrooms": 1,
        "surface": 80,
        "tagline": "Bungalow créole avec véranda et studio kitchenette",
        "folder": "Espace_Piscine_Journee_Bungalow",
        "main_features": ["Bungalow créole", "Véranda", "Studio kitchenette", "Piscine journée"],
        "description": """
        <p><strong>Espace Piscine Journée Bungalow - Charme créole authentique.</strong></p>
        <p>Ce charmant bungalow créole avec sa véranda traditionnelle offre un cadre authentique pour 15 personnes. Le studio avec kitchenette et l'accès piscine en font un lieu idéal pour une journée tropicale.</p>
        <p><strong>Authenticité créole :</strong><br>
        • Bungalow extérieur avec véranda créole<br>
        • Studio intérieur avec kitchenette équipée<br>
        • Accès piscine pour la journée<br>
        • Architecture traditionnelle martiniquaise</p>
        """
    }
]

def create_villa_detail_page(villa):
    """Crée une page détail complète pour une villa"""
    
    # Template HTML de base
    html_template = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- SEO Optimisé -->
    <title>{name} - {location} | KhanelConcept Villas Luxe Martinique</title>
    <meta name="description" content="{name} à {location} - Villa de luxe {capacity} avec {main_features_text}. Prix à partir de {price}€/nuit. Réservation en ligne sécurisée.">
    <meta name="keywords" content="villa martinique, {location}, location villa luxe, {name}, vacances martinique, {keywords}">
    <meta name="author" content="KhanelConcept">
    
    <!-- OpenGraph pour partage social -->
    <meta property="og:title" content="{name} - Villa de luxe en Martinique">
    <meta property="og:description" content="{tagline}">
    <meta property="og:image" content="./images/{folder}/{main_image}">
    <meta property="og:type" content="website">
    
    <!-- CSS Libraries -->
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/swiper@8/swiper-bundle.min.css" rel="stylesheet">
    
    <!-- Custom CSS -->
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
    
        :root {{
            --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            --glass-bg: rgba(255, 255, 255, 0.1);
            --glass-border: rgba(255, 255, 255, 0.2);
            --text-primary: #2d3748;
            --text-secondary: #718096;
            --accent-gold: #f6ad55;
            --shadow-soft: 0 10px 25px rgba(0, 0, 0, 0.1);
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            position: relative;
            overflow-x: hidden;
            line-height: 1.6;
            color: var(--text-primary);
        }}
        
        /* Video Background identique à l'index */
        .video-background {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -2;
            overflow: hidden;
        }}
        
        .video-background video {{
            position: absolute;
            top: 50%;
            left: 50%;
            min-width: 100%;
            min-height: 100%;
            width: auto;
            height: auto;
            transform: translate(-50%, -50%);
            object-fit: cover;
            filter: brightness(0.7) contrast(1.1) saturate(1.2);
        }}
        
        .video-overlay {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.3);
            z-index: -1;
        }}
        
        .villa-header {{
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%);
            position: relative;
            overflow: hidden;
        }}
        
        .glass-overlay {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: var(--shadow-soft);
        }}
        
        .breadcrumb {{
            background: rgba(255, 255, 255, 0.03);
            padding: 15px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }}
        
        .gallery-container {{
            position: relative;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: var(--shadow-soft);
        }}
        
        .swiper-slide img {{
            width: 100%;
            height: 400px;
            object-fit: cover;
            border-radius: 15px;
            cursor: pointer;
        }}
        
        .gallery-thumbnails img {{
            width: 80px;
            height: 60px;
            object-fit: cover;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }}
        
        .gallery-thumbnails img:hover,
        .gallery-thumbnails img.active {{
            border-color: var(--accent-gold);
            transform: scale(1.05);
        }}
        
        .info-card {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: var(--shadow-soft);
            transition: transform 0.3s ease;
        }}
        
        .info-card:hover {{
            transform: translateY(-5px);
        }}
        
        .star-rating {{
            color: var(--accent-gold);
            font-size: 1.2rem;
        }}
        
        .price-display {{
            background: var(--secondary-gradient);
            color: white;
            padding: 15px 25px;
            border-radius: 50px;
            font-weight: bold;
            font-size: 1.5rem;
        }}
        
        .amenity-item {{
            display: flex;
            align-items: center;
            padding: 10px;
            background: rgba(102, 126, 234, 0.1);
            border-radius: 10px;
            margin-bottom: 10px;
            transition: all 0.3s ease;
        }}
        
        .amenity-item:hover {{
            background: rgba(102, 126, 234, 0.2);
            transform: translateX(5px);
        }}
        
        .btn-primary {{
            background: var(--primary-gradient);
            color: white;
            padding: 15px 30px;
            border-radius: 50px;
            border: none;
            font-weight: 600;
            transition: all 0.3s ease;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }}
        
        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        }}
        
        .btn-secondary {{
            background: white;
            color: var(--text-primary);
            border: 2px solid var(--accent-gold);
            padding: 12px 25px;
            border-radius: 50px;
            font-weight: 600;
            transition: all 0.3s ease;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }}
        
        .btn-secondary:hover {{
            background: var(--accent-gold);
            color: white;
        }}
        
        .modal-gallery {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.9);
            z-index: 9999;
            justify-content: center;
            align-items: center;
        }}
        
        .modal-gallery.active {{
            display: flex;
        }}
        
        .modal-content {{
            position: relative;
            max-width: 90%;
            max-height: 90%;
        }}
        
        .modal-content img {{
            width: 100%;
            height: auto;
            border-radius: 10px;
        }}
        
        .social-share {{
            display: flex;
            gap: 15px;
            margin-top: 20px;
        }}
        
        .social-btn {{
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            text-decoration: none;
            transition: transform 0.3s ease;
        }}
        
        .social-btn:hover {{
            transform: translateY(-3px);
        }}
        
        .social-btn.facebook {{ background: #4267B2; }}
        .social-btn.instagram {{ background: linear-gradient(45deg, #405DE6, #5851DB, #833AB4, #C13584, #E1306C, #FD1D1D); }}
        .social-btn.whatsapp {{ background: #25D366; }}
        
        @media (max-width: 768px) {{
            .swiper-slide img {{
                height: 250px;
            }}
            
            .price-display {{
                font-size: 1.2rem;
                padding: 12px 20px;
            }}
            
            .info-card {{
                padding: 20px;
            }}
        }}
    </style>
</head>

<body>
    <!-- Background Video Cloudinary avec support iOS -->
    <div class="video-background">
        <video id="backgroundVideo" autoplay muted loop playsinline preload="metadata" webkit-playsinline>
            <source src="https://res.cloudinary.com/ddulasmtz/video/upload/v1752950782/background-video.mp4_qoofsz.mp4" type="video/mp4">
            Votre navigateur ne supporte pas la lecture de vidéos HTML5.
        </video>
        <div class="video-overlay"></div>
    </div>
    
    <!-- Navigation & Breadcrumb -->
    <nav class="villa-header">
        <div class="breadcrumb">
            <div class="container mx-auto px-6">
                <div class="flex items-center text-white text-sm">
                    <a href="index.html" class="hover:text-yellow-300 transition-colors">
                        <i class="fas fa-home mr-2"></i>Accueil
                    </a>
                    <i class="fas fa-chevron-right mx-3"></i>
                    <a href="index.html#villas" class="hover:text-yellow-300 transition-colors">Villas</a>
                    <i class="fas fa-chevron-right mx-3"></i>
                    <span class="text-yellow-300">{name}</span>
                </div>
            </div>
        </div>
        
        <!-- Villa Header Info -->
        <div class="container mx-auto px-6 py-16">
            <div class="glass-overlay p-8">
                <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center">
                    <div class="flex-1">
                        <h1 class="text-4xl lg:text-5xl font-bold text-white mb-4">{name}</h1>
                        <div class="flex items-center mb-4">
                            <div class="star-rating mr-4">
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                                <i class="fas fa-star"></i>
                                <span class="text-white ml-2">(5.0)</span>
                            </div>
                            <div class="text-white">
                                <i class="fas fa-map-marker-alt mr-2"></i>{location}
                            </div>
                        </div>
                        <p class="text-white text-lg opacity-90">{tagline}</p>
                    </div>
                    <div class="mt-6 lg:mt-0">
                        <div class="price-display">
                            À partir de {price}€<span class="text-sm font-normal">/nuit</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="container mx-auto px-6 py-12">
        
        <!-- Gallery Section -->
        <section class="mb-16" data-aos="fade-up">
            <div class="gallery-container">
                <!-- Main Swiper Gallery -->
                <div class="swiper villa-gallery mb-6">
                    <div class="swiper-wrapper">
                        {gallery_slides}
                    </div>
                    <div class="swiper-pagination"></div>
                    <div class="swiper-button-next"></div>
                    <div class="swiper-button-prev"></div>
                </div>
                
                <!-- Thumbnails -->
                <div class="gallery-thumbnails flex gap-3 overflow-x-auto p-4 bg-gray-100 rounded-b-xl">
                    {gallery_thumbnails}
                </div>
            </div>
        </section>

        <!-- Quick Info Cards -->
        <section class="mb-16" data-aos="fade-up" data-aos-delay="200">
            <div class="grid grid-cols-2 lg:grid-cols-4 gap-6">
                <div class="info-card text-center">
                    <div class="text-3xl text-blue-600 mb-3"><i class="fas fa-users"></i></div>
                    <div class="text-lg font-semibold">{capacity}</div>
                    <div class="text-sm text-gray-600">Voyageurs</div>
                </div>
                <div class="info-card text-center">
                    <div class="text-3xl text-green-600 mb-3"><i class="fas fa-bed"></i></div>
                    <div class="text-lg font-semibold">{bedrooms}</div>
                    <div class="text-sm text-gray-600">Chambres</div>
                </div>
                <div class="info-card text-center">
                    <div class="text-3xl text-purple-600 mb-3"><i class="fas fa-bath"></i></div>
                    <div class="text-lg font-semibold">{bathrooms}</div>
                    <div class="text-sm text-gray-600">Salles de bain</div>
                </div>
                <div class="info-card text-center">
                    <div class="text-3xl text-orange-600 mb-3"><i class="fas fa-expand-arrows-alt"></i></div>
                    <div class="text-lg font-semibold">{surface}m²</div>
                    <div class="text-sm text-gray-600">Surface</div>
                </div>
            </div>
        </section>

        <!-- Description & Amenities -->
        <div class="grid lg:grid-cols-3 gap-12 mb-16">
            <!-- Description -->
            <div class="lg:col-span-2" data-aos="fade-up" data-aos-delay="300">
                <div class="info-card">
                    <h2 class="text-3xl font-bold mb-6 flex items-center">
                        <i class="fas fa-info-circle text-blue-600 mr-3"></i>
                        Description de la villa
                    </h2>
                    <div class="prose prose-lg max-w-none">
                        {description}
                    </div>
                    
                    <!-- Action Buttons -->
                    <div class="mt-8 flex flex-wrap gap-4">
                        <button class="btn-primary" onclick="openReservationModal()">
                            <i class="fas fa-calendar-check"></i>
                            Réserver maintenant
                        </button>
                        <button class="btn-secondary" onclick="addToFavorites()">
                            <i class="fas fa-heart"></i>
                            Ajouter aux favoris
                        </button>
                        <button class="btn-secondary" onclick="window.print()">
                            <i class="fas fa-print"></i>
                            Imprimer
                        </button>
                    </div>
                    
                    <!-- Social Share -->
                    <div class="social-share">
                        <a href="#" class="social-btn facebook" onclick="shareOnFacebook()" title="Partager sur Facebook">
                            <i class="fab fa-facebook-f"></i>
                        </a>
                        <a href="#" class="social-btn instagram" onclick="shareOnInstagram()" title="Partager sur Instagram">
                            <i class="fab fa-instagram"></i>
                        </a>
                        <a href="#" class="social-btn whatsapp" onclick="shareOnWhatsApp()" title="Partager sur WhatsApp">
                            <i class="fab fa-whatsapp"></i>
                        </a>
                    </div>
                </div>
            </div>
            
            <!-- Quick Amenities -->
            <div data-aos="fade-up" data-aos-delay="400">
                <div class="info-card">
                    <h3 class="text-2xl font-bold mb-6 flex items-center">
                        <i class="fas fa-star text-yellow-500 mr-3"></i>
                        Équipements principaux
                    </h3>
                    <div class="space-y-3">
                        {main_amenities_html}
                    </div>
                </div>
            </div>
        </div>

        <!-- Location -->
        <section class="mb-16" data-aos="fade-up" data-aos-delay="600">
            <div class="grid lg:grid-cols-2 gap-12">
                <div class="info-card">
                    <h2 class="text-3xl font-bold mb-6 flex items-center">
                        <i class="fas fa-map-marker-alt text-red-600 mr-3"></i>
                        Localisation
                    </h2>
                    
                    <div class="mb-6">
                        <h4 class="font-semibold text-lg mb-2">Adresse</h4>
                        <p class="text-gray-600 mb-4">{location}, Martinique</p>
                        
                        <h4 class="font-semibold text-lg mb-2">Points d'intérêt à proximité</h4>
                        <div class="space-y-2">
                            <div class="flex items-center"><i class="fas fa-umbrella-beach text-blue-500 mr-2"></i> Plages les plus proches - 2-5 km</div>
                            <div class="flex items-center"><i class="fas fa-store text-green-500 mr-2"></i> Commerces et supermarchés - 1-3 km</div>
                            <div class="flex items-center"><i class="fas fa-utensils text-orange-500 mr-2"></i> Restaurants locaux - 1-2 km</div>
                            <div class="flex items-center"><i class="fas fa-gas-pump text-red-500 mr-2"></i> Stations service - 2-3 km</div>
                        </div>
                        
                        <h4 class="font-semibold text-lg mt-6 mb-2">Temps de trajet</h4>
                        <div class="space-y-2">
                            <div class="flex items-center"><i class="fas fa-plane text-blue-500 mr-2"></i> Aéroport Martinique - 30-50 min</div>
                            <div class="flex items-center"><i class="fas fa-city text-gray-500 mr-2"></i> Fort-de-France - 35-60 min</div>
                            <div class="flex items-center"><i class="fas fa-mountain text-green-500 mr-2"></i> Montagne Pelée - 1h-1h30</div>
                        </div>
                    </div>
                </div>
                
                <div class="info-card">
                    <h3 class="text-2xl font-bold mb-6">Carte de localisation</h3>
                    <div class="bg-gray-100 rounded-15 h-96 flex items-center justify-center">
                        <div class="text-center text-gray-500">
                            <i class="fas fa-map text-6xl mb-4"></i>
                            <p class="text-lg font-semibold">{name}</p>
                            <p>{location}, Martinique</p>
                            <p class="text-sm mt-2">Carte interactive disponible lors de la réservation</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <!-- Back to Top -->
    <button id="backToTop" class="fixed bottom-6 right-6 bg-blue-600 text-white w-12 h-12 rounded-full shadow-lg opacity-0 transition-all duration-300 hover:bg-blue-700" style="display: none;">
        <i class="fas fa-chevron-up"></i>
    </button>

    <!-- Modal Gallery -->
    <div id="modalGallery" class="modal-gallery">
        <div class="modal-content">
            <img id="modalImage" src="" alt="Villa Image">
            <button class="absolute top-4 right-4 text-white text-3xl bg-black bg-opacity-50 rounded-full w-12 h-12 flex items-center justify-center" onclick="closeModal()">
                <i class="fas fa-times"></i>
            </button>
            <button class="absolute left-4 top-1/2 transform -translate-y-1/2 text-white text-2xl bg-black bg-opacity-50 rounded-full w-10 h-10 flex items-center justify-center" onclick="prevImage()">
                <i class="fas fa-chevron-left"></i>
            </button>
            <button class="absolute right-4 top-1/2 transform -translate-y-1/2 text-white text-2xl bg-black bg-opacity-50 rounded-full w-10 h-10 flex items-center justify-center" onclick="nextImage()">
                <i class="fas fa-chevron-right"></i>
            </button>
        </div>
    </div>

    <!-- Scripts -->
    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/swiper@8/swiper-bundle.min.js"></script>
    
    <script>
        // Initialize AOS Animation
        AOS.init({{
            duration: 1000,
            once: true
        }});

        // Gallery images array
        const galleryImages = {gallery_images_js};

        let currentImageIndex = 0;

        // Initialize Swiper Gallery
        const villaSwiper = new Swiper('.villa-gallery', {{
            loop: true,
            pagination: {{
                el: '.swiper-pagination',
                clickable: true,
            }},
            navigation: {{
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            }},
            autoplay: {{
                delay: 5000,
                disableOnInteraction: false,
            }},
            effect: 'fade',
            fadeEffect: {{
                crossFade: true
            }},
        }});

        // Thumbnail Gallery
        function initThumbnails() {{
            const thumbnails = document.querySelectorAll('.gallery-thumbnails img');
            thumbnails.forEach((thumb, index) => {{
                thumb.addEventListener('click', () => {{
                    villaSwiper.slideToLoop(index);
                    updateActiveThumbnail(index);
                }});
            }});
        }}

        function updateActiveThumbnail(activeIndex) {{
            const thumbnails = document.querySelectorAll('.gallery-thumbnails img');
            thumbnails.forEach((thumb, index) => {{
                thumb.classList.toggle('active', index === activeIndex);
            }});
        }}

        // Modal Gallery Functions
        function openModal(imageSrc, imageIndex = 0) {{
            const modal = document.getElementById('modalGallery');
            const modalImage = document.getElementById('modalImage');
            modalImage.src = imageSrc;
            modal.classList.add('active');
            currentImageIndex = imageIndex;
            document.body.style.overflow = 'hidden';
        }}

        function closeModal() {{
            const modal = document.getElementById('modalGallery');
            modal.classList.remove('active');
            document.body.style.overflow = 'auto';
        }}

        function nextImage() {{
            currentImageIndex = (currentImageIndex + 1) % galleryImages.length;
            document.getElementById('modalImage').src = galleryImages[currentImageIndex];
        }}

        function prevImage() {{
            currentImageIndex = currentImageIndex === 0 ? galleryImages.length - 1 : currentImageIndex - 1;
            document.getElementById('modalImage').src = galleryImages[currentImageIndex];
        }}

        // Initialize Modal Gallery
        function initModalGallery() {{
            const galleryImageElements = document.querySelectorAll('.swiper-slide img, .gallery-thumbnails img');
            galleryImageElements.forEach((img, index) => {{
                img.addEventListener('click', () => {{
                    const actualIndex = index >= galleryImages.length ? index - galleryImages.length : index;
                    openModal(img.src, actualIndex);
                }});
            }});
        }}

        // Social Share Functions
        function shareOnFacebook() {{
            const url = encodeURIComponent(window.location.href);
            const title = encodeURIComponent('{name} - KhanelConcept');
            window.open(`https://www.facebook.com/sharer/sharer.php?u=${{url}}&title=${{title}}`, '_blank', 'width=600,height=400');
        }}

        function shareOnInstagram() {{
            navigator.clipboard.writeText(window.location.href).then(() => {{
                alert('Lien copié ! Collez-le dans votre post Instagram.');
            }});
        }}

        function shareOnWhatsApp() {{
            const text = encodeURIComponent(`Découvrez {name} ! ${{window.location.href}}`);
            window.open(`https://wa.me/?text=${{text}}`, '_blank');
        }}

        // Reservation
        function openReservationModal() {{
            const villaName = '{name}';
            window.location.href = `reservation.html?villa=${{encodeURIComponent(villaName)}}&price={price}`;
        }}

        // Add to Favorites
        function addToFavorites() {{
            const villaData = {{
                name: '{name}',
                location: '{location}',
                price: '{price}',
                image: './images/{folder}/{main_image}',
                url: window.location.href
            }};
            
            let favorites = JSON.parse(localStorage.getItem('villa_favorites') || '[]');
            
            const exists = favorites.some(fav => fav.name === villaData.name);
            
            if (exists) {{
                alert('Cette villa est déjà dans vos favoris !');
            }} else {{
                favorites.push(villaData);
                localStorage.setItem('villa_favorites', JSON.stringify(favorites));
                alert('Villa ajoutée à vos favoris !');
            }}
        }}

        // Back to Top Button
        function initBackToTop() {{
            const backToTop = document.getElementById('backToTop');
            
            window.addEventListener('scroll', () => {{
                if (window.scrollY > 500) {{
                    backToTop.style.display = 'block';
                    backToTop.style.opacity = '1';
                }} else {{
                    backToTop.style.opacity = '0';
                    setTimeout(() => {{
                        if (backToTop.style.opacity === '0') {{
                            backToTop.style.display = 'none';
                        }}
                    }}, 300);
                }}
            }});
            
            backToTop.addEventListener('click', () => {{
                window.scrollTo({{ top: 0, behavior: 'smooth' }});
            }});
        }}

        // Keyboard Navigation
        document.addEventListener('keydown', (e) => {{
            const modal = document.getElementById('modalGallery');
            if (modal.classList.contains('active')) {{
                if (e.key === 'Escape') {{
                    closeModal();
                }} else if (e.key === 'ArrowLeft') {{
                    prevImage();
                }} else if (e.key === 'ArrowRight') {{
                    nextImage();
                }}
            }}
        }});

        // Correction vidéo background pour iOS
        function initBackgroundVideoiOS() {{
            const video = document.getElementById('backgroundVideo');
            if (video) {{
                // Détecter iOS
                const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
                
                if (isIOS) {{
                    console.log('iOS détecté - Initialisation vidéo background villa');
                    
                    // Forcer les attributs iOS
                    video.setAttribute('webkit-playsinline', '');
                    video.setAttribute('playsinline', '');
                    video.muted = true;
                    video.defaultMuted = true;
                    video.volume = 0;
                    
                    // Essayer de démarrer immédiatement
                    video.play().catch(error => {{
                        console.log('Autoplay bloqué - Attente interaction utilisateur');
                        
                        // Démarrer au premier touch/click
                        function startVideo() {{
                            video.play().then(() => {{
                                console.log('✅ Vidéo background villa démarrée sur iOS');
                                document.removeEventListener('touchstart', startVideo);
                                document.removeEventListener('click', startVideo);
                            }}).catch(err => console.log('Erreur vidéo iOS:', err));
                        }}
                        
                        document.addEventListener('touchstart', startVideo, {{ once: true }});
                        document.addEventListener('click', startVideo, {{ once: true }});
                    }});
                }} else {{
                    // Non-iOS : démarrage normal
                    video.play().catch(error => {{
                        console.log('Erreur autoplay:', error);
                    }});
                }}
            }}
        }}

        // Initialize all functions
        document.addEventListener('DOMContentLoaded', () => {{
            initThumbnails();
            initModalGallery();
            initBackToTop();
            initBackgroundVideoiOS();
            
            console.log('{name} - Page détail chargée avec succès');
        }});
    </script>
</body>
</html>"""

    # Découvrir automatiquement les images de la villa
    image_files = []
    discovered_images = discover_villa_images(villa['folder'])
    
    if discovered_images:
        # Extraire juste les noms de fichiers des chemins complets
        for img_path in discovered_images:
            img_filename = img_path.split('/')[-1]  # Récupère juste le nom de fichier
            image_files.append(img_filename)
    
    # Si aucune image trouvée, utiliser la méthode de fallback
    if not image_files:
        image_folder = Path(f"/app/images/{villa['folder']}")
        if image_folder.exists():
            for img_file in image_folder.glob("*.jpg"):
                if "information" not in img_file.name.lower() and "tarif" not in img_file.name.lower():
                    image_files.append(img_file.name)
    
    # Trier les images par numéro si possible
    image_files.sort()
    
    # Générer les slides de la galerie
    gallery_slides = ""
    for img_file in image_files[:10]:  # Maximum 10 images par galerie
        gallery_slides += f"""
                        <div class="swiper-slide">
                            <img src="./images/{villa['folder']}/{img_file}" alt="{villa['name']} - {img_file}" loading="lazy">
                        </div>"""
    
    # Générer les thumbnails
    gallery_thumbnails = ""
    for i, img_file in enumerate(image_files[:10]):
        active_class = "active" if i == 0 else ""
        gallery_thumbnails += f"""
                    <img src="./images/{villa['folder']}/{img_file}" alt="Thumbnail {i+1}" class="{active_class}">"""
    
    # Générer les équipements principaux HTML
    main_amenities_html = ""
    icons = ["fas fa-swimming-pool", "fas fa-hot-tub", "fas fa-spa", "fas fa-snowflake", "fas fa-wifi", "fas fa-utensils", "fas fa-car", "fas fa-leaf"]
    colors = ["text-cyan-500", "text-red-500", "text-blue-500", "text-blue-400", "text-purple-500", "text-orange-500", "text-gray-600", "text-green-500"]
    
    for i, feature in enumerate(villa['main_features'][:8]):
        icon = icons[i] if i < len(icons) else "fas fa-star"
        color = colors[i] if i < len(colors) else "text-blue-500"
        main_amenities_html += f"""
                        <div class="amenity-item">
                            <i class="{icon} {color} mr-3"></i>
                            <span>{feature}</span>
                        </div>"""
    
    # Préparer les données pour le template
    main_image = image_files[0] if image_files else "default.jpg"
    main_features_text = ", ".join(villa['main_features'][:3])
    keywords = ", ".join(villa['main_features']).lower()
    
    # Images JavaScript array
    gallery_images_js = json.dumps([f"./images/{villa['folder']}/{img}" for img in image_files])
    
    # Remplir le template
    html_content = html_template.format(
        name=villa['name'],
        location=villa['location'],
        price=villa['price'],
        capacity=villa['capacity'],
        bedrooms=villa['bedrooms'],
        bathrooms=villa['bathrooms'],
        surface=villa['surface'],
        tagline=villa['tagline'],
        folder=villa['folder'],
        main_image=main_image,
        main_features_text=main_features_text,
        keywords=keywords,
        description=villa['description'],
        gallery_slides=gallery_slides,
        gallery_thumbnails=gallery_thumbnails,
        main_amenities_html=main_amenities_html,
        gallery_images_js=gallery_images_js
    )
    
    return html_content

def main():
    """Génère toutes les pages détails des villas"""
    print("🏗️ Génération des 21 pages détails KhanelConcept...")
    
    pages_created = 0
    
    for villa in villas_data:
        try:
            # Générer le contenu HTML
            html_content = create_villa_detail_page(villa)
            
            # Créer le fichier
            filename = f"/app/{villa['id']}.html"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            pages_created += 1
            print(f"✅ {villa['name']} - {filename}")
            
        except Exception as e:
            print(f"❌ Erreur pour {villa['name']}: {e}")
    
    print(f"\n🎉 Génération terminée : {pages_created}/{len(villas_data)} pages créées avec succès !")
    
    # Créer un fichier index des villas
    create_villa_index()

def create_villa_index():
    """Crée un fichier index listant toutes les villas"""
    index_content = "# INDEX DES PAGES DÉTAILS VILLAS\n\n"
    
    for villa in villas_data:
        index_content += f"- **{villa['name']}** ({villa['location']}) - {villa['price']}€/nuit\n"
        index_content += f"  - URL: `{villa['id']}.html`\n"
        index_content += f"  - Capacité: {villa['capacity']} - {villa['bedrooms']} chambres\n"
        index_content += f"  - Tagline: {villa['tagline']}\n\n"
    
    with open("/app/VILLA_PAGES_INDEX.md", 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print("📋 Index des villas créé : VILLA_PAGES_INDEX.md")

if __name__ == "__main__":
    main()