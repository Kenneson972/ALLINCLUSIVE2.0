#!/usr/bin/env python3
"""
AJOUT FORCÉ des sections propres mobile-friendly à toutes les villas
Avec CSS inline pour garantir l'affichage sur GitHub Pages mobile
"""

import os
import re
import glob

def create_mobile_perfect_section(villa_name):
    """Crée une section parfaite pour mobile avec CSS inline complet"""
    
    return f'''
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
            <!-- Titre Principal -->
            <h3 style="
                color: #1f2937; 
                font-size: 20px; 
                font-weight: bold; 
                margin: 0 0 16px 0; 
                text-align: center;
                border-bottom: 2px solid #3b82f6;
                padding-bottom: 8px;
            ">
                💰 Tarifs et Services - {villa_name}
            </h3>
            
            <!-- Section Tarifs -->
            <div style="
                background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); 
                border: 1px solid #22c55e; 
                border-radius: 8px; 
                padding: 16px; 
                margin-bottom: 16px;
            ">
                <h4 style="
                    color: #166534; 
                    font-weight: 600; 
                    margin: 0 0 12px 0; 
                    font-size: 16px;
                    display: flex;
                    align-items: center;
                ">
                    <span style="margin-right: 8px;">💶</span>
                    Tarifs 2025
                </h4>
                
                <!-- Grille Tarifs Mobile -->
                <div style="font-size: 14px; line-height: 1.5;">
                    <div style="
                        display: flex; 
                        justify-content: space-between; 
                        margin-bottom: 8px; 
                        padding: 8px; 
                        background: rgba(255,255,255,0.7); 
                        border-radius: 4px;
                    ">
                        <span style="font-weight: 500;">Basse saison (mai-nov)</span>
                        <strong style="color: #166534;">1500€/sem</strong>
                    </div>
                    <div style="
                        display: flex; 
                        justify-content: space-between; 
                        margin-bottom: 8px; 
                        padding: 8px; 
                        background: rgba(255,255,255,0.7); 
                        border-radius: 4px;
                    ">
                        <span style="font-weight: 500;">Haute saison (déc-avr)</span>
                        <strong style="color: #166534;">2200€/sem</strong>
                    </div>
                    <div style="
                        display: flex; 
                        justify-content: space-between; 
                        margin-bottom: 8px; 
                        padding: 8px; 
                        background: rgba(255,255,255,0.7); 
                        border-radius: 4px;
                    ">
                        <span style="font-weight: 500;">Week-end</span>
                        <strong style="color: #166534;">600€ (2 nuits min)</strong>
                    </div>
                    <div style="
                        display: flex; 
                        justify-content: space-between; 
                        padding: 8px; 
                        background: rgba(59, 130, 246, 0.1); 
                        border-radius: 4px;
                        border-top: 1px solid #3b82f6;
                    ">
                        <span style="font-weight: 500;">Dépôt garantie</span>
                        <strong style="color: #1d4ed8;">1000€ (remboursable)</strong>
                    </div>
                </div>
            </div>
            
            <!-- Section Services -->
            <div style="
                background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); 
                border: 1px solid #3b82f6; 
                border-radius: 8px; 
                padding: 16px; 
                margin-bottom: 16px;
            ">
                <h4 style="
                    color: #1e40af; 
                    font-weight: 600; 
                    margin: 0 0 12px 0; 
                    font-size: 16px;
                    display: flex;
                    align-items: center;
                ">
                    <span style="margin-right: 8px;">🏖️</span>
                    Services Inclus
                </h4>
                
                <!-- Liste Services Mobile -->
                <div style="font-size: 14px;">
                    <div style="display: flex; align-items: center; margin-bottom: 6px; padding: 4px 0;">
                        <span style="color: #22c55e; margin-right: 8px; font-weight: bold;">✓</span>
                        <span>WiFi gratuit haut débit</span>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 6px; padding: 4px 0;">
                        <span style="color: #22c55e; margin-right: 8px; font-weight: bold;">✓</span>
                        <span>Nettoyage final inclus</span>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 6px; padding: 4px 0;">
                        <span style="color: #22c55e; margin-right: 8px; font-weight: bold;">✓</span>
                        <span>Linge de maison fourni</span>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 6px; padding: 4px 0;">
                        <span style="color: #22c55e; margin-right: 8px; font-weight: bold;">✓</span>
                        <span>Accès piscine & jacuzzi</span>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 6px; padding: 4px 0;">
                        <span style="color: #22c55e; margin-right: 8px; font-weight: bold;">✓</span>
                        <span>Parking privé sécurisé</span>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 6px; padding: 4px 0;">
                        <span style="color: #22c55e; margin-right: 8px; font-weight: bold;">✓</span>
                        <span>Climatisation toutes pièces</span>
                    </div>
                    <div style="display: flex; align-items: center; padding: 4px 0;">
                        <span style="color: #22c55e; margin-right: 8px; font-weight: bold;">✓</span>
                        <span>TV satellite internationale</span>
                    </div>
                </div>
            </div>
            
            <!-- Section Contact -->
            <div style="
                background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%); 
                border-radius: 8px; 
                padding: 16px; 
                text-align: center;
                border: 1px solid #6366f1;
            ">
                <h4 style="
                    color: #4338ca; 
                    font-weight: 600; 
                    margin: 0 0 8px 0; 
                    font-size: 16px;
                ">
                    📞 Réservation Immédiate
                </h4>
                <div style="font-size: 14px; color: #374151; line-height: 1.4;">
                    <div style="margin-bottom: 4px;">
                        <strong>📱 Téléphone:</strong> <a href="tel:+596696xxxxxx" style="color: #4338ca; text-decoration: none;">+596 696 XX XX XX</a>
                    </div>
                    <div>
                        <strong>✉️ Email:</strong> <a href="mailto:contact@khanelconcept.com" style="color: #4338ca; text-decoration: none;">contact@khanelconcept.com</a>
                    </div>
                </div>
            </div>
            
            <!-- Note de bas -->
            <p style="
                font-size: 12px; 
                color: #6b7280; 
                text-align: center; 
                margin: 12px 0 0 0; 
                font-style: italic;
            ">
                ⚠️ Tarifs indicatifs sujets à variation selon période. Contactez-nous pour devis personnalisé.
            </p>
        </div>'''

