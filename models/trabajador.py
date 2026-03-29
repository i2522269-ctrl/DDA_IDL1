# ================================================================
# CLASE TRABAJADOR - SISTEMA RRHH
# ================================================================
#
# PROPÓSITO: Representar a un trabajador de la empresa.
# 
# CONCEPTOS POO:
#   - ENCAPSULAMIENTO: Atributos privados con "_"
#   - GETTERS: Métodos para LEER datos
#   - SETTERS: Métodos para MODIFICAR datos
#
# ATRIBUTOS:
#   - _nombre: Nombre completo del trabajador
#   - _puesto: Puesto completo (ej: "Gerente General")
#   - _estado: Estado laboral (A, TC, D, R)
#   - _jefe_inmediato: Referencia al objeto de su jefe
#
# ================================================================

class Trabajador:
    """
    Clase que representa a un trabajador de la empresa.
    """
    
    def __init__(self, nombre, puesto, estado, jefe_inmediato=None):
        """
        Inicializa los datos del trabajador.
        
        Args:
            nombre: Nombre completo
            puesto: Puesto completo en la empresa
            estado: Estado laboral (A, TC, D, R)
            jefe_inmediato: Objeto del jefe (None si es Gerente)
        """
        self._nombre = nombre
        self._puesto = puesto
        self._estado = estado
        self._jefe_inmediato = jefe_inmediato
    
    # ================================================================
    # GETTERS
    # ================================================================
    
    def get_nombre(self):
        """Retorna el nombre completo."""
        return self._nombre
    
    def get_puesto(self):
        """Retorna el puesto completo."""
        return self._puesto
    
    def get_resumen(self):
        """Retorna el puesto para la tabla."""
        return self._puesto
    
    def get_estado(self):
        """
        Traduce el código de estado a texto legible.
        
        Estados:
            A  → Activo (verde)
            TC → Término de contrato (rojo)
            D  → Despido (negro)
            R  → Renuncia (naranja)
        """
        estados = {
            "A": "Activo",
            "TC": "Término de contrato",
            "D": "Despido",
            "R": "Renuncia"
        }
        return estados.get(self._estado, "Desconocido")
    
    def get_estado_codigo(self):
        """Retorna el código de estado (A, TC, D, R)."""
        return self._estado
    
    def get_jefe_inmediato(self):
        """
        Retorna el nombre del jefe inmediato.
        Si no tiene jefe (Gerente), retorna mensaje especial.
        """
        if self._jefe_inmediato:
            return self._jefe_inmediato.get_nombre()
        return "Sin jefe (Alta Dirección)"
    
    # ================================================================
    # SETTERS
    # ================================================================
    
    def set_nombre(self, nuevo_nombre):
        """Modifica el nombre."""
        self._nombre = nuevo_nombre
    
    def set_puesto(self, nuevo_puesto):
        """Modifica el puesto."""
        self._puesto = nuevo_puesto
    
    def set_estado(self, nuevo_estado):
        """Modifica el estado."""
        self._estado = nuevo_estado
    
    def set_jefe_inmediato(self, nuevo_jefe):
        """Modifica el jefe inmediato."""
        self._jefe_inmediato = nuevo_jefe
    
    # ================================================================
    # REPRESENTACIÓN
    # ================================================================
    
    def __str__(self):
        return f"Trabajador({self._nombre}, {self._puesto}, {self._estado})"
