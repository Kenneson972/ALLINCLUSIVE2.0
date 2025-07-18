// Base de données complète des villas KhanelConcept
const VILLAS_DATABASE = {
    "villas": [
        {
            "id": 1,
            "nom": "Villa F3 Petit Macabou",
            "prix_base": 850,
            "prix_affiche": "850€",
            "localisation": "Petit Macabou au Vauclin",
            "capacite": 6,
            "capacite_detail": "6 personnes + 9 invités",
            "type_logement": "2 chambres climatisées, salon avec canapé-lit",
            "equipements": "Sauna, Jacuzzi, 2 douches extérieures",
            "proximite_plage": "Non spécifié",
            "horaires": "09h-20h",
            "prix_periode": "Weekend: 850€ + 100€/nuit suppl. | Semaine: 1550€",
            "disponibilites": "28/07-03/08, 11/08-14/08, 29/08-31/08",
            "caution": "1500€ par chèque",
            "conditions": "Pas de nuisance sonore, respect voisinage",
            "categorie": "sejour",
            "photos": [
                "/assets/images/villa_f3_petit_macabou/01_piscine_principale.jpg",
                "/assets/images/villa_f3_petit_macabou/02_salle_de_bain.jpg",
                "/assets/images/villa_f3_petit_macabou/03_cuisine.jpg",
                "/assets/images/villa_f3_petit_macabou/04_sauna.jpg",
                "/assets/images/villa_f3_petit_macabou/05_douche_exterieure.jpg",
                "/assets/images/villa_f3_petit_macabou/06_chambre1.jpg",
                "/assets/images/villa_f3_petit_macabou/07_chambre2.jpg",
                "/assets/images/villa_f3_petit_macabou/08_salon.jpg",
                "/assets/images/villa_f3_petit_macabou/09_terrasse.jpg"
            ]
        },
        {
            "id": 2,
            "nom": "Villa F5 Ste Anne",
            "prix_base": 1300,
            "prix_affiche": "1300€",
            "localisation": "Quartier Les Anglais, Ste Anne",
            "capacite": 10,
            "capacite_detail": "10 personnes + 15 invités",
            "type_logement": "4 chambres, 4 salles d'eau",
            "equipements": "Piscine, décoration rose distinctive, terrasses couvertes",
            "proximite_plage": "Non spécifié",
            "horaires": "09h-19h",
            "prix_periode": "Weekend: 1350€ (hors vacances) | Semaine: 2251€",
            "disponibilites": "02/07-20/07, puis à partir du 21/08",
            "caution": "500€ espèces + 1500€ empreinte",
            "conditions": "Paiement plusieurs fois, cautions rendues si OK",
            "categorie": "sejour",
            "photos": [
                "/assets/images/villa_f5_ste_anne/01_piscine_principale.jpg",
                "/assets/images/villa_f5_ste_anne/02_piscine_vue_aerienne.jpg",
                "/assets/images/villa_f5_ste_anne/03_facade_villa_rose.jpg",
                "/assets/images/villa_f5_ste_anne/04_cuisine_moderne.jpg",
                "/assets/images/villa_f5_ste_anne/05_salon_principal.jpg",
                "/assets/images/villa_f5_ste_anne/06_chambre_principale.jpg",
                "/assets/images/villa_f5_ste_anne/07_chambre_enfants.jpg",
                "/assets/images/villa_f5_ste_anne/08_terrasse_couverte.jpg",
                "/assets/images/villa_f5_ste_anne/09_terrasse_vue_jardin.jpg",
                "/assets/images/villa_f5_ste_anne/10_informations_catalogue.jpg"
            ]
        },
        {
            "id": 3,
            "nom": "Villa F3 POUR LA BACCHA",
            "prix_base": 1350,
            "prix_affiche": "1350€",
            "localisation": "Petit Macabou",
            "capacite": 6,
            "capacite_detail": "6 personnes + 9 convives",
            "type_logement": "2 chambres climatisées, canapé-lit salon climatisé",
            "equipements": "Piscine, terrasses modernes, finitions contemporaines",
            "proximite_plage": "Non spécifié",
            "horaires": "09h-18h",
            "prix_periode": "Juillet complet: 1350€ | Périodes août disponibles: 1350€",
            "disponibilites": "Juillet complet, périodes août disponibles",
            "caution": "1500€ par chèque",
            "conditions": "Consignes à respecter, PAS DE NUISANCE SONORE",
            "categorie": "sejour",
            "photos": [
                "/assets/images/villa_f3_baccha/01_terrasse_piscine.jpg",
                "/assets/images/villa_f3_baccha/02_chambre1.jpg",
                "/assets/images/villa_f3_baccha/03_chambre2.jpg",
                "/assets/images/villa_f3_baccha/04_cuisine.jpg",
                "/assets/images/villa_f3_baccha/05_salle_de_bain.jpg",
                "/assets/images/villa_f3_baccha/06_salon.jpg",
                "/assets/images/villa_f3_baccha/07_terrasse.jpg",
                "/assets/images/villa_f3_baccha/08_piscine.jpg"
            ]
        },
        {
            "id": 4,
            "nom": "Villa Fête Ducos",
            "prix_base": 375,
            "prix_affiche": "375€",
            "localisation": "Ducos",
            "capacite": 30,
            "capacite_detail": "5 à 30 personnes selon formule",
            "type_logement": "Villa avec espaces de réception extérieurs",
            "equipements": "Piscine, bar extérieur, terrasse couverte, salon rotin, gazebo",
            "proximite_plage": "Non spécifié",
            "horaires": "Formule 1: 10h-20h | Formule 2: 13h-18h",
            "prix_periode": "Formule 1: 375€-510€ | Formule 2: 260€-375€",
            "disponibilites": "Sur demande",
            "caution": "Non spécifié",
            "conditions": "Enfants comptés à partir de 6 ans, 12 places parking",
            "categorie": "fete",
            "photos": [
                "/assets/images/villa_fete_ducos/01_piscine_avec_jouets.jpg",
                "/assets/images/villa_fete_ducos/02_terrasse_salon.jpg",
                "/assets/images/villa_fete_ducos/03_bar_exterieur.jpg",
                "/assets/images/villa_fete_ducos/04_mobilier.jpg",
                "/assets/images/villa_fete_ducos/05_jardin.jpg",
                "/assets/images/villa_fete_ducos/06_decoration.jpg",
                "/assets/images/villa_fete_ducos/07_gazebo.jpg",
                "/assets/images/villa_fete_ducos/08_terrasse_couverte.jpg",
                "/assets/images/villa_fete_ducos/09_salon_rotin.jpg",
                "/assets/images/villa_fete_ducos/10_vue_ensemble.jpg"
            ]
        },
        {
            "id": 5,
            "nom": "Studio Cocooning Lamentin",
            "prix_base": 290,
            "prix_affiche": "290€",
            "localisation": "Morne Pitault, Lamentin",
            "capacite": 2,
            "capacite_detail": "2 personnes (couple)",
            "type_logement": "Studio avec bac à punch privé (petite piscine)",
            "equipements": "Cuisine moderne équipée, jacuzzi/bac à punch, vue panoramique",
            "proximite_plage": "Hauteurs de Morne Pitault",
            "horaires": "Arrivée 16h, Départ 11h",
            "prix_periode": "À partir de 290€, tarif variable selon date",
            "disponibilites": "Location UNIQUEMENT à la SEMAINE en période vacances",
            "caution": "Non spécifiée",
            "conditions": "Pas d'invités, paiement en plusieurs fois possible",
            "categorie": "special",
            "photos": [
                "/assets/images/studio_cocooning/01_studio_vue_ensemble.jpg",
                "/assets/images/studio_cocooning/02_cuisine_moderne.jpg",
                "/assets/images/studio_cocooning/03_terrasse_jacuzzi.jpg",
                "/assets/images/studio_cocooning/04_cuisine_ouverte.jpg",
                "/assets/images/studio_cocooning/05_chambre_salon.jpg",
                "/assets/images/studio_cocooning/06_cuisine_vue_panoramique.jpg",
                "/assets/images/studio_cocooning/07_chambre_mur_vert.jpg",
                "/assets/images/studio_cocooning/08_salle_de_bain.jpg",
                "/assets/images/studio_cocooning/09_vue_integree.jpg",
                "/assets/images/studio_cocooning/10_informations_location.jpg"
            ]
        }
    ],
    "categories": {
        "sejour": {
            "nom": "Villas de Séjour",
            "description": "Villas pour séjours et vacances",
            "icon": "🏖️",
            "count": 13
        },
        "fete": {
            "nom": "Villas Fête/Journée",
            "description": "Espaces pour événements et fêtes",
            "icon": "🎉",
            "count": 5
        },
        "special": {
            "nom": "Locations Spéciales",
            "description": "Studios et locations particulières",
            "icon": "🏠",
            "count": 3
        }
    },
    "locations": [
        "Petit Macabou",
        "Sainte-Anne",
        "Ducos",
        "Lamentin",
        "Fort-de-France",
        "Rivière-Pilote",
        "Sainte-Luce",
        "Le François",
        "Trinité",
        "Le Robert",
        "Vauclin"
    ],
    "prix_range": {
        "min": 100,
        "max": 2200,
        "moyenne": 750
    },
    "stats": {
        "total_villas": 21,
        "total_photos": 195,
        "capacite_max": 100,
        "prix_moyen": 750
    }
};

// Fonction pour récupérer les villas
function getVillas() {
    return VILLAS_DATABASE.villas;
}

// Fonction pour filtrer les villas
function filterVillas(category = null, minPrice = null, maxPrice = null, location = null) {
    let villas = VILLAS_DATABASE.villas;
    
    if (category) {
        villas = villas.filter(villa => villa.categorie === category);
    }
    
    if (minPrice) {
        villas = villas.filter(villa => villa.prix_base >= minPrice);
    }
    
    if (maxPrice) {
        villas = villas.filter(villa => villa.prix_base <= maxPrice);
    }
    
    if (location) {
        villas = villas.filter(villa => villa.localisation.toLowerCase().includes(location.toLowerCase()));
    }
    
    return villas;
}

// Fonction pour chercher une villa
function searchVillas(query) {
    const searchTerm = query.toLowerCase();
    return VILLAS_DATABASE.villas.filter(villa => 
        villa.nom.toLowerCase().includes(searchTerm) ||
        villa.localisation.toLowerCase().includes(searchTerm) ||
        villa.equipements.toLowerCase().includes(searchTerm)
    );
}

// Export pour utilisation
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { VILLAS_DATABASE, getVillas, filterVillas, searchVillas };
}
