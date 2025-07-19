from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import os
from datetime import datetime, timedelta
import uuid
import json
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="KhanelConcept API",
    description="API pour la plateforme de location de villas de luxe en Martinique",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration MongoDB
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/khanelconcept")
client = AsyncIOMotorClient(MONGO_URL)
db = client.khanelconcept

# Servir les images statiques
app.mount("/images", StaticFiles(directory="../images"), name="images")

# ========== MODELS ==========

class Villa(BaseModel):
    id: Optional[str] = None
    name: str
    location: str
    price: float
    guests: int
    guests_detail: str
    features: str
    category: str
    image: str
    gallery: List[str]
    fallback_icon: str
    amenities: Optional[List[str]] = []
    description: Optional[str] = ""
    available_dates: Optional[List[str]] = []

class ReservationCreate(BaseModel):
    villa_id: str
    customer_name: str
    customer_email: EmailStr
    customer_phone: str
    checkin_date: str
    checkout_date: str
    guests_count: int
    message: Optional[str] = ""
    total_price: float

class Reservation(ReservationCreate):
    id: Optional[str] = None
    status: str = "pending"  # pending, confirmed, cancelled
    created_at: datetime
    villa_name: Optional[str] = None

class SearchFilters(BaseModel):
    destination: Optional[str] = None
    checkin: Optional[str] = None
    checkout: Optional[str] = None
    guests: Optional[int] = None
    category: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None

# ========== VILLA DATA ==========

villas_data = [
    {
        "id": "1",
        "name": "Villa F3 Petit Macabou",
        "location": "Petit Macabou au Vauclin",
        "price": 850.0,
        "guests": 6,
        "guests_detail": "6 personnes + 9 invités",
        "features": "Sauna, Jacuzzi, 2 douches extérieures",
        "category": "sejour",
        "image": "/images/Villa_F3_Petit_Macabou/01_piscine_exterieur.jpg",
        "gallery": [
            "/images/Villa_F3_Petit_Macabou/01_piscine_exterieur.jpg",
            "/images/Villa_F3_Petit_Macabou/02_terrasse_salon_exterieur.jpg",
            "/images/Villa_F3_Petit_Macabou/03_salle_de_bain_moderne.jpg",
            "/images/Villa_F3_Petit_Macabou/04_chambre_principale.jpg",
            "/images/Villa_F3_Petit_Macabou/05_cuisine_equipee.jpg",
            "/images/Villa_F3_Petit_Macabou/07_sauna_detente.jpg",
            "/images/Villa_F3_Petit_Macabou/08_douche_exterieure.jpg"
        ],
        "fallback_icon": "🏊",
        "amenities": ["Piscine", "Sauna", "Jacuzzi", "Cuisine équipée", "WiFi", "Climatisation"],
        "description": "Magnifique villa F3 avec sauna et jacuzzi, parfaite pour un séjour de détente en famille."
    },
    {
        "id": "2",
        "name": "Villa F5 Ste Anne",
        "location": "Quartier Les Anglais, Ste Anne",
        "price": 1300.0,
        "guests": 10,
        "guests_detail": "10 personnes + 15 invités",
        "features": "Piscine, décoration rose distinctive",
        "category": "sejour",
        "image": "/images/Villa_F5_Ste_Anne/01_piscine_principale.jpg",
        "gallery": [
            "/images/Villa_F5_Ste_Anne/01_piscine_principale.jpg",
            "/images/Villa_F5_Ste_Anne/02_piscine_vue_aerienne.jpg",
            "/images/Villa_F5_Ste_Anne/03_facade_villa_rose.jpg",
            "/images/Villa_F5_Ste_Anne/04_cuisine_moderne.jpg",
            "/images/Villa_F5_Ste_Anne/05_salon_principal.jpg",
            "/images/Villa_F5_Ste_Anne/06_chambre_principale.jpg"
        ],
        "fallback_icon": "🌸",
        "amenities": ["Piscine", "Cuisine moderne", "Grande terrasse", "WiFi", "Climatisation", "Parking"],
        "description": "Villa F5 distinctive avec sa décoration rose, idéale pour grands groupes et fêtes."
    },
    {
        "id": "3",
        "name": "Villa F3 POUR LA BACCHA",
        "location": "Petit Macabou",
        "price": 1350.0,
        "guests": 6,
        "guests_detail": "6 personnes + 9 convives",
        "features": "Piscine, terrasses modernes",
        "category": "sejour",
        "image": "/images/Villa_F3_Baccha_Petit_Macabou/01_terrasse_piscine_salon_ext.jpg",
        "gallery": [
            "/images/Villa_F3_Baccha_Petit_Macabou/01_terrasse_piscine_salon_ext.jpg",
            "/images/Villa_F3_Baccha_Petit_Macabou/02_terrasse_piscine_angle.jpg",
            "/images/Villa_F3_Baccha_Petit_Macabou/03_chambre_moderne.jpg",
            "/images/Villa_F3_Baccha_Petit_Macabou/04_terrasse_jardin.jpg",
            "/images/Villa_F3_Baccha_Petit_Macabou/05_cuisine_equipee.jpg",
            "/images/Villa_F3_Baccha_Petit_Macabou/06_chambre_2.jpg"
        ],
        "fallback_icon": "🏖️",
        "amenities": ["Piscine", "Terrasses multiples", "Jardin", "Cuisine équipée", "WiFi", "Climatisation"],
        "description": "Villa moderne avec terrasses magnifiques et espace piscine exceptionnel."
    },
    {
        "id": "4",
        "name": "Studio Cocooning Lamentin",
        "location": "Morne Pitault, Lamentin",
        "price": 290.0,
        "guests": 2,
        "guests_detail": "2 personnes (couple)",
        "features": "Jacuzzi privé, vue panoramique",
        "category": "special",
        "image": "/images/Studio_Cocooning_Lamentin/01_studio_vue_ensemble.jpg",
        "gallery": [
            "/images/Studio_Cocooning_Lamentin/01_studio_vue_ensemble.jpg",
            "/images/Studio_Cocooning_Lamentin/02_cuisine_moderne.jpg",
            "/images/Studio_Cocooning_Lamentin/03_terrasse_jacuzzi.jpg",
            "/images/Studio_Cocooning_Lamentin/04_cuisine_ouverte.jpg",
            "/images/Studio_Cocooning_Lamentin/05_chambre_salon.jpg",
            "/images/Studio_Cocooning_Lamentin/07_chambre_mur_vert.jpg"
        ],
        "fallback_icon": "💕",
        "amenities": ["Jacuzzi privé", "Vue panoramique", "Cuisine équipée", "WiFi", "Climatisation"],
        "description": "Studio romantique parfait pour couples avec jacuzzi privé et vue imprenable."
    }
]

