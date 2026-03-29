# ================================================================
# APP STREAMLIT - SISTEMA RRHH BUSINESS CORPORATION
# ================================================================

import streamlit as st
import pandas as pd

from models.trabajador import Trabajador
from services.reporte_service import generar_reporte_html, get_colores_estado
from services.empleado_service import (
    crear_empleado,
    cargar_empleados,
    guardar_empleados
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
# JERARQUÍA DE PUESTOS (POO - Encapsulamiento de reglas de negocio)
# ================================================================

JERARQUIA = {
    "Gerente General": {"nivel": 1, "area": None, "jefes_validos": [None]},
    "Jefe de Marketing": {"nivel": 2, "area": "Marketing", "jefes_validos": ["Gerente General"]},
    "Jefe de Sistemas": {"nivel": 2, "area": "Sistemas", "jefes_validos": ["Gerente General"]},
    "Jefe de Finanzas": {"nivel": 2, "area": "Finanzas", "jefes_validos": ["Gerente General"]},
    "Jefe de Logística": {"nivel": 2, "area": "Logística", "jefes_validos": ["Gerente General"]},
    "Asistente de Marketing": {"nivel": 3, "area": "Marketing", "jefes_validos": ["Jefe de Marketing"]},
    "Asistente de Sistemas": {"nivel": 3, "area": "Sistemas", "jefes_validos": ["Jefe de Sistemas"]},
    "Asistente de Finanzas": {"nivel": 3, "area": "Finanzas", "jefes_validos": ["Jefe de Finanzas"]},
    "Asistente de Logística": {"nivel": 3, "area": "Logística", "jefes_validos": ["Jefe de Logística"]},
    "Técnico de Marketing": {"nivel": 3, "area": "Marketing", "jefes_validos": ["Jefe de Marketing"]},
    "Técnico de Sistemas": {"nivel": 3, "area": "Sistemas", "jefes_validos": ["Jefe de Sistemas"]},
    "Técnico de Finanzas": {"nivel": 3, "area": "Finanzas", "jefes_validos": ["Jefe de Finanzas"]},
    "Técnico de Logística": {"nivel": 3, "area": "Logística", "jefes_validos": ["Jefe de Logística"]},
}

TODOS_LOS_PUESTOS = list(JERARQUIA.keys())


def obtener_puestos_por_nivel(nivel):
    """Devuelve puestos filtrados por nivel de jerarquía."""
    return [p for p, info in JERARQUIA.items() if info["nivel"] == nivel]


def obtener_jefes_validos_para_puesto(puesto):
    """POO: Polimorfismo - según el puesto, retorna los tipos de jefe válidos."""
    if puesto not in JERARQUIA:
        return TODOS_LOS_PUESTOS
    return JERARQUIA[puesto]["jefes_validos"]


def obtener_puestos_validos_para_jefe(jefe_nombre, empleados):
    """
    POO: Polimorfismo - según el jefe seleccionado, retorna puestos válidos.
    Si jefe=None → solo Gerente General
    Si jefe es Gerente → Jefes de todas las áreas
    Si jefe es Jefe de X → Asistentes y Técnicos de X
    """
    puestos = []
    
    if jefe_nombre is None:
        puestos = ["Gerente General"]
    else:
        for emp in empleados:
            if emp.get_nombre() == jefe_nombre:
                puesto_jefe = emp.get_puesto()
                if puesto_jefe in JERARQUIA:
                    nivel_jefe = JERARQUIA[puesto_jefe]["nivel"]
                    if nivel_jefe == 1:
                        puestos = obtener_puestos_por_nivel(2)
                    elif nivel_jefe == 2:
                        area_jefe = JERARQUIA[puesto_jefe]["area"]
                        puestos = [p for p, info in JERARQUIA.items() 
                                   if info["nivel"] == 3 and info["area"] == area_jefe]
                break
    
    return puestos if puestos else TODOS_LOS_PUESTOS


def encontrar_jefe_por_puesto(puesto_buscado, empleados):
    """Encuentra un empleado con el puesto que sería jefe válido."""
    if puesto_buscado not in JERARQUIA:
        return None
    tipos_jefe = JERARQUIA[puesto_buscado]["jefes_validos"]
    for emp in empleados:
        if emp.get_puesto() in tipos_jefe:
            return emp.get_nombre()
    return None


# ================================================================
# FUNCIONES DE APOYO
# ================================================================

def convertir_a_dataframe(lista):
    """Convierte la lista a DataFrame."""
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
    
    # Tabla
    st.subheader("👥 Lista de Empleados")
    df = convertir_a_dataframe(st.session_state.empleados)
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
    
    st.info("💡 **Selección bidireccional:** Elige puesto o jefe y el otro se auto-completa según la jerarquía.")
    
    nombre = st.text_input("Nombre completo *", placeholder="Ej: Juan Pérez")
    
    col1, col2 = st.columns(2)
    
    with col1:
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
    
    with col2:
        modo_seleccion = st.radio(
            "Seleccionar por:",
            ["Puesto", "Jefe"],
            horizontal=True,
            help="Elige cómo quieres buscar: por puesto o por jefe directo"
        )
    
    st.markdown("---")
    
    if modo_seleccion == "Puesto":
        st.markdown("**Paso 1: Selecciona el puesto**")
        
        puesto_idx = 0
        if "puesto_idx" not in st.session_state:
            st.session_state.puesto_idx = 0
            st.session_state.jefe_idx = 0
        
        puesto = st.selectbox(
            "Puesto *",
            options=TODOS_LOS_PUESTOS,
            index=st.session_state.puesto_idx,
            key="puesto_key"
        )
        
        if puesto == "Gerente General":
            st.success("✓ Gerente General no necesita jefe")
            jefe_resultado = None
            puesto_confirmado = puesto
        else:
            st.markdown("**Paso 2: Selecciona el jefe directo**")
            
            puestos_validos_jefe = obtener_jefes_validos_para_puesto(puesto)
            empleados_filtrados = [
                e for e in st.session_state.empleados 
                if e.get_puesto() in puestos_validos_jefe
            ]
            
            opciones_jefe = ["-- Seleccionar --"] + [e.get_nombre() for e in empleados_filtrados]
            
            if st.session_state.jefe_idx >= len(opciones_jefe):
                st.session_state.jefe_idx = 0
            
            jefe_seleccionado = st.selectbox(
                "Jefe inmediato *",
                options=opciones_jefe,
                index=st.session_state.jefe_idx,
                key="jefe_key"
            )
            
            if jefe_seleccionado == "-- Seleccionar --":
                st.warning("⚠️ Selecciona un jefe válido para este puesto")
                jefe_resultado = None
                puesto_confirmado = None
            else:
                jefe_resultado = jefe_seleccionado
                puesto_confirmado = puesto
                st.success(f"✓ {puesto} bajo la supervisión de {jefe_resultado}")
    else:
        st.markdown("**Paso 1: Selecciona el jefe directo**")
        
        opciones_jefes = ["-- Seleccionar --"] + [e.get_nombre() for e in st.session_state.empleados]
        
        if "jefe_idx" not in st.session_state:
            st.session_state.jefe_idx = 0
            st.session_state.puesto_idx = 0
        
        jefe_seleccionado = st.selectbox(
            "Jefe inmediato *",
            options=opciones_jefes,
            index=st.session_state.jefe_idx,
            key="jefe_key"
        )
        
        if jefe_seleccionado == "-- Seleccionar --":
            st.warning("⚠️ Selecciona un jefe para ver los puestos disponibles")
            puesto_confirmado = None
            jefe_resultado = None
        else:
            st.markdown("**Paso 2: Selecciona el puesto**")
            
            puestos_validos = obtener_puestos_validos_para_jefe(jefe_seleccionado, st.session_state.empleados)
            
            if st.session_state.puesto_idx >= len(puestos_validos):
                st.session_state.puesto_idx = 0
            
            puesto = st.selectbox(
                "Puesto *",
                options=puestos_validos,
                index=st.session_state.puesto_idx,
                key="puesto_key"
            )
            
            puesto_confirmado = puesto
            jefe_resultado = jefe_seleccionado
            st.success(f"✓ {puesto} bajo la supervisión de {jefe_resultado}")
    
    st.markdown("---")
    
    col_btn1, col_btn2 = st.columns([1, 3])
    
    with col_btn1:
        registrar = st.button(
            "➕ Registrar",
            type="primary",
            use_container_width=True,
            disabled=(puesto_confirmado is None or not nombre.strip())
        )
    
    with col_btn2:
        if st.button("🔄 Limpiar", use_container_width=True):
            st.session_state.puesto_idx = 0
            st.session_state.jefe_idx = 0
            st.rerun()
    
    if registrar:
        errores = []
        
        if not nombre.strip():
            errores.append("El nombre es obligatorio")
        
        if puesto_confirmado is None:
            errores.append("Selecciona un puesto y jefe válidos")
        
        if errores:
            for error in errores:
                st.error(f"❌ {error}")
        else:
            jefe_obj = None
            if jefe_resultado:
                for emp in st.session_state.empleados:
                    if emp.get_nombre() == jefe_resultado:
                        jefe_obj = emp
                        break
            
            try:
                nuevo = crear_empleado(
                    nombre=nombre,
                    puesto=puesto_confirmado,
                    estado=estado,
                    jefe=jefe_obj
                )
                
                st.session_state.empleados.append(nuevo)
                guardar_empleados(st.session_state.empleados)
                
                st.session_state.puesto_idx = 0
                st.session_state.jefe_idx = 0
                
                st.success(f"✅ ¡{nombre} registrado como {puesto_confirmado}!")
                st.balloons()
                st.rerun()
                
            except ValueError as e:
                st.error(f"❌ {e}")


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
