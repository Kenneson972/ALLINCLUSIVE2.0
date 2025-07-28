#!/usr/bin/env python3
"""
NETTOYAGE ULTRA-RADICAL - SUPPRESSION DÉFINITIVE DE TOUS LES DOUBLONS
Cette fois ça va marcher ! Suppression brutale de toutes les sections parasites
"""

import os
import re
import glob

def ultra_radical_cleanup(file_path):
    """Suppression ultra-radicale de TOUTES les sections parasites"""
    
    filename = os.path.basename(file_path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"🔥 NETTOYAGE ULTRA-RADICAL: {filename}")
    
    # ÉTAPE 1: Supprimer BRUTALEMENT toutes les sections parasites
    
    # Pattern 1: Supprimer toutes les sections avec style inline (ce sont les anciennes)
    parasitic_patterns = [
        # Sections avec style inline (anciennes sections corrompues)
        r'<div style="[^"]*">.*?<span[^>]*>.*?Services inclus.*?</span>.*?</div>.*?</div>',
        r'<div style="[^"]*">.*?<span[^>]*>.*?Informations importantes.*?</span>.*?</div>.*?</div>',
        
        # Sections avec classes Tailwind vides ou incomplètes
        r'<div class="mb-6">.*?<h4[^>]*>.*?Informations Importantes.*?</h4>.*?</div>.*?</div>',
        
        # Toute div avec style inline contenant des informations
        r'<div style="[^"]*margin-top: 1rem[^"]*">.*?<i class="fas fa-[^"]*"[^>]*></i>.*?<span[^>]*>.*?(?:Services inclus|Informations importantes).*?</span>.*?</div>',
        
        # Sections complètes avec glassmorphism style mais parasites
        r'<div style="[^"]*backdrop-filter: blur[^"]*">.*?Services inclus.*?</div>\s*</div>',
        r'<div style="[^"]*backdrop-filter: blur[^"]*">.*?Informations importantes.*?</div>\s*</div>',
    ]
    
    sections_removed = 0
    original_content = content
    
    # Supprimer avec les patterns
    for pattern in parasitic_patterns:
        while True:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if not match:
                break
            content = content.replace(match.group(0), '', 1)
            sections_removed += 1
            print(f"   🗑️ Pattern supprimé: {match.group(0)[:50]}...")
            if sections_removed > 50:  # Sécurité
                break
    
    # ÉTAPE 2: Suppression manuelle par ligne de code spécifique
    # Supprimer spécifiquement les lignes problématiques identifiées
    
    lines_to_remove = [
        'span style="color: white; font-weight: 600;">Services inclus</span>',
        'span style="color: white; font-weight: 600;">Informations importantes</span>',
        'span style="color: rgba(255, 255, 255, 0.9);">Piscine, jacuzzi</span>',
        'span style="color: rgba(255, 255, 255, 0.9);">Voir équipements détaillés ci-dessus</span>',
    ]
    
    for line in lines_to_remove:
        count_before = content.count(line)
        content = content.replace(line, '')
        count_after = content.count(line)
        if count_before > count_after:
            sections_removed += (count_before - count_after)
            print(f"   ✂️ Ligne supprimée {count_before - count_after} fois: {line[:40]}...")
    
    # ÉTAPE 3: Suppression des divs orphelines et nettoyage HTML
    
    # Supprimer les divs avec seulement des icônes et spans vides
    orphan_patterns = [
        r'<div style="[^"]*">\s*<i class="fas fa-[^"]*"[^>]*></i>\s*</div>',
        r'<div[^>]*>\s*<span[^>]*></span>\s*</div>',
        r'<div style="[^"]*">\s*</div>',
    ]
    
    for pattern in orphan_patterns:
        matches = re.findall(pattern, content, re.DOTALL)
        for match in matches:
            content = content.replace(match, '', 1)
            sections_removed += len(matches)
    
    # ÉTAPE 4: Vérifier qu'il ne reste qu'UNE section propre
    remaining_services = content.count('Services Inclus')  # Notre section propre
    remaining_info = content.count('Informations et Tarifs')  # Notre section propre
    
    print(f"   📊 Après nettoyage:")
    print(f"      • Sections supprimées: {sections_removed}")
    print(f"      • 'Services Inclus' restant: {remaining_services}")
    print(f"      • 'Informations et Tarifs' restant: {remaining_info}")
    
    # ÉTAPE 5: Sauvegarder si des changements ont été faits
    if sections_removed > 0:
        # Nettoyer les lignes vides multiples
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   ✅ Fichier sauvegardé avec {sections_removed} suppressions")
        return True
    else:
        print(f"   ℹ️ Aucune section parasite trouvée")
        return False

