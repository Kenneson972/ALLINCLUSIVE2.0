// KhanelConcept Glassmorphism JavaScript - Interactions pour toutes les pages villa

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    initializeGlassmorphism();
    initializeVideoBackground();
    initializeGallery();
    initializeBookingForm();
    initializeScrollEffects();
});

// Initialisation des effets glassmorphism
function initializeGlassmorphism() {
    // Animation des cartes au scroll
    const cards = document.querySelectorAll('.glass-card');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });

    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.6s ease';
        observer.observe(card);
    });
}

// Initialisation du background vidéo avec support iOS
function initializeVideoBackground() {
    const video = document.querySelector('.video-background video');
    if (video) {
        // Configuration iOS
        video.setAttribute('webkit-playsinline', 'webkit-playsinline');
        video.setAttribute('playsinline', 'playsinline');
        
        // Détection iOS
        const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
        
        if (isIOS) {
            // Fallback pour iOS
            video.muted = true;
            video.preload = 'metadata';
            
            // Tentative de lecture automatique
            const playPromise = video.play();
            if (playPromise !== undefined) {
                playPromise.catch(error => {
                    console.log('Autoplay failed on iOS, adding touch listener');
                    document.addEventListener('touchstart', () => {
                        video.play();
                    }, { once: true });
                });
            }
        } else {
            // Lecture normale pour autres navigateurs
            video.play().catch(error => {
                console.log('Video autoplay failed:', error);
            });
        }
    }
}

// Initialisation de la galerie photos
function initializeGallery() {
    const photos = document.querySelectorAll('.photo-slider img');
    
    photos.forEach(photo => {
        photo.addEventListener('click', function() {
            openPhotoModal(this.src, this.alt);
        });
    });
}

// Ouverture du modal photo
function openPhotoModal(src, alt) {
    const modal = document.createElement('div');
    modal.className = 'photo-modal';
    modal.innerHTML = `
        <div class="modal-backdrop">
            <div class="modal-content">
                <span class="modal-close">&times;</span>
                <img src="${src}" alt="${alt}">
            </div>
        </div>
    `;
    
    // Styles du modal
    const modalStyles = `
        .photo-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 2000;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .modal-backdrop {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(10px);
            cursor: pointer;
        }
        
        .modal-content {
            position: relative;
            max-width: 90%;
            max-height: 90%;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .modal-content img {
            max-width: 100%;
            max-height: 100%;
            border-radius: 15px;
        }
        
        .modal-close {
            position: absolute;
            top: 10px;
            right: 20px;
            font-size: 30px;
            color: white;
            cursor: pointer;
            z-index: 2001;
        }
    `;
    
    // Ajout des styles
    if (!document.getElementById('modal-styles')) {
        const styleEl = document.createElement('style');
        styleEl.id = 'modal-styles';
        styleEl.textContent = modalStyles;
        document.head.appendChild(styleEl);
    }
    
    document.body.appendChild(modal);
    
    // Fermeture du modal
    const closeModal = () => {
        document.body.removeChild(modal);
    };
    
    modal.querySelector('.modal-close').addEventListener('click', closeModal);
    modal.querySelector('.modal-backdrop').addEventListener('click', closeModal);
    
    // Fermeture avec Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeModal();
        }
    });
}

// Initialisation du formulaire de réservation
function initializeBookingForm() {
    const form = document.querySelector('.booking-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            handleBookingSubmission(this);
        });
        
        // Validation en temps réel
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
        });
    }
}

// Gestion de la soumission du formulaire
function handleBookingSubmission(form) {
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);
    
    // Validation
    if (!validateForm(data)) {
        return;
    }
    
    // Simulation d'envoi
    showNotification('Demande de réservation envoyée avec succès!', 'success');
    
    // Ici vous pouvez ajouter l'intégration avec votre backend
    console.log('Booking data:', data);
}

