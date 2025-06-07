from datetime import datetime
from database.models.models import Materia
from jwtoken.auth import get_current_rol
from schemas.schemas import MateriaCreate, MateriaEdit, MateriaResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.base import get_db

router = APIRouter(tags=["materias"])
@router.get("/api/materias/", response_model=list[MateriaResponse])
def get_materias(db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion":
        raise HTTPException(status_code=403, detail="No tienes permisos para ver las materias")
    materias = db.query(Materia).all()
    return materias

@router.get("/api/materias/{plan_id}", response_model=list[MateriaResponse])
def get_materias_by_carrera(plan_id: int, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion" and rol != "Jefe de Carrera":
        raise HTTPException(status_code=403, detail="No tienes permisos para ver las materias")
    materias = db.query(Materia).filter(Materia.plan_estudio_id == plan_id).all()
    return materias

@router.post("/api/materias/", response_model=MateriaResponse)
def create_materia(materia_data: MateriaCreate, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion" and rol != "Jefe de Carrera":
        raise HTTPException(status_code=403, detail="No tienes permisos para crear materias")
    new_materia = Materia(
        nombre=materia_data.nombre,
        plan_estudio_id=materia_data.plan_estudio_id
    )
    db.add(new_materia)
    db.commit()
    db.refresh(new_materia)
    return new_materia

@router.post("/api/materias/list/", response_model=list[MateriaResponse])
def create_materias(materias_data: list[MateriaCreate], db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion" and rol != "Jefe de Carrera":
        raise HTTPException(status_code=403, detail="No tienes permisos para crear materias")
    materias = []
    for materia_data in materias_data:
        new_materia = Materia(
            nombre=materia_data.nombre,
            plan_estudio_id=materia_data.plan_estudio_id
        )
        db.add(new_materia)
        materias.append(new_materia)
    db.commit()
    return materias

@router.delete("/api/materias/{materia_id}/", response_model=dict)
def delete_materia(materia_id: int, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion" and rol != "Jefe de Carrera":
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar materias")
    materia = db.query(Materia).filter(Materia.id == materia_id).first()
    if not materia:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    db.delete(materia)
    db.commit()
    return {"message": "Materia eliminada"}

@router.get("/api/materias/materia/{materia_id}/", response_model=MateriaResponse)
def get_materia(materia_id: int, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    print(rol)
    if rol != "Administracion" and rol != "Jefe de Carrera":
        raise HTTPException(status_code=403, detail="No tienes permisos para ver materias")
    materia = db.query(Materia).filter(Materia.id == materia_id).first()
    if not materia:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    return materia

@router.put("/api/materias/materia/{materia_id}/", response_model=MateriaResponse)
def modify_horario(materia_data: MateriaEdit, materia_id: int, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion" and rol != "Jefe de Carrera":
        raise HTTPException(status_code=403, detail="No tienes permisos para modificar Materias")
    materia = db.query(Materia).filter(Materia.id == materia_id).first()
    if not materia:
        raise HTTPException(status_code=404, detail="Materia no encontrado")
    for key, value in materia_data.model_dump(exclude_unset=True).items():
        setattr(materia, key, value)

    db.commit()
    db.refresh(materia)
    return materia

