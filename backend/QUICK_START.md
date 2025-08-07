# ⚡ Démarrage Rapide - Test de Charge KhanelConcept

## 🚀 Commandes Prêtes à l'Emploi

### Option 1: Script Automatique (Recommandé)
```bash
cd /app/backend
./run_load_tests.sh
```

### Option 2: Locust avec Interface Web
```bash
cd /app/backend
locust -f load_test_locust.py --host=http://localhost:8001
# Ouvrir: http://localhost:8089
# Config: 100 users, 10 spawn rate
```

### Option 3: k6 Ligne de Commande
```bash
cd /app/backend
# Installation k6 (Linux)
curl https://github.com/grafana/k6/releases/download/v0.47.0/k6-v0.47.0-linux-amd64.tar.gz -L | tar xvz --strip-components 1

# Lancement test
./k6 run --vus 100 --duration 300s load_test_k6.js
```

### Option 4: Test Rapide 30 secondes
```bash
cd /app/backend
locust -f load_test_locust.py --host=http://localhost:8001 --users=20 --spawn-rate=5 --run-time=30s --headless --html=quick_report.html
```

## 📊 Résultats Attendus

### ✅ Performance Acceptable
- **Taux de réussite:** > 95%
- **Latence P95:** < 2000ms
- **RPS:** > 30 req/sec
- **Erreurs:** < 5%

### 🎯 Endpoints Testés
- `POST /api/admin/login` - Authentification admin
- `GET /api/villas` - Liste des villas  
- `POST /api/villas/search` - Recherche avec filtres
- `POST /api/reservations` - Création réservations
- `GET /api/health` - Santé de l'API
- `GET /api/stats/dashboard` - Statistiques

## 🔧 Dépannage Rapide

### Backend non accessible
```bash
# Vérifier que l'API est lancée
curl http://localhost:8001/api/health

# Si non lancée:
cd /app/backend
uvicorn server:app --host 0.0.0.0 --port 8001
```

### Erreurs de performance
```bash
# Analyser les résultats
cd /app/backend
python performance_analysis.py

# Vérifier les ressources système  
htop
free -h
```

## 📋 Checklist Avant Test

- [ ] API lancée sur port 8001
- [ ] MongoDB connecté et opérationnel
- [ ] Aucune erreur dans les logs backend
- [ ] Test rapide des endpoints OK
- [ ] Ressources système suffisantes

## 🎉 C'est Parti !

Votre API KhanelConcept est maintenant prête pour un test de charge professionnel avec 100 utilisateurs simultanés !

```bash
cd /app/backend && ./run_load_tests.sh
```