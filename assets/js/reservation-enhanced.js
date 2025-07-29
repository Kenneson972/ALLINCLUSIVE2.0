// RESERVATION ENHANCED JS - Gestion paramètres URL et pré-remplissage automatique

// 🏠 BASE DE DONNÉES DES VILLAS - CORRECTION PRIORITÉ 1
const villaData = {
    'bas-de-f3-sur-le-robert': {
        id: 'bas-de-f3-sur-le-robert',
        nom: 'Bas de villa F3 sur le Robert',
        localisation: 'Pointe Hyacinthe, Le Robert',
        prix: 900,
        capacite: 10,
        chambres: 2,
        sallesDeBain: 1,
        surface: 120,
        description: 'Villa moderne avec terrasses panoramiques au Robert',
        image: '/ALLINCLUSIVE2.0/images/Villa_F3_Robert_Pointe_Hyacinthe/01_piscine_rectangulaire.jpg'
    },
    'villa-f3-petit-macabou': {
        id: 'villa-f3-petit-macabou',
        nom: 'Villa F3 sur Petit Macabou',
        localisation: 'Petit Macabou, Vauclin',
        prix: 1550,
        capacite: 6,
        chambres: 3,
        sallesDeBain: 2,
        surface: 140,
        description: 'Villa F3 moderne au Petit Macabou avec possibilité journée',
        image: '/ALLINCLUSIVE2.0/images/Villa_F3_Petit_Macabou/01_piscine_exterieur.jpg'
    },
    'villa-f3-pour-la-baccha': {
        id: 'villa-f3-pour-la-baccha',
        nom: 'Villa F3 POUR LA BACCHA',
        localisation: 'Petit Macabou',
        prix: 750,
        capacite: 6,
        chambres: 2,
        sallesDeBain: 1,
        surface: 120,
        description: 'Villa F3 à la Baccha avec invités journée',
        image: '/ALLINCLUSIVE2.0/images/Villa_F3_Baccha_Petit_Macabou/01_terrasse_piscine_salon_ext.jpg'
    },
    'villa-f3-sur-le-francois': {
        id: 'villa-f3-sur-le-francois',
        nom: 'Villa F3 sur le François',
        localisation: 'Hauteurs du Morne Carrière au François',
        prix: 800,
        capacite: 4,
        chambres: 2,
        sallesDeBain: 1,
        surface: 110,
        description: 'Villa F3 panoramique au François',
        image: '/ALLINCLUSIVE2.0/images/Villa_F3_Le_Francois/01_terrasse_panoramique_vue_mer.jpg'
    },
    'villa-f5-sur-ste-anne': {
        id: 'villa-f5-sur-ste-anne',
        nom: 'Villa F5 sur Ste Anne',
        localisation: 'Quartier les Anglais, Ste Anne',
        prix: 1350,
        capacite: 10,
        chambres: 4,
        sallesDeBain: 4,
        surface: 200,
        description: 'Villa F5 spacieuse à Ste Anne avec invités journée',
        image: '/ALLINCLUSIVE2.0/images/Villa_F5_Ste_Anne/01_piscine_principale.jpg'
    },
    'villa-f6-au-lamentin': {
        id: 'villa-f6-au-lamentin',
        nom: 'Villa F6 au Lamentin',
        localisation: 'Quartier Béleme, Lamentin',
        prix: 1200,
        capacite: 12,
        chambres: 5,
        sallesDeBain: 4,
        surface: 250,
        description: 'Villa F6 avec piscine et jacuzzi au Lamentin',
        image: '/ALLINCLUSIVE2.0/images/Villa_F6_Lamentin/01_piscine_jacuzzi_vue_ensemble.jpg'
    },
    'villa-f6-sur-ste-luce-a-1mn-de-la-plage': {
        id: 'villa-f6-sur-ste-luce-a-1mn-de-la-plage',
        nom: 'Villa F6 sur Ste Luce à 1mn de la plage',
        localisation: 'Zac de Pont Café, Ste Luce',
        prix: 1800,
        capacite: 14,
        chambres: 5,
        sallesDeBain: 5,
        surface: 280,
        description: 'Villa F6 complexe près de la plage Corps de garde',
        image: '/ALLINCLUSIVE2.0/images/Villa_F6_Ste_Luce_Plage/02_chambre_poutres.jpg'
    },
    'villa-f7-baie-des-mulets': {
        id: 'villa-f7-baie-des-mulets',
        nom: 'Villa F7 Baie des Mulets',
        localisation: 'Baie des Mulets, Vauclin',
        prix: 2200,
        capacite: 16,
        chambres: 7,
        sallesDeBain: 6,
        surface: 350,
        description: 'Villa F7 exceptionnelle (F5+F3) à Baie des Mulets',
        image: '/ALLINCLUSIVE2.0/images/Villa_F7_Baie_des_Mulets_Vauclin/01_chambre_climatisee.jpg'
    },
    'villa-f3-bas-de-villa-trinite-cosmy': {
        id: 'villa-f3-bas-de-villa-trinite-cosmy',
        nom: 'Villa F3 Bas de villa Trinité Cosmy',
        localisation: 'Cosmy, Trinité',
        prix: 500,
        capacite: 5,
        chambres: 2,
        sallesDeBain: 1,
        surface: 100,
        description: 'Bas de villa charmant avec piscine chauffée',
        image: '/ALLINCLUSIVE2.0/images/Villa_F3_Trinite_Cosmy/01_piscine_chauffee_vue_collines.jpg'
    },
    'villa-f5-vauclin-ravine-plate': {
        id: 'villa-f5-vauclin-ravine-plate',
        nom: 'Villa F5 Vauclin Ravine Plate',
        localisation: 'Hauteurs de Ravine Plate, Vauclin',
        prix: 1550,
        capacite: 8,
        chambres: 4,
        sallesDeBain: 4,
        surface: 180,
        description: 'Villa F5 avec piscine à débordement panoramique',
        image: '/ALLINCLUSIVE2.0/images/Villa_F5_Vauclin_Ravine_Plate/01_piscine_debordement_vue_panoramique.jpg'
    },
    'villa-f5-la-renee': {
        id: 'villa-f5-la-renee',
        nom: 'Villa F5 La Renée',
        localisation: 'Quartier La Renée, Rivière-Pilote',
        prix: 900,
        capacite: 10,
        chambres: 4,
        sallesDeBain: 2,
        surface: 170,
        description: 'Villa F5 avec jacuzzi et grande terrasse',
        image: '/ALLINCLUSIVE2.0/images/Villa_F5_R_Pilote_La_Renee/01_terrasse_bois_piscine_palmiers.jpg'
    },
    'bas-villa-f3-sur-ste-luce': {
        id: 'bas-villa-f3-sur-ste-luce',
        nom: 'Bas de villa F3 sur Ste Luce',
        localisation: 'Sainte-Luce',
        prix: 570,
        capacite: 6,
        chambres: 2,
        sallesDeBain: 1,
        surface: 90,
        description: 'Bas de villa cosy à Sainte-Luce',
        image: '/ALLINCLUSIVE2.0/images/Bas_Villa_F3_Ste_Luce/01_eclairage_led_terrasse_lounge.jpg'
    },
    'studio-cocooning-lamentin': {
        id: 'studio-cocooning-lamentin',
        nom: 'Studio Cocooning Lamentin',
        localisation: 'Hauteurs de Morne Pitault, Lamentin',
        prix: 290,
        capacite: 2,
        chambres: 1,
        sallesDeBain: 1,
        surface: 45,
        description: 'Studio cocooning avec bac à punch privé',
        image: '/ALLINCLUSIVE2.0/images/Studio_Cocooning_Lamentin/01_jacuzzi_terrasse_privee.jpg'
    },
    'villa-f6-sur-petit-macabou': {
        id: 'villa-f6-sur-petit-macabou',
        nom: 'Villa F6 sur Petit Macabou (séjour + fête)',
        localisation: 'Petit Macabou au Vauclin',
        prix: 2000,
        capacite: 13,
        chambres: 6,
        sallesDeBain: 6,
        surface: 320,
        description: 'Villa F6 somptueuse avec possibilité événements',
        image: '/ALLINCLUSIVE2.0/images/Villa_F6_Petit_Macabou/02_salle_de_bain.jpg'
    },
    'appartement-f3-trenelle': {
        id: 'appartement-f3-trenelle',
        nom: 'Appartement F3 Trenelle (Location Annuelle)',
        localisation: 'Trenelle, à 2 minutes du PPM',
        prix: 700,
        capacite: 2,
        chambres: 2,
        sallesDeBain: 1,
        surface: 80,
        description: 'Appartement F3 meublé pour location annuelle',
        image: '/ALLINCLUSIVE2.0/images/Villa_F3_Trenelle_Location_Annuelle/01_cuisine_equipee_evier_double.jpg'
    }
};

