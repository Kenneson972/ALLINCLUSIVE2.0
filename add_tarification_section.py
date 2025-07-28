#!/usr/bin/env python3
"""
Ajouter une section tarification dans les pages de villa existantes
"""

import os
import re
from pathlib import Path

def find_villa_pages():
    """Trouve toutes les pages de villa HTML"""
    app_dir = Path('/app')
    villa_pages = []
    
    # Chercher les pages villa-*.html
    for html_file in app_dir.glob('villa-*.html'):
        villa_pages.append(html_file)
    
    # Chercher les pages avec des noms de villa
    for html_file in app_dir.glob('*.html'):
        if 'villa' in html_file.name.lower() or 'studio' in html_file.name.lower():
            if html_file.name not in ['villa-template.html', 'villa-details.html']:
                villa_pages.append(html_file)
    
    return villa_pages

def get_villa_pricing_from_api(villa_name):
    """Récupère les tarifs d'une villa depuis l'API"""
    import requests
    try:
        response = requests.get("https://60538156-1356-4530-8795-27ab33f42945.preview.emergentagent.com/api/villas")
        if response.status_code == 200:
            villas = response.json()
            for villa in villas:
                if villa_name.lower() in villa.get('name', '').lower():
                    return villa.get('pricing_details', {})
    except:
        pass
    return {}

def create_tarification_section(villa_name, pricing_data):
    """Crée la section tarification HTML"""
    if not pricing_data:
        return ""
    
    # Prix de base
    base_price = pricing_data.get('base_price', 0)
    weekend_price = pricing_data.get('weekend', base_price)
    week_price = pricing_data.get('week', base_price)
    high_season_price = pricing_data.get('high_season', base_price)
    
    # Section tarification
    tarification_html = f"""
    <!-- Section Tarification -->
    <div class="tarification-section">
        <div class="glass-card p-6 mb-8">
            <h3 class="text-2xl font-bold text-white mb-6 flex items-center">
                <i class="fas fa-euro-sign mr-3 text-[#4a9eff]"></i>
                Tarification
            </h3>
            
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <!-- Prix de base -->
                <div class="tarif-card">
                    <div class="tarif-header">
                        <i class="fas fa-calendar-day"></i>
                        <h4>Prix de base</h4>
                    </div>
                    <div class="tarif-price">{base_price}€</div>
                    <div class="tarif-period">par nuit</div>
                </div>
                
                <!-- Weekend -->
                <div class="tarif-card">
                    <div class="tarif-header">
                        <i class="fas fa-calendar-week"></i>
                        <h4>Weekend</h4>
                    </div>
                    <div class="tarif-price">{weekend_price}€</div>
                    <div class="tarif-period">2-3 nuits</div>
                </div>
                
                <!-- Semaine -->
                <div class="tarif-card">
                    <div class="tarif-header">
                        <i class="fas fa-calendar-alt"></i>
                        <h4>Semaine</h4>
                    </div>
                    <div class="tarif-price">{week_price}€</div>
                    <div class="tarif-period">7 jours</div>
                </div>
                
                <!-- Haute saison -->
                <div class="tarif-card highlight">
                    <div class="tarif-header">
                        <i class="fas fa-star"></i>
                        <h4>Haute saison</h4>
                    </div>
                    <div class="tarif-price">{high_season_price}€</div>
                    <div class="tarif-period">Juillet/Août/Décembre</div>
                </div>
    """
    
    # Ajouter les suppléments fêtes si disponibles
    party_rates = pricing_data.get('party_rates', {})
    if party_rates:
        tarification_html += """
                <!-- Suppléments fêtes -->
                <div class="tarif-card party">
                    <div class="tarif-header">
                        <i class="fas fa-glass-cheers"></i>
                        <h4>Suppléments fêtes</h4>
                    </div>
                    <div class="tarif-details">
        """
        
        for guest_count, price in party_rates.items():
            guests_num = guest_count.replace('_guests', '').replace('_', ' ')
            tarification_html += f"""
                        <div class="supplement-item">
                            <span>{guests_num} invités</span>
                            <span class="supplement-price">+{price - base_price}€</span>
                        </div>
            """
        
        tarification_html += """
                    </div>
                </div>
        """
    
    tarification_html += """
            </div>
            
            <!-- Détails supplémentaires -->
            <div class="tarif-details-section mt-6">
                <h4 class="text-lg font-semibold text-white mb-3">Détails</h4>
                <div class="tarif-note">
                    <i class="fas fa-info-circle text-[#4a9eff] mr-2"></i>
                    <span class="text-white/80">{}</span>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Styles pour la section tarification -->
    <style>
        .tarification-section {{
            margin: 2rem 0;
        }}
        
        .tarif-card {{
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            transition: all 0.3s ease;
        }}
        
        .tarif-card:hover {{
            background: rgba(255, 255, 255, 0.15);
            transform: translateY(-2px);
        }}
        
        .tarif-card.highlight {{
            background: rgba(74, 158, 255, 0.2);
            border-color: rgba(74, 158, 255, 0.5);
        }}
        
        .tarif-card.party {{
            background: rgba(255, 107, 107, 0.2);
            border-color: rgba(255, 107, 107, 0.5);
        }}
        
        .tarif-header {{
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1rem;
        }}
        
        .tarif-header i {{
            color: #4a9eff;
            font-size: 1.2rem;
            margin-right: 0.5rem;
        }}
        
        .tarif-header h4 {{
            color: white;
            font-size: 1.1rem;
            font-weight: 600;
        }}
        
        .tarif-price {{
            font-size: 2rem;
            font-weight: bold;
            color: #4a9eff;
            margin-bottom: 0.5rem;
        }}
        
        .tarif-period {{
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.9rem;
        }}
        
        .tarif-details {{
            text-align: left;
        }}
        
        .supplement-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.5rem 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .supplement-item:last-child {{
            border-bottom: none;
        }}
        
        .supplement-item span {{
            color: white;
            font-size: 0.9rem;
        }}
        
        .supplement-price {{
            color: #ff6b6b;
            font-weight: bold;
        }}
        
        .tarif-note {{
            background: rgba(255, 255, 255, 0.05);
            padding: 1rem;
            border-radius: 8px;
            display: flex;
            align-items: flex-start;
        }}
        
        @media (max-width: 768px) {{
            .tarif-card {{
                padding: 1rem;
            }}
            
            .tarif-price {{
                font-size: 1.5rem;
            }}
        }}
    </style>
    """.format(pricing_data.get('details', 'Tarifs selon saison et durée de séjour'))
    
    return tarification_html

