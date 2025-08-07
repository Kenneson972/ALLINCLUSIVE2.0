
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
 * PHASE 3 - UX/UI : Système de Notifications Temps Réel
 * Notifications interactives, accessibles et élégantes
 */

class NotificationSystem {
    constructor() {
        this.notifications = new Map();
        this.queue = [];
        this.maxNotifications = 5;
        this.defaultDuration = 5000;
        this.positions = {
            'top-right': { top: '20px', right: '20px' },
            'top-left': { top: '20px', left: '20px' },
            'bottom-right': { bottom: '20px', right: '20px' },
            'bottom-left': { bottom: '20px', left: '20px' },
            'top-center': { top: '20px', left: '50%', transform: 'translateX(-50%)' },
            'bottom-center': { bottom: '20px', left: '50%', transform: 'translateX(-50%)' }
        };
        this.position = 'top-right';
        this.soundEnabled = true;
        this.animationDuration = 300;
        
        this.init();
    }

    init() {
        this.createContainer();
        this.injectStyles();
        this.setupEventListeners();
        this.loadUserPreferences();
    }

    createContainer() {
        if (document.getElementById('notification-container')) return;

        const container = document.createElement('div');
        container.id = 'notification-container';
        container.className = 'notification-container';
        container.setAttribute('aria-live', 'polite');
        container.setAttribute('aria-atomic', 'false');
        container.style.position = 'fixed';
        container.style.zIndex = '9999';
        container.style.pointerEvents = 'none';
        
        this.setPosition(this.position);
        document.body.appendChild(container);
    }

