#!/usr/bin/env python3
"""
AUDIT COMPLET DE TOUTE LA PLATEFORME KHANELCONCEPT
Vérification et correction de toutes les pages importantes
"""

import os
import re
from pathlib import Path
import json

# Pages principales à auditer par catégorie
PAGES_PRINCIPALES = {
    'core': [
        'index.html',           # Page d'accueil
        'reservation.html',     # Réservation
    ],
    'auth': [
        'login.html',           # Connexion
        'register.html',        # Inscription  
        'dashboard.html',       # Tableau de bord membre
        'profile.html',         # Profil membre
        'reset-password.html',  # Réinitialisation mot de passe
        'email-verification.html' # Vérification email
    ],
    'member': [
        'loyalty.html',         # Programme fidélité
        'wishlist.html',        # Liste de souhaits
        'notifications.html',   # Notifications
        'wallet.html',          # Portefeuille
        'concierge.html',       # Service conciergerie
        'sos-depannage.html'    # SOS dépannage
    ],
    'services': [
        'prestataires.html',    # Prestataires
        'billetterie.html',     # Billetterie
        'mobilier.html',        # Mobilier
        'excursions.html',      # Excursions
        'pmr.html'              # Accessibilité PMR
    ],
    'admin': [
        'admin/admin.html',     # Panel admin
        'admin/login.html',     # Connexion admin
        'admin/dashboard.html', # Dashboard admin
        'admin/villas-management.html',     # Gestion villas
        'admin/reservations-management.html' # Gestion réservations
    ]
}

def audit_page_errors(file_path):
    """Audit approfondi d'une page"""
    errors = []
    warnings = []
    
    try:
        if not os.path.exists(file_path):
            return {
                'exists': False,
                'errors': ['Page manquante'],
                'warnings': [],
                'file_size_kb': 0
            }
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        file_size = os.path.getsize(file_path) / 1024
        
        # 1. STRUCTURE HTML BASIQUE
        if '<!DOCTYPE html>' not in content:
            errors.append("DOCTYPE HTML5 manquant")
        
        if '<html' not in content:
            errors.append("Balise <html> manquante")
            
        if '<head>' not in content or '</head>' not in content:
            errors.append("Section <head> malformée")
            
        if '<body' not in content or '</body>' not in content:
            errors.append("Section <body> malformée")
        
        # 2. META DONNÉES ESSENTIELLES
        if '<meta charset=' not in content:
            errors.append("Charset non défini")
            
        if 'viewport' not in content:
            warnings.append("Meta viewport manquant (SEO mobile)")
            
        if '<title>' not in content:
            errors.append("Titre de page manquant")
        elif len(re.findall(r'<title>(.*?)</title>', content)) > 1:
            warnings.append("Titres multiples détectés")
        
        # 3. RESSOURCES EXTERNES
        # CSS
        css_links = re.findall(r'<link[^>]*href="([^"]*\.css[^"]*)"', content)
        for css_link in css_links:
            if css_link.startswith('http') or css_link.startswith('//'):
                continue  # CDN ok
            elif css_link.startswith('./'):
                local_path = f"/app/{css_link[2:]}"
                if not os.path.exists(local_path):
                    errors.append(f"CSS manquant: {css_link}")
        
        # JavaScript
        js_scripts = re.findall(r'<script[^>]*src="([^"]*\.js[^"]*)"', content)
        for js_script in js_scripts:
            if js_script.startswith('http') or js_script.startswith('//'):
                continue  # CDN ok
            elif js_script.startswith('./'):
                local_path = f"/app/{js_script[2:]}"
                if not os.path.exists(local_path):
                    errors.append(f"JavaScript manquant: {js_script}")
        
        # 4. NAVIGATION ET LIENS
        internal_links = re.findall(r'href="(\./[^"]*\.html)"', content)
        for link in internal_links:
            link_path = f"/app/{link[2:]}"
            if not os.path.exists(link_path):
                errors.append(f"Lien cassé: {link}")
        
        # 5. IMAGES
        images = re.findall(r'src="(\./images/[^"]*)"', content)
        broken_images = 0
        for img in images:
            img_path = f"/app/{img[2:]}"
            if not os.path.exists(img_path):
                broken_images += 1
        
        if broken_images > 0:
            warnings.append(f"{broken_images} image(s) manquante(s)")
        
        # 6. FORMULAIRES
        forms = re.findall(r'<form[^>]*>', content)
        for form in forms:
            if 'action=' not in form:
                warnings.append("Formulaire sans action définie")
        
        # 7. SPÉCIFICITÉS PAR TYPE DE PAGE
        page_name = os.path.basename(file_path)
        
        # Page d'accueil
        if page_name == 'index.html':
            if 'video-background' not in content:
                warnings.append("Vidéo background manquante sur l'accueil")
            if 'villa-card' not in content:
                errors.append("Cards villa manquantes sur l'accueil")
        
        # Page réservation
        elif page_name == 'reservation.html':
            if 'reservationForm' not in content:
                errors.append("Formulaire de réservation manquant")
            if 'calculateTotalPrice' not in content:
                warnings.append("Calcul de prix manquant")
        
        # Pages auth
        elif page_name in ['login.html', 'register.html']:
            if 'password' not in content:
                errors.append("Champs mot de passe manquant")
            if 'email' not in content:
                errors.append("Champs email manquant")
        
        # Dashboard
        elif page_name == 'dashboard.html':
            if 'user-profile' not in content and 'member-' not in content:
                warnings.append("Éléments dashboard manquants")
        
        # 8. SÉCURITÉ
        if 'password' in content and 'type="text"' in content:
            warnings.append("Possible champ mot de passe non sécurisé")
        
        # 9. PERFORMANCE
        if file_size > 500:
            warnings.append(f"Page lourde ({file_size:.1f}KB)")
        
        if content.count('<script') > 15:
            warnings.append(f"Nombreux scripts ({content.count('<script')})")
        
        # 10. ACCESSIBILITÉ
        img_without_alt = len(re.findall(r'<img(?![^>]*alt=)', content))
        if img_without_alt > 0:
            warnings.append(f"{img_without_alt} image(s) sans attribut alt")
        
        return {
            'exists': True,
            'errors': errors,
            'warnings': warnings,
            'file_size_kb': round(file_size, 1),
            'css_count': len(css_links),
            'js_count': len(js_scripts),
            'form_count': len(forms),
            'image_count': len(images)
        }
        
    except Exception as e:
        return {
            'exists': True,
            'errors': [f"Erreur lecture: {str(e)}"],
            'warnings': [],
            'file_size_kb': 0
        }

