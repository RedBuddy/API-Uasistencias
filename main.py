from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from database.base import Base, engine, get_db
import database.models.models as models
from fastapi.middleware.cors import CORSMiddleware
#Importamos los routers
from endpoints.routers import asistencias, carreras, credentials, planes, reportes, roles, users, grupos, materias, maestros, horarios
app = FastAPI(    title="UASISTENCIA",
    description="UASISTENCIA API",
    version="1.0.0",
    openapi_tags=[{"name": "auth", "description": "Operaciones de autenticación"},
                  {"name": "users", "description": "Operaciones de usuarios"},
                  {"name": "roles", "description": "Operaciones de roles"},
                  {"name": "planes", "description": "Operaciones de planes de estudio"},
                  {"name": "carreras", "description": "Operaciones de carreras"},
                  {"name": "grupos", "description": "Operaciones de grupos"},
                  {"name": "materias", "description": "Operaciones de materias"},
                  {"name": "asistencias", "description": "Operaciones de asistencias"},
                  {"name": "reportes", "description": "Operaciones de reportes"},
                  {"name": "maestros", "description": "Operaciones de maestros"}],

    # Esto es lo que habilitará el envío de token por Swagger
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url=None,)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia "*" por la URL del frontend si es necesario
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Crear la base de datos y las tablas
Base.metadata.create_all(bind=engine)

#Agregamos los routers
app.include_router(credentials.router)
app.include_router(users.router)
app.include_router(roles.router)
app.include_router(planes.router)
app.include_router(carreras.router)
app.include_router(grupos.router)
app.include_router(materias.router)
app.include_router(maestros.router)
app.include_router(asistencias.router)
app.include_router(horarios.router)
app.include_router(reportes.router)
@app.get("/")
async def read_root():
    
    return {"Hola": "Que andas viendo pues"}