# ========== STARTUP ==========

@app.on_event("startup")
async def startup_db_client():
    """Initialiser la base de données avec les données des villas"""
    try:
        # Vérifier si les villas existent déjà
        existing_villas = await db.villas.count_documents({})
        if existing_villas == 0:
            # Insérer les données initiales des villas
            await db.villas.insert_many(villas_data)
            print(f"✅ {len(villas_data)} villas ajoutées à la base de données")
        else:
            print(f"✅ {existing_villas} villas déjà présentes dans la base de données")
            
        # Créer les index
        await db.villas.create_index("id", unique=True)
        await db.reservations.create_index("villa_id")
        await db.reservations.create_index("customer_email")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation de la DB: {e}")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

# ========== API ROUTES ==========

@app.get("/api/health")
async def health_check():
    """Vérification de santé de l'API"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.get("/api/villas", response_model=List[Villa])
async def get_villas():
    """Récupérer toutes les villas"""
    try:
        villas = await db.villas.find({}).to_list(1000)
        return villas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des villas: {e}")

@app.get("/api/villas/{villa_id}", response_model=Villa)
async def get_villa(villa_id: str):
    """Récupérer une villa spécifique"""
    villa = await db.villas.find_one({"id": villa_id})
    if not villa:
        raise HTTPException(status_code=404, detail="Villa non trouvée")
    return villa

@app.post("/api/villas/search", response_model=List[Villa])
async def search_villas(filters: SearchFilters):
    """Rechercher des villas selon les critères"""
    query = {}
    
    if filters.destination:
        query["$or"] = [
            {"location": {"$regex": filters.destination, "$options": "i"}},
            {"name": {"$regex": filters.destination, "$options": "i"}}
        ]
    
    if filters.guests:
        query["guests"] = {"$gte": filters.guests}
    
    if filters.category and filters.category != "all":
        if filters.category == "pmr":
            query["$or"] = [
                {"features": {"$regex": "accessible", "$options": "i"}},
                {"location": {"$regex": "ste-luce", "$options": "i"}},
                {"guests": {"$lte": 4}}
            ]
        else:
            query["category"] = filters.category
    
    if filters.min_price or filters.max_price:
        price_query = {}
        if filters.min_price:
            price_query["$gte"] = filters.min_price
        if filters.max_price:
            price_query["$lte"] = filters.max_price
        query["price"] = price_query
    
    try:
        villas = await db.villas.find(query).to_list(1000)
        return villas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la recherche: {e}")

@app.post("/api/reservations", response_model=dict)
async def create_reservation(reservation: ReservationCreate):
    """Créer une nouvelle réservation"""
    try:
        # Vérifier que la villa existe
        villa = await db.villas.find_one({"id": reservation.villa_id})
        if not villa:
            raise HTTPException(status_code=404, detail="Villa non trouvée")
        
        # Créer la réservation
        reservation_data = {
            "id": str(uuid.uuid4()),
            "villa_id": reservation.villa_id,
            "villa_name": villa["name"],
            "customer_name": reservation.customer_name,
            "customer_email": reservation.customer_email,
            "customer_phone": reservation.customer_phone,
            "checkin_date": reservation.checkin_date,
            "checkout_date": reservation.checkout_date,
            "guests_count": reservation.guests_count,
            "message": reservation.message,
            "total_price": reservation.total_price,
            "status": "pending",
            "created_at": datetime.utcnow()
        }
        
        result = await db.reservations.insert_one(reservation_data)
        
        if result.inserted_id:
            return {
                "success": True,
                "reservation_id": reservation_data["id"],
                "message": "Réservation créée avec succès",
                "villa_name": villa["name"]
            }
        else:
            raise HTTPException(status_code=500, detail="Erreur lors de la création de la réservation")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {e}")

@app.get("/api/reservations/{reservation_id}")
async def get_reservation(reservation_id: str):
    """Récupérer une réservation"""
    reservation = await db.reservations.find_one({"id": reservation_id})
    if not reservation:
        raise HTTPException(status_code=404, detail="Réservation non trouvée")
    return reservation

@app.get("/api/reservations/customer/{email}")
async def get_customer_reservations(email: str):
    """Récupérer les réservations d'un client"""
    reservations = await db.reservations.find({"customer_email": email}).to_list(1000)
    return reservations

