# ================================================================
# APP STREAMLIT - SISTEMA RRHH BUSINESS CORPORATION
# ================================================================
#
# PROPÓSITO: Interfaz web interactiva para el sistema de RRHH
#
# FUNCIONALIDADES:
#   - Ver lista de empleados en una tabla
#   - Generar reporte HTML con un botón
#   - Estadísticas de la empresa
#
# PARA EJECUTAR:
#   streamlit run app.py
#
# ================================================================


# ================================================================
# IMPORTACIONES
# ================================================================
import streamlit as st
import pandas as pd

from models.trabajador import Trabajador
from models.tecnico import Tecnico
from services.reporte_service import generar_reporte_html, mostrar_resumen_lista


# ================================================================
# CONFIGURACIÓN DE LA PÁGINA
# ================================================================
st.set_page_config(
    page_title="Sistema RRHH",
    page_icon="🏢",
    layout="wide"
)


# ================================================================
# FUNCIÓN PARA CREAR EMPLEADOS (CÓDIGO REUTILIZABLE)
# ================================================================
@st.cache_data
def crear_lista_empleados():
    """
    Crea la lista de empleados de la empresa.
    Usa @st.cache_data para evitar recrear los objetos en cada刷新.
    
    Returns:
        list: Lista de objetos empleado
    """
    
    # ───────────────────────────────────────────────────────────
    # GERENTE GENERAL
    # ───────────────────────────────────────────────────────────
    gerente = Trabajador(
        nombre="Roberto Carlos",
        puesto="Gerente General",
        estado="A",
        jefe_inmediato=None
    )
    
    # ───────────────────────────────────────────────────────────
    # JEFES DE ÁREA (5)
    # ───────────────────────────────────────────────────────────
    jefe_mkt = Trabajador("Lucía Méndez", "Jefe de Marketing", "A", gerente)
    jefe_sis = Trabajador("Alan Turing", "Jefe de Sistemas", "A", gerente)
    jefe_pro = Trabajador("Henry Ford", "Jefe de Producción", "A", gerente)
    jefe_log = Trabajador("Jeff Bezos", "Jefe de Logística", "TC", gerente)
    jefe_fin = Trabajador("Warren Buffett", "Jefe de Finanzas", "R", gerente)
    
    # ───────────────────────────────────────────────────────────
    # ASISTENTES (5)
    # ───────────────────────────────────────────────────────────
    asistente_mkt = Trabajador("Juan Pérez", "Asistente de Marketing", "A", jefe_mkt)
    asistente_sis = Trabajador("Ada Lovelace", "Asistente de Sistemas", "A", jefe_sis)
    asistente_pro = Trabajador("Carlos Slim", "Asistente de Producción", "D", jefe_pro)
    asistente_log = Trabajador("Marie Curie", "Asistente de Logística", "A", jefe_log)
    asistente_fin = Trabajador("Nikola Tesla", "Asistente de Finanzas", "A", jefe_fin)
    
    # ───────────────────────────────────────────────────────────
    # TÉCNICOS (15)
    # ───────────────────────────────────────────────────────────
    # Marketing
    tecnico_mkt_1 = Tecnico("Elon Musk", "Técnico de Marketing", "A", jefe_mkt, 5)
    tecnico_mkt_2 = Tecnico("Grace Hopper", "Técnico de Marketing", "A", jefe_mkt, 9)
    tecnico_mkt_3 = Tecnico("Margaret Hamilton", "Técnico de Marketing", "A", jefe_mkt, 11)
    
    # Sistemas
    tecnico_sis_1 = Tecnico("Linus Torvalds", "Técnico de Sistemas", "A", jefe_sis, 10)
    tecnico_sis_2 = Tecnico("Steve Wozniak", "Técnico de Sistemas", "A", jefe_sis, 15)
    tecnico_sis_3 = Tecnico("Bill Gates", "Técnico de Sistemas", "TC", jefe_sis, 8)
    
    # Producción
    tecnico_pro_1 = Tecnico("Tim Berners-Lee", "Técnico de Producción", "A", jefe_pro, 12)
    tecnico_pro_2 = Tecnico("Vint Cerf", "Técnico de Producción", "A", jefe_pro, 7)
    tecnico_pro_3 = Tecnico("Ken Thompson", "Técnico de Producción", "A", jefe_pro, 14)
    
    # Logística
    tecnico_log_1 = Tecnico("Alan Kay", "Técnico de Logística", "A", jefe_log, 6)
    tecnico_log_2 = Tecnico("Dennis Ritchie", "Técnico de Logística", "A", jefe_log, 9)
    tecnico_log_3 = Tecnico("Bjarne Stroustrup", "Técnico de Logística", "R", jefe_log, 4)
    
    # Finanzas
    tecnico_fin_1 = Tecnico("Larry Page", "Técnico de Finanzas", "A", jefe_fin, 8)
    tecnico_fin_2 = Tecnico("Sergey Brin", "Técnico de Finanzas", "A", jefe_fin, 6)
    tecnico_fin_3 = Tecnico("Larry Ellison", "Técnico de Finanzas", "A", jefe_fin, 10)
    
    # ───────────────────────────────────────────────────────────
    # ARRAY DE OBJETOS (LISTA)
    # ───────────────────────────────────────────────────────────
    lista_empleados = [
        gerente,
        jefe_mkt, jefe_sis, jefe_pro, jefe_log, jefe_fin,
        asistente_mkt, asistente_sis, asistente_pro, asistente_log, asistente_fin,
        tecnico_mkt_1, tecnico_mkt_2, tecnico_mkt_3,
        tecnico_sis_1, tecnico_sis_2, tecnico_sis_3,
        tecnico_pro_1, tecnico_pro_2, tecnico_pro_3,
        tecnico_log_1, tecnico_log_2, tecnico_log_3,
        tecnico_fin_1, tecnico_fin_2, tecnico_fin_3
    ]
    
    return lista_empleados


