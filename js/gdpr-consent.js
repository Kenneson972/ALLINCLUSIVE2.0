
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
 * PHASE 4 - PERFORMANCE & RGPD : Système de Consentement RGPD
 * Consentement granulaire avec design glassmorphism
 */

class GDPRConsentSystem {
    constructor() {
        this.config = {
            position: 'bottom-right',
            language: 'fr',
            showOnFirstVisit: true,
            autoShow: true,
            showRejectAll: true,
            showAcceptAll: true,
            showSettings: true,
            persistDays: 365,
            animationDuration: 300,
            theme: 'glassmorphism'
        };
        
        this.consentData = {
            necessary: true, // Toujours true, ne peut pas être désactivé
            analytics: false,
            marketing: false,
            personalization: false,
            functional: false,
            timestamp: null,
            version: '1.0.0',
            userAgent: navigator.userAgent,
            consentGiven: false
        };
        
        this.cookieCategories = {
            necessary: {
                name: 'Cookies nécessaires',
                description: 'Ces cookies sont essentiels au fonctionnement du site web et ne peuvent pas être désactivés.',
                required: true,
                cookies: [
                    {
                        name: 'khanelconcept_consent',
                        purpose: 'Stockage des préférences de consentement',
                        duration: '1 an',
                        type: 'localStorage'
                    },
                    {
                        name: 'khanelconcept_token',
                        purpose: 'Authentification utilisateur',
                        duration: 'Session',
                        type: 'localStorage'
                    }
                ]
            },
            analytics: {
                name: 'Cookies analytiques',
                description: 'Ces cookies nous aident à comprendre comment les visiteurs utilisent notre site.',
                required: false,
                cookies: [
                    {
                        name: 'khanelconcept_analytics',
                        purpose: 'Analyse du comportement utilisateur',
                        duration: '2 ans',
                        type: 'cookie'
                    }
                ]
            },
            marketing: {
                name: 'Cookies marketing',
                description: 'Ces cookies sont utilisés pour afficher des publicités personnalisées.',
                required: false,
                cookies: [
                    {
                        name: 'khanelconcept_marketing',
                        purpose: 'Publicités ciblées',
                        duration: '1 an',
                        type: 'cookie'
                    }
                ]
            },
            personalization: {
                name: 'Cookies de personnalisation',
                description: 'Ces cookies permettent de personnaliser votre expérience sur le site.',
                required: false,
                cookies: [
                    {
                        name: 'khanelconcept_prefs',
                        purpose: 'Préférences utilisateur',
                        duration: '6 mois',
                        type: 'localStorage'
                    }
                ]
            },
            functional: {
                name: 'Cookies fonctionnels',
                description: 'Ces cookies activent des fonctionnalités avancées et améliorent l\'expérience utilisateur.',
                required: false,
                cookies: [
                    {
                        name: 'khanelconcept_cache',
                        purpose: 'Optimisation des performances',
                        duration: '1 jour',
                        type: 'localStorage'
                    }
                ]
            }
        };
        
        this.texts = {
            fr: {
                title: 'Gestion des cookies',
                description: 'Nous utilisons des cookies pour améliorer votre expérience sur notre site. Vous pouvez choisir quels cookies accepter.',
                acceptAll: 'Accepter tout',
                rejectAll: 'Rejeter tout',
                saveSettings: 'Sauvegarder mes préférences',
                settings: 'Paramètres',
                close: 'Fermer',
                moreInfo: 'Plus d\'informations',
                settingsTitle: 'Paramètres des cookies',
                settingsDescription: 'Vous pouvez activer ou désactiver les différents types de cookies ci-dessous. Ces paramètres seront sauvegardés pour votre prochaine visite.',
                dataProcessing: 'Traitement des données',
                dataProcessingText: 'Vos données sont traitées conformément à notre politique de confidentialité et aux réglementations RGPD.',
                privacyPolicy: 'Politique de confidentialité',
                legalBasis: 'Base légale',
                consent: 'Consentement',
                legitimateInterest: 'Intérêt légitime',
                vitalInterest: 'Intérêt vital',
                dataRetention: 'Conservation des données',
                dataRetentionText: 'Vos données de consentement sont conservées pendant 1 an maximum.',
                yourRights: 'Vos droits',
                yourRightsText: 'Vous avez le droit d\'accéder, de rectifier, de supprimer et de transférer vos données. Contactez-nous pour exercer ces droits.',
                contact: 'Contact',
                contactEmail: 'privacy@khanelconcept.com',
                lastUpdated: 'Dernière mise à jour',
                version: 'Version'
            }
        };
        
        this.modal = null;
        this.banner = null;
        this.isVisible = false;
        
        this.init();
    }

