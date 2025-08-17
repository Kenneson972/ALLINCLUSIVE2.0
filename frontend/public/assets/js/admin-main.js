window.ADMIN_WRITE_ENABLED = (typeof window.ADMIN_WRITE_ENABLED !== 'undefined') ? window.ADMIN_WRITE_ENABLED : false;
async function apiPost(endpoint,payload){ if(!window.ADMIN_WRITE_ENABLED){ const b=document.querySelector('.api-banner')||(function(){const d=document.createElement('div');d.className='api-banner';d.style.cssText='position:fixed;bottom:10px;left:10px;background:rgba(0,0,0,.65);color:#fff;padding:6px 10px;border-radius:8px;font-size:12px;z-index:9999';document.body.appendChild(d);return d;})(); b.textContent='ℹ️ Fonction disponible bientôt — backend en préparation'; return {status:'disabled'};} try{ const res=await fetch(endpoint,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(payload||{})}); if(!res.ok) throw new Error('API'); const data=await res.json(); const b=document.querySelector('.api-banner')||(function(){const d=document.createElement('div');d.className='api-banner';d.style.cssText='position:fixed;bottom:10px;left:10px;background:rgba(0,0,0,.65);color:#fff;padding:6px 10px;border-radius:8px;font-size:12px;z-index:9999';document.body.appendChild(d);return d;})(); b.textContent='✅ Action simulée — en attente du backend réel'; return data;}catch(e){ const b=document.querySelector('.api-banner')||(function(){const d=document.createElement('div');d.className='api-banner';d.style.cssText='position:fixed;bottom:10px;left:10px;background:rgba(0,0,0,.65);color:#fff;padding:6px 10px;border-radius:8px;font-size:12px;z-index:9999';document.body.appendChild(d);return d;})(); b.textContent='Service momentanément indisponible (mode dégradé)'; return {status:'error'};}}
async function apiPut(endpoint,payload){ if(!window.ADMIN_WRITE_ENABLED){ const b=document.querySelector('.api-banner')||(function(){const d=document.createElement('div');d.className='api-banner';d.style.cssText='position:fixed;bottom:10px;left:10px;background:rgba(0,0,0,.65);color:#fff;padding:6px 10px;border-radius:8px;font-size:12px;z-index:9999';document.body.appendChild(d);return d;})(); b.textContent='ℹ️ Fonction disponible bientôt — backend en préparation'; return {status:'disabled'};} try{ const res=await fetch(endpoint,{method:'PUT',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(payload||{})}); if(!res.ok) throw new Error('API'); const data=await res.json(); const b=document.querySelector('.api-banner')||(function(){const d=document.createElement('div');d.className='api-banner';d.style.cssText='position:fixed;bottom:10px;left:10px;background:rgba(0,0,0,.65);color:#fff;padding:6px 10px;border-radius:8px;font-size:12px;z-index:9999';document.body.appendChild(d);return d;})(); b.textContent='✅ Action simulée — en attente du backend réel'; return data;}catch(e){ const b=document.querySelector('.api-banner')||(function(){const d=document.createElement('div');d.className='api-banner';d.style.cssText='position:fixed;bottom:10px;left:10px;background:rgba(0,0,0,.65);color:#fff;padding:6px 10px;border-radius:8px;font-size:12px;z-index:9999';document.body.appendChild(d);return d;})(); b.textContent='Service momentanément indisponible (mode dégradé)'; return {status:'error'};}}

async function apiGet(endpoint){
  try{
    const res = await fetch(`${endpoint}`, { headers: { 'Accept':'application/json' } });
    if(!res.ok) throw new Error('API error');
    return await res.json();
  }catch(e){
    console.warn('API fallback for', endpoint, e);
    const banner=document.querySelector('.api-banner') || (function(){const b=document.createElement('div'); b.className='api-banner'; b.style.cssText='position:fixed;bottom:10px;left:10px;background:rgba(0,0,0,.6);color:#fff;padding:6px 10px;border-radius:8px;font-size:12px;z-index:9999'; b.textContent='Service momentanément indisponible (mode dégradé)'; document.body.appendChild(b); return b;})();
    return [];
  }
}

// Admin Main JavaScript
class AdminApp {
    constructor() {
        this.currentSection = 'dashboard';
        this.villas = [];
        this.settings = {};
        this.charts = {};
        
        this.init();
    }

    init() {
        this.loadData();
        this.setupEventListeners();
        this.checkAuthentication();
        
        // Initialize managers
        this.villaManager = new VillaManager(this);
        this.exportManager = new DataExportManager(this);
        this.syncManager = new SyncManager(this);
        
        // Initialize image handler
        window.imageHandler = new ImageHandler(this);
        
        this.updateDashboard();
    }

    checkAuthentication() {
        const adminAccess = sessionStorage.getItem('admin_access');
        if (adminAccess !== 'true') {
            window.location.href = 'login.html';
            return;
        }
        
        // Display username
        const adminUser = sessionStorage.getItem('admin_user') || 'Admin';
        const usernameElement = document.getElementById('adminUsername');
        if (usernameElement) {
            usernameElement.textContent = adminUser;
        }
    }

    async loadData() {
        // Load from API (mock) instead of localStorage
        try {
            this.villas = await apiGet('/api/v1/villas');
            this.settings = await apiGet('/api/v1/settings');
        } catch(e){
            console.warn('API error, using defaults');
            this.villas = this.getDefaultVillas();
            this.settings = this.getDefaultSettings();
        }
    }

    saveData() {
  apiPut('/api/v1/settings', this.settings);// Sync with main website data
        this.syncWithMainSite();
    }

    syncWithMainSite() {
  apiPost('/api/v1/reservations', {sync:true, villasCount: (this.villas||[]).length});
        // Generate data for main website integration
        try {
            const mainSiteData = this.villas
                .filter(villa => villa.status === 'active')
                .map(villa => ({
                    id: villa.id,
                    name: villa.name,
                    location: villa.location,
                    price: villa.price,
                    guests: villa.capacity,
                    guestsDetail: `${villa.capacity} personnes`,
                    features: (villa.amenities || []).join(', '),
                    category: 'sejour',
                    image: villa.photos && villa.photos[0] ? villa.photos[0] : './images/placeholder.jpg',
                    gallery: villa.photos || [],
                    fallbackIcon: this.getVillaIcon(villa),
                    description: villa.description,
                    amenities: this.formatAmenitiesForWebsite(villa.amenities || [])
                }));

            // Store synchronized data for main siteconsole.log('Data synchronized with main site:', mainSiteData.length, 'active villas');
        } catch (error) {
            console.error('Error syncing with main site:', error);
        }
    }

