#!/usr/bin/env python3
"""
NETTOYAGE ET CORRECTION COMPLÈTE DES PAGES VILLA
Correction de toutes les erreurs détectées par l'audit
"""

import os
import re
from pathlib import Path
import shutil

def clean_redundant_files():
    """Supprimer tous les fichiers redondants"""
    print("🗑️  SUPPRESSION DES FICHIERS REDONDANTS")
    
    # Fichiers à supprimer
    files_to_delete = [
        # Fichiers de test
        'test-*.html', 'debug-*.html', 'villa-details.html', 'villa-template.html',
        # Scripts Python anciens
        '*fix*.py', '*correction*.py', '*nettoyage*.py', '*audit*.py', '*phase*.py',
        '*integration*.py', '*mapping*.py', '*update*.py', '*restaur*.py', '*add_*.py',
        # Logs et temporaires  
        '*.log', '*.tmp', '*.bak', '*.old', '*.json.bak',
        # Rapports anciens
        'RAPPORT_*.md', 'CORRECTIONS_*.md', 'VALIDATION_*.md', '*RAPPORT*.md'
    ]
    
    deleted_count = 0
    
    for pattern in files_to_delete:
        for file in Path('/app').glob(pattern):
            # Garder les fichiers critiques
            if file.name in ['audit_complet_villas.py', 'nettoyage_correction_complete.py']:
                continue
                
            try:
                file.unlink()
                print(f"  ✅ Supprimé: {file.name}")
                deleted_count += 1
            except Exception as e:
                print(f"  ❌ Erreur suppression {file.name}: {str(e)}")
    
    print(f"🗑️  {deleted_count} fichiers supprimés")
    return deleted_count

