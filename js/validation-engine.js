/**
 * PHASE 3 - UX/UI : Moteur de Validation Temps Réel Avancée
 * Système de validation interactif et accessible pour tous les formulaires
 */

class ValidationEngine {
    constructor() {
        this.validators = new Map();
        this.fields = new Map();
        this.rules = {
            required: {
                test: (value) => value && value.trim().length > 0,
                message: 'Ce champ est requis'
            },
            email: {
                test: (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
                message: 'Format email invalide'
            },
            phone: {
                test: (value) => /^\+?[\d\s\-\(\)]{10,}$/.test(value),
                message: 'Format téléphone invalide'
            },
            password: {
                test: (value) => value.length >= 8 && 
                    /(?=.*[a-z])/.test(value) && 
                    /(?=.*[A-Z])/.test(value) && 
                    /(?=.*\d)/.test(value) && 
                    /(?=.*[@$!%*?&])/.test(value),
                message: 'Mot de passe : 8+ caractères, majuscule, minuscule, chiffre, caractère spécial'
            },
            minLength: (length) => ({
                test: (value) => value.length >= length,
                message: `Minimum ${length} caractères requis`
            }),
            maxLength: (length) => ({
                test: (value) => value.length <= length,
                message: `Maximum ${length} caractères autorisés`
            }),
            match: (targetFieldId) => ({
                test: (value) => {
                    const targetField = document.getElementById(targetFieldId);
                    return targetField ? value === targetField.value : false;
                },
                message: 'Les mots de passe ne correspondent pas'
            }),
            pattern: (regex, message) => ({
                test: (value) => regex.test(value),
                message: message || 'Format invalide'
            })
        };
        
        // Debounce pour éviter trop de validations
        this.debounceTimeouts = new Map();
        
        // Indicateurs de force pour mots de passe
        this.strengthIndicators = new Map();
        
        // Système de notifications
        this.notifications = [];
        
        this.init();
    }

    init() {
        // Créer le conteneur de notifications
        this.createNotificationContainer();
        
        // Styles CSS pour les validations
        this.injectStyles();
        
        // Écouter les changements dans les formulaires
        this.setupGlobalListeners();
    }

    createNotificationContainer() {
        if (!document.getElementById('validation-notifications')) {
            const container = document.createElement('div');
            container.id = 'validation-notifications';
            container.className = 'validation-notifications-container';
            container.setAttribute('aria-live', 'polite');
            container.setAttribute('aria-atomic', 'true');
            document.body.appendChild(container);
        }
    }

    injectStyles() {
        const styles = `
            <style id="validation-engine-styles">
                /* PHASE 3 - Styles de validation temps réel */
                .validation-field {
                    position: relative;
                    margin-bottom: 1.5rem;
                }

                .validation-input {
                    transition: all 0.3s ease;
                    border: 2px solid rgba(255, 255, 255, 0.3);
                }

                .validation-input:focus {
                    outline: none;
                    border-color: #f6ad55;
                    box-shadow: 0 0 0 3px rgba(246, 173, 85, 0.1);
                }

                .validation-input.valid {
                    border-color: #10b981;
                    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='%2310b981'%3e%3cpath d='M12.736 3.97a.733.733 0 0 1 1.047 0c.286.289.29.756.01 1.05L7.88 12.01a.733.733 0 0 1-1.065.02L3.217 8.384a.757.757 0 0 1 0-1.06.733.733 0 0 1 1.047 0l3.052 3.093 5.4-6.425a.247.247 0 0 1 .02-.022Z'/%3e%3c/svg%3e");
                    background-repeat: no-repeat;
                    background-position: right 0.75rem center;
                    background-size: 1rem;
                }

                .validation-input.invalid {
                    border-color: #ef4444;
                    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='%23ef4444'%3e%3cpath d='M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z'/%3e%3cpath d='M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z'/%3e%3c/svg%3e");
                    background-repeat: no-repeat;
                    background-position: right 0.75rem center;
                    background-size: 1rem;
                }

                .validation-message {
                    position: absolute;
                    top: 100%;
                    left: 0;
                    right: 0;
                    padding: 0.5rem 0;
                    font-size: 0.875rem;
                    font-weight: 500;
                    opacity: 0;
                    transform: translateY(-10px);
                    transition: all 0.3s ease;
                    pointer-events: none;
                }

                .validation-message.show {
                    opacity: 1;
                    transform: translateY(0);
                }

                .validation-message.error {
                    color: #ef4444;
                }

                .validation-message.success {
                    color: #10b981;
                }

                .validation-message.warning {
                    color: #f59e0b;
                }

                /* Indicateur de force du mot de passe */
                .password-strength {
                    margin-top: 0.5rem;
                    padding: 0.75rem;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 8px;
                    backdrop-filter: blur(10px);
                }

                .strength-bar {
                    height: 4px;
                    background: rgba(255, 255, 255, 0.2);
                    border-radius: 2px;
                    overflow: hidden;
                    margin-bottom: 0.5rem;
                }

                .strength-fill {
                    height: 100%;
                    transition: all 0.3s ease;
                    border-radius: 2px;
                }

                .strength-weak { 
                    background: linear-gradient(90deg, #ef4444, #f97316);
                    width: 25%;
                }

                .strength-fair { 
                    background: linear-gradient(90deg, #f59e0b, #eab308);
                    width: 50%;
                }

                .strength-good { 
                    background: linear-gradient(90deg, #3b82f6, #8b5cf6);
                    width: 75%;
                }

                .strength-strong { 
                    background: linear-gradient(90deg, #10b981, #059669);
                    width: 100%;
                }

                .strength-text {
                    font-size: 0.8rem;
                    color: rgba(255, 255, 255, 0.9);
                    text-align: center;
                }

                /* Notifications de validation */
                .validation-notifications-container {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    z-index: 1000;
                    pointer-events: none;
                }

                .validation-notification {
                    background: rgba(255, 255, 255, 0.95);
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 12px;
                    padding: 1rem 1.5rem;
                    margin-bottom: 0.5rem;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                    transform: translateX(100%);
                    opacity: 0;
                    transition: all 0.3s ease;
                    pointer-events: auto;
                    max-width: 300px;
                }

                .validation-notification.show {
                    transform: translateX(0);
                    opacity: 1;
                }

                .validation-notification.success {
                    border-left: 4px solid #10b981;
                    color: #065f46;
                }

                .validation-notification.error {
                    border-left: 4px solid #ef4444;
                    color: #991b1b;
                }

                .validation-notification.warning {
                    border-left: 4px solid #f59e0b;
                    color: #92400e;
                }

                /* Indicateurs de validation en temps réel */
                .validation-indicator {
                    position: absolute;
                    right: 0.75rem;
                    top: 50%;
                    transform: translateY(-50%);
                    opacity: 0;
                    transition: all 0.3s ease;
                }

                .validation-indicator.show {
                    opacity: 1;
                }

                .validation-indicator.loading {
                    width: 1rem;
                    height: 1rem;
                    border: 2px solid rgba(255, 255, 255, 0.3);
                    border-top: 2px solid #f6ad55;
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                }

                @keyframes spin {
                    0% { transform: translateY(-50%) rotate(0deg); }
                    100% { transform: translateY(-50%) rotate(360deg); }
                }

                /* Amélioration du focus pour l'accessibilité */
                .validation-input:focus + .validation-indicator {
                    opacity: 0;
                }

                /* Styles pour les suggestions */
                .validation-suggestions {
                    margin-top: 0.5rem;
                    padding: 0.5rem;
                    background: rgba(59, 130, 246, 0.1);
                    border-radius: 6px;
                    border-left: 3px solid #3b82f6;
                }

                .validation-suggestions ul {
                    list-style: none;
                    padding: 0;
                    margin: 0;
                    font-size: 0.8rem;
                    color: rgba(255, 255, 255, 0.8);
                }

                .validation-suggestions li {
                    padding: 0.2rem 0;
                    position: relative;
                    padding-left: 1.5rem;
                }

                .validation-suggestions li:before {
                    content: "•";
                    position: absolute;
                    left: 0.5rem;
                    color: #3b82f6;
                }

                .validation-suggestions li.completed:before {
                    content: "✓";
                    color: #10b981;
                }
            </style>
        `;
        
        if (!document.getElementById('validation-engine-styles')) {
            document.head.insertAdjacentHTML('beforeend', styles);
        }
    }

    setupGlobalListeners() {
        // Écouter les changements sur tous les formulaires
        document.addEventListener('input', (e) => {
            if (e.target.matches('[data-validate]')) {
                this.validateField(e.target);
            }
        });

        // Écouter les événements de focus/blur
        document.addEventListener('focus', (e) => {
            if (e.target.matches('[data-validate]')) {
                this.onFieldFocus(e.target);
            }
        }, true);

        document.addEventListener('blur', (e) => {
            if (e.target.matches('[data-validate]')) {
                this.onFieldBlur(e.target);
            }
        }, true);

        // Écouter les soumissions de formulaire
        document.addEventListener('submit', (e) => {
            if (e.target.matches('[data-validate-form]')) {
                this.validateForm(e.target, e);
            }
        });
    }

    // Enregistrer un champ pour validation
    registerField(fieldId, rules, options = {}) {
        const field = document.getElementById(fieldId);
        if (!field) {
            console.error(`Field with id '${fieldId}' not found`);
            return;
        }

        // Ajouter l'attribut de validation
        field.setAttribute('data-validate', 'true');
        
        // Wrapper le champ si nécessaire
        this.wrapField(field, options);

        // Enregistrer les règles
        this.fields.set(fieldId, {
            element: field,
            rules: rules,
            options: options,
            isValid: false,
            lastValue: '',
            showSuggestions: options.showSuggestions || false
        });

        // Configurer l'indicateur de force pour les mots de passe
        if (options.type === 'password' && options.showStrength) {
            this.setupPasswordStrength(field);
        }
    }

    wrapField(field, options) {
        if (field.parentElement.classList.contains('validation-field')) {
            return; // Déjà wrappé
        }

        const wrapper = document.createElement('div');
        wrapper.className = 'validation-field';
        
        field.parentNode.insertBefore(wrapper, field);
        wrapper.appendChild(field);

        // Ajouter la classe de validation
        field.classList.add('validation-input');

        // Ajouter l'indicateur de validation
        const indicator = document.createElement('div');
        indicator.className = 'validation-indicator';
        wrapper.appendChild(indicator);

        // Ajouter le conteneur de message
        const messageContainer = document.createElement('div');
        messageContainer.className = 'validation-message';
        messageContainer.id = `${field.id}-message`;
        messageContainer.setAttribute('aria-live', 'polite');
        messageContainer.setAttribute('role', 'alert');
        wrapper.appendChild(messageContainer);

        // Ajouter les suggestions si demandées
        if (options.showSuggestions) {
            const suggestionsContainer = document.createElement('div');
            suggestionsContainer.className = 'validation-suggestions';
            suggestionsContainer.id = `${field.id}-suggestions`;
            suggestionsContainer.style.display = 'none';
            wrapper.appendChild(suggestionsContainer);
        }

        // Associer le champ au message pour l'accessibilité
        field.setAttribute('aria-describedby', `${field.id}-message`);
    }

    validateField(field) {
        const fieldId = field.id;
        const fieldData = this.fields.get(fieldId);
        
        if (!fieldData) return;

        // Debounce la validation
        if (this.debounceTimeouts.has(fieldId)) {
            clearTimeout(this.debounceTimeouts.get(fieldId));
        }

        this.debounceTimeouts.set(fieldId, setTimeout(() => {
            this.performValidation(fieldId);
        }, 300));
    }

    performValidation(fieldId) {
        const fieldData = this.fields.get(fieldId);
        if (!fieldData) return;

        const { element, rules, options } = fieldData;
        const value = element.value;
        
        // Afficher l'indicateur de chargement
        this.showLoadingIndicator(element);

        // Effectuer la validation
        const validationResult = this.validateValue(value, rules);
        
        // Mettre à jour l'état du champ
        fieldData.isValid = validationResult.isValid;
        fieldData.lastValue = value;

        // Mettre à jour l'interface
        setTimeout(() => {
            this.updateFieldUI(element, validationResult);
            
            // Mettre à jour l'indicateur de force si c'est un mot de passe
            if (options.type === 'password' && options.showStrength) {
                this.updatePasswordStrength(element, value);
            }
            
            // Afficher les suggestions si demandées
            if (options.showSuggestions) {
                this.updateSuggestions(element, value, validationResult);
            }
        }, 200);
    }

    validateValue(value, rules) {
        const errors = [];
        const warnings = [];
        
        for (const rule of rules) {
            let ruleObj;
            
            if (typeof rule === 'string') {
                ruleObj = this.rules[rule];
            } else if (typeof rule === 'object') {
                ruleObj = rule;
            } else if (typeof rule === 'function') {
                ruleObj = rule();
            }

            if (ruleObj && !ruleObj.test(value)) {
                if (ruleObj.severity === 'warning') {
                    warnings.push(ruleObj.message);
                } else {
                    errors.push(ruleObj.message);
                }
            }
        }

        return {
            isValid: errors.length === 0,
            errors: errors,
            warnings: warnings,
            hasWarnings: warnings.length > 0
        };
    }

    updateFieldUI(field, validationResult) {
        const { isValid, errors, warnings } = validationResult;
        
        // Mettre à jour les classes CSS
        field.classList.remove('valid', 'invalid');
        field.classList.add(isValid ? 'valid' : 'invalid');
        
        // Mettre à jour l'attribut aria-invalid
        field.setAttribute('aria-invalid', !isValid);
        
        // Mettre à jour le message
        const messageContainer = document.getElementById(`${field.id}-message`);
        if (messageContainer) {
            messageContainer.innerHTML = '';
            messageContainer.classList.remove('show', 'error', 'success', 'warning');
            
            if (errors.length > 0) {
                messageContainer.textContent = errors[0];
                messageContainer.classList.add('show', 'error');
            } else if (warnings.length > 0) {
                messageContainer.textContent = warnings[0];
                messageContainer.classList.add('show', 'warning');
            } else if (field.value.trim()) {
                messageContainer.textContent = 'Valide ✓';
                messageContainer.classList.add('show', 'success');
            }
        }
        
        // Cacher l'indicateur de chargement
        this.hideLoadingIndicator(field);
    }

    setupPasswordStrength(field) {
        const wrapper = field.closest('.validation-field');
        if (!wrapper) return;

        const strengthContainer = document.createElement('div');
        strengthContainer.className = 'password-strength';
        strengthContainer.innerHTML = `
            <div class="strength-bar">
                <div class="strength-fill"></div>
            </div>
            <div class="strength-text">Tapez votre mot de passe</div>
        `;
        
        wrapper.appendChild(strengthContainer);
        
        this.strengthIndicators.set(field.id, {
            container: strengthContainer,
            bar: strengthContainer.querySelector('.strength-fill'),
            text: strengthContainer.querySelector('.strength-text')
        });
    }

    updatePasswordStrength(field, password) {
        const indicator = this.strengthIndicators.get(field.id);
        if (!indicator) return;

        const strength = this.calculatePasswordStrength(password);
        
        // Mettre à jour la barre
        indicator.bar.className = `strength-fill strength-${strength.level}`;
        
        // Mettre à jour le texte
        indicator.text.textContent = strength.text;
        
        // Mettre à jour l'attribut aria pour l'accessibilité
        indicator.container.setAttribute('aria-label', `Force du mot de passe : ${strength.text}`);
    }

    calculatePasswordStrength(password) {
        let score = 0;
        let feedback = [];

        if (password.length >= 8) score += 1;
        else feedback.push('8 caractères minimum');

        if (/[a-z]/.test(password)) score += 1;
        else feedback.push('minuscules');

        if (/[A-Z]/.test(password)) score += 1;
        else feedback.push('majuscules');

        if (/\d/.test(password)) score += 1;
        else feedback.push('chiffres');

        if (/[@$!%*?&]/.test(password)) score += 1;
        else feedback.push('caractères spéciaux');

        const levels = {
            0: { level: 'weak', text: 'Très faible' },
            1: { level: 'weak', text: 'Faible' },
            2: { level: 'fair', text: 'Moyen' },
            3: { level: 'good', text: 'Bon' },
            4: { level: 'good', text: 'Très bon' },
            5: { level: 'strong', text: 'Excellent' }
        };

        return levels[score] || levels[0];
    }

    updateSuggestions(field, value, validationResult) {
        const suggestionsContainer = document.getElementById(`${field.id}-suggestions`);
        if (!suggestionsContainer) return;

        // Générer les suggestions basées sur le type de champ
        const suggestions = this.generateSuggestions(field, value, validationResult);
        
        if (suggestions.length > 0) {
            suggestionsContainer.innerHTML = `
                <ul>
                    ${suggestions.map(suggestion => `
                        <li class="${suggestion.completed ? 'completed' : ''}">
                            ${suggestion.text}
                        </li>
                    `).join('')}
                </ul>
            `;
            suggestionsContainer.style.display = 'block';
        } else {
            suggestionsContainer.style.display = 'none';
        }
    }

    generateSuggestions(field, value, validationResult) {
        const suggestions = [];
        const fieldData = this.fields.get(field.id);
        
        if (!fieldData || !fieldData.options.showSuggestions) return suggestions;

        // Suggestions pour les mots de passe
        if (fieldData.options.type === 'password') {
            suggestions.push(
                { text: 'Au moins 8 caractères', completed: value.length >= 8 },
                { text: 'Une majuscule', completed: /[A-Z]/.test(value) },
                { text: 'Une minuscule', completed: /[a-z]/.test(value) },
                { text: 'Un chiffre', completed: /\d/.test(value) },
                { text: 'Un caractère spécial', completed: /[@$!%*?&]/.test(value) }
            );
        }

        // Suggestions pour les emails
        if (fieldData.options.type === 'email') {
            const hasAt = value.includes('@');
            const hasDot = value.includes('.');
            
            suggestions.push(
                { text: 'Contient @', completed: hasAt },
                { text: 'Contient un domaine', completed: hasAt && hasDot },
                { text: 'Format valide', completed: validationResult.isValid }
            );
        }

        return suggestions;
    }

    showLoadingIndicator(field) {
        const indicator = field.parentElement.querySelector('.validation-indicator');
        if (indicator) {
            indicator.className = 'validation-indicator loading show';
        }
    }

    hideLoadingIndicator(field) {
        const indicator = field.parentElement.querySelector('.validation-indicator');
        if (indicator) {
            indicator.className = 'validation-indicator';
        }
    }

    onFieldFocus(field) {
        // Afficher les suggestions si configurées
        const fieldData = this.fields.get(field.id);
        if (fieldData && fieldData.options.showSuggestions) {
            const suggestionsContainer = document.getElementById(`${field.id}-suggestions`);
            if (suggestionsContainer) {
                suggestionsContainer.style.display = 'block';
            }
        }
    }

    onFieldBlur(field) {
        // Validation immédiate au blur
        this.validateField(field);
    }

    validateForm(form, event) {
        event.preventDefault();
        
        const fields = form.querySelectorAll('[data-validate]');
        let isFormValid = true;
        const errors = [];

        // Valider tous les champs
        fields.forEach(field => {
            this.performValidation(field.id);
            const fieldData = this.fields.get(field.id);
            
            if (fieldData && !fieldData.isValid) {
                isFormValid = false;
                errors.push({
                    field: field.id,
                    message: this.getFieldError(field.id)
                });
            }
        });

        // Afficher les résultats
        if (isFormValid) {
            this.showNotification('Formulaire valide ! ✓', 'success');
            
            // Déclencher un événement personnalisé
            form.dispatchEvent(new CustomEvent('validation:success', {
                detail: { form: form }
            }));
        } else {
            this.showNotification(`${errors.length} erreur(s) dans le formulaire`, 'error');
            
            // Faire défiler vers le premier champ en erreur
            const firstErrorField = document.getElementById(errors[0].field);
            if (firstErrorField) {
                firstErrorField.scrollIntoView({ behavior: 'smooth', block: 'center' });
                firstErrorField.focus();
            }
            
            // Déclencher un événement personnalisé
            form.dispatchEvent(new CustomEvent('validation:error', {
                detail: { form: form, errors: errors }
            }));
        }

        return isFormValid;
    }

    getFieldError(fieldId) {
        const messageContainer = document.getElementById(`${fieldId}-message`);
        return messageContainer ? messageContainer.textContent : '';
    }

    showNotification(message, type = 'info') {
        const container = document.getElementById('validation-notifications');
        if (!container) return;

        const notification = document.createElement('div');
        notification.className = `validation-notification ${type}`;
        notification.innerHTML = `
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <i class="fas fa-${type === 'success' ? 'check' : type === 'error' ? 'times' : 'info'}-circle"></i>
                <span>${message}</span>
            </div>
        `;

        container.appendChild(notification);

        // Animer l'apparition
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);

        // Supprimer après 4 secondes
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 4000);
    }

    // Méthodes utilitaires
    getFieldData(fieldId) {
        return this.fields.get(fieldId);
    }

    isFieldValid(fieldId) {
        const fieldData = this.fields.get(fieldId);
        return fieldData ? fieldData.isValid : false;
    }

    isFormValid(formId) {
        const form = document.getElementById(formId);
        if (!form) return false;

        const fields = form.querySelectorAll('[data-validate]');
        for (const field of fields) {
            if (!this.isFieldValid(field.id)) {
                return false;
            }
        }
        return true;
    }

    reset(fieldId) {
        const fieldData = this.fields.get(fieldId);
        if (!fieldData) return;

        const { element } = fieldData;
        
        // Réinitialiser les classes
        element.classList.remove('valid', 'invalid');
        element.setAttribute('aria-invalid', 'false');
        
        // Réinitialiser le message
        const messageContainer = document.getElementById(`${fieldId}-message`);
        if (messageContainer) {
            messageContainer.innerHTML = '';
            messageContainer.classList.remove('show', 'error', 'success', 'warning');
        }
        
        // Réinitialiser les suggestions
        const suggestionsContainer = document.getElementById(`${fieldId}-suggestions`);
        if (suggestionsContainer) {
            suggestionsContainer.style.display = 'none';
        }
        
        // Réinitialiser l'indicateur de force
        if (fieldData.options.type === 'password') {
            this.updatePasswordStrength(element, '');
        }
    }
}

// Initialiser le moteur de validation
const ValidationEngine = new ValidationEngine();

// Exporter pour utilisation globale
window.ValidationEngine = ValidationEngine;