def add_tarification_to_villa_page(villa_page_path):
    """Ajoute la section tarification à une page de villa"""
    try:
        # Lire le contenu de la page
        with open(villa_page_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extraire le nom de la villa du contenu
        villa_name = ""
        title_match = re.search(r'<title>([^<]+)</title>', content)
        if title_match:
            villa_name = title_match.group(1).split(' - ')[0]
        
        # Récupérer les données de tarification
        pricing_data = get_villa_pricing_from_api(villa_name)
        
        if not pricing_data:
            print(f"⚠️  Pas de données de tarification pour: {villa_name}")
            return False
        
        # Créer la section tarification
        tarification_section = create_tarification_section(villa_name, pricing_data)
        
        # Chercher où insérer la section (après les équipements ou la description)
        insertion_patterns = [
            r'(</div>\s*<!-- Fin équipements -->)',
            r'(</div>\s*<!-- Fin description -->)',
            r'(<div class="amenities-section">)',
            r'(<div class="location-section">)',
            r'(<div class="reservation-section">)'
        ]
        
        inserted = False
        for pattern in insertion_patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, tarification_section + r'\1', content)
                inserted = True
                break
        
        # Si pas d'insertion trouvée, insérer avant la section de réservation
        if not inserted:
            reservation_match = re.search(r'(<div[^>]*class="[^"]*reservation[^"]*"[^>]*>)', content)
            if reservation_match:
                content = content.replace(reservation_match.group(1), tarification_section + reservation_match.group(1))
                inserted = True
        
        # Sauvegarder le fichier modifié
        if inserted:
            with open(villa_page_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Section tarification ajoutée à: {villa_page_path.name}")
            return True
        else:
            print(f"⚠️  Impossible d'insérer la section dans: {villa_page_path.name}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur avec {villa_page_path.name}: {e}")
        return False

def main():
    """Fonction principale"""
    print("💰 AJOUT DE LA SECTION TARIFICATION AUX PAGES VILLA")
    print("=" * 60)
    
    # Trouver toutes les pages villa
    villa_pages = find_villa_pages()
    
    if not villa_pages:
        print("⚠️  Aucune page villa trouvée")
        return
    
    print(f"📋 {len(villa_pages)} pages villa trouvées:")
    for page in villa_pages:
        print(f"   - {page.name}")
    
    # Ajouter la section tarification à chaque page
    print(f"\n🔄 AJOUT DE LA SECTION TARIFICATION")
    print("-" * 40)
    
    success_count = 0
    for villa_page in villa_pages:
        if add_tarification_to_villa_page(villa_page):
            success_count += 1
    
    print(f"\n📊 RÉSULTATS:")
    print(f"   - Pages modifiées: {success_count}/{len(villa_pages)}")
    print(f"   - Taux de réussite: {(success_count/len(villa_pages))*100:.1f}%")
    
    print(f"\n✅ AJOUT DE LA SECTION TARIFICATION TERMINÉ")

if __name__ == "__main__":
    main()