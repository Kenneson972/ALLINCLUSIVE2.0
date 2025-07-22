#!/usr/bin/env python3
"""
🧪 TEST INSCRIPTION BACKEND - Vérification connexion frontend → backend

Test urgent pour vérifier que l'endpoint d'inscription fonctionne correctement
avec des données réalistes françaises/martiniquaises.

FOCUS: Tester le cycle complet inscription → connexion
"""

import requests
import json
import time
from datetime import datetime
import uuid

# Configuration
BACKEND_URL = "http://localhost:8001"  # Backend URL interne
API_BASE = f"{BACKEND_URL}/api"

# Données de test françaises/martiniquaises
TEST_DATA = {
    "firstName": "Marie-Claire",
    "lastName": "Dubois", 
    "email": f"marie.dubois.{int(time.time())}@martinique.com",  # Email unique
    "phone": "+596123456789",
    "password": "MonMotDePasse2025!",
    "birthDate": "1985-03-15",
    "nationality": "FR",
    "acceptTerms": True
}

def print_test_header(test_name):
    """Afficher l'en-tête du test"""
    print(f"\n{'='*60}")
    print(f"🧪 {test_name}")
    print(f"{'='*60}")

def print_result(success, message, details=None):
    """Afficher le résultat d'un test"""
    status = "✅ SUCCÈS" if success else "❌ ÉCHEC"
    print(f"{status}: {message}")
    if details:
        print(f"   Détails: {details}")

