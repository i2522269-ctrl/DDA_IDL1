# ================================================================
# SERVICIO DE REPORTE - GENERACIÓN DE ARCHIVO HTML CON COLORES
# ================================================================
#
# PROPÓSITO: Generar un archivo HTML con la lista de empleados
#
# COLORES POR ESTADO:
#   - A (Activo) → Verde (#4CAF50)
#   - TC (Término contrato) → Rojo (#f44336)
#   - D (Despido) → Negro (#333333)
#   - R (Renuncia) → Naranja (#FF9800)
#
# ================================================================


# ================================================================
# FUNCIÓN DE COLORES
# ================================================================

def get_colores_estado(estado):
    """
    Retorna los colores HTML según el estado del empleado.
    
    Args:
        estado (str): Código del estado (A, TC, D, R)
    
    Returns:
        tuple: (color_fondo, color_texto)
    
    Colores:
        - A  → Verde claro
        - TC → Rojo
        - D  → Negro
        - R  → Naranja
    """
    colores = {
        "A":  ("#4CAF50", "white"),   # Verde - Activo
        "TC": ("#f44336", "white"),   # Rojo - Término de contrato
        "D":  ("#333333", "white"),   # Negro - Despido
        "R":  ("#FF9800", "white")    # Naranja - Renuncia
    }
    return colores.get(estado, ("#999999", "white"))


# ================================================================
# FUNCIÓN PRINCIPAL
# ================================================================

def generar_reporte_html(lista_empleados, nombre_archivo="reporte_rrhh.html"):
    """
    Genera un archivo HTML con la tabla de empleados y colores por estado.
    
    Args:
        lista_empleados (list): Lista de objetos Trabajador
        nombre_archivo (str): Nombre del archivo HTML
    
    Returns:
        str: Nombre del archivo generado
    """
    
    # Abrir archivo en modo escritura
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        
        # ================================================================
        # ENCABEZADO HTML
        # ================================================================
        archivo.write("<!DOCTYPE html>\n")
        archivo.write("<html lang='es'>\n")
        archivo.write("<head>\n")
        archivo.write("    <meta charset='UTF-8'>\n")
        archivo.write("    <title>Reporte RRHH - Business Corporation</title>\n")
        
        # CSS con colores
        archivo.write("    <style>\n")
        archivo.write("        body { font-family: Arial, sans-serif; margin: 20px; }\n")
        archivo.write("        h1 { color: #333; }\n")
        archivo.write("        table { border-collapse: collapse; width: 100%; margin-top: 20px; }\n")
        archivo.write("        th, td { border: 1px solid #333; padding: 12px; text-align: left; }\n")
        archivo.write("        th { background-color: #2196F3; color: white; }\n")
        archivo.write("        tr:nth-child(even) { background-color: #f9f9f9; }\n")
        archivo.write("        tr:hover { background-color: #e3f2fd; }\n")
        archivo.write("        .estado { padding: 5px 10px; border-radius: 4px; text-align: center; font-weight: bold; }\n")
        archivo.write("        .badge { display: inline-block; padding: 5px 12px; border-radius: 12px; font-weight: bold; }\n")
        archivo.write("    </style>\n")
        archivo.write("</head>\n")
        archivo.write("<body>\n")
        
        # Título
        archivo.write("    <h1>Reporte de Recursos Humanos</h1>\n")
        archivo.write("    <h2>Business Corporation - Lista de Trabajadores</h2>\n")
        archivo.write(f"    <p>Total de empleados: {len(lista_empleados)}</p>\n")
        
        # ================================================================
        # TABLA HTML
        # ================================================================
        archivo.write("    <table>\n")
        
        # Cabecera
        archivo.write("        <tr>\n")
        archivo.write("            <th>Nombre Completo</th>\n")
        archivo.write("            <th>Puesto</th>\n")
        archivo.write("            <th>Jefe Inmediato</th>\n")
        archivo.write("            <th>Estado</th>\n")
        archivo.write("        </tr>\n")
        
        # Filas de empleados
        for emp in lista_empleados:
            # Obtener datos
            nombre = emp.get_nombre()
            puesto = emp.get_resumen()
            jefe = emp.get_jefe_inmediato()
            estado_texto = emp.get_estado()
            estado_codigo = emp.get_estado_codigo()
            
            # Obtener colores para el estado
            color_fondo, color_texto = get_colores_estado(estado_codigo)
            
            # Escribir fila
            archivo.write("        <tr>\n")
            archivo.write(f"            <td>{nombre}</td>\n")
            archivo.write(f"            <td><strong>{puesto}</strong></td>\n")
            archivo.write(f"            <td>{jefe}</td>\n")
            # Celda de estado CON COLOR
            archivo.write(f"            <td style='background-color: {color_fondo}; color: {color_texto}; text-align: center;'>\n")
            archivo.write(f"                <span class='badge'>{estado_texto}</span>\n")
            archivo.write("            </td>\n")
            archivo.write("        </tr>\n")
        
        # Cerrar tabla
        archivo.write("    </table>\n")
        archivo.write("</body>\n")
        archivo.write("</html>\n")
    
    return nombre_archivo


def mostrar_resumen_lista(lista_empleados):
    """
    Muestra un resumen de la lista en consola.
    """
    print("=" * 60)
    print("LISTA DE EMPLEADOS")
    print("=" * 60)
    
    for i, emp in enumerate(lista_empleados, 1):
        estado = emp.get_estado()
        # Usar texto en lugar de emojis para evitar problemas de codificación
        print(f"{i}. {emp.get_nombre()} | {emp.get_puesto()} | {estado}")
    
    print("=" * 60)
    print(f"Total: {len(lista_empleados)} empleados")
    print("=" * 60)
    
    return len(lista_empleados)
