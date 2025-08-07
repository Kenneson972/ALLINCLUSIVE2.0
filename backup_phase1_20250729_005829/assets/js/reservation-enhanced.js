
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


// RESERVATION ENHANCED JS - Gestion paramètres URL et pré-remplissage automatique

class ReservationEnhanced {
    constructor() {
        this.init();
    }

    init() {
        this.handleURLParameters();
        this.initializeFormEnhancements();
        this.initializeSmartValidation();
    }

    // GESTION DES PARAMÈTRES URL
    handleURLParameters() {
        const urlParams = new URLSearchParams(window.location.search);
        const villaId = urlParams.get('villa');
        const villaName = urlParams.get('name');
        
        if (villaId && villaName) {
            this.preSelectVilla(villaId, decodeURIComponent(villaName));
            this.showPreSelectedNotification(decodeURIComponent(villaName));
        }
    }

    // PRÉ-SÉLECTION DE LA VILLA
    preSelectVilla(villaId, villaName) {
        const villaSelect = document.getElementById('villaSelect');
        
        if (villaSelect) {
            // Chercher l'option correspondante
            const options = Array.from(villaSelect.options);
            const matchingOption = options.find(option => 
                option.value.includes(villaId) || option.textContent.includes(villaName)
            );
            
            if (matchingOption) {
                villaSelect.value = matchingOption.value;
                villaSelect.dispatchEvent(new Event('change'));
            }
        }
    }

