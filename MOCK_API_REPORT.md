# MOCK API REPORT

## Endpoints appelés par le front
- GET /api/v1/villas (admin-main.js loadData)
- GET /api/v1/settings (admin-main.js loadData)
- GET /api/v1/reservations (data-export.js export si nécessaire)

## Endpoints no-op ajoutés (FastAPI)
- POST /api/v1/reservations → retourne {status:'created', id:'mock_<villa_id>', data:<payload>}
- POST /api/v1/images → retourne {status:'uploaded', url:'assets/images/placeholders/villa-placeholder.jpg'}
- PUT /api/v1/settings → retourne l'objet reçu (echo)

## CRUD réel (MySQL) à implémenter
- Villas: GET/POST/GET:id/PUT:id/DELETE:id (protégé en écriture)
- Images: GET:villa/:id/images, POST:villa/:id/images, DELETE:image/:id (protégé)
- Reservations: GET/POST/PUT:id/DELETE:id (protégé pour PUT/DELETE; POST public)
- Users: POST auth/login, GET auth/me (protégé), POST users (inscription), etc.
- Settings: GET public, PUT protégé
