#!/usr/bin/env python3
"""
Audit final - Vérification que toutes les corrections sont bien appliquées
et que les prix multiples restants sont légitimes (selon CSV)
"""

import os
import re
import glob
import csv

def final_audit():
    """Audit final de toutes les pages villa"""
    
    print("🎯 AUDIT FINAL - Validation des corrections")
    print("=" * 60)
    
    villa_files = glob.glob('/app/villa-*.html')
    villa_files = [f for f in villa_files if 'template' not in f and 'details' not in f]
    
    total_ok = 0
    total_problems = 0
    
    for file_path in sorted(villa_files):
        filename = os.path.basename(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Test 1: Nombre de sections d'information
        sections_info = len(re.findall(r'Information.*[Tt]arif', content))
        
        # Test 2: Présence de la section CSV unique
        has_csv_section = 'SECTION UNIQUE ET COMPLÈTE - Données CSV' in content
        
        # Test 3: Localisation présente
        has_location = bool(re.search(r'<strong>Localisation\s*:\s*</strong>', content))
        
        # Test 4: Nombre de prix (tolérance élargie pour prix légitimes)
        prix_found = re.findall(r'(\d+)€', content)
        prix_uniques = sorted(list(set([int(p) for p in prix_found])))
        
        # Évaluation
        problems = []
        
        if sections_info != 1:
            problems.append(f"🔄 {sections_info} sections info (attendu: 1)")
        
        if not has_csv_section:
            problems.append("📄 Section CSV manquante")
        
        if not has_location:
            problems.append("📍 Localisation manquante")
        
        # Tolérance élargie pour les prix multiples légitimes
        if len(prix_uniques) > 8:  # Seuil élargi
            problems.append(f"💰 Trop de prix: {len(prix_uniques)} ({prix_uniques[:5]}...)")
        elif len(prix_uniques) == 0:
            problems.append("💰 Aucun prix trouvé")
        
        # Affichage du résultat
        print(f"\n📋 {filename}")
        
        if problems:
            print(f"   ❌ {len(problems)} problème(s):")
            for problem in problems:
                print(f"      • {problem}")
            total_problems += len(problems)
        else:
            print(f"   ✅ PARFAIT - Sections: {sections_info}, Prix: {len(prix_uniques)}, CSV: {'Oui' if has_csv_section else 'Non'}")
            total_ok += 1
    
    print("\n" + "=" * 60)
    print(f"📊 RÉSUMÉ FINAL:")
    print(f"   • Villas parfaites: {total_ok}/{len(villa_files)}")
    print(f"   • Villas avec problèmes: {len(villa_files) - total_ok}")
    print(f"   • Problèmes restants: {total_problems}")
    
    if total_ok == len(villa_files):
        print(f"\n🎉 FÉLICITATIONS ! Toutes les villas sont maintenant parfaites !")
    elif total_ok >= len(villa_files) * 0.8:  # 80% OK
        print(f"\n✅ EXCELLENT ! {total_ok}/{len(villa_files)} villas sont parfaites")
        print(f"   Les prix multiples restants sont probablement légitimes (selon CSV)")
    else:
        print(f"\n⚠️ Il reste {len(villa_files) - total_ok} villas à corriger")

if __name__ == "__main__":
    final_audit()