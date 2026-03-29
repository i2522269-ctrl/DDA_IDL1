# ================================================================
# SERVICIO DE EMPLEADOS - CREACIÓN Y PERSISTENCIA
# ================================================================
#
# PROPÓSITO: Manejar la creación de empleados y guardar datos en JSON
#
# FUNCIONALIDADES:
#   - crear_empleado(): Valida y crea nuevo empleado
#   - cargar_empleados(): Lee del JSON y crea objetos
#   - guardar_empleados(): Guarda el array en JSON
#
# CONCEPTOS:
#   - Persistencia de datos (archivos JSON)
#   - Serialización (objeto → dict → JSON)
#   - Deserialización (JSON → dict → objeto)
#
# ================================================================

import json
import os

from models.trabajador import Trabajador
from models.tecnico import Tecnico


# ================================================================
# CONSTANTES
# ================================================================

# Ruta del archivo JSON donde se guardan los empleados
RUTA_JSON = "data/empleados.json"


# ================================================================
# FUNCIONES DE CONVERSIÓN (Serialización/Deserialización)
# ================================================================

def empleado_a_diccionario(emp):
    """
    Convierte un objeto empleado a un diccionario.
    NECESARIO para guardar en JSON (JSON no guarda objetos, solo datos simples).
    
    Args:
        emp: Objeto Trabajador o Tecnico
    
    Returns:
        dict: Diccionario con los datos del empleado
    
    Ejemplo:
        emp = Trabajador("Juan", "Asistente", "A", None)
        dicc = empleado_a_diccionario(emp)
        # Resultado: {"tipo": "Trabajador", "nombre": "Juan", ...}
    """
    # Determinar si es Técnico o Trabajador
    tipo = "Tecnico" if isinstance(emp, Tecnico) else "Trabajador"
    
    # Obtener el nombre del jefe (si existe)
    # Si es None, guardar None en el JSON
    if emp._jefe_inmediato is not None:
        nombre_jefe = emp._jefe_inmediato.get_nombre()
    else:
        nombre_jefe = None
    
    # Crear diccionario con los datos
    datos = {
        "tipo": tipo,
        "nombre": emp._nombre,
        "puesto": emp._puesto,
        "estado": emp._estado,
        "jefe_inmediato": nombre_jefe,
        "anios_experiencia": emp._anios_experiencia if tipo == "Tecnico" else None
    }
    
    return datos


def diccionario_a_empleado(dicc, lista_obj):
    """
    Convierte un diccionario a un objeto empleado.
    NECESARIO para cargar desde JSON (JSON guarda datos, hay que crear objetos).
    
    Args:
        dicc (dict): Diccionario con los datos del empleado
        lista_obj (list): Lista de objetos ya creados (para buscar el jefe)
    
    Returns:
        Trabajador or Tecnico: Objeto empleado creado
    
    Ejemplo:
        dicc = {"tipo": "Tecnico", "nombre": "Juan", ...}
        emp = diccionario_a_empleado(dicc, lista_objetos)
    """
    # Buscar el objeto del jefe por nombre
    # Si no hay jefe (None), pasar None al constructor
    jefe = None
    if dicc["jefe_inmediato"] is not None:
        # Recorrer la lista para encontrar el jefe por nombre
        for obj in lista_obj:
            if obj.get_nombre() == dicc["jefe_inmediato"]:
                jefe = obj
                break
    
    # Crear el objeto según el tipo
    if dicc["tipo"] == "Tecnico":
        # Crear Técnico (con años de experiencia)
        emp = Tecnico(
            nombre=dicc["nombre"],
            puesto=dicc["puesto"],
            estado=dicc["estado"],
            jefe_inmediato=jefe,
            anios_experiencia=dicc["anios_experiencia"]
        )
    else:
        # Crear Trabajador (sin años de experiencia)
        emp = Trabajador(
            nombre=dicc["nombre"],
            puesto=dicc["puesto"],
            estado=dicc["estado"],
            jefe_inmediato=jefe
        )
    
    return emp


# ================================================================
# FUNCIONES DE PERSISTENCIA (Guardar/Cargar)
# ================================================================

def guardar_empleados(lista_empleados):
    """
    Guarda la lista de empleados en un archivo JSON.
    Convierte los objetos a diccionarios y los guarda.
    
    Args:
        lista_empleados (list): Lista de objetos empleado
    
    Returns:
        bool: True si se guardó exitosamente
    
    Flujograma:
        INICIO
          ↓
        Convertir cada objeto → diccionario (empleado_a_diccionario)
          ↓
        Guardar lista de diccionarios en JSON (json.dump)
          ↓
        FIN (archivo guardado)
    """
    try:
        # Crear carpeta 'data' si no existe
        os.makedirs("data", exist_ok=True)
        
        # Convertir cada objeto a diccionario
        lista_diccionarios = []
        for emp in lista_empleados:
            dicc = empleado_a_diccionario(emp)
            lista_diccionarios.append(dicc)
        
        # Guardar en archivo JSON
        # json.dump() convierte Python → JSON y escribe en archivo
        with open(RUTA_JSON, "w", encoding="utf-8") as archivo:
            json.dump(lista_diccionarios, archivo, ensure_ascii=False, indent=2)
        
        return True
    
    except Exception as e:
        print(f"Error al guardar: {e}")
        return False


