# ================================================================
# SCRIPT EDUCATIVO: SISTEMA RRHH - BUSINESS CORPORATION
# ================================================================
# 
# PROPÓSITO: Aprender POO con un ejemplo completo y documentado.
# 
# ESTE SCRIPT:
#   ✓ Demuestra HERENCIA (Tecnico hereda de Trabajador)
#   ✓ Demuestra POLIMORFISMO (get_resumen() se comporta diferente)
#   ✓ Demuestra ENCAPSULAMIENTO (_atributos con getters/setters)
#   ✓ Usa ARRAY DE OBJETOS (lista de instancias)
#   ✓ Genera TABLAS HTML con comandos nativos de Python
#   ✓ Implementa FLUJOGRAMA de procesos como comentarios
#
# CONCEPTOS CUBIERTOS:
#   - Clases y objetos
#   - Herencia (padre → hija)
#   - Polimorfismo (sobreescritura de métodos)
#   - Encapsulamiento (atributos privados, getters/setters)
#   - Listas (arrays en Python)
#   - Manejo de archivos (open, write, with)
#   - Estructuras repetitivas (for...in)
#
# AUTOR: Estudiante DDA/IDL1
# FECHA: 2026
#
# ================================================================


# ================================================================
# PASO 1: IMPORTAR LAS CLASES
# ================================================================
#
# Antes de usar una clase, debemos importarla.
# Usamos "from" para importar desde el paquete "models"
#
from models.trabajador import Trabajador
from models.tecnico import Tecnico


# ================================================================
# FLUJOGRAMA DE PROCESOS (INTEGRADO COMO COMENTARIOS)
# ================================================================
#
#     ┌─────────────────────────────────────────────────────────┐
#     │                    INICIO                               │
#     └─────────────────────────┬───────────────────────────────┘
#                               ↓
#     ┌─────────────────────────────────────────────────────────┐
#     │ PASO 1: Crear objetos (INSTANCIACIÓN)                 │
#     │         Instanciar Gerente, Jefes, Asistentes, Técnicos│
#     │                                                         │
#     │   gerente = Trabajador("Roberto", "Gerente", "A")      │
#     │   jefe = Trabajador("Lucía", "Jefe Marketing", "A")   │
#     │   tecnico = Tecnico("Linus", "Técnico", "A", jefe, 10)│
#     └─────────────────────────┬───────────────────────────────┘
#                               ↓
#     ┌─────────────────────────────────────────────────────────┐
#     │ PASO 2: Almacenar en ARRAY (LISTA DE PYTHON)           │
#     │         Juntar todos los objetos en una lista           │
#     │                                                         │
#     │   lista_empleados = [gerente, jefe, tecnico, ...]     │
#     └─────────────────────────┬───────────────────────────────┘
#                               ↓
#     ┌─────────────────────────────────────────────────────────┐
#     │ PASO 3: Abrir archivo HTML                              │
#     │         with open("archivo.html", "w") as archivo:      │
#     │                                                         │
#     │   - Modo "w" = write (escritura)                       │
#     │   - "with" = cierra automáticamente                    │
#     │   - encoding="utf-8" = caracteres especiales           │
#     └─────────────────────────┬───────────────────────────────┘
#                               ↓
#                         ┌─────┴─────┐
#                         │   FOR     │◄──────────────────┐
#                         │ emp in    │                   │
#                         │ lista     │                   │
#                         └─────┬─────┘                   │
#                               ↓                          │
#     ┌─────────────────────────────────────────────────────────┐
#     │ PASO 4: Extraer datos con GETTERS (POO)                │
#     │                                                         │
#     │   n = emp.get_nombre()          → "Lucía Méndez"       │
#     │   r = emp.get_resumen()         → "Puesto: Jefe..."    │
#     │   j = emp.get_jefe_inmediato()  → "Roberto Carlos"     │
#     │   e = emp.get_estado()          → "Activo"            │
#     └─────────────────────────┬───────────────────────────────┘
#                               ↓
#     ┌─────────────────────────────────────────────────────────┐
#     │ PASO 5: Escribir fila HTML                             │
#     │         archivo.write(f"<tr><td>{n}</td>...</tr>")     │
#     │                                                         │
#     │   - f-string para insertar variables                   │
#     │   - Etiquetas <tr> = fila, <td> = celda                │
#     └─────────────────────────┬───────────────────────────────┘
#                               ↓
#                         ┌─────┴─────┐
#                         │¿Hay más?   │
#                         └─────┬─────┘
#                              SÍ
#                               │
#                              NO
#                               ↓
#     ┌─────────────────────────────────────────────────────────┐
#     │ PASO 6: Cerrar archivo (automático con "with")          │
#     │         Fin del bloque with → archivo.close()          │
#     └─────────────────────────┬───────────────────────────────┘
#                               ↓
#     ┌─────────────────────────────────────────────────────────┐
#     │                    FIN                                  │
#     │    → Archivo reporte_rrhh.html generado                │
#     └─────────────────────────────────────────────────────────┘
#
# ================================================================