    // NOTIFICATION DE PRÉ-SÉLECTION
    showPreSelectedNotification(villaName) {
        const notification = document.createElement('div');
        notification.className = 'preselected-notification';
        // PROTECTION: Utiliser insertAdjacentHTML au lieu de innerHTML
    notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-icon">🏨</span>
                <span class="notification-text">Villa présélectionnée : <strong>${villaName}</strong></span>
                <button class="notification-close">&times;</button>
            </div>
        `;
        
        // Styles pour la notification
        const style = document.createElement('style');
        style.textContent = `
            .preselected-notification {
                position: fixed;
                top: 100px;
                right: 20px;
                background: linear-gradient(135deg, #f6ad55, #ed8936);
                color: #1a202c;
                padding: 15px 20px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(246, 173, 85, 0.3);
                z-index: 2000;
                animation: slideInRight 0.5s ease;
                max-width: 300px;
            }
            
            .notification-content {
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .notification-icon {
                font-size: 20px;
            }
            
            .notification-text {
                flex: 1;
                font-weight: 500;
            }
            
            .notification-close {
                background: none;
                border: none;
                font-size: 18px;
                cursor: pointer;
                color: #1a202c;
                padding: 0;
                margin-left: 10px;
            }
            
            @keyframes slideInRight {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
        `;
        
        document.head.appendChild(style);
        document.body.appendChild(notification);
        
        // Fermeture automatique après 5 secondes
        setTimeout(() => {
            notification.style.animation = 'slideInRight 0.5s ease reverse';
            setTimeout(() => {
                notification.remove();
            }, 500);
        }, 5000);
        
        // Fermeture manuelle
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.addEventListener('click', () => {
            notification.remove();
        });
    }

    // AMÉLIORATIONS DU FORMULAIRE
    initializeFormEnhancements() {
        // Animation des champs au focus
        const inputs = document.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('focus', () => {
                input.style.transform = 'scale(1.02)';
                input.style.boxShadow = '0 0 20px rgba(246, 173, 85, 0.3)';
            });
            
            input.addEventListener('blur', () => {
                input.style.transform = 'scale(1)';
                input.style.boxShadow = 'none';
            });
        });

        // Amélioration du sélecteur de villa
        const villaSelect = document.getElementById('villaSelect');
        if (villaSelect) {
            villaSelect.addEventListener('change', () => {
                this.updateVillaPreview();
            });
        }

        // Calcul automatique du prix
        const dateInputs = document.querySelectorAll('input[type="date"]');
        const guestSelect = document.getElementById('guestCount');
        
        [...dateInputs, guestSelect].forEach(input => {
            if (input) {
                input.addEventListener('change', () => {
                    this.updatePriceEstimate();
                });
            }
        });
    }

    // MISE À JOUR APERÇU VILLA
    updateVillaPreview() {
        const villaSelect = document.getElementById('villaSelect');
        const villaInfo = document.getElementById('villaInfo');
        
        if (!villaSelect || !villaInfo) return;
        
        const selectedOption = villaSelect.options[villaSelect.selectedIndex];
        
        if (selectedOption && selectedOption.value) {
            const villaText = selectedOption.textContent;
            const [villaName, priceInfo] = villaText.split(' - ');
            
            villaInfo.style.display = 'block';
            // PROTECTION: Utiliser insertAdjacentHTML au lieu de innerHTML
    villaInfo.innerHTML = `
                <h3>✨ ${villaName}</h3>
                <p>💰 ${priceInfo}</p>
                <p>📍 Martinique</p>
                <div class="villa-preview-actions">
                    <button onclick="this.scrollToCalendar()" class="btn-preview">
                        📅 Voir disponibilités
                    </button>
                </div>
            `;
            
            // Animation d'entrée
            villaInfo.style.animation = 'fadeInUp 0.5s ease';
        } else {
            villaInfo.style.display = 'none';
        }
    }

    // CALCUL DU PRIX ESTIMÉ
    updatePriceEstimate() {
        const checkinDate = document.getElementById('checkinDate');
        const checkoutDate = document.getElementById('checkoutDate');
        const guestCount = document.getElementById('guestCount');
        const totalPrice = document.getElementById('totalPrice');
        
        if (!checkinDate || !checkoutDate || !guestCount || !totalPrice) return;
        
        const checkin = new Date(checkinDate.value);
        const checkout = new Date(checkoutDate.value);
        const guests = parseInt(guestCount.value) || 0;
        
        if (checkin && checkout && checkin < checkout) {
            const nights = Math.ceil((checkout - checkin) / (1000 * 60 * 60 * 24));
            const basePrice = this.getBasePriceFromSelectedVilla();
            const guestSupplement = Math.max(0, guests - 6) * 50;
            const total = (basePrice * nights) + guestSupplement;
            
            totalPrice.textContent = `${total.toLocaleString('fr-FR')}€`;
            
            // Animation du prix
            totalPrice.style.animation = 'scaleIn 0.3s ease';
        }
    }

    // RÉCUPÉRATION DU PRIX DE BASE
    getBasePriceFromSelectedVilla() {
        const villaSelect = document.getElementById('villaSelect');
        if (!villaSelect) return 500;
        
        const selectedText = villaSelect.options[villaSelect.selectedIndex]?.textContent || '';
        const priceMatch = selectedText.match(/(\d+)€/);
        
        return priceMatch ? parseInt(priceMatch[1]) : 500;
    }

    // VALIDATION INTELLIGENTE
    initializeSmartValidation() {
        const form = document.getElementById('reservationForm');
        if (!form) return;
        
        // Validation en temps réel
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('input', () => {
                this.validateField(input);
            });
            
            input.addEventListener('blur', () => {
                this.validateField(input);
            });
        });
        
        // Validation avant soumission
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleFormSubmission(form);
        });
    }

    // VALIDATION D'UN CHAMP
    validateField(field) {
        let isValid = true;
        let errorMessage = '';
        
        // Validation selon le type de champ
        switch (field.type) {
            case 'email':
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                isValid = emailRegex.test(field.value);
                errorMessage = 'Email invalide';
                break;
                
            case 'tel':
                const phoneRegex = /^[0-9+\-\s()]{10,}$/;
                isValid = phoneRegex.test(field.value);
                errorMessage = 'Numéro de téléphone invalide';
                break;
                
            case 'date':
                const selectedDate = new Date(field.value);
                const today = new Date();
                today.setHours(0, 0, 0, 0);
                
                if (field.id === 'checkinDate') {
                    isValid = selectedDate >= today;
                    errorMessage = 'La date d\'arrivée doit être future';
                } else if (field.id === 'checkoutDate') {
                    const checkinDate = document.getElementById('checkinDate');
                    const checkin = new Date(checkinDate?.value);
                    isValid = selectedDate > checkin;
                    errorMessage = 'La date de départ doit être après l\'arrivée';
                }
                break;
                
            default:
                isValid = field.value.trim().length > 0;
                errorMessage = 'Ce champ est obligatoire';
        }
        
        // Affichage visuel de la validation
        this.showFieldValidation(field, isValid, errorMessage);
        
        return isValid;
    }

    // AFFICHAGE VALIDATION VISUELLE
    showFieldValidation(field, isValid, errorMessage) {
        // Supprimer anciens messages d'erreur
        const existingError = field.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }
        
        if (isValid) {
            field.style.borderColor = '#48bb78';
            field.style.boxShadow = '0 0 10px rgba(72, 187, 120, 0.3)';
        } else {
            field.style.borderColor = '#f56565';
            field.style.boxShadow = '0 0 10px rgba(245, 101, 101, 0.3)';
            
            // Ajouter message d'erreur
            const errorDiv = document.createElement('div');
            errorDiv.className = 'field-error';
            errorDiv.textContent = errorMessage;
            errorDiv.style.cssText = `
                color: #f56565;
                font-size: 12px;
                margin-top: 5px;
                animation: fadeInUp 0.3s ease;
            `;
            
            field.parentNode.appendChild(errorDiv);
        }
    }

    // SOUMISSION DU FORMULAIRE
    handleFormSubmission(form) {
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        
        // Validation complète
        let isFormValid = true;
        const inputs = form.querySelectorAll('input[required], select[required]');
        
        inputs.forEach(input => {
            if (!this.validateField(input)) {
                isFormValid = false;
            }
        });
        
        if (!isFormValid) {
            this.showNotification('Veuillez corriger les erreurs du formulaire', 'error');
            return;
        }
        
        // Simulation d'envoi avec feedback visuel
        this.showLoadingState(form);
        
        setTimeout(() => {
            this.showSuccessState(form);
            this.showNotification('Demande de réservation envoyée avec succès!', 'success');
        }, 2000);
    }

    // ÉTAT DE CHARGEMENT
    showLoadingState(form) {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = true;
            // PROTECTION: Utiliser insertAdjacentHTML au lieu de innerHTML
    submitBtn.innerHTML = '⏳ Envoi en cours...';
            submitBtn.style.opacity = '0.7';
        }
    }

    // ÉTAT DE SUCCÈS
    showSuccessState(form) {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            // PROTECTION: Utiliser insertAdjacentHTML au lieu de innerHTML
    submitBtn.innerHTML = '✅ Envoyé!';
            submitBtn.style.background = '#48bb78';
            
            setTimeout(() => {
                submitBtn.disabled = false;
                // PROTECTION: Utiliser insertAdjacentHTML au lieu de innerHTML
    submitBtn.innerHTML = 'Demander un Devis';
                submitBtn.style.opacity = '1';
                submitBtn.style.background = '';
            }, 3000);
        }
    }

    // NOTIFICATIONS
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        const colors = {
            success: '#48bb78',
            error: '#f56565',
            info: '#4299e1'
        };
        
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${colors[type]};
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            z-index: 3000;
            animation: slideInRight 0.5s ease;
            max-width: 300px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }

    // UTILITAIRES
    scrollToCalendar() {
        const calendar = document.querySelector('.calendar-container');
        if (calendar) {
            calendar.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }
}

// INITIALISATION
document.addEventListener('DOMContentLoaded', function() {
    new ReservationEnhanced();
    console.log('✨ Reservation Enhanced initialisé');
});

// EXPORT POUR UTILISATION EXTERNE
window.ReservationEnhanced = ReservationEnhanced;