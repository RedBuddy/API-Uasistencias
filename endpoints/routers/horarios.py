from datetime import datetime
from database.models.models import Grupo, Horario
from jwtoken.auth import get_current_rol
from schemas.schemas import HorarioCreate, HorarioResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.base import get_db

router=APIRouter(tags=["horarios"])

@router.post("/api/horarios/{grupo_id}/", response_model=list[HorarioResponse])
def create_horario_list(horarios_data: list[HorarioCreate], grupo_id: int, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion" and rol != "Jefe de Carrera":
        raise HTTPException(status_code=403, detail="No tienes permisos para crear horarios")
    horarios = []
    for horario_data in horarios_data:
        new_horario = Horario(
            dia_semana=horario_data.dia_semana,
            hora_inicio=horario_data.hora_inicio,
            hora_fin=horario_data.hora_fin,
            materia_id=horario_data.materia_id,
            maestro_id=horario_data.maestro_id,
            grupo_id=grupo_id
        )
        db.add(new_horario)
        horarios.append(new_horario)
    db.commit()
    return horarios


@router.post("/api/horarios/{grupo_id}/individual", response_model=HorarioResponse)
def create_horario(horario_data: HorarioCreate, grupo_id: int, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion" and rol != "Jefe de Carrera":
        raise HTTPException(status_code=403, detail="No tienes permisos para crear horarios")
    
    new_horario = Horario(
        dia_semana=horario_data.dia_semana,
        hora_inicio=horario_data.hora_inicio,
        hora_fin=horario_data.hora_fin,
        materia_id=horario_data.materia_id,
        maestro_id=horario_data.maestro_id,
        grupo_id=grupo_id
    )
    db.add(new_horario)
    db.commit()
    db.refresh(new_horario)
    return new_horario


# Lunes, Martes, Miercoles, Jueves, Viernes
@router.get("/api/horarios/{grupo_id}/{dia}/", response_model=list[HorarioResponse])
def get_horario_diario(grupo_id: int, dia: str, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol not in ["Administracion", "Jefe de Grupo", "Maestro", "Checador", "Jefe de Carrera"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para ver los horarios")
    horarios = db.query(Horario).filter(Horario.grupo_id == grupo_id, Horario.dia_semana == dia).all()
    return horarios

@router.get("/api/horarios/{dia}/hora/{hora}", response_model=list[HorarioResponse])
def get_horario_por_hora(dia: str, hora: str, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol not in ["Administracion", "Jefe de Grupo", "Maestro", "Checador", "Jefe de Carrera"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para ver los horarios")
    horarios = db.query(Horario).filter(Horario.hora_inicio == hora, Horario.dia_semana==dia).all()
    return horarios

@router.get("/api/horarios/{grupo_id}/semana/all", response_model=list[list[HorarioResponse]])
def get_horario_semanal(grupo_id: int, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol not in ["Administracion", "Jefe de Grupo", "Maestro", "Checador", "Jefe de Carrera"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para ver los horarios")
    horarios = []
    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    for dia in dias:
        horarios.append(db.query(Horario).filter(Horario.grupo_id == grupo_id, Horario.dia_semana == dia).all())
    return horarios

@router.put("/api/horarios/{horario_id}/", response_model=HorarioResponse)
def modify_horario(horario_data: HorarioCreate, horario_id: int, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion" and rol != "Jefe de Carrera":
        raise HTTPException(status_code=403, detail="No tienes permisos para crear horarios")
    horario = db.query(Horario).filter(Horario.id == horario_id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    for key, value in horario_data.model_dump(exclude_unset=True).items():
        setattr(horario, key, value)

    db.commit()
    db.refresh(horario)
    return horario

@router.delete("/api/horarios/{horario_id}/")
def delete_horario(horario_id: int, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion" and rol != "Jefe de Carrera":
        raise HTTPException(status_code=403, detail="No tienes permisos para crear horarios")
    horario = db.query(Horario).filter(Horario.id == horario_id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    db.delete(horario)
    db.commit()
    return {"message": "Horario eliminado"}

