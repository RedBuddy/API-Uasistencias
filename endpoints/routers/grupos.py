from datetime import datetime
from database.models.models import Carrera, Grupo, PlanEstudio
from jwtoken.auth import get_current_rol
from schemas.schemas import GrupoCreate, GrupoResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.base import get_db
router=APIRouter(tags=["grupos"])


@router.get("/api/grupos/", response_model=list[GrupoResponse])
def get_grupos(db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion" and rol != "Jefe de Carrera":
        raise HTTPException(status_code=403, detail="No tienes permisos para ver los grupos")
    grupos = db.query(Grupo).all()
    return grupos

@router.post("/api/grupos/", response_model=GrupoResponse)
def create_grupo(grupo_data: GrupoCreate, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion" and rol != "Jefe de Carrera":
        raise HTTPException(status_code=403, detail="No tienes permisos para crear grupos")
    new_grupo = Grupo(
        nombre=grupo_data.nombre,
        plan_estudio_id=grupo_data.plan_estudio_id,
        jefe_id = grupo_data.jefe_id
    )
    db.add(new_grupo)
    db.commit()
    db.refresh(new_grupo)
    return new_grupo

@router.put("/api/grupos/{grupo_id}/", response_model=GrupoResponse)
def modify_grupo(grupo_data: GrupoCreate,grupo_id: int,  db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion" and rol != "Jefe de Carrera":
        raise HTTPException(status_code=403, detail="No tienes permisos para crear horarios")
    grupo = db.query(Grupo).filter(Grupo.id == grupo_id).first()
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    for key, value in grupo_data.model_dump(exclude_unset=True).items():
        setattr(grupo, key, value)

    db.commit()
    db.refresh(grupo)
    return grupo

@router.delete("/api/grupos/{grupo_id}/", response_model=dict)
def delete_grupo(grupo_id: int, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion" and rol != "Jefe de Carrera":
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar grupos")
    grupo = db.query(Grupo).filter(Grupo.id == grupo_id).first()
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    db.delete(grupo)
    db.commit()
    return {"message": "Grupo eliminado"}

@router.get("/api/grupos/{grupo_id}/", response_model=GrupoResponse)
def get_grupo(grupo_id: int, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion" and rol != "Jefe de Carrera":
        raise HTTPException(status_code=403, detail="No tienes permisos para ver grupos")
    grupo = db.query(Grupo).filter(Grupo.id == grupo_id).first()
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return grupo

#Ver todos los grupos por plan de estudio
@router.get("/api/grupos/plan/{plan_id}/", response_model=list[GrupoResponse])
def get_grupoPlan(plan_id: int, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion" and rol != "Jefe de Carrera":
        raise HTTPException(status_code=403, detail="No tienes permisos para ver grupos")
    grupos = db.query(Grupo).filter(Grupo.plan_estudio_id == plan_id).all()
    return grupos

@router.get("/api/grupos/jefe/{jefe_id}/", response_model=GrupoResponse)
def get_grupoJefe(jefe_id: int, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion" and rol != "Jefe de Carrera" and rol != "Jefe de Grupo":
        raise HTTPException(status_code=403, detail="No tienes permisos para ver grupos")
    grupo = db.query(Grupo).filter(Grupo.jefe_id == jefe_id).first()
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return grupo

@router.get("/api/grupos/carrera/{carrera_id}", response_model=list[GrupoResponse])
def get_grupoCarrera(carrera_id: int, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion" and rol != "Jefe de Carrera" and rol != "Checador":
        raise HTTPException(status_code=403, detail="No tienes permisos para ver grupos")
    grupos = (
    db.query(Grupo)
    .join(PlanEstudio, Grupo.plan_estudio_id == PlanEstudio.id)
    .join(Carrera, PlanEstudio.carrera_id == Carrera.id)
    .filter(Carrera.id == carrera_id)
    .all()
)
    return grupos