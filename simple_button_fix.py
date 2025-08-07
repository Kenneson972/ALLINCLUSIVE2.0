#!/usr/bin/env python3
"""
Script simplifié pour analyser et corriger les boutons d'action
==============================================================
"""

import re
from pathlib import Path

def analyze_buttons_simple():
    """Analyser simplement les boutons d'action"""
    print("🔘 ANALYSE SIMPLIFIÉE DES BOUTONS")
    print("-" * 40)
    
    app_dir = Path("/app")
    html_files = list(app_dir.glob("*.html"))
    issues = []
    
    for html_file in html_files[:5]:  # Tester sur 5 fichiers
        print(f"Analyse: {html_file.name}")
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Recherche simple des boutons
            buttons = re.findall(r'<(?:button|a)[^>]*>.*?</(?:button|a)>', content, re.DOTALL)
            
            critical_keywords = ['réserver', 'booking', 'détails', 'details', 'contact', 'devis']
            buttons_found = 0
            buttons_without_action = 0
            
            for button in buttons:
                button_text = re.sub(r'<[^>]+>', '', button).lower().strip()
                
                # Vérifier si c'est un bouton critique
                is_critical = any(keyword in button_text for keyword in critical_keywords)
                
                if is_critical:
                    buttons_found += 1
                    # Vérifier si le bouton a une action
                    has_action = any(attr in button for attr in ['onclick=', 'href=', 'javascript:', 'data-action='])
                    
                    if not has_action:
                        buttons_without_action += 1
            
            if buttons_without_action > 0:
                issues.append({
                    'file': html_file.name,
                    'critical_buttons': buttons_found,
                    'buttons_without_action': buttons_without_action
                })
                print(f"  ⚠️  {buttons_without_action}/{buttons_found} boutons critiques sans action")
            else:
                print(f"  ✅ {buttons_found} boutons critiques ont des actions")
                
        except Exception as e:
            print(f"  ❌ Erreur: {e}")
    
    return issues

def create_universal_button_fix():
    """Créer un script universel pour corriger les boutons"""
    
    js_content = '''
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
                        .replace(/[^a-z0-9\\s-]/g, '')
                        .replace(/\\s+/g, '-')
                        .replace(/^villa-?/, '');
                }
                
                // Chercher attributs data
                villaId = container.dataset.villa || container.dataset.villaId || villaId;
            }
            
            // Extraire depuis URL si page villa
            if (villaId === 'unknown' && location.pathname.includes('villa-')) {
                const match = location.pathname.match(/villa-(.+?)\\.html/);
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
'''
    
    # Sauvegarder le script
    output_file = Path("/app/assets/js/universal-button-fixer.js")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"✅ Script universel créé: {output_file}")
    return output_file

def main():
    print("🔧 CORRECTEUR SIMPLIFIÉ DE BOUTONS")
    print("=" * 50)
    
    # Analyser les boutons
    issues = analyze_buttons_simple()
    
    # Créer le script correcteur universel
    script_file = create_universal_button_fix()
    
    print(f"\n📊 RÉSUMÉ:")
    if issues:
        print(f"   - {len(issues)} fichiers avec boutons à corriger")
        for issue in issues:
            print(f"     • {issue['file']}: {issue['buttons_without_action']} boutons sans action")
    else:
        print("   - Tous les boutons analysés ont des actions")
    
    print(f"\n✅ SOLUTION:")
    print(f"   Script universel créé: {script_file}")
    print(f"\n🚀 INTÉGRATION:")
    print(f"   Ajoutez avant </body> dans vos pages HTML:")
    print(f'   <script src="./assets/js/universal-button-fixer.js"></script>')
    
    return True

if __name__ == "__main__":
    main()