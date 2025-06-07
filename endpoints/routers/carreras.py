from datetime import datetime
from database.models.models import Carrera
from jwtoken.auth import get_current_rol
from schemas.schemas import  CarreraResponse, CarreraCreate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.base import get_db

router = APIRouter(tags=["carreras"])

@router.get("/api/carreras/", response_model=list[CarreraResponse])
def get_carreras(db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion" and rol != "Checador":
        raise HTTPException(status_code=403, detail="No tienes permisos para ver las carreras")
    carreras = db.query(Carrera).all()
    return carreras

@router.post("/api/carreras/", response_model=CarreraResponse)
def create_carrera(carrera_data: CarreraCreate, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion" and rol != "Checador":
        raise HTTPException(status_code=403, detail="No tienes permisos para crear carreras")
    new_carrera = Carrera(
        nombre=carrera_data.nombre,
        jefe_id=carrera_data.jefe_id
    )
    db.add(new_carrera)
    db.commit()
    db.refresh(new_carrera)
    return new_carrera

@router.put("/api/carreras/{carrera_id}", response_model=CarreraResponse)
def modify_horario(carrera_data: CarreraCreate, carrera_id: int, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion":
        raise HTTPException(status_code=403, detail="No tienes permisos para crear horarios")
    carrera = db.query(Carrera).filter(Carrera.id == carrera_id).first()
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrado")
    for key, value in carrera_data.model_dump(exclude_unset=True).items():
        setattr(carrera, key, value)

    db.commit()
    db.refresh(carrera)
    return carrera

@router.delete("/api/carreras/{carrera_id}/", response_model=dict)
def delete_carrera(carrera_id: int, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion":
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar carreras")
    carrera = db.query(Carrera).filter(Carrera.id == carrera_id).first()
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    db.delete(carrera)
    db.commit()
    return {"message": "Carrera eliminada"}

@router.get("/api/carreras/{carrera_id}/", response_model=CarreraResponse)
def get_carrera(carrera_id: int, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion" and rol != "Jefe de Carrera":
        raise HTTPException(status_code=403, detail="No tienes permisos para ver carreras")
    carrera = db.query(Carrera).filter(Carrera.id == carrera_id).first()
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return carrera

@router.get("/api/carreras/jefe/{usuario_id}/", response_model=CarreraResponse)
def get_carrera_jefe(usuario_id: int, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    print(rol)
    print(rol=="Administracion")
    if rol != "Administracion" and rol != "Jefe de Carrera":
        raise HTTPException(status_code=403, detail="No tienes permisos para ver carreras")
    carrera = db.query(Carrera).filter(Carrera.jefe_id == usuario_id).first()
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return carrera