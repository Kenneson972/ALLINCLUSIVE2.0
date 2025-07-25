# 🌳 Arborescence du Projet - Couche Pré-backend Jamstack

## 📂 Structure Complète

```
/app/
├── 📦 CONFIGURATION JAMSTACK
│   ├── package.json              # Configuration npm avec scripts json-server
│   ├── routes.json               # Mapping des routes API (/api/* -> /*)
│   ├── db.json                   # Base de données JSON complète
│   ├── .gitignore                # Fichiers à ignorer (node_modules, etc.)
│   └── yarn.lock                 # Fichier de lock des dépendances
│
├── 📚 MODULES & LIBRAIRIES
│   ├── fetchData.js              # Module ES6 pour récupération des données
│   ├── node_modules/             # Dépendances npm (json-server, etc.)
│   └── json-server.log           # Logs du serveur json-server
│
├── 🌐 PAGES WEB
│   ├── index.html                # Page principale (version statique actuelle)
│   ├── index-jamstack.html       # Version Jamstack avec fetchData.js
│   ├── index-example.html        # Page de test et démonstration
│   ├── prestataires.html         # Page des prestataires
│   ├── billetterie.html          # Page de billetterie
│   ├── mobilier.html             # Page mobilier
│   ├── excursions.html           # Page excursions
│   ├── pmr.html                  # Page PMR
│   └── sos-depannage.html        # Page SOS dépannage
│
├── 🔐 ESPACE MEMBRE
│   ├── login.html                # Page de connexion
│   ├── register.html             # Page d'inscription
│   ├── dashboard.html            # Tableau de bord membre
│   ├── profile.html              # Profil utilisateur
│   ├── loyalty.html              # Programme fidélité
│   ├── wishlist.html             # Liste de souhaits
│   ├── wallet.html               # Portefeuille
│   ├── concierge.html            # Service conciergerie
│   ├── notifications.html        # Notifications
│   └── reset-password.html       # Réinitialisation mot de passe
│
├── 👨‍💼 ADMINISTRATION
│   ├── admin/
│   │   ├── admin.html            # Interface d'administration
│   │   ├── login.html            # Connexion admin
│   │   ├── guide.html            # Guide d'utilisation
│   │   ├── css/                  # Styles admin
│   │   │   ├── admin-style.css
│   │   │   └── components.css
│   │   └── js/                   # Scripts admin
│   │       ├── admin-main.js
│   │       ├── villa-manager.js
│   │       ├── image-handler.js
│   │       ├── data-export.js
│   │       └── sync-manager.js
│   └── README.md                 # Documentation admin
│
├── 🖼️ RESSOURCES MÉDIAS
│   ├── images/                   # Images des villas (21 dossiers)
│   │   ├── Villa_F3_Petit_Macabou/
│   │   ├── Villa_F5_Ste_Anne/
│   │   ├── Villa_F3_Baccha_Petit_Macabou/
│   │   ├── Studio_Cocooning_Lamentin/
│   │   ├── Villa_F6_Lamentin/
│   │   └── [... 16 autres dossiers]
│   └── prestataires/             # Images des prestataires (simulées)
│
├── 🔧 BACKEND & API
│   ├── backend/
│   │   ├── server.py             # Serveur FastAPI complet
│   │   ├── requirements.txt      # Dépendances Python
│   │   └── __pycache__/          # Cache Python
│   └── supervisord.conf          # Configuration Supervisor
│
├── 📄 PAGES VILLA STATIQUES
│   ├── villa-details.html        # Template de détails villa
│   ├── villa-template.html       # Template de base
│   ├── villa-f3-petit-macabou.html
│   ├── villa-f5-ste-anne.html
│   ├── villa-f3-baccha-petit-macabou.html
│   ├── studio-cocooning-lamentin.html
│   ├── villa-f6-lamentin.html
│   └── [... 16 autres pages villa]
│
├── 🛠️ SCRIPTS & UTILITAIRES
│   ├── generate_villa_pages.py   # Générateur de pages villa
│   ├── reservation.html          # Page de réservation
│   ├── test_result.md            # Résultats des tests
│   └── js/                       # Scripts JavaScript
│       ├── data-export.js
│       ├── image-handler.js
│       ├── admin-main.js
│       ├── villa-manager.js
│       └── sync-manager.js
│
└── 📚 DOCUMENTATION
    ├── README.md                 # Documentation principale
    ├── README-JAMSTACK.md        # Guide Jamstack
    ├── ARBORESCENCE_JAMSTACK.md  # Cette arborescence
    ├── AMELIORATIONS.md          # Améliorations apportées
    ├── AUTHENTIFICATION_GUIDE.md # Guide d'authentification
    ├── VILLA_PAGES_INDEX.md      # Index des pages villa
    ├── GITHUB_UPDATE.md          # Mise à jour GitHub
    └── SOLUTION_GITHUB.md        # Solution GitHub Pages
```