def check_backend_integration():
    """Vérifier l'intégration backend"""
    issues = []
    
    # Vérifier server.py
    if not os.path.exists('/app/backend/server.py'):
        issues.append("Backend server.py manquant")
        return issues
    
    try:
        with open('/app/backend/server.py', 'r', encoding='utf-8') as f:
            backend_content = f.read()
        
        # Endpoints critiques
        critical_endpoints = [
            '/api/villas', '/api/reservations', '/api/auth/login', 
            '/api/auth/register', '/api/members', '/api/admin'
        ]
        
        for endpoint in critical_endpoints:
            if endpoint not in backend_content:
                issues.append(f"Endpoint manquant: {endpoint}")
        
        # MongoDB
        if 'mongodb' not in backend_content.lower() and 'mongo' not in backend_content.lower():
            issues.append("Configuration MongoDB manquante")
            
    except Exception as e:
        issues.append(f"Erreur lecture backend: {str(e)}")
    
    return issues

def check_assets_consistency():
    """Vérifier la cohérence des assets"""
    issues = []
    
    # CSS
    css_dir = Path('/app/assets/css')
    if css_dir.exists():
        for css_file in css_dir.glob('*.css'):
            if css_file.stat().st_size == 0:
                issues.append(f"CSS vide: {css_file.name}")
    else:
        issues.append("Dossier assets/css manquant")
    
    # JS
    js_dir = Path('/app/assets/js')
    if js_dir.exists():
        for js_file in js_dir.glob('*.js'):
            if js_file.stat().st_size == 0:
                issues.append(f"JS vide: {js_file.name}")
    else:
        issues.append("Dossier assets/js manquant")
    
    # Images critiques
    logo_exists = any(Path('/app').glob('**/logo*.png'))
    if not logo_exists:
        issues.append("Logo principal manquant")
    
    return issues

