# ================================================================
# CLASE TRABAJADOR - SISTEMA RRHH SIMPLIFICADO
# ================================================================
#
# PROPÓSITO: Representar a cualquier trabajador de la empresa.
# 
# CONCEPTOS POO APLICADOS:
#   - ENCAPSULAMIENTO: Atributos privados con "_"
#   - GETTERS: Métodos para LEER datos
#   - SETTERS: Métodos para MODIFICAR datos
#
# ATRIBUTOS:
#   - _nombre: Nombre completo del trabajador
#   - _puesto: Puesto abreviado (ej: "JEF MK")
#   - _puesto_completo: Nombre completo del puesto
#   - _estado: Estado laboral (A, TC, D, R)
#   - _jefe_inmediato: Referencia al objeto de su jefe
#
# ================================================================

class Trabajador:
    """
    Clase que representa a un trabajador de la empresa.
    
    Args:
        nombre (str): Nombre completo del trabajador
        puesto (str): Puesto abreviado (ej: "JEF MK", "AST SIS")
        puesto_completo (str): Nombre completo del puesto
        estado (str): Estado laboral (A, TC, D, R)
        jefe_inmediato (Trabajador, optional): Referencia al jefe
    
    Ejemplo:
        gerente = Trabajador("Roberto Carlos", "GER", "Gerente General", "A", None)
        jefe = Trabajador("Lucía", "JEF MK", "Jefe de Marketing", "A", gerente)
    """
    
    # ================================================================
    # CONSTRUCTOR
    # ================================================================
    def __init__(self, nombre, puesto, puesto_completo, estado, jefe_inmediato=None):
        """
        Inicializa los datos del trabajador.
        """
        self._nombre = nombre
        self._puesto = puesto              # Abreviado (ej: "JEF MK")
        self._puesto_completo = puesto_completo  # Completo (ej: "Jefe de Marketing")
        self._estado = estado              # A, TC, D, R
        self._jefe_inmediato = jefe_inmediato  # Referencia al objeto jefe
    
    # ================================================================
    # GETTERS - Leer datos
    # ================================================================
    
    def get_nombre(self):
        """Retorna el nombre completo del trabajador."""
        return self._nombre
    
    def get_puesto(self):
        """Retorna el puesto abreviado."""
        return self._puesto
    
    def get_puesto_completo(self):
        """Retorna el nombre completo del puesto."""
        return self._puesto_completo
    
    def get_resumen(self):
        """Retorna el puesto abreviado para la tabla."""
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
        Si no tiene jefe (es Gerente), retorna mensaje especial.
        """
        if self._jefe_inmediato:
            return self._jefe_inmediato.get_nombre()
        return "Sin jefe (Alta Dirección)"
    
    # ================================================================
    # SETTERS - Modificar datos
    # ================================================================
    
    def set_nombre(self, nuevo_nombre):
        """Modifica el nombre del trabajador."""
        self._nombre = nuevo_nombre
    
    def set_puesto(self, nuevo_puesto):
        """Modifica el puesto abreviado."""
        self._puesto = nuevo_puesto
    
    def set_puesto_completo(self, nuevo_completo):
        """Modifica el nombre completo del puesto."""
        self._puesto_completo = nuevo_completo
    
    def set_estado(self, nuevo_estado):
        """Modifica el estado laboral."""
        self._estado = nuevo_estado
    
    def set_jefe_inmediato(self, nuevo_jefe):
        """Modifica el jefe inmediato."""
        self._jefe_inmediato = nuevo_jefe
    
    # ================================================================
    # REPRESENTACIÓN
    # ================================================================
    
    def __str__(self):
        return f"Trabajador({self._nombre}, {self._puesto}, {self._estado})"
