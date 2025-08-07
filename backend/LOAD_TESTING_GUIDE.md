# 🚀 Guide de Test de Charge - KhanelConcept API

## 📋 Vue d'ensemble

Ce guide vous permet de tester la performance de votre API KhanelConcept avec **100 utilisateurs simultanés** effectuant des opérations réalistes.

### 🎯 Scénarios testés
- **Authentification** admin/membre  
- **Recherche de villas** avec filtres
- **Création de réservations**
- **Consultation des statistiques**

---

## ⚡ Démarrage Rapide

### 1️⃣ Vérification préalable
```bash
# L'API doit être lancée sur le port 8001
curl http://localhost:8001/api/health

# Si pas lancée:
cd /app/backend
uvicorn server:app --host 0.0.0.0 --port 8001
```

### 2️⃣ Lancement du test
```bash
cd /app/backend
./run_load_tests.sh
```

**Menu interactif :**
- `1` : Locust (interface web)
- `2` : k6 (ligne de commande)  
- `3` : Les deux
- `4` : Test rapide 30s

---

## 🐍 Option 1: Locust (Recommandé)

### Installation
```bash
pip install locust
```

### Lancement manuel
```bash
cd /app/backend
locust -f load_test_locust.py --host=http://localhost:8001
```

### Interface Web
- **URL:** http://localhost:8089
- **Configuration recommandée:**
  - Utilisateurs: `100`
  - Spawn rate: `10` utilisateurs/seconde
  - Host: `http://localhost:8001`

### ✅ Avantages Locust
- Interface web intuitive
- Graphiques en temps réel
- Rapports HTML détaillés
- Contrôle interactif du test

---

## ⚡ Option 2: k6 (Performance)

### Installation Linux
```bash
curl https://github.com/grafana/k6/releases/download/v0.47.0/k6-v0.47.0-linux-amd64.tar.gz -L | tar xvz --strip-components 1
chmod +x k6
```

### Installation macOS
```bash
brew install k6
```

### Lancement
```bash
cd /app/backend
./k6 run --vus 100 --duration 300s load_test_k6.js
```

### ✅ Avantages k6
- Performance optimale
- Métriques détaillées
- Seuils de performance configurés
- Intégration CI/CD facile

---

## 📊 Métriques Surveillées

### 🎯 Objectifs de Performance

| Métrique | Objectif | Critique |
|----------|----------|----------|
| **Taux de réussite** | > 95% | < 90% |
| **Temps de réponse P95** | < 2000ms | > 3000ms |
| **Taux d'erreur** | < 5% | > 10% |
| **RPS soutenu** | > 30 req/s | < 15 req/s |

### 📈 Métriques par Endpoint

#### GET /api/health
- **Objectif:** < 100ms, 100% succès
- **Criticité:** Critique pour monitoring

#### POST /api/villas/search  
- **Objectif:** < 300ms, 95% succès
- **Criticité:** Haute (fonctionnalité clé)

#### POST /api/reservations
- **Objectif:** < 500ms, 90% succès  
- **Criticité:** Critique (revenue)

#### POST /api/admin/login
- **Objectif:** < 200ms, 98% succès
- **Criticité:** Haute (sécurité)

---

## 🔧 Résolution des Problèmes

### ❌ Taux d'erreur élevé (> 10%)

**Causes possibles:**
- Surcharge CPU/RAM du serveur
- Connexions MongoDB insuffisantes
- Rate limiting trop restrictif
- Validation des données trop stricte

**Solutions:**
```bash
# Vérifier les ressources système
htop
df -h

# Augmenter les connexions MongoDB
# Dans server.py: maxPoolSize=50

# Ajuster le rate limiting  
# Dans SecurityMiddleware: limite à 200 req/min
```

### ⏱️ Latence élevée (P95 > 2000ms)

**Causes possibles:**
- Requêtes MongoDB lentes
- Absence d'index sur les recherches
- Sérialisation JSON lourde
- Manque de cache

**Solutions:**
```bash
# Ajouter des index MongoDB
mongo> db.villas.createIndex({"location": 1, "guests": 1})

# Implémenter un cache Redis
pip install redis
```

### 🔒 Échecs d'authentification

**Causes possibles:**  
- Hash bcrypt trop lent
- Rate limiting sur les logins
- Base de données surchargée

**Solutions:**
```bash
# Réduire les rounds bcrypt (production: 12, test: 4)
# Ajuster failed_login_attempts reset time
```

---

## 📋 Scénarios de Test Avancés

