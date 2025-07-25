// Script pour corriger le menu hamburger sur toutes les pages
// Ce script ne sera pas exécuté mais sert de template pour les corrections manuelles

const CSS_MOBILE_MENU = `
        /* Responsive Hamburger Menu */
        .mobile-nav-toggle {
            display: none;
        }
        
        @media (max-width: 768px) {
            .nav-links {
                display: none;
                visibility: hidden;
                opacity: 0;
            }
            
            .mobile-nav-toggle {
                display: block !important;
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                color: white;
                font-size: 1.2rem;
                cursor: pointer;
                padding: 0.5rem;
                transition: all 0.3s ease;
            }
            
            .mobile-nav-toggle:hover {
                background: rgba(255, 255, 255, 0.2);
                transform: scale(1.05);
            }
            
            .header-content {
                padding: 0 1rem;
            }
            
            /* Show mobile menu when active - GLASSMORPHISM AMÉLIORÉ */
            .nav-links.nav-menu.mobile-open {
                display: flex !important;
                visibility: visible !important;
                opacity: 1 !important;
                position: fixed !important;
                top: 60px !important;
                left: 0 !important;
                right: 0 !important;
                background: rgba(15, 25, 50, 0.85) !important;
                backdrop-filter: blur(40px) saturate(180%) !important;
                -webkit-backdrop-filter: blur(40px) saturate(180%) !important;
                padding: 2.5rem 1.5rem !important;
                border-radius: 0 0 25px 25px !important;
                flex-direction: column !important;
                gap: 1rem !important;
                z-index: 1000 !important;
                box-shadow: 
                    0 20px 60px rgba(0, 0, 0, 0.6),
                    0 8px 32px rgba(102, 126, 234, 0.15),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                animation: slideDownGlass 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
            }

            @keyframes slideDownGlass {
                0% {
                    opacity: 0;
                    transform: translateY(-20px) scale(0.95);
                    backdrop-filter: blur(0px);
                }
                100% {
                    opacity: 1;
                    transform: translateY(0) scale(1);
                    backdrop-filter: blur(40px) saturate(180%);
                }
            }

            @keyframes slideInStagger {
                0% {
                    opacity: 0;
                    transform: translateY(20px) scale(0.9);
                }
                100% {
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }
            }

            @keyframes slideOutStagger {
                0% {
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }
                100% {
                    opacity: 0;
                    transform: translateY(-15px) scale(0.9);
                }
            }
            
            .nav-links.nav-menu.mobile-open a {
                color: white !important;
                font-size: 1.15rem !important;
                font-weight: 600 !important;
                padding: 16px 24px !important;
                border-radius: 16px !important;
                background: rgba(255, 255, 255, 0.08) !important;
                backdrop-filter: blur(20px) !important;
                -webkit-backdrop-filter: blur(20px) !important;
                transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
                text-decoration: none !important;
                text-align: center !important;
                display: block !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                box-shadow: 
                    0 4px 20px rgba(0, 0, 0, 0.1),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
                position: relative !important;
                overflow: hidden !important;
            }

            /* Effet de brillance sur hover */
            .nav-links.nav-menu.mobile-open a::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
                transition: left 0.6s ease;
            }

            .nav-links.nav-menu.mobile-open a:hover::before {
                left: 100%;
            }

            .nav-links.nav-menu.mobile-open a:hover {
                background: rgba(255, 255, 255, 0.15) !important;
                backdrop-filter: blur(25px) saturate(150%) !important;
                transform: translateY(-2px) scale(1.02) !important;
                box-shadow: 
                    0 8px 30px rgba(102, 126, 234, 0.2),
                    0 4px 15px rgba(255, 255, 255, 0.1),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
                border-color: rgba(255, 255, 255, 0.2) !important;
                color: #E3F2FD !important;
            }

            .nav-links.nav-menu.mobile-open a:active {
                transform: translateY(0) scale(0.98) !important;
                transition: all 0.1s ease !important;
            }

            /* SOS Link style en mobile - GLASSMORPHISM AMÉLIORÉ */
            .nav-links.nav-menu.mobile-open .sos-link {
                background: linear-gradient(135deg, 
                    rgba(255, 68, 68, 0.25) 0%, 
                    rgba(255, 100, 100, 0.15) 100%) !important;
                border: 1px solid rgba(255, 68, 68, 0.4) !important;
                color: #FFE4E4 !important;
                box-shadow: 
                    0 6px 25px rgba(255, 68, 68, 0.15),
                    inset 0 1px 0 rgba(255, 255, 255, 0.15),
                    0 0 20px rgba(255, 68, 68, 0.1) !important;
                position: relative !important;
            }

            .nav-links.nav-menu.mobile-open .sos-link:hover {
                background: linear-gradient(135deg, 
                    rgba(255, 68, 68, 0.4) 0%, 
                    rgba(255, 100, 100, 0.25) 100%) !important;
                border-color: rgba(255, 68, 68, 0.6) !important;
                transform: translateY(-3px) scale(1.03) !important;
                box-shadow: 
                    0 12px 40px rgba(255, 68, 68, 0.25),
                    0 6px 20px rgba(255, 68, 68, 0.15),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2),
                    0 0 30px rgba(255, 68, 68, 0.2) !important;
                color: white !important;
            }
        }
`;

