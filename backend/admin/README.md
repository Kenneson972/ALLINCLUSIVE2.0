# KhanelConcept - Interface d'Administration

## 🚀 APERÇU

Interface d'administration complète et professionnelle pour gérer les villas de KhanelConcept. Système entièrement statique compatible GitHub Pages avec stockage localStorage.

## 📋 FONCTIONNALITÉS PRINCIPALES

### 🏠 **Gestion des Villas**
- ✅ Liste complète avec photos et informations
- ✅ Ajout de nouvelles villas (formulaire complet)
- ✅ Édition de villas existantes
- ✅ Duplication de villas
- ✅ Suppression avec confirmation
- ✅ Recherche et filtres (nom, statut, prix)
- ✅ Import/Export de données

### 📊 **Dashboard Analytique**
- ✅ Statistiques temps réel (villas totales, actives, prix moyen)
- ✅ Graphiques interactifs (répartition prix, statuts)
- ✅ Activité récente
- ✅ Vue d'ensemble performance

### 🖼️ **Gestion d'Images**
- ✅ Upload par glisser-déposer
- ✅ Compression automatique
- ✅ Galerie organisée
- ✅ Prévisualisation et métadonnées
- ✅ Stockage base64 pour GitHub Pages

### ⚙️ **Paramètres & Export**
- ✅ Configuration générale du site
- ✅ Export/Import JSON complet
- ✅ Export CSV pour analyse
- ✅ Génération données website
- ✅ Sauvegarde automatique

### 🔒 **Sécurité**
- ✅ Authentification par mot de passe
- ✅ Protection contre brute force
- ✅ Gestion session sécurisée
- ✅ Auto-logout inactivité

## 🔧 INSTALLATION

### 1. Structure des fichiers
```
/admin/
├── admin.html          # Interface principale
├── login.html          # Page de connexion
├── css/
│   └── admin-style.css # Styles complets
├── js/
│   ├── admin-main.js   # Logique principale
│   ├── villa-manager.js # Gestion CRUD villas
│   ├── image-handler.js # Upload et galerie
│   └── data-export.js  # Import/Export
```

### 2. Intégration au site principal
Lien discret ajouté dans `index.html` :
```html
<a href="/admin/login.html" class="admin-link" style="display:none">⚙️</a>
```

### 3. Accès administrateur
1. Aller sur `/admin/login.html`
2. Mot de passe : `khanel-admin-2025`
3. Accès automatique à l'interface admin

## 📱 UTILISATION

### **Première Connexion**
1. Accéder à `votre-site.com/admin/login.html`
2. Saisir le mot de passe admin
3. Dashboard s'ouvre automatiquement

### **Gestion des Villas**
```javascript
// Ajouter une villa
1. Cliquer "Ajouter Villa"
2. Remplir le formulaire complet
3. Sélectionner équipements
4. Sauvegarder

// Modifier une villa
1. Cliquer "Éditer" sur une villa
2. Modifier les champs nécessaires
3. Sauvegarder les modifications

// Importer des villas
1. Section Paramètres
2. "Importer données" 
3. Sélectionner fichier JSON
```

### **Upload d'Images**
```javascript
// Upload simple
1. Section "Galerie Images"
2. Glisser-déposer les images
3. Compression automatique
4. Images stockées en base64

// Utilisation dans villas
- Les images uploadées apparaissent
- Copier l'URL pour les villas
- Réorganisation par drag&drop
```

## 🔐 SÉCURITÉ

### **Mot de passe Admin**
```javascript
// À changer en production dans login.html
this.adminPassword = "khanel-admin-2025";
```

### **Protection Brute Force**
- 3 tentatives maximum
- Blocage 5 minutes après échec
- Nettoyage automatique des tentatives

### **Session Management**
```javascript
// Auto-logout après 30 min d'inactivité
// Session stockée dans sessionStorage
// Vérification authentification sur chaque page
```

## 💾 DONNÉES

### **Stockage localStorage**
```javascript
// Données stockées localement
admin_villas     // Liste des villas
admin_settings   // Paramètres du site
admin_images     // Images uploadées
admin_reservations // Réservations futures
```

### **Export/Import**
```javascript
// Export complet (JSON)
{
  "villas": [...],
  "settings": {...},
  "images": [...],
  "metadata": {...}
}

// Export CSV (analyse)
ID,Nom,Prix,Capacité,Statut...

// Export website (integration)
const villasData = [...]; // Pour site principal
```

## 🎨 PERSONNALISATION

### **Couleurs du thème**
```css
:root {
    --primary: #2563eb;    /* Bleu principal */
    --secondary: #64748b;   /* Gris secondaire */
    --success: #22c55e;     /* Vert succès */
    --danger: #ef4444;      /* Rouge erreur */
    --dark: #1e293b;        /* Sombre sidebar */
}
```

### **Ajout de fonctionnalités**
```javascript
// Nouveau manager dans admin-main.js
this.customManager = new CustomManager(this);

// Nouvelle section dans admin.html
<section id="custom-section" class="content-section">
```

## 🔄 MIGRATION FUTURE API

### **Structure préparée**
```javascript
// Endpoints mockés prêts
const API_ENDPOINTS = {
  villas: 'GET /api/villas',
  create: 'POST /api/villas',
  // ...
};

// Couche d'abstraction données
class DataManager {
  async getVillas() {
    // localStorage OU API call
  }
}
```

## 🚨 MAINTENANCE

### **Sauvegarde régulière**
1. Section Paramètres
2. "Exporter toutes les données"
3. Sauvegarder le fichier JSON

### **Mise à jour données**
```javascript
// Synchroniser avec site principal
1. Exporter villas depuis admin
2. Intégrer dans villa-details.html
3. Déployer sur GitHub Pages
```

### **Monitoring**
```javascript
// Dashboard analytics
- Nombre de villas par statut
- Prix moyen évolution
- Activité récente
- Performance générale
```

## 🆘 DÉPANNAGE

### **Problèmes courants**

**Page blanche / Erreurs JS**
```bash
# Vérifier console navigateur F12
# Vérifier chemins des fichiers JS/CSS
# Vérifier localStorage disponible
```

**Données perdues**
```bash
# Export/import pour restaurer
# Vérifier localStorage quota
# Utiliser mode incognito pour tester
```

**Upload images non fonctionnel**
```bash
# Vérifier taille fichiers (max 5MB)
# Vérifier format supporté (JPG/PNG)
# Vérifier quota localStorage
```

## 📞 SUPPORT

### **Logs de débogage**
```javascript
// Console navigateur (F12)
console.log("Villa data:", app.villas);
console.log("Settings:", app.settings);
```

### **Reset complet**
```javascript
// En cas de problème majeur
localStorage.clear();
sessionStorage.clear();
location.reload();
```

---

## 🎯 PROCHAINES VERSIONS

- [ ] Intégration API backend
- [ ] Système de réservations avancé
- [ ] Multi-utilisateurs avec rôles
- [ ] Analytics avancées
- [ ] Notifications push
- [ ] Mobile app native

---

**Version**: 1.0  
**Compatible**: GitHub Pages, Navigateurs modernes  
**Développé pour**: KhanelConcept Martinique  
**Statut**: ✅ Production Ready