# ================================================================
# PASO 1: CREAR OBJETOS (INSTANCIACIÓN)
# ================================================================
#
# SINTAXIS DE CREACIÓN DE OBJETOS:
#   objeto = NombreClase(param1, param2, ...)
#
# PARAMETROS DEL CONSTRUCTOR:
#   Trabajador(nombre, puesto, estado, jefe_inmediato)
#   Tecnico(nombre, puesto, estado, jefe_inmediato, anios_experiencia)
#
# NOTA: jefe_inmediato es una REFERENCIA AL OBJETO del jefe
#       No es el nombre, es el OBJETO completo
#

# ───────────────────────────────────────────────────────────────
# GERENTE GENERAL (Nivel más alto de la jerarquía)
# ───────────────────────────────────────────────────────────────
# El gerente NO tiene jefe inmediato, por eso jefe_inmediato=None
gerente = Trabajador(
    nombre="Roberto Carlos",
    puesto="Gerente General",
    estado="A",
    jefe_inmediato=None  # No tiene jefe (es el más alto)
)

# ───────────────────────────────────────────────────────────────
# JEFES DE ÁREA (5 en total)
# ───────────────────────────────────────────────────────────────
# Todos los jefes tienen como jefe_inmediato al GERENTE

jefe_mkt = Trabajador(
    nombre="Lucía Méndez",
    puesto="Jefe de Marketing",
    estado="A",
    jefe_inmediato=gerente  # El jefe de Marketing reporta al Gerente
)

jefe_sis = Trabajador(
    nombre="Alan Turing",
    puesto="Jefe de Sistemas",
    estado="A",
    jefe_inmediato=gerente
)

jefe_pro = Trabajador(
    nombre="Henry Ford",
    puesto="Jefe de Producción",
    estado="A",
    jefe_inmediato=gerente
)

jefe_log = Trabajador(
    nombre="Jeff Bezos",
    puesto="Jefe de Logística",
    estado="TC",  # Término de contrato
    jefe_inmediato=gerente
)

jefe_fin = Trabajador(
    nombre="Warren Buffett",
    puesto="Jefe de Finanzas",
    estado="R",  # Renuncia
    jefe_inmediato=gerente
)

# ───────────────────────────────────────────────────────────────
# ASISTENTES (1 por cada jefe de área, 5 en total)
# ───────────────────────────────────────────────────────────────
# Cada asistente tiene como jefe_inmediato a su JEFErespectivo

asistente_mkt = Trabajador(
    nombre="Juan Pérez",
    puesto="Asistente de Marketing",
    estado="A",
    jefe_inmediato=jefe_mkt  # Reporta al Jefe de Marketing
)

asistente_sis = Trabajador(
    nombre="Ada Lovelace",
    puesto="Asistente de Sistemas",
    estado="A",
    jefe_inmediato=jefe_sis
)

asistente_pro = Trabajador(
    nombre="Carlos Slim",
    puesto="Asistente de Producción",
    estado="D",  # Despido
    jefe_inmediato=jefe_pro
)

asistente_log = Trabajador(
    nombre="Marie Curie",
    puesto="Asistente de Logística",
    estado="A",
    jefe_inmediato=jefe_log
)

asistente_fin = Trabajador(
    nombre="Nikola Tesla",
    puesto="Asistente de Finanzas",
    estado="A",
    jefe_inmediato=jefe_fin
)

# ───────────────────────────────────────────────────────────────
# PERSONAL TÉCNICO (3 por cada área, 15 en total)
# ───────────────────────────────────────────────────────────────
# La clase Tecnico HEREDA de Trabajador y añade anios_experiencia
# SINTAXIS: Tecnico(nombre, puesto, estado, jefe, experiencia)
#
# POLIMORFISMO EN ACCIÓN:
#   - get_resumen() de Trabajador → "Puesto: X"
#   - get_resumen() de Tecnico → "Puesto: X | Experiencia: N años"
#
# Técnicos de Marketing (3)
tecnico_mkt_1 = Tecnico(
    nombre="Elon Musk",
    puesto="Técnico de Marketing",
    estado="A",
    jefe_inmediato=jefe_mkt,
    anios_experiencia=5
)

tecnico_mkt_2 = Tecnico(
    nombre="Grace Hopper",
    puesto="Técnico de Marketing",
    estado="A",
    jefe_inmediato=jefe_mkt,
    anios_experiencia=9
)

tecnico_mkt_3 = Tecnico(
    nombre="Margaret Hamilton",
    puesto="Técnico de Marketing",
    estado="A",
    jefe_inmediato=jefe_mkt,
    anios_experiencia=11
)

