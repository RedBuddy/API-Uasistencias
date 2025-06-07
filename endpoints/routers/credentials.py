from datetime import datetime
from database.models.models import Usuario
from schemas.schemas import UsuarioCreate, UsuarioResponse 
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.base import get_db
from sqlalchemy.exc import IntegrityError

router = APIRouter(tags=["auth"])
from jwtoken.auth import get_current_user, create_jwt_token, verify_password, authenticate_user, create_user
from schemas.token import TokenResponse, LoginRequest

@router.post("/api/auth/login", response_model=TokenResponse)
def login(user: LoginRequest, db: Session = Depends(get_db)):
    auth_user = authenticate_user(db, user.username, user.password)
    if not auth_user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    # Asegúrate de extraer el rol correctamente
    rol_nombre = auth_user["rol"]["nombre"] if "rol" in auth_user and "nombre" in auth_user["rol"] else None

    token = create_jwt_token({"sub": auth_user["username"], "rol": rol_nombre, "id": auth_user["id"]}) 
    return {"token": token}


@router.post("/api/auth/register")
def register(user_data: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        new_user = create_user(db, user_data)
        return {"message": "Usuario registrado exitosamente", "user": new_user}
    except IntegrityError as e:
        db.rollback()
        print("IntegrityError:", e)
        raise HTTPException(
            status_code=400,
            detail="Ya existe un usuario con los datos proporcionados (número de cuenta, username o email duplicado)."
        )
    except HTTPException as e:
        db.rollback()
        print("HTTPException:", e)
        # Reemplaza cualquier variante del mensaje corto por el formal
        if str(e.detail).strip().lower() == "el usuario ya existe":
            raise HTTPException(
                status_code=400,
                detail="Ya existe un usuario con los datos proporcionados (número de cuenta, username o email duplicado)."
            )
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail.replace("El usuario ya existe", "Ya existe un usuario con los datos proporcionados (número de cuenta, username o email duplicado).")
        )
    except Exception as e:
        db.rollback()
        print("Exception:", e)
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/api/auth/me")
def get_me(current_user: UsuarioResponse = Depends(get_current_user)):

    return current_user