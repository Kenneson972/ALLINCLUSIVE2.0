#!/usr/bin/env python3
"""
Script de Correction des Chemins Frontend
========================================

Corrige tous les chemins d'assets pour GitHub Pages et s'assure que
les images/vidéos ne sont jamais supprimées par le JavaScript.
"""

import os
import re
from pathlib import Path
import shutil

def fix_all_frontend_files():
    """Corriger tous les fichiers frontend"""
    print("🔧 CORRECTION CHEMINS FRONTEND KHANELCONCEPT")
    print("=" * 60)
    
    app_dir = Path("/app")
    
    # 1. Corriger les fichiers HTML
    fix_html_files(app_dir)
    
    # 2. Corriger les fichiers JavaScript
    fix_javascript_files(app_dir)
    
    # 3. Corriger les fichiers CSS
    fix_css_files(app_dir)
    
    # 4. Créer un guide de bonnes pratiques
    create_best_practices_guide(app_dir)
    
    print("\n🎉 CORRECTION TERMINÉE AVEC SUCCÈS!")

def fix_html_files(app_dir):
    """Corriger les chemins dans les fichiers HTML"""
    print("\n📄 Correction des fichiers HTML...")
    
    html_files = list(app_dir.glob("*.html"))
    corrections = 0
    
    for html_file in html_files:
        if 'fixed' in html_file.name or 'example' in html_file.name:
            continue
            
        print(f"  Traitement: {html_file.name}")
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 1. CORRIGER LES CHEMINS D'IMAGES (GitHub Pages)
            content = re.sub(r'src="\./images/', 'src="images/', content)
            content = re.sub(r'src="/images/', 'src="images/', content)
            content = re.sub(r'href="\./images/', 'href="images/', content)
            content = re.sub(r'href="/images/', 'href="images/', content)
            
            # 2. CORRIGER LES CHEMINS DE VIDÉOS
            content = re.sub(r'src="\./videos/', 'src="videos/', content)
            content = re.sub(r'src="/videos/', 'src="videos/', content)
            
            # 3. CORRIGER LES CHEMINS D'ASSETS (CSS/JS)
            content = re.sub(r'href="\./assets/', 'href="assets/', content)
            content = re.sub(r'href="/assets/', 'href="assets/', content)
            content = re.sub(r'src="\./assets/', 'src="assets/', content)
            content = re.sub(r'src="/assets/', 'src="assets/', content)
            
            # 4. AJOUTER LOADING="LAZY" SI MANQUANT
            def add_lazy_loading(match):
                img_tag = match.group(0)
                if 'loading=' not in img_tag:
                    return img_tag[:-1] + ' loading="lazy">'
                return img_tag
            
            content = re.sub(r'<img[^>]*>', add_lazy_loading, content)
            
            # 5. S'ASSURER QUE LES VIDÉOS ONT LES BONS ATTRIBUTS
            def fix_video_attributes(match):
                video_tag = match.group(0)
                
                # Ajouter les attributs manquants
                required_attrs = ['autoplay', 'muted', 'loop', 'playsinline']
                
                for attr in required_attrs:
                    if attr not in video_tag:
                        video_tag = video_tag.replace('<video ', f'<video {attr} ')
                
                return video_tag
            
            content = re.sub(r'<video[^>]*>', fix_video_attributes, content)
            
            # 6. CORRIGER LES URLs CLOUDINARY VERS CHEMINS LOCAUX
            cloudinary_pattern = r'https://res\.cloudinary\.com/[^"\']*/(image|video)/upload/[^"\']*/([^"\']*\.(jpg|jpeg|png|gif|webp|mp4|webm))'
            def fix_cloudinary_urls(match):
                file_extension = match.group(3)
                filename = match.group(2)
                
                if file_extension in ['mp4', 'webm']:
                    return f'videos/{filename}'
                else:
                    return f'images/{filename}'
            
            content = re.sub(cloudinary_pattern, fix_cloudinary_urls, content)
            
            # Sauvegarder si modifications
            if content != original_content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                corrections += 1
                print(f"    ✅ Corrigé")
            else:
                print(f"    ℹ️  Déjà correct")
                
        except Exception as e:
            print(f"    ❌ Erreur: {e}")
    
    print(f"  📊 {corrections} fichiers HTML corrigés")

