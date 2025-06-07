
from fastapi import Depends, HTTPException, Header

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.base import get_db
from database.models.models import Materia, PlanEstudio
from jwtoken.auth import get_current_rol
from schemas.schemas import MateriaBase, MateriaResponse, MateriaSoft, PlanEstudioCreate, PlanEstudioResponse, PlanMateriasResponse

router = APIRouter(tags=["planes"])

@router.get("/api/planes/", response_model=list[PlanEstudioResponse])
def get_planes(db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion":
        raise HTTPException(status_code=403, detail="No tienes permisos para ver los planes de estudio")
    planes = db.query(PlanEstudio).all()
    return planes

@router.post("/api/planes/", response_model=PlanEstudioResponse)
def create_plan(plan_data: PlanEstudioCreate, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion" and rol != "Jefe de Carrera":
        raise HTTPException(status_code=403, detail="No tienes permisos para crear planes de estudio")
    new_plan = PlanEstudio(
        nombre=plan_data.nombre,
        semestres=plan_data.semestres,
        carrera_id=plan_data.carrera_id
    )
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return new_plan

@router.delete("/api/planes/{plan_id}/", response_model=dict)
def delete_plan(plan_id: int, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion" and rol != "Jefe de Carrera":
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar planes de estudio")
    plan = db.query(PlanEstudio).filter(PlanEstudio.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan de estudio no encontrado")
    db.delete(plan)
    db.commit()
    return {"message": "Plan de estudio eliminado"}

@router.get("/api/planes/{carrera_id}/", response_model=list[PlanMateriasResponse])
def get_planes_by_carrera(carrera_id: int, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion" and rol != "Jefe de Carrera":
        raise HTTPException(status_code=403, detail="No tienes permisos para ver los planes de estudio")
    planesMateria = []
    planes = db.query(PlanEstudio).filter(PlanEstudio.carrera_id == carrera_id).all()
    for plan in planes:
        
        materiasBD  = db.query(Materia).filter(Materia.plan_estudio_id == plan.id).all()
        materiass = []
        for materia in materiasBD:
            materia = MateriaSoft(
                id=materia.id,
                nombre=materia.nombre,
                plan_estudio_id=materia.plan_estudio_id
            )
            materiass.append(materia)
        
        plansito = PlanMateriasResponse(
            id=plan.id,
            nombre=plan.nombre,
            semestres=plan.semestres,
            materias=materiass
        )
        
        planesMateria.append(plansito)
    return planesMateria

@router.put("/api/materias/{plan_id}", response_model=PlanEstudioResponse)
def modify_horario(carrera_data: PlanEstudioCreate, plan_id: int, db: Session = Depends(get_db), rol: str = Depends(get_current_rol)):
    if rol != "Administracion" and rol != "Jefe de Carrera":
        raise HTTPException(status_code=403, detail="No tienes permisos para modificar los planes de estudio")
    plan = db.query(PlanEstudio).filter(PlanEstudio.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan de estudios no encontrado")
    for key, value in carrera_data.model_dump(exclude_unset=True).items():
        setattr(plan, key, value)

    db.commit()
    db.refresh(plan)
    return plan

