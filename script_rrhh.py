# ================================================================
# SCRIPT RRHH - SISTEMA RRHH BUSINESS CORPORATION
# ================================================================

from models.trabajador import Trabajador
from services.reporte_service import generar_reporte_html, mostrar_resumen_lista


# ================================================================
# CREAR EMPLEADOS (10 en total)
# ================================================================

# Nivel 1: Gerente
gerente = Trabajador(
    nombre="Roberto Carlos",
    puesto="Gerente General",
    estado="A",
    jefe_inmediato=None
)

# Nivel 2: Jefes
jefe_mkt = Trabajador("Lucía Méndez", "Jefe de Marketing", "A", gerente)
jefe_sis = Trabajador("Alan Turing", "Jefe de Sistemas", "A", gerente)

# Nivel 3: Asistentes
asistente_mkt = Trabajador("Juan Pérez", "Asistente de Marketing", "A", jefe_mkt)
asistente_sis = Trabajador("Carlos Slim", "Asistente de Sistemas", "D", jefe_sis)
asistente_log = Trabajador("Marie Curie", "Asistente de Logística", "R", jefe_mkt)

# Nivel 4: Técnicos
tecnico_sis = Trabajador("Linus Torvalds", "Técnico de Sistemas", "A", jefe_sis)
tecnico_mkt = Trabajador("Tim Berners-Lee", "Técnico de Marketing", "A", jefe_mkt)
tecnico_log = Trabajador("Elon Musk", "Técnico de Logística", "TC", jefe_mkt)
tecnico_fin = Trabajador("Larry Page", "Técnico de Finanzas", "A", gerente)


# ================================================================
# ARRAY DE OBJETOS
# ================================================================

lista_empleados = [
    gerente,
    jefe_mkt,
    jefe_sis,
    asistente_mkt,
    asistente_sis,
    asistente_log,
    tecnico_sis,
    tecnico_mkt,
    tecnico_log,
    tecnico_fin
]


# ================================================================
# EJECUTAR
# ================================================================

print("=" * 50)
print("SISTEMA RRHH - BUSINESS CORPORATION")
print("=" * 50)
print()

mostrar_resumen_lista(lista_empleados)
print()

archivo = generar_reporte_html(lista_empleados)
print(f"OK - Reporte generado: {archivo}")