    getVillaIcon(villa) {
        if (villa.amenities) {
            if (villa.amenities.includes('piscine')) return '🏊';
            if (villa.amenities.includes('vue-mer')) return '🌊';
            if (villa.amenities.includes('jacuzzi')) return '🛁';
            if (villa.amenities.includes('plage')) return '🏖️';
        }
        return '🏠';
    }

    formatAmenitiesForWebsite(amenities) {
        const iconMap = {
            'piscine': '🏊',
            'wifi': '📶',
            'climatisation': '❄️',
            'vue-mer': '🌊',
            'parking': '🚗',
            'cuisine': '🍳',
            'terrasse': '🏖️',
            'barbecue': '🔥',
            'jacuzzi': '🛁',
            'plage': '🏖️',
            'jardin': '🌳',
            'tv': '📺',
            'sauna': '🧖‍♀️'
        };

        return amenities.map(amenity => ({
            icon: iconMap[amenity] || '✨',
            name: this.capitalizeFirst(amenity.replace('-', ' '))
        }));
    }

    capitalizeFirst(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    getDefaultVillas() {
        // Import all 21 villas from the main site with real data
        return [
            {
                id: 1,
                name: "Villa F3 Petit Macabou",
                description: "Magnifique villa F3 avec sauna et jacuzzi, parfaite pour un séjour de détente en famille. Située à Petit Macabou au Vauclin, cette villa offre une piscine extérieure, un sauna privé, un jacuzzi et deux douches extérieures dans un cadre tropical exceptionnel.",
                price: 850,
                capacity: 6,
                bedrooms: 2,
                bathrooms: 2,
                location: "Petit Macabou au Vauclin",
                gps: "14.5428, -60.8357",
                amenities: ["piscine", "sauna", "jacuzzi", "wifi", "terrasse"],
                photos: [
                    "./images/Villa_F3_Petit_Macabou/01_piscine_exterieur.jpg",
                    "./images/Villa_F3_Petit_Macabou/02_terrasse_salon_exterieur.jpg",
                    "./images/Villa_F3_Petit_Macabou/03_salle_de_bain_moderne.jpg",
                    "./images/Villa_F3_Petit_Macabou/04_chambre_principale.jpg",
                    "./images/Villa_F3_Petit_Macabou/05_cuisine_equipee.jpg",
                    "./images/Villa_F3_Petit_Macabou/07_sauna_detente.jpg",
                    "./images/Villa_F3_Petit_Macabou/08_douche_exterieure.jpg"
                ],
                status: "active",
                created: new Date().toISOString(),
                updated: new Date().toISOString()
            },
            {
                id: 2,
                name: "Villa F5 Ste Anne",
                description: "Villa F5 distinctive avec sa façade rose emblématique, située dans le quartier résidentiel des Anglais à Sainte-Anne. Cette spacieuse propriété dispose d'une grande piscine, cuisine moderne, salon principal et chambres confortables dont une spécialisée pour enfants.",
                price: 1300,
                capacity: 10,
                bedrooms: 3,
                bathrooms: 2,
                location: "Quartier Les Anglais, Ste Anne",
                gps: "14.4298, -60.8824",
                amenities: ["piscine", "wifi", "cuisine", "parking", "terrasse"],
                photos: [
                    "./images/Villa_F5_Ste_Anne/01_piscine_principale.jpg",
                    "./images/Villa_F5_Ste_Anne/02_piscine_vue_aerienne.jpg",
                    "./images/Villa_F5_Ste_Anne/03_facade_villa_rose.jpg",
                    "./images/Villa_F5_Ste_Anne/04_cuisine_moderne.jpg",
                    "./images/Villa_F5_Ste_Anne/05_salon_principal.jpg",
                    "./images/Villa_F5_Ste_Anne/06_chambre_principale.jpg"
                ],
                status: "active",
                created: new Date().toISOString(),
                updated: new Date().toISOString()
            },
            {
                id: 3,
                name: "Villa F3 Baccha Petit Macabou",
                description: "Villa F3 moderne 'Pour la Baccha' à Petit Macabou, avec terrasses étagées offrant différents espaces de vie selon vos envies. Parfaite pour les moments festifs avec piscine, terrasse jardin et équipements modernes pour célébrations.",
                price: 1350,
                capacity: 6,
                bedrooms: 2,
                bathrooms: 2,
                location: "Petit Macabou",
                gps: "14.5428, -60.8357",
                amenities: ["piscine", "wifi", "terrasse", "jardin"],
                photos: [
                    "./images/Villa_F3_Baccha_Petit_Macabou/01_terrasse_piscine_salon_ext.jpg",
                    "./images/Villa_F3_Baccha_Petit_Macabou/02_terrasse_piscine_angle.jpg",
                    "./images/Villa_F3_Baccha_Petit_Macabou/03_chambre_moderne.jpg",
                    "./images/Villa_F3_Baccha_Petit_Macabou/04_terrasse_jardin.jpg",
                    "./images/Villa_F3_Baccha_Petit_Macabou/05_cuisine_equipee.jpg",
                    "./images/Villa_F3_Baccha_Petit_Macabou/06_chambre_2.jpg"
                ],
                status: "active",
                created: new Date().toISOString(),
                updated: new Date().toISOString()
            },
            {
                id: 4,
                name: "Villa F6 Lamentin",
                description: "Villa F6 au Lamentin avec piscine et jacuzzi vue d'ensemble spectaculaire. Propriété spacieuse idéale pour grands groupes avec équipements complets pour séjours détente et fêtes familiales dans un cadre luxueux.",
                price: 1500,
                capacity: 10,
                bedrooms: 4,
                bathrooms: 3,
                location: "Quartier Bélème au Lamentin",
                gps: "14.6097, -61.0242",
                amenities: ["piscine", "jacuzzi", "wifi", "cuisine"],
                photos: [
                    "./images/Villa_F6_Lamentin/01_piscine_jacuzzi_vue_ensemble.jpg"
                ],
                status: "active",
                created: new Date().toISOString(),
                updated: new Date().toISOString()
            },
            {
                id: 5,
                name: "Villa F6 Ste Luce Plage",
                description: "Villa F6 à Sainte-Luce à seulement 1 minute de la plage avec vue aérienne spectaculaire sur la piscine. Salon donnant sur piscine, cuisine moderne équipée, salle à manger spacieuse et chambres authentiques avec poutres apparentes.",
                price: 1700,
                capacity: 14,
                bedrooms: 4,
                bathrooms: 3,
                location: "Zac de Pont Café, Ste Luce",
                gps: "14.4686, -61.0553",
                amenities: ["piscine", "vue-mer", "plage", "wifi", "cuisine"],
                photos: [
                    "./images/Villa_F6_Ste_Luce_Plage/02_chambre_poutres.jpg",
                    "./images/Villa_F6_Ste_Luce_Plage/03_cuisine_moderne.jpg",
                    "./images/Villa_F6_Ste_Luce_Plage/04_salle_a_manger.jpg",
                    "./images/Villa_F6_Ste_Luce_Plage/05_vue_aerienne_piscine.jpg",
                    "./images/Villa_F6_Ste_Luce_Plage/06_salon_piscine.jpg"
                ],
                status: "active",
                created: new Date().toISOString(),
                updated: new Date().toISOString()
            },
            {
                id: 6,
                name: "Villa F6 Petit Macabou",
                description: "Villa F6 événementielle d'exception à Petit Macabou. Vue aérienne spectaculaire jour/nuit, 3 chambres climatisées + mezzanine + 2 studios indépendants. Fêtes autorisées jusqu'à 150 convives avec terrasses multiples et piscine XXL.",
                price: 2000,
                capacity: 13,
                bedrooms: 3,
                bathrooms: 3,
                location: "Petit Macabou au Vauclin",
                gps: "14.5428, -60.8357",
                amenities: ["piscine", "wifi", "terrasse", "vue-mer", "jacuzzi"],
                photos: [
                    "./images/Villa_F6_Petit_Macabou/02_salle_de_bain.jpg",
                    "./images/Villa_F6_Petit_Macabou/03_chambre_studio.jpg",
                    "./images/Villa_F6_Petit_Macabou/04_salon_mezzanine.jpg",
                    "./images/Villa_F6_Petit_Macabou/05_cuisine_moderne.jpg",
                    "./images/Villa_F6_Petit_Macabou/06_terrasse_couverte.jpg",
                    "./images/Villa_F6_Petit_Macabou/07_terrasse_piscine.jpg",
                    "./images/Villa_F6_Petit_Macabou/10_vue_aerienne_jour.jpg"
                ],
                status: "active",
                created: new Date().toISOString(),
                updated: new Date().toISOString()
            },
            {
                id: 7,
                name: "Villa F7 Baie des Mulets",
                description: "Villa F7 prestige à la Baie des Mulets avec véranda salle à manger en bambou et coin détente avec fauteuils suspendus uniques. Design moderne blanc épuré avec chambre principale aux couleurs vives bleu-jaune. Fêtes autorisées jusqu'à 160 convives.",
                price: 2200,
                capacity: 16,
                bedrooms: 5,
                bathrooms: 4,
                location: "Baie des Mulets, Vauclin",
                gps: "14.5428, -60.8357",
                amenities: ["piscine", "vue-mer", "wifi", "terrasse", "jardin"],
                photos: [
                    "./images/Villa_F7_Baie_des_Mulets_Vauclin/veranda_salle_a_manger_bambou.jpg",
                    "./images/Villa_F7_Baie_des_Mulets_Vauclin/salon_canape_angle_gris.jpg",
                    "./images/Villa_F7_Baie_des_Mulets_Vauclin/chambre_principale_bleu_jaune.jpg",
                    "./images/Villa_F7_Baie_des_Mulets_Vauclin/cuisine_moderne_blanche.jpg",
                    "./images/Villa_F7_Baie_des_Mulets_Vauclin/coin_detente_fauteuils_suspendus.jpg"
                ],
                status: "active",
                created: new Date().toISOString(),
                updated: new Date().toISOString()
            },
            {
                id: 8,
                name: "Villa F3 Trinité (Cosmy)",
                description: "Villa F3 Cosmy à La Trinité avec double vue exceptionnelle : piscine chauffée vue collines et panorama océan. Décoration tropicale turquoise et bleue avec cuisine américaine bois et salon cosy avec coussins turquoise.",
                price: 670,
                capacity: 5,
                bedrooms: 2,
                bathrooms: 2,
                location: "Cosmy, Trinité Martinique",
                gps: "14.7394, -60.9693",
                amenities: ["piscine", "vue-mer", "wifi", "cuisine"],
                photos: [
                    "./images/Villa_F3_Trinite_Cosmy/piscine_chauffee_vue_collines.jpg",
                    "./images/Villa_F3_Trinite_Cosmy/piscine_vue_panoramique_ocean.jpg",
                    "./images/Villa_F3_Trinite_Cosmy/salon_canape_angle_marron_coussins_turquoise.jpg",
                    "./images/Villa_F3_Trinite_Cosmy/cuisine_americaine_jaune_bois.jpg",
                    "./images/Villa_F3_Trinite_Cosmy/chambre_1_linge_tropical_turquoise.jpg",
                    "./images/Villa_F3_Trinite_Cosmy/chambre_2_bleu_blanc_tapis_moelleux.jpg"
                ],
                status: "active",
                created: new Date().toISOString(),
                updated: new Date().toISOString()
            },
            {
                id: 9,
                name: "Villa F3 Le Robert",
                description: "Villa F3 au Robert avec piscine rectangulaire moderne et équipements complets. Cuisine ouverte avec plan de travail, salon TV spacieux et magnifique terrasse couverte avec pergola et kitchenette extérieure.",
                price: 750,
                capacity: 10,
                bedrooms: 2,
                bathrooms: 2,
                location: "Pointe Hyacinthe, Robert",
                gps: "14.6753, -60.9398",
                amenities: ["piscine", "wifi", "cuisine", "terrasse", "tv"],
                photos: [
                    "./images/Villa_F3_Robert_Pointe_Hyacinthe/piscine_rectangulaire_moderne.jpg",
                    "./images/Villa_F3_Robert_Pointe_Hyacinthe/terrasse_couverte_pergola_kitchenette.jpg",
                    "./images/Villa_F3_Robert_Pointe_Hyacinthe/salon_salle_a_manger_tv.jpg",
                    "./images/Villa_F3_Robert_Pointe_Hyacinthe/cuisine_ouverte_plan_travail.jpg",
                    "./images/Villa_F3_Robert_Pointe_Hyacinthe/cuisine_equipee_frigo_congelateur.jpg"
                ],
                status: "active",
                created: new Date().toISOString(),
                updated: new Date().toISOString()
            },
            {
                id: 10,
                name: "Villa F5 R.Pilote",
                description: "Villa F5 à La Renée avec piscine sur terrasse bois entourée de palmiers tropicaux. Design audacieux avec salon cuir noir sous plafond vert unique, terrasse hamacs pour la détente et cuisine bois clair moderne.",
                price: 900,
                capacity: 10,
                bedrooms: 3,
                bathrooms: 2,
                location: "Quartier La Renée, Rivière-Pilote",
                gps: "14.4172, -60.8945",
                amenities: ["piscine", "wifi", "terrasse", "cuisine", "jardin"],
                photos: [
                    "./images/Villa_F5_R_Pilote_La_Renee/piscine_terrasse_bois_palmiers.jpg",
                    "./images/Villa_F5_R_Pilote_La_Renee/terrasse_hamacs_salon_exterieur.jpg",
                    "./images/Villa_F5_R_Pilote_La_Renee/salon_cuir_noir_plafond_vert.jpg",
                    "./images/Villa_F5_R_Pilote_La_Renee/cuisine_equipee_bois_clair.jpg"
                ],
                status: "active",
                created: new Date().toISOString(),
                updated: new Date().toISOString()
            },
            {
                id: 11,
                name: "Villa F3 Le François",
                description: "Villa F3 au François avec terrasse piscine et vue mer panoramique spectaculaire. Design coloré avec cuisine bleue équipée, chambre moderne et salon extérieur détente avec vue aérienne exceptionnelle.",
                price: 950,
                capacity: 6,
                bedrooms: 2,
                bathrooms: 2,
                location: "Le François, Martinique",
                gps: "14.6207, -60.9067",
                amenities: ["piscine", "vue-mer", "wifi", "cuisine", "terrasse"],
                photos: [
                    "./images/Villa_F3_Le_Francois/01_terrasse_piscine_vue_mer.jpg",
                    "./images/Villa_F3_Le_Francois/02_terrasse_repas_vue_panoramique.jpg",
                    "./images/Villa_F3_Le_Francois/03_salon_exterieur_detente.jpg",
                    "./images/Villa_F3_Le_Francois/04_chambre_bleue_moderne.jpg",
                    "./images/Villa_F3_Le_Francois/05_cuisine_bleue_equipee.jpg",
                    "./images/Villa_F3_Le_Francois/06_salon_colore_deco.jpg",
                    "./images/Villa_F3_Le_Francois/07_vue_aerienne_villa.jpg"
                ],
                status: "active",
                created: new Date().toISOString(),
                updated: new Date().toISOString()
            },
            {
                id: 12,
                name: "Villa F5 Vauclin Ravine Plate",
                description: "Villa F5 moderne au Vauclin avec piscine à débordement et vue panoramique sur les collines. Architecture contemporaine avec poutres apparentes, cuisine granite et suite parentale avec salle de bain attenante.",
                price: 1200,
                capacity: 10,
                bedrooms: 3,
                bathrooms: 2,
                location: "Ravine Plate, Vauclin",
                gps: "14.5428, -60.8357",
                amenities: ["piscine", "vue-mer", "wifi", "cuisine", "terrasse"],
                photos: [
                    "./images/Villa_F5_Vauclin_Ravine_Plate/piscine_a_debordement_vue_panoramique.jpg",
                    "./images/Villa_F5_Vauclin_Ravine_Plate/terrasse_panoramique_gazebo_vue_collines.jpg",
                    "./images/Villa_F5_Vauclin_Ravine_Plate/salon_moderne_rouge_noir_escalier.jpg",
                    "./images/Villa_F5_Vauclin_Ravine_Plate/cuisine_equipee_bois_fonce_granite.jpg",
                    "./images/Villa_F5_Vauclin_Ravine_Plate/chambre_1_poutres_apparentes_orange.jpg",
                    "./images/Villa_F5_Vauclin_Ravine_Plate/chambre_2_suite_parentale_sdb_attenante.jpg"
                ],
                status: "active",
                created: new Date().toISOString(),
                updated: new Date().toISOString()
            },
            {
                id: 13,
                name: "Bas Villa F3 Ste Luce",
                description: "Bas Villa F3 à Sainte-Luce avec terrasse couverte et éclairage LED ambiance unique. Équipements modernes avec salon TV, salle de bain contemporaine, chambre climatisée et terrasse lounge pour la détente.",
                price: 470,
                capacity: 4,
                bedrooms: 1,
                bathrooms: 1,
                location: "Sainte-Luce",
                gps: "14.4686, -61.0553",
                amenities: ["wifi", "tv", "climatisation", "terrasse"],
                photos: [
                    "./images/Bas_Villa_F3_Ste_Luce/01_chambre_salle_a_manger.jpg",
                    "./images/Bas_Villa_F3_Ste_Luce/02_salle_de_bain_moderne.jpg",
                    "./images/Bas_Villa_F3_Ste_Luce/03_salon_tv_eclairage_led.jpg",
                    "./images/Bas_Villa_F3_Ste_Luce/05_terrasse_eclairage_ambiance.jpg",
                    "./images/Bas_Villa_F3_Ste_Luce/06_chambre_climatisee.jpg",
                    "./images/Bas_Villa_F3_Ste_Luce/08_terrasse_lounge.jpg"
                ],
                status: "active",
                created: new Date().toISOString(),
                updated: new Date().toISOString()
            },
            {
                id: 14,
                name: "Villa F3 Trenelle",
                description: "Villa F3 à Trenelle pour location longue durée, entièrement équipée avec salon salle à manger spacieux, espace détente confortable, cuisine moderne avec évier et entrée accueillante.",
                price: 800,
                capacity: 6,
                bedrooms: 2,
                bathrooms: 2,
                location: "Trenelle, Location Annuelle",
                gps: "14.6097, -61.0242",
                amenities: ["wifi", "cuisine", "tv", "parking"],
                photos: [
                    "./images/Villa_F3_Trenelle_Location_Annuelle/01_salon_salle_a_manger.jpg",
                    "./images/Villa_F3_Trenelle_Location_Annuelle/02_espace_detente.jpg",
                    "./images/Villa_F3_Trenelle_Location_Annuelle/03_salon_television.jpg",
                    "./images/Villa_F3_Trenelle_Location_Annuelle/04_couloir_entree.jpg",
                    "./images/Villa_F3_Trenelle_Location_Annuelle/05_cuisine_equipee.jpg",
                    "./images/Villa_F3_Trenelle_Location_Annuelle/06_cuisine_evier.jpg"
                ],
                status: "active",
                created: new Date().toISOString(),
                updated: new Date().toISOString()
            },
            {
                id: 15,
                name: "Studio Cocooning Lamentin",
                description: "Studio cocooning romantique au Morne Pitault au Lamentin, avec vue panoramique sur la baie de Fort-de-France. Parfait pour couples avec jacuzzi privé, cuisine moderne et chambre au décor zen.",
                price: 290,
                capacity: 2,
                bedrooms: 1,
                bathrooms: 1,
                location: "Morne Pitault, Lamentin",
                gps: "14.6097, -61.0242",
                amenities: ["jacuzzi", "vue-mer", "wifi", "cuisine"],
                photos: [
                    "./images/Studio_Cocooning_Lamentin/01_studio_vue_ensemble.jpg",
                    "./images/Studio_Cocooning_Lamentin/02_cuisine_moderne.jpg",
                    "./images/Studio_Cocooning_Lamentin/03_terrasse_jacuzzi.jpg",
                    "./images/Studio_Cocooning_Lamentin/04_cuisine_ouverte.jpg",
                    "./images/Studio_Cocooning_Lamentin/05_chambre_salon.jpg",
                    "./images/Studio_Cocooning_Lamentin/07_chambre_mur_vert.jpg"
                ],
                status: "active",
                created: new Date().toISOString(),
                updated: new Date().toISOString()
            },
            {
                id: 16,
                name: "Espace Piscine Journée Bungalow",
                description: "Espace piscine journée avec bungalow créole authentique et véranda traditionnelle. Studio intérieur avec kitchenette pour vos repas en journée dans un cadre tropical unique.",
                price: 150,
                capacity: 8,
                bedrooms: 1,
                bathrooms: 1,
                location: "Martinique",
                gps: "14.6415, -61.0242",
                amenities: ["piscine", "cuisine", "terrasse"],
                photos: [
                    "./images/Espace_Piscine_Journee_Bungalow/bungalow_exterieur_veranda_creole.jpg",
                    "./images/Espace_Piscine_Journee_Bungalow/bungalow_interieur_studio_kitchenette.jpg"
                ],
                status: "active",
                created: new Date().toISOString(),
                updated: new Date().toISOString()
            },
            {
                id: 17,
                name: "Villa Fête Ducos",
                description: "Villa fête à Ducos avec piscine équipée de jouets gonflables et bar extérieur gazebo. Parfaite pour événements avec terrasse couverte salon, mobilier extérieur et jardin parasol détente.",
                price: 200,
                capacity: 25,
                bedrooms: 2,
                bathrooms: 2,
                location: "Ducos, Martinique",
                gps: "14.7394, -60.8945",
                amenities: ["piscine", "barbecue", "terrasse", "jardin"],
                photos: [
                    "./images/Villa_Fete_Journee_Ducos/01_piscine_jouets_gonflables.jpg",
                    "./images/Villa_Fete_Journee_Ducos/02_terrasse_couverte_salon.jpg",
                    "./images/Villa_Fete_Journee_Ducos/03_bar_exterieur_gazebo.jpg",
                    "./images/Villa_Fete_Journee_Ducos/04_piscine_mobilier_exterieur.jpg",
                    "./images/Villa_Fete_Journee_Ducos/05_espace_repas_piscine.jpg",
                    "./images/Villa_Fete_Journee_Ducos/06_jardin_parasol_detente.jpg"
                ],
                status: "active",
                created: new Date().toISOString(),
                updated: new Date().toISOString()
            },
            {
                id: 18,
                name: "Villa Fête Fort-de-France",
                description: "Villa événementielle à Fort-de-France avec piscine panoramique et décor zen avec statues Buddha. Architecture coloniale authentique avec véranda à arches, terrasse à colonnes et cuisine moderne équipée.",
                price: 250,
                capacity: 30,
                bedrooms: 3,
                bathrooms: 2,
                location: "Fort-de-France, Martinique",
                gps: "14.6415, -61.0574",
                amenities: ["piscine", "vue-mer", "terrasse", "cuisine", "jardin"],
                photos: [
                    "./images/Villa_Fete_Journee_Fort_de_France/01_piscine_vue_panoramique.jpg",
                    "./images/Villa_Fete_Journee_Fort_de_France/02_piscine_statues_buddha.jpg",
                    "./images/Villa_Fete_Journee_Fort_de_France/03_terrasse_colonnes_vue.jpg",
                    "./images/Villa_Fete_Journee_Fort_de_France/04_veranda_arches_coloniales.jpg",
                    "./images/Villa_Fete_Journee_Fort_de_France/05_cuisine_moderne_equipee.jpg"
                ],
                status: "active",
                created: new Date().toISOString(),
                updated: new Date().toISOString()
            },
            {
                id: 19,
                name: "Villa Fête Rivière-Pilote",
                description: "Villa fête créole à Rivière-Pilote avec piscine tropicale vue panoramique. Architecture authentique avec salle à manger intérieure, cuisine moderne équipée et terrasse pierre donnant sur piscine.",
                price: 180,
                capacity: 20,
                bedrooms: 2,
                bathrooms: 2,
                location: "Rivière-Pilote, Martinique",
                gps: "14.4172, -60.8945",
                amenities: ["piscine", "cuisine", "terrasse", "vue-mer"],
                photos: [
                    "./images/Villa_Fete_Journee_R_Pilote/03_villa_creole_piscine_terrasse.jpg",
                    "./images/Villa_Fete_Journee_R_Pilote/04_piscine_tropicale_vue_panoramique.jpg",
                    "./images/Villa_Fete_Journee_R_Pilote/01_salle_a_manger_interieur.jpg",
                    "./images/Villa_Fete_Journee_R_Pilote/05_cuisine_moderne_equipee.jpg",
                    "./images/Villa_Fete_Journee_R_Pilote/06_terrasse_pierre_piscine.jpg"
                ],
                status: "active",
                created: new Date().toISOString(),
                updated: new Date().toISOString()
            },
            {
                id: 20,
                name: "Villa Fête Sainte-Luce",
                description: "Villa fête moderne à Sainte-Luce avec piscine et terrasse aménagée. Équipements événementiels complets avec tentes blanches, mobilier professionnel et décorations anniversaire pour célébrations mémorables.",
                price: 220,
                capacity: 35,
                bedrooms: 3,
                bathrooms: 2,
                location: "Sainte-Luce, Martinique",
                gps: "14.4686, -61.0553",
                amenities: ["piscine", "terrasse", "cuisine", "jardin"],
                photos: [
                    "./images/Villa_Fete_Journee_Sainte_Luce/01_villa_moderne_piscine_terrasse.jpg",
                    "./images/Villa_Fete_Journee_Sainte_Luce/02_piscine_tentes_amenagement.jpg",
                    "./images/Villa_Fete_Journee_Sainte_Luce/03_tentes_blanches_mobilier.jpg",
                    "./images/Villa_Fete_Journee_Sainte_Luce/04_villa_contemporaine_exterieur.jpg",
                    "./images/Villa_Fete_Journee_Sainte_Luce/05_decoration_anniversaire_fete.jpg"
                ],
                status: "active",
                created: new Date().toISOString(),
                updated: new Date().toISOString()
            },
            {
                id: 21,
                name: "Villa Fête Rivière-Salée",
                description: "Villa fête à Rivière-Salée avec piscine et tente couverte pour événements intimistes. Parfaite pour petites célébrations familiales ou entre amis dans un cadre convivial et protégé.",
                price: 160,
                capacity: 15,
                bedrooms: 2,
                bathrooms: 1,
                location: "Rivière-Salée, Martinique",
                gps: "14.4172, -60.8945",
                amenities: ["piscine", "terrasse"],
                photos: [
                    "./images/Villa_Fete_Journee_Riviere_Salee/01_piscine_tente_couverte.jpg"
                ],
                status: "active",
                created: new Date().toISOString(),
                updated: new Date().toISOString()
            }
        ];
    }

    getDefaultSettings() {
        return {
            siteName: "KhanelConcept",
            contactEmail: "contact@khanelconcept.com",
            contactPhone: "+596 696 XX XX XX",
            currency: "EUR",
            language: "fr"
        };
    }

    setupEventListeners() {
        // Sidebar navigation
        document.querySelectorAll('.menu-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const section = item.getAttribute('data-section');
                this.showSection(section);
            });
        });

        // Search and filters
        const searchInput = document.getElementById('villaSearch');
        if (searchInput) {
            searchInput.addEventListener('input', () => this.filterVillas());
        }

        const statusFilter = document.getElementById('statusFilter');
        if (statusFilter) {
            statusFilter.addEventListener('change', () => this.filterVillas());
        }

        const priceFilter = document.getElementById('priceFilter');
        if (priceFilter) {
            priceFilter.addEventListener('change', () => this.filterVillas());
        }

        // Settings form
        const settingsForm = document.getElementById('settingsForm');
        if (settingsForm) {
            settingsForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.saveSettings();
            });
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 's') {
                e.preventDefault();
                this.saveData();
                this.showToast('Données sauvegardées', 'success');
            }
            if (e.key === 'Escape') {
                const modals = document.querySelectorAll('.modal.show');
                modals.forEach(modal => {
                    bootstrap.Modal.getInstance(modal)?.hide();
                });
            }
        });
    }

    showSection(sectionName) {
        // Update active menu item
        document.querySelectorAll('.menu-item').forEach(item => {
            item.classList.remove('active');
        });
        document.querySelector(`[data-section="${sectionName}"]`).classList.add('active');

        // Update active section
        document.querySelectorAll('.content-section').forEach(section => {
            section.classList.remove('active');
        });
        document.getElementById(`${sectionName}-section`).classList.add('active');

        // Update page title
        const titles = {
            'dashboard': 'Dashboard',
            'villas': 'Gestion des Villas',
            'reservations': 'Réservations',
            'images': 'Gestion des Images',
            'settings': 'Paramètres'
        };
        document.getElementById('pageTitle').textContent = titles[sectionName];

        this.currentSection = sectionName;

        // Load section-specific data
        switch (sectionName) {
            case 'dashboard':
                this.updateDashboard();
                break;
            case 'villas':
                this.loadVillasGrid();
                break;
            case 'images':
                this.loadImageGallery();
                break;
            case 'settings':
                this.loadSettings();
                break;
        }
    }

    loadImageGallery() {
        if (window.imageHandler) {
            window.imageHandler.loadImageGallery();
        }
    }

    // Villa management methods
    editVilla(villaId) {
        if (this.villaManager) {
            this.villaManager.editVilla(villaId);
        }
    }

    duplicateVilla(villaId) {
        if (this.villaManager) {
            this.villaManager.duplicateVilla(villaId);
        }
    }

    deleteVilla(villaId) {
        if (this.villaManager) {
            this.villaManager.deleteVilla(villaId);
        }
    }

    showAddVillaModal() {
        if (this.villaManager) {
            this.villaManager.showAddVillaModal();
        }
    }

    previewVilla(villaId) {
        const villa = this.villas.find(v => v.id === villaId);
        if (!villa) return;

        // Open villa details in new tab/window
        const url = `../villa-details.html?id=${villaId}`;
        window.open(url, '_blank');
    }

    getAmenityIcon(amenity) {
        const iconMap = {
            'piscine': '🏊',
            'wifi': '📶',
            'climatisation': '❄️',
            'vue-mer': '🌊',
            'parking': '🚗',
            'cuisine': '🍳',
            'terrasse': '🏖️',
            'barbecue': '🔥',
            'jacuzzi': '🛁',
            'plage': '🏖️',
            'jardin': '🌳',
            'tv': '📺',
            'sauna': '🧖‍♀️'
        };
        return iconMap[amenity] || '✨';
    }

    updateDashboard() {
        // Update stats
        document.getElementById('totalVillas').textContent = this.villas.length;
        document.getElementById('activeVillas').textContent = 
            this.villas.filter(v => v.status === 'active').length;
        document.getElementById('totalReservations').textContent = '0'; // Placeholder
        
        const avgPrice = this.villas.length > 0 ? 
            Math.round(this.villas.reduce((sum, v) => sum + v.price, 0) / this.villas.length) : 0;
        document.getElementById('averagePrice').textContent = `${avgPrice}€`;

        // Update charts
        this.updateCharts();

        // Update recent activity
        this.updateRecentActivity();
    }

    updateCharts() {
        // Price distribution chart
        const priceCtx = document.getElementById('priceChart');
        if (priceCtx && this.charts.priceChart) {
            this.charts.priceChart.destroy();
        }
        
        const priceRanges = {
            '0-500€': this.villas.filter(v => v.price < 500).length,
            '500-1000€': this.villas.filter(v => v.price >= 500 && v.price < 1000).length,
            '1000-1500€': this.villas.filter(v => v.price >= 1000 && v.price < 1500).length,
            '1500€+': this.villas.filter(v => v.price >= 1500).length
        };

        this.charts.priceChart = new Chart(priceCtx, {
            type: 'bar',
            data: {
                labels: Object.keys(priceRanges),
                datasets: [{
                    label: 'Nombre de villas',
                    data: Object.values(priceRanges),
                    backgroundColor: 'rgba(37, 99, 235, 0.8)',
                    borderColor: 'rgba(37, 99, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });

        // Status chart
        const statusCtx = document.getElementById('statusChart');
        if (statusCtx && this.charts.statusChart) {
            this.charts.statusChart.destroy();
        }

        const statusData = {
            'Actif': this.villas.filter(v => v.status === 'active').length,
            'Inactif': this.villas.filter(v => v.status === 'inactive').length
        };

        this.charts.statusChart = new Chart(statusCtx, {
            type: 'doughnut',
            data: {
                labels: Object.keys(statusData),
                datasets: [{
                    data: Object.values(statusData),
                    backgroundColor: [
                        'rgba(34, 197, 94, 0.8)',
                        'rgba(239, 68, 68, 0.8)'
                    ],
                    borderColor: [
                        'rgba(34, 197, 94, 1)',
                        'rgba(239, 68, 68, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    updateRecentActivity() {
        const activityContainer = document.getElementById('recentActivity');
        const recentVillas = this.villas
            .sort((a, b) => new Date(b.updated) - new Date(a.updated))
            .slice(0, 5);

        if (recentVillas.length === 0) {
            activityContainer.innerHTML = '<p class="text-muted">Aucune activité récente</p>';
            return;
        }

        activityContainer.innerHTML = recentVillas.map(villa => `
            <div class="d-flex align-items-center mb-3">
                <div class="me-3">
                    <i class="fas fa-home text-primary"></i>
                </div>
                <div class="flex-grow-1">
                    <h6 class="mb-0">${villa.name}</h6>
                    <small class="text-muted">Modifié ${this.formatDate(villa.updated)}</small>
                </div>
                <span class="badge bg-${villa.status === 'active' ? 'success' : 'danger'}">${villa.status}</span>
            </div>
        `).join('');
    }

    loadVillasGrid() {
        this.renderVillas(this.villas);
    }

    renderVillas(villas) {
        const grid = document.getElementById('villasGrid');
        if (!grid) return;

        if (villas.length === 0) {
            grid.innerHTML = `
                <div class="col-12 text-center py-5">
                    <i class="fas fa-home fa-3x text-muted mb-3"></i>
                    <h4>Aucune villa trouvée</h4>
                    <p class="text-muted">Commencez par ajouter votre première villa</p>
                    <button class="btn btn-primary" onclick="app.showAddVillaModal()">
                        <i class="fas fa-plus me-2"></i>Ajouter Villa
                    </button>
                </div>
            `;
            return;
        }

        grid.innerHTML = villas.map(villa => `
            <div class="col-lg-4 col-md-6 mb-4">
                <div class="card villa-card">
                    <div class="position-relative">
                        <img src="${villa.photos && villa.photos[0] ? villa.photos[0] : 'https://via.placeholder.com/300x200?text=Aucune+image'}" 
                             class="card-img-top" alt="${villa.name}" style="height: 200px; object-fit: cover;">
                        <span class="villa-status status-${villa.status}">
                            ${villa.status === 'active' ? 'Actif' : 'Inactif'}
                        </span>
                        <div class="position-absolute top-0 start-0 p-2">
                            <span class="badge bg-primary">ID: ${villa.id}</span>
                        </div>
                        ${villa.photos && villa.photos.length > 1 ? 
                            `<div class="position-absolute bottom-0 end-0 p-2">
                                <span class="badge bg-info"><i class="fas fa-images"></i> ${villa.photos.length}</span>
                            </div>` : ''
                        }
                    </div>
                    <div class="card-body">
                        <h5 class="card-title">${villa.name}</h5>
                        <p class="card-text text-muted small">
                            <i class="fas fa-map-marker-alt me-1"></i>${villa.location}
                        </p>
                        <p class="card-text">${villa.description.substring(0, 80)}...</p>
                        
                        <div class="row mb-2">
                            <div class="col-6">
                                <div class="villa-price">${villa.price}€</div>
                                <small class="text-muted">par nuit</small>
                            </div>
                            <div class="col-6 text-end">
                                <small class="text-muted">
                                    <i class="fas fa-users me-1"></i>${villa.capacity} pers.
                                </small>
                                <br>
                                <small class="text-muted">
                                    <i class="fas fa-bed me-1"></i>${villa.bedrooms || 0} ch.
                                </small>
                            </div>
                        </div>

                        <!-- Amenities preview -->
                        <div class="mb-3">
                            <div class="d-flex flex-wrap gap-1">
                                ${(villa.amenities || []).slice(0, 4).map(amenity => 
                                    `<span class="badge bg-light text-dark">${this.getAmenityIcon(amenity)}</span>`
                                ).join('')}
                                ${villa.amenities && villa.amenities.length > 4 ? 
                                    `<span class="badge bg-secondary">+${villa.amenities.length - 4}</span>` : ''
                                }
                            </div>
                        </div>
                        
                        <div class="btn-group w-100" role="group">
                            <button class="btn btn-outline-primary btn-sm" onclick="app.editVilla(${villa.id})" title="Éditer">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn btn-outline-info btn-sm" onclick="app.previewVilla(${villa.id})" title="Aperçu">
                                <i class="fas fa-eye"></i>
                            </button>
                            <button class="btn btn-outline-success btn-sm" onclick="app.duplicateVilla(${villa.id})" title="Dupliquer">
                                <i class="fas fa-copy"></i>
                            </button>
                            <button class="btn btn-outline-danger btn-sm" onclick="app.deleteVilla(${villa.id})" title="Supprimer">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');
    }

    filterVillas() {
        const searchTerm = document.getElementById('villaSearch')?.value.toLowerCase() || '';
        const statusFilter = document.getElementById('statusFilter')?.value || '';
        const priceFilter = document.getElementById('priceFilter')?.value || '';

        let filteredVillas = this.villas.filter(villa => {
            const matchesSearch = villa.name.toLowerCase().includes(searchTerm) ||
                                villa.location.toLowerCase().includes(searchTerm) ||
                                villa.description.toLowerCase().includes(searchTerm);

            const matchesStatus = statusFilter === '' || villa.status === statusFilter;

            let matchesPrice = true;
            if (priceFilter) {
                if (priceFilter === '0-500') {
                    matchesPrice = villa.price >= 0 && villa.price < 500;
                } else if (priceFilter === '500-1000') {
                    matchesPrice = villa.price >= 500 && villa.price < 1000;
                } else if (priceFilter === '1000-1500') {
                    matchesPrice = villa.price >= 1000 && villa.price < 1500;
                } else if (priceFilter === '1500+') {
                    matchesPrice = villa.price >= 1500;
                }
            }

            return matchesSearch && matchesStatus && matchesPrice;
        });

        this.renderVillas(filteredVillas);
    }

    clearFilters() {
        document.getElementById('villaSearch').value = '';
        document.getElementById('statusFilter').value = '';
        document.getElementById('priceFilter').value = '';
        this.renderVillas(this.villas);
    }

    loadSettings() {
        document.getElementById('siteName').value = this.settings.siteName || '';
        document.getElementById('contactEmail').value = this.settings.contactEmail || '';
        document.getElementById('contactPhone').value = this.settings.contactPhone || '';
    }

    saveSettings() {
        this.settings = {
            ...this.settings,
            siteName: document.getElementById('siteName').value,
            contactEmail: document.getElementById('contactEmail').value,
            contactPhone: document.getElementById('contactPhone').value
        };
        
        this.saveData();
        this.showToast('Paramètres sauvegardés avec succès', 'success');
    }

    showToast(message, type = 'success') {
        const toastElement = document.getElementById(`${type}Toast`);
        const messageElement = document.getElementById(`${type}Message`);
        
        messageElement.textContent = message;
        
        const toast = new bootstrap.Toast(toastElement);
        toast.show();
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffTime = Math.abs(now - date);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        if (diffDays === 0) return "aujourd'hui";
        if (diffDays === 1) return "hier";
        if (diffDays < 7) return `il y a ${diffDays} jours`;
        return date.toLocaleDateString('fr-FR');
    }
}

// Global functions
function toggleSidebar() {
    document.querySelector('.sidebar').classList.toggle('show');
}

function logout() {
    if (confirm('Êtes-vous sûr de vouloir vous déconnecter ?')) {
        sessionStorage.removeItem('admin_access');
        window.location.href = 'login.html';
    }
}

function exportData() {
    const data = {
        villas: app.villas,
        settings: app.settings,
        exported: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `khanelconcept-data-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    app.showToast('Données exportées avec succès', 'success');
}

function importData() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.onchange = function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    const data = JSON.parse(e.target.result);
                    if (data.villas && data.settings) {
                        if (confirm('Cette action remplacera toutes les données actuelles. Continuer ?')) {
                            app.villas = data.villas;
                            app.settings = data.settings;
                            app.saveData();
                            app.updateDashboard();
                            app.loadVillasGrid();
                            app.loadSettings();
                            app.showToast('Données importées avec succès', 'success');
                        }
                    } else {
                        app.showToast('Format de fichier invalide', 'error');
                    }
                } catch (error) {
                    app.showToast('Erreur lors de la lecture du fichier', 'error');
                }
            };
            reader.readAsText(file);
        }
    };
    input.click();
}

function resetData() {
    if (confirm('Cette action supprimera toutes les données. Cette action est irréversible. Continuer ?')) {
        if (confirm('Êtes-vous absolument certain ? Toutes les villas et paramètres seront perdus.')) {
            // removeItem removed (API managed)
            // removeItem removed (API managed)
            location.reload();
        }
    }
}

// Initialize app when page loads
let app;
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM Content Loaded - Initializing admin app...");
    try {
        app = new AdminApp();
        console.log("Admin app initialized successfully");
        
        // Make app globally accessible for debugging
        window.app = app;
        
        // Initialize default villa data if empty
        if (!app.villas || app.villas.length === 0) {
            console.log("No villas found, loading default data...");
            app.villas = app.getDefaultVillas();
            app.saveData();
            app.updateDashboard();
            console.log("Default villas loaded:", app.villas.length);
        }
        
    } catch (error) {
        console.error("Error initializing admin app:", error);
    }
});