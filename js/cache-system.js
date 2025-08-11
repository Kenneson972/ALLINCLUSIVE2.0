/**
 * PHASE 4 - PERFORMANCE & RGPD : Système de Cache Intelligent
 * Cache avancé avec TTL, invalidation et compression
 */

class CacheSystem {
    constructor() {
        this.cache = new Map();
        this.config = {
            maxSize: 100, // Nombre maximum d'entrées
            defaultTTL: 5 * 60 * 1000, // 5 minutes par défaut
            cleanupInterval: 60 * 1000, // Nettoyage toutes les minutes
            compression: true,
            enablePersistence: true
        };
        
        // Stratégies de cache
        this.strategies = {
            'static': 24 * 60 * 60 * 1000, // 24 heures pour contenu statique
            'dynamic': 5 * 60 * 1000,      // 5 minutes pour contenu dynamique
            'user': 15 * 60 * 1000,        // 15 minutes pour données utilisateur
            'admin': 2 * 60 * 1000,        // 2 minutes pour données admin
            'realtime': 30 * 1000          // 30 secondes pour temps réel
        };
        
        // Métriques de performance
        this.metrics = {
            hits: 0,
            misses: 0,
            writes: 0,
            evictions: 0,
            startTime: Date.now()
        };
        
        this.init();
    }

