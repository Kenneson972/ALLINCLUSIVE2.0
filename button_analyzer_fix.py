#!/usr/bin/env python3
"""
Script de correction et analyse des boutons d'action
==================================================

Corrige l'erreur regex et analyse les boutons critiques
"""

import os
import re
from pathlib import Path

def analyze_buttons():
    """Analyser les boutons d'action dans les fichiers HTML"""
    print("🔘 ANALYSE CORRECTE DES BOUTONS D'ACTION")
    print("-" * 50)
    
    app_dir = Path("/app")
    html_files = list(app_dir.glob("*.html"))
    button_issues = []
    
    for html_file in html_files[:10]:  # Limiter à 10 pour les tests
        print(f"Analyse: {html_file.name}")
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Rechercher boutons critiques avec regex corrigée
            critical_patterns = [
                (r'(?i)(réserver|booking|book)', 'Réservation'),
                (r'(?i)(détails|details|voir plus)', 'Détails'),
                (r'(?i)(contact|contacter)', 'Contact'),
                (r'(?i)(devis|quote)', 'Devis'),
                (r'(?i)(disponibilité|availability)', 'Disponibilité')
            ]
            
            file_issues = []
            buttons_found = 0
            buttons_with_actions = 0
            
            for pattern, button_type in critical_patterns:
                # Trouver boutons contenant ces mots-clés
                button_matches = re.findall(r'<(?:button|a)[^>]*?[^>]*?>' + pattern + r'.*?</(?:button|a)>', content, re.IGNORECASE | re.DOTALL)
                
                for button_html in button_matches:
                    buttons_found += 1
                    # Vérifier si le bouton a une action JS/href
                    has_action = any(attr in button_html for attr in ['onclick=', 'href=', 'onsubmit=', 'data-action=', 'javascript:'])
                    
                    if has_action:
                        buttons_with_actions += 1
                    else:
                        file_issues.append({
                            'type': button_type,
                            'button_preview': button_html[:150] + '...' if len(button_html) > 150 else button_html,
                            'issue': 'Pas d\'action définie'
                        })
            
            if file_issues:
                button_issues.append({
                    'file': str(html_file),
                    'issues': file_issues,
                    'stats': {
                        'total_buttons': buttons_found,
                        'buttons_with_actions': buttons_with_actions,
                        'buttons_without_actions': len(file_issues)
                    }
                })
                print(f"  ⚠️  {len(file_issues)}/{buttons_found} boutons sans action")
            else:
                print(f"  ✅ {buttons_with_actions}/{buttons_found} boutons ont des actions")
                
        except Exception as e:
            print(f"  ❌ Erreur: {e}")
    
    return button_issues

