from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

# ----- Rol -----
class RolBase(BaseModel):
    nombre: str

class RolCreate(RolBase):
    pass

class RolResponse(RolBase):
    id: int

    class Config:
        from_atributes = True
        

# ----- Usuario -----
class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    username: str
    rol_id: int

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    password: Optional[str] = None
    
    rol_id: Optional[int] = None

class UsuarioResponse(UsuarioBase):
    id: int
    rol: RolResponse

    class Config:
        from_atributes = True
        

# ----- Carrera -----
class CarreraBase(BaseModel):
    nombre: str
    jefe_id: Optional[int] = None

class CarreraCreate(CarreraBase):
    pass

class CarreraResponse(CarreraBase):
    id: int
    class Config:
        from_atributes = True

# ----- Plan de Estudio -----
class PlanEstudioBase(BaseModel):
    nombre: str
    carrera_id: int
    semestres: int

class PlanEstudioCreate(PlanEstudioBase):
    pass

class PlanEstudioResponse(PlanEstudioBase):
    id: int
    carrera: CarreraResponse

    model_config = {
        "from_attributes": True
    }

# ----- Grupo -----
class GrupoBase(BaseModel):
    nombre: str
    plan_estudio_id: int
    jefe_id: int

class GrupoCreate(GrupoBase):
    pass

class GrupoResponse(GrupoBase):
    id: int
    plan_estudio: PlanEstudioResponse
    jefe_grupo: UsuarioResponse

    model_config = {
        "from_attributes": True
    }

# ----- Materia -----
class MateriaBase(BaseModel):
    nombre: str
    plan_estudio_id: int

class MateriaCreate(MateriaBase):
    pass

class MateriaResponse(MateriaBase):
    id: int
    plan_estudio: PlanEstudioResponse

    class Config:
        
        from_atributes = True

class MateriaEdit(BaseModel):
    nombre: Optional[str] = None

# ----- Horario -----
class HorarioBase(BaseModel):
    grupo_id: int
    materia_id: int
    maestro_id: int
    dia_semana: str
    hora_inicio: str
    hora_fin: str

class HorarioCreate(HorarioBase):
    pass

class HorarioResponse(HorarioBase):
    id: int
    grupo: GrupoResponse
    materias: MateriaResponse
    maestros: UsuarioResponse

    class Config:
        from_atributes = True

# ----- Asistencia -----
class AsistenciaBase(BaseModel):
    usuario_id: int
    horario_id: int
    fecha: Optional[date] = None
    asistencia: Optional[bool] = None
    observaciones: Optional[str] = None

class AsistenciaCreate(AsistenciaBase):
    pass

class AsistenciaUpdate(BaseModel):
    
    asistencia: Optional[bool] = None
    observaciones: Optional[str] = None

class AsistenciaResponse(AsistenciaBase):
    id: int
    usuario: UsuarioResponse
    horarios: HorarioResponse

    class Config:
        from_atributes = True

# ----- HorarioMateriaMaestro -----
class HorarioMateriaMaestroBase(BaseModel):
    materia_id: int
    horario_id: int
    usuario_id: int

class MateriaSoft(BaseModel):
    id: int
    nombre: str
    plan_estudio_id: int

class PlanMateriasResponse(BaseModel):
    id: int
    nombre: str
    semestres: int
    materias: list[MateriaSoft]