def convertir_a_dataframe(lista_empleados):
    """
    Convierte la lista de empleados a un DataFrame de Pandas.
    Útil para mostrar en st.dataframe().
    
    Args:
        lista_empleados (list): Lista de objetos empleado
    
    Returns:
        pd.DataFrame: DataFrame con los datos
    """
    datos = []
    for emp in lista_empleados:
        datos.append({
            "Nombre": emp.get_nombre(),
            "Puesto": emp.get_puesto(),
            "Resumen": emp.get_resumen(),
            "Jefe Inmediato": emp.get_jefe_inmediato(),
            "Estado": emp.get_estado()
        })
    
    return pd.DataFrame(datos)


# ================================================================
# INTERFAZ STREAMLIT
# ================================================================

# ───────────────────────────────────────────────────────────────
# ENCABEZADO
# ───────────────────────────────────────────────────────────────
st.title("🏢 Sistema de Recursos Humanos")
st.markdown("**Business Corporation**")
st.markdown("---")


# ───────────────────────────────────────────────────────────────
# CARGAR DATOS
# ───────────────────────────────────────────────────────────────
empleados = crear_lista_empleados()


# ───────────────────────────────────────────────────────────────
# ESTADÍSTICAS
# ───────────────────────────────────────────────────────────────
st.subheader("📊 Estadísticas de la Empresa")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Empleados", len(empleados))

with col2:
    activos = sum(1 for e in empleados if e.get_estado() == "Activo")
    st.metric("Activos", activos)

with col3:
    tecnicos = sum(1 for e in empleados if isinstance(e, Tecnico))
    st.metric("Personal Técnico", tecnicos)

with col4:
    inactivos = len(empleados) - activos
    st.metric("Inactivos", inactivos)

st.markdown("---")


# ───────────────────────────────────────────────────────────────
# BOTÓN PARA GENERAR REPORTE HTML
# ───────────────────────────────────────────────────────────────
st.subheader("📄 Generar Reporte HTML")

if st.button("🔵 Generar Reporte de Empleados", type="primary"):
    with st.spinner("Generando reporte..."):
        archivo = generar_reporte_html(empleados)
    
    st.success(f"✅ ¡Reporte generado exitosamente!")
    st.info(f"📁 Archivo: `{archivo}`")
    st.info("💡 Abre el archivo en tu navegador para ver la tabla HTML.")
    
    # Mostrar en consola también
    mostrar_resumen_lista(empleados)

st.markdown("---")


# ───────────────────────────────────────────────────────────────
# TABLA DE EMPLEADOS
# ───────────────────────────────────────────────────────────────
st.subheader("👥 Lista de Empleados")

df = convertir_a_dataframe(empleados)
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)


# ───────────────────────────────────────────────────────────────
# DETALLES POR EMPLEADO
# ───────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("🔍 Detalle por Empleado")

# Selector de empleado
nombres = [emp.get_nombre() for emp in empleados]
empleado_seleccionado = st.selectbox("Selecciona un empleado:", nombres)

# Mostrar detalles del seleccionado
for emp in empleados:
    if emp.get_nombre() == empleado_seleccionado:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Nombre:** {emp.get_nombre()}")
            st.write(f"**Puesto:** {emp.get_puesto()}")
            st.write(f"**Resumen:** {emp.get_resumen()}")
        
        with col2:
            st.write(f"**Jefe Inmediato:** {emp.get_jefe_inmediato()}")
            st.write(f"**Estado:** {emp.get_estado()}")
            
            # Si es técnico, mostrar años de experiencia
            if isinstance(emp, Tecnico):
                st.write(f"**Años de Experiencia:** {emp.get_anios_experiencia()}")
                st.write(f"**Nivel:** {emp.get_nivel_experiencia()}")
        
        break


# ───────────────────────────────────────────────────────────────
# FOOTER
# ───────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("Sistema RRHH - Business Corporation | Desarrollado con Python + Streamlit")
