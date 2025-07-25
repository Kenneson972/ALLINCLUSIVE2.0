# 🚀 KhanelConcept - Couche Pré-backend Jamstack

## 📋 Vue d'ensemble

Cette couche pré-backend permet à KhanelConcept de fonctionner en mode **statique** (compatible GitHub Pages) tout en simulant un backend via **json-server** pour le développement local.

## 🎯 Objectif

Créer une solution **Jamstack** qui :
- ✅ Fonctionne en **développement** avec json-server (port 3001)
- ✅ Fonctionne en **production** avec fichiers statiques (GitHub Pages)
- ✅ Gère automatiquement le **fallback** entre les deux modes
- ✅ Maintient la compatibilité avec l'existant

## 🏗️ Architecture

```
/app/
├── package.json          # Configuration npm avec scripts json-server
├── db.json              # Base de données JSON (50 villas, 20 prestataires, 10 événements)
├── routes.json          # Configuration des routes API
├── fetchData.js         # Module ES6 pour récupération des données
├── index-example.html   # Page de test et démo
└── README-JAMSTACK.md   # Cette documentation
```

## 📦 Installation

### 1. Installation des dépendances

```bash
# Installation rapide (< 2 minutes)
npm install

# Ou avec yarn
yarn install
```

### 2. Lancement du serveur de développement

```bash
# Lancement json-server
npm run dev

# Ou
npm start

# Serveur accessible sur http://localhost:3001
```

## 🔧 Configuration

### Scripts npm disponibles

```json
{
  "dev": "json-server --watch db.json --port 3001 --routes routes.json",
  "start": "json-server --watch db.json --port 3001 --routes routes.json",
  "build": "echo 'Build static files'",
  "serve": "json-server --watch db.json --port 3001 --routes routes.json --host 0.0.0.0"
}
```

### Routes API configurées

```json
{
  "/api/villas": "/villas",
  "/api/villas/:id": "/villas/:id",
  "/api/villas/search": "/villas",
  "/api/prestataires": "/prestataires",
  "/api/events": "/events",
  "/api/health": "/health",
  "/api/stats": "/stats"
}
```

## 📊 Données disponibles

### 🏖️ Villas (21 villas)
- **Catégories** : sejour, fete, speciale
- **Localisations** : Vauclin, Lamentin, Ste Anne, Fort-de-France, etc.
- **Prix** : 450€ à 1800€
- **Capacité** : 2 à 30 personnes

### 🤝 Prestataires (20 prestataires)
- **Catégories** : traiteur, animation, decoration, transport, etc.
- **Services** : Traiteur, DJ, Photographe, Transport VIP, etc.
- **Prix** : 15€ à 1200€

### 🎉 Événements (10 événements)
- **Catégories** : gastronomie, excursion, atelier, soiree, etc.
- **Dates** : Mars à Mai 2025
- **Prix** : 15€ à 120€

## 🔄 Utilisation du module fetchData.js

### Import ES6

```javascript
import { getVillas, getPrestataires, getEvents } from './fetchData.js';
```

### Exemples d'utilisation

```javascript
// Récupérer toutes les villas
const villas = await getVillas();

// Filtrer les villas par catégorie
const villasSejourj = await getVillas({ category: 'sejour' });

// Filtrer par localisation
const villasVauclin = await getVillas({ location: 'Vauclin' });

// Filtrer par prix maximum
const villasAbordables = await getVillas({ max_price: 1000 });

// Récupérer les prestataires
const prestataires = await getPrestataires();

// Récupérer les événements disponibles
const events = await getEvents({ available: true });

// Vérifier la santé de l'API
const health = await getHealth();

// Obtenir les statistiques
const stats = await getStats();
```

### Gestion automatique des environnements

```javascript
// Le module détecte automatiquement l'environnement
const config = getApiConfig();
console.log('Environnement:', config.current);
// development: utilise json-server
// production: utilise db.json local
```

## 🔄 Fallback automatique

Le module **fetchData.js** gère automatiquement :

