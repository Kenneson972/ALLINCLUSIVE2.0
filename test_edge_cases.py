#!/usr/bin/env python3
"""
🧪 TESTS COMPLÉMENTAIRES - EDGE CASES ET SÉCURITÉ
Tests des cas limites et de la sécurité du système d'inscription
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8001"
API_BASE = f"{BASE_URL}/api"

def test_security_validation():
    """Tests de sécurité et validation avancés"""
    print("🔒 TESTS DE SÉCURITÉ ET VALIDATION")
    print("="*50)
    
    test_cases = [
        {
            "name": "Tentative avec nationalité (doit être ignorée)",
            "data": {
                "firstName": "Test",
                "lastName": "User",
                "email": f"test.nationality.{int(time.time())}@test.com",
                "phone": "+596123456789",
                "password": "TestPass2025!",
                "birthDate": "1990-01-01",
                "acceptTerms": True,
                "nationality": "FR"  # Ce champ doit être ignoré
            },
            "should_succeed": True,
            "check": "nationality_ignored"
        },
        {
            "name": "Mot de passe très faible",
            "data": {
                "firstName": "Test",
                "lastName": "User", 
                "email": f"test.weak.{int(time.time())}@test.com",
                "phone": "+596123456789",
                "password": "123",
                "birthDate": "1990-01-01",
                "acceptTerms": True
            },
            "should_succeed": False,
            "check": "password_validation"
        },
        {
            "name": "Téléphone format Martinique invalide",
            "data": {
                "firstName": "Test",
                "lastName": "User",
                "email": f"test.phone.{int(time.time())}@test.com", 
                "phone": "0596123456",  # Format local au lieu d'international
                "password": "TestPass2025!",
                "birthDate": "1990-01-01",
                "acceptTerms": True
            },
            "should_succeed": False,
            "check": "phone_validation"
        },
        {
            "name": "Champs requis manquants",
            "data": {
                "firstName": "Test",
                # lastName manquant
                "email": f"test.missing.{int(time.time())}@test.com",
                "phone": "+596123456789",
                "password": "TestPass2025!",
                "acceptTerms": True
            },
            "should_succeed": False,
            "check": "required_fields"
        },
        {
            "name": "XSS dans les noms",
            "data": {
                "firstName": "<script>alert('xss')</script>",
                "lastName": "User",
                "email": f"test.xss.{int(time.time())}@test.com",
                "phone": "+596123456789", 
                "password": "TestPass2025!",
                "birthDate": "1990-01-01",
                "acceptTerms": True
            },
            "should_succeed": True,  # Doit réussir mais avec sanitisation
            "check": "xss_sanitization"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Test {i}: {test_case['name']}")
        
        try:
            response = requests.post(
                f"{API_BASE}/members/register",
                json=test_case["data"],
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            success = response.status_code == 200
            expected_success = test_case["should_succeed"]
            
            if success == expected_success:
                if success:
                    data = response.json()
                    member = data.get("member", {})
                    
                    # Vérifications spécifiques
                    if test_case["check"] == "nationality_ignored":
                        if "nationality" not in member:
                            print("   ✅ Champ nationalité correctement ignoré")
                            results.append(True)
                        else:
                            print("   ❌ Champ nationalité non ignoré!")
                            results.append(False)
                    
                    elif test_case["check"] == "xss_sanitization":
                        first_name = member.get("firstName", "")
                        if "<script>" not in first_name:
                            print("   ✅ XSS correctement sanitisé")
                            results.append(True)
                        else:
                            print("   ❌ XSS non sanitisé!")
                            results.append(False)
                    else:
                        print("   ✅ Test réussi comme attendu")
                        results.append(True)
                else:
                    print(f"   ✅ Erreur correctement détectée (Status: {response.status_code})")
                    results.append(True)
            else:
                print(f"   ❌ Résultat inattendu - Status: {response.status_code}")
                print(f"   Attendu: {'succès' if expected_success else 'échec'}")
                results.append(False)
                
        except Exception as e:
            print(f"   ❌ Erreur test: {e}")
            results.append(False)
    
    return results

def test_duplicate_registration():
    """Test de gestion des doublons"""
    print("\n👥 TEST GESTION DOUBLONS")
    print("="*30)
    
    # Créer un membre
    test_email = f"duplicate.test.{int(time.time())}@test.com"
    member_data = {
        "firstName": "Duplicate",
        "lastName": "Test",
        "email": test_email,
        "phone": "+596123456789",
        "password": "TestPass2025!",
        "birthDate": "1990-01-01",
        "acceptTerms": True
    }
    
    try:
        # Première inscription
        print("🔄 Première inscription...")
        response1 = requests.post(
            f"{API_BASE}/members/register",
            json=member_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response1.status_code == 200:
            print("   ✅ Première inscription réussie")
            
            # Tentative de doublon
            print("🔄 Tentative de doublon...")
            response2 = requests.post(
                f"{API_BASE}/members/register",
                json=member_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response2.status_code == 400:
                print("   ✅ Doublon correctement rejeté")
                return True
            else:
                print(f"   ❌ Doublon non détecté - Status: {response2.status_code}")
                return False
        else:
            print(f"   ❌ Première inscription échouée - Status: {response1.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur test doublon: {e}")
        return False

def test_complete_cycle():
    """Test du cycle complet inscription → connexion → profil"""
    print("\n🔄 TEST CYCLE COMPLET")
    print("="*25)
    
    test_email = f"cycle.test.{int(time.time())}@test.com"
    password = "CycleTest2025!"
    
    member_data = {
        "firstName": "Cycle",
        "lastName": "Test",
        "email": test_email,
        "phone": "+596123456789",
        "password": password,
        "birthDate": "1990-01-01",
        "acceptTerms": True
    }
    
    try:
        # 1. Inscription
        print("1️⃣ Inscription...")
        reg_response = requests.post(
            f"{API_BASE}/members/register",
            json=member_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if reg_response.status_code != 200:
            print(f"   ❌ Inscription échouée: {reg_response.status_code}")
            return False
        
        reg_data = reg_response.json()
        member = reg_data["member"]
        member_id = member["id"]
        print(f"   ✅ Membre créé: {member_id}")
        
        # 2. Connexion
        print("2️⃣ Connexion...")
        login_response = requests.post(
            f"{API_BASE}/members/login",
            json={"email": test_email, "password": password, "remember": False},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if login_response.status_code != 200:
            print(f"   ❌ Connexion échouée: {login_response.status_code}")
            return False
        
        login_data = login_response.json()
        token = login_data["token"]
        print("   ✅ Connexion réussie")
        
        # 3. Vérification profil
        print("3️⃣ Vérification profil...")
        profile_response = requests.get(
            f"{API_BASE}/members/profile/{member_id}",
            timeout=10
        )
        
        if profile_response.status_code != 200:
            print(f"   ❌ Accès profil échoué: {profile_response.status_code}")
            return False
        
        profile_data = profile_response.json()
        
        # Vérifications finales
        checks = [
            ("nationality" not in profile_data, "Nationalité absente du profil"),
            (profile_data.get("firstName") == "Cycle", "Prénom correct"),
            (profile_data.get("email") == test_email, "Email correct"),
            ("password" not in profile_data, "Mot de passe non exposé")
        ]
        
        all_good = True
        for check, description in checks:
            if check:
                print(f"   ✅ {description}")
            else:
                print(f"   ❌ {description}")
                all_good = False
        
        return all_good
        
    except Exception as e:
        print(f"   ❌ Erreur cycle complet: {e}")
        return False

def main():
    print("🌴 KHANELCONCEPT - TESTS COMPLÉMENTAIRES")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔗 {BASE_URL}")
    
    # Exécuter tous les tests
    security_results = test_security_validation()
    duplicate_result = test_duplicate_registration()
    cycle_result = test_complete_cycle()
    
    # Résumé
    print("\n" + "="*60)
    print("📊 RÉSUMÉ TESTS COMPLÉMENTAIRES")
    
    security_passed = sum(security_results)
    security_total = len(security_results)
    
    print(f"🔒 Sécurité: {security_passed}/{security_total} tests réussis")
    print(f"👥 Doublons: {'✅' if duplicate_result else '❌'}")
    print(f"🔄 Cycle complet: {'✅' if cycle_result else '❌'}")
    
    total_passed = security_passed + (1 if duplicate_result else 0) + (1 if cycle_result else 0)
    total_tests = security_total + 2
    success_rate = (total_passed / total_tests) * 100
    
    print(f"\n🎯 SCORE GLOBAL: {total_passed}/{total_tests} ({success_rate:.1f}%)")
    
    if success_rate >= 90:
        print("🎉 EXCELLENT: Système très robuste!")
    elif success_rate >= 80:
        print("✅ BON: Système fonctionnel avec quelques améliorations possibles")
    else:
        print("⚠️ ATTENTION: Des améliorations sont nécessaires")

if __name__ == "__main__":
    main()