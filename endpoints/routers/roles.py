
from fastapi import Depends, HTTPException, Header

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.base import get_db
from database.models.models import Rol
from jwtoken.auth import get_current_rol
from schemas.schemas import RolResponse

router = APIRouter(tags=["roles"])

@router.get("/api/roles/", response_model=list[RolResponse])
def get_roles(db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion":
        raise HTTPException(status_code=403, detail="No tienes permisos para ver los roles")
    roles = db.query(Rol).all()
    return roles

@router.post("/api/roles/", response_model=RolResponse)
def create_rol(rol_data: RolResponse, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion":
        raise HTTPException(status_code=403, detail="No tienes permisos para crear roles")
    new_rol = Rol(
        nombre=rol_data.nombre
    )
    db.add(new_rol)
    db.commit()
    db.refresh(new_rol)
    return new_rol
