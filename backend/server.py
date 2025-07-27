from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional
import os
from datetime import datetime, timedelta
import uuid
import json
from dotenv import load_dotenv
import hashlib
import secrets
from jose import JWTError, jwt
import bcrypt
import bleach
import re
import time
from collections import defaultdict
# PHASE 1 - SÉCURITÉ CRITIQUE
import pyotp
import qrcode
import io
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from cryptography.fernet import Fernet

load_dotenv()

# =============================================================================
# MIDDLEWARE DE SÉCURITÉ CRITIQUE
# =============================================================================

# Rate limiting pour protection brute force
request_counts = defaultdict(lambda: {'count': 0, 'reset_time': time.time()})
# Suivi des tentatives de login échouées
failed_login_attempts = defaultdict(lambda: {'count': 0, 'reset_time': time.time()})

class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        
        # 1. Protection Path Traversal
        path = request.url.path
        if ".." in path or "%2e%2e" in path.lower() or "etc/passwd" in path.lower():
            raise HTTPException(status_code=400, detail="Invalid path detected")
        
        # 2. Rate limiting basique
        current_time = time.time()
        if current_time - request_counts[client_ip]['reset_time'] > 60:
            request_counts[client_ip] = {'count': 0, 'reset_time': current_time}
        
        request_counts[client_ip]['count'] += 1
        
        # Limiter à 60 requêtes par minute par IP
        if request_counts[client_ip]['count'] > 60:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        # 3. Headers de sécurité
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response

# Utilitaires de sécurité
def sanitize_input(text: str) -> str:
    """Nettoie les entrées utilisateur contre XSS"""
    if not text:
        return text
    # Supprime/échappe les balises HTML et scripts
    cleaned = bleach.clean(text, tags=[], attributes={}, strip=True)
    return cleaned.strip()

