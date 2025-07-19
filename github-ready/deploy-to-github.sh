#!/bin/bash

# 🚀 Script de Mise à Jour GitHub - KhanelConcept v2.0
# Ce script met à jour automatiquement votre repository GitHub

echo "🏖️ KhanelConcept - Mise à jour GitHub"
echo "======================================"

# Vérifications préalables
echo "📋 Vérification des fichiers..."

if [ ! -f "index.html" ]; then
    echo "❌ Erreur: index.html manquant"
    exit 1
fi

if [ ! -d "images" ]; then
    echo "❌ Erreur: Dossier images manquant"
    exit 1
fi

echo "✅ Tous les fichiers sont présents"

# Initialiser Git si nécessaire
if [ ! -d ".git" ]; then
    echo "🔄 Initialisation Git..."
    git init
    echo "📝 Configuration Git..."
    read -p "Votre nom d'utilisateur GitHub: " github_username
    read -p "Votre email GitHub: " github_email
    
    git config user.name "$github_username"
    git config user.email "$github_email"
    
    read -p "URL de votre repository GitHub (ex: https://github.com/username/repo.git): " repo_url
    git remote add origin "$repo_url"
fi

# Ajouter tous les fichiers
echo "📁 Ajout des fichiers..."
git add .

# Commit avec message détaillé
echo "💾 Création du commit..."
git commit -m "🚀 KhanelConcept v2.0 - Interface Avancée

✨ Nouvelles fonctionnalités:
- Interface glassmorphism moderne
- Galeries d'images interactives (12 villas)
- Système de réservation avancé avec calendriers
- Recherche style Booking.com
- Design responsive parfait
- 60+ photos haute qualité

🎯 Technologies:
- HTML5/CSS3/JavaScript ES6+
- Tailwind CSS + FontAwesome
- Flatpickr pour calendriers
- Animations GPU optimisées

📱 Compatible: Mobile, Tablette, Desktop
🚀 Prêt pour production"

# Pousser vers GitHub
echo "🚀 Publication sur GitHub..."
git branch -M main

# Première fois ou mise à jour
if git ls-remote --exit-code origin >/dev/null 2>&1; then
    echo "🔄 Mise à jour du repository existant..."
    git push origin main
else
    echo "🆕 Premier push vers GitHub..."
    git push -u origin main
fi

echo ""
echo "🎉 SUCCÈS!"
echo "========"
echo "✅ Votre site KhanelConcept v2.0 est maintenant sur GitHub"
echo ""
echo "📍 Prochaines étapes:"
echo "1. Allez dans Settings → Pages de votre repository"
echo "2. Activez GitHub Pages (source: main branch)"
echo "3. Votre site sera disponible à:"
echo "   https://votre-username.github.io/nom-du-repo"
echo ""
echo "🏖️ Profitez de votre magnifique site de villas!"