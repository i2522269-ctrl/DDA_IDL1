# ================================================================
# APP STREAMLIT - SISTEMA RRHH BUSINESS CORPORATION
# ================================================================
#
# FUNCIONALIDADES:
#   - Ver lista de empleados en tabla
#   - Registrar nuevos empleados (con puestos predefinidos)
#   - Generar reporte HTML con colores por estado
#
# COLORES POR ESTADO:
#   🟢 Activo        → Verde (#4CAF50)
#   🔴 Término contrato → Rojo (#f44336)
#   ⚫ Despido       → Negro (#333333)
#   🟠 Renuncia      → Naranja (#FF9800)
#
# ================================================================


# ================================================================
# IMPORTACIONES
# ================================================================
import streamlit as st
import pandas as pd

from models.trabajador import Trabajador
from services.reporte_service import generar_reporte_html, get_colores_estado
from services.empleado_service import (
    crear_empleado,
    cargar_empleados,
    guardar_empleados,
    PUESTOS_DISPONIBLES
)


# ================================================================
# CONFIGURACIÓN
# ================================================================
st.set_page_config(
    page_title="Sistema RRHH",
    page_icon="🏢",
    layout="wide"
)


# ================================================================
# ESTADO DE SESIÓN
# ================================================================
if "empleados" not in st.session_state:
    st.session_state.empleados = cargar_empleados()


# ================================================================
# FUNCIONES DE APOYO
# ================================================================

def convertir_a_dataframe(lista):
    """Convierte la lista a DataFrame con colores."""
    datos = []
    for emp in lista:
        estado_codigo = emp.get_estado_codigo()
        color_fondo, _ = get_colores_estado(estado_codigo)
        
        datos.append({
            "Nombre": emp.get_nombre(),
            "Puesto": emp.get_puesto(),
            "Jefe Inmediato": emp.get_jefe_inmediato(),
            "Estado": emp.get_estado(),
            "_color": color_fondo
        })
    return pd.DataFrame(datos)


def recargar_datos():
    """Recarga los datos desde JSON."""
    guardar_empleados(st.session_state.empleados)
    st.session_state.empleados = cargar_empleados()


# ================================================================
# ENCABEZADO
# ================================================================
st.title("🏢 Sistema de Recursos Humanos")
st.markdown("**Business Corporation**")
st.markdown("---")


# ================================================================
# PESTAÑAS
# ================================================================
tab1, tab2, tab3 = st.tabs([
    "📊 Dashboard",
    "🆕 Registrar",
    "📄 Reporte"
])


# ================================================================
# TAB 1: DASHBOARD
# ================================================================
with tab1:
    st.subheader("📊 Estadísticas")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total", len(st.session_state.empleados))
    
    with col2:
        activos = sum(1 for e in st.session_state.empleados if e.get_estado_codigo() == "A")
        st.metric("🟢 Activos", activos)
    
    with col3:
        tc = sum(1 for e in st.session_state.empleados if e.get_estado_codigo() == "TC")
        st.metric("🔴 TC", tc)
    
    with col4:
        otros = sum(1 for e in st.session_state.empleados if e.get_estado_codigo() in ["D", "R"])
        st.metric("⚫ D + 🟠 R", otros)
    
    st.markdown("---")
    
    # Tabla con colores
    st.subheader("👥 Lista de Empleados")
    
    df = convertir_a_dataframe(st.session_state.empleados)
    
    # Mostrar tabla con estilo
    st.dataframe(
        df[["Nombre", "Puesto", "Jefe Inmediato", "Estado"]],
        use_container_width=True,
        hide_index=True
    )


# ================================================================
# TAB 2: REGISTRAR EMPLEADO
# ================================================================
with tab2:
    st.subheader("🆕 Registrar Nuevo Empleado")
    
    with st.form("form_empleado", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            # Selector de puesto (dropdown)
            puesto_opciones = list(PUESTOS_DISPONIBLES.keys())
            puesto = st.selectbox(
                "Puesto *",
                options=puesto_opciones,
                format_func=lambda x: f"{x} - {PUESTOS_DISPONIBLES[x]}"
            )
        
        with col2:
            # Selector de estado con colores
            estado = st.selectbox(
                "Estado *",
                options=["A", "TC", "D", "R"],
                format_func=lambda x: {
                    "A": "🟢 Activo",
                    "TC": "🔴 Término de contrato",
                    "D": "⚫ Despido",
                    "R": "🟠 Renuncia"
                }[x]
            )
        
        nombre = st.text_input("Nombre completo *", placeholder="Ej: Juan Pérez")
        
        # Selector de jefe
        opciones_jefe = ["Sin jefe (Gerente)"] + [e.get_nombre() for e in st.session_state.empleados]
        jefe_seleccionado = st.selectbox("Jefe inmediato", opciones_jefe)
        
        st.markdown("---")
        
        submitted = st.form_submit_button(
            "➕ Registrar",
            type="primary",
            use_container_width=True
        )
        
        if submitted:
            errores = []
            
            if not nombre.strip():
                errores.append("El nombre es obligatorio")
            
            if errores:
                for error in errores:
                    st.error(f"❌ {error}")
            else:
                # Buscar jefe
                jefe_obj = None
                if jefe_seleccionado != "Sin jefe (Gerente)":
                    for emp in st.session_state.empleados:
                        if emp.get_nombre() == jefe_seleccionado:
                            jefe_obj = emp
                            break
                
                try:
                    nuevo = crear_empleado(
                        nombre=nombre,
                        puesto=puesto,
                        estado=estado,
                        jefe=jefe_obj
                    )
                    
                    st.session_state.empleados.append(nuevo)
                    guardar_empleados(st.session_state.empleados)
                    
                    st.success(f"✅ ¡{nombre} registrado!")
                    st.balloons()
                    
                except ValueError as e:
                    st.error(f"❌ {e}")
    
    # Info de puestos
    with st.expander("ℹ️ Lista de puestos"):
        for codigo, nombre_completo in PUESTOS_DISPONIBLES.items():
            st.write(f"**{codigo}** → {nombre_completo}")


# ================================================================
# TAB 3: REPORTE HTML
# ================================================================
with tab3:
    st.subheader("📄 Generar Reporte HTML")
    
    # Leyenda de colores
    st.markdown("""
    **Leyenda de colores por estado:**
    - 🟢 **Activo** → Verde
    - 🔴 **Término de contrato** → Rojo
    - ⚫ **Despido** → Negro
    - 🟠 **Renuncia** → Naranja
    """)
    
    st.markdown("---")
    
    if st.button("🔵 Generar Reporte", type="primary", use_container_width=True):
        with st.spinner("Generando..."):
            archivo = generar_reporte_html(st.session_state.empleados)
        
        st.success(f"✅ Reporte generado: `{archivo}`")
        st.info("💡 Abre el archivo en tu navegador")
        
        # Preview
        with st.expander("👁️ Previsualizar"):
            df_preview = convertir_a_dataframe(st.session_state.empleados)
            st.dataframe(df_preview[["Nombre", "Puesto", "Jefe Inmediato", "Estado"]], hide_index=True)


# ================================================================
# FOOTER
# ================================================================
st.markdown("---")
st.caption("Sistema RRHH - Business Corporation | Python + Streamlit")