    injectStyles() {
        const styles = `
            <style id="notification-system-styles">
                /* PHASE 3 - Système de notifications */
                .notification-container {
                    max-width: 400px;
                    transition: all 0.3s ease;
                }

                .notification {
                    background: rgba(255, 255, 255, 0.95);
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 16px;
                    padding: 1rem 1.5rem;
                    margin-bottom: 0.75rem;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                    transform: translateX(100%);
                    opacity: 0;
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                    pointer-events: auto;
                    position: relative;
                    overflow: hidden;
                    min-height: 60px;
                    display: flex;
                    align-items: center;
                    gap: 1rem;
                    cursor: pointer;
                }

                .notification.show {
                    transform: translateX(0);
                    opacity: 1;
                }

                .notification.hide {
                    transform: translateX(100%);
                    opacity: 0;
                    margin-bottom: 0;
                    padding-top: 0;
                    padding-bottom: 0;
                    min-height: 0;
                }

                /* Types de notifications */
                .notification.success {
                    border-left: 4px solid #10b981;
                }

                .notification.error {
                    border-left: 4px solid #ef4444;
                }

                .notification.warning {
                    border-left: 4px solid #f59e0b;
                }

                .notification.info {
                    border-left: 4px solid #3b82f6;
                }

                /* Icônes */
                .notification-icon {
                    font-size: 1.5rem;
                    width: 2rem;
                    height: 2rem;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border-radius: 50%;
                    flex-shrink: 0;
                }

                .notification.success .notification-icon {
                    color: #10b981;
                    background: rgba(16, 185, 129, 0.1);
                }

                .notification.error .notification-icon {
                    color: #ef4444;
                    background: rgba(239, 68, 68, 0.1);
                }

                .notification.warning .notification-icon {
                    color: #f59e0b;
                    background: rgba(245, 158, 11, 0.1);
                }

                .notification.info .notification-icon {
                    color: #3b82f6;
                    background: rgba(59, 130, 246, 0.1);
                }

                /* Contenu */
                .notification-content {
                    flex: 1;
                    min-width: 0;
                }

                .notification-title {
                    font-weight: 600;
                    font-size: 0.95rem;
                    color: #1f2937;
                    margin-bottom: 0.25rem;
                    line-height: 1.2;
                }

                .notification-message {
                    font-size: 0.875rem;
                    color: #6b7280;
                    line-height: 1.4;
                    word-wrap: break-word;
                }

                /* Actions */
                .notification-actions {
                    display: flex;
                    gap: 0.5rem;
                    margin-top: 0.5rem;
                }

                .notification-action {
                    padding: 0.25rem 0.75rem;
                    border: 1px solid #e5e7eb;
                    border-radius: 6px;
                    background: white;
                    color: #374151;
                    font-size: 0.8rem;
                    cursor: pointer;
                    transition: all 0.2s ease;
                }

                .notification-action:hover {
                    background: #f9fafb;
                    border-color: #d1d5db;
                }

                .notification-action.primary {
                    background: #3b82f6;
                    color: white;
                    border-color: #3b82f6;
                }

                .notification-action.primary:hover {
                    background: #2563eb;
                }

                /* Bouton de fermeture */
                .notification-close {
                    position: absolute;
                    top: 0.5rem;
                    right: 0.5rem;
                    width: 1.5rem;
                    height: 1.5rem;
                    border: none;
                    background: none;
                    color: #9ca3af;
                    cursor: pointer;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    transition: all 0.2s ease;
                    font-size: 0.9rem;
                }

                .notification-close:hover {
                    background: rgba(156, 163, 175, 0.1);
                    color: #6b7280;
                }

                .notification-close:focus {
                    outline: 2px solid #3b82f6;
                    outline-offset: 2px;
                }

                /* Barre de progression */
                .notification-progress {
                    position: absolute;
                    bottom: 0;
                    left: 0;
                    height: 3px;
                    background: linear-gradient(90deg, #3b82f6, #8b5cf6);
                    border-radius: 0 0 16px 16px;
                    transform-origin: left;
                    animation: notificationProgress linear;
                }

                @keyframes notificationProgress {
                    from {
                        transform: scaleX(1);
                    }
                    to {
                        transform: scaleX(0);
                    }
                }

                /* Notifications avec image */
                .notification-image {
                    width: 3rem;
                    height: 3rem;
                    border-radius: 8px;
                    object-fit: cover;
                    flex-shrink: 0;
                }

                /* Animations d'entrée alternatives */
                .notification.slide-down {
                    transform: translateY(-100%);
                }

                .notification.slide-down.show {
                    transform: translateY(0);
                }

                .notification.slide-up {
                    transform: translateY(100%);
                }

                .notification.slide-up.show {
                    transform: translateY(0);
                }

                .notification.fade-in {
                    transform: scale(0.8);
                }

                .notification.fade-in.show {
                    transform: scale(1);
                }

                .notification.bounce-in {
                    transform: scale(0.3);
                }

                .notification.bounce-in.show {
                    transform: scale(1);
                    animation: bounceIn 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
                }

                @keyframes bounceIn {
                    0% {
                        transform: scale(0.3);
                    }
                    50% {
                        transform: scale(1.05);
                    }
                    70% {
                        transform: scale(0.9);
                    }
                    100% {
                        transform: scale(1);
                    }
                }

                /* Responsive */
                @media (max-width: 480px) {
                    .notification-container {
                        max-width: calc(100vw - 40px);
                        left: 20px !important;
                        right: 20px !important;
                        transform: none !important;
                    }

                    .notification {
                        padding: 0.75rem 1rem;
                        font-size: 0.875rem;
                    }

                    .notification-icon {
                        width: 1.5rem;
                        height: 1.5rem;
                        font-size: 1rem;
                    }
                }

                /* Thème sombre */
                .notification.dark {
                    background: rgba(31, 41, 55, 0.95);
                    border: 1px solid rgba(75, 85, 99, 0.3);
                    color: white;
                }

                .notification.dark .notification-title {
                    color: white;
                }

                .notification.dark .notification-message {
                    color: #d1d5db;
                }

                .notification.dark .notification-close {
                    color: #d1d5db;
                }

                .notification.dark .notification-close:hover {
                    background: rgba(209, 213, 219, 0.1);
                    color: white;
                }

                /* Accessibility */
                .notification:focus {
                    outline: 2px solid #3b82f6;
                    outline-offset: 2px;
                }

                /* Reduced motion */
                @media (prefers-reduced-motion: reduce) {
                    .notification {
                        transition: opacity 0.2s ease;
                    }
                    
                    .notification-progress {
                        animation: none;
                    }
                }

                /* High contrast */
                @media (prefers-contrast: high) {
                    .notification {
                        border: 2px solid #000;
                        background: #fff;
                    }
                    
                    .notification-title {
                        color: #000;
                    }
                    
                    .notification-message {
                        color: #000;
                    }
                }
            </style>
        `;
        
        if (!document.getElementById('notification-system-styles')) {
            document.head.insertAdjacentHTML('beforeend', styles);
        }
    }