# Técnicos de Sistemas (3)
tecnico_sis_1 = Tecnico(
    nombre="Linus Torvalds",
    puesto="Técnico de Sistemas",
    estado="A",
    jefe_inmediato=jefe_sis,
    anios_experiencia=10
)

tecnico_sis_2 = Tecnico(
    nombre="Steve Wozniak",
    puesto="Técnico de Sistemas",
    estado="A",
    jefe_inmediato=jefe_sis,
    anios_experiencia=15
)

tecnico_sis_3 = Tecnico(
    nombre="Bill Gates",
    puesto="Técnico de Sistemas",
    estado="TC",
    jefe_inmediato=jefe_sis,
    anios_experiencia=8
)

# Técnicos de Producción (3)
tecnico_pro_1 = Tecnico(
    nombre="Tim Berners-Lee",
    puesto="Técnico de Producción",
    estado="A",
    jefe_inmediato=jefe_pro,
    anios_experiencia=12
)

tecnico_pro_2 = Tecnico(
    nombre="Vint Cerf",
    puesto="Técnico de Producción",
    estado="A",
    jefe_inmediato=jefe_pro,
    anios_experiencia=7
)

tecnico_pro_3 = Tecnico(
    nombre="Ken Thompson",
    puesto="Técnico de Producción",
    estado="A",
    jefe_inmediato=jefe_pro,
    anios_experiencia=14
)

# Técnicos de Logística (3)
tecnico_log_1 = Tecnico(
    nombre="Alan Kay",
    puesto="Técnico de Logística",
    estado="A",
    jefe_inmediato=jefe_log,
    anios_experiencia=6
)

tecnico_log_2 = Tecnico(
    nombre="Dennis Ritchie",
    puesto="Técnico de Logística",
    estado="A",
    jefe_inmediato=jefe_log,
    anios_experiencia=9
)

tecnico_log_3 = Tecnico(
    nombre="Bjarne Stroustrup",
    puesto="Técnico de Logística",
    estado="R",
    jefe_inmediato=jefe_log,
    anios_experiencia=4
)

# Técnicos de Finanzas (3)
tecnico_fin_1 = Tecnico(
    nombre="Larry Page",
    puesto="Técnico de Finanzas",
    estado="A",
    jefe_inmediato=jefe_fin,
    anios_experiencia=8
)

tecnico_fin_2 = Tecnico(
    nombre="Sergey Brin",
    puesto="Técnico de Finanzas",
    estado="A",
    jefe_inmediato=jefe_fin,
    anios_experiencia=6
)

tecnico_fin_3 = Tecnico(
    nombre="Larry Ellison",
    puesto="Técnico de Finanzas",
    estado="A",
    jefe_inmediato=jefe_fin,
    anios_experiencia=10
)


# ================================================================
# PASO 2: CREAR ARRAY DE OBJETOS (LISTA EN PYTHON)
# ================================================================
#
# Un ARRAY en Python se llama LISTA y se define con corchetes [].
# Cada elemento es un OBJETO (instancia de una clase).
#
# SINTAXIS:
#   lista = [elemento1, elemento2, elemento3, ...]
#
# VENTAJA DE USAR LISTA:
#   - Podemos recorrerla con un FOR
#   - Podemos agregar/quitar elementos dinámicamente
#   - Accedemos por índice: lista[0], lista[1], etc.
#

lista_empleados = [
    # Nivel 1: Gerente (1)
    gerente,
    
    # Nivel 2: Jefes de Área (5)
    jefe_mkt,
    jefe_sis,
    jefe_pro,
    jefe_log,
    jefe_fin,
    
    # Nivel 3: Asistentes (5)
    asistente_mkt,
    asistente_sis,
    asistente_pro,
    asistente_log,
    asistente_fin,
    
    # Nivel 4: Técnicos (15)
    tecnico_mkt_1,
    tecnico_mkt_2,
    tecnico_mkt_3,
    tecnico_sis_1,
    tecnico_sis_2,
    tecnico_sis_3,
    tecnico_pro_1,
    tecnico_pro_2,
    tecnico_pro_3,
    tecnico_log_1,
    tecnico_log_2,
    tecnico_log_3,
    tecnico_fin_1,
    tecnico_fin_2,
    tecnico_fin_3
]

# ================================================================
# CONTADORES POR NIVEL (PARA VERIFICACIÓN)
# ================================================================
print("=" * 60)
print("VERIFICACIÓN DE JERARQUÍA EMPRESARIAL")
print("=" * 60)
print(f"Gerentes:     1 (Roberto Carlos)")
print(f"Jefes:        5 (Marketing, Sistemas, Producción, Logística, Finanzas)")
print(f"Asistentes:   5 (1 por cada jefe)")
print(f"Técnicos:    15 (3 por cada área)")
print(f"TOTAL:       {len(lista_empleados)} EMPLEADOS")
print("=" * 60)
print()


