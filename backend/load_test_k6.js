/*
Test de Charge KhanelConcept API avec k6
=======================================

Script de test de performance pour simuler 100 utilisateurs simultanés
effectuant des opérations réalistes sur l'API KhanelConcept.

Scénarios testés:
1. Connexion admin/membre
2. Recherche de villas
3. Création de réservation  
4. Récupération des statistiques

Usage:
    # Installation k6
    curl https://github.com/grafana/k6/releases/download/v0.47.0/k6-v0.47.0-linux-amd64.tar.gz -L | tar xvz --strip-components 1
    
    # Lancer le test
    ./k6 run --vus 100 --duration 300s load_test_k6.js
*/

import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';

// Métriques personnalisées
const loginSuccessRate = new Rate('login_success_rate');
const searchSuccessRate = new Rate('search_success_rate');
const reservationSuccessRate = new Rate('reservation_success_rate');
const responseTime = new Trend('response_time');
const errorCounter = new Counter('errors');

// Configuration du test
export let options = {
  stages: [
    { duration: '30s', target: 20 },   // Montée progressive à 20 utilisateurs
    { duration: '60s', target: 50 },   // Montée à 50 utilisateurs  
    { duration: '120s', target: 100 }, // Montée à 100 utilisateurs (pic)
    { duration: '60s', target: 100 },  // Maintien à 100 utilisateurs
    { duration: '30s', target: 0 },    // Descente progressive
  ],
  thresholds: {
    http_req_duration: ['p(95)<2000'], // 95% des requêtes < 2s
    http_req_failed: ['rate<0.1'],      // Taux d'erreur < 10%
    login_success_rate: ['rate>0.8'],   // Taux de succès login > 80%
    search_success_rate: ['rate>0.9'],  // Taux de succès recherche > 90%
    reservation_success_rate: ['rate>0.7'], // Taux de succès réservation > 70%
  },
};

// Configuration de base
const BASE_URL = 'http://localhost:8001/api';

// Données de test
const destinations = [
  'Fort-de-France', 'Lamentin', 'Schoelcher', 'Vauclin',
  'Ste-Anne', 'Ducos', 'Rivière-Salée', 'Petit-Macabou'
];

const categories = ['sejour', 'fete', 'all'];

// Fonction utilitaire pour générer des données aléatoires
function randomChoice(array) {
  return array[Math.floor(Math.random() * array.length)];
}

function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function generateEmail() {
  return `loadtest_${randomInt(1000, 9999)}@test.com`;
}

function generateDates() {
  const checkin = new Date();
  checkin.setDate(checkin.getDate() + randomInt(7, 60));
  
  const checkout = new Date(checkin);
  checkout.setDate(checkout.getDate() + randomInt(2, 14));
  
  return {
    checkin: checkin.toISOString().split('T')[0],
    checkout: checkout.toISOString().split('T')[0]
  };
}

