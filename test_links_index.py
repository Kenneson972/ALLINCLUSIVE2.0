#!/usr/bin/env python3
"""
Test des liens entre index.html et les nouvelles pages villa
"""

import re
from pathlib import Path

def test_villa_links():
    """Teste que tous les liens de l'index pointent vers les bonnes pages"""
    
    # Lire l'index.html
    with open('/app/index.html', 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    # Extraire le mapping des villas
    mapping_match = re.search(r'const villaPageMapping = {(.*?)};', index_content, re.DOTALL)
    if not mapping_match:
        print("❌ Impossible de trouver le mapping des villas dans index.html")
        return False
    
    mapping_text = mapping_match.group(1)
    
    # Extraire tous les noms de fichiers du mapping
    villa_files = re.findall(r'"([^"]*\.html)"', mapping_text)
    
    print("🔍 VÉRIFICATION DES LIENS INDEX → PAGES VILLA")
    print("=" * 60)
    
    all_files_exist = True
    missing_files = []
    existing_files = []
    
    for villa_file in villa_files:
        file_path = Path(f'/app/{villa_file}')
        if file_path.exists():
            existing_files.append(villa_file)
            print(f"✅ {villa_file}")
        else:
            missing_files.append(villa_file)
            print(f"❌ {villa_file} - FICHIER MANQUANT")
            all_files_exist = False
    
    print(f"\n📊 RÉSULTATS:")
    print(f"✅ Fichiers existants: {len(existing_files)}")
    print(f"❌ Fichiers manquants: {len(missing_files)}")
    
    if missing_files:
        print(f"\n⚠️ FICHIERS MANQUANTS:")
        for missing in missing_files:
            print(f"   - {missing}")
    
    # Vérifier que toutes les 21 nouvelles pages sont référencées
    expected_pages = [
        'villa-f3-petit-macabou.html',
        'villa-f3-baccha.html', 
        'villa-f3-francois.html',
        'villa-f5-ste-anne.html',
        'villa-f6-lamentin.html',
        'villa-f6-ste-luce.html',
        'villa-f5-vauclin.html',
        'villa-f7-baie-mulets.html',
        'villa-f5-la-renee.html',
        'bas-villa-trinite-cosmy.html',
        'bas-villa-robert.html',
        'bas-villa-ste-luce.html',
        'studio-cocooning-lamentin.html',
        'appartement-trenelle.html',
        'villa-fete-ducos.html',
        'villa-fete-fort-de-france.html',
        'villa-fete-riviere-pilote.html',
        'villa-fete-riviere-salee.html',
        'villa-fete-sainte-luce.html',
        'espace-piscine-bungalow.html',
        'villa-f6-petit-macabou-fete.html'
    ]
    
    print(f"\n📋 VÉRIFICATION PAGES CRÉÉES vs MAPPING:")
    referenced_pages = set(villa_files)
    expected_pages_set = set(expected_pages)
    
    not_referenced = expected_pages_set - referenced_pages
    not_created = referenced_pages - expected_pages_set
    
    if not_referenced:
        print(f"⚠️ PAGES CRÉÉES NON RÉFÉRENCÉES dans index.html:")
        for page in not_referenced:
            print(f"   - {page}")
    
    if not_created:
        print(f"⚠️ PAGES RÉFÉRENCÉES NON CRÉÉES:")
        for page in not_created:
            print(f"   - {page}")
    
    success = all_files_exist and not not_referenced and not not_created
    
    if success:
        print(f"\n🎉 SUCCÈS COMPLET!")
        print(f"✅ Tous les liens index → pages villa fonctionnent")
        print(f"✅ Les 21 pages villa sont toutes référencées")
        print(f"✅ Navigation parfaitement synchronisée")
    else:
        print(f"\n⚠️ ACTIONS REQUISES:")
        if missing_files:
            print(f"   - Créer les fichiers manquants")
        if not_referenced:
            print(f"   - Ajouter les pages non référencées au mapping")
        if not_created:
            print(f"   - Créer les pages référencées manquantes ou corriger le mapping")
    
    return success

def test_reverse_links():
    """Teste que toutes les nouvelles pages pointent bien vers index.html"""
    
    expected_pages = [
        'villa-f3-petit-macabou.html',
        'villa-f3-baccha.html', 
        'villa-f3-francois.html',
        'villa-f5-ste-anne.html',
        'villa-f6-lamentin.html',
        'villa-f6-ste-luce.html',
        'villa-f5-vauclin.html',
        'villa-f7-baie-mulets.html',
        'villa-f5-la-renee.html',
        'bas-villa-trinite-cosmy.html',
        'bas-villa-robert.html',
        'bas-villa-ste-luce.html',
        'studio-cocooning-lamentin.html',
        'appartement-trenelle.html',
        'villa-fete-ducos.html',
        'villa-fete-fort-de-france.html',
        'villa-fete-riviere-pilote.html',
        'villa-fete-riviere-salee.html',
        'villa-fete-sainte-luce.html',
        'espace-piscine-bungalow.html',
        'villa-f6-petit-macabou-fete.html'
    ]
    
    print(f"\n🔗 VÉRIFICATION LIENS RETOUR: PAGES VILLA → INDEX")
    print("=" * 60)
    
    missing_back_links = []
    
    for page in expected_pages:
        file_path = Path(f'/app/{page}')
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'href="./index.html"' in content:
                print(f"✅ {page}")
            else:
                missing_back_links.append(page)
                print(f"❌ {page} - LIEN VERS INDEX MANQUANT")
    
    if not missing_back_links:
        print(f"\n🎉 Tous les liens retour vers index.html sont présents!")
    else:
        print(f"\n⚠️ {len(missing_back_links)} pages sans lien retour vers index.html")
    
    return len(missing_back_links) == 0

if __name__ == "__main__":
    print("🧪 TEST COMPLET DES LIENS INDEX ↔ PAGES VILLA")
    print("=" * 70)
    
    # Test liens index → pages villa
    forward_links_ok = test_villa_links()
    
    # Test liens pages villa → index
    back_links_ok = test_reverse_links()
    
    print(f"\n" + "="*70)
    if forward_links_ok and back_links_ok:
        print("🎉 NAVIGATION PARFAITEMENT SYNCHRONISÉE!")
        print("✅ Index.html → Pages villa : FONCTIONNEL")
        print("✅ Pages villa → Index.html : FONCTIONNEL")
        print("✅ Toutes les 21 pages villa sont connectées")
    else:
        print("⚠️ PROBLÈMES DE NAVIGATION DÉTECTÉS")
        if not forward_links_ok:
            print("❌ Liens index → pages villa à corriger")
        if not back_links_ok:
            print("❌ Liens pages villa → index à corriger")