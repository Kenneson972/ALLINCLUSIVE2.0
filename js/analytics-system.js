
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
 * PHASE 4 - PERFORMANCE & RGPD : Système d'Analytics
 * Analytics respectueux de la vie privée avec conformité RGPD
 */

class AnalyticsSystem {
    constructor() {
        this.config = {
            enabled: false,
            respectDNT: true, // Respecter Do Not Track
            anonymizeIP: true,
            sessionTimeout: 30 * 60 * 1000, // 30 minutes
            batchSize: 10,
            batchTimeout: 5000,
            endpoint: '/api/analytics',
            localStorageKey: 'khanelconcept_analytics',
            enableRealtime: true,
            enableHeatmap: false,
            enableUserJourney: true
        };
        
        this.session = {
            id: null,
            startTime: null,
            lastActivity: null,
            pageViews: 0,
            events: [],
            userId: null,
            userRole: null,
            isAuthenticated: false
        };
        
        this.metrics = {
            performance: {
                loadTime: 0,
                domContentLoaded: 0,
                firstContentfulPaint: 0,
                largestContentfulPaint: 0,
                cumulativeLayoutShift: 0,
                firstInputDelay: 0
            },
            engagement: {
                timeOnPage: 0,
                scrollDepth: 0,
                clickCount: 0,
                formInteractions: 0,
                videoPlays: 0,
                downloadCount: 0
            },
            technical: {
                viewport: { width: 0, height: 0 },
                deviceType: null,
                browser: null,
                os: null,
                referrer: null,
                language: null,
                timezone: null
            }
        };
        
        this.eventQueue = [];
        this.batchTimer = null;
        this.observers = new Map();
        
        this.init();
    }

    init() {
        // Vérifier le consentement RGPD
        if (!this.checkGDPRConsent()) {
            this.setupGDPRListener();
            return;
        }
        
        // Vérifier Do Not Track
        if (this.config.respectDNT && navigator.doNotTrack === '1') {
            console.log('Analytics disabled: Do Not Track enabled');
            return;
        }
        
        this.config.enabled = true;
        this.setupSession();
        this.collectTechnicalData();
        this.setupEventListeners();
        this.startTracking();
    }

    checkGDPRConsent() {
        if (typeof window.gdprConsent !== 'undefined') {
            return window.gdprConsent.hasConsent('analytics');
        }
        
        // Fallback: vérifier localStorage
        const consent = localStorage.getItem('khanelconcept_consent');
        if (consent) {
            try {
                const data = JSON.parse(consent);
                return data.analytics === true;
            } catch (e) {
                return false;
            }
        }
        
        return false;
    }

    setupGDPRListener() {
        // Écouter les changements de consentement
        window.addEventListener('gdpr:analyticsEnabled', () => {
            this.config.enabled = true;
            this.init();
        });
        
        window.addEventListener('gdpr:analyticsDisabled', () => {
            this.config.enabled = false;
            this.cleanup();
        });
    }

    setupSession() {
        // Récupérer ou créer une session
        const existingSession = localStorage.getItem(this.config.localStorageKey);
        
        if (existingSession) {
            try {
                const sessionData = JSON.parse(existingSession);
                
                // Vérifier si la session est expirée
                if (Date.now() - sessionData.lastActivity < this.config.sessionTimeout) {
                    this.session = { ...this.session, ...sessionData };
                    this.session.lastActivity = Date.now();
                } else {
                    this.createNewSession();
                }
            } catch (e) {
                this.createNewSession();
            }
        } else {
            this.createNewSession();
        }
        
        // Récupérer les informations utilisateur si connecté
        this.updateUserInfo();
        
        // Sauvegarder la session
        this.saveSession();
    }

    createNewSession() {
        this.session = {
            id: this.generateSessionId(),
            startTime: Date.now(),
            lastActivity: Date.now(),
            pageViews: 0,
            events: [],
            userId: null,
            userRole: null,
            isAuthenticated: false
        };
    }

