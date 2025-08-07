#!/bin/bash
# Script pour lancer les tests de charge KhanelConcept API
# Supporte Locust (Python) et k6 (JavaScript)

set -e

echo "🚀 Tests de Charge KhanelConcept API"
echo "===================================="

# Configuration
BACKEND_URL="http://localhost:8001"
USERS=100
DURATION="300s"  # 5 minutes
SPAWN_RATE=10

# Vérifier que l'API est accessible
echo "🔍 Vérification de l'API..."
if ! curl -s "$BACKEND_URL/api/health" > /dev/null; then
    echo "❌ API non accessible sur $BACKEND_URL"
    echo "💡 Assurez-vous que le backend FastAPI est lancé:"
    echo "   cd /app/backend && uvicorn server:app --host 0.0.0.0 --port 8001"
    exit 1
fi

echo "✅ API accessible"
echo ""

# Menu de choix
echo "📊 Choisissez votre outil de test de charge:"
echo "1) Locust (Python) - Interface web, rapports HTML"
echo "2) k6 (JavaScript) - Performance optimale, métriques détaillées"
echo "3) Les deux (séquentiel)"
echo "4) Test rapide (30s avec Locust)"

read -p "Votre choix (1-4): " choice

case $choice in
    1)
        echo "🐍 Lancement de Locust..."
        
        # Installer Locust si nécessaire
        if ! command -v locust &> /dev/null; then
            echo "📦 Installation de Locust..."
            pip install locust
        fi
        
        # Lancer Locust avec interface web
        echo "🌐 Interface web disponible sur: http://localhost:8089"
        echo "⚙️  Configuration recommandée:"
        echo "   - Utilisateurs: $USERS"
        echo "   - Spawn rate: $SPAWN_RATE/sec"
        echo "   - Host: $BACKEND_URL"
        echo ""
        echo "🚀 Lancement de Locust (Ctrl+C pour arrêter)..."
        
        locust -f load_test_locust.py \
               --host=$BACKEND_URL \
               --web-port=8089
        ;;
        
    2)
        echo "⚡ Lancement de k6..."
        
        # Installer k6 si nécessaire
        if ! command -v k6 &> /dev/null; then
            echo "📦 Installation de k6..."
            if [[ "$OSTYPE" == "linux-gnu"* ]]; then
                curl https://github.com/grafana/k6/releases/download/v0.47.0/k6-v0.47.0-linux-amd64.tar.gz -L | tar xvz --strip-components 1
                chmod +x k6
            elif [[ "$OSTYPE" == "darwin"* ]]; then
                brew install k6
            else
                echo "❌ Installation automatique k6 non supportée pour votre OS"
                echo "💡 Installez k6 manuellement: https://k6.io/docs/get-started/installation/"
                exit 1
            fi
        fi
        
        # Configurer k6 pour le test
        echo "⚙️  Configuration k6:"
        echo "   - Utilisateurs: $USERS simultanés"
        echo "   - Durée: $DURATION"
        echo "   - URL: $BACKEND_URL"
        echo ""
        
        # Lancer k6
        ./k6 run --vus $USERS --duration $DURATION load_test_k6.js
        ;;
        
    3)
        echo "🔄 Lancement des deux outils (séquentiel)..."
        
        # Test k6 d'abord (plus rapide)
        echo "⚡ Phase 1: k6 (5 minutes)"
        if command -v k6 &> /dev/null; then
            ./k6 run --vus $USERS --duration $DURATION load_test_k6.js
        else
            echo "⚠️  k6 non installé, ignoré"
        fi
        
        echo ""
        echo "🐍 Phase 2: Locust (interface web)"
        echo "💡 Fermez Locust quand vous avez terminé (Ctrl+C)"
        read -p "Appuyez sur Entrée pour continuer..."
        
        if command -v locust &> /dev/null; then
            locust -f load_test_locust.py \
                   --host=$BACKEND_URL \
                   --web-port=8089
        else
            echo "⚠️  Locust non installé, ignoré"
        fi
        ;;
        
    4)
        echo "⚡ Test rapide (30 secondes)..."
        
        # Test rapide avec Locust
        if command -v locust &> /dev/null; then
            echo "🐍 Locust - Test automatique 30s"
            locust -f load_test_locust.py \
                   --host=$BACKEND_URL \
                   --users=20 \
                   --spawn-rate=5 \
                   --run-time=30s \
                   --headless \
                   --html=quick_test_report.html
            
            echo "✅ Rapport généré: quick_test_report.html"
        else
            echo "❌ Locust non installé"
            echo "💡 Installation: pip install locust"
            exit 1
        fi
        ;;
        
    *)
        echo "❌ Choix invalide"
        exit 1
        ;;
esac

echo ""
echo "🏁 Test de charge terminé!"
echo ""
echo "📋 Métriques à analyser:"
echo "   - Taux de réussite: > 90% (acceptable)"  
echo "   - Latence P95: < 2000ms (acceptable)"
echo "   - Taux d'erreur: < 10% (acceptable)"
echo "   - RPS: Requêtes par seconde soutenues"
echo ""
echo "📊 Fichiers générés:"
if [ -f "quick_test_report.html" ]; then
    echo "   - quick_test_report.html (rapport Locust)"
fi
echo "   - Logs dans le terminal ci-dessus"
echo ""
echo "🔧 Si vous constatez des problèmes:"
echo "   1. Vérifiez les logs du backend FastAPI"
echo "   2. Surveillez l'utilisation CPU/RAM"
echo "   3. Ajustez la configuration MongoDB"
echo "   4. Optimisez les requêtes lentes"

# Afficher un résumé des performances système
echo ""
echo "📈 Performance système actuelle:"
echo "CPU: $(top -l 1 -s 0 | grep "CPU usage" || echo "N/A")"
echo "RAM: $(free -h 2>/dev/null | grep "Mem:" || echo "N/A")"