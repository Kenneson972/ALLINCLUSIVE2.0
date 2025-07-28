#!/usr/bin/env python3
"""
Correction finale des 6 villas avec prix multiples
Nettoyage des prix parasites qui traînent dans le HTML
"""

import os
import re
import glob

def clean_parasitic_prices(file_path):
    """Supprime les prix parasites qui traînent dans le HTML"""
    
    filename = os.path.basename(file_path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Compter les prix avant nettoyage
    prix_avant = len(re.findall(r'(\d+)€', content))
    
    # Patterns de prix parasites à supprimer (en dehors de la section CSV)
    parasitic_patterns = [
        # Prix dans des spans ou divs orphelins
        r'<span[^>]*>\s*\d+€[^<]*</span>',
        r'<div[^>]*>\s*Prix[^:]*:\s*\d+€[^<]*</div>',
        # Prix dans des structures de cards anciennes
        r'<div class="[^"]*price[^"]*"[^>]*>\s*\d+€',
        r'class="[^"]*font-semibold[^"]*">\s*\d+€',
        # Prix dans des descriptions ou titres
        r'(\d+)€\s*(?:par|pour|/)?\s*(?:nuit|jour|semaine|weekend)?(?![^<]*</strong>)',
        # Prix dans les Quick Info Cards (garder seulement la section CSV)
        r'<div[^>]*text-lg font-semibold[^>]*>\d+[^<]*</div>(?![^<]*€)',
    ]
    
    sections_removed = 0
    
    # Nettoyer seulement AVANT la section CSV pour préserver les vrais prix
    # Trouver le début de la section CSV
    csv_section_start = content.find('<!-- SECTION UNIQUE ET COMPLÈTE - Données CSV -->')
    
    if csv_section_start > -1:
        # Séparer le contenu : avant CSV / section CSV / après CSV
        before_csv = content[:csv_section_start]
        csv_and_after = content[csv_section_start:]
        
        # Nettoyer seulement la partie AVANT la section CSV
        for pattern in parasitic_patterns:
            matches = re.findall(pattern, before_csv)
            for match in matches:
                before_csv = before_csv.replace(match, '', 1)
                sections_removed += 1
        
        # Reconstruire le contenu
        content = before_csv + csv_and_after
    else:
        print(f"⚠️ {filename}: Section CSV non trouvée")
        return False
    
    # Compter les prix après nettoyage
    prix_apres = len(re.findall(r'(\d+)€', content))
    
    if sections_removed > 0:
        # Sauvegarder les changements
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {filename}: {sections_removed} prix parasites supprimés ({prix_avant} → {prix_apres} prix)")
        return True
    else:
        print(f"ℹ️ {filename}: Aucun prix parasite trouvé")
        return False

def main():
    print("🧹 NETTOYAGE FINAL - Suppression des prix parasites")
    print("=" * 60)
    print("Cible: 6 villas avec trop de prix multiples")
    print("=" * 60)
    
    # Villas identifiées comme problématiques par l'audit
    problematic_villas = [
        '/app/villa-f3-le-francois.html',
        '/app/villa-f3-robert-pointe-hyacinthe.html', 
        '/app/villa-f3-trinite-cosmy.html',
        '/app/villa-f6-lamentin.html',
        '/app/villa-f7-baie-des-mulets-vauclin.html',
        '/app/villa-fete-journee-ducos.html'
    ]
    
    cleaned_count = 0
    
    for file_path in problematic_villas:
        if os.path.exists(file_path):
            if clean_parasitic_prices(file_path):
                cleaned_count += 1
        else:
            print(f"❌ Fichier non trouvé: {file_path}")
    
    print("=" * 60)
    print(f"🎯 NETTOYAGE TERMINÉ : {cleaned_count}/{len(problematic_villas)} villas nettoyées")
    
    # Relancer un audit rapide sur ces villas
    print("\n🔍 VÉRIFICATION POST-NETTOYAGE:")
    
    for file_path in problematic_villas:
        if os.path.exists(file_path):
            filename = os.path.basename(file_path)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Compter les prix restants
            prix_restants = re.findall(r'(\d+)€', content)
            prix_uniques = sorted(list(set([int(p) for p in prix_restants])))
            
            if len(prix_uniques) <= 4:  # Tolérance pour les vrais prix CSV
                print(f"   ✅ {filename}: {len(prix_uniques)} prix restants (OK)")
            else:
                print(f"   ⚠️ {filename}: {len(prix_uniques)} prix restants: {prix_uniques}")

if __name__ == "__main__":
    main()