"""
Test de Charge KhanelConcept API avec Locust
==========================================

Script de test de performance pour simuler 100 utilisateurs simultanés
effectuant des opérations réalistes sur l'API KhanelConcept.

Scénarios testés:
1. Connexion membre (POST /api/members/login)
2. Recherche de villas (POST /api/villas/search)  
3. Création de réservation (POST /api/reservations)

Usage:
    pip install locust
    locust -f load_test_locust.py --host=http://localhost:8001
"""

from locust import HttpUser, task, between
import json
import random
from datetime import datetime, timedelta
import uuid

class KhanelConceptUser(HttpUser):
    wait_time = between(1, 3)  # Attendre 1-3 secondes entre les requêtes
    
    def on_start(self):
        """Initialisation - Créer et connecter un membre de test"""
        self.member_token = None
        self.member_email = f"loadtest_{random.randint(1000, 9999)}@test.com"
        self.member_data = {
            "firstName": f"User{random.randint(1, 1000)}",
            "lastName": f"Test{random.randint(1, 1000)}",
            "email": self.member_email,
            "phone": f"+596{random.randint(100000000, 999999999)}",
            "password": "LoadTest123!",
            "acceptTerms": True
        }
        
        # Destinations possibles pour les recherches
        self.destinations = [
            "Fort-de-France", "Lamentin", "Schoelcher", "Vauclin", 
            "Ste-Anne", "Ducos", "Rivière-Salée", "Petit-Macabou"
        ]
        
        # Essayer de se connecter (les membres existants ou créer si nécessaire)
        self.login_member()
    
    def login_member(self):
        """Connexion d'un membre (ou inscription si nécessaire)"""
        try:
            # Essayer de se connecter d'abord
            login_data = {
                "email": self.member_email,
                "password": "LoadTest123!"
            }
            
            with self.client.post(
                "/api/members/login", 
                json=login_data, 
                catch_response=True,
                name="Member Login (Existing)"
            ) as response:
                if response.status_code == 200:
                    data = response.json()
                    self.member_token = data.get("token")
                    response.success()
                elif response.status_code == 401:
                    # Membre n'existe pas, l'inscrire
                    self.register_member()
                else:
                    response.failure(f"Login failed: {response.status_code}")
                    
        except Exception as e:
            print(f"Login error: {e}")
    
    def register_member(self):
        """Inscription d'un nouveau membre pour les tests"""
        try:
            with self.client.post(
                "/api/members/register",
                json=self.member_data,
                catch_response=True,
                name="Member Registration"
            ) as response:
                if response.status_code == 200:
                    # En production, il faudrait vérifier l'email
                    # Pour les tests, on simule un membre actif
                    response.success()
                    # Essayer de se connecter après inscription
                    # Note: En réalité, il faut vérifier l'email d'abord
                    print("Member registered, but email verification needed")
                else:
                    response.failure(f"Registration failed: {response.status_code}")
                    
        except Exception as e:
            print(f"Registration error: {e}")

    @task(3)
    def search_villas(self):
        """Recherche de villas avec différents critères"""
        search_criteria = {
            "destination": random.choice(self.destinations),
            "guests": random.randint(2, 8),
            "category": random.choice(["sejour", "fete", "all"])
        }
        
        with self.client.post(
            "/api/villas/search",
            json=search_criteria,
            catch_response=True,
            name="Villa Search"
        ) as response:
            if response.status_code == 200:
                villas = response.json()
                if len(villas) > 0:
                    response.success()
                    # Stocker une villa pour les réservations
                    self.selected_villa = random.choice(villas)
                else:
                    response.success()  # Pas d'erreur si aucun résultat
            else:
                response.failure(f"Search failed: {response.status_code}")

    @task(2)
    def get_all_villas(self):
        """Récupération de toutes les villas"""
        with self.client.get(
            "/api/villas",
            catch_response=True,
            name="Get All Villas"
        ) as response:
            if response.status_code == 200:
                villas = response.json()
                if len(villas) > 0:
                    response.success()
                    # Stocker une villa pour les réservations
                    self.selected_villa = random.choice(villas)
                else:
                    response.failure("No villas returned")
            else:
                response.failure(f"Get villas failed: {response.status_code}")

    @task(1)
    def create_reservation(self):
        """Création d'une réservation"""
        if not hasattr(self, 'selected_villa') or not self.selected_villa:
            # Pas de villa sélectionnée, en choisir une par défaut
            self.selected_villa = {"id": "1", "name": "Villa Test", "price": 150}
        
        # Générer des dates de réservation
        checkin = datetime.now() + timedelta(days=random.randint(7, 60))
        checkout = checkin + timedelta(days=random.randint(2, 14))
        
        reservation_data = {
            "villa_id": str(self.selected_villa.get("id", "1")),
            "customer_name": f"{self.member_data['firstName']} {self.member_data['lastName']}",
            "customer_email": self.member_email,
            "customer_phone": self.member_data["phone"],
            "checkin_date": checkin.strftime("%Y-%m-%d"),
            "checkout_date": checkout.strftime("%Y-%m-%d"),
            "guests_count": random.randint(2, 6),
            "message": "Réservation de test de charge",
            "total_price": float(random.randint(300, 2000))
        }
        
        with self.client.post(
            "/api/reservations",
            json=reservation_data,
            catch_response=True,
            name="Create Reservation"
        ) as response:
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    response.success()
                else:
                    response.failure(f"Reservation not successful: {data}")
            else:
                response.failure(f"Reservation failed: {response.status_code}")

    @task(1)
    def admin_login_test(self):
        """Test de connexion admin (pour tester la charge sur l'auth)"""
        admin_data = {
            "username": "admin",
            "password": "khanelconcept2025"
        }
        
        with self.client.post(
            "/api/admin/login",
            json=admin_data,
            catch_response=True,
            name="Admin Login"
        ) as response:
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data:
                    response.success()
                else:
                    response.failure("No access token in response")
            else:
                response.failure(f"Admin login failed: {response.status_code}")

    @task(1)  
    def health_check(self):
        """Test de l'endpoint de santé"""
        with self.client.get(
            "/api/health",
            catch_response=True,
            name="Health Check"
        ) as response:
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    response.success()
                else:
                    response.failure(f"API not healthy: {data}")
            else:
                response.failure(f"Health check failed: {response.status_code}")

    @task(1)
    def dashboard_stats(self):
        """Test des statistiques dashboard"""
        with self.client.get(
            "/api/stats/dashboard",
            catch_response=True,
            name="Dashboard Stats"
        ) as response:
            if response.status_code == 200:
                data = response.json()
                if "total_villas" in data:
                    response.success()
                else:
                    response.failure("Missing stats data")
            else:
                response.failure(f"Dashboard stats failed: {response.status_code}")

# Configuration personnalisée pour le test
class WebsiteUser(KhanelConceptUser):
    weight = 1  # Poids relatif de ce type d'utilisateur

if __name__ == "__main__":
    # Pour lancer directement le script
    import subprocess
    import sys
    
    print("🚀 Lancement du test de charge KhanelConcept...")
    print("📊 Configuration: 100 utilisateurs, montée en charge progressive")
    print("🎯 URL cible: http://localhost:8001")
    print("\nLancement de Locust...")
    
    # Commande Locust avec paramètres optimisés
    cmd = [
        "locust",
        "-f", "load_test_locust.py",
        "--host=http://localhost:8001",
        "--users=100",
        "--spawn-rate=10", 
        "--run-time=300s",  # 5 minutes
        "--html=load_test_report.html"
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print("❌ Erreur lors du lancement de Locust")
        print("💡 Vérifiez que Locust est installé: pip install locust")
        sys.exit(1)