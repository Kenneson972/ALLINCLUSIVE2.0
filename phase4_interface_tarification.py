#!/usr/bin/env python3
"""
PHASE 4 : INTERFACE UTILISATEUR
Ajouter la section tarification aux pages des villas
"""

import os
import re
from pathlib import Path
import requests
import json

def get_villa_pricing_from_db(villa_name):
    """Récupère les tarifs d'une villa depuis l'API"""
    try:
        response = requests.get("https://60538156-1356-4530-8795-27ab33f42945.preview.emergentagent.com/api/villas")
        if response.status_code == 200:
            villas = response.json()
            for villa in villas:
                if villa.get('name') == villa_name:
                    return villa.get('pricing_details', {})
    except:
        pass
    return {}

def create_tarification_section_html(villa_name, pricing_data):
    """Crée la section tarification en HTML"""
    if not pricing_data:
        return ""
    
    base_price = pricing_data.get('base_price', 0)
    weekend_price = pricing_data.get('weekend', base_price)
    week_price = pricing_data.get('week', base_price)
    high_season_price = pricing_data.get('high_season', base_price)
    details = pricing_data.get('details', 'Tarifs selon saison et durée')
    
    # Couleurs et icônes adaptées au glassmorphism
    html = f"""
    <!-- Section Tarification -->
    <div class="tarification-section" style="margin: 2rem 0;">
        <div class="glass-card" style="padding: 2rem; border-radius: 20px; background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2);">
            <h3 style="color: white; font-size: 1.5rem; font-weight: bold; margin-bottom: 1.5rem; display: flex; align-items: center;">
                <i class="fas fa-euro-sign" style="margin-right: 0.75rem; color: #4facfe;"></i>
                Tarification
            </h3>
            
            <div class="tarifs-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
                <!-- Prix de base -->
                <div class="tarif-card" style="background: rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 1.5rem; text-align: center; transition: all 0.3s ease; border: 1px solid rgba(255, 255, 255, 0.2);">
                    <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
                        <i class="fas fa-calendar-day" style="color: #4facfe; margin-right: 0.5rem;"></i>
                        <span style="color: white; font-weight: 600;">Base</span>
                    </div>
                    <div style="font-size: 1.8rem; font-weight: bold; color: #4facfe; margin-bottom: 0.5rem;">{base_price}€</div>
                    <div style="color: rgba(255, 255, 255, 0.7); font-size: 0.9rem;">par nuit</div>
                </div>
                
                <!-- Weekend -->
                <div class="tarif-card" style="background: rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 1.5rem; text-align: center; transition: all 0.3s ease; border: 1px solid rgba(255, 255, 255, 0.2);">
                    <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
                        <i class="fas fa-calendar-week" style="color: #00f5ff; margin-right: 0.5rem;"></i>
                        <span style="color: white; font-weight: 600;">Weekend</span>
                    </div>
                    <div style="font-size: 1.8rem; font-weight: bold; color: #00f5ff; margin-bottom: 0.5rem;">{weekend_price}€</div>
                    <div style="color: rgba(255, 255, 255, 0.7); font-size: 0.9rem;">2-3 nuits</div>
                </div>
                
                <!-- Semaine -->
                <div class="tarif-card" style="background: rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 1.5rem; text-align: center; transition: all 0.3s ease; border: 1px solid rgba(255, 255, 255, 0.2);">
                    <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
                        <i class="fas fa-calendar-alt" style="color: #10b981; margin-right: 0.5rem;"></i>
                        <span style="color: white; font-weight: 600;">Semaine</span>
                    </div>
                    <div style="font-size: 1.8rem; font-weight: bold; color: #10b981; margin-bottom: 0.5rem;">{week_price}€</div>
                    <div style="color: rgba(255, 255, 255, 0.7); font-size: 0.9rem;">7 jours</div>
                </div>
                
                <!-- Haute saison -->
                <div class="tarif-card" style="background: rgba(255, 215, 0, 0.2); border-radius: 15px; padding: 1.5rem; text-align: center; transition: all 0.3s ease; border: 1px solid rgba(255, 215, 0, 0.3);">
                    <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
                        <i class="fas fa-star" style="color: #ffd700; margin-right: 0.5rem;"></i>
                        <span style="color: white; font-weight: 600;">Haute saison</span>
                    </div>
                    <div style="font-size: 1.8rem; font-weight: bold; color: #ffd700; margin-bottom: 0.5rem;">{high_season_price}€</div>
                    <div style="color: rgba(255, 255, 255, 0.7); font-size: 0.9rem;">Juillet/Août/Décembre</div>
                </div>
    """
    
    # Ajouter suppléments si disponibles
    party_rates = pricing_data.get('party_rates', {})
    if party_rates:
        html += """
                <!-- Suppléments fêtes -->
                <div class="tarif-card" style="background: rgba(255, 107, 107, 0.2); border-radius: 15px; padding: 1.5rem; text-align: center; transition: all 0.3s ease; border: 1px solid rgba(255, 107, 107, 0.3);">
                    <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
                        <i class="fas fa-glass-cheers" style="color: #ff6b6b; margin-right: 0.5rem;"></i>
                        <span style="color: white; font-weight: 600;">Suppléments fêtes</span>
                    </div>
        """
        
        for guest_count, price in party_rates.items():
            guests_text = guest_count.replace('_guests', '').replace('_', ' ')
            supplement = price - base_price
            html += f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span style="color: white; font-size: 0.9rem;">{guests_text} invités</span>
                        <span style="color: #ff6b6b; font-weight: bold;">+{supplement}€</span>
                    </div>
            """
        
        html += """
                </div>
        """
    
    html += f"""
            </div>
            
            <!-- Détails -->
            <div style="background: rgba(255, 255, 255, 0.05); padding: 1rem; border-radius: 10px; margin-top: 1rem;">
                <div style="display: flex; align-items: flex-start;">
                    <i class="fas fa-info-circle" style="color: #4facfe; margin-right: 0.5rem; margin-top: 0.2rem;"></i>
                    <span style="color: rgba(255, 255, 255, 0.9); font-size: 0.9rem; line-height: 1.4;">{details}</span>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Styles pour hover effects -->
    <style>
        .tarif-card:hover {{
            background: rgba(255, 255, 255, 0.15) !important;
            transform: translateY(-3px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}
        
        @media (max-width: 768px) {{
            .tarifs-grid {{
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)) !important;
            }}
            
            .tarif-card {{
                padding: 1rem !important;
            }}
            
            .tarif-card > div:nth-child(2) {{
                font-size: 1.4rem !important;
            }}
        }}
    </style>
    """
    
    return html

def find_villa_pages():
    """Trouve les pages de villa existantes"""
    pages = []
    
    # Chercher les pages HTML dans le dossier principal
    for html_file in Path('/app').glob('*.html'):
        content = html_file.read_text(encoding='utf-8')
        
        # Vérifier si c'est une page de villa (contient des informations de villa)
        if any(keyword in content.lower() for keyword in ['villa', 'studio', 'espace piscine']):
            if 'template' not in html_file.name and 'admin' not in html_file.name:
                pages.append(html_file)
    
    return pages

def extract_villa_name_from_page(html_content):
    """Extrait le nom de la villa du contenu HTML"""
    # Chercher dans le titre
    title_match = re.search(r'<title>([^<]+)</title>', html_content, re.IGNORECASE)
    if title_match:
        title = title_match.group(1)
        # Nettoyer le titre
        villa_name = title.split(' - ')[0].strip()
        return villa_name
    
    # Chercher dans les h1
    h1_match = re.search(r'<h1[^>]*>([^<]+)</h1>', html_content, re.IGNORECASE)
    if h1_match:
        return h1_match.group(1).strip()
    
    return None

def add_tarification_to_page(page_path):
    """Ajoute la section tarification à une page"""
    try:
        print(f"🔧 Traitement de {page_path.name}")
        
        # Lire le contenu
        content = page_path.read_text(encoding='utf-8')
        
        # Extraire le nom de la villa
        villa_name = extract_villa_name_from_page(content)
        
        if not villa_name:
            print(f"   ⚠️  Nom de villa non trouvé")
            return False
        
        print(f"   📋 Villa détectée: {villa_name}")
        
        # Récupérer les données de tarification
        pricing_data = get_villa_pricing_from_db(villa_name)
        
        if not pricing_data:
            print(f"   ⚠️  Pas de données de tarification")
            return False
        
        print(f"   💰 Tarifs trouvés: {pricing_data.get('base_price', 0)}€")
        
        # Créer la section tarification
        tarification_html = create_tarification_section_html(villa_name, pricing_data)
        
        # Chercher où insérer (après les équipements ou avant la réservation)
        patterns = [
            r'(</div>\s*<!-- Fin équipements -->)',
            r'(</div>\s*<!-- Fin description -->)',
            r'(<div[^>]*class="[^"]*reservation[^"]*")',
            r'(<div[^>]*class="[^"]*booking[^"]*")',
            r'(<div[^>]*class="[^"]*contact[^"]*")',
            r'(<footer)'
        ]
        
        inserted = False
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                content = re.sub(pattern, tarification_html + r'\1', content, flags=re.IGNORECASE)
                inserted = True
                break
        
        if not inserted:
            # Insérer avant la fin du body
            content = content.replace('</body>', tarification_html + '\n</body>')
            inserted = True
        
        # Sauvegarder le fichier modifié
        if inserted:
            page_path.write_text(content, encoding='utf-8')
            print(f"   ✅ Section tarification ajoutée")
            return True
        else:
            print(f"   ❌ Impossible d'insérer la section")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def main():
    """Fonction principale Phase 4"""
    print("🔧 PHASE 4 : INTERFACE UTILISATEUR")
    print("=" * 40)
    
    # Trouver les pages de villa
    villa_pages = find_villa_pages()
    
    print(f"📋 {len(villa_pages)} pages HTML trouvées")
    
    # Filtrer les pages pertinentes
    relevant_pages = []
    for page in villa_pages:
        if any(keyword in page.name.lower() for keyword in ['villa', 'studio', 'espace']):
            relevant_pages.append(page)
    
    print(f"🎯 {len(relevant_pages)} pages de villa détectées")
    
    # Ajouter la section tarification à chaque page
    print(f"\n🔄 AJOUT DE LA SECTION TARIFICATION")
    print("-" * 40)
    
    success_count = 0
    for page in relevant_pages:
        if add_tarification_to_page(page):
            success_count += 1
    
    print(f"\n📊 RÉSULTATS PHASE 4:")
    print(f"   - Pages traitées: {len(relevant_pages)}")
    print(f"   - Pages modifiées: {success_count}")
    print(f"   - Taux de réussite: {(success_count/len(relevant_pages))*100:.1f}%")
    
    if success_count > 0:
        print(f"\n✅ PHASE 4 TERMINÉE AVEC SUCCÈS")
        print(f"🎯 Section tarification ajoutée à {success_count} pages")
    else:
        print(f"\n⚠️  PHASE 4 TERMINÉE AVEC AVERTISSEMENT")
        print(f"🎯 Aucune modification effectuée")

if __name__ == "__main__":
    main()