# ================================================================
# SERVICIO DE EMPLEADOS - CREACIÓN Y PERSISTENCIA
# ================================================================

import json
import os

from models.trabajador import Trabajador


# ================================================================
# CONSTANTES
# ================================================================

RUTA_JSON = "data/empleados.json"


# ================================================================
# FUNCIONES DE CONVERSIÓN
# ================================================================

def empleado_a_diccionario(emp):
    """Convierte objeto a diccionario para guardar en JSON."""
    if emp._jefe_inmediato is not None:
        nombre_jefe = emp._jefe_inmediato.get_nombre()
    else:
        nombre_jefe = None
    
    return {
        "nombre": emp._nombre,
        "puesto": emp._puesto,
        "estado": emp._estado,
        "jefe_inmediato": nombre_jefe
    }


def diccionario_a_empleado(dicc, lista_obj):
    """Convierte diccionario a objeto."""
    # Buscar el jefe por nombre
    jefe = None
    if dicc["jefe_inmediato"] is not None:
        for obj in lista_obj:
            if obj.get_nombre() == dicc["jefe_inmediato"]:
                jefe = obj
                break
    
    return Trabajador(
        nombre=dicc["nombre"],
        puesto=dicc["puesto"],
        estado=dicc["estado"],
        jefe_inmediato=jefe
    )


# ================================================================
# PERSISTENCIA
# ================================================================

def guardar_empleados(lista_empleados):
    """Guarda la lista de empleados en JSON."""
    try:
        os.makedirs("data", exist_ok=True)
        
        lista_diccionarios = []
        for emp in lista_empleados:
            lista_diccionarios.append(empleado_a_diccionario(emp))
        
        with open(RUTA_JSON, "w", encoding="utf-8") as archivo:
            json.dump(lista_diccionarios, archivo, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"Error al guardar: {e}")
        return False


def cargar_empleados():
    """Carga los empleados desde el archivo JSON."""
    if not os.path.exists(RUTA_JSON):
        print("No existe archivo JSON.")
        return []
    
    try:
        with open(RUTA_JSON, "r", encoding="utf-8") as archivo:
            lista_diccionarios = json.load(archivo)
        
        # Crear objetos sin jefe primero
        lista_objetos = []
        for dicc in lista_diccionarios:
            emp = Trabajador(
                nombre=dicc["nombre"],
                puesto=dicc["puesto"],
                estado=dicc["estado"],
                jefe_inmediato=None
            )
            lista_objetos.append(emp)
        
        # Asignar los bosses
        for i, dicc in enumerate(lista_diccionarios):
            if dicc["jefe_inmediato"] is not None:
                for obj in lista_objetos:
                    if obj.get_nombre() == dicc["jefe_inmediato"]:
                        lista_objetos[i]._jefe_inmediato = obj
                        break
        
        return lista_objetos
    
    except Exception as e:
        print(f"Error al cargar: {e}")
        return []


# ================================================================
# CREACIÓN DE EMPLEADOS
# ================================================================

def crear_empleado(nombre, puesto, estado, jefe=None):
    """
    Crea un nuevo empleado.
    """
    # Validaciones
    if not nombre or nombre.strip() == "":
        raise ValueError("El nombre es obligatorio")
    
    if not puesto or puesto.strip() == "":
        raise ValueError("El puesto es obligatorio")
    
    estados_validos = ["A", "TC", "D", "R"]
    if estado not in estados_validos:
        raise ValueError(f"Estado inválido")
    
    # Crear objeto
    nuevo_empleado = Trabajador(
        nombre=nombre.strip(),
        puesto=puesto.strip(),
        estado=estado,
        jefe_inmediato=jefe
    )
    
    return nuevo_empleado


def eliminar_empleado(lista_empleados, nombre):
    """Elimina un empleado de la lista."""
    lista_nueva = [emp for emp in lista_empleados if emp.get_nombre() != nombre]
    eliminado = len(lista_nueva) < len(lista_empleados)
    return lista_nueva, eliminado
