// KHANELCONCEPT - Utilitaires JavaScript

// Gestion des notifications
function showNotification(message, type = 'info') {
    console.log(`[${type.toUpperCase()}] ${message}`);
    // TODO: Implémenter notifications visuelles
}

// Validation email
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Formatage prix
function formatPrice(price) {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR'
    }).format(price);
}

// Initialisation vidéo background universelle
function initUniversalVideoBackground() {
    const video = document.querySelector('#backgroundVideo, .video-background video');
    if (video) {
        video.muted = true;
        video.loop = true;
        video.play().catch(() => console.log('Autoplay bloqué'));
    }
}

// Initialiser au chargement
document.addEventListener('DOMContentLoaded', initUniversalVideoBackground);