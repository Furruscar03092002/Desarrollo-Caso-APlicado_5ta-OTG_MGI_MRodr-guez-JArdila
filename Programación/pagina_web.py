#librerias
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from flask_mail import Mail, Message
from reportlab.pdfgen import canvas
from flask import Flask, send_file
from flask import render_template
from flask_mysqldb import MySQL
from io import BytesIO
from flask import request, redirect,  url_for, flash, render_template_string, Response, session
from reportlab.lib import pagesizes

#genera servidor con el local host y en cada función es una ruta de la pag
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'prueba'
app.secret_key = 'arroz'
mysql= MySQL(app)
app.config["SERVER_NAME"]="localhost:9191"
#--------------configuración para mandar correo--------------------
#
#----------░█▀▀▀█ ░█▀▀█ ░█▀▀▀ ░█▀▀█ ─█▀▀█ ░█▀▀█ ▀█▀ ░█▀▀▀█ 
#----------░█──░█ ░█▄▄█ ░█▀▀▀ ░█▄▄▀ ░█▄▄█ ░█▄▄▀ ░█─ ░█──░█ 
#----------░█▄▄▄█ ░█─── ░█▄▄▄ ░█─░█ ░█─░█ ░█─░█ ▄█▄ ░█▄▄▄█----------------------------------------------------------
@app.route('/Operario')
def Operario():   
    cur= mysql.connection.cursor()
    cur.execute('SELECT * FROM proyecto ORDER BY Nombre_del_proyecto ASC')
    data= cur.fetchall()
    return render_template('operario.html', proyecto = data)

#-----------------------Agregar datos etiqueta-------------------------------------
@app.route('/Nueva_etiqueta', methods=['POST'])
def Etiqueta():
    if request.method == 'POST':
        muestra = request.form['muestra']
        Proyecto = request.form['proyecto']
        Sondeo = request.form['sondeo']
        Localizacion = request.form['localizacion']
        profundidad = request.form['profundidad']
        tipo_muestra = request.form['tipo_muestra']
        golpes = request.form['golpes']
        fecha = request.form['fecha']

        try:
            cur = mysql.connection.cursor()

            # Inicia una transacción

            # Inserta datos en la tabla 'proyecto'
            nuevaetiqueta = (muestra, Proyecto, Sondeo, Localizacion, profundidad, tipo_muestra, golpes, fecha)
            consulta_proyecto = "INSERT INTO proyecto(N_de_muestra, Nombre_del_proyecto, Sondeo, Localizacion, Profundidad, Tipo_de_muestra, N_de_golpes, Fecha) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(consulta_proyecto, nuevaetiqueta)

            # Commit de la transacción
            mysql.connection.commit()

            flash('Datos guardados exitosamente')
            return redirect(url_for('Operario'))

        except Exception as e:
            # Si ocurre un error, hace un rollback de la transacción
            mysql.connection.rollback()
            flash(f'Error: {str(e)}')
            return redirect(url_for('Operario'))

        finally:
            cur.close()
            
#-------------------------------------Editar tabla----------------------------------------------------------
@app.route('/obtener_datos/<ID>')
def datos(ID):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM proyecto WHERE ID = %s ORDER BY Nombre_del_proyecto ASC', (ID,))
    data = cur.fetchall()
    if data:
        return render_template('editar_etiqueta.html', contact=data[0])
    else:
        flash('No se encontraron datos para el proyecto seleccionado')
        return redirect(url_for('Operario'))