### Test de Montée en Charge
```bash
# k6 avec montée progressive
./k6 run --stage 30s:20 --stage 60s:50 --stage 120s:100 load_test_k6.js
```

### Test d'Endurance (30 minutes)
```bash
./k6 run --vus 50 --duration 1800s load_test_k6.js  
```

### Test de Stress (dépassement capacité)
```bash
./k6 run --vus 200 --duration 180s load_test_k6.js
```

### Test de Pic (spike testing)  
```bash
./k6 run --stage 10s:10 --stage 10s:100 --stage 10s:10 load_test_k6.js
```

---

## 📊 Analyse des Résultats

### Script d'analyse automatique
```bash
cd /app/backend
python performance_analysis.py

# Avec fichier de résultats k6
python performance_analysis.py results.json
```

### Métriques Locust
- **Interface web:** Onglet "Statistics", "Charts", "Failures"
- **Rapport HTML:** `load_test_report.html` (généré automatiquement)

### Métriques k6
```
✅ Métriques clés à surveiller:
- http_req_duration: temps de réponse
- http_req_failed: taux d'échec  
- login_success_rate: succès connexions
- search_success_rate: succès recherches
- reservation_success_rate: succès réservations
```

---

## 🚀 Optimisations Recommandées

### 🗃️ Cache et Base de Données
```python
# Cache Redis pour villas populaires
import redis
cache = redis.Redis()

@app.get("/api/villas")
async def get_villas():
    cached = cache.get("villas:all")
    if cached:
        return json.loads(cached)
    # ... requête DB et cache.setex("villas:all", 300, result)
```

### 📊 Index MongoDB
```javascript
// Index pour les recherches de villas
db.villas.createIndex({"location": 1, "guests": 1, "category": 1})
db.villas.createIndex({"price": 1})

// Index pour les réservations
db.reservations.createIndex({"customer_email": 1, "created_at": -1})
```

### 🔄 Pool de Connexions
```python
# Configuration optimisée MongoDB
client = AsyncIOMotorClient(
    MONGO_URL,
    maxPoolSize=50,        # Plus de connexions
    serverSelectionTimeoutMS=5000,
    socketTimeoutMS=30000
)
```

### ⚡ Optimisations FastAPI
```python
# Utiliser orjson pour JSON plus rapide
from fastapi.responses import ORJSONResponse

app = FastAPI(default_response_class=ORJSONResponse)

# Compression gzip
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

---

## 📈 Benchmarks de Référence

### 🎯 Performance Attendue (Serveur Standard)

| Charge | RPS | P95 Latence | CPU | RAM |
|--------|-----|-------------|-----|-----|
| 20 users | 15 req/s | < 800ms | < 50% | < 1GB |
| 50 users | 35 req/s | < 1200ms | < 70% | < 1.5GB |  
| 100 users | 60 req/s | < 2000ms | < 85% | < 2GB |

### 🚀 Performance Optimisée (avec cache)

| Charge | RPS | P95 Latence | CPU | RAM |
|--------|-----|-------------|-----|-----|
| 20 users | 40 req/s | < 300ms | < 30% | < 1GB |
| 50 users | 85 req/s | < 500ms | < 50% | < 1.5GB |
| 100 users | 150 req/s | < 800ms | < 70% | < 2GB |

---

## 🎯 Checklist Post-Test

### ✅ Validation des Résultats
- [ ] Taux de réussite > 95%
- [ ] P95 latence < 2000ms  
- [ ] Aucune erreur 500 en masse
- [ ] CPU serveur < 85%
- [ ] RAM disponible > 500MB
- [ ] Connexions MongoDB stables

### 📋 Actions si Problèmes
- [ ] Analyser les logs d'erreur
- [ ] Identifier les endpoints lents
- [ ] Optimiser les requêtes critiques
- [ ] Ajuster la configuration serveur
- [ ] Planifier les optimisations

### 📊 Documentation
- [ ] Sauvegarder les résultats
- [ ] Documenter les configurations
- [ ] Planifier les tests réguliers
- [ ] Partager avec l'équipe

---

## 🤝 Support

**Problèmes courants :**
- **"Connection refused"** → Vérifier que l'API est lancée
- **"High error rate"** → Réduire la charge ou optimiser
- **"Locust UI inaccessible"** → Port 8089 déjà utilisé
- **"k6 command not found"** → Réinstaller k6

**Besoin d'aide ?**
1. Consultez les logs FastAPI dans le terminal
2. Vérifiez `performance_analysis.py` pour des recommandations
3. Ajustez les paramètres dans les scripts selon vos besoins

---

*Guide créé pour KhanelConcept API - Tests de charge automatisés 🚀*