    generateSessionId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }

    updateUserInfo() {
        // Vérifier si l'utilisateur est connecté
        const token = localStorage.getItem('khanelconcept_token') || 
                     localStorage.getItem('khanelconcept_admin_token');
        
        if (token) {
            try {
                const payload = JSON.parse(atob(token.split('.')[1]));
                this.session.userId = this.config.anonymizeIP ? 
                    this.hashString(payload.sub) : payload.sub;
                this.session.userRole = payload.role || 'member';
                this.session.isAuthenticated = true;
            } catch (e) {
                this.session.isAuthenticated = false;
            }
        } else {
            this.session.isAuthenticated = false;
        }
    }

    collectTechnicalData() {
        this.metrics.technical = {
            viewport: {
                width: window.innerWidth,
                height: window.innerHeight
            },
            deviceType: this.getDeviceType(),
            browser: this.getBrowserInfo(),
            os: this.getOSInfo(),
            referrer: this.config.anonymizeIP ? 
                this.anonymizeURL(document.referrer) : document.referrer,
            language: navigator.language,
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
        };
    }

    getDeviceType() {
        const width = window.innerWidth;
        if (width < 768) return 'mobile';
        if (width < 1024) return 'tablet';
        return 'desktop';
    }

    getBrowserInfo() {
        const ua = navigator.userAgent;
        
        if (ua.includes('Firefox')) return 'Firefox';
        if (ua.includes('Chrome')) return 'Chrome';
        if (ua.includes('Safari')) return 'Safari';
        if (ua.includes('Edge')) return 'Edge';
        if (ua.includes('Opera')) return 'Opera';
        
        return 'Unknown';
    }

    getOSInfo() {
        const ua = navigator.userAgent;
        
        if (ua.includes('Windows')) return 'Windows';
        if (ua.includes('Mac')) return 'macOS';
        if (ua.includes('Linux')) return 'Linux';
        if (ua.includes('Android')) return 'Android';
        if (ua.includes('iOS')) return 'iOS';
        
        return 'Unknown';
    }

    setupEventListeners() {
        // Page view tracking
        this.trackPageView();
        
        // Performance tracking
        this.trackPerformance();
        
        // Engagement tracking
        this.trackEngagement();
        
        // Error tracking
        this.trackErrors();
        
        // Unload tracking
        this.trackUnload();
    }

    trackPageView() {
        const pageData = {
            type: 'pageview',
            timestamp: Date.now(),
            url: this.anonymizeURL(window.location.href),
            title: document.title,
            referrer: this.anonymizeURL(document.referrer),
            sessionId: this.session.id,
            userId: this.session.userId,
            userRole: this.session.userRole,
            isAuthenticated: this.session.isAuthenticated
        };
        
        this.session.pageViews++;
        this.queueEvent(pageData);
    }

    trackPerformance() {
        // Performance API
        if (window.performance) {
            const perfData = window.performance.getEntriesByType('navigation')[0];
            
            if (perfData) {
                this.metrics.performance = {
                    loadTime: perfData.loadEventEnd - perfData.loadEventStart,
                    domContentLoaded: perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart,
                    firstContentfulPaint: this.getFirstContentfulPaint(),
                    largestContentfulPaint: this.getLargestContentfulPaint(),
                    cumulativeLayoutShift: this.getCumulativeLayoutShift(),
                    firstInputDelay: this.getFirstInputDelay()
                };
            }
        }
        
        // Core Web Vitals
        if ('web-vital' in window) {
            this.trackWebVitals();
        }
    }

    getFirstContentfulPaint() {
        const fcpEntry = performance.getEntriesByName('first-contentful-paint')[0];
        return fcpEntry ? fcpEntry.startTime : 0;
    }

    getLargestContentfulPaint() {
        return new Promise((resolve) => {
            const observer = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                const lastEntry = entries[entries.length - 1];
                resolve(lastEntry.startTime);
            });
            
            observer.observe({ entryTypes: ['largest-contentful-paint'] });
            
            // Timeout après 10 secondes
            setTimeout(() => resolve(0), 10000);
        });
    }

    getCumulativeLayoutShift() {
        return new Promise((resolve) => {
            let clsValue = 0;
            
            const observer = new PerformanceObserver((list) => {
                for (const entry of list.getEntries()) {
                    if (!entry.hadRecentInput) {
                        clsValue += entry.value;
                    }
                }
            });
            
            observer.observe({ entryTypes: ['layout-shift'] });
            
            // Calculer CLS après 5 secondes
            setTimeout(() => {
                observer.disconnect();
                resolve(clsValue);
            }, 5000);
        });
    }

    getFirstInputDelay() {
        return new Promise((resolve) => {
            const observer = new PerformanceObserver((list) => {
                for (const entry of list.getEntries()) {
                    resolve(entry.processingStart - entry.startTime);
                    observer.disconnect();
                    return;
                }
            });
            
            observer.observe({ entryTypes: ['first-input'] });
            
            // Timeout après 10 secondes
            setTimeout(() => resolve(0), 10000);
        });
    }

    trackEngagement() {
        // Temps sur la page
        const startTime = Date.now();
        
        window.addEventListener('beforeunload', () => {
            this.metrics.engagement.timeOnPage = Date.now() - startTime;
        });
        
        // Scroll depth
        this.trackScrollDepth();
        
        // Clics
        this.trackClicks();
        
        // Interactions avec les formulaires
        this.trackFormInteractions();
        
        // Lectures vidéo
        this.trackVideoPlays();
        
        // Téléchargements
        this.trackDownloads();
    }

    trackScrollDepth() {
        let maxScrollDepth = 0;
        
        const updateScrollDepth = () => {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            const windowHeight = window.innerHeight;
            const documentHeight = document.documentElement.scrollHeight;
            
            const scrollDepth = Math.round(((scrollTop + windowHeight) / documentHeight) * 100);
            
            if (scrollDepth > maxScrollDepth) {
                maxScrollDepth = scrollDepth;
                this.metrics.engagement.scrollDepth = Math.min(maxScrollDepth, 100);
                
                // Événements de milestone
                if (scrollDepth >= 25 && scrollDepth < 50) {
                    this.queueEvent({
                        type: 'scroll_milestone',
                        milestone: 25,
                        timestamp: Date.now()
                    });
                } else if (scrollDepth >= 50 && scrollDepth < 75) {
                    this.queueEvent({
                        type: 'scroll_milestone',
                        milestone: 50,
                        timestamp: Date.now()
                    });
                } else if (scrollDepth >= 75 && scrollDepth < 100) {
                    this.queueEvent({
                        type: 'scroll_milestone',
                        milestone: 75,
                        timestamp: Date.now()
                    });
                } else if (scrollDepth >= 100) {
                    this.queueEvent({
                        type: 'scroll_milestone',
                        milestone: 100,
                        timestamp: Date.now()
                    });
                }
            }
        };
        
        window.addEventListener('scroll', this.throttle(updateScrollDepth, 100));
    }

    trackClicks() {
        document.addEventListener('click', (event) => {
            this.metrics.engagement.clickCount++;
            
            const target = event.target;
            const clickData = {
                type: 'click',
                timestamp: Date.now(),
                element: target.tagName.toLowerCase(),
                className: target.className,
                text: target.textContent ? target.textContent.substring(0, 100) : '',
                href: target.href || null,
                position: {
                    x: event.clientX,
                    y: event.clientY
                }
            };
            
            // Anonymiser les données sensibles
            if (this.config.anonymizeIP) {
                clickData.text = this.anonymizeText(clickData.text);
                clickData.href = this.anonymizeURL(clickData.href);
            }
            
            this.queueEvent(clickData);
        });
    }

    trackFormInteractions() {
        document.addEventListener('focus', (event) => {
            if (event.target.matches('input, textarea, select')) {
                this.metrics.engagement.formInteractions++;
                
                this.queueEvent({
                    type: 'form_interaction',
                    timestamp: Date.now(),
                    element: event.target.tagName.toLowerCase(),
                    inputType: event.target.type || 'text',
                    formId: event.target.form ? event.target.form.id : null
                });
            }
        });
        
        document.addEventListener('submit', (event) => {
            this.queueEvent({
                type: 'form_submit',
                timestamp: Date.now(),
                formId: event.target.id || null,
                formAction: this.anonymizeURL(event.target.action),
                formMethod: event.target.method || 'GET'
            });
        });
    }

    trackVideoPlays() {
        document.addEventListener('play', (event) => {
            if (event.target.tagName === 'VIDEO') {
                this.metrics.engagement.videoPlays++;
                
                this.queueEvent({
                    type: 'video_play',
                    timestamp: Date.now(),
                    videoSrc: this.anonymizeURL(event.target.src),
                    videoDuration: event.target.duration || 0
                });
            }
        });
    }

    trackDownloads() {
        document.addEventListener('click', (event) => {
            const target = event.target;
            
            if (target.tagName === 'A' && target.href) {
                const url = new URL(target.href, window.location.origin);
                const extension = url.pathname.split('.').pop().toLowerCase();
                
                const downloadExtensions = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar'];
                
                if (downloadExtensions.includes(extension)) {
                    this.metrics.engagement.downloadCount++;
                    
                    this.queueEvent({
                        type: 'download',
                        timestamp: Date.now(),
                        fileName: url.pathname.split('/').pop(),
                        fileType: extension,
                        fileUrl: this.anonymizeURL(target.href)
                    });
                }
            }
        });
    }

    trackErrors() {
        // Erreurs JavaScript
        window.addEventListener('error', (event) => {
            this.queueEvent({
                type: 'javascript_error',
                timestamp: Date.now(),
                message: event.message,
                filename: this.anonymizeURL(event.filename),
                line: event.lineno,
                column: event.colno,
                stack: event.error ? event.error.stack : null
            });
        });
        
        // Erreurs de ressources
        window.addEventListener('error', (event) => {
            if (event.target !== window) {
                this.queueEvent({
                    type: 'resource_error',
                    timestamp: Date.now(),
                    element: event.target.tagName,
                    source: this.anonymizeURL(event.target.src || event.target.href),
                    message: 'Resource failed to load'
                });
            }
        }, true);
        
        // Promesses rejetées
        window.addEventListener('unhandledrejection', (event) => {
            this.queueEvent({
                type: 'promise_rejection',
                timestamp: Date.now(),
                reason: event.reason ? event.reason.toString() : 'Unknown',
                stack: event.reason && event.reason.stack ? event.reason.stack : null
            });
        });
    }

    trackUnload() {
        window.addEventListener('beforeunload', () => {
            // Envoyer les données en attente
            this.flushEvents(true);
            
            // Enregistrer les métriques finales
            this.queueEvent({
                type: 'session_end',
                timestamp: Date.now(),
                sessionDuration: Date.now() - this.session.startTime,
                pageViews: this.session.pageViews,
                metrics: this.metrics
            });
            
            // Sauvegarder la session
            this.saveSession();
        });
    }

    queueEvent(eventData) {
        if (!this.config.enabled) return;
        
        // Ajouter les données communes
        const enrichedEvent = {
            ...eventData,
            sessionId: this.session.id,
            userId: this.session.userId,
            userRole: this.session.userRole,
            url: this.anonymizeURL(window.location.href),
            userAgent: this.config.anonymizeIP ? 
                this.anonymizeUserAgent(navigator.userAgent) : navigator.userAgent,
            technical: this.metrics.technical
        };
        
        this.eventQueue.push(enrichedEvent);
        
        // Traitement par batch
        if (this.eventQueue.length >= this.config.batchSize) {
            this.flushEvents();
        } else if (!this.batchTimer) {
            this.batchTimer = setTimeout(() => {
                this.flushEvents();
            }, this.config.batchTimeout);
        }
    }

    async flushEvents(force = false) {
        if (this.eventQueue.length === 0) return;
        
        const events = [...this.eventQueue];
        this.eventQueue = [];
        
        if (this.batchTimer) {
            clearTimeout(this.batchTimer);
            this.batchTimer = null;
        }
        
        try {
            if (force) {
                // Utiliser sendBeacon pour les envois synchrones
                if (navigator.sendBeacon) {
                    const blob = new Blob([JSON.stringify(events)], {
                        type: 'application/json'
                    });
                    navigator.sendBeacon(this.config.endpoint, blob);
                } else {
                    // Fallback pour les navigateurs plus anciens
                    const xhr = new XMLHttpRequest();
                    xhr.open('POST', this.config.endpoint, false);
                    xhr.setRequestHeader('Content-Type', 'application/json');
                    xhr.send(JSON.stringify(events));
                }
            } else {
                // Envoi asynchrone normal
                const response = await fetch(this.config.endpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('khanelconcept_token') || localStorage.getItem('khanelconcept_admin_token')}`
                    },
                    body: JSON.stringify(events)
                });
                
                if (!response.ok) {
                    throw new Error(`Analytics request failed: ${response.status}`);
                }
            }
        } catch (error) {
            console.warn('Analytics request failed:', error);
            
            // Remettre les événements en queue en cas d'échec
            if (!force) {
                this.eventQueue.unshift(...events);
            }
        }
    }

    saveSession() {
        if (!this.config.enabled) return;
        
        try {
            localStorage.setItem(this.config.localStorageKey, JSON.stringify(this.session));
        } catch (e) {
            console.warn('Could not save analytics session:', e);
        }
    }

    // Méthodes d'anonymisation
    anonymizeURL(url) {
        if (!url) return url;
        
        try {
            const parsedUrl = new URL(url, window.location.origin);
            
            // Supprimer les paramètres sensibles
            const sensitiveParams = ['token', 'key', 'password', 'email', 'phone', 'id'];
            
            sensitiveParams.forEach(param => {
                parsedUrl.searchParams.delete(param);
            });
            
            return parsedUrl.toString();
        } catch (e) {
            return url;
        }
    }

    anonymizeText(text) {
        if (!text) return text;
        
        // Supprimer les emails
        text = text.replace(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g, '[EMAIL]');
        
        // Supprimer les numéros de téléphone
        text = text.replace(/[\+]?[1-9]?[\-\s]?[\(]?[0-9]{1,3}[\)]?[\-\s]?[0-9]{1,4}[\-\s]?[0-9]{1,4}[\-\s]?[0-9]{1,9}/g, '[PHONE]');
        
        // Supprimer les numéros de carte de crédit
        text = text.replace(/[0-9]{4}[\-\s]?[0-9]{4}[\-\s]?[0-9]{4}[\-\s]?[0-9]{4}/g, '[CARD]');
        
        return text;
    }

    anonymizeUserAgent(userAgent) {
        // Conserver seulement les informations essentielles
        const parts = userAgent.split(' ');
        return parts.filter(part => 
            part.includes('Chrome/') || 
            part.includes('Firefox/') || 
            part.includes('Safari/') ||
            part.includes('Edge/')
        ).join(' ');
    }

    hashString(str) {
        let hash = 0;
        if (str.length === 0) return hash;
        
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // Convert to 32-bit integer
        }
        
        return hash.toString(36);
    }

    // Méthodes utilitaires
    throttle(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    startTracking() {
        if (!this.config.enabled) return;
        
        // Démarrer le tracking en temps réel si activé
        if (this.config.enableRealtime) {
            this.startRealtimeTracking();
        }
        
        // Mise à jour de l'activité
        this.updateActivity();
    }

    startRealtimeTracking() {
        // Envoyer des données en temps réel toutes les 30 secondes
        setInterval(() => {
            if (this.eventQueue.length > 0) {
                this.flushEvents();
            }
        }, 30000);
    }

    updateActivity() {
        // Mettre à jour l'activité utilisateur
        ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'].forEach(event => {
            document.addEventListener(event, () => {
                this.session.lastActivity = Date.now();
            }, true);
        });
        
        // Sauvegarder la session régulièrement
        setInterval(() => {
            this.saveSession();
        }, 60000); // Toutes les minutes
    }

    // Méthodes publiques
    trackCustomEvent(eventName, eventData = {}) {
        if (!this.config.enabled) return;
        
        this.queueEvent({
            type: 'custom_event',
            eventName: eventName,
            eventData: eventData,
            timestamp: Date.now()
        });
    }

    trackConversion(conversionType, value = 0, currency = 'EUR') {
        if (!this.config.enabled) return;
        
        this.queueEvent({
            type: 'conversion',
            conversionType: conversionType,
            value: value,
            currency: currency,
            timestamp: Date.now()
        });
    }

    setUserProperty(property, value) {
        if (!this.config.enabled) return;
        
        this.queueEvent({
            type: 'user_property',
            property: property,
            value: value,
            timestamp: Date.now()
        });
    }

    getSessionData() {
        return { ...this.session };
    }

    getMetrics() {
        return { ...this.metrics };
    }

    cleanup() {
        // Nettoyer les observers
        this.observers.forEach(observer => {
            if (observer.disconnect) {
                observer.disconnect();
            }
        });
        
        // Vider la queue
        this.eventQueue = [];
        
        // Arrêter les timers
        if (this.batchTimer) {
            clearTimeout(this.batchTimer);
            this.batchTimer = null;
        }
        
        // Supprimer les données locales
        localStorage.removeItem(this.config.localStorageKey);
        
        this.config.enabled = false;
    }

    configure(options) {
        this.config = { ...this.config, ...options };
    }
}

// Initialiser le système d'analytics
const analyticsSystem = new AnalyticsSystem();

// Exporter pour utilisation globale
window.AnalyticsSystem = analyticsSystem;
window.analytics = {
    track: (eventName, eventData) => analyticsSystem.trackCustomEvent(eventName, eventData),
    conversion: (type, value, currency) => analyticsSystem.trackConversion(type, value, currency),
    setUserProperty: (property, value) => analyticsSystem.setUserProperty(property, value),
    getSession: () => analyticsSystem.getSessionData(),
    getMetrics: () => analyticsSystem.getMetrics()
};

// Utilitaires pour les développeurs
window.analyticsDebug = {
    getSession: () => analyticsSystem.getSessionData(),
    getMetrics: () => analyticsSystem.getMetrics(),
    getQueue: () => analyticsSystem.eventQueue,
    flush: () => analyticsSystem.flushEvents(),
    cleanup: () => analyticsSystem.cleanup()
};