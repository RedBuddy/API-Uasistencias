from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from io import StringIO
import csv
from datetime import date, datetime, timedelta
from database.base import get_db
from database.models.models import Usuario, Horario, Asistencia, Grupo, Materia
import unicodedata

router = APIRouter()

def normaliza(texto):
    if not texto:
        return ""
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto.lower())
        if unicodedata.category(c) != 'Mn'
    ).strip()


@router.get("/api/reportes/maestros/{maestro_id}/asistencia/json")
def generar_asistencia_maestro_json(
    maestro_id: int,
    fecha_inicio: date,
    fecha_fin: Optional[date] = None,
    checador: bool = True,
    maestro: bool = True,
    jefe_grupo: bool = True,
    db: Session = Depends(get_db)
):
    """
    Genera un archivo JSON con los registros de asistencia para un maestro específico 
    en un rango de fechas, filtrando por roles de usuario.
    """

    if fecha_fin is None:
        fecha_fin = fecha_inicio
    
    if fecha_fin < fecha_inicio:
        raise HTTPException(status_code=400, detail="La fecha final debe ser posterior o igual a la fecha inicial")
    
    maestroinfo = db.query(Usuario).filter(Usuario.id == maestro_id).first()
    if not maestroinfo:
        raise HTTPException(status_code=404, detail="Maestro no encontrado")
    
    fechas = []
    fecha_actual = fecha_inicio
    while fecha_actual <= fecha_fin:
        fechas.append(fecha_actual)
        fecha_actual += timedelta(days=1)
    
    horarios = db.query(Horario).filter(Horario.maestro_id == maestro_id).all()
    if not horarios:
        raise HTTPException(status_code=404, detail="El maestro no tiene horarios asignados")
    
    asistencias_data = []

    for fecha in fechas:
        dia_semana = fecha.strftime("%A").lower()
        mapeo_dias = {
            "monday": "lunes", "tuesday": "martes", "wednesday": "miércoles",
            "thursday": "jueves", "friday": "viernes", "saturday": "sábado", "sunday": "domingo"
        }
        dia_semana_es = mapeo_dias.get(dia_semana, dia_semana)
        
        # Debug: imprime la comparación de días
        # for h in horarios:
        #     print(f"Comparando: '{normaliza(h.dia_semana)}' == '{normaliza(dia_semana_es)}'")

        horarios_del_dia = [h for h in horarios if normaliza(h.dia_semana) == normaliza(dia_semana_es)]
        if not horarios_del_dia:
            continue
        
        for horario in horarios_del_dia:
            materia = db.query(Materia).filter(Materia.id == horario.materia_id).first()
            grupo = db.query(Grupo).filter(Grupo.id == horario.grupo_id).first()
            
            asistencias = db.query(Asistencia).filter(
                Asistencia.horario_id == horario.id,
                Asistencia.fecha == fecha
            ).all()
            
            for asistencia in asistencias:
                usuario_asistencia = db.query(Usuario).filter(Usuario.id == asistencia.usuario_id).first()
                
                if not usuario_asistencia:
                    continue
                
                # Filtrar por roles
                if not (
                    (checador and usuario_asistencia.rol.nombre == "Checador") or
                    (maestro and usuario_asistencia.rol.nombre == "Maestro") or
                    (jefe_grupo and usuario_asistencia.rol.nombre == "Jefe de Grupo")
                ):
                    continue

                estado_asistencia = "No registrado"
                if asistencia.asistencia is not None:
                    estado_asistencia = "Presente" if asistencia.asistencia else "Ausente"

                asistencias_data.append({
                    "ID": asistencia.id,
                    "Fecha": fecha.strftime("%d/%m/%Y"),
                    "Día": dia_semana_es.capitalize(),
                    "Maestro": f"{maestroinfo.nombre} {maestroinfo.apellido}",
                    "Grupo": grupo.nombre if grupo else "No disponible",
                    "Materia": materia.nombre if materia else "No disponible",
                    "Hora Inicio": horario.hora_inicio,
                    "Hora Fin": horario.hora_fin,
                    "Estado": estado_asistencia,
                    "Observaciones": asistencia.observaciones or "",
                    "Registrado por": f"{usuario_asistencia.nombre} {usuario_asistencia.apellido}"
                })

    if not asistencias_data:
        raise HTTPException(status_code=404, detail="No hay registros de asistencia para los filtros especificados")

    return JSONResponse(content=asistencias_data)


