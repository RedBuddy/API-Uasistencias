from fastapi import Depends, HTTPException, Header

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.base import get_db
from database.models.models import Rol, Usuario
from jwtoken.auth import get_current_user, get_user_by_username, hash_password
from schemas.schemas import UsuarioResponse, UsuarioUpdate

router = APIRouter(tags=["users"])

@router.get("/api/users/{username}/", response_model=UsuarioResponse)
def get_user(username: str, db: Session = Depends(get_db)):
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.get("/api/users/", response_model=list[UsuarioResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(Usuario).all()
    return users

@router.put("/api/users/{username}/admin", response_model=UsuarioResponse)
def update_userAdmin(username: str, user_data: UsuarioUpdate, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user_data.password = hash_password(user_data.password)
    for key, value in user_data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

@router.put("/api/users/{username}/", response_model=UsuarioResponse)
def update_user(username: str, user_data: UsuarioUpdate, current_user: UsuarioResponse = Depends(get_current_user), db: Session = Depends(get_db)):
    # Verificar que el username en la URL coincida con el username en el token
    if current_user.username != username:
        raise HTTPException(status_code=403, detail="No puedes actualizar el perfil de otro usuario")
    
    user = db.query(Usuario).filter(Usuario.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user_data.password = hash_password(user_data.password)
    # Actualizar solo los campos que han sido enviados
    for key, value in user_data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

@router.delete("/api/users/{username}/", response_model=dict)
def delete_user(username: str, current_user: UsuarioResponse = Depends(get_current_user), db: Session = Depends(get_db)):
    # Verificar que el username en la URL coincida con el username en el token
    if current_user.username != username:
        raise HTTPException(status_code=403, detail="No puedes eliminar el perfil de otro usuario")
    
    user = db.query(Usuario).filter(Usuario.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(user)
    db.commit()
    return {"message": "Usuario eliminado exitosamente"}

@router.delete("/api/users/{username}/admin", response_model=dict)
def delete_userAdmin(username: str, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(user)
    db.commit()
    return {"message": "Usuario eliminado exitosamente"}

@router.get("/api/users/rol/{rol}", response_model=list[UsuarioResponse])
def get_usuarios_rol(rol: str, db: Session = Depends(get_db)):
    usuarios = []
    if (rol=="administracion"):
        rol_data = db.query(Rol).filter(Rol.nombre=="Administracion").first()
        usuarios = db.query(Usuario).filter(Usuario.rol_id==rol_data.id).all()
    else:
        if (rol=="jefegrupo"):
            rol_data = db.query(Rol).filter(Rol.nombre=="Jefe de Grupo").first()
            usuarios = db.query(Usuario).filter(Usuario.rol_id==rol_data.id).all()
        else:
            if (rol=="jefecarrera"):
                rol_data = db.query(Rol).filter(Rol.nombre=="Jefe de Carrera").first()
                usuarios = db.query(Usuario).filter(Usuario.rol_id==rol_data.id).all()
            else:
                if (rol=="checador"):
                    rol_data = db.query(Rol).filter(Rol.nombre=="Checador").first()
                    usuarios = db.query(Usuario).filter(Usuario.rol_id==rol_data.id).all()
                else:
                    if (rol=="maestro"):
                        rol_data = db.query(Rol).filter(Rol.nombre=="Maestro").first()
                        usuarios = db.query(Usuario).filter(Usuario.rol_id==rol_data.id).all()
                    else:
                            raise HTTPException(status_code=404, detail="Rol no encontrado")
    return usuarios