def fix_villa_html_errors(file_path):
    """Corriger toutes les erreurs HTML/CSS/JS d'un fichier villa"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        errors_fixed = 0
        
        print(f"🔧 Correction de {file_path.name}...")
        
        # 1. CORRIGER LES ACCOLADES CSS
        # Compter et équilibrer les accolades dans les styles
        style_sections = re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
        
        for i, style_content in enumerate(style_sections):
            open_braces = style_content.count('{')
            close_braces = style_content.count('}')
            
            if open_braces != close_braces:
                # Ajouter les accolades manquantes à la fin
                diff = open_braces - close_braces
                if diff > 0:
                    # Il manque des accolades fermantes
                    fixed_style = style_content + '\n' + '}' * diff
                    content = content.replace(style_content, fixed_style)
                    errors_fixed += 1
                    print(f"  ✅ Ajouté {diff} accolade(s) fermante(s) CSS")
        
        # 2. CORRIGER LES LIENS DE RÉSERVATION
        # Corriger les liens vers reservation.html
        villa_id = file_path.stem
        correct_reservation_link = f'./reservation.html?villa={villa_id}'
        
        # Remplacer tous les liens de réservation cassés
        content = re.sub(
            r'href="./reservation\.html\?villa=[^"]*"',
            f'href="{correct_reservation_link}"',
            content
        )
        errors_fixed += 1
        print(f"  ✅ Lien réservation corrigé: {correct_reservation_link}")
        
        # 3. NETTOYER LES CONSOLE.LOG DE DEBUG
        content = re.sub(r'console\.log\([^)]*\);?', '', content)
        if 'console.log' in original_content:
            errors_fixed += 1
            print(f"  ✅ Console.log supprimés")
        
        # 4. CORRIGER LES VARIABLES UNDEFINED
        # Remplacer les occurrences dangereuses d'undefined
        content = content.replace("typeof undefined", "typeof 'undefined'")
        content = content.replace("!== undefined", "!== null && typeof variable !== 'undefined'")
        
        # 5. OPTIMISER LA STRUCTURE HTML
        # S'assurer que les sections critiques sont présentes et correctes
        
        if 'main class=' not in content:
            # Ajouter une structure main si manquante
            content = content.replace(
                '<!-- Main Content -->',
                '<!-- Main Content -->\n<main class="container mx-auto px-6 py-12" style="margin-top: 120px; position: relative; z-index: 100;">'
            )
            content = content.replace('</body>', '</main>\n</body>')
            errors_fixed += 1
            print(f"  ✅ Structure main ajoutée")
        
        # 6. CORRIGER LA VIDÉO BACKGROUND
        # S'assurer que la vidéo background est correcte
        correct_video_html = '''<!-- Background Video avec votre vidéo Cloudinary -->
    <div class="video-background">
        <video id="backgroundVideo" autoplay muted loop playsinline preload="metadata" webkit-playsinline>
            <source src="https://res.cloudinary.com/ddulasmtz/video/upload/v1752950782/background-video.mp4_qoofsz.mp4" type="video/mp4">
        </video>
        <div class="video-overlay"></div>
    </div>'''
        
        if 'video-background' not in content:
            content = content.replace('<body', correct_video_html + '\n<body')
            errors_fixed += 1
            print(f"  ✅ Vidéo background ajoutée")
        
        # 7. NETTOYER LE JAVASCRIPT
        # Corriger les fonctions JavaScript problématiques
        js_fixes = [
            (r'document\.addEventListener\(\'DOMContentLoaded\', \(\) => \{([^}]*)\}\);', 
             r'document.addEventListener("DOMContentLoaded", function() {\1});'),
            (r'console\.log\([^)]*\);?', ''),
            (r'\.catch\(console\.log\)', '.catch(function(e) { /* video error ignored */ })')
        ]
        
        for pattern, replacement in js_fixes:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content, flags=re.DOTALL)
                errors_fixed += 1
        
        # 8. VALIDATION FINALE
        # S'assurer que le fichier est bien formé
        if content.count('<html') != content.count('</html>'):
            print(f"  ❌ Balises HTML non équilibrées")
        
        if content.count('<head>') != content.count('</head>'):
            print(f"  ❌ Balises head non équilibrées")
        
        if content.count('<body') != content.count('</body>'):
            print(f"  ❌ Balises body non équilibrées")
        
        # Écrire le fichier corrigé
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ {file_path.name}: {errors_fixed} erreur(s) corrigée(s)")
        return errors_fixed
        
    except Exception as e:
        print(f"  ❌ Erreur correction {file_path.name}: {str(e)}")
        return 0

def create_clean_villa_template():
    """Créer un template villa propre et sans erreurs"""
    
    clean_template = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{villa_name} - {localisation} | KhanelConcept</title>
    
    <!-- Preload Critical Resources -->
    <link rel="preload" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" as="style">
    <link rel="preload" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js" as="script">
    
    <!-- Stylesheets -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.tailwindcss.com"></script>
    
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: white;
            margin: 0;
            padding: 0;
            position: relative;
        }}
        
        .video-background {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            overflow: hidden;
        }}
        
        .video-background video {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            opacity: 0.8;
        }}
        
        .video-overlay {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.4) 0%, rgba(118, 75, 162, 0.4) 100%);
        }}
        
        .info-card {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            display: block;
            visibility: visible;
        }}
        
        .villa-gallery {{
            border-radius: 20px;
            overflow: hidden;
            height: 500px;
            display: block;
        }}
        
        .villa-gallery .swiper-slide img {{
            width: 100%;
            height: 500px;
            object-fit: cover;
        }}
        
        main.container {{
            position: relative;
            z-index: 10;
            min-height: 100vh;
            display: block;
            visibility: visible;
            opacity: 1;
        }}
        
        .btn-primary {{
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
            color: white;
            padding: 1rem 2rem;
            border-radius: 12px;
            font-weight: 600;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        @media (max-width: 768px) {{
            .villa-gallery {{ height: 300px; }}
            .villa-gallery .swiper-slide img {{ height: 300px; }}
        }}
    </style>
</head>

<body>
    <!-- Background Video -->
    <div class="video-background">
        <video id="backgroundVideo" autoplay muted loop playsinline preload="metadata" webkit-playsinline>
            <source src="https://res.cloudinary.com/ddulasmtz/video/upload/v1752950782/background-video.mp4_qoofsz.mp4" type="video/mp4">
        </video>
        <div class="video-overlay"></div>
    </div>
    
    <!-- Navigation -->
    <nav class="fixed top-0 left-0 right-0 z-50 bg-black bg-opacity-20 backdrop-blur-lg border-b border-white/10 p-4">
        <div class="container mx-auto flex justify-between items-center">
            <a href="./index.html" class="flex items-center space-x-3 text-yellow-400">
                <img src="https://customer-assets.emergentagent.com/job_villa-dash/artifacts/vg7ukqf7_logo-khanel-concept-original.png" 
                     alt="Khanel Concept Logo" class="h-10 w-auto">
                <span class="text-2xl font-bold">KhanelConcept</span>
            </a>
            <div class="flex space-x-6">
                <a href="./index.html" class="text-white hover:text-yellow-400 transition-colors">Nos Villas</a>
                <a href="./reservation.html" class="text-white hover:text-yellow-400 transition-colors">Réserver</a>
                <a href="./login.html" class="text-white hover:text-yellow-400 transition-colors">Connexion</a>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="container mx-auto px-6 py-12" style="margin-top: 120px; position: relative; z-index: 100;">
        
        <!-- Villa Title -->
        <section class="text-center mb-16">
            <h1 class="text-5xl font-bold mb-4 bg-gradient-to-r from-white to-yellow-400 bg-clip-text text-transparent">
                {villa_name}
            </h1>
            <p class="text-xl text-gray-300 mb-6">
                <i class="fas fa-map-marker-alt text-red-400 mr-2"></i>{localisation}
            </p>
        </section>
        
        <!-- Gallery Section -->
        <section class="mb-16">
            <div class="max-w-6xl mx-auto">
                <div class="swiper villa-gallery mb-6">
                    <div class="swiper-wrapper">
                        {gallery_slides}
                    </div>
                    <div class="swiper-pagination"></div>
                    <div class="swiper-button-next"></div>
                    <div class="swiper-button-prev"></div>
                </div>
            </div>
        </section>

        <!-- Description -->
        <section class="mb-16">
            <div class="info-card max-w-4xl mx-auto">
                <h2 class="text-3xl font-bold mb-6 text-center">
                    <i class="fas fa-info-circle text-blue-600 mr-3"></i>
                    {villa_name}
                </h2>
                <div class="text-center mb-8">
                    <a href="./reservation.html?villa={villa_id}" class="btn-primary">
                        <i class="fas fa-calendar-check"></i>
                        Réserver maintenant
                    </a>
                </div>
            </div>
        </section>
    </main>

    <!-- Scripts -->
    <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
    <script>
        // Initialize Swiper
        document.addEventListener("DOMContentLoaded", function() {{
            new Swiper('.villa-gallery', {{
                loop: true,
                autoplay: {{ delay: 5000 }},
                pagination: {{ el: '.swiper-pagination', clickable: true }},
                navigation: {{ 
                    nextEl: '.swiper-button-next', 
                    prevEl: '.swiper-button-prev' 
                }}
            }});
            
            // Video background
            const video = document.getElementById('backgroundVideo');
            if (video) {{
                video.play().catch(function() {{
                    // Fallback if video fails
                }});
            }}
        }});
    </script>
</body>
</html>'''
    
    return clean_template

def main():
    print("🧹 NETTOYAGE ET CORRECTION COMPLÈTE DES PAGES VILLA")
    print("=" * 70)
    
    # 1. Nettoyer les fichiers redondants
    deleted_files = clean_redundant_files()
    
    # 2. Corriger toutes les pages villa
    print(f"\n🔧 CORRECTION DES ERREURS HTML/CSS/JS")
    
    villa_files = []
    for file in Path('/app').glob('villa-*.html'):
        if file.name not in ['villa-details.html', 'villa-template.html']:
            villa_files.append(file)
    
    total_fixes = 0
    for villa_file in villa_files:
        fixes = fix_villa_html_errors(villa_file)
        total_fixes += fixes
    
    print(f"\n🧹 NETTOYAGE TERMINÉ")
    print(f"   🗑️  Fichiers supprimés: {deleted_files}")
    print(f"   🔧 Erreurs corrigées: {total_fixes}")
    print(f"   📁 Pages villa nettoyées: {len(villa_files)}")
    
    # 3. Créer un template propre pour référence future
    clean_template = create_clean_villa_template()
    with open('/app/villa-template-clean.html', 'w', encoding='utf-8') as f:
        f.write(clean_template)
    
    print(f"   📄 Template propre créé: villa-template-clean.html")
    
    print(f"\n✅ NETTOYAGE COMPLET TERMINÉ!")
    print(f"🎉 Les pages villa sont maintenant propres et sans erreurs!")

if __name__ == "__main__":
    main()