def test_backend_health():
    """Test 1: Vérifier que le backend répond"""
    print_test_header("TEST 1: Santé du Backend")
    
    try:
        response = requests.get(f"{API_BASE}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_result(True, "Backend accessible", f"Status: {data.get('status')}")
            return True
        else:
            print_result(False, f"Backend inaccessible", f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_result(False, "Erreur de connexion backend", str(e))
        return False

def test_member_registration():
    """Test 2: Inscription d'un nouveau membre"""
    print_test_header("TEST 2: Inscription Membre")
    
    try:
        print(f"📝 Données d'inscription:")
        print(f"   Nom: {TEST_DATA['firstName']} {TEST_DATA['lastName']}")
        print(f"   Email: {TEST_DATA['email']}")
        print(f"   Téléphone: {TEST_DATA['phone']}")
        print(f"   Nationalité: {TEST_DATA['nationality']}")
        
        response = requests.post(
            f"{API_BASE}/members/register",
            json=TEST_DATA,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"📡 Réponse HTTP: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                member = data.get("member", {})
                token = data.get("token")
                
                print_result(True, "Inscription réussie")
                print(f"   👤 Membre ID: {member.get('id')}")
                print(f"   📧 Email: {member.get('email')}")
                print(f"   🏆 Niveau: {member.get('level')}")
                print(f"   ⭐ Points: {member.get('points')}")
                print(f"   🔑 Token JWT: {'Présent' if token else 'Absent'}")
                
                # Sauvegarder les infos pour les tests suivants
                TEST_DATA['member_id'] = member.get('id')
                TEST_DATA['token'] = token
                
                return True
            else:
                print_result(False, "Inscription échouée", data.get("message"))
                return False
        else:
            error_msg = response.text
            print_result(False, f"Erreur HTTP {response.status_code}", error_msg)
            return False
            
    except Exception as e:
        print_result(False, "Erreur lors de l'inscription", str(e))
        return False

def test_member_login():
    """Test 3: Connexion avec les mêmes credentials"""
    print_test_header("TEST 3: Connexion Membre")
    
    try:
        login_data = {
            "email": TEST_DATA["email"],
            "password": TEST_DATA["password"],
            "remember": False
        }
        
        print(f"🔐 Tentative de connexion:")
        print(f"   Email: {login_data['email']}")
        print(f"   Password: {'*' * len(login_data['password'])}")
        
        response = requests.post(
            f"{API_BASE}/members/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"📡 Réponse HTTP: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                member = data.get("member", {})
                token = data.get("token")
                
                print_result(True, "Connexion réussie")
                print(f"   👤 Membre ID: {member.get('id')}")
                print(f"   📧 Email: {member.get('email')}")
                print(f"   🏆 Niveau: {member.get('level')}")
                print(f"   ⭐ Points: {member.get('points')}")
                print(f"   🔑 Token JWT: {'Présent' if token else 'Absent'}")
                
                # Vérifier cohérence avec l'inscription
                if member.get('id') == TEST_DATA.get('member_id'):
                    print_result(True, "Cohérence des données", "ID membre identique")
                else:
                    print_result(False, "Incohérence des données", "ID membre différent")
                
                return True
            else:
                print_result(False, "Connexion échouée", data.get("message"))
                return False
        else:
            error_msg = response.text
            print_result(False, f"Erreur HTTP {response.status_code}", error_msg)
            return False
            
    except Exception as e:
        print_result(False, "Erreur lors de la connexion", str(e))
        return False

def test_token_verification():
    """Test 4: Vérification du token JWT"""
    print_test_header("TEST 4: Vérification Token JWT")
    
    if not TEST_DATA.get('token'):
        print_result(False, "Pas de token à vérifier", "Token manquant des tests précédents")
        return False
    
    try:
        token_data = {"token": TEST_DATA['token']}
        
        response = requests.post(
            f"{API_BASE}/members/verify-token",
            json=token_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"📡 Réponse HTTP: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("valid"):
                member = data.get("member", {})
                print_result(True, "Token valide")
                print(f"   👤 Membre vérifié: {member.get('firstName')} {member.get('lastName')}")
                print(f"   📧 Email: {member.get('email')}")
                return True
            else:
                print_result(False, "Token invalide", "Validation échouée")
                return False
        else:
            error_msg = response.text
            print_result(False, f"Erreur HTTP {response.status_code}", error_msg)
            return False
            
    except Exception as e:
        print_result(False, "Erreur lors de la vérification", str(e))
        return False

def test_member_profile():
    """Test 5: Récupération du profil membre"""
    print_test_header("TEST 5: Profil Membre")
    
    if not TEST_DATA.get('member_id'):
        print_result(False, "Pas d'ID membre", "ID manquant des tests précédents")
        return False
    
    try:
        response = requests.get(
            f"{API_BASE}/members/profile/{TEST_DATA['member_id']}",
            timeout=10
        )
        
        print(f"📡 Réponse HTTP: {response.status_code}")
        
        if response.status_code == 200:
            member = response.json()
            print_result(True, "Profil récupéré")
            print(f"   👤 Nom complet: {member.get('firstName')} {member.get('lastName')}")
            print(f"   📧 Email: {member.get('email')}")
            print(f"   📱 Téléphone: {member.get('phone')}")
            print(f"   🎂 Date naissance: {member.get('birthDate')}")
            print(f"   🌍 Nationalité: {member.get('nationality')}")
            print(f"   🏆 Niveau: {member.get('level')}")
            print(f"   ⭐ Points: {member.get('points')}")
            print(f"   📅 Date inscription: {member.get('joinDate')}")
            print(f"   ✅ Actif: {member.get('isActive')}")
            
            # Vérifier que le mot de passe n'est pas exposé
            if 'password' not in member:
                print_result(True, "Sécurité OK", "Mot de passe non exposé")
            else:
                print_result(False, "Faille sécurité", "Mot de passe exposé dans le profil")
            
            return True
        else:
            error_msg = response.text
            print_result(False, f"Erreur HTTP {response.status_code}", error_msg)
            return False
            
    except Exception as e:
        print_result(False, "Erreur lors de la récupération", str(e))
        return False

def test_duplicate_registration():
    """Test 6: Tentative d'inscription avec le même email"""
    print_test_header("TEST 6: Protection Doublons")
    
    try:
        # Tenter de s'inscrire avec le même email
        response = requests.post(
            f"{API_BASE}/members/register",
            json=TEST_DATA,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"📡 Réponse HTTP: {response.status_code}")
        
        if response.status_code == 400:
            error_data = response.json()
            print_result(True, "Protection doublons active", error_data.get("detail"))
            return True
        elif response.status_code == 200:
            print_result(False, "Protection doublons défaillante", "Inscription dupliquée autorisée")
            return False
        else:
            error_msg = response.text
            print_result(False, f"Erreur inattendue {response.status_code}", error_msg)
            return False
            
    except Exception as e:
        print_result(False, "Erreur lors du test", str(e))
        return False

def run_inscription_tests():
    """Exécuter tous les tests d'inscription"""
    print(f"\n🌴 TESTS INSCRIPTION BACKEND KHANELCONCEPT")
    print(f"⏰ Démarrage: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Focus: Cycle inscription → connexion")
    
    tests = [
        ("Santé Backend", test_backend_health),
        ("Inscription Membre", test_member_registration),
        ("Connexion Membre", test_member_login),
        ("Vérification Token", test_token_verification),
        ("Profil Membre", test_member_profile),
        ("Protection Doublons", test_duplicate_registration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            
            # Pause entre les tests
            time.sleep(1)
            
        except Exception as e:
            print_result(False, f"Erreur critique dans {test_name}", str(e))
            results.append((test_name, False))
    
    # Résumé final
    print(f"\n{'='*60}")
    print(f"📊 RÉSUMÉ DES TESTS")
    print(f"{'='*60}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    success_rate = (passed / total) * 100 if total > 0 else 0
    
    for test_name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 RÉSULTAT GLOBAL: {passed}/{total} tests réussis ({success_rate:.1f}%)")
    
    if success_rate >= 80:
        print(f"✅ INSCRIPTION BACKEND OPÉRATIONNELLE")
        print(f"   Le cycle inscription → connexion fonctionne correctement")
    else:
        print(f"❌ PROBLÈMES DÉTECTÉS DANS L'INSCRIPTION")
        print(f"   Le backend nécessite des corrections")
    
    print(f"\n⏰ Fin des tests: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return success_rate >= 80

if __name__ == "__main__":
    success = run_inscription_tests()
    exit(0 if success else 1)