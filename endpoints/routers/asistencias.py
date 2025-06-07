"""
Generar asistencia del dia (Lunes a viernes), para cada uno (Maestro, Jefe de Grupo, Checador)

Ver historial de asistencias 


"""

from datetime import date, datetime
from database.models.models import Asistencia, Grupo, Horario
from jwtoken.auth import get_current_rol
from schemas.schemas import AsistenciaResponse, AsistenciaCreate, AsistenciaUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.base import get_db

router = APIRouter(tags=["asistencia"])

@router.get("/api/asistencias/{usuario_id}/{fecha}", response_model=list[AsistenciaResponse])
def get_asistencias(usuario_id: int, fecha: date, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol not in ["Administracion", "Jefe de Grupo", "Maestro", "Checador"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para ver las asistencias")
    asistencias = db.query(Asistencia).filter(Asistencia.usuario_id == usuario_id, Asistencia.fecha == fecha).all()
    return asistencias

@router.get("/api/asistencias/{usuario_id}/{fecha}/{grupo_id}", response_model=list[AsistenciaResponse])
def get_asistencias(usuario_id: int, fecha: date, grupo_id: int, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol not in ["Administracion", "Jefe de Grupo", "Maestro", "Checador"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para ver las asistencias")
    asistencias = db.query(Asistencia).join(Horario, Asistencia.horario_id == Horario.id).join(Grupo, Horario.grupo_id == Grupo.id).filter(Asistencia.usuario_id == usuario_id, Asistencia.fecha == fecha, Grupo.id == grupo_id).all()

    return asistencias

@router.get("/api/asistencias/{usuario_id}/{fecha}/hora/{hora}", response_model=list[AsistenciaResponse])
def get_asistencias(usuario_id: int, fecha: date, hora: str, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol not in ["Administracion", "Jefe de Grupo", "Maestro", "Checador"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para ver las asistencias")
    asistencias = db.query(Asistencia).join(Horario, Asistencia.horario_id == Horario.id).filter(Asistencia.usuario_id == usuario_id, Asistencia.fecha == fecha, Horario.hora_inicio == hora).all()
    return asistencias


@router.get("/api/asistencias/{usuario_id}/", response_model=list[AsistenciaResponse])
def get_asistencias(usuario_id: int, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol not in ["Administracion", "Jefe de Grupo", "Maestro", "Checador"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para ver las asistencias")
    asistencias = db.query(Asistencia).filter(Asistencia.usuario_id == usuario_id).all()
    return asistencias  



@router.post("/api/asistencias/", response_model=AsistenciaResponse)
def create_asistencia(asistencia_data: AsistenciaCreate, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol not in ["Administracion", "Jefe de Grupo", "Maestro", "Checador"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para crear asistencias")
    asistencia = Asistencia(
        usuario_id = asistencia_data.usuario_id,
        horario_id = asistencia_data.horario_id,
        fecha = asistencia_data.fecha,
        asistencia = asistencia_data.asistencia,
        observaciones = asistencia_data.observaciones
    )
    db.add(asistencia)
    db.commit()
    db.refresh(asistencia)
    return asistencia

@router.post("/api/asistencias/list/", response_model=list[AsistenciaResponse])
def create_asistencia(asistencias_data: list[AsistenciaCreate], db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol not in ["Administracion", "Jefe de Grupo", "Maestro", "Checador"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para crear asistencias")
    asistencias = []
    for asistencia_data in asistencias_data:
        asistencia = Asistencia(
            usuario_id = asistencia_data.usuario_id,
            horario_id = asistencia_data.horario_id,
            fecha = asistencia_data.fecha,
            asistencia = asistencia_data.asistencia,
            observaciones = asistencia_data.observaciones
        )
        db.add(asistencia)
        asistencias.append(asistencia)
    db.commit()
    return asistencias

@router.put("/api/asistencias/{asistencia_id}/", response_model=AsistenciaResponse)
def modify_asistencia(asistencia_data: AsistenciaUpdate, asistencia_id: int, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol not in ["Administracion", "Jefe de Grupo", "Maestro", "Checador"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para modificar asistencias")
    asistencia = db.query(Asistencia).filter(Asistencia.id == asistencia_id).first()
    if not asistencia:
        raise HTTPException(status_code=404, detail="Asistencia no encontrada")
    for key, value in asistencia_data.model_dump(exclude_unset=True).items():
        setattr(asistencia, key, value)
    db.commit()
    db.refresh(asistencia)
    return asistencia