    init() {
        this.injectStyles();
        this.loadConsentData();
        
        if (this.config.autoShow && this.shouldShowBanner()) {
            this.showBanner();
        }
        
        this.setupEventListeners();
    }

    injectStyles() {
        const styles = `
            <style id="gdpr-consent-styles">
                /* PHASE 4 - RGPD avec design glassmorphism */
                .gdpr-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0, 0, 0, 0.7);
                    backdrop-filter: blur(8px);
                    z-index: 10000;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    opacity: 0;
                    visibility: hidden;
                    transition: all 0.3s ease;
                }

                .gdpr-overlay.show {
                    opacity: 1;
                    visibility: visible;
                }

                .gdpr-banner {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    max-width: 400px;
                    background: rgba(255, 255, 255, 0.95);
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 20px;
                    padding: 1.5rem;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
                    z-index: 9999;
                    transform: translateY(100%);
                    opacity: 0;
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                }

                .gdpr-banner.show {
                    transform: translateY(0);
                    opacity: 1;
                }

                .gdpr-banner.bottom-left {
                    bottom: 20px;
                    left: 20px;
                    right: auto;
                }

                .gdpr-banner.top-right {
                    top: 20px;
                    bottom: auto;
                    transform: translateY(-100%);
                }

                .gdpr-banner.top-left {
                    top: 20px;
                    left: 20px;
                    right: auto;
                    bottom: auto;
                    transform: translateY(-100%);
                }

                .gdpr-modal {
                    background: rgba(255, 255, 255, 0.95);
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 20px;
                    max-width: 700px;
                    width: 90%;
                    max-height: 90vh;
                    overflow-y: auto;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
                    transform: scale(0.9);
                    opacity: 0;
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                }

                .gdpr-modal.show {
                    transform: scale(1);
                    opacity: 1;
                }

                .gdpr-header {
                    padding: 2rem 2rem 1rem;
                    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
                    position: relative;
                }

                .gdpr-title {
                    font-size: 1.5rem;
                    font-weight: 600;
                    color: #1f2937;
                    margin-bottom: 0.5rem;
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                }

                .gdpr-description {
                    color: #6b7280;
                    font-size: 0.95rem;
                    line-height: 1.5;
                }

                .gdpr-close {
                    position: absolute;
                    top: 1rem;
                    right: 1rem;
                    background: none;
                    border: none;
                    font-size: 1.5rem;
                    color: #6b7280;
                    cursor: pointer;
                    width: 40px;
                    height: 40px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border-radius: 50%;
                    transition: all 0.2s ease;
                }

                .gdpr-close:hover {
                    background: rgba(0, 0, 0, 0.1);
                    color: #374151;
                }

                .gdpr-close:focus {
                    outline: 2px solid #3b82f6;
                    outline-offset: 2px;
                }

                .gdpr-content {
                    padding: 1.5rem 2rem;
                }

                .gdpr-category {
                    border: 1px solid rgba(0, 0, 0, 0.1);
                    border-radius: 12px;
                    margin-bottom: 1rem;
                    background: rgba(255, 255, 255, 0.5);
                    transition: all 0.2s ease;
                }

                .gdpr-category:hover {
                    background: rgba(255, 255, 255, 0.7);
                }

                .gdpr-category-header {
                    padding: 1rem 1.5rem;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    cursor: pointer;
                    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
                }

                .gdpr-category-header:last-child {
                    border-bottom: none;
                }

                .gdpr-category-info {
                    flex: 1;
                }

                .gdpr-category-name {
                    font-weight: 600;
                    color: #1f2937;
                    margin-bottom: 0.25rem;
                }

                .gdpr-category-description {
                    color: #6b7280;
                    font-size: 0.9rem;
                    line-height: 1.4;
                }

                .gdpr-toggle {
                    position: relative;
                    width: 50px;
                    height: 24px;
                    background: #d1d5db;
                    border-radius: 12px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }

                .gdpr-toggle.active {
                    background: #10b981;
                }

                .gdpr-toggle.disabled {
                    background: #f3f4f6;
                    cursor: not-allowed;
                }

                .gdpr-toggle::after {
                    content: '';
                    position: absolute;
                    top: 2px;
                    left: 2px;
                    width: 20px;
                    height: 20px;
                    background: white;
                    border-radius: 50%;
                    transition: all 0.3s ease;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
                }

                .gdpr-toggle.active::after {
                    transform: translateX(26px);
                }

                .gdpr-toggle.disabled::after {
                    background: #e5e7eb;
                }

                .gdpr-category-details {
                    padding: 1.5rem;
                    background: rgba(255, 255, 255, 0.3);
                    border-top: 1px solid rgba(0, 0, 0, 0.1);
                    display: none;
                }

                .gdpr-category-details.show {
                    display: block;
                }

                .gdpr-cookies-list {
                    margin-top: 1rem;
                }

                .gdpr-cookie {
                    background: rgba(255, 255, 255, 0.8);
                    border: 1px solid rgba(0, 0, 0, 0.1);
                    border-radius: 8px;
                    padding: 1rem;
                    margin-bottom: 0.5rem;
                }

                .gdpr-cookie-name {
                    font-weight: 600;
                    color: #1f2937;
                    margin-bottom: 0.25rem;
                    font-size: 0.9rem;
                }

                .gdpr-cookie-info {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 0.5rem;
                    font-size: 0.8rem;
                    color: #6b7280;
                }

                .gdpr-footer {
                    padding: 1.5rem 2rem;
                    border-top: 1px solid rgba(0, 0, 0, 0.1);
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    flex-wrap: wrap;
                    gap: 1rem;
                }

                .gdpr-buttons {
                    display: flex;
                    gap: 0.75rem;
                    flex-wrap: wrap;
                }

                .gdpr-btn {
                    padding: 0.75rem 1.5rem;
                    border: none;
                    border-radius: 10px;
                    font-size: 0.9rem;
                    font-weight: 500;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    text-decoration: none;
                    display: inline-flex;
                    align-items: center;
                    gap: 0.5rem;
                }

                .gdpr-btn-primary {
                    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                    color: white;
                }

                .gdpr-btn-primary:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3);
                }

                .gdpr-btn-secondary {
                    background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
                    color: white;
                }

                .gdpr-btn-secondary:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 8px 20px rgba(107, 114, 128, 0.3);
                }

                .gdpr-btn-outline {
                    background: transparent;
                    color: #6b7280;
                    border: 2px solid #e5e7eb;
                }

                .gdpr-btn-outline:hover {
                    background: rgba(107, 114, 128, 0.1);
                    border-color: #6b7280;
                }

                .gdpr-btn:focus {
                    outline: 2px solid #3b82f6;
                    outline-offset: 2px;
                }

                .gdpr-legal-info {
                    margin-top: 1rem;
                    padding: 1rem;
                    background: rgba(59, 130, 246, 0.1);
                    border: 1px solid rgba(59, 130, 246, 0.2);
                    border-radius: 8px;
                    font-size: 0.85rem;
                    color: #1e40af;
                }

                .gdpr-legal-info h4 {
                    color: #1e40af;
                    margin-bottom: 0.5rem;
                    font-size: 0.9rem;
                }

                .gdpr-legal-info p {
                    margin-bottom: 0.5rem;
                    line-height: 1.4;
                }

                .gdpr-legal-info a {
                    color: #2563eb;
                    text-decoration: underline;
                }

                .gdpr-version-info {
                    font-size: 0.75rem;
                    color: #9ca3af;
                    text-align: center;
                    margin-top: 1rem;
                }

                .gdpr-required-badge {
                    background: #fef3c7;
                    color: #92400e;
                    font-size: 0.7rem;
                    padding: 0.25rem 0.5rem;
                    border-radius: 4px;
                    font-weight: 500;
                    margin-left: 0.5rem;
                }

                .gdpr-expand-toggle {
                    background: none;
                    border: none;
                    color: #6b7280;
                    cursor: pointer;
                    font-size: 1.2rem;
                    padding: 0.25rem;
                    transition: all 0.2s ease;
                }

                .gdpr-expand-toggle:hover {
                    color: #374151;
                }

                .gdpr-expand-toggle.expanded {
                    transform: rotate(180deg);
                }

                /* Responsive */
                @media (max-width: 768px) {
                    .gdpr-banner {
                        bottom: 0;
                        left: 0;
                        right: 0;
                        max-width: none;
                        border-radius: 20px 20px 0 0;
                        transform: translateY(100%);
                    }

                    .gdpr-modal {
                        width: 95%;
                        max-height: 95vh;
                    }

                    .gdpr-header,
                    .gdpr-content,
                    .gdpr-footer {
                        padding: 1rem;
                    }

                    .gdpr-footer {
                        flex-direction: column;
                        align-items: stretch;
                    }

                    .gdpr-buttons {
                        justify-content: center;
                    }

                    .gdpr-btn {
                        flex: 1;
                        justify-content: center;
                    }

                    .gdpr-category-header {
                        padding: 0.75rem 1rem;
                    }

                    .gdpr-category-details {
                        padding: 1rem;
                    }

                    .gdpr-cookie-info {
                        grid-template-columns: 1fr;
                    }
                }

                /* Thème sombre */
                .gdpr-dark .gdpr-banner,
                .gdpr-dark .gdpr-modal {
                    background: rgba(31, 41, 55, 0.95);
                    border-color: rgba(75, 85, 99, 0.3);
                }

                .gdpr-dark .gdpr-title {
                    color: #f9fafb;
                }

                .gdpr-dark .gdpr-description,
                .gdpr-dark .gdpr-category-description {
                    color: #d1d5db;
                }

                .gdpr-dark .gdpr-category {
                    background: rgba(55, 65, 81, 0.5);
                    border-color: rgba(75, 85, 99, 0.3);
                }

                .gdpr-dark .gdpr-category-name {
                    color: #f9fafb;
                }

                .gdpr-dark .gdpr-cookie {
                    background: rgba(55, 65, 81, 0.8);
                    border-color: rgba(75, 85, 99, 0.3);
                }

                .gdpr-dark .gdpr-cookie-name {
                    color: #f9fafb;
                }

                .gdpr-dark .gdpr-cookie-info {
                    color: #d1d5db;
                }

                /* Animations */
                .gdpr-fade-in {
                    animation: gdprFadeIn 0.3s ease-out;
                }

                @keyframes gdprFadeIn {
                    from {
                        opacity: 0;
                        transform: translateY(20px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }

                /* Accessibilité */
                .gdpr-toggle:focus {
                    outline: 2px solid #3b82f6;
                    outline-offset: 2px;
                }

                .gdpr-category-header:focus {
                    outline: 2px solid #3b82f6;
                    outline-offset: 2px;
                }

                /* Reduced motion */
                @media (prefers-reduced-motion: reduce) {
                    .gdpr-banner,
                    .gdpr-modal,
                    .gdpr-overlay,
                    .gdpr-toggle,
                    .gdpr-toggle::after,
                    .gdpr-btn,
                    .gdpr-expand-toggle {
                        transition: none;
                    }
                    
                    .gdpr-fade-in {
                        animation: none;
                    }
                }
            </style>
        `;
        
        if (!document.getElementById('gdpr-consent-styles')) {
            document.head.insertAdjacentHTML('beforeend', styles);
        }
    }