1. **Développement** (`localhost`) → json-server sur port 3001
2. **Production** (GitHub Pages) → fichier db.json local
3. **Fallback** → Si json-server échoue, utilise db.json local

## 🎮 Page de test

### Accès à la démo

```bash
# Ouvrir dans le navigateur
open http://localhost:8001/index-example.html

# Ou directement
open ./index-example.html
```

### Fonctionnalités de test

- ✅ **Chargement villas** avec filtres (catégorie, localisation, prix, invités)
- ✅ **Chargement prestataires** par catégorie
- ✅ **Chargement événements** disponibles
- ✅ **Statistiques** du système
- ✅ **Santé API** et diagnostic
- ✅ **Gestion du cache** (5 minutes TTL)

## 🌍 Intégration dans index.html

### Exemple d'intégration

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>KhanelConcept</title>
</head>
<body>
    <div id="villas-container"></div>
    
    <script type="module">
        import { getVillas } from './fetchData.js';
        
        // Chargement dynamique des villas
        async function loadVillas() {
            try {
                const villas = await getVillas();
                const container = document.getElementById('villas-container');
                
                villas.forEach(villa => {
                    const card = document.createElement('div');
                    card.className = 'villa-card';
                    card.innerHTML = `
                        <h3>${villa.name}</h3>
                        <p>${villa.location}</p>
                        <p>${villa.price}€</p>
                        <p>${villa.guests_detail}</p>
                    `;
                    container.appendChild(card);
                });
                
            } catch (error) {
                console.error('Erreur chargement villas:', error);
            }
        }
        
        // Chargement au démarrage
        document.addEventListener('DOMContentLoaded', loadVillas);
    </script>
</body>
</html>
```

## 🔍 Debugging

### Vérification de l'environnement

```javascript
import { getApiConfig } from './fetchData.js';

const config = getApiConfig();
console.log('Configuration API:', config);
```

### Vérification de la santé

```javascript
import { getHealth } from './fetchData.js';

const health = await getHealth();
console.log('Santé API:', health);
```

### Gestion des erreurs

```javascript
try {
    const villas = await getVillas();
} catch (error) {
    console.error('Erreur API:', error.message);
    // Fallback sur données statiques si nécessaire
}
```

## 📈 Performance

- **Cache** : 5 minutes TTL pour éviter les requêtes répétées
- **Fallback** : Basculement automatique en cas d'erreur
- **Compression** : Données JSON optimisées
- **Lazy Loading** : Chargement à la demande

## 🚀 Déploiement

### Développement local

```bash
# Terminal 1: Backend json-server
npm run dev

# Terminal 2: Frontend (si existant)
# sudo supervisorctl restart all
```

### Production GitHub Pages

```bash
# Les fichiers statiques sont déjà prêts
# db.json, fetchData.js, routes.json
# Aucune configuration supplémentaire nécessaire
```

## 🔒 Sécurité

- **CORS** : Configuré pour tous les domaines
- **Validation** : Validation des données côté client
- **Fallback** : Pas de données sensibles exposées
- **Cache** : Expiration automatique

## 🎯 Avantages

- ✅ **Développement rapide** avec json-server
- ✅ **Production statique** pour GitHub Pages
- ✅ **Fallback automatique** robuste
- ✅ **Cache intelligent** pour performance
- ✅ **ES6 modules** modernes
- ✅ **TypeScript ready** (types disponibles)

## 🔧 Maintenance

### Mise à jour des données

```bash
# Éditer le fichier db.json
nano db.json

# Redémarrer json-server
npm run dev
```

### Ajout de nouveaux endpoints

```bash
# Éditer routes.json
nano routes.json

# Ajouter les fonctions dans fetchData.js
```

## 📞 Support

Pour toute question concernant la couche Jamstack :

1. **Vérifier** la page de test : `index-example.html`
2. **Consulter** les logs de console
3. **Tester** l'API santé : `getHealth()`
4. **Vider** le cache : `clearCache()`

---

**🎉 Installation terminée en moins de 2 minutes !**

La couche pré-backend Jamstack est maintenant opérationnelle et prête pour le développement et la production.