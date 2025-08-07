
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


/**
 * FETCHDATA.JS - Module ES6 pour couche pré-backend Jamstack
 * Compatible GitHub Pages avec fallback sur db.json local
 * 
 * Utilisation:
 * import { getVillas, getPrestataires, getEvents } from './fetchData.js';
 * 
 * @version 1.0.0
 * @author KhanelConcept
 */

// Configuration API avec fallback automatique
const API_CONFIG = {
    // En développement local: json-server sur port 3001
    development: 'http://localhost:3001',
    // En production GitHub Pages: fallback sur db.json
    production: './db.json',
    // Détection automatique de l'environnement
    current: window.location.hostname === 'localhost' ? 'development' : 'production'
};

// Cache pour optimiser les performances
const dataCache = new Map();
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

/**
 * Fonction utilitaire pour les requêtes HTTP avec gestion d'erreurs
 * @param {string} url - URL de la requête
 * @param {Object} options - Options fetch
 * @returns {Promise<Object>} - Données JSON ou erreur
 */
async function fetchWithFallback(url, options = {}) {
    try {
        const response = await fetch(url, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status} - ${response.statusText}`);
        }

        const data = await response.json();
        console.log(`✅ Données récupérées depuis: ${url}`);
        return data;

    } catch (error) {
        console.warn(`⚠️ Erreur API ${url}:`, error.message);
        
        // Fallback sur db.json local en cas d'erreur
        if (API_CONFIG.current === 'development') {
            console.log('🔄 Fallback vers db.json local...');
            try {
                const fallbackResponse = await fetch('./db.json');
                const fallbackData = await fallbackResponse.json();
                return fallbackData;
            } catch (fallbackError) {
                console.error('❌ Erreur fallback:', fallbackError);
                throw new Error('Impossible de charger les données');
            }
        }
        
        throw error;
    }
}

/**
 * Récupère les données depuis le cache ou l'API
 * @param {string} key - Clé de cache
 * @param {Function} fetchFunction - Fonction de récupération
 * @returns {Promise<Object>} - Données mises en cache
 */
async function getCachedData(key, fetchFunction) {
    const cached = dataCache.get(key);
    const now = Date.now();
    
    if (cached && (now - cached.timestamp) < CACHE_DURATION) {
        console.log(`🚀 Données en cache pour: ${key}`);
        return cached.data;
    }
    
    const data = await fetchFunction();
    dataCache.set(key, {
        data,
        timestamp: now
    });
    
    return data;
}

/**
 * VILLAS - Récupère toutes les villas avec options de filtrage
 * @param {Object} filters - Filtres optionnels
 * @returns {Promise<Array>} - Liste des villas
 */
export async function getVillas(filters = {}) {
    console.log('🏖️ Récupération des villas...', filters);
    
    return getCachedData('villas', async () => {
        const baseUrl = API_CONFIG.current === 'development' 
            ? API_CONFIG.development 
            : API_CONFIG.production;
        
        if (API_CONFIG.current === 'development') {
            // Mode développement: utilise json-server avec requêtes
            let url = `${baseUrl}/villas`;
            const params = new URLSearchParams();
            
            // Filtres supportés par json-server
            if (filters.category) params.append('category', filters.category);
            if (filters.location) params.append('location_like', filters.location);
            if (filters.min_price) params.append('price_gte', filters.min_price);
            if (filters.max_price) params.append('price_lte', filters.max_price);
            if (filters.guests) params.append('guests_gte', filters.guests);
            
            if (params.toString()) url += `?${params.toString()}`;
            
            const data = await fetchWithFallback(url);
            return data;
            
        } else {
            // Mode production: charge db.json et filtre côté client
            const data = await fetchWithFallback(baseUrl);
            let villas = data.villas || [];
            
            // Filtrage côté client pour GitHub Pages
            if (filters.category) {
                villas = villas.filter(villa => villa.category === filters.category);
            }
            if (filters.location) {
                villas = villas.filter(villa => 
                    villa.location.toLowerCase().includes(filters.location.toLowerCase())
                );
            }
            if (filters.min_price) {
                villas = villas.filter(villa => villa.price >= filters.min_price);
            }
            if (filters.max_price) {
                villas = villas.filter(villa => villa.price <= filters.max_price);
            }
            if (filters.guests) {
                villas = villas.filter(villa => villa.guests >= filters.guests);
            }
            
            return villas;
        }
    });
}

/**
 * VILLA BY ID - Récupère une villa spécifique
 * @param {string} id - ID de la villa
 * @returns {Promise<Object>} - Données de la villa
 */
export async function getVillaById(id) {
    console.log(`🏡 Récupération villa ID: ${id}`);
    
    const baseUrl = API_CONFIG.current === 'development' 
        ? API_CONFIG.development 
        : API_CONFIG.production;
    
    if (API_CONFIG.current === 'development') {
        const data = await fetchWithFallback(`${baseUrl}/villas/${id}`);
        return data;
    } else {
        const data = await fetchWithFallback(baseUrl);
        const villa = data.villas?.find(v => v.id === id);
        if (!villa) throw new Error(`Villa ${id} non trouvée`);
        return villa;
    }
}

/**
 * PRESTATAIRES - Récupère tous les prestataires avec options de filtrage
 * @param {Object} filters - Filtres optionnels
 * @returns {Promise<Array>} - Liste des prestataires
 */
export async function getPrestataires(filters = {}) {
    console.log('🤝 Récupération des prestataires...', filters);
    
    return getCachedData('prestataires', async () => {
        const baseUrl = API_CONFIG.current === 'development' 
            ? API_CONFIG.development 
            : API_CONFIG.production;
        
        if (API_CONFIG.current === 'development') {
            let url = `${baseUrl}/prestataires`;
            const params = new URLSearchParams();
            
            if (filters.category) params.append('category', filters.category);
            if (filters.location) params.append('location_like', filters.location);
            if (filters.verified) params.append('verified', filters.verified);
            
            if (params.toString()) url += `?${params.toString()}`;
            
            const data = await fetchWithFallback(url);
            return data;
            
        } else {
            const data = await fetchWithFallback(baseUrl);
            let prestataires = data.prestataires || [];
            
            // Filtrage côté client
            if (filters.category) {
                prestataires = prestataires.filter(p => p.category === filters.category);
            }
            if (filters.location) {
                prestataires = prestataires.filter(p => 
                    p.location.toLowerCase().includes(filters.location.toLowerCase())
                );
            }
            if (filters.verified !== undefined) {
                prestataires = prestataires.filter(p => p.verified === filters.verified);
            }
            
            return prestataires;
        }
    });
}

/**
 * EVENTS - Récupère tous les événements avec options de filtrage
 * @param {Object} filters - Filtres optionnels
 * @returns {Promise<Array>} - Liste des événements
 */
export async function getEvents(filters = {}) {
    console.log('🎉 Récupération des événements...', filters);
    
    return getCachedData('events', async () => {
        const baseUrl = API_CONFIG.current === 'development' 
            ? API_CONFIG.development 
            : API_CONFIG.production;
        
        if (API_CONFIG.current === 'development') {
            let url = `${baseUrl}/events`;
            const params = new URLSearchParams();
            
            if (filters.category) params.append('category', filters.category);
            if (filters.date) params.append('date', filters.date);
            if (filters.available) params.append('available_gte', 1);
            
            if (params.toString()) url += `?${params.toString()}`;
            
            const data = await fetchWithFallback(url);
            return data;
            
        } else {
            const data = await fetchWithFallback(baseUrl);
            let events = data.events || [];
            
            // Filtrage côté client
            if (filters.category) {
                events = events.filter(e => e.category === filters.category);
            }
            if (filters.date) {
                events = events.filter(e => e.date === filters.date);
            }
            if (filters.available) {
                events = events.filter(e => e.available > 0);
            }
            
            // Tri par date
            events.sort((a, b) => new Date(a.date) - new Date(b.date));
            
            return events;
        }
    });
}

/**
 * HEALTH CHECK - Vérifie la santé de l'API
 * @returns {Promise<Object>} - Statut de l'API
 */
export async function getHealth() {
    console.log('🏥 Vérification santé API...');
    
    const baseUrl = API_CONFIG.current === 'development' 
        ? API_CONFIG.development 
        : API_CONFIG.production;
    
    if (API_CONFIG.current === 'development') {
        const data = await fetchWithFallback(`${baseUrl}/health`);
        return data;
    } else {
        const data = await fetchWithFallback(baseUrl);
        return data.health || {
            status: "OK",
            timestamp: new Date().toISOString(),
            mode: "static"
        };
    }
}

/**
 * STATS - Récupère les statistiques générales
 * @returns {Promise<Object>} - Statistiques
 */
export async function getStats() {
    console.log('📊 Récupération des statistiques...');
    
    const baseUrl = API_CONFIG.current === 'development' 
        ? API_CONFIG.development 
        : API_CONFIG.production;
    
    if (API_CONFIG.current === 'development') {
        const data = await fetchWithFallback(`${baseUrl}/stats`);
        return data;
    } else {
        const data = await fetchWithFallback(baseUrl);
        return data.stats || {
            total_villas: data.villas?.length || 0,
            total_prestataires: data.prestataires?.length || 0,
            total_events: data.events?.length || 0
        };
    }
}

/**
 * CLEAR CACHE - Vide le cache des données
 */
export function clearCache() {
    console.log('🗑️ Vidage du cache...');
    dataCache.clear();
}

/**
 * GET CONFIG - Récupère la configuration actuelle
 * @returns {Object} - Configuration API
 */
export function getApiConfig() {
    return {
        ...API_CONFIG,
        cacheSize: dataCache.size,
        cacheDuration: CACHE_DURATION
    };
}

// Export par défaut pour compatibilité
export default {
    getVillas,
    getVillaById,
    getPrestataires,
    getEvents,
    getHealth,
    getStats,
    clearCache,
    getApiConfig
};

// Message de démarrage
console.log('🚀 Module fetchData.js initialisé');
console.log(`📍 Environnement: ${API_CONFIG.current}`);
console.log(`🔗 Base URL: ${API_CONFIG.current === 'development' ? API_CONFIG.development : API_CONFIG.production}`);