@app.route('/actualizar_etiqueta/<string:ID>', methods=['POST'])
def actualizar_etiqueta(ID):
    if request.method == 'POST':
        muestra = request.form['muestra']
        Proyecto = request.form['proyecto']
        Sondeo = request.form['sondeo']
        Localizacion = request.form['localizacion']
        profundidad = request.form['profundidad']
        tipo_muestra = request.form['tipo_muestra']
        golpes = request.form['golpes']
        fecha = request.form['fecha']
        cur = mysql.connection.cursor()
        consulta = """
            UPDATE proyecto
            SET N_de_muestra = %s,
                Nombre_del_proyecto = %s,
                Sondeo = %s,
                Localizacion = %s,
                Profundidad = %s,
                Tipo_de_muestra = %s,
                N_de_golpes = %s,
                Fecha = %s
            WHERE ID = %s 
        """
        cur.execute(consulta, (muestra, Proyecto, Sondeo, Localizacion, profundidad, tipo_muestra, golpes, fecha, ID))
        mysql.connection.commit()
        flash('Etiqueta Actualizada')
        return redirect(url_for('Operario'))

#-------------------------------------Generar Etiqueta-------------------------------------------------------
@app.route('/Generar_etiqueta/<string:ID>')
def GenerarEtiqueta(ID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT Nombre_del_proyecto, Sondeo, Localizacion, Profundidad, Tipo_de_muestra, N_de_muestra, N_de_golpes, Fecha FROM proyecto WHERE ID = %s", (ID,))
    data = cur.fetchall()

    if data:
        # Desempaqueta la tupla de datos
        data=(Nombre_del_proyecto, Sondeo, Localizacion, Profundidad, Tipo_de_muestra, N_de_muestra, N_de_golpes, Fecha) = data[0]

        # Formato vertical de los datos con negrita
        return render_template('etiqueta.html', resultados=data)
        #return render_template_string(resultado)
    else:
        return "No se encontraron datos para el ID proporcionado."

#-------------------------------------Eliminar Etiqueta--------------------------------------------------
@app.route('/Eliminar_etiqueta/<string:ID>')
def delete_contact(ID):
    try:
        cur = mysql.connection.cursor()
        # Verificar el valor de ID
        print("Deleting ID:", ID)
        cur.execute('DELETE FROM proyecto WHERE ID = %s', (ID,))
        # Confirmar la eliminación
        print("Number of rows deleted:", cur.rowcount)
        mysql.connection.commit()
        flash('Etiqueta Eliminada')
        return redirect(url_for('Operario'))
    except Exception as e:
        # Manejar errores y mostrarlos para depuración
        print("Error:", e)
        flash('Error al eliminar etiqueta')
        return redirect(url_for('Operario'))

#-------------------------█░░ ▄▀█ █▄▄ █▀█ █▀█ ▄▀█ ▀█▀ █▀█ █▀█ █ █▀ ▀█▀ ▄▀█
#-------------------------█▄▄ █▀█ █▄█ █▄█ █▀▄ █▀█ ░█░ █▄█ █▀▄ █ ▄█ ░█░ █▀█----------------------------------------------------
    


#----------------------------Etiqueta de almacenamiento, con boton= nuevo boton= check
# -------------------------------------------------imterfaz decente= maso
#---------------------------- Recuadros de comentar del ingeniero y guardar el comentario y la retroalimentaciíon
#ñ-------- No mostrar toda la info del inge---Repreguntar
#-----------------------------en el informe comparativos de la eficiencia, tiempos y el etiquetado
#-------- agregar imagen en la tabla--generaretiqueta, check
#-----------------------------pop up para demostrar que ya se corrigió la información= # falta retroalimentacion
#-----------------------------Informe paulatino=Check

@app.route('/Laboratorista')
def Laboratorista():   
    cur= mysql.connection.cursor()
    cur.execute('SELECT * FROM proyecto ORDER BY Nombre_del_proyecto ASC')
    data= cur.fetchall()
    return render_template('laboratorista.html', proyecto = data)

#-------------------------------------Buscar muestra laboratorista----------------------------------
@app.route('/buscar_proyecto_lab', methods=['POST'])
def buscar():
    if request.method == 'POST':
        buscar_proyecto = request.form['buscar_proyecto_lab']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM proyecto WHERE Nombre_del_proyecto = %s ORDER BY ID ASC", (buscar_proyecto,))
        data = cur.fetchall()

        if data:
            return render_template('resultado_busqueda_lab.html', resultados=data)
        else:
            return "No se encontraron datos para el nombre del proyecto proporcionado."    
#------------------------------------obtener datos 3
@app.route('/obtener_datos3/<string:ID>')
def datos_buscar_lab(ID):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM proyecto WHERE ID = %s', (ID,))
    data = cur.fetchall()
    if data:
        return render_template('editar_buscar.html', contact=data[0])
    else:
        flash('No se encontraron datos para el proyecto seleccionado')
        return redirect(url_for('buscar_proyecto_lab'))
# -------------------------------------Editar tabla buscar----------------------------------------------------------
@app.route('/actualizar_buscar/<string:ID>', methods=['POST'])
def actualizar_buscar(ID):
    if request.method == 'POST':
        muestra = request.form['muestra']
        Proyecto = request.form['proyecto']
        Sondeo = request.form['sondeo']
        Localizacion = request.form['localizacion']
        profundidad = request.form['profundidad']
        tipo_muestra = request.form['tipo_muestra']
        golpes = request.form['golpes']
        humedad = request.form['humedad']
        peso = request.form['peso']
        gravas = request.form['gravas']
        arenas = request.form['arenas']
        finos = request.form['finos']
        d10 = request.form['d10']
        d50 = request.form['d50']
        d90 = request.form['d90']
        almacen = request.form['almacen']
        estado = request.form['estado']
        fecha = request.form['fecha']
        cur = mysql.connection.cursor()
        consulta = """
            UPDATE proyecto
            SET N_de_muestra = %s,
                Nombre_del_proyecto = %s,
                Sondeo = %s,
                Localizacion = %s,
                Profundidad = %s,
                Tipo_de_muestra = %s,
                N_de_golpes = %s,
                Humedad = %s,
                Peso_Unitario_gr = %s, 
                gravas = %s,
                arenas = %s,
                finos = %s,
                D10 = %s, 
                D50 = %s,
                D90 = %s,
                Almacen = %s,
                Estado = %s,
                Fecha = %s
            WHERE ID = %s
        """
        cur.execute(consulta, (muestra, Proyecto, Sondeo, Localizacion, profundidad, tipo_muestra, golpes, humedad, peso, gravas, arenas, finos, d10, d50, d90, almacen, estado, fecha, ID))
        mysql.connection.commit()
        flash('Muestra Actualizada')
        return redirect(url_for('Laboratorista'))
#--------------------------------------Corregido--------------------------------------------------------------
@app.route('/Corregido/<string:ID>')
def corregido(ID):
    try:
        cur = mysql.connection.cursor()

        # Actualizar la columna 'comentarios' a un valor vacío para el ID específico
        cur.execute('UPDATE proyecto SET comentarios = "" WHERE ID = %s', (ID,))

        mysql.connection.commit()
        flash('Comentarios de la muestra eliminados')
        return redirect(url_for('Laboratorista'))
    except Exception as ex:
        # Manejar errores y mostrarlos para depuración
        print("Error:", ex)
        flash('Error al eliminar comentarios de la muestra')
        return redirect(url_for('Laboratorista'))
#--------------------------------------Obtener de Laboratorista----------------------------------------------------------
@app.route('/obtener_datos2/<string:ID>')
def datoslab(ID):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM proyecto WHERE ID = %s', (ID,))
    data = cur.fetchall()
    if data:
        return render_template('editar_muestra.html', contact=data[0])
    else:
        flash('No se encontraron datos para el proyecto seleccionado')
        return redirect(url_for('Laboratorista'))

# -------------------------------------Editar tabla laboratorista----------------------------------------------------------
@app.route('/actualizar_muestra/<string:ID>', methods=['POST'])
def actualizar_muestra(ID):
    if request.method == 'POST':
        humedad = request.form['humedad']
        peso = request.form['peso']
        gravas = request.form['gravas']
        arenas = request.form['arenas']
        finos = request.form['finos']
        d10 = request.form['d10']
        d50 = request.form['d50']
        d90 = request.form['d90']
        almacen = request.form['almacen']
        estado = request.form['estado']

        try:
            cur = mysql.connection.cursor()

            # Inicia una transacción
            cur.execute("START TRANSACTION")

            # Actualiza datos en la tabla 'proyecto'
            consulta_proyecto = """
                UPDATE proyecto
                SET Humedad = %s,
                    Peso_Unitario_gr = %s, 
                    gravas = %s,
                    arenas = %s,
                    finos = %s,
                    D10 = %s, 
                    D50 = %s,
                    D90 = %s,
                    Almacen = %s,
                    Estado = %s
                WHERE ID = %s
            """
            cur.execute(consulta_proyecto, (humedad, peso, gravas, arenas, finos, d10, d50, d90, almacen, estado, ID))

            # Commit de la transacción
            mysql.connection.commit()

            flash('Muestra Actualizada')
            return redirect(url_for('Laboratorista'))

        except Exception as e:
            # Si ocurre un error, hace un rollback de la transacción
            mysql.connection.rollback()
            flash(f'Error: {str(e)}')
            return redirect(url_for('Laboratorista'))

        finally:
            cur.close()

#-------------------------------------Generar Stock---------------------------------------------------------
@app.route('/contador_almacen/<string:ID>')
def contador_almacen(ID):
    try:
        cur = mysql.connection.cursor()

        # Consulta para contar las repeticiones de cada valor en la columna 'Almacen'
        consulta_contador_almacen = """
            SELECT Almacen, COUNT(*) AS Repeticiones
            FROM proyecto
            GROUP BY Almacen
        """
        cur.execute(consulta_contador_almacen)
        resultados = cur.fetchall()

        # Puedes imprimir o procesar los resultados según tus necesidades
        for resultado in resultados:
            almacen = resultado[0]
            repeticiones = resultado[1]

            # Actualizar la columna 'Cantidad' en la tabla 'proyecto'
            consulta_actualizar_proyecto = """
                UPDATE proyecto
                SET Cantidad = %s
                WHERE Almacen = %s
            """
            consulta_actualizar_maximo = """
                UPDATE proyecto
                SET maximo = 50 - cantidad
            """
            cur.execute(consulta_actualizar_maximo)
            cur.execute(consulta_actualizar_proyecto, (repeticiones, almacen)) 
            cur.execute("SELECT * FROM proyecto WHERE ID = %s", (ID,))
            data2 = cur.fetchall()

        # Commit de la transacción
        mysql.connection.commit()

        # Obtener los resultados nuevamente después de las actualizaciones
        cur.execute(consulta_contador_almacen)
        data = cur.fetchall()

        return render_template('stock.html', resultados=data, resul=data2)

    except Exception as e:
        # Manejo del error, podrías agregar un mensaje flash o redireccionar a una página de error
        return f'Error: {str(e)}'

    finally:
        cur.close()

#-----------------------------------Función para obtener el nombre del proyecto por ID
def obtener_nombre_proyecto(ID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT Nombre_del_proyecto FROM proyecto WHERE ID = %s", (ID,))
    nombre_proyecto = cur.fetchone()[0]
    cur.close()
    return nombre_proyecto

#-------------------------------- Función para obtener los datos del proyecto filtrando por nombre
def obtener_datos_proyecto_por_nombre(nombre_proyecto):
    cur = mysql.connection.cursor()
    cur.execute("SELECT Nombre_del_proyecto, Localizacion, Sondeo, N_de_muestra, profundidad, Tipo_de_muestra, Humedad, Peso_Unitario_gr, gravas, arenas, finos, D10, D50, D90 FROM proyecto WHERE Nombre_del_proyecto = %s", (nombre_proyecto,))
    data = cur.fetchall()
    cur.close()
    return data
#-------------------------------------Generar Informe-------------------------------------------------------
@app.route('/Generar_informe/<string:ID>')
def Generar_informe(ID):
    try:
        cur = mysql.connection.cursor()
        nombre_proyecto = obtener_nombre_proyecto(ID)

        # Llamada a la función que realiza la consulta filtrando por nombre
        data = obtener_datos_proyecto_por_nombre(nombre_proyecto)

        if data:
            # Crear un objeto BytesIO para almacenar el PDF en memoria
            pdf_output = BytesIO()

            # Crear el archivo PDF con reportlab
            pdf = canvas.Canvas(pdf_output, pagesize=(612, 792), pageCompression=1)  # Letter size in landscape orientation (612x792 points)

            # Encabezado
            pdf.setFont("Helvetica-Bold", 20)
            pdf.drawCentredString(306, 750, f"Informe del proyecto - {nombre_proyecto}")

            # Definir márgenes y posición inicial de la cuadrícula
            margin_left = 20
            margin_right = 20
            margin_bottom = 20
            margin_top = 20
            y_position = 720

            # Dibujar la cuadrícula
            pdf.setStrokeColor('black')
            pdf.setLineWidth(1)
            #Distancia entre columnas 8.5
            col_widths = [pdf.stringWidth(header, "Helvetica-Bold", 8.5) for header in ["Nombre del proyecto", "Localizacion", "Sondeo", "N de muestra", "Profundidad", "Tipo de muestra", "Humedad", "Peso Unitario gr", "Gravas", "Arenas", "Finos", "D10", "D50", "D90"]]
            row_height = 40

            # Líneas horizontales aca se modifica que tan largas las horizontales
            for i in range(int(y_position), margin_bottom - row_height, -row_height):
                pdf.line(margin_left, i, 609 - margin_right, i)

            # Línea horizontal al final
            pdf.line(margin_left, margin_bottom, 612 - margin_right, margin_bottom)

            # Líneas verticales
            for i in range(len(col_widths) + 1):
                x = margin_left + sum(col_widths[:i])
                pdf.line(x, y_position, x, margin_bottom)

            # Encabezados de la tabla
            pdf.setFont("Helvetica-Bold", 7)
            y_position -= 10

            for i, header in enumerate(["Nombre del proyecto", "Localizacion", "Sondeo", "N de muestra", "Profundidad", "Tipo de muestra", "Humedad", "Peso Unitario gr", "Gravas", "Arenas", "Finos", "D10", "D50", "D90"]):
                x = margin_left + sum(col_widths[:i])
                pdf.drawCentredString(x + col_widths[i] / 2, y_position - row_height / 2, header)

            # Contenido de la tabla
            pdf.setFont("Helvetica", 7)
            y_position -= row_height

            for row in data:
                for i, value in enumerate(row):
                    x = margin_left + sum(col_widths[:i])
                    pdf.drawCentredString(x + col_widths[i] / 2, y_position - row_height / 2, str(value))
                y_position -= row_height

            # Guardar el PDF
            pdf.save()

            # Enviar el archivo PDF como respuesta
            pdf_output.seek(0)
            return send_file(pdf_output, as_attachment=True, download_name=f'informe_muestra_{ID}.pdf', mimetype='application/pdf')
        else:
            return "No se encontraron datos para el proyecto proporcionado."

    except Exception as e:
        return f'Error: {str(e)}'

    finally:
        cur.close()
#-------------------------------------Eliminar Muestra--------------------------------------------------
@app.route('/Eliminar_muestra/<string:ID>')
def delete(ID):
    try:
        cur = mysql.connection.cursor()
        # Verificar el valor de ID
        print("Deleting ID:", ID)
        cur.execute('DELETE FROM proyecto WHERE ID = %s', (ID,))
        # Confirmar la eliminación
        print("Number of rows deleted:", cur.rowcount)
        mysql.connection.commit()
        flash('Muestra Eliminada')
        return redirect(url_for('Laboratorista'))
    except Exception as ex:
        # Manejar errores y mostrarlos para depuración
        print("Error:", ex)
        flash('Error al eliminar muestra')
        return redirect(url_for('Laboratorista'))
#-----------------------█ █▄░█ █▀▀ █▀▀ █▄░█ █ █▀▀ █▀█ █▀█
#-----------------------█ █░▀█ █▄█ ██▄ █░▀█ █ ██▄ █▀▄ █▄█-------------------------------------------------------------------------
@app.route('/Ingeniero')
def Ingeniero():   
    cur= mysql.connection.cursor()
    cur.execute('SELECT * FROM proyecto ORDER BY Nombre_del_proyecto ASC')
    data= cur.fetchall()
    return render_template('ingeniero.html', proyecto = data)
#-----------------------Redireccionar cunado la pag no existe-----------------------------------------
@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('home'))
#-------------------------------------Comentar-----------------------------------------------------------
#-------------------------------------Buscar muestra-----------------------------------------------------
@app.route('/buscar_proyecto', methods=['POST'])
def buscar_proyecto_lab():
    if request.method == 'POST':
        buscar_proyecto = request.form['buscar_proyecto']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM proyecto WHERE Nombre_del_proyecto = %s ORDER BY ID ASC", (buscar_proyecto,))
        data = cur.fetchall()

        if data:
            return render_template('resultado_busqueda.html', resultados=data)
        else:
            return "No se encontraron datos para el nombre del proyecto proporcionado."
#-------------------------------------Comentar muestra--------------------------------------------------
@app.route('/comentar/<string:ID>', methods=['POST'])
def comentar(ID):
    if request.method == 'POST':
        comentar = request.form['comentar']
        cur = mysql.connection.cursor()
        consulta = """
            UPDATE proyecto
            SET comentarios = %s
            WHERE ID = %s
        """
        cur.execute(consulta, (comentar,ID))
        mysql.connection.commit()
        flash('Muestra Actualizada')
        return redirect(url_for('Ingeniero'))
#-------------------------------------Inicio-----------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html')   

@app.route('/acceso-login', methods=["GET","POST"])
def login():
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword' in request.form:
        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE correo = %s AND password = %s', (_correo, _password,))
        account = cur.fetchone()

        if account:
            session['logueado'] = True
            session['id'] = account[0] #id
            session['id_rol'] = account[3] #id_rol

            if session['id_rol'] == 1:
                return redirect(url_for('Operario'))
            elif session['id_rol'] == 2:
                return redirect(url_for('Laboratorista'))
            elif session['id_rol'] == 3:
                return redirect(url_for('Ingeniero'))
        else:
            return render_template('index.html', mensaje="Usuario o Contraseña Incorrectas")

#------------------------------------Registrar usuario----------------------------------------------
@app.route('/Registro')
def registro():
    return render_template('registro.html')  

@app.route('/registro_ope', methods= ["GET", "POST"])
def registro_ope(): 
    
    correo=request.form['txtCorreo']
    password=request.form['txtPassword']
    
    cur = mysql.connection.cursor()
    cur.execute(" INSERT INTO usuarios (correo, password, id_rol) VALUES (%s, %s, '1')",(correo,password))
    mysql.connection.commit()
    
    return render_template("index.html",mensaje2="Operario Registrado Exitosamente")

@app.route('/registro_lab', methods=["GET", 'POST'])
def registro_lab(): 
    correo = request.form['txtCorreo']
    password = request.form['txtPassword']
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO usuarios (correo, password, id_rol) VALUES (%s, %s, '2')", (correo, password))
    mysql.connection.commit()
    
    return render_template("index.html", mensaje3="Laboratorista Registrado Exitosamente")

@app.route('/registro_ing', methods=["GET", 'POST'])
def registro_ing(): 
    correo = request.form['txtCorreo']
    password = request.form['txtPassword']
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO usuarios (correo, password, id_rol) VALUES (%s, %s, '3')", (correo, password))
    mysql.connection.commit()
    
    return render_template("index.html", mensaje4="Ingeniero Registrado Exitosamente")

if __name__=="__main__":
    app.run(debug=True, use_reloader=False)
