# ================================================================
# MODELOS - MÓDULO DE CLASES (POO)
# ================================================================
# 
# Este paquete contiene las clases del sistema:
#   - Trabajador: Clase padre con atributos comunes
#   - Tecnico: Clase hija con atributos específicos
#
# ================================================================

# Importamos las clases para que se puedan usar desde outside
# Ejemplo: from models.trabajador import Trabajador
from .trabajador import Trabajador
from .tecnico import Tecnico

# Exportamos las clases para facilitar las importaciones
__all__ = ['Trabajador', 'Tecnico']
