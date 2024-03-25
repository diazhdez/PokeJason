from flask import Flask, render_template, request, redirect, url_for, session
import os
import conexion as db


# Configurar la aplicacion para ser ejecutado
template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__)
app.secret_key = 'M0i1Xc$GfPw3Yz@2SbQ9lKpA5rJhDtE7'


@app.route('/', methods=['GET'])
def home():
    insertObjeto = []
    if 'logueado' in session and session['logueado']:

        return render_template('index.html', datos=insertObjeto)
    else:
        return redirect('/login')

# Registro e Inicio De Sesión


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        correo = request.form.get('txtcorreo')
        contraseña = request.form.get('txtcontraseña')

        # Aquí asumimos que "connection" es un objeto de conexión MySQL ya configurado
        cursor = db.conexion.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE correo = %s AND contraseña = %s", (correo, contraseña))
        account = cursor.fetchone()
        cursor.close()

        if account:
            session['logueado'] = True
            session['id_rol'] = account[0]

            if session['id_rol'] == 1:
                return redirect(url_for('administrador'))
            else:
                return redirect('/')
        else:
            # Si no se encuentra la cuenta, muestra el mensaje como un modal
            mensaje = "Correo o Contraseña erronea"
            tipo_mensaje = "error"
            return render_template("login.html", mensaje=mensaje, tipo_mensaje=tipo_mensaje)
    return render_template("login.html")


@app.route('/registro', methods=['POST'])
def registro():
    # Importamos las variables desde el form del index.htlm
    correo = request.form["correo"]
    contraseña = request.form["contraseña"]
    nombre = request.form["nombre"]
    apellidos = request.form["apellidos"]
    if correo and contraseña and nombre and apellidos:
        cursor = db.conexion.cursor()
        # Verificar si el correo electrónico ya existe en la base de datos
        sql_verificar_correo = "SELECT COUNT(*) FROM users WHERE correo = %s"
        cursor.execute(sql_verificar_correo, (correo,))
        num_registros = cursor.fetchone()[0]

    if num_registros > 0:
        mensaje = "Correo ya en uso"
        tipo_mensaje = "error"
        return redirect(url_for("login", mensajeError=mensaje, tipo_mensaje=tipo_mensaje))
    else:
        sql = """INSERT INTO users (correo, contraseña, nombre, apellidos, id_rol) values (%s, %s, %s, %s, "2")"""
    # Declaramos a "datos" como una variable de tipo tupla para mandar la información
    datos = (correo, contraseña, nombre, apellidos)
    cursor.execute(sql, datos)
    mensaje = "Registro hecho de manera exitosa"
    tipo_mensaje = "exito"
    db.conexion.commit()
    return redirect(url_for("login", mensaje=mensaje, tipo_mensaje=tipo_mensaje))


@app.route('/logout')
def logout():
    session.clear()  # Elimina todas las variables de sesión
    return redirect('/login')  # Redirige al inicio de sesión


@app.route('/recuperar-cuenta')
def recuperar():
    return render_template('recuperar.html')


@app.route('/reestablecer')
def reestablecer():
    return render_template('reestablecer.html')


@app.route('/pokedex')
def pokedex():
    return render_template('pokedex.html')


@app.route('/favorites')
def favorites():
    cursor = db.conexion.cursor()
    cursor.execute("SELECT * FROM favorites")  # ORDER BY quejaID DESC
    datosDB = cursor.fetchall()
    total = cursor.rowcount
    # Convertir los datos a diccionario
    insertObjeto = []
    columnName = [column[0] for column in cursor.description]
    for registro in datosDB:
        insertObjeto.append(dict(zip(columnName, registro)))
    cursor.close()
    return render_template('favorites.html', data=insertObjeto, dataTotal=total)


def status_401(error):
    return redirect(url_for('login'))


def pagina_no_encontrada(error):
    return render_template('error.html'), 404


if __name__ == '__main__':
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True)