def cargar_empleados():
    """
    Carga los empleados desde el archivo JSON.
    Crea objetos a partir de los diccionarios guardados.
    
    Returns:
        list: Lista de objetos empleado
    
    Flujograma:
        INICIO
          ↓
        ¿Existe archivo JSON?
        ├── SÍ → Continuar
        └── NO → Devolver lista vacía (no hay datos guardados)
          ↓
        Leer archivo JSON (json.load)
          ↓
        Convertir cada diccionario → objeto (diccionario_a_empleado)
          ↓
        Devolver lista de objetos
          ↓
        FIN
    """
    # Verificar si existe el archivo
    if not os.path.exists(RUTA_JSON):
        print("No existe archivo JSON. Se creará al guardar.")
        return []
    
    try:
        # Leer archivo JSON
        with open(RUTA_JSON, "r", encoding="utf-8") as archivo:
            lista_diccionarios = json.load(archivo)
        
        # Crear objetos a partir de los diccionarios
        # NOTA: Necesitamos crear objetos SIN jefe primero,
        #       porque los jefes pueden estar más adelante en la lista
        lista_objetos = []
        
        # Paso 1: Crear todos los objetos sin jefe (jefe=None)
        for dicc in lista_diccionarios:
            # Crear objeto sin jefe (temporalmente)
            if dicc["tipo"] == "Tecnico":
                emp = Tecnico(
                    nombre=dicc["nombre"],
                    puesto=dicc["puesto"],
                    estado=dicc["estado"],
                    jefe_inmediato=None,  # Temporal
                    anios_experiencia=dicc["anios_experiencia"]
                )
            else:
                emp = Trabajador(
                    nombre=dicc["nombre"],
                    puesto=dicc["puesto"],
                    estado=dicc["estado"],
                    jefe_inmediato=None  # Temporal
                )
            lista_objetos.append(emp)
        
        # Paso 2: Asignar los bosses correctamente
        # Ahora que tenemos todos los objetos, podemos buscarlos por nombre
        for i, dicc in enumerate(lista_diccionarios):
            if dicc["jefe_inmediato"] is not None:
                # Buscar el jefe por nombre en la lista de objetos
                for obj in lista_objetos:
                    if obj.get_nombre() == dicc["jefe_inmediato"]:
                        # Asignar el jefe al empleado
                        lista_objetos[i]._jefe_inmediato = obj
                        break
        
        return lista_objetos
    
    except Exception as e:
        print(f"Error al cargar: {e}")
        return []


# ================================================================
# FUNCIÓN DE CREACIÓN DE EMPLEADOS
# ================================================================

def crear_empleado(nombre, puesto, estado, tipo, jefe=None, anios_experiencia=None):
    """
    Crea un nuevo empleado y lo devuelve.
    
    Args:
        nombre (str): Nombre completo del empleado
        puesto (str): Cargo en la empresa
        estado (str): Estado laboral (A, TC, D, R)
        tipo (str): "Trabajador" o "Tecnico"
        jefe (Trabajador, optional): Objeto del jefe inmediato
        anios_experiencia (int, optional): Solo para Técnicos
    
    Returns:
        Trabajador or Tecnico: El nuevo empleado creado
    
    Validaciones:
        - Nombre no puede estar vacío
        - Puesto no puede estar vacío
        - Estado debe ser válido (A, TC, D, R)
    
    Raises:
        ValueError: Si algún dato no es válido
    """
    # ============================================================
    # VALIDACIONES
    # ============================================================
    
    # Validar nombre
    if not nombre or nombre.strip() == "":
        raise ValueError("El nombre es obligatorio")
    
    # Validar puesto
    if not puesto or puesto.strip() == "":
        raise ValueError("El puesto es obligatorio")
    
    # Validar estado
    estados_validos = ["A", "TC", "D", "R"]
    if estado not in estados_validos:
        raise ValueError(f"Estado inválido. Use: {estados_validos}")
    
    # Validar años de experiencia (solo para Técnicos)
    if tipo == "Tecnico":
        if anios_experiencia is None or anios_experiencia < 0:
            raise ValueError("Los años de experiencia son obligatorios para técnicos")
    
    # ============================================================
    # CREAR EL OBJETO
    # ============================================================
    
    if tipo == "Tecnico":
        # Crear Técnico con años de experiencia
        nuevo_empleado = Tecnico(
            nombre=nombre.strip(),
            puesto=puesto.strip(),
            estado=estado,
            jefe_inmediato=jefe,
            anios_experiencia=anios_experiencia
        )
    else:
        # Crear Trabajador normal
        nuevo_empleado = Trabajador(
            nombre=nombre.strip(),
            puesto=puesto.strip(),
            estado=estado,
            jefe_inmediato=jefe
        )
    
    return nuevo_empleado


# ================================================================
# FUNCIÓN DE ELIMINACIÓN (BONUS)
# ================================================================

def eliminar_empleado(lista_empleados, nombre):
    """
    Elimina un empleado de la lista por nombre.
    
    Args:
        lista_empleados (list): Lista de empleados
        nombre (str): Nombre del empleado a eliminar
    
    Returns:
        tuple: (lista_actualizada, bool_exito)
    """
    lista_nueva = [emp for emp in lista_empleados if emp.get_nombre() != nombre]
    eliminado = len(lista_nueva) < len(lista_empleados)
    return lista_nueva, eliminado
