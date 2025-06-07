from datetime import datetime
from sqlalchemy import Column, Date, Integer, String, Text, Float, ForeignKey, DateTime, Time, Boolean
from database.base import Base
from sqlalchemy.orm import relationship

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    apellido = Column(String(200), nullable=False)
    username = Column(String(200), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    rol_id = Column(Integer, ForeignKey("roles.id"))

    rol = relationship("Rol", back_populates="usuarios")
    asistencias = relationship("Asistencia", back_populates="usuario")
    horarios = relationship("Horario", back_populates="maestros")
    carrera = relationship("Carrera", back_populates="jefe_carrera")
    grupo = relationship("Grupo", back_populates="jefe_grupo")

class Rol(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), unique=True, nullable=False)

    usuarios = relationship("Usuario", back_populates="rol")

class Carrera(Base):
    __tablename__ = "carreras"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    jefe_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)

    planes_estudio = relationship("PlanEstudio", back_populates="carrera")
    jefe_carrera = relationship("Usuario", back_populates="carrera")



class PlanEstudio(Base):
    __tablename__ = "planes_estudio"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    semestres = Column(Integer, nullable=False)
    carrera_id = Column(Integer, ForeignKey("carreras.id"))

    carrera = relationship("Carrera", back_populates="planes_estudio")
    grupos = relationship("Grupo", back_populates="plan_estudio")
    materias = relationship("Materia", back_populates="plan_estudio")

class Grupo(Base):
    __tablename__ = "grupos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    plan_estudio_id = Column(Integer, ForeignKey("planes_estudio.id"))
    jefe_id = Column(Integer, ForeignKey("usuarios.id"))

    jefe_grupo = relationship("Usuario", back_populates="grupo")
    plan_estudio = relationship("PlanEstudio", back_populates="grupos")
    horarios = relationship("Horario", back_populates="grupo")

class Materia(Base):
    __tablename__ = "materias"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    plan_estudio_id = Column(Integer, ForeignKey("planes_estudio.id"))

    plan_estudio = relationship("PlanEstudio", back_populates="materias")
    horarios = relationship("Horario", back_populates="materias")


class Horario(Base):
    __tablename__ = "horarios"
    id = Column(Integer, primary_key=True, index=True)
    grupo_id = Column(Integer, ForeignKey("grupos.id"))
    materia_id = Column(Integer, ForeignKey("materias.id"))
    maestro_id = Column(Integer, ForeignKey("usuarios.id"))
    dia_semana = Column(String(200), nullable=False)  
    hora_inicio = Column(String(200), nullable=False)
    hora_fin = Column(String(200), nullable=False)

    asistencias = relationship("Asistencia", back_populates="horarios")
    grupo = relationship("Grupo", back_populates="horarios")
    materias = relationship("Materia", back_populates="horarios")
    maestros = relationship("Usuario", back_populates="horarios")

class Asistencia(Base):
    __tablename__ = "asistencias"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    horario_id = Column(Integer, ForeignKey("horarios.id"))
    fecha = Column(Date, default=datetime.now)
    asistencia = Column(Boolean, nullable=True)
    observaciones = Column(String(200), nullable=True)
    usuario = relationship("Usuario", back_populates="asistencias")
    horarios = relationship("Horario", back_populates="asistencias")
