#!/usr/bin/env python3
"""
🔍 DIAGNOSTIC INSCRIPTION - Analyse du problème de connexion

Investigation approfondie du problème "compte introuvable" après inscription
"""

import requests
import json
import time
from datetime import datetime
import bcrypt

# Configuration
BACKEND_URL = "http://localhost:8001"
API_BASE = f"{BACKEND_URL}/api"

def test_password_hashing():
    """Tester le mécanisme de hachage des mots de passe"""
    print("🔍 DIAGNOSTIC: Mécanisme de hachage des mots de passe")
    
    test_password = "MonMotDePasse2025!"
    
    # Test bcrypt hashing (comme dans le backend)
    hashed = bcrypt.hashpw(test_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    print(f"   Password original: {test_password}")
    print(f"   Hash bcrypt: {hashed[:50]}...")
    
    # Test verification
    is_valid = bcrypt.checkpw(test_password.encode('utf-8'), hashed.encode('utf-8'))
    print(f"   Vérification bcrypt: {'✅ OK' if is_valid else '❌ ÉCHEC'}")
    
    return is_valid

def test_registration_and_immediate_login():
    """Test complet avec diagnostic détaillé"""
    print("\n🧪 TEST DIAGNOSTIC COMPLET")
    
    # Données de test avec email unique
    test_data = {
        "firstName": "Jean-Baptiste",
        "lastName": "Martineau",
        "email": f"jean.martineau.{int(time.time())}@martinique.com",
        "phone": "+596987654321",
        "password": "TestPassword2025!",
        "birthDate": "1990-05-20",
        "nationality": "FR",
        "acceptTerms": True
    }
    
    print(f"\n📝 ÉTAPE 1: Inscription")
    print(f"   Email: {test_data['email']}")
    print(f"   Password: {test_data['password']}")
    
    # Inscription
    try:
        reg_response = requests.post(
            f"{API_BASE}/members/register",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"   Status: {reg_response.status_code}")
        
        if reg_response.status_code == 200:
            reg_data = reg_response.json()
            member_id = reg_data.get("member", {}).get("id")
            print(f"   ✅ Inscription réussie - ID: {member_id}")
            
            # Attendre un peu pour s'assurer que les données sont persistées
            time.sleep(2)
            
            print(f"\n🔐 ÉTAPE 2: Connexion immédiate")
            
            # Tentative de connexion
            login_data = {
                "email": test_data["email"],
                "password": test_data["password"],
                "remember": False
            }
            
            login_response = requests.post(
                f"{API_BASE}/members/login",
                json=login_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            print(f"   Status: {login_response.status_code}")
            
            if login_response.status_code == 200:
                login_data_resp = login_response.json()
                print(f"   ✅ Connexion réussie")
                print(f"   Membre: {login_data_resp.get('member', {}).get('firstName')} {login_data_resp.get('member', {}).get('lastName')}")
                return True
            else:
                print(f"   ❌ Connexion échouée")
                print(f"   Erreur: {login_response.text}")
                
                # Diagnostic supplémentaire - vérifier si le membre existe
                print(f"\n🔍 DIAGNOSTIC: Vérification existence membre")
                
                profile_response = requests.get(f"{API_BASE}/members/profile/{member_id}")
                if profile_response.status_code == 200:
                    profile = profile_response.json()
                    print(f"   ✅ Membre existe en base")
                    print(f"   Email en base: {profile.get('email')}")
                    print(f"   Email login: {login_data['email']}")
                    print(f"   Match email: {'✅' if profile.get('email') == login_data['email'] else '❌'}")
                else:
                    print(f"   ❌ Membre introuvable en base")
                
                return False
        else:
            print(f"   ❌ Inscription échouée: {reg_response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_existing_member_login():
    """Tester la connexion avec un membre existant"""
    print(f"\n🔐 TEST: Connexion membre existant")
    
    # Utiliser les credentials du test précédent si disponible
    # Ou créer un nouveau membre
    existing_email = "demo@khanelconcept.com"  # Email de test connu
    existing_password = "demo123"
    
    login_data = {
        "email": existing_email,
        "password": existing_password,
        "remember": False
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/members/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Connexion réussie avec membre existant")
            print(f"   Membre: {data.get('member', {}).get('firstName')} {data.get('member', {}).get('lastName')}")
            return True
        else:
            print(f"   ❌ Connexion échouée: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def run_diagnostic():
    """Exécuter le diagnostic complet"""
    print("🔍 DIAGNOSTIC INSCRIPTION BACKEND")
    print("=" * 50)
    
    # Test 1: Mécanisme de hachage
    hash_ok = test_password_hashing()
    
    # Test 2: Cycle complet inscription → connexion
    cycle_ok = test_registration_and_immediate_login()
    
    # Test 3: Connexion membre existant
    existing_ok = test_existing_member_login()
    
    print("\n" + "=" * 50)
    print("📊 RÉSULTATS DIAGNOSTIC")
    print("=" * 50)
    
    print(f"🔐 Hachage password: {'✅ OK' if hash_ok else '❌ PROBLÈME'}")
    print(f"🔄 Cycle inscription→connexion: {'✅ OK' if cycle_ok else '❌ PROBLÈME'}")
    print(f"👤 Connexion existant: {'✅ OK' if existing_ok else '❌ PROBLÈME'}")
    
    if not cycle_ok:
        print(f"\n🚨 PROBLÈME IDENTIFIÉ:")
        print(f"   Le problème 'compte introuvable' est confirmé")
        print(f"   L'inscription fonctionne mais la connexion échoue")
        print(f"   Cause probable: Incohérence dans le hachage/vérification des mots de passe")
    else:
        print(f"\n✅ SYSTÈME OPÉRATIONNEL:")
        print(f"   Le cycle inscription → connexion fonctionne correctement")
    
    return cycle_ok

if __name__ == "__main__":
    success = run_diagnostic()
    exit(0 if success else 1)