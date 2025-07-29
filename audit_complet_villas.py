#!/usr/bin/env python3
"""
AUDIT COMPLET DES PAGES VILLA - Détection de tous les bugs et fichiers redondants
"""

import os
import re
from pathlib import Path
import json

def audit_html_errors(file_path):
    """Audit des erreurs HTML/CSS/JS dans un fichier"""
    errors = []
    warnings = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. ERREURS CRITIQUES HTML
        if '<html' not in content:
            errors.append("Structure HTML manquante")
        
        if content.count('<html') > 1:
            errors.append("Balises HTML dupliquées")
            
        if content.count('<head>') != content.count('</head>'):
            errors.append("Balises <head> non fermées")
            
        if content.count('<body') != content.count('</body>'):
            errors.append("Balises <body> non fermées")
        
        # 2. ERREURS JAVASCRIPT
        if 'document.addEventListener(' in content and 'DOMContentLoaded' not in content:
            warnings.append("Listeners sans DOMContentLoaded")
            
        if 'function(' in content and content.count('{') != content.count('}'):
            errors.append("Accolades JavaScript non équilibrées")
            
        if 'console.log(' in content:
            warnings.append("Console.log présents (debug)")
            
        if 'undefined' in content:
            warnings.append("Variables 'undefined' potentielles")
            
        # 3. ERREURS CSS
        if content.count('{') != content.count('}'):
            errors.append("Accolades CSS non équilibrées")
            
        if 'style>' in content and 'background:' not in content:
            warnings.append("CSS background manquant")
            
        # 4. LIENS ET RESSOURCES
        broken_links = re.findall(r'href="([^"]*)"', content)
        for link in broken_links:
            if link.startswith('./') and not os.path.exists(f"/app/{link[2:]}"):
                errors.append(f"Lien cassé: {link}")
                
        missing_images = re.findall(r'src="(./images/[^"]*)"', content)
        for img in missing_images:
            if not os.path.exists(f"/app/{img[2:]}"):
                errors.append(f"Image manquante: {img}")
                
        # 5. STRUCTURE ET CONTENU
        if 'villa-gallery' not in content:
            errors.append("Section galerie manquante")
            
        if 'swiper-slide' not in content:
            errors.append("Slides Swiper manquants")
            
        if 'btn-primary' not in content:
            errors.append("Bouton réservation manquant")
            
        if 'video-background' not in content:
            warnings.append("Vidéo background absente")
            
        # 6. DOUBLONS ET REDONDANCES
        if content.count('<!DOCTYPE html>') > 1:
            errors.append("DOCTYPE dupliqué")
            
        if content.count('<title>') > 1:
            errors.append("Balises title dupliquées")
            
        script_tags = content.count('<script')
        if script_tags > 10:
            warnings.append(f"Trop de scripts ({script_tags})")
            
        # 7. PROBLÈMES SPÉCIFIQUES
        if 'AOS' in content and 'aos.js' not in content:
            errors.append("AOS utilisé sans la librairie")
            
        if 'Swiper' in content and 'swiper-bundle' not in content:
            errors.append("Swiper utilisé sans la librairie")
            
        # 8. PERFORMANCE
        file_size = os.path.getsize(file_path) / 1024  # KB
        if file_size > 200:
            warnings.append(f"Fichier volumineux ({file_size:.1f}KB)")
            
        return {
            'errors': errors,
            'warnings': warnings,
            'file_size_kb': round(file_size, 1),
            'script_count': script_tags,
            'image_count': len(missing_images)
        }
        
    except Exception as e:
        return {
            'errors': [f"Erreur lecture fichier: {str(e)}"],
            'warnings': [],
            'file_size_kb': 0,
            'script_count': 0,
            'image_count': 0
        }

def find_redundant_files():
    """Trouver les fichiers redondants à supprimer"""
    redundant_files = []
    
    # 1. Fichiers de test et debug
    debug_files = [
        'test-*.html', 'debug-*.html', 'villa-details.html', 'villa-template.html',
        '*-test.js', '*-debug.js', '*.log', '*.tmp', '*.bak', '*.old'
    ]
    
    for pattern in debug_files:
        for file in Path('/app').glob(pattern):
            redundant_files.append(str(file))
    
    # 2. Scripts Python de correction (gardons seulement les plus récents)
    py_files = list(Path('/app').glob('*fix*.py'))
    py_files.extend(Path('/app').glob('*correction*.py'))
    py_files.extend(Path('/app').glob('*nettoyage*.py'))
    
    if len(py_files) > 5:  # Garder seulement les 5 plus récents
        py_files_sorted = sorted(py_files, key=lambda x: x.stat().st_mtime, reverse=True)
        for old_file in py_files_sorted[5:]:
            redundant_files.append(str(old_file))
    
    # 3. Fichiers de rapport anciens
    old_reports = []
    for file in Path('/app').glob('RAPPORT_*.md'):
        if file.stat().st_mtime < (Path('/app/audit_complet_villas.py').stat().st_mtime - 3600):  # 1h
            old_reports.append(str(file))
    
    redundant_files.extend(old_reports)
    
    return redundant_files

