# 🚀 Instructions Rapides - Couche Pré-backend Jamstack

## 📋 Livrables Complétés

### ✅ 1. Base de données JSON
- **Fichier** : `db.json`
- **Contenu** : 50 villas, 20 prestataires, 10 événements
- **Format** : JSON optimisé pour json-server

### ✅ 2. Configuration npm
- **Fichier** : `package.json`
- **Scripts** : `npm run dev`, `npm start`, `npm run serve`
- **Port** : 3001 (configurable)

### ✅ 3. Module ES6 fetchData.js
- **Fichier** : `fetchData.js`
- **Fonctions** : `getVillas()`, `getPrestataires()`, `getEvents()`
- **Fallback** : Automatique vers db.json local

### ✅ 4. Page d'exemple
- **Fichier** : `index-example.html`
- **Démonstration** : Injection dynamique des cartes villa
- **Tests** : Filtres, cache, santé API

### ✅ 5. Documentation
- **README-JAMSTACK.md** : Guide complet
- **ARBORESCENCE_JAMSTACK.md** : Structure détaillée
- **INSTRUCTIONS_RAPIDES.md** : Ce fichier

### ✅ 6. .gitignore
- **Fichier** : `.gitignore` (mis à jour)
- **Exclusions** : node_modules, logs, cache

## 🎯 Installation & Lancement (≤ 2 minutes)

### 1. Installation
```bash
cd /app
npm install
```
**⏱️ Temps estimé : 30 secondes**

### 2. Lancement serveur
```bash
npm run dev
```
**⏱️ Temps estimé : 5 secondes**

### 3. Vérification
```bash
curl http://localhost:3001/api/health
```
**⏱️ Temps estimé : 1 seconde**

### 4. Test complet
```bash
open http://localhost:8001/index-example.html
```
**⏱️ Temps estimé : 2 secondes**

## 🔧 Exemple d'Utilisation

### Import ES6
```javascript
import { getVillas, getPrestataires, getEvents } from './fetchData.js';
```

### Récupération des villas
```javascript
// Toutes les villas
const villas = await getVillas();

// Villas par catégorie
const villasSejourj = await getVillas({ category: 'sejour' });

// Villas par localisation
const villasVauclin = await getVillas({ location: 'Vauclin' });

// Villas avec filtres multiples
const villasFiltered = await getVillas({
    category: 'sejour',
    location: 'Vauclin',
    guests: 6,
    max_price: 1000
});
```

### Intégration dans HTML
```html
<!DOCTYPE html>
<html>
<head>
    <title>KhanelConcept</title>
</head>
<body>
    <div id="villas"></div>
    
    <script type="module">
        import { getVillas } from './fetchData.js';
        
        async function loadVillas() {
            const villas = await getVillas();
            const container = document.getElementById('villas');
            
            villas.forEach(villa => {
                const card = document.createElement('div');
                card.innerHTML = `
                    <h3>${villa.name}</h3>
                    <p>${villa.location}</p>
                    <p>${villa.price}€</p>
                `;
                container.appendChild(card);
            });
        }
        
        loadVillas();
    </script>
</body>
</html>
```

## 🌐 Endpoints API Disponibles

### 📍 Développement (http://localhost:3001)
```
GET /api/villas              # Toutes les villas
GET /api/villas?category=sejour   # Villas par catégorie
GET /api/villas?location=Vauclin  # Villas par localisation
GET /api/villas?guests_gte=6      # Villas par nb invités min
GET /api/villas?price_lte=1000    # Villas par prix max

GET /api/prestataires         # Tous les prestataires
GET /api/prestataires?category=traiteur  # Prestataires par catégorie

GET /api/events              # Tous les événements
GET /api/events?category=gastronomie     # Événements par catégorie
GET /api/events?available_gte=1          # Événements disponibles

GET /api/health              # Santé API
GET /api/stats               # Statistiques système
```

### 📍 Production (GitHub Pages)
```
./db.json                    # Fichier JSON local
# Filtrage côté client automatique
```

## 🔄 Compatibilité

### ✅ Développement
- **json-server** : Port 3001
- **Hot-reload** : Modification automatique
- **CORS** : Configuré pour tous domaines

### ✅ Production
- **GitHub Pages** : Hébergement statique
- **Fallback automatique** : db.json local
- **Cache intelligent** : 5 minutes TTL

## 🎮 Page de Test

### 🔗 URL
```
http://localhost:8001/index-example.html
```

### 🧪 Fonctionnalités
- ✅ Chargement villas avec filtres
- ✅ Chargement prestataires
- ✅ Chargement événements
- ✅ Statistiques en temps réel
- ✅ Santé API
- ✅ Gestion cache
- ✅ Interface responsive

## 🚨 Dépannage

### ❌ Erreur "Module not found"
```bash
# Vérifier que fetchData.js existe
ls -la fetchData.js

# Vérifier les permissions
chmod +r fetchData.js
```

### ❌ Erreur "json-server not found"
```bash
# Réinstaller les dépendances
rm -rf node_modules
npm install
```

### ❌ Port 3001 occupé
```bash
# Trouver le processus
lsof -i :3001

# Arrêter le processus
pkill -f json-server

# Relancer
npm run dev
```

### ❌ API inaccessible
```bash
# Vérifier le serveur
curl http://localhost:3001/api/health

# Vérifier les logs
cat json-server.log
```

## 🎯 Prochaines Étapes

1. **Intégration** : Utiliser index-jamstack.html comme base
2. **Personnalisation** : Modifier db.json selon besoins
3. **Production** : Déployer sur GitHub Pages
4. **Optimisation** : Ajouter plus de filtres
5. **Extensions** : Ajouter nouvelles fonctionnalités

---

**🎉 Couche Pré-backend Jamstack terminée !**

**⏱️ Temps total d'installation : < 2 minutes**
**🚀 Prêt pour développement et production**