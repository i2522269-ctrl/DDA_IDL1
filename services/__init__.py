# ================================================================
# SERVICES - MÓDULO DE LÓGICA DE NEGOCIO
# ================================================================
#
# Este paquete contiene las funciones de servicio:
#   - generar_reporte_html(): Genera el archivo HTML
#   - crear_empleado(): Crea un nuevo empleado
#   - cargar_empleados(): Carga desde JSON
#   - guardar_empleados(): Guarda en JSON
#
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