@app.put("/api/reservations/{reservation_id}/status")
async def update_reservation_status(reservation_id: str, status: str):
    """Mettre à jour le statut d'une réservation"""
    valid_statuses = ["pending", "confirmed", "cancelled"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Statut invalide")
    
    result = await db.reservations.update_one(
        {"id": reservation_id},
        {"$set": {"status": status}}
    )
    
    if result.modified_count:
        return {"success": True, "message": "Statut mis à jour"}
    else:
        raise HTTPException(status_code=404, detail="Réservation non trouvée")

@app.get("/api/stats/dashboard")
async def get_dashboard_stats():
    """Statistiques pour le tableau de bord admin"""
    try:
        total_villas = await db.villas.count_documents({})
        total_reservations = await db.reservations.count_documents({})
        pending_reservations = await db.reservations.count_documents({"status": "pending"})
        confirmed_reservations = await db.reservations.count_documents({"status": "confirmed"})
        
        # Revenus du mois (approximatif)
        start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        monthly_reservations = await db.reservations.find({
            "created_at": {"$gte": start_of_month},
            "status": {"$in": ["confirmed", "pending"]}
        }).to_list(1000)
        
        monthly_revenue = sum([res.get("total_price", 0) for res in monthly_reservations])
        
        return {
            "total_villas": total_villas,
            "total_reservations": total_reservations,
            "pending_reservations": pending_reservations,
            "confirmed_reservations": confirmed_reservations,
            "monthly_revenue": monthly_revenue,
            "monthly_reservations": len(monthly_reservations)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur statistiques: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)