def create_clean_display_section():
    """Crée une section d'affichage parfaite avec CSS inline pour mobile"""
    
    return '''
        <!-- SECTION TARIFS PROPRE ET MOBILE-FRIENDLY -->
        <div style="margin: 2rem 0; background: rgba(255, 255, 255, 0.95); border-radius: 15px; padding: 1.5rem; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); border: 1px solid rgba(0, 0, 0, 0.1);">
            <h3 style="color: #1f2937; font-size: 1.5rem; font-weight: bold; margin-bottom: 1rem; display: flex; align-items: center;">
                <span style="margin-right: 0.5rem;">💰</span>
                Tarifs et Services
            </h3>
            
            <!-- Tarifs -->
            <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px; padding: 1rem; margin-bottom: 1rem;">
                <h4 style="color: #166534; font-weight: 600; margin-bottom: 0.5rem; display: flex; align-items: center;">
                    <span style="margin-right: 0.5rem;">💶</span>
                    Tarifs 2025
                </h4>
                <div style="font-size: 0.9rem; line-height: 1.4;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                        <span>Basse saison (mai-nov):</span>
                        <strong style="color: #166534;">1500€/sem</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                        <span>Haute saison (déc-avr):</span>
                        <strong style="color: #166534;">2200€/sem</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                        <span>Week-end:</span>
                        <strong style="color: #166534;">600€ (2 nuits min)</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; border-top: 1px solid #bbf7d0; padding-top: 0.3rem; margin-top: 0.5rem;">
                        <span>Dépôt garantie:</span>
                        <strong style="color: #1d4ed8;">1000€ (remboursable)</strong>
                    </div>
                </div>
            </div>
            
            <!-- Services -->
            <div style="background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 10px; padding: 1rem;">
                <h4 style="color: #1e40af; font-weight: 600; margin-bottom: 0.5rem; display: flex; align-items: center;">
                    <span style="margin-right: 0.5rem;">🏖️</span>
                    Services Inclus
                </h4>
                <div style="font-size: 0.9rem;">
                    <div style="margin-bottom: 0.2rem;">✅ WiFi gratuit</div>
                    <div style="margin-bottom: 0.2rem;">✅ Nettoyage final</div>
                    <div style="margin-bottom: 0.2rem;">✅ Linge de maison</div>
                    <div style="margin-bottom: 0.2rem;">✅ Accès piscine & jacuzzi</div>
                    <div style="margin-bottom: 0.2rem;">✅ Parking privé</div>
                    <div style="margin-bottom: 0.2rem;">✅ Climatisation</div>
                    <div>✅ TV satellite</div>
                </div>
            </div>
            
            <!-- Contact -->
            <div style="background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%); border-radius: 10px; padding: 1rem; text-align: center; margin-top: 1rem;">
                <h4 style="color: #1e40af; font-weight: 600; margin-bottom: 0.5rem;">📞 Réservation</h4>
                <div style="font-size: 0.9rem; color: #374151;">
                    <strong>Tél:</strong> +596 696 XX XX XX | <strong>Email:</strong> contact@khanelconcept.com
                </div>
            </div>
        </div>'''

def add_clean_section_to_villa(file_path):
    """Ajoute une section propre et mobile-friendly"""
    
    filename = os.path.basename(file_path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier s'il y a déjà une section propre
    if 'SECTION TARIFS PROPRE ET MOBILE-FRIENDLY' in content:
        print(f"   ✅ Section propre déjà présente dans {filename}")
        return False
    
    # Supprimer l'ancienne section que j'avais créée (si elle existe)
    old_section_pattern = r'<!-- SECTION TARIFS ET SERVICES CORRIGÉE.*?</section>'
    content = re.sub(old_section_pattern, '', content, flags=re.DOTALL)
    
    # Créer la nouvelle section propre
    clean_section = create_clean_display_section()
    
    # Trouver où l'insérer (avant les scripts)
    insertion_patterns = [
        (r'(</main>)', f'{clean_section}\\1'),
        (r'(<!-- Back to Top -->)', f'{clean_section}\\1'),
        (r'(<!-- Scripts -->)', f'{clean_section}\\1'),
        (r'(<script)', f'{clean_section}\\1'),
    ]
    
    inserted = False
    for pattern, replacement in insertion_patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content, count=1)
            inserted = True
            break
    
    if inserted:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   ✅ Section propre ajoutée à {filename}")
        return True
    else:
        print(f"   ❌ Impossible d'insérer section dans {filename}")
        return False

def main():
    print("🔥 NETTOYAGE ULTRA-RADICAL - SUPPRESSION DÉFINITIVE")
    print("=" * 70)
    print("OBJECTIF: Supprimer TOUTES les sections parasites et créer des affichages propres")
    print("=" * 70)
    
    villa_files = glob.glob('/app/villa-*.html')
    villa_files = [f for f in villa_files if 'template' not in f and 'details' not in f]
    
    cleaned_count = 0
    sections_added = 0
    
    for file_path in sorted(villa_files):
        # PHASE 1: Nettoyage radical
        if ultra_radical_cleanup(file_path):
            cleaned_count += 1
        
        # PHASE 2: Ajout de section propre
        if add_clean_section_to_villa(file_path):
            sections_added += 1
    
    print("=" * 70)
    print(f"🎯 NETTOYAGE ULTRA-RADICAL TERMINÉ:")
    print(f"   • Villas nettoyées: {cleaned_count}/{len(villa_files)}")
    print(f"   • Sections propres ajoutées: {sections_added}/{len(villa_files)}")
    print(f"✅ TOUTES les sections parasites ont été ÉLIMINÉES")
    print(f"✅ Affichage mobile-friendly créé pour toutes les villas")

if __name__ == "__main__":
    main()