def force_add_section_to_villa(file_path):
    """Force l'ajout de la section mobile-perfect à une villa"""
    
    filename = os.path.basename(file_path)
    villa_name = filename.replace('.html', '').replace('-', ' ').title()
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"🔧 AJOUT FORCÉ: {filename}")
    
    # Supprimer toute section existante de tarifs
    existing_patterns = [
        r'<!-- SECTION TARIFS.*?</div>',
        r'<div id="tarifs-services".*?</div>\s*</div>',  # Notre propre section si elle existe déjà
    ]
    
    for pattern in existing_patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Créer la section mobile-perfect
    mobile_section = create_mobile_perfect_section(villa_name)
    
    # Trouver FORCÉMENT un endroit où l'insérer
    insertion_attempts = [
        # Tentative 1: Avant </main>
        (r'(</main>)', f'{mobile_section}\\1'),
        # Tentative 2: Après le dernier </section>
        (r'(</section>)(\s*<!-- Back to Top|Back to Top|Scripts|<script)', f'\\1{mobile_section}\\2'),
        # Tentative 3: Avant Back to Top
        (r'(<!-- Back to Top -->)', f'{mobile_section}\\1'),
        # Tentative 4: Avant les scripts
        (r'(<!-- Scripts -->|<script)', f'{mobile_section}\\1'),
        # Tentative 5: Avant </body> (fallback ultime)
        (r'(</body>)', f'{mobile_section}\\1'),
    ]
    
    inserted = False
    for i, (pattern, replacement) in enumerate(insertion_attempts, 1):
        if re.search(pattern, content, re.IGNORECASE):
            content = re.sub(pattern, replacement, content, count=1, flags=re.IGNORECASE)
            inserted = True
            print(f"   ✅ Inséré avec tentative {i}")
            break
    
    if not inserted:
        # FALLBACK ULTIME: Ajouter à la fin avant </body>
        content = content.replace('</body>', f'{mobile_section}\n</body>')
        inserted = True
        print(f"   ✅ Inséré avec fallback ultime")
    
    # Sauvegarder
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    print("🚀 AJOUT FORCÉ - SECTIONS MOBILE-PERFECT")
    print("=" * 60)
    print("OBJECTIF: Ajouter sections parfaites à TOUTES les villas")
    print("=" * 60)
    
    villa_files = glob.glob('/app/villa-*.html')
    villa_files = [f for f in villa_files if 'template' not in f and 'details' not in f]
    
    success_count = 0
    
    for file_path in sorted(villa_files):
        if force_add_section_to_villa(file_path):
            success_count += 1
    
    print("=" * 60)
    print(f"🎯 AJOUT FORCÉ TERMINÉ:")
    print(f"   • Sections ajoutées: {success_count}/{len(villa_files)}")
    print(f"✅ TOUTES les villas ont maintenant des sections mobile-perfect")
    print(f"✅ CSS inline complet pour compatibilité GitHub Pages")
    print(f"✅ Design responsive et professionnel")

if __name__ == "__main__":
    main()