def main():
    print("🔍 AUDIT COMPLET DE LA PLATEFORME KHANELCONCEPT")
    print("=" * 80)
    
    all_results = {}
    total_errors = 0
    total_warnings = 0
    pages_auditées = 0
    
    # Auditer toutes les pages par catégorie
    for category, pages in PAGES_PRINCIPALES.items():
        print(f"\n📂 CATÉGORIE: {category.upper()}")
        print("-" * 40)
        
        category_results = {}
        
        for page in pages:
            file_path = f"/app/{page}"
            print(f"🔍 Audit de {page}...")
            
            result = audit_page_errors(file_path)
            category_results[page] = result
            
            if result['exists']:
                pages_auditées += 1
                errors_count = len(result['errors'])
                warnings_count = len(result['warnings'])
                
                total_errors += errors_count
                total_warnings += warnings_count
                
                if errors_count == 0 and warnings_count == 0:
                    print(f"  ✅ {page}: Aucun problème")
                else:
                    if errors_count > 0:
                        print(f"  🔴 {page}: {errors_count} erreur(s)")
                        for error in result['errors'][:2]:  # Afficher 2 premières erreurs
                            print(f"     • {error}")
                    
                    if warnings_count > 0:
                        print(f"  🟡 {page}: {warnings_count} warning(s)")
            else:
                print(f"  ❌ {page}: Page manquante")
        
        all_results[category] = category_results
    
    # Vérifications système
    print(f"\n🔧 VÉRIFICATIONS SYSTÈME")
    print("-" * 40)
    
    backend_issues = check_backend_integration()
    if backend_issues:
        print(f"🔴 Backend: {len(backend_issues)} problème(s)")
        for issue in backend_issues[:3]:
            print(f"  • {issue}")
    else:
        print("✅ Backend: Configuration OK")
    
    assets_issues = check_assets_consistency()
    if assets_issues:
        print(f"🟡 Assets: {len(assets_issues)} problème(s)")
        for issue in assets_issues[:3]:
            print(f"  • {issue}")
    else:
        print("✅ Assets: Structure OK")
    
    # Pages villa
    villa_files = list(Path('/app').glob('villa-*.html'))
    villa_count = len([f for f in villa_files if f.name not in ['villa-details.html', 'villa-template.html']])
    print(f"🏠 Pages villa: {villa_count} pages détectées")
    
    # RÉSUMÉ FINAL
    print(f"\n" + "=" * 80)
    print(f"📊 RÉSUMÉ DE L'AUDIT COMPLET")
    print(f"   📄 Pages auditées: {pages_auditées}")
    print(f"   🔴 Total erreurs: {total_errors}")
    print(f"   🟡 Total warnings: {total_warnings}")
    print(f"   🏠 Pages villa: {villa_count}")
    print(f"   🔧 Problèmes backend: {len(backend_issues)}")
    print(f"   📦 Problèmes assets: {len(assets_issues)}")
    
    # Sauvegarder les résultats
    audit_data = {
        'pages': all_results,
        'backend_issues': backend_issues,
        'assets_issues': assets_issues,
        'summary': {
            'pages_audited': pages_auditées,
            'total_errors': total_errors,
            'total_warnings': total_warnings,
            'villa_pages': villa_count
        }
    }
    
    with open('/app/audit_plateforme_complete.json', 'w', encoding='utf-8') as f:
        json.dump(audit_data, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"💾 Résultats sauvés: audit_plateforme_complete.json")
    
    # RECOMMANDATIONS
    print(f"\n🛠️  RECOMMANDATIONS PRIORITAIRES:")
    
    if total_errors > 20:
        print("  🚨 CRITIQUE: Nombreuses erreurs - correction urgente requise")
    elif total_errors > 5:
        print("  ⚠️  Erreurs modérées - correction recommandée")
    elif total_errors == 0:
        print("  ✅ Aucune erreur critique détectée")
    
    if len(backend_issues) > 3:
        print("  🔧 Backend: Problèmes d'intégration à corriger")
    
    if total_warnings > 30:
        print("  🔄 Optimisations: Nombreuses améliorations possibles")
    
    # Pages manquantes critiques
    pages_manquantes = []
    for category, results in all_results.items():
        for page, result in results.items():
            if not result['exists'] and category in ['core', 'auth']:
                pages_manquantes.append(page)
    
    if pages_manquantes:
        print(f"  📄 Pages critiques manquantes: {', '.join(pages_manquantes)}")
    
    return audit_data

if __name__ == "__main__":
    results = main()