    shouldShowBanner() {
        const consentData = this.getConsentData();
        
        // Nouvelle visite ou consentement expiré
        if (!consentData || !consentData.consentGiven) {
            return true;
        }
        
        // Vérifier l'expiration
        const consentDate = new Date(consentData.timestamp);
        const now = new Date();
        const daysDiff = Math.floor((now - consentDate) / (1000 * 60 * 60 * 24));
        
        if (daysDiff > this.config.persistDays) {
            return true;
        }
        
        // Vérifier si la version a changé
        if (consentData.version !== this.consentData.version) {
            return true;
        }
        
        return false;
    }

    showBanner() {
        if (this.isVisible) return;
        
        const banner = this.createBanner();
        document.body.appendChild(banner);
        
        // Déclencher l'animation
        requestAnimationFrame(() => {
            banner.classList.add('show');
        });
        
        this.banner = banner;
        this.isVisible = true;
        
        // Événement personnalisé
        this.dispatchEvent('bannerShown');
    }

    createBanner() {
        const texts = this.texts[this.config.language];
        
        const banner = document.createElement('div');
        banner.className = `gdpr-banner ${this.config.position}`;
        banner.setAttribute('role', 'dialog');
        banner.setAttribute('aria-labelledby', 'gdpr-banner-title');
        banner.setAttribute('aria-describedby', 'gdpr-banner-description');
        
        // PROTECTION: Utiliser insertAdjacentHTML au lieu de innerHTML
    banner.innerHTML = `
            <div class="gdpr-fade-in">
                <h3 id="gdpr-banner-title" class="gdpr-title">
                    <i class="fas fa-shield-alt" aria-hidden="true"></i>
                    ${texts.title}
                </h3>
                <p id="gdpr-banner-description" class="gdpr-description">
                    ${texts.description}
                </p>
                <div class="gdpr-buttons" style="margin-top: 1rem;">
                    ${this.config.showAcceptAll ? `
                        <button class="gdpr-btn gdpr-btn-primary" onclick="gdprConsent.acceptAll()">
                            <i class="fas fa-check" aria-hidden="true"></i>
                            ${texts.acceptAll}
                        </button>
                    ` : ''}
                    ${this.config.showSettings ? `
                        <button class="gdpr-btn gdpr-btn-outline" onclick="gdprConsent.showSettings()">
                            <i class="fas fa-cog" aria-hidden="true"></i>
                            ${texts.settings}
                        </button>
                    ` : ''}
                    ${this.config.showRejectAll ? `
                        <button class="gdpr-btn gdpr-btn-secondary" onclick="gdprConsent.rejectAll()">
                            <i class="fas fa-times" aria-hidden="true"></i>
                            ${texts.rejectAll}
                        </button>
                    ` : ''}
                </div>
            </div>
        `;
        
        return banner;
    }