def hash_password(password: str) -> str:
    """Hash sécurisé du mot de passe avec bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie le mot de passe"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def validate_password_strength(password: str) -> bool:
    """Valide la force du mot de passe"""
    if len(password) < 8:
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password):
        return False
    return True

# Configuration sécurité - PHASE 1 SÉCURISÉE
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-here-change-in-production")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
MEMBER_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 jours pour les membres

# Admin credentials sécurisés - PHASE 1
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "khanelconcept2025")
ADMIN_SECRET_KEY = os.getenv("ADMIN_SECRET_KEY", "admin-secret-key-change-in-production")
ADMIN_2FA_SECRET = os.getenv("ADMIN_2FA_SECRET", "your-2fa-secret-key-here")

# Données admin sécurisées
ADMIN_USERS = {
    ADMIN_USERNAME: {
        "username": ADMIN_USERNAME,
        "hashed_password": hashlib.sha256(ADMIN_PASSWORD.encode()).hexdigest(),
        "role": "admin",
        "2fa_secret": ADMIN_2FA_SECRET
    }
}

# Niveaux de membre et seuils de points
MEMBER_LEVELS = {
    "Découvreur": {"min_points": 0, "max_points": 499, "benefits": ["Avantages de base", "Support standard"]},
    "Explorateur": {"min_points": 500, "max_points": 1499, "benefits": ["Check-in prioritaire", "Late checkout", "WiFi premium"]},
    "Aventurier": {"min_points": 1500, "max_points": 2999, "benefits": ["Surclassement gratuit", "Minibar offert", "Room service 24/7"]},
    "Légende": {"min_points": 3000, "max_points": float('inf'), "benefits": ["Conciergerie 24/7", "Transferts VIP", "Expériences privées"]}
}

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

# ⚠️ MIDDLEWARE DE SÉCURITÉ OBLIGATOIRE
app.add_middleware(SecurityMiddleware)

# Configuration MongoDB
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/khanelconcept")
client = AsyncIOMotorClient(MONGO_URL)
db = client.khanelconcept

# ========== MODELS ==========

# ========== MEMBER MODELS ==========

class MemberRegister(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    phone: str
    password: str
    birthDate: Optional[str] = None
    acceptTerms: bool = True
    
    @validator('firstName', 'lastName')
    def validate_names(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('Le nom doit contenir au moins 2 caractères')
        if len(v.strip()) > 50:
            raise ValueError('Le nom ne peut dépasser 50 caractères')
        # Supprimer les caractères potentiellement dangereux
        sanitized = sanitize_input(v.strip())
        if not re.match(r"^[a-zA-ZÀ-ÿ\s\-'\.]*$", sanitized):
            raise ValueError('Le nom contient des caractères non autorisés')
        return sanitized
    
    @validator('phone')
    def validate_phone(cls, v):
        if not v:
            raise ValueError('Le téléphone est requis')
        # Supprimer espaces et caractères spéciaux
        phone_clean = re.sub(r'[^\d\+]', '', v)
        # Vérifier format international
        if not re.match(r'^\+[\d]{10,15}$', phone_clean):
            raise ValueError('Format téléphone invalide (ex: +596123456789)')
        return phone_clean
    
    @validator('password')
    def validate_password(cls, v):
        if not v:
            raise ValueError('Le mot de passe est requis')
        if not validate_password_strength(v):
            raise ValueError('Mot de passe faible: 8+ caractères, majuscule, minuscule, chiffre, caractère spécial requis')
        # Vérifier mots de passe communs
        weak_passwords = ['password', 'admin', '123456', 'password123', 'azerty', 'qwerty']
        if v.lower() in weak_passwords:
            raise ValueError('Mot de passe trop commun, choisissez un mot de passe plus sûr')
        return v
    
    @validator('acceptTerms')
    def validate_terms(cls, v):
        if not v:
            raise ValueError('L\'acceptation des conditions générales est obligatoire')
        return v

class MemberLogin(BaseModel):
    email: EmailStr
    password: str
    remember: bool = False

class Member(BaseModel):
    id: Optional[str] = None
    firstName: str
    lastName: str
    email: EmailStr
    phone: str
    birthDate: Optional[str] = None
    level: str = "Découvreur"  # Découvreur, Explorateur, Aventurier, Légende
    points: int = 0
    joinDate: str
    isVerified: bool = False
    isActive: bool = True
    avatar: Optional[str] = None
    preferences: Optional[dict] = {}

class MemberProfile(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    phone: Optional[str] = None
    birthDate: Optional[str] = None
    avatar: Optional[str] = None
    preferences: Optional[dict] = None

class MemberNotification(BaseModel):
    id: Optional[str] = None
    memberId: str
    type: str  # reservation, loyalty, system, promotion
    title: str
    message: str
    isRead: bool = False
    createdAt: datetime
    actionUrl: Optional[str] = None

class LoyaltyTransaction(BaseModel):
    id: Optional[str] = None
    memberId: str
    type: str  # earn, spend, bonus
    amount: int
    description: str
    reference: Optional[str] = None  # reservation_id, etc.
    createdAt: datetime

class MemberWishlist(BaseModel):
    id: Optional[str] = None
    memberId: str
    villaId: str
    villaName: str
    addedAt: datetime
    notes: Optional[str] = None

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

class AdminLogin(BaseModel):
    username: str
    password: str
    totp_code: Optional[str] = None  # Code 2FA optionnel

class AdminSetup2FA(BaseModel):
    password: str  # Mot de passe pour vérifier l'identité

class AdminEnable2FA(BaseModel):
    totp_code: str  # Code pour valider la 2FA

class AdminDisable2FA(BaseModel):
    password: str
    totp_code: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenVerify(BaseModel):
    token: str

class VillaCreate(BaseModel):
    name: str
    location: str
    price: float
    guests: int
    guests_detail: str
    features: str
    category: str
    description: Optional[str] = ""
    amenities: Optional[List[str]] = []

class VillaUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    price: Optional[float] = None
    guests: Optional[int] = None
    guests_detail: Optional[str] = None
    features: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    amenities: Optional[List[str]] = None

class ReservationStatusUpdate(BaseModel):
    status: str

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
    },
    {
        "id": "5",
        "name": "Villa Sunset Paradise",
        "location": "Sainte-Anne",
        "price": 950.0,
        "guests": 8,
        "guests_detail": "8 personnes + 12 invités",
        "features": "Piscine privée 8x4m, vue mer",
        "category": "sejour",
        "image": "/images/villa_sunset_paradise.jpg",
        "gallery": ["/images/villa_sunset_paradise.jpg"],
        "fallback_icon": "🌅",
        "amenities": ["Piscine privée", "Vue mer", "Cuisine équipée", "WiFi", "Climatisation", "Terrasse"],
        "description": "Villa exceptionnelle avec vue imprenable sur le coucher de soleil et piscine privée."
    },
    {
        "id": "6",
        "name": "Villa Océan Bleu",
        "location": "Les Trois-Îlets",
        "price": 1200.0,
        "guests": 10,
        "guests_detail": "10 personnes + 15 invités",
        "features": "Accès direct plage, piscine à débordement",
        "category": "sejour",
        "image": "/images/villa_ocean_bleu.jpg",
        "gallery": ["/images/villa_ocean_bleu.jpg"],
        "fallback_icon": "🌊",
        "amenities": ["Accès plage", "Piscine à débordement", "Cuisine moderne", "WiFi", "Climatisation", "Jardin tropical"],
        "description": "Villa de prestige avec accès direct à la plage et piscine à débordement face à la mer."
    },
    {
        "id": "7",
        "name": "Villa Tropicale Zen",
        "location": "Sainte-Luce",
        "price": 780.0,
        "guests": 6,
        "guests_detail": "6 personnes + 8 invités",
        "features": "Jardin tropical, spa extérieur",
        "category": "sejour",
        "image": "/images/villa_tropicale_zen.jpg",
        "gallery": ["/images/villa_tropicale_zen.jpg"],
        "fallback_icon": "🌴",
        "amenities": ["Jardin tropical", "Spa extérieur", "Piscine", "Cuisine équipée", "WiFi", "Climatisation"],
        "description": "Havre de paix au cœur d'un jardin tropical luxuriant avec espace spa."
    },
    {
        "id": "8",
        "name": "Villa Carbet Deluxe",
        "location": "Le Carbet",
        "price": 1100.0,
        "guests": 8,
        "guests_detail": "8 personnes + 12 invités",
        "features": "Vue montagne Pelée, piscine chauffée",
        "category": "sejour",
        "image": "/images/villa_carbet_deluxe.jpg",
        "gallery": ["/images/villa_carbet_deluxe.jpg"],
        "fallback_icon": "🏔️",
        "amenities": ["Vue montagne", "Piscine chauffée", "Grande terrasse", "Cuisine moderne", "WiFi", "Climatisation"],
        "description": "Villa de luxe avec vue spectaculaire sur la montagne Pelée et piscine chauffée."
    },
    {
        "id": "9",
        "name": "Appartement Marina Fort-de-France",
        "location": "Fort-de-France Marina",
        "price": 320.0,
        "guests": 4,
        "guests_detail": "4 personnes max",
        "features": "Vue marina, balcon panoramique",
        "category": "special",
        "image": "/images/appartement_marina_fdf.jpg",
        "gallery": ["/images/appartement_marina_fdf.jpg"],
        "fallback_icon": "⛵",
        "amenities": ["Vue marina", "Balcon", "Cuisine équipée", "WiFi", "Climatisation", "Parking"],
        "description": "Appartement moderne avec vue imprenable sur la marina et les bateaux."
    },
    {
        "id": "10",
        "name": "Villa Diamant Prestige",
        "location": "Le Diamant",
        "price": 1400.0,
        "guests": 12,
        "guests_detail": "12 personnes + 20 invités",
        "features": "Vue Rocher du Diamant, piscine infinity",
        "category": "fete",
        "image": "/images/villa_diamant_prestige.jpg",
        "gallery": ["/images/villa_diamant_prestige.jpg"],
        "fallback_icon": "💎",
        "amenities": ["Vue Rocher du Diamant", "Piscine infinity", "Grande cuisine", "WiFi", "Climatisation", "Barbecue"],
        "description": "Villa de prestige avec vue exceptionnelle sur le célèbre Rocher du Diamant."
    },
    {
        "id": "11",
        "name": "Villa Bord de Mer Tartane",
        "location": "La Trinité - Tartane",
        "price": 890.0,
        "guests": 6,
        "guests_detail": "6 personnes + 10 invités",
        "features": "Pieds dans l'eau, piscine naturelle",
        "category": "sejour",
        "image": "/images/villa_tartane.jpg",
        "gallery": ["/images/villa_tartane.jpg"],
        "fallback_icon": "🏖️",
        "amenities": ["Accès direct mer", "Piscine naturelle", "Cuisine créole", "WiFi", "Climatisation", "Kayaks"],
        "description": "Villa authentique les pieds dans l'eau avec accès à une piscine naturelle."
    },
    {
        "id": "12",
        "name": "Studio Marin Cosy",
        "location": "Le Marin",
        "price": 280.0,
        "guests": 2,
        "guests_detail": "2 personnes (couple)",
        "features": "Port de plaisance, terrasse privée",
        "category": "special",
        "image": "/images/studio_marin_cosy.jpg",
        "gallery": ["/images/studio_marin_cosy.jpg"],
        "fallback_icon": "⚓",
        "amenities": ["Vue port", "Terrasse privée", "Kitchenette", "WiFi", "Climatisation"],
        "description": "Studio douillet avec vue sur le port de plaisance du Marin."
    },
    {
        "id": "13",
        "name": "Villa Anses d'Arlet",
        "location": "Les Anses d'Arlet",
        "price": 1050.0,
        "guests": 8,
        "guests_detail": "8 personnes + 12 invités",
        "features": "Proche Grande Anse, piscine avec bar",
        "category": "sejour",
        "image": "/images/villa_anses_arlet.jpg",
        "gallery": ["/images/villa_anses_arlet.jpg"],
        "fallback_icon": "🥥",
        "amenities": ["Proche plage", "Piscine avec bar", "Cuisine tropicale", "WiFi", "Climatisation", "Hamacs"],
        "description": "Villa caribéenne authentique à proximité de la magnifique Grande Anse."
    },
    {
        "id": "14",
        "name": "Penthouse Schoelcher Vue Mer",
        "location": "Schoelcher",
        "price": 620.0,
        "guests": 6,
        "guests_detail": "6 personnes max",
        "features": "Dernier étage, terrasse 360°",
        "category": "special",
        "image": "/images/penthouse_schoelcher.jpg",
        "gallery": ["/images/penthouse_schoelcher.jpg"],
        "fallback_icon": "🏙️",
        "amenities": ["Vue panoramique", "Terrasse 360°", "Cuisine moderne", "WiFi", "Climatisation", "Ascenseur"],
        "description": "Penthouse moderne avec vue panoramique exceptionnelle sur la baie de Fort-de-France."
    },
    {
        "id": "15",
        "name": "Villa Rivière-Pilote Charme",
        "location": "Rivière-Pilote",
        "price": 720.0,
        "guests": 6,
        "guests_detail": "6 personnes + 8 invités",
        "features": "Architecture créole, jardin centenaire",
        "category": "sejour",
        "image": "/images/villa_riviere_pilote.jpg",
        "gallery": ["/images/villa_riviere_pilote.jpg"],
        "fallback_icon": "🏛️",
        "amenities": ["Architecture créole", "Jardin centenaire", "Piscine traditionnelle", "WiFi", "Climatisation"],
        "description": "Villa de charme à l'architecture créole authentique dans un jardin centenaire."
    },
    {
        "id": "16",
        "name": "Villa François Moderne",
        "location": "Le François",
        "price": 980.0,
        "guests": 8,
        "guests_detail": "8 personnes + 12 invités",
        "features": "Fonds blancs, excursions incluses",
        "category": "sejour",
        "image": "/images/villa_francois_moderne.jpg",
        "gallery": ["/images/villa_francois_moderne.jpg"],
        "fallback_icon": "🛥️",
        "amenities": ["Accès fonds blancs", "Excursions incluses", "Piscine", "Cuisine équipée", "WiFi", "Climatisation"],
        "description": "Villa moderne avec accès privilégié aux fameux fonds blancs du François."
    },
    {
        "id": "17",
        "name": "Studio Ducos Pratique",
        "location": "Ducos Centre",
        "price": 250.0,
        "guests": 2,
        "guests_detail": "2 personnes max",
        "features": "Centre-ville, tous commerces",
        "category": "special",
        "image": "/images/studio_ducos.jpg",
        "gallery": ["/images/studio_ducos.jpg"],
        "fallback_icon": "🛍️",
        "amenities": ["Centre-ville", "Commerces proches", "Kitchenette", "WiFi", "Climatisation"],
        "description": "Studio pratique en centre-ville avec tous les commerces à proximité."
    },
    {
        "id": "18",
        "name": "Villa Sainte-Marie Familiale",
        "location": "Sainte-Marie",
        "price": 850.0,
        "guests": 8,
        "guests_detail": "8 personnes + 10 invités",
        "features": "Proche distillerie, piscine familiale",
        "category": "sejour",
        "image": "/images/villa_sainte_marie.jpg",
        "gallery": ["/images/villa_sainte_marie.jpg"],
        "fallback_icon": "🥃",
        "amenities": ["Proche distilleries", "Piscine familiale", "Grand jardin", "WiFi", "Climatisation", "Barbecue"],
        "description": "Villa familiale idéalement située près des distilleries de rhum de Sainte-Marie."
    },
    {
        "id": "19",
        "name": "Villa Marigot Exclusive",
        "location": "Le Marigot",
        "price": 1180.0,
        "guests": 10,
        "guests_detail": "10 personnes + 15 invités",
        "features": "Plage privée, piscine olympique",
        "category": "fete",
        "image": "/images/villa_marigot_exclusive.jpg",
        "gallery": ["/images/villa_marigot_exclusive.jpg"],
        "fallback_icon": "🏊‍♀️",
        "amenities": ["Plage privée", "Piscine olympique", "Cuisine professionnelle", "WiFi", "Climatisation", "Staff inclus"],
        "description": "Villa exclusive avec plage privée et piscine olympique, staff de service inclus."
    },
    {
        "id": "20",
        "name": "Bungalow Trenelle Nature",
        "location": "Trenelle, Trinité",
        "price": 420.0,
        "guests": 4,
        "guests_detail": "4 personnes max",
        "features": "Écotourisme, randonnées",
        "category": "special",
        "image": "/images/bungalow_trenelle.jpg",
        "gallery": ["/images/bungalow_trenelle.jpg"],
        "fallback_icon": "🦋",
        "amenities": ["Nature préservée", "Randonnées", "Petit bassin", "WiFi", "Ventilation naturelle"],
        "description": "Bungalow écologique en pleine nature pour les amateurs d'écotourisme."
    },
    {
        "id": "21",
        "name": "Villa Grand Luxe Pointe du Bout",
        "location": "Pointe du Bout, Trois-Îlets",
        "price": 1800.0,
        "guests": 14,
        "guests_detail": "14 personnes + 25 invités",
        "features": "Villa de prestige, service conciergerie",
        "category": "fete",
        "image": "/images/villa_grand_luxe_pointe.jpg",
        "gallery": ["/images/villa_grand_luxe_pointe.jpg"],
        "fallback_icon": "👑",
        "amenities": ["Service conciergerie", "Piscine à débordement", "Cuisine chef", "WiFi", "Climatisation", "Spa privé"],
        "description": "Villa de grand luxe avec service conciergerie et toutes les prestations haut de gamme."
    },
    {
        "id": "22",
        "name": "Villa F6 Petit Macabou",
        "location": "Petit Macabou au Vauclin",
        "price": 2000.0,
        "guests": 13,
        "guests_detail": "10 à 13 personnes (14 max)",
        "features": "3 chambres climatisées, 1 mezzanine, 2 studios aux extrémités",
        "category": "fete",
        "image": "/images/Villa_F6_Petit_Macabou/02_salle_de_bain.jpg",
        "gallery": [
            "/images/Villa_F6_Petit_Macabou/02_salle_de_bain.jpg",
            "/images/Villa_F6_Petit_Macabou/03_chambre_studio.jpg",
            "/images/Villa_F6_Petit_Macabou/04_salon_mezzanine.jpg",
            "/images/Villa_F6_Petit_Macabou/05_cuisine_moderne.jpg",
            "/images/Villa_F6_Petit_Macabou/06_terrasse_couverte.jpg",
            "/images/Villa_F6_Petit_Macabou/07_terrasse_piscine.jpg",
            "/images/Villa_F6_Petit_Macabou/10_vue_aerienne_jour.jpg"
        ],
        "fallback_icon": "🎊",
        "amenities": ["3 chambres climatisées", "1 mezzanine", "2 studios aux extrémités", "Piscine", "Terrasse couverte", "WiFi", "Climatisation", "Cuisine moderne"],
        "description": "Villa F6 exceptionnelle à Petit Macabou avec 3 chambres climatisées avec salle d'eau attenante, 1 mezzanine et 2 studios aux extrémités. Fête autorisée de 09h à 19h, 30 convives max. Possibilité de louer en supplément les 3 bungalows avec SDB à 5 punch chacun situés sur le même terrain. Piscine et fêtes jusqu'à 150 convives."
    }
]

# ========== STARTUP ==========

@app.on_event("startup")
async def startup_db_client():
    """Initialiser la base de données avec les données des villas"""
    try:
        # Supprimer toutes les villas existantes et recharger les nouvelles données
        await db.villas.delete_many({})
        
        # Insérer les nouvelles données des villas (21 villas)
        await db.villas.insert_many(villas_data)
        print(f"✅ {len(villas_data)} villas ajoutées à la base de données")
            
        # Créer les index
        await db.villas.create_index("id", unique=True)
        await db.reservations.create_index("villa_id")
        await db.reservations.create_index("customer_email")
        
        # Index pour les membres
        await db.members.create_index("email", unique=True)
        await db.members.create_index("id", unique=True)
        await db.member_notifications.create_index("memberId")
        await db.loyalty_transactions.create_index("memberId")
        await db.member_wishlist.create_index("memberId")
        await db.member_wishlist.create_index([("memberId", 1), ("villaId", 1)], unique=True)
        
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
            # Vérifier si c'est un membre et ajouter des points
            member = await db.members.find_one({"email": reservation.customer_email})
            if member:
                # Ajouter des points (1 point par euro dépensé)
                points_earned = int(reservation.total_price)
                await add_loyalty_points(
                    member["id"],
                    points_earned,
                    f"Réservation villa {villa['name']} - {reservation.checkin_date}",
                    reservation_data["id"]
                )
                
                # Notification de réservation
                notification = {
                    "id": str(uuid.uuid4()),
                    "memberId": member["id"],
                    "type": "reservation",
                    "title": "✅ Réservation confirmée",
                    "message": f"Votre réservation pour {villa['name']} est confirmée. Vous avez gagné {points_earned} points !",
                    "isRead": False,
                    "createdAt": datetime.utcnow(),
                    "actionUrl": f"/reservations/{reservation_data['id']}"
                }
                await db.member_notifications.insert_one(notification)
            
            return {
                "success": True,
                "reservation_id": reservation_data["id"],
                "message": "Réservation créée avec succès",
                "villa_name": villa["name"],
                "points_earned": int(reservation.total_price) if member else 0
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

# ========== FONCTIONS DE SÉCURITÉ PHASE 1 ==========

def generate_2fa_secret():
    """Générer un secret 2FA"""
    return pyotp.random_base32()

def generate_qr_code(username: str, secret: str):
    """Générer un QR code pour la 2FA"""
    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=username,
        issuer_name="KhanelConcept Admin"
    )
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(totp_uri)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"

def verify_2fa_code(secret: str, code: str):
    """Vérifier un code 2FA"""
    totp = pyotp.TOTP(secret)
    return totp.verify(code, valid_window=1)

def send_security_alert_email(admin_username: str, action: str, ip_address: str):
    """Envoyer une alerte de sécurité par email"""
    try:
        msg = MIMEMultipart()
        msg['From'] = os.getenv("EMAIL_FROM", "security@khanelconcept.com")
        msg['To'] = f"{admin_username}@khanelconcept.com"
        msg['Subject'] = f"🔐 Alerte Sécurité KhanelConcept - {action}"
        
        body = f"""
        Alerte de sécurité :
        
        Action : {action}
        Utilisateur : {admin_username}
        Adresse IP : {ip_address}
        Heure : {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
        
        Si ce n'est pas vous, veuillez immédiatement changer votre mot de passe.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Configuration SMTP
        smtp_server = os.getenv("SMTP_HOST", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(msg['From'], os.getenv("EMAIL_PASSWORD", ""))
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Alerte sécurité envoyée à {admin_username}")
        
    except Exception as e:
        print(f"❌ Erreur envoi email sécurité: {e}")

def log_security_event(event_type: str, username: str, ip_address: str, success: bool, details: str = ""):
    """Logger les événements de sécurité - PHASE 1"""
    timestamp = datetime.utcnow().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "event_type": event_type,
        "username": username,
        "ip_address": ip_address,
        "success": success,
        "details": details
    }
    
    # Log dans le fichier
    log_file = "/var/log/khanelconcept_security.log"
    try:
        with open(log_file, "a") as f:
            f.write(f"{json.dumps(log_entry)}\n")
    except:
        pass
    
    # Log dans la console
    status = "✅" if success else "❌"
    print(f"{status} SECURITY: {event_type} - {username} from {ip_address} - {details}")

# ========== FONCTIONS D'AUTHENTIFICATION SÉCURISÉES ==========

def verify_admin_password(plain_password, hashed_password):
    """Vérifier le mot de passe admin (SHA256)"""
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

def authenticate_user(username: str, password: str):
    """Authentifier un utilisateur admin"""
    user = ADMIN_USERS.get(username)
    if not user:
        return False
    if not verify_admin_password(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Créer un token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_member_token(member_data: dict):
    """Créer un token JWT pour membre"""
    expire = timedelta(minutes=MEMBER_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": member_data["email"],
        "member_id": member_data["id"],
        "type": "member"
    }
    return create_access_token(to_encode, expire)

def verify_token(token: str):
    """Vérifier un token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return payload
    except JWTError:
        return None

def get_member_level(points: int):
    """Déterminer le niveau d'un membre basé sur ses points"""
    for level_name, level_data in MEMBER_LEVELS.items():
        if level_data["min_points"] <= points <= level_data["max_points"]:
            return level_name
    return "Découvreur"

async def add_loyalty_points(member_id: str, amount: int, description: str, reference: str = None):
    """Ajouter des points de fidélité à un membre"""
    try:
        # Ajouter la transaction
        transaction = {
            "id": str(uuid.uuid4()),
            "memberId": member_id,
            "type": "earn",
            "amount": amount,
            "description": description,
            "reference": reference,
            "createdAt": datetime.utcnow()
        }
        await db.loyalty_transactions.insert_one(transaction)
        
        # Mettre à jour les points du membre
        member = await db.members.find_one({"id": member_id})
        if member:
            new_points = member.get("points", 0) + amount
            new_level = get_member_level(new_points)
            
            # Vérifier si le niveau a changé
            old_level = member.get("level", "Découvreur")
            level_changed = old_level != new_level
            
            await db.members.update_one(
                {"id": member_id},
                {
                    "$set": {
                        "points": new_points,
                        "level": new_level
                    }
                }
            )
            
            # Notifier si niveau changé
            if level_changed:
                notification = {
                    "id": str(uuid.uuid4()),
                    "memberId": member_id,
                    "type": "loyalty",
                    "title": f"🎉 Nouveau niveau atteint !",
                    "message": f"Félicitations ! Vous êtes maintenant {new_level} avec {new_points} points.",
                    "isRead": False,
                    "createdAt": datetime.utcnow(),
                    "actionUrl": "/dashboard"
                }
                await db.member_notifications.insert_one(notification)
            
            return {"success": True, "new_points": new_points, "new_level": new_level, "level_changed": level_changed}
        
    except Exception as e:
        print(f"Erreur ajout points: {e}")
        return {"success": False, "error": str(e)}

# ========== ROUTES D'AUTHENTIFICATION ==========

@app.post("/api/admin/login", response_model=Token)
async def admin_login(login_data: AdminLogin):
    """Connexion administrateur"""
    user = authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"], "role": user["role"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/admin/verify-token")
async def verify_admin_token(token_data: TokenVerify):
    """Vérifier un token admin"""
    payload = verify_token(token_data.token)
    if payload is None or payload.get("type") == "member":
        raise HTTPException(status_code=401, detail="Token admin invalide")
    return {"valid": True, "username": payload.get("sub")}

# ========== ROUTES D'AUTHENTIFICATION MEMBRE ==========

@app.post("/api/members/register")
async def member_register(member_data: MemberRegister):
    """Inscription d'un nouveau membre"""
    try:
        # Vérifier si l'email existe déjà
        existing_member = await db.members.find_one({"email": member_data.email})
        if existing_member:
            raise HTTPException(status_code=400, detail="Un compte existe déjà avec cet email")
        
        # Créer le nouveau membre
        new_member = {
            "id": str(uuid.uuid4()),
            "firstName": member_data.firstName,
            "lastName": member_data.lastName,
            "email": member_data.email,
            "phone": member_data.phone,
            "password": hash_password(member_data.password),
            "birthDate": member_data.birthDate,
            "level": "Découvreur",
            "points": 100,  # Bonus d'inscription
            "joinDate": datetime.utcnow().isoformat(),
            "isVerified": False,
            "isActive": True,
            "avatar": None,
            "preferences": {
                "notifications": {
                    "email": True,
                    "sms": False,
                    "push": True
                },
                "marketing": True,
                "language": "fr"
            }
        }
        
        # Insérer en base
        result = await db.members.insert_one(new_member)
        
        if result.inserted_id:
            # Ajouter la transaction de bonus d'inscription
            await add_loyalty_points(
                new_member["id"], 
                100, 
                "Bonus d'inscription - Bienvenue chez KhanelConcept !", 
                "registration"
            )
            
            # Créer notification de bienvenue
            welcome_notification = {
                "id": str(uuid.uuid4()),
                "memberId": new_member["id"],
                "type": "system",
                "title": "🌴 Bienvenue chez KhanelConcept !",
                "message": f"Bonjour {member_data.firstName} ! Votre compte a été créé avec succès. Vous avez reçu 100 points de bienvenue.",
                "isRead": False,
                "createdAt": datetime.utcnow(),
                "actionUrl": "/dashboard"
            }
            await db.member_notifications.insert_one(welcome_notification)
            
            # Créer le token
            token = create_member_token(new_member)
            
            # Retourner les infos (sans le mot de passe et _id MongoDB)
            new_member.pop("password", None)
            new_member.pop("_id", None)  # Remove MongoDB ObjectId
            return {
                "success": True,
                "message": "Compte créé avec succès",
                "member": new_member,
                "token": token
            }
        else:
            raise HTTPException(status_code=500, detail="Erreur lors de la création du compte")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {e}")

@app.post("/api/members/login")
async def member_login(login_data: MemberLogin, request: Request):
    """Connexion d'un membre avec protection brute force"""
    try:
        client_ip = request.client.host if request.client else "unknown"
        email_key = f"{login_data.email}_{client_ip}"
        
        # 🔒 PROTECTION BRUTE FORCE
        current_time = time.time()
        if current_time - failed_login_attempts[email_key]['reset_time'] > 900:  # Reset après 15 min
            failed_login_attempts[email_key] = {'count': 0, 'reset_time': current_time}
        
        # Bloquer après 5 tentatives échouées
        if failed_login_attempts[email_key]['count'] >= 5:
            remaining_time = int(900 - (current_time - failed_login_attempts[email_key]['reset_time']))
            raise HTTPException(
                status_code=429, 
                detail=f"Trop de tentatives échouées. Réessayez dans {remaining_time//60} minutes"
            )
        
        # Rechercher le membre
        member = await db.members.find_one({"email": login_data.email})
        if not member:
            # Incrémenter les tentatives échouées
            failed_login_attempts[email_key]['count'] += 1
            raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
        
        # Vérifier le mot de passe
        if not verify_password(login_data.password, member["password"]):
            # Incrémenter les tentatives échouées
            failed_login_attempts[email_key]['count'] += 1
            raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
        
        # Vérifier que le compte est actif
        if not member.get("isActive", True):
            raise HTTPException(status_code=401, detail="Compte désactivé")
        
        # LOGIN RÉUSSI - Reset les tentatives échouées
        failed_login_attempts[email_key] = {'count': 0, 'reset_time': current_time}
        
        # Créer le token
        token = create_member_token(member)
        
        # Mettre à jour la dernière connexion
        await db.members.update_one(
            {"id": member["id"]},
            {"$set": {"lastLogin": datetime.utcnow().isoformat()}}
        )
        
        # 📊 LOG DE SÉCURITÉ
        print(f"🔐 LOGIN SUCCESS: {login_data.email} from {client_ip} at {datetime.utcnow()}")
        
        # Retourner les infos (sans le mot de passe et _id MongoDB)
        member.pop("password", None)
        member.pop("_id", None)  # Remove MongoDB ObjectId
        return {
            "success": True,
            "message": "Connexion réussie",
            "member": member,
            "token": token
        }
        
    except HTTPException:
        # LOG DE SÉCURITÉ pour tentatives échouées
        client_ip = request.client.host if request.client else "unknown"
        print(f"🚨 LOGIN FAILED: {login_data.email} from {client_ip} at {datetime.utcnow()}")
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {e}")

@app.post("/api/members/verify-token")
async def verify_member_token(token_data: TokenVerify):
    """Vérifier un token membre"""
    try:
        payload = verify_token(token_data.token)
        if payload is None or payload.get("type") != "member":
            raise HTTPException(status_code=401, detail="Token invalide")
        
        # Vérifier que le membre existe toujours
        member = await db.members.find_one({"id": payload.get("member_id")})
        if not member or not member.get("isActive", True):
            raise HTTPException(status_code=401, detail="Membre introuvable ou inactif")
        
        member.pop("password", None)
        member.pop("_id", None)  # Remove MongoDB ObjectId
        return {"valid": True, "member": member}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token invalide")

# ========== ROUTES MEMBRE PROTÉGÉES ==========

@app.get("/api/members/profile/{member_id}")
async def get_member_profile(member_id: str):
    """Récupérer le profil d'un membre"""
    try:
        member = await db.members.find_one({"id": member_id})
        if not member:
            raise HTTPException(status_code=404, detail="Membre introuvable")
        
        member.pop("password", None)
        member.pop("_id", None)  # Remove MongoDB ObjectId
        return member
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {e}")

@app.put("/api/members/profile/{member_id}")
async def update_member_profile(member_id: str, profile_data: MemberProfile):
    """Mettre à jour le profil d'un membre"""
    try:
        # Construire les données à mettre à jour
        update_data = {k: v for k, v in profile_data.dict().items() if v is not None}
        
        if update_data:
            result = await db.members.update_one(
                {"id": member_id},
                {"$set": update_data}
            )
            
            if result.modified_count:
                # Récupérer le profil mis à jour
                updated_member = await db.members.find_one({"id": member_id})
                updated_member.pop("password", None)
                updated_member.pop("_id", None)  # Remove MongoDB ObjectId
                return {"success": True, "member": updated_member}
            else:
                raise HTTPException(status_code=404, detail="Membre introuvable")
        else:
            raise HTTPException(status_code=400, detail="Aucune donnée à mettre à jour")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {e}")

@app.get("/api/members/{member_id}/reservations")
async def get_member_reservations(member_id: str):
    """Récupérer les réservations d'un membre"""
    try:
        # Récupérer le membre pour obtenir l'email
        member = await db.members.find_one({"id": member_id})
        if not member:
            raise HTTPException(status_code=404, detail="Membre introuvable")
        
        # Récupérer les réservations
        reservations = await db.reservations.find(
            {"customer_email": member["email"]}, 
            {"_id": 0}
        ).sort("created_at", -1).to_list(100)
        
        # Enrichir avec les infos des villas
        for reservation in reservations:
            villa = await db.villas.find_one({"id": reservation["villa_id"]})
            if villa:
                reservation["villa_info"] = {
                    "name": villa["name"],
                    "location": villa["location"],
                    "image": villa["image"],
                    "price": villa["price"]
                }
        
        return reservations
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {e}")

@app.get("/api/members/{member_id}/loyalty")
async def get_member_loyalty(member_id: str):
    """Récupérer les informations de fidélité d'un membre"""
    try:
        member = await db.members.find_one({"id": member_id})
        if not member:
            raise HTTPException(status_code=404, detail="Membre introuvable")
        
        # Récupérer l'historique des transactions
        transactions = await db.loyalty_transactions.find(
            {"memberId": member_id}, 
            {"_id": 0}
        ).sort("createdAt", -1).to_list(50)
        
        # Calculer les points par type
        earned_points = sum([t["amount"] for t in transactions if t["type"] == "earn"])
        spent_points = sum([t["amount"] for t in transactions if t["type"] == "spend"])
        
        # Informations du niveau actuel
        current_level = member.get("level", "Découvreur")
        current_points = member.get("points", 0)
        level_info = MEMBER_LEVELS.get(current_level, MEMBER_LEVELS["Découvreur"])
        
        # Prochain niveau
        next_level = None
        points_to_next = 0
        for level_name, level_data in MEMBER_LEVELS.items():
            if level_data["min_points"] > current_points:
                next_level = level_name
                points_to_next = level_data["min_points"] - current_points
                break
        
        return {
            "member_id": member_id,
            "current_points": current_points,
            "current_level": current_level,
            "level_benefits": level_info["benefits"],
            "next_level": next_level,
            "points_to_next": points_to_next,
            "total_earned": earned_points,
            "total_spent": spent_points,
            "transactions": transactions[:10]  # Dernières 10 transactions
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {e}")

@app.get("/api/members/{member_id}/notifications")
async def get_member_notifications(member_id: str, limit: int = 20):
    """Récupérer les notifications d'un membre"""
    try:
        notifications = await db.member_notifications.find(
            {"memberId": member_id}, 
            {"_id": 0}
        ).sort("createdAt", -1).limit(limit).to_list(limit)
        
        return notifications
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {e}")

@app.put("/api/members/{member_id}/notifications/{notification_id}/read")
async def mark_notification_read(member_id: str, notification_id: str):
    """Marquer une notification comme lue"""
    try:
        result = await db.member_notifications.update_one(
            {"id": notification_id, "memberId": member_id},
            {"$set": {"isRead": True}}
        )
        
        if result.modified_count:
            return {"success": True, "message": "Notification marquée comme lue"}
        else:
            raise HTTPException(status_code=404, detail="Notification introuvable")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {e}")

@app.get("/api/members/{member_id}/wishlist")
async def get_member_wishlist(member_id: str):
    """Récupérer la wishlist d'un membre"""
    try:
        wishlist_items = await db.member_wishlist.find(
            {"memberId": member_id}, 
            {"_id": 0}
        ).sort("addedAt", -1).to_list(100)
        
        # Enrichir avec les informations des villas
        for item in wishlist_items:
            villa = await db.villas.find_one({"id": item["villaId"]})
            if villa:
                item["villa"] = villa
        
        return wishlist_items
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {e}")

@app.post("/api/members/{member_id}/wishlist")
async def add_to_wishlist(member_id: str, villa_id: str):
    """Ajouter une villa à la wishlist"""
    try:
        # Vérifier que la villa existe
        villa = await db.villas.find_one({"id": villa_id})
        if not villa:
            raise HTTPException(status_code=404, detail="Villa introuvable")
        
        # Vérifier si déjà dans la wishlist
        existing = await db.member_wishlist.find_one({
            "memberId": member_id, 
            "villaId": villa_id
        })
        
        if existing:
            raise HTTPException(status_code=400, detail="Villa déjà dans la wishlist")
        
        # Ajouter à la wishlist
        wishlist_item = {
            "id": str(uuid.uuid4()),
            "memberId": member_id,
            "villaId": villa_id,
            "villaName": villa["name"],
            "addedAt": datetime.utcnow(),
            "notes": None
        }
        
        await db.member_wishlist.insert_one(wishlist_item)
        
        return {"success": True, "message": "Villa ajoutée à la wishlist"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {e}")

@app.delete("/api/members/{member_id}/wishlist/{villa_id}")
async def remove_from_wishlist(member_id: str, villa_id: str):
    """Retirer une villa de la wishlist"""
    try:
        result = await db.member_wishlist.delete_one({
            "memberId": member_id,
            "villaId": villa_id
        })
        
        if result.deleted_count:
            return {"success": True, "message": "Villa retirée de la wishlist"}
        else:
            raise HTTPException(status_code=404, detail="Villa non trouvée dans la wishlist")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {e}")

@app.get("/api/members/stats")
async def get_member_stats():
    """Statistiques générales des membres pour l'admin"""
    try:
        total_members = await db.members.count_documents({"isActive": True})
        new_members_month = await db.members.count_documents({
            "joinDate": {"$gte": datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0).isoformat()},
            "isActive": True
        })
        
        # Stats par niveau
        level_stats = await db.members.aggregate([
            {"$match": {"isActive": True}},
            {"$group": {"_id": "$level", "count": {"$sum": 1}}}
        ]).to_list(None)
        
        return {
            "total_members": total_members,
            "new_members_month": new_members_month,
            "level_distribution": level_stats
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {e}")

# ========== ROUTES ADMIN SÉCURISÉES ==========

@app.get("/api/admin/villas", response_model=List[Villa])
async def get_admin_villas():
    """Récupérer toutes les villas (admin)"""
    try:
        villas = await db.villas.find({}).to_list(1000)
        return villas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {e}")

@app.post("/api/admin/villas", response_model=dict)
async def create_villa(villa_data: VillaCreate):
    """Créer une nouvelle villa (admin)"""
    try:
        # Générer un nouvel ID
        villa_count = await db.villas.count_documents({})
        new_id = str(villa_count + 1)
        
        villa_dict = villa_data.dict()
        villa_dict["id"] = new_id
        villa_dict["image"] = f"./images/villa_{new_id}.jpg"
        villa_dict["gallery"] = [f"./images/villa_{new_id}.jpg"]
        villa_dict["fallback_icon"] = "🏖️"
        
        result = await db.villas.insert_one(villa_dict)
        
        if result.inserted_id:
            return {"success": True, "villa_id": new_id, "message": "Villa créée avec succès"}
        else:
            raise HTTPException(status_code=500, detail="Erreur lors de la création")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {e}")

@app.put("/api/admin/villas/{villa_id}")
async def update_villa(villa_id: str, villa_data: VillaUpdate):
    """Mettre à jour une villa (admin)"""
    try:
        update_data = {k: v for k, v in villa_data.dict().items() if v is not None}
        
        result = await db.villas.update_one(
            {"id": villa_id},
            {"$set": update_data}
        )
        
        if result.modified_count:
            return {"success": True, "message": "Villa mise à jour"}
        else:
            raise HTTPException(status_code=404, detail="Villa non trouvée")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {e}")

@app.delete("/api/admin/villas/{villa_id}")
async def delete_villa(villa_id: str):
    """Supprimer une villa (admin)"""
    try:
        # Vérifier s'il y a des réservations actives
        active_reservations = await db.reservations.count_documents({
            "villa_id": villa_id,
            "status": {"$in": ["pending", "confirmed"]}
        })
        
        if active_reservations > 0:
            raise HTTPException(
                status_code=400, 
                detail="Impossible de supprimer une villa avec des réservations actives"
            )
        
        result = await db.villas.delete_one({"id": villa_id})
        
        if result.deleted_count:
            return {"success": True, "message": "Villa supprimée"}
        else:
            raise HTTPException(status_code=404, detail="Villa non trouvée")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {e}")

@app.get("/api/admin/reservations")
async def get_all_reservations():
    """Récupérer toutes les réservations (admin)"""
    try:
        reservations = await db.reservations.find({}, {"_id": 0}).sort("created_at", -1).to_list(1000)
        return reservations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {e}")

@app.put("/api/admin/reservations/{reservation_id}/status")
async def update_reservation_status_admin(reservation_id: str, status_update: ReservationStatusUpdate):
    """Mettre à jour le statut d'une réservation (admin)"""
    valid_statuses = ["pending", "confirmed", "cancelled"]
    if status_update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Statut invalide")
    
    try:
        result = await db.reservations.update_one(
            {"id": reservation_id},
            {
                "$set": {
                    "status": status_update.status,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        if result.modified_count:
            return {"success": True, "message": "Statut mis à jour"}
        else:
            raise HTTPException(status_code=404, detail="Réservation non trouvée")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {e}")

@app.get("/api/admin/stats/detailed")
async def get_detailed_stats():
    """Statistiques détaillées pour l'admin"""
    try:
        # Compter les villas par catégorie
        villa_stats = await db.villas.aggregate([
            {"$group": {"_id": "$category", "count": {"$sum": 1}}}
        ]).to_list(None)
        
        # Compter les réservations par statut
        reservation_stats = await db.reservations.aggregate([
            {"$group": {"_id": "$status", "count": {"$sum": 1}, "total_revenue": {"$sum": "$total_price"}}}
        ]).to_list(None)
        
        # Revenus par mois
        start_of_year = datetime.utcnow().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        monthly_stats = await db.reservations.aggregate([
            {
                "$match": {
                    "created_at": {"$gte": start_of_year},
                    "status": {"$in": ["confirmed", "pending"]}
                }
            },
            {
                "$group": {
                    "_id": {
                        "year": {"$year": "$created_at"},
                        "month": {"$month": "$created_at"}
                    },
                    "reservations": {"$sum": 1},
                    "revenue": {"$sum": "$total_price"}
                }
            },
            {"$sort": {"_id.year": 1, "_id.month": 1}}
        ]).to_list(None)
        
        return {
            "villa_stats": villa_stats,
            "reservation_stats": reservation_stats,
            "monthly_stats": monthly_stats
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur statistiques détaillées: {e}")

# ========== STATIC FILE SERVING ==========
# IMPORTANT: Static file mounts MUST be after all API routes to prevent routing conflicts

# Servir les images statiques
app.mount("/images", StaticFiles(directory="../images"), name="images")

# Servir les fichiers statiques de l'admin
app.mount("/admin", StaticFiles(directory="../admin", html=True), name="admin")

# Servir les fichiers statiques du site principal
app.mount("/", StaticFiles(directory="../", html=True), name="main_site")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)