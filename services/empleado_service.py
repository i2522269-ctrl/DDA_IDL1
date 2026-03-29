# ================================================================
# SERVICIO DE EMPLEADOS - CREACIÓN Y PERSISTENCIA SIMPLIFICADO
# ================================================================
#
# PROPÓSITO: Manejar la creación de empleados y guardar en JSON
#
# SIN TECNICO: Ahora todos son Trabajadores con puesto abreviado
#
# ================================================================

import json
import os

from models.trabajador import Trabajador


# ================================================================
# CONSTANTES
# ================================================================

RUTA_JSON = "data/empleados.json"

# ================================================================
# OPCIONES DE PUESTOS (Dropdown)
# ================================================================

PUESTOS_DISPONIBLES = {
    "GER": "Gerente General",
    "JEF MK": "Jefe de Marketing",
    "JEF SIS": "Jefe de Sistemas",
    "JEF PRO": "Jefe de Producción",
    "JEF LOG": "Jefe de Logística",
    "JEF FIN": "Jefe de Finanzas",
    "AST MK": "Asistente de Marketing",
    "AST SIS": "Asistente de Sistemas",
    "AST PRO": "Asistente de Producción",
    "AST LOG": "Asistente de Logística",
    "AST FIN": "Asistente de Finanzas",
    "TEC MK": "Técnico de Marketing",
    "TEC SIS": "Técnico de Sistemas",
    "TEC PRO": "Técnico de Producción",
    "TEC LOG": "Técnico de Logística",
    "TEC FIN": "Técnico de Finanzas",
}


# ================================================================
# FUNCIONES DE CONVERSIÓN
# ================================================================

def empleado_a_diccionario(emp):
    """
    Convierte un objeto Trabajador a un diccionario.
    """
    if emp._jefe_inmediato is not None:
        nombre_jefe = emp._jefe_inmediato.get_nombre()
    else:
        nombre_jefe = None
    
    return {
        "nombre": emp._nombre,
        "puesto": emp._puesto,
        "puesto_completo": emp._puesto_completo,
        "estado": emp._estado,
        "jefe_inmediato": nombre_jefe
    }


def diccionario_a_empleado(dicc, lista_obj):
    """
    Convierte un diccionario a un objeto Trabajador.
    """
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
        puesto_completo=dicc["puesto_completo"],
        estado=dicc["estado"],
        jefe_inmediato=jefe
    )


# ================================================================
# PERSISTENCIA
# ================================================================

def guardar_empleados(lista_empleados):
    """
    Guarda la lista de empleados en un archivo JSON.
    """
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
    """
    Carga los empleados desde el archivo JSON.
    """
    if not os.path.exists(RUTA_JSON):
        print("No existe archivo JSON. Se creará al guardar.")
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
                puesto_completo=dicc["puesto_completo"],
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
    
    Args:
        nombre (str): Nombre completo
        puesto (str): Código abreviado del puesto (ej: "JEF MK")
        estado (str): Estado laboral (A, TC, D, R)
        jefe (Trabajador, optional): Objeto del jefe
    
    Returns:
        Trabajador: Nuevo empleado
    
    Raises:
        ValueError: Si algún dato no es válido
    """
    # Validaciones
    if not nombre or nombre.strip() == "":
        raise ValueError("El nombre es obligatorio")
    
    if puesto not in PUESTOS_DISPONIBLES:
        raise ValueError(f"Puesto inválido. Use: {list(PUESTOS_DISPONIBLES.keys())}")
    
    estados_validos = ["A", "TC", "D", "R"]
    if estado not in estados_validos:
        raise ValueError(f"Estado inválido. Use: {estados_validos}")
    
    # Obtener nombre completo del puesto
    puesto_completo = PUESTOS_DISPONIBLES[puesto]
    
    # Crear objeto
    nuevo_empleado = Trabajador(
        nombre=nombre.strip(),
        puesto=puesto,
        puesto_completo=puesto_completo,
        estado=estado,
        jefe_inmediato=jefe
    )
    
    return nuevo_empleado


def eliminar_empleado(lista_empleados, nombre):
    """
    Elimina un empleado de la lista por nombre.
    """
    lista_nueva = [emp for emp in lista_empleados if emp.get_nombre() != nombre]
    eliminado = len(lista_nueva) < len(lista_empleados)
    return lista_nueva, eliminado
