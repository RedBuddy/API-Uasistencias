from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from database.base import get_db
from database.models.models import Usuario
from schemas.schemas import UsuarioCreate, UsuarioResponse

from schemas.token import TokenResponse
from fastapi import Depends, HTTPException, Header

# Clave secreta y algoritmo para JWT
SECRET_KEY = "supersecreto"
ALGORITHM = "HS256"

# Configurar bcrypt para hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Función para hashear contraseñas
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Función para registrar un usuario nuevo
def create_user(db: Session, user_data: UsuarioCreate) -> UsuarioResponse:
    existing_user = db.query(Usuario).filter(Usuario.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    new_user = Usuario(
        nombre=user_data.nombre,
        apellido=user_data.apellido,
        username=user_data.username,
        rol_id=user_data.rol_id,
        password=hash_password(user_data.password)
    
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UsuarioResponse.model_validate(new_user, from_attributes=True)

# Función para verificar la contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Función para obtener usuario desde la BD por username
def get_user_by_username(db: Session, username: str) -> Usuario:
    return db.query(Usuario).filter(Usuario.username == username).first()

# Función para obtener los datos de usuario por ID
def get_user_by_id(db: Session, user_id: int) -> UsuarioResponse:
    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UsuarioResponse.from_orm(user)

# Función para autenticar usuario
def authenticate_user(db: Session, username: str, password: str) -> UsuarioResponse:
    user = get_user_by_username(db, username)
    if user and verify_password(password, user.password):
        user_response = UsuarioResponse.model_validate(user, from_attributes=True)
        print (user_response.model_dump())
        print (user_response)
        return user_response.model_dump()  # Convertimos a diccionario para evitar problemas de serialización
    
    raise HTTPException(status_code=401, detail="Credenciales inválidas")


# Función para generar token JWT
def create_jwt_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=2)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Función para verificar token JWT y obtener usuario actual
def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)) -> UsuarioResponse:
    print(f"Authorization Header: {authorization}")
    if authorization is None:
        raise HTTPException(status_code=401, detail="Falta el encabezado de autorización")

    try:
        token = authorization.split(" ")[1]  # Formato 'Bearer <token>'
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return UsuarioResponse.model_validate(user, from_attributes=True)

def get_current_rol(authorization: str = Header(None), db: Session = Depends(get_db)) -> str:
    if authorization is None:
        raise HTTPException(status_code=401, detail="Falta el encabezado de autorización")

    try:
        token = authorization.split(" ")[1]  # Formato 'Bearer <token>'
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        rol: str = payload.get("rol")
        if rol is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    return rol