const JAVASCRIPT_MOBILE_MENU = `
        // =====================================================
        // NAVIGATION MOBILE HAMBURGER - GLASSMORPHISM
        // =====================================================
        
        function toggleMobileMenu() {
            const navMenu = document.querySelector('.nav-links.nav-menu');
            const toggle = document.querySelector('.mobile-nav-toggle i');
            
            console.log('🍔 Toggle menu - Current state:', navMenu.classList.contains('mobile-open'));
            
            if (navMenu.classList.contains('mobile-open')) {
                closeMobileMenu();
            } else {
                openMobileMenu();
            }
        }
        
        function openMobileMenu() {
            const navMenu = document.querySelector('.nav-links.nav-menu');
            const toggle = document.querySelector('.mobile-nav-toggle i');
            
            navMenu.classList.add('mobile-open');
            toggle.className = 'fas fa-times';
            
            // Animation staggered pour les liens
            const menuLinks = navMenu.querySelectorAll('a');
            menuLinks.forEach((link, index) => {
                link.style.opacity = '0';
                link.style.transform = 'translateY(20px)';
                link.style.animation = \`slideInStagger 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94) \${index * 0.05}s forwards\`;
            });
            
            // Fermer le menu lors du clic sur un lien
            menuLinks.forEach(link => {
                link.addEventListener('click', function(e) {
                    closeMobileMenu();
                    // Permettre la navigation normale
                    return true;
                });
            });
            
            // Fermer le menu si clic à l'extérieur
            setTimeout(() => {
                document.addEventListener('click', handleOutsideClick);
            }, 100);
        }
        
        function closeMobileMenu() {
            const navMenu = document.querySelector('.nav-links.nav-menu');
            const toggle = document.querySelector('.mobile-nav-toggle i');
            
            console.log('❌ Fermeture menu mobile');
            
            // Animation de sortie pour les liens
            const menuLinks = navMenu.querySelectorAll('a');
            menuLinks.forEach((link, index) => {
                link.style.animation = \`slideOutStagger 0.3s cubic-bezier(0.55, 0.085, 0.68, 0.53) \${index * 0.03}s forwards\`;
            });
            
            // Fermer le menu après l'animation
            setTimeout(() => {
                navMenu.classList.remove('mobile-open');
                toggle.className = 'fas fa-bars';
                
                // Reset des styles inline
                menuLinks.forEach(link => {
                    link.style.animation = '';
                    link.style.opacity = '';
                    link.style.transform = '';
                });
            }, 300);
            
            document.removeEventListener('click', handleOutsideClick);
        }
        
        function handleOutsideClick(event) {
            const navMenu = document.querySelector('.nav-links.nav-menu');
            const toggleBtn = document.querySelector('.mobile-nav-toggle');
            
            if (!navMenu.contains(event.target) && !toggleBtn.contains(event.target)) {
                closeMobileMenu();
            }
        }
`;

// Template pour les pages à corriger
const PAGES_TO_FIX = [
    'billetterie.html',
    'mobilier.html', 
    'excursions.html',
    'pmr.html'
];

console.log('Template créé pour corriger le menu hamburger sur toutes les pages');