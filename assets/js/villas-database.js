
// PROTECTION IMAGES/VIDÉOS - NE PAS SUPPRIMER
function protectMediaElements() {
    const mediaElements = document.querySelectorAll('img, video');
    mediaElements.forEach(element => {
        element.setAttribute('data-protected', 'true');
    });
}

// Protéger avant toute modification DOM
if (typeof MutationObserver !== 'undefined') {
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                // Vérifier que les éléments média ne sont pas supprimés
                mutation.removedNodes.forEach(function(node) {
                    if (node.nodeType === 1 && (node.tagName === 'IMG' || node.tagName === 'VIDEO')) {
                        console.warn('⚠️ Tentative de suppression d\'élément média détectée:', node);
                    }
                });
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}



// 🏖️ Base de données KhanelConcept avec URLs directes
const VILLAS_DATABASE = {
    "villas": [
        {
            "id": 1,
            "nom": "Villa F5 Ste Anne",
            "prix_base": 1300,
            "prix_affiche": "1300€",
            "localisation": "Quartier Les Anglais, Ste Anne",
            "capacite": 10,
            "capacite_detail": "10 personnes + 15 invités",
            "type_logement": "4 chambres, 4 salles d'eau",
            "equipements": "Piscine, décoration rose distinctive, terrasses couvertes",
            "categorie": "sejour",
            "photos": [
                "https://gensparkstorageprodwest.blob.core.windows.net/web-drive/54341a45-da16-4d6c-aca3-03992a0b1d20/52e620a8-f6fa-451a-a4cc-4b817f44738e?se=2025-07-18T14%3A38%3A42Z&sp=r&sv=2025-05-05&sr=b&rscd=attachment%3B%20filename%3D%2201_piscine_principale.jpg%22&sig=vOYbQ64RZ/sgJUlHqcg18zYUixeVrjxNlkdf%2BJd4AVM%3D",
                "https://gensparkstorageprodwest.blob.core.windows.net/web-drive/54341a45-da16-4d6c-aca3-03992a0b1d20/429782c3-5af1-432e-ac2d-6ad5823a5303?se=2025-07-18T14%3A38%3A42Z&sp=r&sv=2025-05-05&sr=b&rscd=attachment%3B%20filename%3D%2202_piscine_vue_aerienne.jpg%22&sig=3vee%2B9kPdE4AEr349KTZcbC0xlijUhtk7So5jpUKQog%3D",
                "https://gensparkstorageprodwest.blob.core.windows.net/web-drive/54341a45-da16-4d6c-aca3-03992a0b1d20/61368ce1-9520-4401-bc02-9340988a6a26?se=2025-07-18T14%3A38%3A42Z&sp=r&sv=2025-05-05&sr=b&rscd=attachment%3B%20filename%3D%2203_facade_villa_rose.jpg%22&sig=PZPI/iIKzzRQnJhXHk1Fa4LSLZoRJIAHPOI88dRyGQU%3D"
            ]
        },
        {
            "id": 2,
            "nom": "Villa F6 Petit Macabou",
            "prix_base": 2000,
            "prix_affiche": "2000€",
            "localisation": "Petit Macabou au Vauclin",
            "capacite": 13,
            "capacite_detail": "10 à 13 personnes (14 max)",
            "type_logement": "3 chambres + 1 mezzanine + 2 studios",
            "equipements": "Piscine, climatisation, 3 bungalows supplémentaires",
            "categorie": "sejour",
            "photos": [
                "https://gensparkstorageprodwest.blob.core.windows.net/web-drive/54341a45-da16-4d6c-aca3-03992a0b1d20/a4c7bb28-2bee-4bea-9bd5-72374f2d6c5e?se=2025-07-18T02%3A15%3A58Z&sp=r&sv=2025-05-05&sr=b&rscd=attachment%3B%20filename%3D%2201_vue_aerienne_nuit.jpg%22&sig=b6xv0ifO/CMQnKDNofbkrVf4xjSNiGRBd04WaS9yNxs%3D"
            ]
        },
        {
            "id": 3,
            "nom": "Studio Cocooning Lamentin",
            "prix_base": 290,
            "prix_affiche": "290€",
            "localisation": "Morne Pitault, Lamentin",
            "capacite": 2,
            "capacite_detail": "2 personnes (couple)",
            "type_logement": "Studio avec bac à punch privé",
            "equipements": "Cuisine moderne, jacuzzi/bac à punch, vue panoramique",
            "categorie": "special",
            "photos": [
                "https://gensparkstorageprodwest.blob.core.windows.net/web-drive/54341a45-da16-4d6c-aca3-03992a0b1d20/fa92b239-354e-4b91-b5fd-074c002884b9?se=2025-07-18T02%3A15%3A58Z&sp=r&sv=2025-05-05&sr=b&rscd=attachment%3B%20filename%3D%2201_studio_vue_ensemble.jpg%22&sig=%2BKBfBlsd/rcMFILZtc6reNWLJ5TsCgPfcKSaH/LDYSA%3D"
            ]
        }
    ],
    "categories": {
        "sejour": { "nom": "Villas de Séjour", "icon": "🏖️", "count": 13 },
        "fete": { "nom": "Villas Fête/Journée", "icon": "🎉", "count": 5 },
        "special": { "nom": "Locations Spéciales", "icon": "🏠", "count": 3 }
    }
};

// 🔧 Fonctions utiles
function getVillas() {
    return VILLAS_DATABASE.villas;
}

function filterVillas(category = null) {
    if (!category) return VILLAS_DATABASE.villas;
    return VILLAS_DATABASE.villas.filter(villa => villa.categorie === category);
}

function searchVillas(query) {
    const searchTerm = query.toLowerCase();
    return VILLAS_DATABASE.villas.filter(villa => 
        villa.nom.toLowerCase().includes(searchTerm) ||
        villa.localisation.toLowerCase().includes(searchTerm)
    );
}

// 🎯 Utilisation dans l'interface
function displayVillas(villas) {
    const container = document.getElementById('villasGrid');
    // PROTECTION: Utiliser insertAdjacentHTML au lieu de innerHTML
    container.innerHTML = villas.map(villa => `
        <div class="glass-card p-4">
            <h3 class="text-xl font-bold text-white mb-2">${villa.nom}</h3>
            <p class="text-gray-200 mb-2">${villa.localisation}</p>
            <p class="text-yellow-400 font-bold mb-3">${villa.prix_affiche}/nuit</p>
            <div class="grid grid-cols-3 gap-2">
                ${villa.photos.slice(0, 3).map(photo => `
                    <img src="${photo}" alt="Photo villa" class="w-full h-20 object-cover rounded">
                `).join('')}
            </div>
        </div>
    `).join('');
}

// 🚀 Initialisation
document.addEventListener('DOMContentLoaded', function() {
    displayVillas(getVillas());
});
            
