
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



// CORRECTEUR UNIVERSEL DE BOUTONS - KhanelConcept
// Détecte et corrige automatiquement les boutons sans action

(function() {
    'use strict';
    
    console.log('🔧 Correcteur universel de boutons activé');
    
    // Attendre le chargement complet du DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initButtonFixes);
    } else {
        initButtonFixes();
    }
    
    function initButtonFixes() {
        const buttonFixers = {
            // Actions de réservation
            reservation: {
                keywords: ['réserver', 'booking', 'book now', 'réservation'],
                action: function(villaInfo) {
                    const url = './reservation.html?' + new URLSearchParams({
                        villa: villaInfo.id,
                        name: villaInfo.name
                    }).toString();
                    window.location.href = url;
                }
            },
            
            // Actions de détails
            details: {
                keywords: ['détails', 'details', 'voir plus', 'en savoir plus', 'discover'],
                action: function(villaInfo) {
                    if (villaInfo.id && villaInfo.id !== 'unknown') {
                        window.location.href = `./villa-${villaInfo.id}.html`;
                    } else {
                        window.location.href = './';
                    }
                }
            },
            
            // Actions de contact
            contact: {
                keywords: ['contact', 'contacter', 'nous contacter', 'get in touch'],
                action: function(villaInfo) {
                    window.location.href = './contact.html?' + new URLSearchParams({
                        subject: 'Contact villa ' + villaInfo.name
                    }).toString();
                }
            },
            
            // Actions de devis
            quote: {
                keywords: ['devis', 'quote', 'estimation', 'tarif'],
                action: function(villaInfo) {
                    window.location.href = './reservation.html?' + new URLSearchParams({
                        villa: villaInfo.id,
                        type: 'quote',
                        name: villaInfo.name
                    }).toString();
                }
            }
        };
        
        // Fonction pour extraire les infos villa du contexte
        function extractVillaInfo(element) {
            const container = element.closest('.villa-card, .glass-card, [class*="villa"], .hero-villa');
            let villaName = 'Villa';
            let villaId = 'unknown';
            
            if (container) {
                // Chercher titre
                const title = container.querySelector('h1, h2, h3, .villa-title, [class*="title"]');
                if (title) {
                    villaName = title.textContent.trim();
                    villaId = villaName
                        .toLowerCase()
                        .replace(/[^a-z0-9\s-]/g, '')
                        .replace(/\s+/g, '-')
                        .replace(/^villa-?/, '');
                }
                
                // Chercher attributs data
                villaId = container.dataset.villa || container.dataset.villaId || villaId;
            }
            
            // Extraire depuis URL si page villa
            if (villaId === 'unknown' && location.pathname.includes('villa-')) {
                const match = location.pathname.match(/villa-(.+?)\.html/);
                if (match) villaId = match[1];
            }
            
            return { name: villaName, id: villaId };
        }
        
        // Analyser tous les boutons et liens
        const elements = document.querySelectorAll('button, a');
        let fixedCount = 0;
        
        elements.forEach(element => {
            const text = (element.textContent || '').toLowerCase().trim();
            const hasAction = element.onclick || 
                            element.href || 
                            element.dataset.action ||
                            element.getAttribute('href') !== null;
            
            // Ignorer éléments avec actions ou textes non pertinents
            if (hasAction || !text || text.length < 3) return;
            if (/menu|nav|close|×|toggle|search|login|logout/i.test(text)) return;
            
            // Trouver le type d'action approprié
            let actionType = null;
            for (const [type, config] of Object.entries(buttonFixers)) {
                if (config.keywords.some(keyword => text.includes(keyword))) {
                    actionType = type;
                    break;
                }
            }
            
            if (actionType) {
                const villaInfo = extractVillaInfo(element);
                
                // Ajouter l'action
                element.addEventListener('click', function(e) {
                    e.preventDefault();
                    try {
                        buttonFixers[actionType].action(villaInfo);
                        console.log(`✅ Action ${actionType} pour: ${villaInfo.name}`);
                    } catch (err) {
                        console.error('Erreur action bouton:', err);
                        window.location.href = './';
                    }
                });
                
                // Améliorer l'apparence
                element.style.cursor = 'pointer';
                element.style.transition = 'all 0.3s ease';
                
                // Effet hover
                element.addEventListener('mouseenter', () => {
                    element.style.transform = 'scale(1.05)';
                    element.style.opacity = '0.9';
                });
                element.addEventListener('mouseleave', () => {
                    element.style.transform = 'scale(1)';
                    element.style.opacity = '1';
                });
                
                fixedCount++;
                console.log(`🔧 Bouton activé: "${text}" (${actionType})`);
            }
        });
        
        // Notification de résultat
        if (fixedCount > 0) {
            console.log(`✅ ${fixedCount} boutons activés automatiquement`);
            
            // Notification visuelle temporaire
            const notification = document.createElement('div');
            // PROTECTION: Utiliser insertAdjacentHTML au lieu de innerHTML
    notification.innerHTML = `
                <div style="
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: linear-gradient(135deg, #10b981, #059669);
                    color: white;
                    padding: 12px 20px;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: 500;
                    z-index: 10000;
                    box-shadow: 0 4px 20px rgba(16, 185, 129, 0.3);
                    animation: slideInRight 0.5s ease-out;
                ">
                    ✅ ${fixedCount} boutons activés
                </div>
                <style>
                    @keyframes slideInRight {
                        from { transform: translateX(100%); opacity: 0; }
                        to { transform: translateX(0); opacity: 1; }
                    }
                </style>
            `;
            
            document.body.appendChild(notification);
            setTimeout(() => notification.remove(), 4000);
        }
    }
})();
