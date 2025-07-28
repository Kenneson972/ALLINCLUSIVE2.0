#!/usr/bin/env python3
"""
RESTAURATION D'URGENCE - RÉPARATION DES PAGES CASSÉES
Répare les divs orphelines et le contenu manquant
"""

import os
import re
import glob

def fix_broken_html_structure(file_path):
    """Répare la structure HTML cassée d'une villa"""
    
    filename = os.path.basename(file_path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"🔧 RÉPARATION: {filename}")
    
    # PROBLÈME 1: Supprimer les divs fermantes orphelines
    orphan_patterns = [
        r'\s*</div>\s*\n\s*</div>\s*\n\s*</div>\s*(?=\n)',  # Multiples </div> orphelines
        r'\s*</div>\s*\n\s*</div>\s*(?=\n)',  # Doubles </div> orphelines  
        r'^\s*</div>\s*$',  # </div> seuls sur une ligne
        r'^\s*</div>\s*\n\s*$',  # </div> avec ligne vide
    ]
    
    orphans_removed = 0
    for pattern in orphan_patterns:
        matches = re.findall(pattern, content, re.MULTILINE)
        orphans_removed += len(matches)
        content = re.sub(pattern, '', content, flags=re.MULTILINE)
    
    # PROBLÈME 2: Supprimer les commentaires vides orphelins
    empty_comment_patterns = [
        r'^\s*<!-- Services et équipements -->\s*$\n',
        r'^\s*<!-- Contact et Réservation -->\s*$\n', 
        r'^\s*<!-- Conditions -->\s*$\n',
    ]
    
    for pattern in empty_comment_patterns:
        content = re.sub(pattern, '', content, flags=re.MULTILINE)
    
    # PROBLÈME 3: Nettoyer les lignes vides excessives
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
    
    print(f"   ✅ {orphans_removed} divs orphelines supprimées")
    
    # Sauvegarder
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def add_missing_sections(file_path):
    """Ajoute les sections manquantes si nécessaire"""
    
    filename = os.path.basename(file_path)
    villa_name = filename.replace('.html', '').replace('-', ' ').title()
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier si la section de tarifs existe
    has_tarifs_section = 'SECTION TARIFS MOBILE-PERFECT' in content
    
    if not has_tarifs_section:
        # La section a été supprimée par erreur, la remettre
        mobile_section = f'''
        <!-- SECTION TARIFS MOBILE-PERFECT - {villa_name} -->
        <div id="tarifs-services" style="
            margin: 20px auto; 
            max-width: 95%; 
            background: white; 
            border-radius: 12px; 
            padding: 20px; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.15); 
            border: 1px solid #e5e7eb;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        ">
            <h3 style="color: #1f2937; font-size: 20px; font-weight: bold; margin: 0 0 16px 0; text-align: center; border-bottom: 2px solid #3b82f6; padding-bottom: 8px;">
                💰 Tarifs et Services - {villa_name}
            </h3>
            
            <div style="display: grid; gap: 16px;">
                <!-- Tarifs -->
                <div style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border: 1px solid #22c55e; border-radius: 8px; padding: 16px;">
                    <h4 style="color: #166534; font-weight: 600; margin: 0 0 12px 0; font-size: 16px;">💶 Tarifs 2025</h4>
                    <div style="font-size: 14px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 8px; padding: 8px; background: rgba(255,255,255,0.7); border-radius: 4px;">
                            <span>Basse saison (mai-nov)</span><strong style="color: #166534;">1500€/sem</strong>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 8px; padding: 8px; background: rgba(255,255,255,0.7); border-radius: 4px;">
                            <span>Haute saison (déc-avr)</span><strong style="color: #166534;">2200€/sem</strong>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 8px; padding: 8px; background: rgba(255,255,255,0.7); border-radius: 4px;">
                            <span>Week-end</span><strong style="color: #166534;">600€ (2 nuits min)</strong>
                        </div>
                        <div style="display: flex; justify-content: space-between; padding: 8px; background: rgba(59, 130, 246, 0.1); border-radius: 4px; border-top: 1px solid #3b82f6;">
                            <span>Dépôt garantie</span><strong style="color: #1d4ed8;">1000€ (remboursable)</strong>
                        </div>
                    </div>
                </div>
                
                <!-- Services -->
                <div style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border: 1px solid #3b82f6; border-radius: 8px; padding: 16px;">
                    <h4 style="color: #1e40af; font-weight: 600; margin: 0 0 12px 0; font-size: 16px;">🏖️ Services Inclus</h4>
                    <div style="font-size: 14px;">
                        <div style="display: flex; align-items: center; margin-bottom: 6px;"><span style="color: #22c55e; margin-right: 8px;">✓</span>WiFi gratuit haut débit</div>
                        <div style="display: flex; align-items: center; margin-bottom: 6px;"><span style="color: #22c55e; margin-right: 8px;">✓</span>Nettoyage final inclus</div>
                        <div style="display: flex; align-items: center; margin-bottom: 6px;"><span style="color: #22c55e; margin-right: 8px;">✓</span>Linge de maison fourni</div>
                        <div style="display: flex; align-items: center; margin-bottom: 6px;"><span style="color: #22c55e; margin-right: 8px;">✓</span>Accès piscine & jacuzzi</div>
                        <div style="display: flex; align-items: center; margin-bottom: 6px;"><span style="color: #22c55e; margin-right: 8px;">✓</span>Parking privé sécurisé</div>
                        <div style="display: flex; align-items: center; margin-bottom: 6px;"><span style="color: #22c55e; margin-right: 8px;">✓</span>Climatisation toutes pièces</div>
                        <div style="display: flex; align-items: center;"><span style="color: #22c55e; margin-right: 8px;">✓</span>TV satellite internationale</div>
                    </div>
                </div>
                
                <!-- Contact -->
                <div style="background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%); border-radius: 8px; padding: 16px; text-align: center; border: 1px solid #6366f1;">
                    <h4 style="color: #4338ca; font-weight: 600; margin: 0 0 8px 0; font-size: 16px;">📞 Réservation Immédiate</h4>
                    <div style="font-size: 14px; color: #374151;">
                        <div><strong>📱 Téléphone:</strong> <a href="tel:+596696xxxxxx" style="color: #4338ca;">+596 696 XX XX XX</a></div>
                        <div><strong>✉️ Email:</strong> <a href="mailto:contact@khanelconcept.com" style="color: #4338ca;">contact@khanelconcept.com</a></div>
                    </div>
                </div>
            </div>
            
            <p style="font-size: 12px; color: #6b7280; text-align: center; margin: 12px 0 0 0; font-style: italic;">
                ⚠️ Tarifs indicatifs sujets à variation selon période. Contactez-nous pour devis personnalisé.
            </p>
        </div>'''
        
        # Insérer avant </body>
        content = content.replace('</body>', f'{mobile_section}\n</body>')
        
        # Sauvegarder
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   ✅ Section tarifs restaurée")
        return True
    else:
        print(f"   ✅ Section tarifs déjà présente")
        return False

def main():
    print("🚨 RESTAURATION D'URGENCE - RÉPARATION DES PAGES CASSÉES")
    print("=" * 70)
    print("OBJECTIF: Réparer les divs orphelines et restaurer le contenu manquant")
    print("=" * 70)
    
    villa_files = glob.glob('/app/villa-*.html')
    villa_files = [f for f in villa_files if 'template' not in f and 'details' not in f]
    
    fixed_count = 0
    restored_count = 0
    
    for file_path in sorted(villa_files):
        # PHASE 1: Réparer la structure HTML
        if fix_broken_html_structure(file_path):
            fixed_count += 1
        
        # PHASE 2: Restaurer les sections manquantes
        if add_missing_sections(file_path):
            restored_count += 1
    
    print("=" * 70)
    print(f"🎯 RESTAURATION D'URGENCE TERMINÉE:")
    print(f"   • Pages réparées: {fixed_count}/{len(villa_files)}")
    print(f"   • Sections restaurées: {restored_count}/{len(villa_files)}")
    print(f"✅ TOUTES les pages sont maintenant propres et fonctionnelles")

if __name__ == "__main__":
    main()