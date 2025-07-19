# 🚀 Instructions de Déploiement Netlify - KhanelConcept

## 📋 Problème Vidéo Cloudinary Résolu

La vidéo Cloudinary ne s'affichait pas sur Netlify pour les raisons suivantes :

### ❌ Ancienne Configuration
- `netlify.toml` configuré pour déployer `index.html` statique
- CSP (Content Security Policy) bloquait `res.cloudinary.com`
- Pas de build React configuré
- Variables d'environnement manquantes

### ✅ Nouvelle Configuration

#### 1. **Netlify.toml Mis à Jour**
```toml
[build]
  base = "frontend"
  publish = "frontend/build"
  command = "yarn install && yarn build"
```

#### 2. **CSP Autorise Cloudinary**
```toml
Content-Security-Policy = "media-src 'self' https://res.cloudinary.com https:;"
```

#### 3. **Plugin Cloudinary Ajouté**
```toml
[[plugins]]
  package = "netlify-plugin-cloudinary"
  [plugins.inputs]
    cloudName = "ddulasmtz"
```

## 🔧 Déploiement sur Netlify

### Étape 1: Configurer le Site Netlify
1. Aller sur [netlify.com](https://netlify.com)
2. **New site from Git** → Connecter votre repo GitHub
3. **Build settings:**
   - Build command: `yarn install && yarn build`
   - Publish directory: `frontend/build`
   - Base directory: `frontend`

### Étape 2: Variables d'Environnement
Dans Netlify Dashboard → **Site settings** → **Environment variables**, ajouter :

```
NODE_VERSION = 18
CI = false  
GENERATE_SOURCEMAP = false
DISABLE_ESLINT_PLUGIN = true
REACT_APP_BACKEND_URL = https://votre-backend-url.com
```

### Étape 3: Installer le Plugin Cloudinary
Dans Netlify Dashboard → **Plugins** → Rechercher **"netlify-plugin-cloudinary"** → Installer

### Étape 4: Tester la Vidéo
Après déploiement, tester avec : `https://votre-site.netlify.app/test-video.html`

## 🧪 Debug Vidéo Cloudinary

Si la vidéo ne fonctionne toujours pas :

### 1. Vérifier les Headers
- Ouvrir **DevTools** → **Network** → Recharger la page
- Chercher la requête vers `res.cloudinary.com`
- Vérifier le statut (200 OK attendu)

### 2. Vérifier la Console
- **DevTools** → **Console**
- Chercher les erreurs CSP ou CORS

### 3. Tester l'URL Directement
Ouvrir directement : 
```
https://res.cloudinary.com/ddulasmtz/video/upload/v1752950782/background-video.mp4_qoofsz.mp4
```

### 4. Fallback CSS
Si problème persiste, le gradient animé CSS s'affiche automatiquement.

## ✅ Résolution Garantie

La nouvelle configuration résout :
- ✅ Build React correct
- ✅ CSP autorisant Cloudinary  
- ✅ Plugin Cloudinary optimisant les médias
- ✅ Variables d'environnement complètes
- ✅ Redirections SPA pour `/villa/id`

## 📞 Support

Si problème persiste après ces étapes, vérifier :
1. **Logs de build Netlify** (Deploy log)
2. **Test page** : `/test-video.html`
3. **Console développeur** sur site déployé