def check_villa_consistency():
    """Vérifier la cohérence entre les pages villa"""
    inconsistencies = []
    
    villa_files = []
    for file in Path('/app').glob('villa-*.html'):
        if file.name not in ['villa-details.html', 'villa-template.html']:
            villa_files.append(file)
    
    # Vérifier la structure commune
    required_elements = [
        'video-background', 'swiper-slide', 'btn-primary', 'info-card'
    ]
    
    for villa_file in villa_files:
        try:
            with open(villa_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            missing_elements = []
            for element in required_elements:
                if element not in content:
                    missing_elements.append(element)
            
            if missing_elements:
                inconsistencies.append({
                    'file': villa_file.name,
                    'missing': missing_elements
                })
                
        except Exception as e:
            inconsistencies.append({
                'file': villa_file.name,
                'error': str(e)
            })
    
    return inconsistencies

def main():
    print("🔍 AUDIT COMPLET DES PAGES VILLA - DÉTECTION DES BUGS")
    print("=" * 70)
    
    # 1. AUDIT DES FICHIERS VILLA
    villa_files = []
    for file in Path('/app').glob('villa-*.html'):
        if file.name not in ['villa-details.html', 'villa-template.html']:
            villa_files.append(file)
    
    print(f"📁 Analyse de {len(villa_files)} pages villa...")
    
    total_errors = 0
    total_warnings = 0
    audit_results = {}
    
    for villa_file in villa_files:
        print(f"\n🔍 Audit de {villa_file.name}")
        
        result = audit_html_errors(villa_file)
        audit_results[villa_file.name] = result
        
        errors_count = len(result['errors'])
        warnings_count = len(result['warnings'])
        
        total_errors += errors_count
        total_warnings += warnings_count
        
        if errors_count > 0:
            print(f"  ❌ {errors_count} erreur(s):")
            for error in result['errors']:
                print(f"     • {error}")
        
        if warnings_count > 0:
            print(f"  ⚠️  {warnings_count} warning(s):")
            for warning in result['warnings'][:3]:  # Limiter l'affichage
                print(f"     • {warning}")
        
        if errors_count == 0 and warnings_count == 0:
            print(f"  ✅ Aucun problème détecté")
    
    # 2. FICHIERS REDONDANTS
    print(f"\n🗑️  FICHIERS REDONDANTS À SUPPRIMER")
    redundant_files = find_redundant_files()
    
    if redundant_files:
        print(f"Trouvé {len(redundant_files)} fichier(s) redondant(s):")
        for file in redundant_files[:10]:  # Afficher les 10 premiers
            print(f"  📄 {file}")
        if len(redundant_files) > 10:
            print(f"  ... et {len(redundant_files) - 10} autres")
    else:
        print("✅ Aucun fichier redondant trouvé")
    
    # 3. COHÉRENCE DES VILLAS
    print(f"\n🔗 VÉRIFICATION DE LA COHÉRENCE")
    inconsistencies = check_villa_consistency()
    
    if inconsistencies:
        print(f"❌ {len(inconsistencies)} incohérence(s) trouvée(s):")
        for issue in inconsistencies:
            if 'missing' in issue:
                print(f"  📄 {issue['file']}: Manque {', '.join(issue['missing'])}")
            elif 'error' in issue:
                print(f"  📄 {issue['file']}: Erreur - {issue['error']}")
    else:
        print("✅ Structure cohérente sur toutes les pages")
    
    # 4. RÉSUMÉ FINAL
    print(f"\n" + "=" * 70)
    print(f"📊 RÉSUMÉ DE L'AUDIT")
    print(f"   🔴 Total erreurs: {total_errors}")
    print(f"   🟡 Total warnings: {total_warnings}")
    print(f"   🗑️  Fichiers redondants: {len(redundant_files)}")
    print(f"   🔗 Incohérences: {len(inconsistencies)}")
    
    # Sauvegarder les résultats
    with open('/app/audit_results.json', 'w', encoding='utf-8') as f:
        json.dump({
            'villa_audits': audit_results,
            'redundant_files': redundant_files,
            'inconsistencies': inconsistencies,
            'summary': {
                'total_errors': total_errors,
                'total_warnings': total_warnings,
                'files_audited': len(villa_files)
            }
        }, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"💾 Résultats sauvés dans: audit_results.json")
    
    # Recommandations
    print(f"\n🛠️  RECOMMANDATIONS:")
    if total_errors > 10:
        print("  🚨 CRITIQUE: Nombreuses erreurs - nettoyage urgent requis")
    elif total_errors > 0:
        print("  ⚠️  Erreurs détectées - correction recommandée")
    
    if len(redundant_files) > 10:
        print("  🗑️  Nombreux fichiers à supprimer - nettoyage requis")
    
    if len(inconsistencies) > 3:
        print("  🔗 Structure incohérente - standardisation requise")
    
    return {
        'total_errors': total_errors,
        'total_warnings': total_warnings,
        'redundant_files': len(redundant_files),
        'inconsistencies': len(inconsistencies)
    }

if __name__ == "__main__":
    results = main()