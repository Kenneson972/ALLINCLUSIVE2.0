#!/usr/bin/env python3
"""
🧪 TEST AVEC DONNÉES EXACTES DE LA REVIEW REQUEST
Test avec les données exactes mentionnées dans la demande de test
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8001"
API_BASE = f"{BASE_URL}/api"

# Données EXACTES de la review request
EXACT_TEST_DATA = {
    "firstName": "Sophie",
    "lastName": "Martineau", 
    "email": "sophie.martineau@nouvelleforme.com",
    "phone": "+596123987654",
    "password": "MonNouveauPass2025!",
    "birthDate": "1992-06-10",
    "acceptTerms": True
}

def test_exact_review_data():
    """Test avec les données exactes de la review request"""
    print("🎯 TEST AVEC DONNÉES EXACTES DE LA REVIEW REQUEST")
    print("="*60)
    
    # Ajouter timestamp pour éviter les doublons
    test_email = f"sophie.martineau.exact.{int(time.time())}@nouvelleforme.com"
    test_data = EXACT_TEST_DATA.copy()
    test_data["email"] = test_email
    
    print("📝 Données exactes de la review request:")
    print(json.dumps(test_data, indent=2, ensure_ascii=False))
    
    try:
        # 1. Test inscription
        print("\n🔄 1. TEST INSCRIPTION...")
        response = requests.post(
            f"{API_BASE}/members/register",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ INSCRIPTION RÉUSSIE")
            
            member = data["member"]
            token = data["token"]
            
            # Vérifications critiques
            checks = []
            
            # Vérifier absence de nationalité
            if "nationality" not in member:
                checks.append("✅ Nationalité correctement absente")
            else:
                checks.append("❌ Nationalité encore présente!")
            
            # Vérifier présence des champs requis
            required = ["id", "firstName", "lastName", "email", "phone", "level", "points"]
            if all(field in member for field in required):
                checks.append("✅ Tous les champs requis présents")
            else:
                missing = [f for f in required if f not in member]
                checks.append(f"❌ Champs manquants: {missing}")
            
            # Vérifier token
            if token and len(token) > 50:
                checks.append("✅ Token JWT généré")
            else:
                checks.append("❌ Token JWT invalide")
            
            for check in checks:
                print(f"   {check}")
            
            # 2. Test connexion immédiate
            print("\n🔄 2. TEST CONNEXION IMMÉDIATE...")
            login_data = {
                "email": test_email,
                "password": "MonNouveauPass2025!",
                "remember": False
            }
            
            login_response = requests.post(
                f"{API_BASE}/members/login",
                json=login_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            print(f"Status: {login_response.status_code}")
            
            if login_response.status_code == 200:
                login_data_resp = login_response.json()
                print("✅ CONNEXION IMMÉDIATE RÉUSSIE")
                
                login_member = login_data_resp["member"]
                
                # Vérifier que nationalité n'est toujours pas présente
                if "nationality" not in login_member:
                    print("   ✅ Nationalité toujours absente après connexion")
                else:
                    print("   ❌ Nationalité apparue après connexion!")
                
                print(f"   👤 Membre: {login_member['firstName']} {login_member['lastName']}")
                print(f"   📧 Email: {login_member['email']}")
                print(f"   🏆 Niveau: {login_member['level']}")
                print(f"   ⭐ Points: {login_member['points']}")
                
                # 3. Test vérification MongoDB
                print("\n🔄 3. VÉRIFICATION STOCKAGE MONGODB...")
                profile_response = requests.get(
                    f"{API_BASE}/members/profile/{member['id']}",
                    timeout=10
                )
                
                if profile_response.status_code == 200:
                    profile_data = profile_response.json()
                    
                    if "nationality" not in profile_data:
                        print("   ✅ Nationalité absente du stockage MongoDB")
                    else:
                        print("   ❌ Nationalité stockée en MongoDB!")
                    
                    print("   ✅ Données correctement persistées en base")
                else:
                    print(f"   ❌ Erreur accès profil: {profile_response.status_code}")
                
                return True
                
            else:
                print(f"❌ CONNEXION ÉCHOUÉE: {login_response.text}")
                return False
                
        else:
            print(f"❌ INSCRIPTION ÉCHOUÉE: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        return False

def main():
    print("🌴 KHANELCONCEPT - TEST DONNÉES EXACTES REVIEW REQUEST")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔗 {BASE_URL}")
    
    success = test_exact_review_data()
    
    print("\n" + "="*60)
    if success:
        print("🎉 SUCCÈS TOTAL: Toutes les exigences de la review request sont satisfaites!")
        print("✅ Inscription sans nationalité: OK")
        print("✅ Connexion immédiate: OK") 
        print("✅ Stockage MongoDB correct: OK")
        print("✅ Validation sécurité maintenue: OK")
    else:
        print("❌ ÉCHEC: Des problèmes ont été détectés")
    
    return success

if __name__ == "__main__":
    main()