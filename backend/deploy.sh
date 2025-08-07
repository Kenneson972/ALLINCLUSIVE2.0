#!/bin/bash
# Script de déploiement KhanelConcept API
# Compatible Railway et Heroku

set -e

echo "🚀 Déploiement KhanelConcept API"
echo "================================="

# Vérifications préliminaires
echo "🔍 Vérifications préliminaires..."

if [ ! -f ".env.production" ]; then
    echo "❌ Fichier .env.production manquant"
    echo "Copiez .env.production.template et configurez les variables"
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo "❌ Fichier requirements.txt manquant"
    exit 1
fi

echo "✅ Fichiers de configuration présents"

# Choix de la plateforme
echo ""
echo "📦 Choisissez votre plateforme de déploiement:"
echo "1) Railway (Recommandé)"
echo "2) Heroku"
echo "3) Docker local"

read -p "Votre choix (1-3): " choice

case $choice in
    1)
        echo "🚀 Déploiement sur Railway..."
        
        # Vérifier Railway CLI
        if ! command -v railway &> /dev/null; then
            echo "📦 Installation de Railway CLI..."
            npm install -g @railway/cli
        fi
        
        # Configuration Railway
        echo "🔧 Configuration Railway..."
        railway login
        
        # Créer le projet si nécessaire
        if [ ! -f "railway.json" ]; then
            railway init
        fi
        
        # Déployer
        echo "🚀 Déploiement en cours..."
        railway up
        
        echo "✅ Déploiement Railway terminé!"
        echo "🌐 URL: $(railway domain)"
        ;;
        
    2)
        echo "🚀 Déploiement sur Heroku..."
        
        # Vérifier Heroku CLI
        if ! command -v heroku &> /dev/null; then
            echo "📦 Installation de Heroku CLI..."
            curl https://cli-assets.heroku.com/install.sh | sh
        fi
        
        # Login et création
        heroku login
        
        if [ ! -f "Procfile" ]; then
            echo "web: uvicorn server:app --host 0.0.0.0 --port \$PORT" > Procfile
        fi
        
        # Créer l'app si nécessaire
        read -p "Nom de l'application Heroku: " app_name
        heroku create $app_name
        
        # Configuration variables d'environnement
        echo "🔧 Configuration des variables d'environnement..."
        heroku config:set ENVIRONMENT=production
        heroku config:set DEBUG=false
        
        # Déployer
        git add .
        git commit -m "Deploy to Heroku" || true
        git push heroku main
        
        echo "✅ Déploiement Heroku terminé!"
        echo "🌐 URL: https://$app_name.herokuapp.com"
        ;;
        
    3)
        echo "🐳 Build Docker local..."
        
        # Créer Dockerfile si nécessaire
        if [ ! -f "Dockerfile" ]; then
            cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
EOF
        fi
        
        # Build et run
        docker build -t khanelconcept-api .
        echo "✅ Image Docker créée: khanelconcept-api"
        echo "🚀 Pour lancer: docker run -p 8000:8000 --env-file .env.production khanelconcept-api"
        ;;
        
    *)
        echo "❌ Choix invalide"
        exit 1
        ;;
esac

echo ""
echo "🎉 Déploiement terminé avec succès!"
echo ""
echo "📋 Étapes post-déploiement:"
echo "1. Vérifier les logs d'application"
echo "2. Tester les endpoints critiques"
echo "3. Configurer le monitoring"
echo "4. Mettre en place les sauvegardes"

# Tests post-déploiement
echo ""
read -p "Lancer les tests post-déploiement ? (y/N): " test_choice

if [[ $test_choice =~ ^[Yy]$ ]]; then
    echo "🧪 Tests post-déploiement..."
    
    # Test de base
    if command -v curl &> /dev/null; then
        echo "Testing health endpoint..."
        curl -f http://localhost:8000/api/health || echo "⚠️ Health check failed"
        curl -f http://localhost:8000/docs || echo "⚠️ Swagger docs not accessible"
    fi
    
    echo "✅ Tests terminés"
fi

echo ""
echo "📚 Documentation disponible sur: /docs"
echo "🔒 Pensez à configurer le monitoring et les alertes!"