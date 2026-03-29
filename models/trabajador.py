# ================================================================
# CLASE TRABAJADOR - CLASE PADRE (POO)
# ================================================================
# 
# PROPÓSITO: Representar a un trabajador genérico de la empresa.
# 
# CONCEPTOS POO APLICADOS:
#   - ENCAPSULAMIENTO: Usamos "_" antes del atributo para indicar
#                      que es "privado" (convenio Python)
#   - GETTERS: Métodos para LEER datos (get_nombre, get_estado, etc.)
#   - SETTERS: Métodos para MODIFICAR datos (set_nombre, set_estado, etc.)
#
# ATRIBUTOS:
#   - _nombre: Nombre completo del trabajador
#   - _puesto: Cargo que ocupa en la empresa
#   - _estado: Situación laboral (A=Activo, TC=Contrato, D=Despido, R=Renuncia)
#   - _jefe_inmediato: Referencia al objeto de su jefe (None si es Gerente)
#
# ================================================================

class Trabajador:
    """
    Clase padre que representa a un trabajador de la empresa.
    
    Args:
        nombre (str): Nombre completo del trabajador
        puesto (str): Cargo o posición en la empresa
        estado (str): Estado laboral (A, TC, D, R)
        jefe_inmediato (Trabajador, optional): Referencia al objeto de su jefe directo
    
    Ejemplo:
        jefe = Trabajador("Roberto Carlos", "Gerente General", "A")
        emp = Trabajador("Juan Pérez", "Asistente", "A", jefe)
    """
    
    # ================================================================
    # CONSTRUCTOR - Se ejecuta al crear un objeto con "new"
    # ================================================================
    def __init__(self, nombre, puesto, estado, jefe_inmediato=None):
        """
        Constructor: Inicializa los atributos del trabajador.
        
        El parámetro jefe_inmediato=None significa que es OPTIONAL.
        Si no se pasa, el valor será None (nulo).
        El Gerente General NO tiene jefe, por eso empieza en None.
        """
        self._nombre = nombre              # Nombre completo
        self._puesto = puesto              # Puesto o cargo
        self._estado = estado              # Código de estado laboral
        self._jefe_inmediato = jefe_inmediato  # Referencia al objeto jefe (None si es Gerente)
    
    # ================================================================
    # GETTERS - Métodos para LEER datos (lectura protegida)
    # ================================================================
    
    def get_nombre(self):
        """
        Retorna el nombre completo del trabajador.
        
        Returns:
            str: Nombre del trabajador
        
        Ejemplo:
            emp.get_nombre() → "Juan Pérez"
        """
        return self._nombre
    
    def get_puesto(self):
        """
        Retorna el puesto/cargo del trabajador.
        
        Returns:
            str: Puesto del trabajador
        
        Ejemplo:
            emp.get_puesto() → "Asistente de Marketing"
        """
        return self._puesto
    
    def get_resumen(self):
        """
        Retorna un resumen del puesto del trabajador.
        NOTA: Este método será SOBRESCRITO (polimorfismo) en la clase Tecnico
              para incluir los años de experiencia.
        
        Returns:
            str: Información del puesto
        
        Ejemplo:
            emp.get_resumen() → "Puesto: Asistente de Marketing"
        """
        # Formateamos el puesto con el prefijo "Puesto: "
        return f"Puesto: {self._puesto}"
    
    def get_estado(self):
        """
        Traduce el código de estado a texto legible.
        
        Estados posibles:
            A  → Activo (trabajando actualmente)
            TC → Término de contrato (contrato finalizado)
            D  → Despido (despedido por la empresa)
            R  → Renuncia (renunció voluntariamente)
        
        Returns:
            str: Descripción del estado laboral
        
        Ejemplo:
            emp.get_estado() → "Activo"
        """
        # Diccionario que relaciona código → texto descriptivo
        estados = {
            "A": "Activo",
            "TC": "Término de contrato",
            "D": "Despido",
            "R": "Renuncia"
        }
        # .get() retorna el valor si existe, o "Estado desconocido" si no
        return estados.get(self._estado, "Estado desconocido")
    
    def get_jefe_inmediato(self):
        """
        Retorna el nombre del jefe inmediato del trabajador.
        
        Lógica:
            - Si _jefe_inmediato tiene valor (no es None): 
              → Llamamos a get_nombre() del objeto jefe
            - Si _jefe_inmediato es None: 
              → Es el Gerente General (Alta Dirección)
        
        Returns:
            str: Nombre del jefe o mensaje especial
        
        Ejemplo:
            emp.get_jefe_inmediato() → "Lucía Méndez"
        """
        # Condicional: verificamos si hay jefe o no
        if self._jefe_inmediato:
            # Existe un jefe, retornamos su nombre
            # Llamamos al método get_nombre() del objeto jefe
            return self._jefe_inmediato.get_nombre()
        else:
            # No hay jefe (es el Gerente), retornamos mensaje especial
            return "Sin jefe (Alta Dirección)"
    
    # ================================================================
    # SETTERS - Métodos para MODIFICAR datos (mantenimiento)
    # ================================================================
    
    def set_nombre(self, nuevo_nombre):
        """
        Modifica el nombre del trabajador.
        
        Args:
            nuevo_nombre (str): Nuevo nombre a asignar
        """
        self._nombre = nuevo_nombre
    
    def set_puesto(self, nuevo_puesto):
        """
        Modifica el puesto del trabajador.
        
        Args:
            nuevo_puesto (str): Nuevo puesto a asignar
        """
        self._puesto = nuevo_puesto
    
    def set_estado(self, nuevo_estado):
        """
        Modifica el estado laboral del trabajador.
        
        Args:
            nuevo_estado (str): Nuevo estado (A, TC, D, R)
        """
        self._estado = nuevo_estado
    
    def set_jefe_inmediato(self, nuevo_jefe):
        """
        Modifica el jefe inmediato del trabajador.
        
        Args:
            nuevo_jefe (Trabajador): Nuevo objeto jefe
        """
        self._jefe_inmediato = nuevo_jefe
    
    # ================================================================
    # MÉTODO ADICIONAL - Para depuración
    # ================================================================
    
    def __str__(self):
        """
        Método especial que define cómo se muestra el objeto como texto.
        Se llama automáticamente cuando usamos print(objeto)
        
        Returns:
            str: Representación textual del trabajador
        """
        return f"Trabajador({self._nombre}, {self._puesto}, {self._estado})"
