#!/usr/bin/env python3
"""
🧪 TEST INSCRIPTION SANS NATIONALITÉ + CONFIRMATION MOT DE PASSE
Test complet du système d'inscription modifié sans champ nationalité
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8001"
API_BASE = f"{BASE_URL}/api"

# Données de test modifiées (SANS nationalité)
TEST_DATA = {
    "firstName": "Sophie",
    "lastName": "Martineau", 
    "email": "sophie.martineau@nouvelleforme.com",
    "phone": "+596123987654",
    "password": "MonNouveauPass2025!",
    "birthDate": "1992-06-10",
    "acceptTerms": True
}

def print_test_header(test_name):
    print(f"\n{'='*60}")
    print(f"🧪 {test_name}")
    print(f"{'='*60}")

def print_result(success, message, details=None):
    status = "✅ PASSED" if success else "❌ FAILED"
    print(f"{status}: {message}")
    if details:
        print(f"   Details: {details}")

def test_api_health():
    """Test de santé de l'API"""
    print_test_header("API HEALTH CHECK")
    
    try:
        response = requests.get(f"{API_BASE}/health", timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            print_result(True, f"API accessible - Status: {data.get('status')}")
            return True
        else:
            print_result(False, f"API non accessible - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print_result(False, f"Erreur connexion API: {e}")
        return False

def test_member_registration():
    """Test d'inscription membre SANS nationalité"""
    print_test_header("INSCRIPTION MEMBRE SANS NATIONALITÉ")
    
    try:
        # Ajouter timestamp pour éviter les doublons
        test_email = f"sophie.martineau.{int(time.time())}@nouvelleforme.com"
        registration_data = TEST_DATA.copy()
        registration_data["email"] = test_email
        
        print(f"📝 Données d'inscription (SANS nationalité):")
        for key, value in registration_data.items():
            if key != "password":
                print(f"   {key}: {value}")
            else:
                print(f"   {key}: {'*' * len(str(value))}")
        
        response = requests.post(
            f"{API_BASE}/members/register",
            json=registration_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"\n📡 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_result(True, "Inscription réussie sans champ nationalité")
            
            # Vérifier la structure de la réponse
            required_fields = ["success", "message", "member", "token"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                print_result(False, f"Champs manquants dans la réponse: {missing_fields}")
                return None, None
            
            member = data["member"]
            token = data["token"]
            
            # Vérifier que nationalité n'est PAS présente
            if "nationality" in member:
                print_result(False, "❌ ERREUR: Le champ 'nationality' est encore présent dans la réponse!")
                return None, None
            else:
                print_result(True, "Champ 'nationality' correctement absent de la réponse")
            
            # Vérifier les champs obligatoires du membre
            member_required = ["id", "firstName", "lastName", "email", "phone", "level", "points"]
            member_missing = [field for field in member_required if field not in member]
            
            if member_missing:
                print_result(False, f"Champs membre manquants: {member_missing}")
            else:
                print_result(True, f"Tous les champs membre présents: {member_required}")
            
            # Vérifier les valeurs
            print(f"   👤 Membre créé: {member['firstName']} {member['lastName']}")
            print(f"   📧 Email: {member['email']}")
            print(f"   📱 Téléphone: {member['phone']}")
            print(f"   🏆 Niveau: {member['level']}")
            print(f"   ⭐ Points: {member['points']}")
            print(f"   🔑 Token JWT: {token[:50]}...")
            
            return member, token
            
        else:
            error_detail = response.text
            print_result(False, f"Inscription échouée - Status: {response.status_code}")
            print(f"   Erreur: {error_detail}")
            return None, None
            
    except Exception as e:
        print_result(False, f"Erreur lors de l'inscription: {e}")
        return None, None

def test_member_login(email, password):
    """Test de connexion membre"""
    print_test_header("CONNEXION MEMBRE APRÈS INSCRIPTION")
    
    try:
        login_data = {
            "email": email,
            "password": password,
            "remember": False
        }
        
        print(f"📝 Tentative de connexion:")
        print(f"   Email: {email}")
        print(f"   Password: {'*' * len(password)}")
        
        response = requests.post(
            f"{API_BASE}/members/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"\n📡 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_result(True, "Connexion réussie immédiatement après inscription")
            
            member = data.get("member", {})
            token = data.get("token", "")
            
            # Vérifier que nationalité n'est toujours PAS présente
            if "nationality" in member:
                print_result(False, "❌ ERREUR: Le champ 'nationality' est présent dans la réponse de login!")
            else:
                print_result(True, "Champ 'nationality' correctement absent du login")
            
            print(f"   👤 Membre connecté: {member.get('firstName')} {member.get('lastName')}")
            print(f"   🔑 Nouveau token: {token[:50]}...")
            
            return True, member, token
            
        else:
            error_detail = response.text
            print_result(False, f"Connexion échouée - Status: {response.status_code}")
            print(f"   Erreur: {error_detail}")
            return False, None, None
            
    except Exception as e:
        print_result(False, f"Erreur lors de la connexion: {e}")
        return False, None, None

def test_validation_errors():
    """Test des erreurs de validation"""
    print_test_header("TESTS DE VALIDATION")
    
    test_cases = [
        {
            "name": "Sans acceptTerms",
            "data": {**TEST_DATA, "acceptTerms": False, "email": f"test1.{int(time.time())}@test.com"},
            "expected_error": "acceptation des conditions"
        },
        {
            "name": "Mot de passe faible",
            "data": {**TEST_DATA, "password": "123456", "email": f"test2.{int(time.time())}@test.com"},
            "expected_error": "Mot de passe faible"
        },
        {
            "name": "Email invalide",
            "data": {**TEST_DATA, "email": "email-invalide"},
            "expected_error": "email"
        },
        {
            "name": "Téléphone invalide",
            "data": {**TEST_DATA, "phone": "123", "email": f"test3.{int(time.time())}@test.com"},
            "expected_error": "téléphone"
        }
    ]
    
    validation_results = []
    
    for test_case in test_cases:
        print(f"\n🔍 Test: {test_case['name']}")
        
        try:
            response = requests.post(
                f"{API_BASE}/members/register",
                json=test_case["data"],
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 400 or response.status_code == 422:
                print_result(True, f"Validation correcte - Erreur détectée (Status: {response.status_code})")
                validation_results.append(True)
            else:
                print_result(False, f"Validation manquée - Status: {response.status_code}")
                print(f"   Réponse: {response.text[:200]}")
                validation_results.append(False)
                
        except Exception as e:
            print_result(False, f"Erreur test validation: {e}")
            validation_results.append(False)
    
    return validation_results

def test_mongodb_storage(member_id):
    """Test indirect du stockage MongoDB via l'API"""
    print_test_header("VÉRIFICATION STOCKAGE MONGODB")
    
    try:
        # Récupérer le profil membre pour vérifier le stockage
        response = requests.get(
            f"{API_BASE}/members/profile/{member_id}",
            timeout=10
        )
        
        if response.status_code == 200:
            member_data = response.json()
            
            # Vérifier que nationalité n'est PAS stockée
            if "nationality" in member_data:
                print_result(False, "❌ ERREUR: Le champ 'nationality' est stocké en base!")
                return False
            else:
                print_result(True, "Champ 'nationality' correctement absent du stockage")
            
            # Vérifier que les autres champs sont bien stockés
            required_stored = ["firstName", "lastName", "email", "phone", "level", "points"]
            stored_fields = [field for field in required_stored if field in member_data]
            
            if len(stored_fields) == len(required_stored):
                print_result(True, f"Tous les champs requis stockés: {stored_fields}")
                return True
            else:
                missing = [field for field in required_stored if field not in member_data]
                print_result(False, f"Champs manquants en base: {missing}")
                return False
                
        else:
            print_result(False, f"Impossible de vérifier le stockage - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print_result(False, f"Erreur vérification stockage: {e}")
        return False

def main():
    """Test principal"""
    print("🌴 KHANELCONCEPT - TEST INSCRIPTION SANS NATIONALITÉ")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔗 Backend URL: {BASE_URL}")
    
    results = {
        "api_health": False,
        "registration": False,
        "login": False,
        "validation": False,
        "storage": False
    }
    
    # 1. Test santé API
    results["api_health"] = test_api_health()
    if not results["api_health"]:
        print("\n❌ ARRÊT: API non accessible")
        return
    
    # 2. Test inscription sans nationalité
    member, token = test_member_registration()
    if member and token:
        results["registration"] = True
        
        # 3. Test connexion immédiate
        login_success, login_member, login_token = test_member_login(
            member["email"], 
            TEST_DATA["password"]
        )
        results["login"] = login_success
        
        # 4. Test stockage MongoDB
        results["storage"] = test_mongodb_storage(member["id"])
    
    # 5. Tests de validation
    validation_results = test_validation_errors()
    results["validation"] = all(validation_results)
    
    # Résumé final
    print_test_header("RÉSUMÉ FINAL")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    success_rate = (passed_tests / total_tests) * 100
    
    print(f"📊 RÉSULTATS: {passed_tests}/{total_tests} tests réussis ({success_rate:.1f}%)")
    
    for test_name, result in results.items():
        status = "✅" if result else "❌"
        print(f"   {status} {test_name.replace('_', ' ').title()}")
    
    if success_rate == 100:
        print(f"\n🎉 SUCCÈS COMPLET: L'inscription sans nationalité fonctionne parfaitement!")
        print(f"✅ Le champ nationalité a été correctement supprimé")
        print(f"✅ L'inscription → connexion fonctionne")
        print(f"✅ La validation de sécurité est maintenue")
    elif success_rate >= 80:
        print(f"\n✅ SUCCÈS PARTIEL: Système fonctionnel avec quelques points d'amélioration")
    else:
        print(f"\n❌ ÉCHEC: Problèmes critiques détectés")
    
    return results

if __name__ == "__main__":
    main()