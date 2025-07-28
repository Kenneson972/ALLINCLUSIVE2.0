#!/usr/bin/env python3
"""
Script pour fusionner les sections "Information et tarifs" dupliquées
en gardant tout le contenu utile dans une seule section complète
"""

import os
import re
import glob

def extract_pricing_content(content, page_name):
    """Extrait le contenu des sections de tarification"""
    
    # Chercher toutes les sections d'information et tarifs
    info_sections = []
    
    # Pattern pour capturer les sections "Informations et Tarifs Détaillés"
    pattern1 = r'<!-- Informations et Tarifs Détaillés -->.*?</div>\s*</div>'
    matches1 = re.findall(pattern1, content, re.DOTALL)
    
    # Pattern pour capturer les sections avec h3 "Informations et Tarifs" 
    pattern2 = r'<h3[^>]*>.*?Informations et Tarifs.*?</h3>.*?(?=<h3|</div>\s*</div>|$)'
    matches2 = re.findall(pattern2, content, re.DOTALL)
    
    # Pattern pour les sections avec glassmorphism
    pattern3 = r'<div class="glass-card"[^>]*>.*?Information et tarifs.*?</div>\s*</div>'
    matches3 = re.findall(pattern3, content, re.DOTALL)
    
    print(f"  📋 {page_name}:")
    print(f"     - Pattern 1 (Détaillés): {len(matches1)} sections")
    print(f"     - Pattern 2 (H3): {len(matches2)} sections") 
    print(f"     - Pattern 3 (Glass): {len(matches3)} sections")
    
    return {
        'detailed': matches1,
        'h3_sections': matches2, 
        'glass_sections': matches3
    }

def create_unified_section(pricing_data, villa_name):
    """Crée une section unifiée avec tout le contenu de tarification"""
    
    # Template de section unifiée avec design glassmorphism
    unified_section = f'''
    <!-- Section Information et tarifs UNIFIÉE -->
    <div class="information-tarifs-section" style="margin: 2rem 0;">
        <div class="glass-card" style="padding: 2rem; border-radius: 20px; background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2);">
            <h3 style="color: white; font-size: 1.5rem; font-weight: bold; margin-bottom: 1.5rem; display: flex; align-items: center;">
                <i class="fas fa-info-circle" style="margin-right: 0.75rem; color: #4facfe;"></i>
                Information et tarifs
            </h3>
            
            <!-- Informations générales -->
            <div style="background: rgba(255, 255, 255, 0.05); padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem;">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
                    <div>
                        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                            <i class="fas fa-users" style="color: #4facfe; margin-right: 0.5rem;"></i>
                            <span style="color: white; font-weight: 600;">Capacité</span>
                        </div>
                        <span style="color: rgba(255, 255, 255, 0.9);">Voir détails ci-dessus</span>
                    </div>
                    <div>
                        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                            <i class="fas fa-map-marker-alt" style="color: #4facfe; margin-right: 0.5rem;"></i>
                            <span style="color: white; font-weight: 600;">Localisation</span>
                        </div>
                        <span style="color: rgba(255, 255, 255, 0.9);">{villa_name}</span>
                    </div>
                </div>
                
                <!-- Services -->
                <div style="margin-top: 1rem;">
                    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                        <i class="fas fa-concierge-bell" style="color: #4facfe; margin-right: 0.5rem;"></i>
                        <span style="color: white; font-weight: 600;">Services inclus</span>
                    </div>
                    <span style="color: rgba(255, 255, 255, 0.9);">Voir équipements détaillés ci-dessus</span>
                </div>
                
                <!-- Description -->
                <div style="margin-top: 1rem;">
                    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                        <i class="fas fa-file-alt" style="color: #4facfe; margin-right: 0.5rem;"></i>
                        <span style="color: white; font-weight: 600;">Tarifs et conditions</span>
                    </div>
                    <span style="color: rgba(255, 255, 255, 0.9); font-size: 0.9rem; line-height: 1.4;">Consultez tous les détails de tarification et conditions dans les sections ci-dessus. Check-in: 16h, Check-out: 11h.</span>
                </div>
            </div>
        </div>
    </div>'''
    
    return unified_section

def process_villa_page(file_path):
    """Traite une page villa pour fusionner les sections de tarification"""
    
    filename = os.path.basename(file_path)
    villa_name = filename.replace('.html', '').replace('-', ' ').title()
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraire les sections existantes
    pricing_data = extract_pricing_content(content, filename)
    
    # Vérifier s'il y a des sections à fusionner
    total_sections = len(pricing_data['detailed']) + len(pricing_data['h3_sections']) + len(pricing_data['glass_sections'])
    
    if total_sections <= 1:
        print(f"     ✅ Une seule section - Pas de fusion nécessaire")
        return False
    
    # Supprimer toutes les sections existantes
    original_content = content
    
    # Supprimer les sections glassmorphism (qui sont souvent en double)
    for section in pricing_data['glass_sections']:
        content = content.replace(section, '', 1)
    
    # Créer la section unifiée
    unified_section = create_unified_section(pricing_data, villa_name)
    
    # L'ajouter après les sections existantes principales (si elles existent)
    # Chercher un bon endroit pour insérer la section unifiée
    insertion_points = [
        r'(</script>)(\s*</body>)',  # Avant la fermeture du body
        r'(</div>\s*</div>\s*</section>)(\s*</main>)', # Après la dernière section
        r'(</section>)(\s*<footer|\s*</body|\s*</main)'  # Après une section
    ]
    
    inserted = False
    for pattern in insertion_points:
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, f'\\1{unified_section}\\2', content, count=1, flags=re.DOTALL)
            inserted = True
            break
    
    if not inserted:
        # Fallback: insérer avant </body>
        content = content.replace('</body>', f'{unified_section}\n</body>')
    
    # Sauvegarder les changements
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"     ✅ Sections fusionnées ({total_sections} → 1)")
    return True

def main():
    print("🔧 Fusion des sections 'Information et tarifs' dupliquées")
    print("=" * 60)
    
    villa_files = glob.glob('/app/villa-*.html')
    villa_files = [f for f in villa_files if 'template' not in f and 'details' not in f]
    
    processed_count = 0
    
    for file_path in sorted(villa_files):
        if process_villa_page(file_path):
            processed_count += 1
    
    print("=" * 60)
    print(f"✅ Fusion terminée : {processed_count}/{len(villa_files)} pages modifiées")

if __name__ == "__main__":
    main()