// Validation des champs
function validateField(field) {
    const value = field.value.trim();
    let isValid = true;
    
    // Validation selon le type de champ
    switch (field.type) {
        case 'email':
            isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
            break;
        case 'tel':
            isValid = /^[0-9+\-\s()]+$/.test(value);
            break;
        case 'date':
            isValid = new Date(value) > new Date();
            break;
        default:
            isValid = value.length > 0;
    }
    
    // Affichage de l'état
    field.style.borderColor = isValid ? 'rgba(72, 187, 120, 0.5)' : 'rgba(245, 101, 101, 0.5)';
    
    return isValid;
}

// Validation complète du formulaire
function validateForm(data) {
    const required = ['name', 'email', 'phone', 'checkin', 'checkout', 'guests', 'stay_type'];
    
    for (let field of required) {
        if (!data[field] || data[field].trim() === '') {
            showNotification(`Le champ "${field}" est obligatoire`, 'error');
            return false;
        }
    }
    
    // Validation des dates
    const checkin = new Date(data.checkin);
    const checkout = new Date(data.checkout);
    
    if (checkin >= checkout) {
        showNotification('La date de départ doit être après la date d\'arrivée', 'error');
        return false;
    }
    
    if (checkin <= new Date()) {
        showNotification('La date d\'arrivée doit être future', 'error');
        return false;
    }
    
    return true;
}

// Système de notifications
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    const styles = `
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 10px;
            color: white;
            font-weight: 500;
            z-index: 3000;
            opacity: 0;
            transform: translateX(100px);
            transition: all 0.3s ease;
        }
        
        .notification-success {
            background: rgba(72, 187, 120, 0.9);
            border: 1px solid rgba(72, 187, 120, 0.3);
        }
        
        .notification-error {
            background: rgba(245, 101, 101, 0.9);
            border: 1px solid rgba(245, 101, 101, 0.3);
        }
        
        .notification-info {
            background: rgba(66, 153, 225, 0.9);
            border: 1px solid rgba(66, 153, 225, 0.3);
        }
    `;
    
    // Ajout des styles
    if (!document.getElementById('notification-styles')) {
        const styleEl = document.createElement('style');
        styleEl.id = 'notification-styles';
        styleEl.textContent = styles;
        document.head.appendChild(styleEl);
    }
    
    document.body.appendChild(notification);
    
    // Animation d'entrée
    setTimeout(() => {
        notification.style.opacity = '1';
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Suppression automatique
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100px)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 5000);
}

// Effets de scroll
function initializeScrollEffects() {
    let scrollTimeout;
    
    window.addEventListener('scroll', function() {
        const header = document.querySelector('.glass-header');
        if (header) {
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        }
        
        // Parallax léger pour les cartes
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(() => {
            const cards = document.querySelectorAll('.glass-card');
            cards.forEach(card => {
                const rect = card.getBoundingClientRect();
                const scrolled = window.pageYOffset;
                const rate = scrolled * -0.5;
                
                if (rect.top <= window.innerHeight && rect.bottom >= 0) {
                    card.style.transform = `translateY(${rate}px)`;
                }
            });
        }, 10);
    });
}

// Fonction utilitaire pour le formatage des prix
function formatPrice(price) {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR'
    }).format(price);
}

// Fonction pour calculer le prix total
function calculateTotalPrice(basePrice, nights, guests, stayType) {
    let multiplier = 1;
    
    // Multiplicateurs selon le type de séjour
    switch (stayType) {
        case 'weekend':
            multiplier = 1;
            break;
        case 'semaine':
            multiplier = 0.85; // Réduction semaine
            break;
        case 'fete':
            multiplier = 1.3; // Supplément fête
            break;
    }
    
    return basePrice * nights * multiplier;
}

// Export des fonctions pour utilisation externe
window.KhanelConcept = {
    formatPrice,
    calculateTotalPrice,
    showNotification,
    openPhotoModal
};