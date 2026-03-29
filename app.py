# ================================================================
# APP STREAMLIT - SISTEMA RRHH BUSINESS CORPORATION
# ================================================================
#
# PROPÓSITO: Interfaz web interactiva para el sistema de RRHH
#
# FUNCIONALIDADES:
#   - Ver lista de empleados en una tabla
#   - Crear nuevos empleados (con persistencia en JSON)
#   - Generar reporte HTML
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
from services.reporte_service import generar_reporte_html
from services.empleado_service import (
    crear_empleado,
    cargar_empleados,
    guardar_empleados
)


# ================================================================
# CONFIGURACIÓN DE LA PÁGINA
# ================================================================
st.set_page_config(
    page_title="Sistema RRHH",
    page_icon="🏢",
    layout="wide"
)


# ================================================================
# INICIALIZACIÓN DEL ESTADO DE SESIÓN
# ================================================================
# session_state mantiene los datos mientras la app está abierta
# Si es la primera vez, carga los empleados desde JSON

if "empleados" not in st.session_state:
    st.session_state.empleados = cargar_empleados()


# ================================================================
# FUNCIONES DE APOYO
# ================================================================

def convertir_a_dataframe(lista_empleados):
    """
    Convierte la lista de empleados a un DataFrame de Pandas.
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


def recargar_y_guardar():
    """
    Recarga la lista de empleados y guarda en JSON.
    Se llama después de crear/eliminar un empleado.
    """
    # Guardar en JSON
    guardar_empleados(st.session_state.empleados)
    # Recargar desde JSON para asegurar consistencia
    st.session_state.empleados = cargar_empleados()


# ================================================================
# ENCABEZADO PRINCIPAL
# ================================================================
st.title("🏢 Sistema de Recursos Humanos")
st.markdown("**Business Corporation**")
st.markdown("---")


# ================================================================
# PESTAÑAS DE NAVEGACIÓN
# ================================================================
tab1, tab2, tab3 = st.tabs([
    "📊 Dashboard",
    "🆕 Registrar Empleado",
    "📄 Reporte HTML"
])


# ================================================================
# TAB 1: DASHBOARD (Estadísticas y Lista)
# ================================================================
with tab1:
    st.subheader("📊 Estadísticas de la Empresa")
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Empleados", len(st.session_state.empleados))
    
    with col2:
        activos = sum(1 for e in st.session_state.empleados if e.get_estado() == "Activo")
        st.metric("Activos", activos)
    
    with col3:
        tecnicos = sum(1 for e in st.session_state.empleados if isinstance(e, Tecnico))
        st.metric("Personal Técnico", tecnicos)
    
    with col4:
        inactivos = len(st.session_state.empleados) - activos
        st.metric("Inactivos", inactivos)
    
    st.markdown("---")
    
    # Tabla de empleados
    st.subheader("👥 Lista de Empleados")
    df = convertir_a_dataframe(st.session_state.empleados)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


# ================================================================
# TAB 2: REGISTRAR NUEVO EMPLEADO
# ================================================================
with tab2:
    st.subheader("🆕 Registrar Nuevo Empleado")
    
    with st.form("form_empleado", clear_on_submit=True):
        # ───────────────────────────────────────────────────────
        # TIPO DE EMPLEADO
        # ───────────────────────────────────────────────────────
        col1, col2 = st.columns(2)
        
        with col1:
            tipo = st.radio(
                "Tipo de empleado:",
                options=["Trabajador", "Tecnico"],
                horizontal=True,
                help="Trabajador: Asistente o similar. Técnico: Con años de experiencia."
            )
        
        # ───────────────────────────────────────────────────────
        # DATOS BÁSICOS
        # ───────────────────────────────────────────────────────
        with col2:
            estado = st.selectbox(
                "Estado laboral:",
                options=["A", "TC", "D", "R"],
                format_func=lambda x: {
                    "A": "Activo",
                    "TC": "Término de contrato",
                    "D": "Despido",
                    "R": "Renuncia"
                }[x],
                help="A=Activo, TC=Contrato terminado, D=Despedido, R=Renunció"
            )
        
        # ───────────────────────────────────────────────────────
        # CAMPOS DEL FORMULARIO
        # ───────────────────────────────────────────────────────
        nombre = st.text_input(
            "Nombre completo *",
            placeholder="Ej: Juan Pérez"
        )
        
        puesto = st.text_input(
            "Puesto *",
            placeholder="Ej: Asistente de Marketing"
        )
        
        # Selector de jefe
        opciones_jefe = ["Sin jefe (Gerente)"] + [e.get_nombre() for e in st.session_state.empleados]
        jefe_seleccionado = st.selectbox(
            "Jefe inmediato:",
            options=opciones_jefe,
            help="Selecciona el jefe directo del nuevo empleado"
        )
        
        # Años de experiencia (solo para Técnicos)
        anios_experiencia = None
        if tipo == "Tecnico":
            anios_experiencia = st.number_input(
                "Años de experiencia *",
                min_value=0,
                max_value=50,
                value=0,
                step=1,
                help="Cantidad de años de experiencia como técnico"
            )
        
        # ───────────────────────────────────────────────────────
        # BOTÓN DE ENVÍO
        # ───────────────────────────────────────────────────────
        st.markdown("---")
        submitted = st.form_submit_button(
            "➕ Registrar Empleado",
            type="primary",
            use_container_width=True
        )
        
        # ───────────────────────────────────────────────────────
        # PROCESAR EL FORMULARIO
        # ───────────────────────────────────────────────────────
        if submitted:
            # Validaciones
            errores = []
            
            if not nombre.strip():
                errores.append("El nombre es obligatorio")
            
            if not puesto.strip():
                errores.append("El puesto es obligatorio")
            
            if tipo == "Tecnico" and (anios_experiencia is None or anios_experiencia < 0):
                errores.append("Los años de experiencia son obligatorios para técnicos")
            
            # Mostrar errores o procesar
            if errores:
                for error in errores:
                    st.error(f"❌ {error}")
            else:
                # Buscar el objeto del jefe
                jefe_obj = None
                if jefe_seleccionado != "Sin jefe (Gerente)":
                    for emp in st.session_state.empleados:
                        if emp.get_nombre() == jefe_seleccionado:
                            jefe_obj = emp
                            break
                
                try:
                    # Crear el empleado
                    nuevo_empleado = crear_empleado(
                        nombre=nombre,
                        puesto=puesto,
                        estado=estado,
                        tipo=tipo,
                        jefe=jefe_obj,
                        anios_experiencia=anios_experiencia
                    )
                    
                    # Agregar al array
                    st.session_state.empleados.append(nuevo_empleado)
                    
                    # Guardar en JSON (persistencia)
                    guardar_empleados(st.session_state.empleados)
                    
                    st.success(f"✅ ¡Empleado '{nombre}' registrado exitosamente!")
                    st.balloons()
                    
                except ValueError as e:
                    st.error(f"❌ Error: {e}")
    
    # ───────────────────────────────────────────────────────
    # INFORMACIÓN ADICIONAL
    # ───────────────────────────────────────────────────────
    with st.expander("ℹ️ Información sobre los campos"):
        st.markdown("""
        **Campos obligatorios (*):**
        - **Nombre completo**: Nombre del nuevo empleado
        - **Puesto**: Cargo que tendrá en la empresa
        - **Años de experiencia**: Solo para técnicos (obligatorio)
        
        **Estados laborales:**
        - **A (Activo)**: Trabajando actualmente
        - **TC (Término de contrato)**: Contrato finalizado
        - **D (Despido)**: Despedido por la empresa
        - **R (Renuncia)**: Renunció voluntariamente
        """)


# ================================================================
# TAB 3: REPORTE HTML
# ================================================================
with tab3:
    st.subheader("📄 Generar Reporte HTML")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.info("""
        **¿Qué hace este reporte?**
        
        Genera un archivo HTML con una tabla que muestra todos los empleados
        registrados en el sistema, incluyendo:
        
        - Nombre completo
        - Resumen del puesto (años de experiencia para técnicos)
        - Jefe inmediato
        - Estado laboral
        """)
    
    with col2:
        st.metric("Empleados en el sistema", len(st.session_state.empleados))
    
    st.markdown("---")
    
    # Botón para generar
    if st.button("🔵 Generar Reporte HTML", type="primary", use_container_width=True):
        with st.spinner("Generando reporte..."):
            # Generar el HTML
            archivo = generar_reporte_html(st.session_state.empleados)
        
        st.success(f"✅ ¡Reporte generado exitosamente!")
        st.markdown(f"**📁 Archivo:** `{archivo}`")
        st.markdown("**💡 Abre el archivo en tu navegador para ver la tabla HTML.**")
        
        # Mostrar preview
        with st.expander("👁️ Previsualizar contenido del reporte"):
            df_preview = convertir_a_dataframe(st.session_state.empleados)
            st.dataframe(df_preview, hide_index=True)


# ================================================================
# FOOTER
# ================================================================
st.markdown("---")
st.caption("Sistema RRHH - Business Corporation | Desarrollado con Python + Streamlit")
