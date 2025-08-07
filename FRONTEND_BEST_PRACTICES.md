# 🔧 Guide de Bonnes Pratiques Frontend - KhanelConcept

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
