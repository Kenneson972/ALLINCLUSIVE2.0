# 🏖️ KhanelConcept Full-Stack

## 🚀 Application Complète

Votre site KhanelConcept est maintenant une **application full-stack complète** avec :

### 🔧 Backend FastAPI
- **API RESTful** complète pour toutes les fonctionnalités
- **Base de données MongoDB** avec collections optimisées
- **Gestion des réservations** avec validation et confirmation
- **Recherche avancée** avec filtres multiples
- **Upload et gestion d'images** pour les galeries
- **Statistiques** et tableau de bord admin

### 🎨 Frontend React
- **Interface identique** à votre version HTML améliorée
- **Galeries d'images interactives** avec navigation
- **Système de réservation avancé** avec calendriers Flatpickr
- **Design glassmorphism** et vidéo d'arrière-plan
- **Responsive design** pour tous les écrans
- **Intégration API** complète avec le backend

### 🗄️ Base de Données MongoDB
- **Collection villas** : Toutes vos villas avec galeries
- **Collection reservations** : Système de réservation complet
- **Index optimisés** pour les recherches rapides

## 🌐 URLs et Endpoints

### Frontend React
- **URL** : http://localhost:3000
- **Interface utilisateur** complète

### Backend FastAPI
- **URL** : http://localhost:8001
- **Documentation API** : http://localhost:8001/docs
- **Endpoints principaux** :
  - `GET /api/villas` - Liste des villas
  - `POST /api/villas/search` - Recherche avec filtres
  - `POST /api/reservations` - Créer une réservation
  - `GET /api/reservations/{id}` - Détails réservation
  - `GET /api/stats/dashboard` - Statistiques admin

## 🎯 Fonctionnalités Conservées

Toutes les améliorations de votre version HTML sont présentes :

✅ **Photos des galeries** - Toutes les images s'affichent parfaitement
✅ **Système de réservation avancé** - Calendriers interactifs et calculs automatiques
✅ **Galeries d'images** - Navigation, zoom et miniatures
✅ **Design glassmorphism** - Effets visuels et vidéo d'arrière-plan
✅ **Responsive design** - Mobile, tablette, desktop
✅ **Recherche et filtres** - Destination, dates, voyageurs, catégories

## 🔗 Architecture Technique

### Communication Frontend ↔ Backend
```
React App (Port 3000) ↔ FastAPI (Port 8001) ↔ MongoDB
```

### Gestion des Images
- **Serveur statique** : FastAPI sert les images depuis `/images`
- **Galeries complètes** : Chaque villa a 3-7 images haute qualité
- **Fallbacks** : Icônes de secours pour images manquantes

### API RESTful
- **Endpoints CRUD** complets pour villas et réservations
- **Validation Pydantic** pour tous les modèles
- **Gestion d'erreurs** avec messages informatifs
- **Logs détaillés** pour debugging

## 🚀 Démarrage

Les services sont configurés avec Supervisor :

```bash
# Démarrer tous les services
sudo supervisorctl start all

# Vérifier le statut
sudo supervisorctl status

# Redémarrer si nécessaire
sudo supervisorctl restart frontend
sudo supervisorctl restart backend
```

## 📊 Données Initiales

Le backend se charge automatiquement avec **4 villas principales** :
1. Villa F3 Petit Macabou (850€/nuit)
2. Villa F5 Ste Anne (1300€/nuit) 
3. Villa F3 Baccha (1350€/nuit)
4. Studio Cocooning Lamentin (290€/nuit)

## 🎉 Résultat Final

Vous avez maintenant une **plateforme de réservation full-stack moderne** avec :

- **Interface utilisateur identique** à votre version améliorée
- **Backend professionnel** avec APIs et base de données
- **Fonctionnalités avancées** : réservations, galeries, recherche
- **Architecture scalable** pour futures extensions
- **Code maintenable** et bien structuré

L'application est **production-ready** et peut être facilement déployée sur des services cloud !