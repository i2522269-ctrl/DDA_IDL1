# ================================================================
# SERVICIO DE REPORTE - GENERACIÓN DE ARCHIVO HTML
# ================================================================
# 
# PROPÓSITO: Generar un archivo HTML con la lista de empleados
#            usando comandos nativos de Python (open, write).
# 
# FUNCIONALIDAD:
#   1. Abre/crea un archivo HTML en modo escritura
#   2. Escribe la estructura HTML (head, body, table)
#   3. Recorre el Array de objetos con un FOR
#   4. Por cada objeto, extrae datos con Getters
#   5. Escribe una fila en la tabla HTML
#   6. Cierra el archivo automáticamente (con "with")
#
# CONCEPTOS APLICADOS:
#   - MANEJO DE ARCHIVOS: open(), write(), with
#   - ESTRUCTURA REPETITIVA: for...in
#   - POO: Llamada a métodos de objetos (emp.get_nombre())
#
# ================================================================


def generar_reporte_html(lista_empleados, nombre_archivo="reporte_rrhh.html"):
    """
    Genera un archivo HTML con la tabla de empleados.
    
    Esta función:
        1. Crea un archivo HTML nuevo (sobrescribe si existe)
        2. Escribe la estructura HTML con estilos CSS básicos
        3. Genera una tabla con los datos de todos los empleados
    
    Args:
        lista_empleados (list): Array (lista) de objetos Trabajador/Tecnico
        nombre_archivo (str): Nombre del archivo HTML a generar
    
    Returns:
        str: Ruta completa del archivo generado
    
    Flujograma:
        INICIO
          ↓
        open("archivo.html", "w") → Abre/Crea archivo
          ↓
        write(estructura HTML) → Escribe head, styles, table header
          ↓
        for emp in lista: → Itera sobre cada empleado
          ↓
        emp.get_nombre() → Extrae datos con getters
          ↓
        write(f"<tr>...</tr>") → Escribe fila
          ↓
        write(cierre HTML) → Finaliza documento
          ↓
        with cierra automático → Cierra archivo
          ↓
        FIN → archivo.html listo
    
    Ejemplo:
        lista = [gerente, jefe_mkt, tecnico1]
        generar_reporte_html(lista)
        # Genera: reporte_rrhh.html
    """
    
    # ================================================================
    # PASO 1: ABRIR ARCHIVO EN MODO ESCRITURA
    # ================================================================
    # 
    # open() es una función nativa de Python para manejar archivos.
    # 
    # Parámetros:
    #   - nombre_archivo: Nombre del archivo a crear/sobrescribir
    #   - "w": Modo escritura (write). Si existe, lo sobrescribe.
    #   - encoding="utf-8": Permite caracteres especiales (ñ, acentos, etc.)
    # 
    # El bloque "with" garantiza que el archivo se cierre automáticamente
    # al terminar el bloque, aunque ocurran errores.
    #
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        
        # ================================================================
        # PASO 2: ESCRIBIR ENCABEZADO HTML
        # ================================================================
        #
        # Escribimos la estructura básica de una página HTML:
        #   - <html>...<head>...<body>: Estructura estándar
        #   - <title>: Título en la pestaña del navegador
        #   - <style>: CSS inline para dar formato a la tabla
        #
        
        # Inicio del documento HTML
        archivo.write("<!DOCTYPE html>\n")
        archivo.write("<html lang='es'>\n")
        archivo.write("<head>\n")
        archivo.write("    <meta charset='UTF-8'>\n")
        archivo.write("    <title>Reporte RRHH - Business Corporation</title>\n")
        
        # CSS Embebido: Estilos para la tabla
        # border-collapse: collapse → Elimina espacios entre celdas
        # padding: 8px → Espacio interno de las celdas
        # text-align: left → Alineación del texto
        archivo.write("    <style>\n")
        archivo.write("        body { font-family: Arial, sans-serif; margin: 20px; }\n")
        archivo.write("        h1 { color: #333; }\n")
        archivo.write("        table { border-collapse: collapse; width: 100%; margin-top: 20px; }\n")
        archivo.write("        th, td { border: 1px solid #333; padding: 10px; text-align: left; }\n")
        archivo.write("        th { background-color: #4CAF50; color: white; }\n")
        archivo.write("        tr:nth-child(even) { background-color: #f2f2f2; }\n")
        archivo.write("        tr:hover { background-color: #ddd; }\n")
        archivo.write("        .estado-activo { color: green; font-weight: bold; }\n")
        archivo.write("        .estado-inactivo { color: red; font-weight: bold; }\n")
        archivo.write("    </style>\n")
        archivo.write("</head>\n")
        archivo.write("<body>\n")
        
        # Título de la página
        archivo.write("    <h1>Reporte de Recursos Humanos</h1>\n")
        archivo.write("    <h2>Business Corporation - Lista de Trabajadores</h2>\n")
        archivo.write(f"    <p>Total de empleados: {len(lista_empleados)}</p>\n")
        
        # ================================================================
        # PASO 3: CREAR TABLA HTML
        # ================================================================
        #
        # Estructura de una tabla HTML:
        #   <table>          → Contenedor de la tabla
        #     <tr>           → Fila (table row)
        #       <th>         → Celda de encabezado (table header)
        #       </th>
        #     </tr>
        #     <tr>           → Fila de datos
        #       <td>          → Celda de datos (table data)
        #       </td>
        #     </tr>
        #   </table>
        #
        archivo.write("    <table>\n")
        
        # Cabecera de la tabla (encabezados de columna)
        archivo.write("        <tr>\n")
        archivo.write("            <th>Nombre Completo</th>\n")
        archivo.write("            <th>Resumen del Puesto</th>\n")
        archivo.write("            <th>Jefe Inmediato</th>\n")
        archivo.write("            <th>Estado</th>\n")
        archivo.write("        </tr>\n")
        
        # ================================================================
        # PASO 4: RECORRER ARRAY CON FOR (ESTRUCTURA REPETITIVA)
        # ================================================================
        #
        # BUCLE FOR: Itera sobre cada objeto en la lista de empleados.
        # 
        # Por cada empleado:
        #   1. Llama a los métodos get_XXX() para obtener los datos
        #   2. Concatena los datos en una fila HTML
        #   3. Escribe la fila en el archivo
        #
        # Sintaxis:
        #   for variable in lista:
        #       # código que se repite
        #
        # Ejemplo:
        #   for emp in lista_empleados:
        #       print(emp.get_nombre())
        #
        for emp in lista_empleados:
            
            # ============================================================
            # PASO 5: EXTRAER DATOS CON GETTERS (POO)
            # ============================================================
            #
            # Por cada empleado, llamamos a sus métodos getter para
            # obtener los datos que queremos mostrar en la tabla.
            #
            # Estos métodos fueron definidos en las clases:
            #   - get_nombre(): Retorna el nombre completo
            #   - get_resumen(): Retorna puesto (+ experiencia si es Técnico)
            #   - get_jefe_inmediato(): Retorna nombre del jefe
            #   - get_estado(): Retorna texto del estado laboral
            #
            
            # Obtenemos el nombre del empleado
            nombre = emp.get_nombre()
            
            # Obtenemos el resumen (puesto + experiencia si es técnico)
            # NOTA: Si es un Técnico, get_resumen() retorna "Puesto: X | Experiencia: N años"
            #       Si es un Trabajador normal, retorna "Puesto: X"
            resumen = emp.get_resumen()
            
            # Obtenemos el nombre del jefe inmediato
            # NOTA: Si es None (Gerente), retorna "Sin jefe (Alta Dirección)"
            jefe = emp.get_jefe_inmediato()
            
            # Obtenemos el estado laboral
            # NOTA: Traduce el código a texto (A → "Activo", TC → "Término de contrato", etc.)
            estado = emp.get_estado()
            
            # ============================================================
            # PASO 6: ESCRIBIR FILA HTML
            # ============================================================
            #
            # Escribimos una fila <tr> con 4 celdas <td>, una por columna.
            #
            # Usamos f-strings (f"...") para insertar variables en el texto:
            #   f"<td>{variable}</td>" → Reemplaza {variable} por su valor
            #
            # Ejemplo:
            #   nombre = "Juan Pérez"
            #   f"<td>{nombre}</td>" → "<td>Juan Pérez</td>"
            #
            
            # Abrimos la fila
            archivo.write("        <tr>\n")
            
            # Celda 1: Nombre completo
            archivo.write(f"            <td>{nombre}</td>\n")
            
            # Celda 2: Resumen del puesto
            archivo.write(f"            <td>{resumen}</td>\n")
            
            # Celda 3: Jefe inmediato
            archivo.write(f"            <td>{jefe}</td>\n")
            
            # Celda 4: Estado
            archivo.write(f"            <td>{estado}</td>\n")
            
            # Cerramos la fila
            archivo.write("        </tr>\n")
        
        # ================================================================
        # PASO 7: CERRAR TABLA Y DOCUMENTO HTML
        # ================================================================
        archivo.write("    </table>\n")
        archivo.write("</body>\n")
        archivo.write("</html>\n")
    
    # ================================================================
    # FIN DE LA FUNCIÓN
    # ================================================================
    # El archivo se cierra automáticamente al salir del bloque "with"
    # No necesitamos llamar a archivo.close() manualmente
    
    # Retornamos el nombre del archivo generado
    return nombre_archivo


def mostrar_resumen_lista(lista_empleados):
    """
    Muestra un resumen de la lista de empleados en consola.
    Función de apoyo para debugging y verificación.
    
    Args:
        lista_empleados (list): Lista de objetos empleado
    
    Returns:
        int: Cantidad total de empleados
    """
    print("=" * 60)
    print("LISTA DE EMPLEADOS - RESUMEN")
    print("=" * 60)
    
    for i, emp in enumerate(lista_empleados, 1):
        print(f"{i}. {emp.get_nombre()}")
        print(f"   Puesto: {emp.get_puesto()}")
        print(f"   Estado: {emp.get_estado()}")
        print(f"   Jefe: {emp.get_jefe_inmediato()}")
        print("-" * 60)
    
    print(f"\nTotal de empleados: {len(lista_empleados)}")
    print("=" * 60)
    
    return len(lista_empleados)