    init() {
        // Démarrer le nettoyage automatique
        this.startCleanup();
        
        // Charger le cache persistant
        this.loadPersistentCache();
        
        // Écouter les événements de déchargement pour sauvegarder
        window.addEventListener('beforeunload', () => {
            this.savePersistentCache();
        });
        
        // Écouter les changements de visibilité
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.savePersistentCache();
            }
        });
    }

    /**
     * Récupérer une valeur du cache
     * @param {string} key - Clé de cache
     * @returns {*} - Valeur ou null si expirée/inexistante
     */
    get(key) {
        const entry = this.cache.get(key);
        
        if (!entry) {
            this.metrics.misses++;
            return null;
        }
        
        // Vérifier l'expiration
        if (Date.now() > entry.expiresAt) {
            this.cache.delete(key);
            this.metrics.misses++;
            return null;
        }
        
        // Mettre à jour le dernier accès
        entry.lastAccess = Date.now();
        this.metrics.hits++;
        
        // Décompresser si nécessaire
        return this.decompress(entry.data);
    }

    /**
     * Stocker une valeur dans le cache
     * @param {string} key - Clé de cache
     * @param {*} value - Valeur à stocker
     * @param {string|number} ttl - TTL ou stratégie
     */
    set(key, value, ttl = 'dynamic') {
        // Déterminer le TTL
        let expirationTime;
        if (typeof ttl === 'number') {
            expirationTime = Date.now() + ttl;
        } else {
            expirationTime = Date.now() + (this.strategies[ttl] || this.config.defaultTTL);
        }
        
        // Créer l'entrée de cache
        const entry = {
            data: this.compress(value),
            expiresAt: expirationTime,
            createdAt: Date.now(),
            lastAccess: Date.now(),
            strategy: ttl,
            size: this.getSize(value)
        };
        
        // Vérifier la taille maximale
        if (this.cache.size >= this.config.maxSize) {
            this.evictLRU();
        }
        
        this.cache.set(key, entry);
        this.metrics.writes++;
    }

    /**
     * Méthode avec pattern async/await pour les requêtes
     * @param {string} key - Clé de cache
     * @param {Function} fetchFn - Fonction de récupération des données
     * @param {string|number} ttl - TTL ou stratégie
     * @returns {Promise<*>} - Données depuis cache ou API
     */
    async getOrSet(key, fetchFn, ttl = 'dynamic') {
        let data = this.get(key);
        
        if (data !== null) {
            return data;
        }
        
        try {
            data = await fetchFn();
            this.set(key, data, ttl);
            return data;
        } catch (error) {
            console.error('Cache fetch error:', error);
            throw error;
        }
    }

    /**
     * Invalidation ciblée du cache
     * @param {string|RegExp} pattern - Pattern ou clé exacte
     */
    invalidate(pattern) {
        if (typeof pattern === 'string') {
            this.cache.delete(pattern);
        } else if (pattern instanceof RegExp) {
            for (const key of this.cache.keys()) {
                if (pattern.test(key)) {
                    this.cache.delete(key);
                }
            }
        }
    }

    /**
     * Invalidation par tags
     * @param {string} tag - Tag à invalider
     */
    invalidateTag(tag) {
        this.invalidate(new RegExp(`^${tag}:`));
    }

    /**
     * Éviction LRU (Least Recently Used)
     */
    evictLRU() {
        let oldestKey = null;
        let oldestTime = Infinity;
        
        for (const [key, entry] of this.cache.entries()) {
            if (entry.lastAccess < oldestTime) {
                oldestTime = entry.lastAccess;
                oldestKey = key;
            }
        }
        
        if (oldestKey) {
            this.cache.delete(oldestKey);
            this.metrics.evictions++;
        }
    }

    /**
     * Nettoyage des entrées expirées
     */
    cleanup() {
        const now = Date.now();
        let cleanedCount = 0;
        
        for (const [key, entry] of this.cache.entries()) {
            if (now > entry.expiresAt) {
                this.cache.delete(key);
                cleanedCount++;
            }
        }
        
        return cleanedCount;
    }

    /**
     * Démarrer le nettoyage automatique
     */
    startCleanup() {
        setInterval(() => {
            this.cleanup();
        }, this.config.cleanupInterval);
    }

    /**
     * Compression des données (simple)
     * @param {*} data - Données à compresser
     * @returns {*} - Données compressées ou originales
     */
    compress(data) {
        if (!this.config.compression) return data;
        
        // Compression simple pour les objets JSON
        if (typeof data === 'object' && data !== null) {
            try {
                const jsonString = JSON.stringify(data);
                // Simulation de compression (en production, utiliser une vraie lib)
                return {
                    __compressed: true,
                    data: jsonString
                };
            } catch (e) {
                return data;
            }
        }
        
        return data;
    }

    /**
     * Décompression des données
     * @param {*} data - Données potentiellement compressées
     * @returns {*} - Données décompressées
     */
    decompress(data) {
        if (data && typeof data === 'object' && data.__compressed) {
            try {
                return JSON.parse(data.data);
            } catch (e) {
                return data;
            }
        }
        
        return data;
    }

    /**
     * Calculer la taille approximative d'un objet
     * @param {*} obj - Objet à mesurer
     * @returns {number} - Taille en octets
     */
    getSize(obj) {
        let size = 0;
        
        if (typeof obj === 'string') {
            size = obj.length * 2; // Unicode = 2 bytes par caractère
        } else if (typeof obj === 'object' && obj !== null) {
            size = JSON.stringify(obj).length * 2;
        } else {
            size = 8; // Estimation pour les primitives
        }
        
        return size;
    }

    /**
     * Sauvegarder le cache dans localStorage
     */
    savePersistentCache() {
        if (!this.config.enablePersistence) return;
        
        try {
            const cacheData = {
                entries: Array.from(this.cache.entries()),
                timestamp: Date.now()
            };
            
            localStorage.setItem('khanelconcept_cache', JSON.stringify(cacheData));
        } catch (error) {
            console.warn('Could not save cache to localStorage:', error);
        }
    }

    /**
     * Charger le cache depuis localStorage
     */
    loadPersistentCache() {
        if (!this.config.enablePersistence) return;
        
        try {
            const savedData = localStorage.getItem('khanelconcept_cache');
            if (!savedData) return;
            
            const cacheData = JSON.parse(savedData);
            const now = Date.now();
            
            // Vérifier que les données ne sont pas trop anciennes (24h max)
            if (now - cacheData.timestamp > 24 * 60 * 60 * 1000) {
                localStorage.removeItem('khanelconcept_cache');
                return;
            }
            
            // Restaurer les entrées valides
            for (const [key, entry] of cacheData.entries) {
                if (now < entry.expiresAt) {
                    this.cache.set(key, entry);
                }
            }
        } catch (error) {
            console.warn('Could not load cache from localStorage:', error);
        }
    }

    /**
     * Obtenir les statistiques du cache
     * @returns {Object} - Statistiques détaillées
     */
    getStats() {
        const totalRequests = this.metrics.hits + this.metrics.misses;
        const hitRate = totalRequests > 0 ? (this.metrics.hits / totalRequests) * 100 : 0;
        const uptime = Date.now() - this.metrics.startTime;
        
        return {
            size: this.cache.size,
            maxSize: this.config.maxSize,
            hits: this.metrics.hits,
            misses: this.metrics.misses,
            writes: this.metrics.writes,
            evictions: this.metrics.evictions,
            hitRate: hitRate.toFixed(2) + '%',
            uptime: Math.floor(uptime / 1000) + 's',
            memoryUsage: this.getMemoryUsage()
        };
    }

    /**
     * Calculer l'utilisation mémoire
     * @returns {Object} - Utilisation mémoire
     */
    getMemoryUsage() {
        let totalSize = 0;
        let entryCount = 0;
        
        for (const [key, entry] of this.cache.entries()) {
            totalSize += entry.size || 0;
            entryCount++;
        }
        
        return {
            totalSize: totalSize,
            averageSize: entryCount > 0 ? Math.round(totalSize / entryCount) : 0,
            entries: entryCount
        };
    }

    /**
     * Vider complètement le cache
     */
    clear() {
        this.cache.clear();
        this.metrics = {
            hits: 0,
            misses: 0,
            writes: 0,
            evictions: 0,
            startTime: Date.now()
        };
        
        if (this.config.enablePersistence) {
            localStorage.removeItem('khanelconcept_cache');
        }
    }

    /**
     * Configurer le cache
     * @param {Object} options - Options de configuration
     */
    configure(options) {
        this.config = { ...this.config, ...options };
    }
}

