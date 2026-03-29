# ================================================================
# CLASE TECNICO - CLASE HIJA (HERENCIA + POLIMORFISMO)
# ================================================================
# 
# PROPÓSITO: Representar al personal técnico de la empresa.
# 
# CONCEPTOS POO APLICADOS:
#   - HERENCIA: Tecnico hereda TODOS los atributos y métodos de Trabajador
#   - POLIMORFISMO: Sobrescribimos get_resumen() para incluir experiencia
#   - ENCAPSULAMIENTO: Atributo _anios_experiencia privado
#
# RELACIÓN:
#   Trabajador (padre) ← hereda ← Tecnico (hija)
#
# ATRIBUTOS PROPIOS:
#   - _anios_experiencia: Cantidad de años trabajando como técnico
#
# ================================================================

# Importamos la clase padre para heredar de ella
from .trabajador import Trabajador


class Tecnico(Trabajador):
    """
    Clase hija que representa al personal técnico de la empresa.
    Hereda de Trabajador y añade el atributo de años de experiencia.
    
    Args:
        nombre (str): Nombre completo del técnico
        puesto (str): Cargo técnico específico
        estado (str): Estado laboral (A, TC, D, R)
        jefe_inmediato (Trabajador): Referencia al objeto de su jefe directo
        anios_experiencia (int): Años de experiencia como técnico
    
    Ejemplo:
        jefe_sis = Trabajador("Alan Turing", "Jefe de Sistemas", "A")
        tecnico = Tecnico("Linus Torvalds", "Técnico IT", "A", jefe_sis, 10)
    """
    
    # ================================================================
    # CONSTRUCTOR - Inicializa atributos propios + llama al padre
    # ================================================================
    def __init__(self, nombre, puesto, estado, jefe_inmediato, anios_experiencia):
        """
        Constructor del Técnico.
        
        Pasos:
            1. Llamar al constructor del padre (super().__init__)
            2. Inicializar el atributo propio _anios_experiencia
        
        Args:
            nombre (str): Nombre completo
            puesto (str): Puesto técnico
            estado (str): Estado laboral
            jefe_inmediato (Trabajador): Jefe del técnico
            anios_experiencia (int): Años de experiencia
        """
        # super().__init__() llama al constructor de la clase padre
        # Esto inicializa los atributos heredados: _nombre, _puesto, _estado, _jefe_inmediato
        super().__init__(nombre, puesto, estado, jefe_inmediato)
        
        # Atributo propio de la clase Tecnico
        # NO existe en la clase padre, es exclusivo de los técnicos
        self._anios_experiencia = anios_experiencia
    
    # ================================================================
    # GETTERS PROPIOS - Solo existen en Tecnico
    # ================================================================
    
    def get_anios_experiencia(self):
        """
        Retorna los años de experiencia del técnico.
        
        Returns:
            int: Cantidad de años de experiencia
        
        Ejemplo:
            tecnico.get_anios_experiencia() → 10
        """
        return self._anios_experiencia
    
    # ================================================================
    # SETTER PROPIO - Solo existe en Tecnico
    # ================================================================
    
    def set_anios_experiencia(self, nuevos_anios):
        """
        Modifica los años de experiencia del técnico.
        
        Args:
            nuevos_anios (int): Nueva cantidad de años
        """
        self._anios_experiencia = nuevos_anios
    
    # ================================================================
    # POLIMORFISMO - Sobrescritura de método del padre
    # ================================================================
    
    def get_resumen(self):
        """
        POLIMORFISMO: Sobrescribe el método del padre para incluir experiencia.
        
        El método del padre retorna: "Puesto: [puesto]"
        Este método retorna: "Puesto: [puesto] | Experiencia: [n] años"
        
        Returns:
            str: Resumen con puesto y años de experiencia
        
        Ejemplo:
            tecnico.get_resumen() → "Puesto: Técnico IT | Experiencia: 10 años"
        """
        # Usamos super() para obtener el formato base del padre
        # y luego añadimos la información de experiencia
        resumen_base = super().get_resumen()
        return f"{resumen_base} | Experiencia: {self._anios_experiencia} años"
    
    # ================================================================
    # MÉTODO ADICIONAL - Verificación de nivel
    # ================================================================
    
    def get_nivel_experiencia(self):
        """
        Clasifica al técnico según sus años de experiencia.
        
        Returns:
            str: Nivel de experiencia (Junior, Semi-Senior, Senior)
        
        Ejemplo:
            tecnico.get_nivel_experiencia() → "Senior" (si tiene >= 10 años)
        """
        if self._anios_experiencia < 3:
            return "Junior"
        elif self._anios_experiencia < 7:
            return "Semi-Senior"
        else:
            return "Senior"
    
    # ================================================================
    # SOBRESCRITURA DE __str__ para depuración
    # ================================================================
    
    def __str__(self):
        """
        Método especial: define cómo se muestra el objeto como texto.
        Llama al __str__ del padre y añade información de experiencia.
        
        Returns:
            str: Representación textual del técnico
        """
        return f"Tecnico({self._nombre}, {self._puesto}, {self._anios_experiencia} años)"
