import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
from dotenv import load_dotenv

# Cargamos las variables de entorno
load_dotenv()

app = FastAPI()

# Configuramos CORS para que tu página web pueda comunicarse con esta API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Datos de conexión (los sacaremos de las variables de entorno de Vercel)
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")

HEADERS = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

@app.get("/api/posts")
async def obtener_posts():
    """Lee todos los posts de la base de datos"""
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{URL}/rest/v1/posts?select=*", headers=HEADERS)
        return res.json()

@app.post("/api/crear-post")
async def crear_post(titulo: str, contenido: str):
    """Guarda un nuevo post en Supabase"""
    async with httpx.AsyncClient() as client:
        nuevo_post = {"titulo": titulo, "contenido": contenido}
        res = await client.post(f"{URL}/rest/v1/posts", headers=HEADERS, json=nuevo_post)
        return res.json()