// Rendre accessible globalement
window.villaData = villaData;

class ReservationEnhanced {
    constructor() {
        this.init();
        this.disableDebugMode(); // CORRECTION PRIORITÉ 2
    }

    init() {
        this.handleURLParameters();
        this.initializeFormEnhancements();
        this.initializeSmartValidation();
    }

    // 🚫 CORRECTION PRIORITÉ 2 : Désactiver le mode debug
    disableDebugMode() {
        // Supprimer tous les éléments de debug
        document.querySelectorAll('.debug-number, .element-index, [data-debug], [class*="debug"], [class*="number-overlay"]').forEach(el => {
            el.remove();
        });

        // Désactiver les variables de debug
        window.DEBUG_MODE = false;
        window.SHOW_ELEMENT_INDICES = false;

        // Supprimer les styles de debug
        const debugStyles = document.querySelectorAll('style[data-debug]');
        debugStyles.forEach(style => style.remove());

        // Ajouter styles pour masquer définitivement
        const hideDebugStyle = document.createElement('style');
        hideDebugStyle.innerHTML = `
            .debug-number,
            .element-index,
            [data-debug],
            [class*="debug"],
            [class*="number-overlay"] {
                display: none !important;
                visibility: hidden !important;
            }
        `;
        document.head.appendChild(hideDebugStyle);

        console.log('🚫 Mode debug désactivé');
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
            submitBtn.innerHTML = '⏳ Envoi en cours...';
            submitBtn.style.opacity = '0.7';
        }
    }

    // ÉTAT DE SUCCÈS
    showSuccessState(form) {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.innerHTML = '✅ Envoyé!';
            submitBtn.style.background = '#48bb78';
            
            setTimeout(() => {
                submitBtn.disabled = false;
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