// Fonction principale de test
export default function() {
  const userEmail = generateEmail();
  let selectedVilla = null;
  
  // 1. TEST DE SANTÉ DE L'API
  const healthStart = Date.now();
  const healthResponse = http.get(`${BASE_URL}/health`);
  responseTime.add(Date.now() - healthStart);
  
  const healthCheck = check(healthResponse, {
    'Health check status is 200': (r) => r.status === 200,
    'Health check has status healthy': (r) => {
      try {
        return r.json().status === 'healthy';
      } catch (e) {
        return false;
      }
    }
  });
  
  if (!healthCheck) {
    errorCounter.add(1);
    console.log('❌ Health check failed, skipping user session');
    return;
  }

  // 2. TEST DE CONNEXION ADMIN (parfois)
  if (Math.random() < 0.3) { // 30% du temps
    const adminLoginStart = Date.now();
    const adminLoginResponse = http.post(`${BASE_URL}/admin/login`, 
      JSON.stringify({
        username: 'admin',
        password: 'khanelconcept2025'
      }), 
      {
        headers: { 'Content-Type': 'application/json' },
      }
    );
    responseTime.add(Date.now() - adminLoginStart);
    
    const adminLoginSuccess = check(adminLoginResponse, {
      'Admin login status is 200': (r) => r.status === 200,
      'Admin login has access_token': (r) => {
        try {
          return r.json().access_token !== undefined;
        } catch (e) {
          return false;
        }
      }
    });
    
    loginSuccessRate.add(adminLoginSuccess);
    
    if (!adminLoginSuccess) {
      errorCounter.add(1);
    }
  }

  // 3. RECHERCHE DE VILLAS
  const searchStart = Date.now();
  const searchCriteria = {
    destination: randomChoice(destinations),
    guests: randomInt(2, 8),
    category: randomChoice(categories)
  };
  
  const searchResponse = http.post(`${BASE_URL}/villas/search`,
    JSON.stringify(searchCriteria),
    {
      headers: { 'Content-Type': 'application/json' },
    }
  );
  responseTime.add(Date.now() - searchStart);
  
  const searchSuccess = check(searchResponse, {
    'Villa search status is 200': (r) => r.status === 200,
    'Villa search returns array': (r) => {
      try {
        return Array.isArray(r.json());
      } catch (e) {
        return false;
      }
    }
  });
  
  searchSuccessRate.add(searchSuccess);
  
  if (searchSuccess) {
    try {
      const villas = searchResponse.json();
      if (villas.length > 0) {
        selectedVilla = villas[Math.floor(Math.random() * villas.length)];
      }
    } catch (e) {
      console.log('Error parsing search results:', e);
    }
  } else {
    errorCounter.add(1);
  }

  // 4. RÉCUPÉRATION DE TOUTES LES VILLAS (alternative)
  if (!selectedVilla) {
    const allVillasStart = Date.now();
    const allVillasResponse = http.get(`${BASE_URL}/villas`);
    responseTime.add(Date.now() - allVillasStart);
    
    const allVillasSuccess = check(allVillasResponse, {
      'Get all villas status is 200': (r) => r.status === 200,
      'Get all villas returns array': (r) => {
        try {
          return Array.isArray(r.json()) && r.json().length > 0;
        } catch (e) {
          return false;
        }
      }
    });
    
    if (allVillasSuccess) {
      try {
        const villas = allVillasResponse.json();
        selectedVilla = villas[Math.floor(Math.random() * villas.length)];
      } catch (e) {
        console.log('Error parsing all villas:', e);
      }
    } else {
      errorCounter.add(1);
    }
  }

  // 5. CRÉATION DE RÉSERVATION
  if (selectedVilla) {
    const dates = generateDates();
    const reservationData = {
      villa_id: selectedVilla.id ? selectedVilla.id.toString() : '1',
      customer_name: `LoadTest User ${randomInt(1, 1000)}`,
      customer_email: userEmail,
      customer_phone: `+596${randomInt(100000000, 999999999)}`,
      checkin_date: dates.checkin,
      checkout_date: dates.checkout,
      guests_count: randomInt(2, 6),
      message: 'Test de charge automatisé',
      total_price: randomInt(300, 2000)
    };
    
    const reservationStart = Date.now();
    const reservationResponse = http.post(`${BASE_URL}/reservations`,
      JSON.stringify(reservationData),
      {
        headers: { 'Content-Type': 'application/json' },
      }
    );
    responseTime.add(Date.now() - reservationStart);
    
    const reservationSuccess = check(reservationResponse, {
      'Reservation status is 200': (r) => r.status === 200,
      'Reservation has success flag': (r) => {
        try {
          return r.json().success === true;
        } catch (e) {
          return false;
        }
      }
    });
    
    reservationSuccessRate.add(reservationSuccess);
    
    if (!reservationSuccess) {
      errorCounter.add(1);
      console.log(`Reservation failed: ${reservationResponse.status} - ${reservationResponse.body}`);
    }
  }

  // 6. STATISTIQUES DASHBOARD
  const statsStart = Date.now();
  const statsResponse = http.get(`${BASE_URL}/stats/dashboard`);
  responseTime.add(Date.now() - statsStart);
  
  const statsSuccess = check(statsResponse, {
    'Dashboard stats status is 200': (r) => r.status === 200,
    'Dashboard stats has data': (r) => {
      try {
        const data = r.json();
        return data.total_villas !== undefined && data.total_reservations !== undefined;
      } catch (e) {
        return false;
      }
    }
  });
  
  if (!statsSuccess) {
    errorCounter.add(1);
  }

  // Pause entre les actions utilisateur
  sleep(Math.random() * 2 + 1); // 1-3 secondes
}

// Fonction de setup (avant les tests)
export function setup() {
  console.log('🚀 Démarrage du test de charge KhanelConcept');
  console.log('📊 Cible: 100 utilisateurs simultanés');
  console.log('⏱️  Durée: 5 minutes');
  console.log('🎯 URL: http://localhost:8001');
  
  // Vérifier que l'API est accessible
  const healthCheck = http.get(`${BASE_URL}/health`);
  if (healthCheck.status !== 200) {
    console.log('❌ API non accessible, arrêt du test');
    throw new Error('API health check failed');
  }
  
  console.log('✅ API accessible, lancement du test...');
  return {};
}

// Fonction de teardown (après les tests)
export function teardown(data) {
  console.log('📈 Test de charge terminé');
  console.log('📊 Consultez les métriques ci-dessus pour les résultats détaillés');
}

/*
MÉTRIQUES IMPORTANTES À SURVEILLER:

1. http_req_duration: Temps de réponse des requêtes
   - p(50): médiane
   - p(95): 95e percentile (seuil critique)

2. http_req_failed: Taux d'échec des requêtes HTTP
   - Objectif: < 10%

3. login_success_rate: Taux de succès des connexions
   - Objectif: > 80%

4. search_success_rate: Taux de succès des recherches
   - Objectif: > 90%

5. reservation_success_rate: Taux de succès des réservations
   - Objectif: > 70%

6. vus (virtual users): Nombre d'utilisateurs simulés
   - Max: 100 utilisateurs simultanés

7. iterations: Nombre total d'itérations exécutées
*/