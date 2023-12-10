import pymysql
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Cambia los valores según tu configuración
conexion_bd = pymysql.connect(
    host="localhost",
    user="root",
    password="",  # <-- Deja la contraseña en blanco si no tienes una
    database="newsletter",
    port=3306,  # Puerto predeterminado para MySQL
)

cursor = conexion_bd.cursor()

@app.route('/')
def index():
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    return render_template('index.html', usuarios=usuarios)

@app.route('/newsletter')
def newsletter():
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    return render_template('newsletter.html', usuarios=usuarios)

@app.route('/contacto')
def contacto():
    # Puedes agregar código para manejar la página de contacto
    return render_template('contacto.html')

@app.route('/cuidados')
def cuidados():
    # Puedes agregar código para manejar la página de cuidados
    return render_template('cuidados.html')

@app.route('/enconstruccion')
def enconstruccion():
    # Puedes agregar código para manejar la página de enconstruccion
    return render_template('enconstruccion.html')

@app.route('/preguntas')
def preguntas():
    # Puedes agregar código para manejar la página de preguntas
    return render_template('preguntas.html')

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form['nombre']
    correo = request.form['correo']
    cursor.execute("INSERT INTO usuarios (nombre, correo) VALUES (%s, %s)", (nombre, correo))
    conexion_bd.commit()
    # No hay instrucción de redirección, el formulario se enviará a la misma URL
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    return render_template('newsletter.html', usuarios=usuarios)

# ...

@app.route('/modificar/<int:id>', methods=['GET', 'POST'])
def modificar(id):
    if request.method == 'POST':
        nuevo_nombre = request.form['nombre']
        nuevo_correo = request.form['correo']
        cursor.execute("UPDATE usuarios SET nombre=%s, correo=%s WHERE id=%s", (nuevo_nombre, nuevo_correo, id))
        conexion_bd.commit()
        # Después de modificar, redirige a la página principal
        return redirect(url_for('index'))
    else:
        # Obtén el usuario específico de la base de datos
        cursor.execute("SELECT * FROM usuarios WHERE id=%s", (id,))
        usuario = cursor.fetchone()
        return render_template('modificar.html', usuario=usuario)




@app.route('/dar_de_baja/<int:id>', methods=['GET', 'POST'])
def dar_de_baja(id):
    if request.method == 'POST':
        cursor.execute("DELETE FROM usuarios WHERE id=%s", (id,))
        conexion_bd.commit()
        # Después de dar de baja, redirige a la misma página (puedes cambiar la URL según sea necesario)
        return redirect(url_for('index'))
    else:
        # Obtén el usuario específico de la base de datos
        cursor.execute("SELECT * FROM usuarios WHERE id=%s", (id,))
        usuario = cursor.fetchone()
        return render_template('dar_de_baja.html', usuario=usuario)




# ...



if __name__ == '__main__':
    app.run(debug=True, port=5001)