    showSettings() {
        if (!this.modal) {
            this.modal = this.createModal();
        }
        
        document.body.appendChild(this.modal);
        
        // Déclencher l'animation
        requestAnimationFrame(() => {
            this.modal.classList.add('show');
            this.modal.querySelector('.gdpr-modal').classList.add('show');
        });
        
        // Focus sur le modal pour l'accessibilité
        this.modal.querySelector('.gdpr-modal').focus();
        
        this.dispatchEvent('settingsShown');
    }

    createModal() {
        const texts = this.texts[this.config.language];
        
        const overlay = document.createElement('div');
        overlay.className = 'gdpr-overlay';
        overlay.setAttribute('role', 'dialog');
        overlay.setAttribute('aria-modal', 'true');
        overlay.setAttribute('aria-labelledby', 'gdpr-modal-title');
        
        const modal = document.createElement('div');
        modal.className = 'gdpr-modal';
        modal.setAttribute('tabindex', '-1');
        
        // PROTECTION: Utiliser insertAdjacentHTML au lieu de innerHTML
    modal.innerHTML = `
            <div class="gdpr-header">
                <h2 id="gdpr-modal-title" class="gdpr-title">
                    <i class="fas fa-shield-alt" aria-hidden="true"></i>
                    ${texts.settingsTitle}
                </h2>
                <p class="gdpr-description">${texts.settingsDescription}</p>
                <button class="gdpr-close" onclick="gdprConsent.hideSettings()" aria-label="${texts.close}">
                    <i class="fas fa-times" aria-hidden="true"></i>
                </button>
            </div>
            
            <div class="gdpr-content">
                ${this.createCategoriesHTML()}
                ${this.createLegalInfoHTML()}
            </div>
            
            <div class="gdpr-footer">
                <div class="gdpr-version-info">
                    ${texts.version} ${this.consentData.version} • ${texts.lastUpdated} ${new Date().toLocaleDateString(this.config.language)}
                </div>
                <div class="gdpr-buttons">
                    <button class="gdpr-btn gdpr-btn-secondary" onclick="gdprConsent.rejectAll()">
                        <i class="fas fa-times" aria-hidden="true"></i>
                        ${texts.rejectAll}
                    </button>
                    <button class="gdpr-btn gdpr-btn-primary" onclick="gdprConsent.saveSettings()">
                        <i class="fas fa-save" aria-hidden="true"></i>
                        ${texts.saveSettings}
                    </button>
                    <button class="gdpr-btn gdpr-btn-primary" onclick="gdprConsent.acceptAll()">
                        <i class="fas fa-check-double" aria-hidden="true"></i>
                        ${texts.acceptAll}
                    </button>
                </div>
            </div>
        `;
        
        overlay.appendChild(modal);
        
        // Fermer en cliquant sur l'overlay
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                this.hideSettings();
            }
        });
        
        // Gestion des touches
        overlay.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.hideSettings();
            }
        });
        
        return overlay;
    }

    createCategoriesHTML() {
        let html = '';
        
        Object.entries(this.cookieCategories).forEach(([key, category]) => {
            const isChecked = this.consentData[key];
            const isRequired = category.required;
            
            html += `
                <div class="gdpr-category">
                    <div class="gdpr-category-header" onclick="gdprConsent.toggleCategoryDetails('${key}')" tabindex="0" role="button" aria-expanded="false">
                        <div class="gdpr-category-info">
                            <div class="gdpr-category-name">
                                ${category.name}
                                ${isRequired ? '<span class="gdpr-required-badge">Requis</span>' : ''}
                            </div>
                            <div class="gdpr-category-description">${category.description}</div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 0.5rem;">
                            <div class="gdpr-toggle ${isChecked ? 'active' : ''} ${isRequired ? 'disabled' : ''}" 
                                 onclick="event.stopPropagation(); gdprConsent.toggleCategory('${key}')"
                                 role="switch" 
                                 aria-checked="${isChecked}"
                                 aria-label="Basculer ${category.name}"
                                 ${isRequired ? 'aria-disabled="true"' : ''}
                                 tabindex="0">
                            </div>
                            <button class="gdpr-expand-toggle" aria-label="Afficher les détails">
                                <i class="fas fa-chevron-down" aria-hidden="true"></i>
                            </button>
                        </div>
                    </div>
                    <div class="gdpr-category-details" id="gdpr-details-${key}">
                        <h4>Cookies utilisés :</h4>
                        <div class="gdpr-cookies-list">
                            ${category.cookies.map(cookie => `
                                <div class="gdpr-cookie">
                                    <div class="gdpr-cookie-name">${cookie.name}</div>
                                    <div class="gdpr-cookie-info">
                                        <div><strong>Finalité :</strong> ${cookie.purpose}</div>
                                        <div><strong>Durée :</strong> ${cookie.duration}</div>
                                        <div><strong>Type :</strong> ${cookie.type}</div>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            `;
        });
        
        return html;
    }

    createLegalInfoHTML() {
        const texts = this.texts[this.config.language];
        
        return `
            <div class="gdpr-legal-info">
                <h4><i class="fas fa-gavel" aria-hidden="true"></i> ${texts.dataProcessing}</h4>
                <p>${texts.dataProcessingText}</p>
                <p><strong>${texts.legalBasis} :</strong> ${texts.consent}</p>
                <p><strong>${texts.dataRetention} :</strong> ${texts.dataRetentionText}</p>
                
                <h4><i class="fas fa-user-shield" aria-hidden="true"></i> ${texts.yourRights}</h4>
                <p>${texts.yourRightsText}</p>
                <p><strong>${texts.contact} :</strong> <a href="mailto:${texts.contactEmail}">${texts.contactEmail}</a></p>
                
                <p><a href="/privacy-policy" target="_blank">${texts.privacyPolicy}</a> | <a href="/privacy-policy#cookies" target="_blank">${texts.moreInfo}</a></p>
            </div>
        `;
    }

    toggleCategoryDetails(categoryKey) {
        const details = document.getElementById(`gdpr-details-${categoryKey}`);
        const toggle = details.parentElement.querySelector('.gdpr-expand-toggle');
        const header = details.parentElement.querySelector('.gdpr-category-header');
        
        if (details.classList.contains('show')) {
            details.classList.remove('show');
            toggle.classList.remove('expanded');
            header.setAttribute('aria-expanded', 'false');
        } else {
            details.classList.add('show');
            toggle.classList.add('expanded');
            header.setAttribute('aria-expanded', 'true');
        }
    }

    toggleCategory(categoryKey) {
        if (this.cookieCategories[categoryKey].required) {
            return; // Ne pas permettre la désactivation des cookies requis
        }
        
        this.consentData[categoryKey] = !this.consentData[categoryKey];
        
        // Mettre à jour l'interface
        const toggle = document.querySelector(`[onclick*="toggleCategory('${categoryKey}')"]`);
        if (toggle) {
            toggle.classList.toggle('active', this.consentData[categoryKey]);
            toggle.setAttribute('aria-checked', this.consentData[categoryKey]);
        }
        
        this.dispatchEvent('categoryToggled', { category: categoryKey, enabled: this.consentData[categoryKey] });
    }

    acceptAll() {
        Object.keys(this.cookieCategories).forEach(key => {
            this.consentData[key] = true;
        });
        
        this.saveConsent();
        this.hideAll();
        this.dispatchEvent('acceptedAll');
    }

    rejectAll() {
        Object.keys(this.cookieCategories).forEach(key => {
            this.consentData[key] = this.cookieCategories[key].required;
        });
        
        this.saveConsent();
        this.hideAll();
        this.dispatchEvent('rejectedAll');
    }

    saveSettings() {
        this.saveConsent();
        this.hideAll();
        this.dispatchEvent('settingsSaved');
    }

    saveConsent() {
        this.consentData.consentGiven = true;
        this.consentData.timestamp = new Date().toISOString();
        
        // Sauvegarder dans localStorage
        localStorage.setItem('khanelconcept_consent', JSON.stringify(this.consentData));
        
        // Appliquer les consentements
        this.applyConsent();
    }

    applyConsent() {
        // Appliquer les consentements aux cookies/scripts
        if (this.consentData.analytics) {
            this.enableAnalytics();
        } else {
            this.disableAnalytics();
        }
        
        if (this.consentData.marketing) {
            this.enableMarketing();
        } else {
            this.disableMarketing();
        }
        
        if (this.consentData.personalization) {
            this.enablePersonalization();
        } else {
            this.disablePersonalization();
        }
        
        if (this.consentData.functional) {
            this.enableFunctional();
        } else {
            this.disableFunctional();
        }
    }

    enableAnalytics() {
        // Activer Google Analytics, etc.
        if (typeof gtag !== 'undefined') {
            gtag('consent', 'update', {
                'analytics_storage': 'granted'
            });
        }
        
        localStorage.setItem('khanelconcept_analytics', 'enabled');
        this.dispatchEvent('analyticsEnabled');
    }

    disableAnalytics() {
        if (typeof gtag !== 'undefined') {
            gtag('consent', 'update', {
                'analytics_storage': 'denied'
            });
        }
        
        localStorage.removeItem('khanelconcept_analytics');
        this.dispatchEvent('analyticsDisabled');
    }

    enableMarketing() {
        if (typeof gtag !== 'undefined') {
            gtag('consent', 'update', {
                'ad_storage': 'granted'
            });
        }
        
        localStorage.setItem('khanelconcept_marketing', 'enabled');
        this.dispatchEvent('marketingEnabled');
    }

    disableMarketing() {
        if (typeof gtag !== 'undefined') {
            gtag('consent', 'update', {
                'ad_storage': 'denied'
            });
        }
        
        localStorage.removeItem('khanelconcept_marketing');
        this.dispatchEvent('marketingDisabled');
    }

    enablePersonalization() {
        localStorage.setItem('khanelconcept_prefs', 'enabled');
        this.dispatchEvent('personalizationEnabled');
    }

    disablePersonalization() {
        localStorage.removeItem('khanelconcept_prefs');
        this.dispatchEvent('personalizationDisabled');
    }

    enableFunctional() {
        // Activer le cache, etc.
        if (window.CacheSystem) {
            window.CacheSystem.configure({ enablePersistence: true });
        }
        
        localStorage.setItem('khanelconcept_functional', 'enabled');
        this.dispatchEvent('functionalEnabled');
    }

    disableFunctional() {
        if (window.CacheSystem) {
            window.CacheSystem.configure({ enablePersistence: false });
        }
        
        localStorage.removeItem('khanelconcept_functional');
        this.dispatchEvent('functionalDisabled');
    }

    hideSettings() {
        if (this.modal) {
            this.modal.classList.remove('show');
            this.modal.querySelector('.gdpr-modal').classList.remove('show');
            
            setTimeout(() => {
                if (this.modal.parentNode) {
                    this.modal.parentNode.removeChild(this.modal);
                }
            }, this.config.animationDuration);
        }
        
        this.dispatchEvent('settingsHidden');
    }

    hideBanner() {
        if (this.banner) {
            this.banner.classList.remove('show');
            
            setTimeout(() => {
                if (this.banner.parentNode) {
                    this.banner.parentNode.removeChild(this.banner);
                }
            }, this.config.animationDuration);
        }
        
        this.isVisible = false;
        this.dispatchEvent('bannerHidden');
    }

    hideAll() {
        this.hideBanner();
        this.hideSettings();
    }

    loadConsentData() {
        const saved = localStorage.getItem('khanelconcept_consent');
        if (saved) {
            try {
                const data = JSON.parse(saved);
                this.consentData = { ...this.consentData, ...data };
                this.applyConsent();
            } catch (e) {
                console.warn('Could not load consent data:', e);
            }
        }
    }

    getConsentData() {
        return { ...this.consentData };
    }

    hasConsent(category) {
        return this.consentData[category] === true;
    }

    revokeConsent() {
        localStorage.removeItem('khanelconcept_consent');
        
        // Réinitialiser les consentements
        Object.keys(this.cookieCategories).forEach(key => {
            this.consentData[key] = this.cookieCategories[key].required;
        });
        this.consentData.consentGiven = false;
        
        this.applyConsent();
        this.showBanner();
        
        this.dispatchEvent('consentRevoked');
    }

    setupEventListeners() {
        // Écouter les changements de préférences
        window.addEventListener('storage', (e) => {
            if (e.key === 'khanelconcept_consent') {
                this.loadConsentData();
            }
        });
    }

    dispatchEvent(eventName, detail = {}) {
        const event = new CustomEvent(`gdpr:${eventName}`, {
            detail: { ...detail, consent: this.getConsentData() }
        });
        
        window.dispatchEvent(event);
    }

    // Méthodes utilitaires
    configure(options) {
        this.config = { ...this.config, ...options };
    }

    showConsentManager() {
        this.showSettings();
    }

    getVersion() {
        return this.consentData.version;
    }

    isConsentGiven() {
        return this.consentData.consentGiven;
    }
}

// Initialiser le système RGPD
const gdprConsent = new GDPRConsentSystem();

// Exporter pour utilisation globale
window.GDPRConsent = gdprConsent;
window.gdprConsent = gdprConsent;

// Utilitaires pour les développeurs
window.gdprDebug = {
    showBanner: () => gdprConsent.showBanner(),
    showSettings: () => gdprConsent.showSettings(),
    getConsent: () => gdprConsent.getConsentData(),
    revokeConsent: () => gdprConsent.revokeConsent(),
    hasConsent: (category) => gdprConsent.hasConsent(category)
};