from datetime import datetime
from database.models.models import Carrera, Usuario, PlanEstudio, Horario
from jwtoken.auth import get_current_rol
from schemas.schemas import HorarioResponse, UsuarioResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.base import get_db

router = APIRouter(tags=["maestros"])

@router.get("/api/maestros/", response_model=list[UsuarioResponse])
def get_maestros(db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion" and rol != "Jefe de Carrera":
        raise HTTPException(status_code=403, detail="No tienes permisos para ver los maestros")
    maestros = db.query(Usuario).filter(Usuario.rol.nombre == "Maestro").all()
    return maestros



@router.get("/api/maestros/horario/{maestro_id}", response_model=list[HorarioResponse])
def get_maestro_horario(maestro_id: int, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion" and rol != "Jefe de Carrera" and rol != "Maestro":
        raise HTTPException(status_code=403, detail="No tienes permisos para ver el horario de los maestros")
    print(maestro_id)
    
    horario = db.query(Horario).filter(Horario.maestro_id == maestro_id).all()
    print(horario)
    return horario

@router.get("/api/maestros/horario/{maestro_id}/{dia}", response_model=list[HorarioResponse])
def get_maestro_horario_dia(maestro_id: int, dia: str, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion" and rol != "Jefe de Carrera" and rol != "Maestro":
        raise HTTPException(status_code=403, detail="No tienes permisos para ver el horario de los maestros")
    horario = db.query(Horario).filter(Horario.maestro_id == maestro_id, Horario.dia_semana == dia).all()
    
    return horario