# ================================================================
# PASO 3: GENERAR REPORTE HTML
# ================================================================
#
# Importamos la función del servicio
from services.reporte_service import generar_reporte_html

# Llamamos a la función que genera el archivo HTML
# Esta función:
#   1. Abre el archivo en modo escritura
#   2. Escribe la estructura HTML
#   3. Recorre la lista con un FOR
#   4. Por cada empleado, extrae datos con getters
#   5. Escribe la fila en la tabla
#   6. Cierra el archivo automáticamente
#
print("Generando reporte HTML...")
print("-" * 40)

archivo_generado = generar_reporte_html(lista_empleados)

print(f"¡ÉXITO! Reporte generado: {archivo_generado}")
print()
print("Para ver el reporte:")
print(f"  1. Abre el archivo '{archivo_generado}' en tu navegador")
print("  2. O ejecuta: start reporte_rrhh.html (Windows)")
print()


# ================================================================
# DEMOSTRACIÓN DE POO (PARA APRENDER)
# ================================================================
print("=" * 60)
print("DEMOSTRACIÓN DE CONCEPTOS POO")
print("=" * 60)
print()

# ───────────────────────────────────────────────────────────────
# 1. ENCAPSULAMIENTO: Atributos privados con "_"
# ───────────────────────────────────────────────────────────────
print("1. ENCAPSULAMIENTO")
print("   Los atributos usan '_' para indicar que son privados")
print(f"   gerente._nombre = '{gerente._nombre}'")
print(f"   gerente._puesto = '{gerente._puesto}'")
print(f"   tecnico_sis_1._anios_experiencia = {tecnico_sis_1._anios_experiencia}")
print()

# ───────────────────────────────────────────────────────────────
# 2. GETTERS: Métodos para LEER datos
# ───────────────────────────────────────────────────────────────
print("2. GETTERS (Lectura de datos)")
print("   Usamos get_nombre(), get_estado(), etc.")
print(f"   gerente.get_nombre() = '{gerente.get_nombre()}'")
print(f"   gerente.get_estado() = '{gerente.get_estado()}'")
print(f"   gerente.get_jefe_inmediato() = '{gerente.get_jefe_inmediato()}'")
print()

# ───────────────────────────────────────────────────────────────
# 3. HERENCIA: Tecnico hereda de Trabajador
# ───────────────────────────────────────────────────────────────
print("3. HERENCIA (Tecnico hereda de Trabajador)")
print(f"   isinstance(tecnico_sis_1, Tecnico) = {isinstance(tecnico_sis_1, Tecnico)}")
print(f"   isinstance(tecnico_sis_1, Trabajador) = {isinstance(tecnico_sis_1, Trabajador)}")
print(f"   issubclass(Tecnico, Trabajador) = {issubclass(Tecnico, Trabajador)}")
print()

# ───────────────────────────────────────────────────────────────
# 4. POLIMORFISMO: get_resumen() diferente en cada clase
# ───────────────────────────────────────────────────────────────
print("4. POLIMORFISMO (get_resumen() se comporta diferente)")
print("   TRABAJADOR.get_resumen():")
print(f"     {asistente_mkt.get_nombre()} → {asistente_mkt.get_resumen()}")
print("   TECNICO.get_resumen():")
print(f"     {tecnico_sis_1.get_nombre()} → {tecnico_sis_1.get_resumen()}")
print("   NOTA: El Técnico incluye los años de experiencia")
print()

# ───────────────────────────────────────────────────────────────
# 5. SETTERS: Métodos para MODIFICAR datos
# ───────────────────────────────────────────────────────────────
print("5. SETTERS (Modificación de datos)")
print(f"   Estado original de {asistente_pro.get_nombre()}: {asistente_pro.get_estado()}")
asistente_pro.set_estado("A")  # Cambiamos de "Despido" a "Activo"
print(f"   Estado modificado: {asistente_pro.get_estado()}")
print()

# ───────────────────────────────────────────────────────────────
# 6. RELACIÓN JEFE-SUBORDINADO (Referencias entre objetos)
# ───────────────────────────────────────────────────────────────
print("6. RELACIÓN JEFE-SUBORDINADO")
print(f"   {tecnico_sis_1.get_nombre()} reporta a:")
print(f"     → {tecnico_sis_1.get_jefe_inmediato()}")
print(f"   {tecnico_sis_1.get_jefe_inmediato()} reporta a:")
print(f"     → {jefe_sis.get_jefe_inmediato()}")
print(f"   {jefe_sis.get_jefe_inmediato()} reporta a:")
print(f"     → {gerente.get_jefe_inmediato()}")
print()

print("=" * 60)
print("FIN DEL SCRIPT EDUCATIVO")
print("=" * 60)