@router.get("/api/reportes/grupos/{grupo_id}/asistencia/json")
def generar_asistencia_grupo_json(
    grupo_id: int,
    fecha_inicio: date,
    fecha_fin: Optional[date] = None,
    checador: bool = True,
    maestro: bool = True,
    jefe_grupo: bool = True,
    db: Session = Depends(get_db)
):
    """
    Genera un archivo JSON con los registros de asistencia para un grupo específico
    en un rango de fechas, filtrando por roles de usuario.
    """
    if fecha_fin is None:
        fecha_fin = fecha_inicio
    
    if fecha_fin < fecha_inicio:
        raise HTTPException(status_code=400, detail="La fecha final debe ser posterior o igual a la fecha inicial")
    
    grupo = db.query(Grupo).filter(Grupo.id == grupo_id).first()
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    
    fechas = []
    fecha_actual = fecha_inicio
    while fecha_actual <= fecha_fin:
        fechas.append(fecha_actual)
        fecha_actual += timedelta(days=1)
    
    horarios = db.query(Horario).filter(Horario.grupo_id == grupo_id).all()
    if not horarios:
        raise HTTPException(status_code=404, detail="El grupo no tiene horarios asignados")
    
    asistencias_data = []
    
    for fecha in fechas:
        dia_semana = fecha.strftime("%A").lower()
        mapeo_dias = {
            "monday": "lunes", "tuesday": "martes", "wednesday": "miércoles",
            "thursday": "jueves", "friday": "viernes", "saturday": "sábado", "sunday": "domingo"
        }
        dia_semana_es = mapeo_dias.get(dia_semana, dia_semana)
        
        # Debug: imprime la comparación de días
        # for h in horarios:
        #     print(f"Comparando: '{normaliza(h.dia_semana)}' == '{normaliza(dia_semana_es)}'")

        horarios_del_dia = [h for h in horarios if normaliza(h.dia_semana) == normaliza(dia_semana_es)]
        if not horarios_del_dia:
            continue
        
        for horario in horarios_del_dia:
            maestroinfo = db.query(Usuario).filter(Usuario.id == horario.maestro_id).first()
            materia = db.query(Materia).filter(Materia.id == horario.materia_id).first()
            
            asistencias = db.query(Asistencia).filter(
                Asistencia.horario_id == horario.id,
                Asistencia.fecha == fecha
            ).all()
            
            for asistencia in asistencias:
                usuario_asistencia = db.query(Usuario).filter(Usuario.id == asistencia.usuario_id).first()
                
                if not usuario_asistencia:
                    continue
                
                if not (
                    (checador and usuario_asistencia.rol.nombre == "Checador") or
                    (maestro and usuario_asistencia.rol.nombre == "Maestro") or
                    (jefe_grupo and usuario_asistencia.rol.nombre == "Jefe de Grupo")
                ):
                    continue

                estado_asistencia = "No registrado"
                if asistencia.asistencia is not None:
                    estado_asistencia = "Presente" if asistencia.asistencia else "Ausente"
                
                asistencias_data.append({
                    "ID": asistencia.id,
                    "Fecha": fecha.strftime("%d/%m/%Y"),
                    "Día": dia_semana_es.capitalize(),
                    "Grupo": grupo.nombre,
                    "Maestro": f"{maestroinfo.nombre} {maestroinfo.apellido}" if maestroinfo else "No disponible",
                    "Materia": materia.nombre if materia else "No disponible",
                    "Hora Inicio": horario.hora_inicio,
                    "Hora Fin": horario.hora_fin,
                    "Estado": estado_asistencia,
                    "Observaciones": asistencia.observaciones or "",
                    "Registrado por": f"{usuario_asistencia.rol.nombre}: {usuario_asistencia.nombre} {usuario_asistencia.apellido}"
                })
    
    if not asistencias_data:
        raise HTTPException(status_code=404, detail="No hay registros de asistencia para los filtros especificados")

    return JSONResponse(content=asistencias_data)