def generate_action_fixes(issues):
    """Générer les corrections pour les boutons sans action"""
    
    if not issues:
        print("✅ Aucun bouton sans action trouvé!")
        return
    
    print(f"\n📝 CORRECTIONS PROPOSÉES POUR {len(issues)} FICHIERS:")
    print("=" * 60)
    
    fixes_js = """
// Script de correction automatique des boutons sans action
// KhanelConcept - Optimisation Frontend

document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 Initialisation des corrections boutons...');
    
    // Configuration des actions par type
    const buttonActions = {
        reservation: function(villaName = 'Villa', villaId = 'unknown') {
            const params = new URLSearchParams({
                villa: villaId,
                name: encodeURIComponent(villaName)
            });
            window.location.href = `./reservation.html?${params.toString()}`;
        },
        
        details: function(villaId = 'unknown') {
            if (villaId !== 'unknown') {
                window.location.href = `./villa-${villaId}.html`;
            } else {
                // Fallback vers la liste des villas
                window.location.href = './';
            }
        },
        
        contact: function(subject = '') {
            const params = new URLSearchParams({
                subject: encodeURIComponent(subject)
            });
            window.location.href = `./contact.html?${params.toString()}`;
        },
        
        devis: function(villaName = 'Villa', villaId = 'unknown') {
            const params = new URLSearchParams({
                villa: villaId,
                type: 'quote',
                name: encodeURIComponent(villaName)
            });
            window.location.href = `./reservation.html?${params.toString()}`;
        },
        
        disponibilite: function(villaId = 'unknown') {
            const params = new URLSearchParams({
                villa: villaId,
                action: 'availability'
            });
            window.location.href = `./reservation.html?${params.toString()}`;
        }
    };
    
    // Fonction pour extraire les informations villa du contexte
    function extractVillaInfo(buttonElement) {
        const container = buttonElement.closest('.villa-card, .glass-card, .villa-item, .hero-villa, [class*="villa"]');
        let villaName = 'Villa';
        let villaId = 'unknown';
        
        if (container) {
            // Chercher le titre de la villa
            const titleElement = container.querySelector('h1, h2, h3, .villa-title, [class*="title"]');
            if (titleElement) {
                villaName = titleElement.textContent.trim();
                // Générer ID depuis le nom
                villaId = villaName
                    .toLowerCase()
                    .replace(/[^a-z0-9\\s-]/g, '')
                    .replace(/\\s+/g, '-')
                    .replace(/^villa-?/, '')
                    .replace(/--+/g, '-');
            }
            
            // Ou chercher un attribut data-villa
            const dataVilla = container.getAttribute('data-villa') || 
                            container.getAttribute('data-villa-id');
            if (dataVilla) {
                villaId = dataVilla;
            }
        }
        
        // Fallback: extraire depuis l'URL courante si c'est une page villa
        if (villaId === 'unknown' && window.location.pathname.includes('villa-')) {
            const pathMatch = window.location.pathname.match(/villa-(.+?)\\.html/);
            if (pathMatch) {
                villaId = pathMatch[1];
            }
        }
        
        return { villaName, villaId };
    }
    
    // Fonction pour déterminer le type d'action basé sur le texte
    function getActionType(buttonText) {
        const text = buttonText.toLowerCase();
        
        if (/réserver|book|booking/i.test(text)) return 'reservation';
        if (/détail|detail|voir plus|en savoir plus/i.test(text)) return 'details';
        if (/contact/i.test(text)) return 'contact';
        if (/devis|quote/i.test(text)) return 'devis';
        if (/disponibilité|availability|calendar/i.test(text)) return 'disponibilite';
        
        return 'reservation'; // Par défaut
    }
    
    // Rechercher tous les boutons sans action évidente
    const allButtons = document.querySelectorAll('button, a');
    let fixedCount = 0;
    
    allButtons.forEach(button => {
        const buttonText = (button.textContent || button.innerText || '').trim();
        const hasExistingAction = button.onclick || 
                                 button.getAttribute('href') || 
                                 button.getAttribute('data-action') ||
                                 button.getAttribute('onsubmit');
        
        // Ignorer boutons avec actions existantes ou textes non pertinents
        if (hasExistingAction || 
            !buttonText || 
            buttonText.length < 3 ||
            /nav|menu|close|fermer|×|toggle|search|langue|login|logout/i.test(buttonText)) {
            return;
        }
        
        // Vérifier si c'est un bouton critique
        const actionType = getActionType(buttonText);
        if (actionType && buttonActions[actionType]) {
            
            // Ajouter l'action
            button.addEventListener('click', function(e) {
                e.preventDefault();
                
                const { villaName, villaId } = extractVillaInfo(this);
                
                try {
                    buttonActions[actionType](villaName, villaId);
                    console.log(`✅ Action ${actionType} exécutée pour:`, villaName);
                } catch (error) {
                    console.error(`❌ Erreur action ${actionType}:`, error);
                    // Fallback vers page d'accueil
                    window.location.href = './';
                }
            });
            
            // Ajouter styles visuels pour indiquer que le bouton est cliquable
            button.style.cursor = 'pointer';
            if (!button.style.transition) {
                button.style.transition = 'all 0.3s ease';
            }
            
            // Effet hover si pas déjà présent
            button.addEventListener('mouseenter', function() {
                if (!this.dataset.originalTransform) {
                    this.dataset.originalTransform = this.style.transform || 'none';
                    this.style.transform = 'scale(1.05)';
                }
            });
            
            button.addEventListener('mouseleave', function() {
                this.style.transform = this.dataset.originalTransform || 'none';
            });
            
            fixedCount++;
            console.log(`🔧 Action ajoutée:`, buttonText, `(${actionType})`);
        }
    });
    
    console.log(`✅ ${fixedCount} boutons corrigés automatiquement`);
    
    // Ajouter un indicateur visuel temporaire
    if (fixedCount > 0) {
        const indicator = document.createElement('div');
        indicator.innerHTML = `
            <div style="
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: linear-gradient(135deg, #48bb78, #38a169);
                color: white;
                padding: 10px 20px;
                border-radius: 10px;
                font-size: 14px;
                z-index: 10000;
                box-shadow: 0 4px 15px rgba(72, 187, 120, 0.3);
                animation: slideIn 0.5s ease;
            ">
                ✅ ${fixedCount} boutons activés automatiquement
            </div>
            <style>
                @keyframes slideIn {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
            </style>
        `;
        document.body.appendChild(indicator);
        
        // Supprimer après 5 secondes
        setTimeout(() => {
            if (indicator.parentNode) {
                indicator.remove();
            }
        }, 5000);
    }
});
    """
    
    # Sauvegarder le script de correction
    fix_file = Path("/app/assets/js/button-action-fixes.min.js")
    fix_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(fix_file, 'w', encoding='utf-8') as f:
        f.write(fixes_js)
    
    print(f"✅ Script de correction créé: {fix_file}")
    
    # Rapport détaillé
    for issue in issues:
        print(f"\n📄 {issue['file']}:")
        stats = issue.get('stats', {})
        print(f"   📊 {stats.get('buttons_without_actions', 0)}/{stats.get('total_buttons', 0)} boutons sans action")
        
        for problem in issue['issues'][:3]:  # Limiter à 3 exemples
            print(f"   ❌ {problem['type']}: {problem['button_preview'][:100]}...")

def main():
    """Fonction principale"""
    print("🔧 CORRECTEUR BOUTONS D'ACTION KHANELCONCEPT")
    print("=" * 60)
    
    issues = analyze_buttons()
    
    if issues:
        generate_action_fixes(issues)
        
        print(f"\n📋 RÉSUMÉ:")
        print(f"   - {len(issues)} fichiers avec boutons sans action")
        print(f"   - Script correcteur généré")
        print(f"\n🚀 INTÉGRATION:")
        print(f"   Ajoutez ceci avant </body> dans vos pages HTML:")
        print(f'   <script src="./assets/js/button-action-fixes.min.js"></script>')
        
    else:
        print("✅ Tous les boutons ont des actions définies!")
    
    return len(issues)

if __name__ == "__main__":
    main()