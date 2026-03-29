# ================================================================
# SERVICES - MÓDULO DE LÓGICA DE NEGOCIO
# ================================================================
# 
# Este paquete contiene las funciones de servicio:
#   - generar_reporte_html(): Genera el archivo HTML con la lista de empleados
#
# ================================================================

# Importamos la función para que se pueda usar desde outside
from .reporte_service import generar_reporte_html

# Exportamos las funciones
__all__ = ['generar_reporte_html']