// Wrapper pour les requêtes API avec cache
class CachedAPIClient {
    constructor(baseURL, cacheSystem) {
        this.baseURL = baseURL;
        this.cache = cacheSystem;
        this.defaultHeaders = {
            'Content-Type': 'application/json'
        };
    }

    /**
     * Requête GET avec cache
     * @param {string} endpoint - Endpoint API
     * @param {Object} options - Options de requête
     * @returns {Promise<*>} - Données depuis cache ou API
     */
    async get(endpoint, options = {}) {
        const { 
            cache = 'dynamic',
            headers = {},
            ignoreCache = false,
            ...fetchOptions 
        } = options;
        
        const cacheKey = this.generateCacheKey('GET', endpoint, fetchOptions);
        
        if (!ignoreCache) {
            const cachedData = this.cache.get(cacheKey);
            if (cachedData) {
                return cachedData;
            }
        }
        
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                method: 'GET',
                headers: { ...this.defaultHeaders, ...headers },
                ...fetchOptions
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Mettre en cache seulement les réponses réussies
            if (response.status === 200) {
                this.cache.set(cacheKey, data, cache);
            }
            
            return data;
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    /**
     * Requête POST (invalide le cache)
     * @param {string} endpoint - Endpoint API
     * @param {*} data - Données à envoyer
     * @param {Object} options - Options de requête
     * @returns {Promise<*>} - Réponse API
     */
    async post(endpoint, data, options = {}) {
        const { headers = {}, invalidateCache = [], ...fetchOptions } = options;
        
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                method: 'POST',
                headers: { ...this.defaultHeaders, ...headers },
                body: JSON.stringify(data),
                ...fetchOptions
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            
            // Invalider le cache après modification
            if (invalidateCache.length > 0) {
                invalidateCache.forEach(pattern => {
                    this.cache.invalidate(pattern);
                });
            }
            
            return result;
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    /**
     * Requête PUT (invalide le cache)
     * @param {string} endpoint - Endpoint API
     * @param {*} data - Données à envoyer
     * @param {Object} options - Options de requête
     * @returns {Promise<*>} - Réponse API
     */
    async put(endpoint, data, options = {}) {
        const { headers = {}, invalidateCache = [], ...fetchOptions } = options;
        
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                method: 'PUT',
                headers: { ...this.defaultHeaders, ...headers },
                body: JSON.stringify(data),
                ...fetchOptions
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            
            // Invalider le cache après modification
            if (invalidateCache.length > 0) {
                invalidateCache.forEach(pattern => {
                    this.cache.invalidate(pattern);
                });
            }
            
            return result;
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    /**
     * Requête DELETE (invalide le cache)
     * @param {string} endpoint - Endpoint API
     * @param {Object} options - Options de requête
     * @returns {Promise<*>} - Réponse API
     */
    async delete(endpoint, options = {}) {
        const { headers = {}, invalidateCache = [], ...fetchOptions } = options;
        
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                method: 'DELETE',
                headers: { ...this.defaultHeaders, ...headers },
                ...fetchOptions
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            
            // Invalider le cache après suppression
            if (invalidateCache.length > 0) {
                invalidateCache.forEach(pattern => {
                    this.cache.invalidate(pattern);
                });
            }
            
            return result;
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    /**
     * Générer une clé de cache unique
     * @param {string} method - Méthode HTTP
     * @param {string} endpoint - Endpoint API
     * @param {Object} options - Options de requête
     * @returns {string} - Clé de cache
     */
    generateCacheKey(method, endpoint, options = {}) {
        const optionsStr = JSON.stringify(options);
        return `${method}:${endpoint}:${btoa(optionsStr)}`;
    }

    /**
     * Ajouter un token d'authentification
     * @param {string} token - Token JWT
     */
    setAuthToken(token) {
        if (token) {
            this.defaultHeaders['Authorization'] = `Bearer ${token}`;
        } else {
            delete this.defaultHeaders['Authorization'];
        }
    }
}

// Initialiser le système de cache
const cacheSystem = new CacheSystem();

// Configurer pour l'environnement de production
cacheSystem.configure({
    maxSize: 200,
    defaultTTL: 10 * 60 * 1000, // 10 minutes
    compression: true,
    enablePersistence: true
});

// Créer le client API avec cache
const backendUrl = window.location.hostname === 'localhost' 
    ? 'http://localhost:8001'
    : 'https://d2494b70-f384-45ab-b3ca-ec242a606843.preview.emergentagent.com';

const apiClient = new CachedAPIClient(backendUrl, cacheSystem);

// Configurer le token d'authentification au chargement
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('khanelconcept_token') || 
                  localStorage.getItem('khanelconcept_admin_token');
    if (token) {
        apiClient.setAuthToken(token);
    }
});

// Exporter pour utilisation globale
window.CacheSystem = cacheSystem;
window.ApiClient = apiClient;

// Utilitaires pour les développeurs
window.cacheDebug = {
    stats: () => cacheSystem.getStats(),
    clear: () => cacheSystem.clear(),
    get: (key) => cacheSystem.get(key),
    invalidate: (pattern) => cacheSystem.invalidate(pattern)
};