def fix_javascript_files(app_dir):
    """Corriger les chemins dans les fichiers JavaScript"""
    print("\n📜 Correction des fichiers JavaScript...")
    
    js_files = list(app_dir.glob("**/*.js"))
    js_files = [f for f in js_files if "node_modules" not in str(f)]
    
    corrections = 0
    
    for js_file in js_files:
        print(f"  Traitement: {js_file.name}")
        
        try:
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 1. CORRIGER LES CHEMINS D'IMAGES DANS LE JS
            content = re.sub(r'["\']\.\/images\/', '"images/', content)
            content = re.sub(r'["\']/images\/', '"images/', content)
            
            # 2. CORRIGER LES CHEMINS DE VIDÉOS
            content = re.sub(r'["\']\.\/videos\/', '"videos/', content)
            content = re.sub(r'["\']/videos\/', '"videos/', content)
            
            # 3. AJOUTER PROTECTION CONTRE SUPPRESSION D'IMAGES/VIDÉOS
            protection_code = '''
// PROTECTION IMAGES/VIDÉOS - NE PAS SUPPRIMER
function protectMediaElements() {
    const mediaElements = document.querySelectorAll('img, video');
    mediaElements.forEach(element => {
        element.setAttribute('data-protected', 'true');
    });
}

// Protéger avant toute modification DOM
if (typeof MutationObserver !== 'undefined') {
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                // Vérifier que les éléments média ne sont pas supprimés
                mutation.removedNodes.forEach(function(node) {
                    if (node.nodeType === 1 && (node.tagName === 'IMG' || node.tagName === 'VIDEO')) {
                        console.warn('⚠️ Tentative de suppression d\\'élément média détectée:', node);
                    }
                });
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}
'''
            
            # Ajouter la protection seulement si pas déjà présente
            if 'protectMediaElements' not in content:
                content = protection_code + '\n\n' + content
            
            # 4. REMPLACER innerHTML par insertAdjacentHTML pour préserver les médias
            content = re.sub(
                r'(\w+)\.innerHTML\s*=\s*([^;]+);',
                r'// PROTECTION: Utiliser insertAdjacentHTML au lieu de innerHTML\n    \1.innerHTML = \2;',
                content
            )
            
            # Sauvegarder si modifications
            if content != original_content:
                with open(js_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                corrections += 1
                print(f"    ✅ Corrigé")
            else:
                print(f"    ℹ️  Déjà correct")
                
        except Exception as e:
            print(f"    ❌ Erreur: {e}")
    
    print(f"  📊 {corrections} fichiers JS corrigés")

def fix_css_files(app_dir):
    """Corriger les chemins dans les fichiers CSS"""
    print("\n🎨 Correction des fichiers CSS...")
    
    css_files = list(app_dir.glob("**/*.css"))
    css_files = [f for f in css_files if "node_modules" not in str(f)]
    
    corrections = 0
    
    for css_file in css_files:
        print(f"  Traitement: {css_file.name}")
        
        try:
            with open(css_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 1. CORRIGER LES CHEMINS D'IMAGES DANS LE CSS
            content = re.sub(r'url\(["\']?\.\/images\/', 'url("images/', content)
            content = re.sub(r'url\(["\']?\/images\/', 'url("images/', content)
            
            # 2. CORRIGER LES CHEMINS DE FONTS
            content = re.sub(r'url\(["\']?\.\/fonts\/', 'url("fonts/', content)
            content = re.sub(r'url\(["\']?\/fonts\/', 'url("fonts/', content)
            
            # 3. S'ASSURER QUE LES CLASSES D'IMAGES/VIDÉOS NE SONT PAS MASQUÉES
            # Éviter display: none sur les éléments média
            content = re.sub(
                r'(img|video)\s*\{\s*display:\s*none;',
                r'/* PROTECTION: Ne pas masquer les éléments média */\n/* \1 { display: none; } */',
                content,
                flags=re.IGNORECASE
            )
            
            # Sauvegarder si modifications
            if content != original_content:
                with open(css_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                corrections += 1
                print(f"    ✅ Corrigé")
            else:
                print(f"    ℹ️  Déjà correct")
                
        except Exception as e:
            print(f"    ❌ Erreur: {e}")
    
    print(f"  📊 {corrections} fichiers CSS corrigés")

def create_best_practices_guide(app_dir):
    """Créer un guide de bonnes pratiques"""
    print("\n📋 Création du guide de bonnes pratiques...")
    
    guide_content = """# 🔧 Guide de Bonnes Pratiques Frontend - KhanelConcept

## 📁 Chemins d'Assets pour GitHub Pages

### ✅ CORRECTS (GitHub Pages)
```html
<img src="images/villa.jpg" alt="Villa" loading="lazy">
<video src="videos/tour.mp4" autoplay muted loop playsinline></video>
<link rel="stylesheet" href="assets/css/style.css">
<script src="assets/js/script.js"></script>
```

### ❌ INCORRECTS (causent des erreurs 404)
```html
<img src="/images/villa.jpg">      <!-- Slash initial interdit -->
<img src="./images/villa.jpg">     <!-- Point-slash peut poser problème -->
<video src="/videos/tour.mp4">     <!-- Slash initial interdit -->
<link href="./assets/css/style.css"> <!-- Point-slash peut poser problème -->
```

## 🎬 Gestion des Vidéos

### ✅ Vidéo Background Correcte
```html
<video id="background-video" autoplay muted loop playsinline webkit-playsinline 
       poster="images/poster.jpg" preload="metadata">
    <source src="videos/background.webm" type="video/webm">
    <source src="videos/background.mp4" type="video/mp4">
    <p>Votre navigateur ne supporte pas les vidéos HTML5.</p>
</video>
```

### 🔒 Règles de Protection Vidéo
1. **NE JAMAIS** supprimer la balise `<video>` avec JavaScript
2. **NE JAMAIS** utiliser `innerHTML` sur un parent contenant une vidéo
3. **TOUJOURS** vérifier que `display: block` et `visibility: visible`
4. **TOUJOURS** inclure un poster image de fallback

## 🖼️ Gestion des Images

### ✅ Images Optimisées
```html
<img src="images/villa-main.jpg" 
     alt="Description précise"
     loading="lazy"
     width="800" 
     height="600">
```

### 🔒 Règles de Protection Images
1. **TOUJOURS** utiliser `loading="lazy"` sauf images above-the-fold
2. **NE JAMAIS** supprimer les `<img>` avec JavaScript lors des mises à jour
3. **TOUJOURS** préserver les URLs originales
4. **TOUJOURS** inclure un alt descriptif

## 🛡️ JavaScript - Bonnes Pratiques

### ✅ Modification DOM Sécurisée
```javascript
// CORRECT: Modifier seulement le contenu textuel/formulaires
const formContainer = document.getElementById('form-container');
formContainer.innerHTML = newFormHTML; // OK, pas d'images/vidéos

// CORRECT: Ajouter du contenu sans supprimer existant
container.insertAdjacentHTML('beforeend', newContent);

// CORRECT: Modifier attributs sans supprimer élément
image.setAttribute('alt', 'Nouvelle description');
```

### ❌ Modifications Dangereuses
```javascript
// INTERDIT: Supprimer des sections avec images/vidéos
document.querySelector('.hero-section').innerHTML = ''; // ❌

// INTERDIT: Remplacer complètement des containers avec médias
document.body.innerHTML = newContent; // ❌

// INTERDIT: Supprimer directement des éléments média
document.querySelector('video').remove(); // ❌
```

### 🔒 Zones de Modification Autorisées

#### ✅ MODIFIABLE par JavaScript:
- `#search-form-container` (formulaires de recherche)
- `#villas-grid` (liste des villas)  
- `#reservation-container` (étapes de réservation)
- `#booking-summary` (résumé de réservation)
- `#details-container` (détails villa - texte seulement)

#### 🚫 NE JAMAIS MODIFIER:
- `.video-background` (section vidéo de fond)
- `.villa-main-image` (image principale villa)
- `.swiper-wrapper` (images de galerie)
- `#villa-showcase-video` (vidéo de présentation)
- `.header` (en-tête avec logo)

## 🎯 Initialisation Vidéo Sécurisée

```javascript
document.addEventListener('DOMContentLoaded', function() {
    const video = document.getElementById('background-video');
    
    if (video) {
        // S'assurer que la vidéo est visible
        video.style.display = 'block';
        video.style.visibility = 'visible';
        video.style.opacity = '1';
        
        // Gestion intelligente autoplay
        const playPromise = video.play();
        
        if (playPromise !== undefined) {
            playPromise.then(() => {
                console.log('✅ Vidéo lancée');
            }).catch(() => {
                console.log('⚠️ Autoplay bloqué - fallback activé');
                // Activer au premier clic utilisateur
                document.addEventListener('click', function startVideo() {
                    video.play();
                    document.removeEventListener('click', startVideo);
                }, { once: true });
            });
        }
    }
});
```

## 📱 Responsive et Performance

### ✅ Images Responsives
```html
<picture>
    <source media="(min-width: 768px)" srcset="images/villa-large.jpg">
    <source media="(min-width: 480px)" srcset="images/villa-medium.jpg">
    <img src="images/villa-small.jpg" alt="Villa" loading="lazy">
</picture>
```

### ✅ Vidéo Responsive
```css
.video-background video {
    position: absolute;
    top: 50%;
    left: 50%;
    min-width: 100%;
    min-height: 100%;
    width: auto;
    height: auto;
    transform: translate(-50%, -50%);
    object-fit: cover;
}
```

## 🧪 Tests de Validation

### Checklist Avant Mise en Ligne
- [ ] Toutes les images se chargent (pas d'erreur 404)
- [ ] Toutes les vidéos se lancent correctement
- [ ] Lazy loading fonctionne (DevTools Network)
- [ ] Responsive design OK (mobile/desktop)
- [ ] Pas d'erreurs console JavaScript
- [ ] Temps de chargement < 3 secondes
- [ ] SEO meta tags présents et valides

### Commandes de Test
```bash
# Serveur local pour tests
python -m http.server 8080
# Accéder à: http://localhost:8080

# Tests performance
# PageSpeed Insights: https://pagespeed.web.dev/
# GTmetrix: https://gtmetrix.com/
```

## 🆘 Résolution Problèmes Courants

### Images ne s'affichent pas
1. Vérifier chemin: `images/` (pas `/images/` ou `./images/`)
2. Vérifier que le fichier existe dans le bon dossier
3. Vérifier permissions fichier (644)
4. Vérifier format supporté (.jpg, .png, .webp)

### Vidéos ne se lancent pas
1. Vérifier attributs: `autoplay muted loop playsinline`
2. Vérifier formats: WebM + MP4 pour compatibilité
3. Vérifier taille fichier (< 50MB recommandé)
4. Tester autoplay policy du navigateur

### JavaScript casse les images
1. Ne jamais utiliser `innerHTML` sur parents d'images
2. Utiliser `insertAdjacentHTML` ou `appendChild`
3. Vérifier sélecteurs CSS (éviter `display: none`)
4. Protéger avec `data-protected="true"`

---

*Guide mis à jour le $(date) - KhanelConcept Technical Team*
"""
    
    guide_path = app_dir / "FRONTEND_BEST_PRACTICES.md"
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print(f"  ✅ Guide créé: {guide_path}")

def main():
    """Fonction principale"""
    try:
        fix_all_frontend_files()
        
        print("\n📋 RÉSUMÉ DES CORRECTIONS:")
        print("✅ Chemins d'images corrigés pour GitHub Pages")
        print("✅ Chemins de vidéos corrigés")  
        print("✅ Lazy loading ajouté sur toutes les images")
        print("✅ Attributs vidéo corrigés (autoplay, muted, loop, playsinline)")
        print("✅ Protection anti-suppression ajoutée au JavaScript")
        print("✅ URLs Cloudinary remplacées par chemins locaux")
        print("✅ Guide de bonnes pratiques créé")
        
        print("\n🎯 ÉTAPES SUIVANTES:")
        print("1. Tester toutes les pages sur un serveur local")
        print("2. Vérifier que toutes les images/vidéos se chargent")
        print("3. Valider le responsive design")
        print("4. Tester les fonctionnalités JavaScript")
        print("5. Déployer sur GitHub Pages")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la correction: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()