    setupEventListeners() {
        // Écouter les changements de préférences utilisateur
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.pauseAllTimers();
            } else {
                this.resumeAllTimers();
            }
        });

        // Écouter les événements de focus/blur pour la navigation clavier
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.dismissAll();
            }
        });
    }

    loadUserPreferences() {
        // Charger les préférences depuis localStorage
        const prefs = localStorage.getItem('notification-preferences');
        if (prefs) {
            try {
                const preferences = JSON.parse(prefs);
                this.position = preferences.position || 'top-right';
                this.soundEnabled = preferences.soundEnabled !== false;
                this.setPosition(this.position);
            } catch (e) {
                console.warn('Could not load notification preferences:', e);
            }
        }
    }

    saveUserPreferences() {
        const preferences = {
            position: this.position,
            soundEnabled: this.soundEnabled
        };
        localStorage.setItem('notification-preferences', JSON.stringify(preferences));
    }

    setPosition(position) {
        this.position = position;
        const container = document.getElementById('notification-container');
        if (container && this.positions[position]) {
            const pos = this.positions[position];
            Object.assign(container.style, pos);
        }
        this.saveUserPreferences();
    }

    show(options) {
        const config = {
            type: 'info',
            title: '',
            message: '',
            duration: this.defaultDuration,
            actions: [],
            image: null,
            animation: 'slide-left',
            showProgress: true,
            persistent: false,
            onClick: null,
            onClose: null,
            sound: this.soundEnabled,
            ...options
        };

        const id = this.generateId();
        const notification = this.createNotification(id, config);
        
        this.notifications.set(id, {
            element: notification,
            config: config,
            timer: null,
            startTime: Date.now()
        });

        this.addToDOM(notification);
        this.scheduleRemoval(id, config.duration);
        
        if (config.sound) {
            this.playSound(config.type);
        }

        // Limiter le nombre de notifications
        this.enforceLimit();

        return id;
    }

    createNotification(id, config) {
        const notification = document.createElement('div');
        notification.id = `notification-${id}`;
        notification.className = `notification ${config.type} ${config.animation}`;
        notification.setAttribute('role', 'alert');
        notification.setAttribute('aria-live', config.type === 'error' ? 'assertive' : 'polite');
        notification.setAttribute('tabindex', '0');

        // Icône
        const iconMap = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle'
        };

        let content = `
            <div class="notification-icon">
                <i class="${iconMap[config.type]}" aria-hidden="true"></i>
            </div>
        `;

        // Image optionnelle
        if (config.image) {
            content += `<img src="${config.image}" alt="" class="notification-image">`;
        }

        // Contenu
        content += `
            <div class="notification-content">
                ${config.title ? `<div class="notification-title">${config.title}</div>` : ''}
                <div class="notification-message">${config.message}</div>
                ${config.actions.length > 0 ? this.createActions(config.actions) : ''}
            </div>
        `;

        // Bouton de fermeture
        if (!config.persistent) {
            content += `
                <button class="notification-close" aria-label="Fermer la notification">
                    <i class="fas fa-times" aria-hidden="true"></i>
                </button>
            `;
        }

        // Barre de progression
        if (config.showProgress && config.duration > 0) {
            content += `<div class="notification-progress" style="animation-duration: ${config.duration}ms"></div>`;
        }

        // PROTECTION: Utiliser insertAdjacentHTML au lieu de innerHTML
    notification.innerHTML = content;

        // Event listeners
        this.setupNotificationEvents(notification, id, config);

        return notification;
    }

    createActions(actions) {
        const actionsHtml = actions.map(action => `
            <button class="notification-action ${action.primary ? 'primary' : ''}" 
                    data-action="${action.id}"
                    aria-label="${action.label}">
                ${action.label}
            </button>
        `).join('');

        return `<div class="notification-actions">${actionsHtml}</div>`;
    }

    setupNotificationEvents(notification, id, config) {
        // Clic sur la notification
        notification.addEventListener('click', (e) => {
            if (e.target.classList.contains('notification-close')) {
                this.dismiss(id);
            } else if (e.target.classList.contains('notification-action')) {
                const actionId = e.target.dataset.action;
                const action = config.actions.find(a => a.id === actionId);
                if (action && action.handler) {
                    action.handler();
                }
                if (action && action.dismissOnClick !== false) {
                    this.dismiss(id);
                }
            } else if (config.onClick) {
                config.onClick();
            }
        });

        // Navigation clavier
        notification.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.dismiss(id);
            } else if (e.key === 'Enter' || e.key === ' ') {
                if (config.onClick) {
                    e.preventDefault();
                    config.onClick();
                }
            }
        });

        // Pause/resume du timer au survol
        notification.addEventListener('mouseenter', () => {
            this.pauseTimer(id);
        });

        notification.addEventListener('mouseleave', () => {
            this.resumeTimer(id);
        });

        // Pause/resume du timer au focus
        notification.addEventListener('focus', () => {
            this.pauseTimer(id);
        });

        notification.addEventListener('blur', () => {
            this.resumeTimer(id);
        });
    }

    addToDOM(notification) {
        const container = document.getElementById('notification-container');
        if (!container) return;

        container.appendChild(notification);
        
        // Déclencher l'animation d'entrée
        requestAnimationFrame(() => {
            notification.classList.add('show');
        });
    }

    scheduleRemoval(id, duration) {
        if (duration <= 0) return;

        const notificationData = this.notifications.get(id);
        if (!notificationData) return;

        notificationData.timer = setTimeout(() => {
            this.dismiss(id);
        }, duration);
    }

    dismiss(id) {
        const notificationData = this.notifications.get(id);
        if (!notificationData) return;

        const { element, config, timer } = notificationData;

        // Annuler le timer
        if (timer) {
            clearTimeout(timer);
        }

        // Déclencher l'animation de sortie
        element.classList.remove('show');
        element.classList.add('hide');

        // Supprimer du DOM après l'animation
        setTimeout(() => {
            if (element.parentNode) {
                element.parentNode.removeChild(element);
            }
            this.notifications.delete(id);
            
            // Callback de fermeture
            if (config.onClose) {
                config.onClose();
            }
        }, this.animationDuration);
    }

    dismissAll() {
        this.notifications.forEach((_, id) => {
            this.dismiss(id);
        });
    }

    pauseTimer(id) {
        const notificationData = this.notifications.get(id);
        if (!notificationData || !notificationData.timer) return;

        clearTimeout(notificationData.timer);
        notificationData.pausedAt = Date.now();
    }

    resumeTimer(id) {
        const notificationData = this.notifications.get(id);
        if (!notificationData || !notificationData.pausedAt) return;

        const elapsed = notificationData.pausedAt - notificationData.startTime;
        const remaining = notificationData.config.duration - elapsed;
        
        if (remaining > 0) {
            notificationData.timer = setTimeout(() => {
                this.dismiss(id);
            }, remaining);
        }
        
        delete notificationData.pausedAt;
    }

    pauseAllTimers() {
        this.notifications.forEach((_, id) => {
            this.pauseTimer(id);
        });
    }

    resumeAllTimers() {
        this.notifications.forEach((_, id) => {
            this.resumeTimer(id);
        });
    }

    enforceLimit() {
        const count = this.notifications.size;
        if (count > this.maxNotifications) {
            const excess = count - this.maxNotifications;
            const oldestIds = Array.from(this.notifications.keys()).slice(0, excess);
            oldestIds.forEach(id => this.dismiss(id));
        }
    }

    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }

    playSound(type) {
        // Créer un son simple pour les notifications
        if (window.AudioContext || window.webkitAudioContext) {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            // Fréquences différentes selon le type
            const frequencies = {
                success: 800,
                error: 400,
                warning: 600,
                info: 500
            };
            
            oscillator.frequency.value = frequencies[type] || 500;
            oscillator.type = 'sine';
            
            gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
            
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.3);
        }
    }

    // Méthodes de convenance
    success(message, title = '', options = {}) {
        return this.show({
            type: 'success',
            title,
            message,
            ...options
        });
    }

    error(message, title = '', options = {}) {
        return this.show({
            type: 'error',
            title,
            message,
            ...options
        });
    }

    warning(message, title = '', options = {}) {
        return this.show({
            type: 'warning',
            title,
            message,
            ...options
        });
    }

    info(message, title = '', options = {}) {
        return this.show({
            type: 'info',
            title,
            message,
            ...options
        });
    }

    // Méthodes utilitaires
    getNotificationCount() {
        return this.notifications.size;
    }

    setMaxNotifications(max) {
        this.maxNotifications = max;
        this.enforceLimit();
    }

    setSoundEnabled(enabled) {
        this.soundEnabled = enabled;
        this.saveUserPreferences();
    }

    setDefaultDuration(duration) {
        this.defaultDuration = duration;
    }

    // Méthodes pour les notifications personnalisées
    showCustom(template, data = {}) {
        const notification = document.createElement('div');
        notification.className = 'notification custom';
        // PROTECTION: Utiliser insertAdjacentHTML au lieu de innerHTML
    notification.innerHTML = template;
        
        // Remplacer les variables dans le template
        Object.keys(data).forEach(key => {
            // PROTECTION: Utiliser insertAdjacentHTML au lieu de innerHTML
    notification.innerHTML = notification.innerHTML.replace(
                new RegExp(`{{${key}}}`, 'g'),
                data[key]
            );
        });
        
        const id = this.generateId();
        this.notifications.set(id, {
            element: notification,
            config: { type: 'custom', duration: this.defaultDuration },
            timer: null,
            startTime: Date.now()
        });
        
        this.addToDOM(notification);
        this.scheduleRemoval(id, this.defaultDuration);
        
        return id;
    }
}

// Initialiser le système de notifications
const notificationSystem = new NotificationSystem();

// Exporter pour utilisation globale
window.NotificationSystem = notificationSystem;

// Alias pour faciliter l'utilisation
window.notify = {
    success: (message, title, options) => notificationSystem.success(message, title, options),
    error: (message, title, options) => notificationSystem.error(message, title, options),
    warning: (message, title, options) => notificationSystem.warning(message, title, options),
    info: (message, title, options) => notificationSystem.info(message, title, options),
    show: (options) => notificationSystem.show(options),
    dismiss: (id) => notificationSystem.dismiss(id),
    dismissAll: () => notificationSystem.dismissAll()
};