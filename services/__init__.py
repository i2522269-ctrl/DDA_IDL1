# ================================================================
# SERVICES - MÓDULO DE LÓGICA DE NEGOCIO
# ================================================================

from .reporte_service import generar_reporte_html
from .empleado_service import (
    crear_empleado,
    cargar_empleados,
    guardar_empleados
)

__all__ = [
    'generar_reporte_html',
    'crear_empleado',
    'cargar_empleados',
    'guardar_empleados'
]