## 🎯 Éléments Clés Ajoutés

### 📦 Configuration Jamstack
- **package.json** : Scripts npm pour json-server
- **routes.json** : Mapping des routes API
- **db.json** : Base de données complète (50 villas, 20 prestataires, 10 événements)

### 🔧 Module Principal
- **fetchData.js** : Module ES6 avec fonctions d'API
  - `getVillas(filters)` : Récupération des villas
  - `getPrestataires(filters)` : Récupération des prestataires
  - `getEvents(filters)` : Récupération des événements
  - `getHealth()` : Vérification santé API
  - `getStats()` : Statistiques système
  - `clearCache()` : Vider le cache
  - `getApiConfig()` : Configuration API

### 🌐 Pages d'Intégration
- **index-jamstack.html** : Version complète avec fetchData.js
- **index-example.html** : Page de test et démonstration
- **index.html** : Version statique actuelle (inchangée)

## 🚀 Modes de Fonctionnement

### 🔧 Mode Développement
```bash
# Lancement json-server
npm run dev
# Serveur API : http://localhost:3001
# Routes API : /api/villas, /api/prestataires, /api/events
```

### 🌍 Mode Production (GitHub Pages)
```bash
# Utilisation directe de db.json
# Fallback automatique si json-server indisponible
# Compatible avec hébergement statique
```

## 📊 Données Disponibles

### 🏖️ Villas (21 villas)
- **Categories** : sejour (15), fete (5), speciale (1)
- **Prix** : 450€ - 1800€
- **Capacité** : 2 - 30 personnes
- **Localisations** : 8 communes de Martinique

### 🤝 Prestataires (20 prestataires)
- **Services** : Traiteur, DJ, Photographe, Transport, Spa, Chef, etc.
- **Catégories** : 12 catégories différentes
- **Prix** : 15€ - 1200€ selon service

### 🎉 Événements (10 événements)
- **Dates** : Mars - Mai 2025
- **Types** : Gastronomie, Excursions, Ateliers, Concerts
- **Capacité** : 10 - 200 personnes

## 🔄 Fallback Automatique

1. **Développement** : json-server (localhost:3001)
2. **Production** : db.json local
3. **Erreur** : Fallback vers db.json + notification

## 🎮 Page de Test

### 🔗 URL d'accès
```
http://localhost:8001/index-example.html
```

### 🧪 Fonctionnalités de test
- ✅ Chargement villas avec filtres
- ✅ Chargement prestataires
- ✅ Chargement événements
- ✅ Statistiques système
- ✅ Santé API
- ✅ Gestion cache

## 🎯 Avantages

- ✅ **Installation rapide** : < 2 minutes
- ✅ **Développement efficace** : Hot-reload avec json-server
- ✅ **Production statique** : Compatible GitHub Pages
- ✅ **Fallback robuste** : Fonctionnement garanti
- ✅ **Cache intelligent** : Performance optimisée
- ✅ **ES6 moderne** : Code maintenable
- ✅ **TypeScript ready** : Évolutif

## 📈 Performance

- **Cache** : 5 minutes TTL
- **Compression** : JSON optimisé
- **Lazy Loading** : Chargement à la demande
- **Fallback** : Basculement automatique

## 🔧 Commandes Utiles

```bash
# Installation
npm install

# Développement
npm run dev

# Test API
curl http://localhost:3001/api/health

# Arrêt serveur
pkill -f json-server

# Nettoyage
rm -rf node_modules && npm install
```

---

**🎉 Couche Pré-backend Jamstack opérationnelle !**

La structure est maintenant complète et prête pour le développement et la production.