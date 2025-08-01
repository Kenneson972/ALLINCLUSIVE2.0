"""
Proxy API pour Admin Propriétaires
=================================

Ce script ajoute des routes proxy à l'API FastAPI existante
pour éviter les problèmes de CORS avec localhost:3002
"""

import requests
import json
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

# Routes à ajouter au serveur FastAPI existant
BACKEND_BASE = "http://localhost:3002/api"

async def proxy_admin_health():
    """Route: GET /api/admin/health"""
    try:
        response = requests.get(f"{BACKEND_BASE}/health", timeout=5)
        return JSONResponse(content=response.json(), status_code=response.status_code)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

async def proxy_admin_validate_code(request: Request):
    """Route: POST /api/admin/validate-code"""
    try:
        body = await request.json()
        response = requests.post(
            f"{BACKEND_BASE}/auth/validate-code",
            json=body,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        return JSONResponse(content=response.json(), status_code=response.status_code)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

async def proxy_admin_login(request: Request):
    """Route: POST /api/admin/login"""
    try:
        body = await request.json()
        response = requests.post(
            f"{BACKEND_BASE}/auth/login",
            json=body,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        return JSONResponse(content=response.json(), status_code=response.status_code)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

async def proxy_admin_validate_token(request: Request):
    """Route: GET /api/admin/validate-token"""
    try:
        auth_header = request.headers.get('Authorization')
        headers = {'Authorization': auth_header} if auth_header else {}
        
        response = requests.get(
            f"{BACKEND_BASE}/auth/validate-token",
            headers=headers,
            timeout=10
        )
        return JSONResponse(content=response.json(), status_code=response.status_code)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Instructions pour ajouter au serveur.py existant :
"""
1. Ajouter ces imports en haut du fichier server.py :
   import requests
   from fastapi.responses import JSONResponse

2. Ajouter ces routes dans server.py :

# Routes Admin Proxy
@app.get("/api/admin/health")
async def admin_health():
    return await proxy_admin_health()

@app.post("/api/admin/validate-code")
async def admin_validate_code(request: Request):
    return await proxy_admin_validate_code(request)

@app.post("/api/admin/login")  
async def admin_login(request: Request):
    return await proxy_admin_login(request)

@app.get("/api/admin/validate-token")
async def admin_validate_token(request: Request):
    return await proxy_admin_validate_token(request)
"""