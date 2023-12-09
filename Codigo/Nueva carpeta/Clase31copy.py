#--------------------------------------------------------------------
# Instalar con pip install Flask
from flask import Flask, request, jsonify
from flask import request
# Instalar con pip install flask-cors
from flask_cors import CORS
# Instalar con pip install mysql-connector-python
import mysql.connector
# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename
# No es necesario instalar, es parte del sistema standard de Python
import os
import time
#--------------------------------------------------------------------


app = Flask(__name__)
CORS(app) # Esto habilitará CORS para todas las rutas


class Newsletter:
    # Constructor de la clase
    def __init__(self, host, user, password, database):
        # Primero, establecemos una conexión sin especificar la base de datos
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()
        
        # Intentamos seleccionar la base de datos
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err


        # Una vez que la base de datos está establecida, creamos la tabla si no existe
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS inscriptos (
            codigo INT,
            nombre VARCHAR(255) NOT NULL,
            correo VARCHAR(255) NOT NULL)''')
        self.conn.commit()


        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)


    #----------------------------------------------------------------
    def listar_inscriptos(self):
        self.cursor.execute("SELECT * FROM inscriptos")
        inscriptos = self.cursor.fetchall()
        return inscriptos


    #----------------------------------------------------------------
    def consultar_inscripto(self, codigo):
        # Consultamos un inscripto a partir de su código
        self.cursor.execute(f"SELECT * FROM inscriptos WHERE codigo = {codigo}")
        return self.cursor.fetchone()


    #----------------------------------------------------------------
    def mostrar_inscripto(self, codigo):
        # Mostramos los datos de un inscripto a partir de su código
        inscripto = self.consultar_inscripto(codigo)
        if inscripto:
            print("-" * 40)
            print(f"Código.....: {inscripto['codigo']}")
            print(f"Nombre.....: {inscripto['nombre']}")
            print(f"Correo.....: {inscripto['correo']}")
            print("-" * 40)
        else:
            print("Inscripto no encontrado.")
    #----------------------------------------------------------------
    def agregar_inscripto(self, codigo, nombre, correo):


        self.cursor.execute(f"SELECT * FROM inscriptos WHERE codigo = {codigo}")
        inscripto_existe = self.cursor.fetchone()
        if inscripto_existe:
            return False
        
        sql = "INSERT INTO inscriptos (codigo, nombre, correo) VALUES (%s, %s, %s)"
        valores = (codigo, nombre, correo)
        self.cursor.execute(sql,valores)
        self.conn.commit()
        return True

    #----------------------------------------------------------------
    def eliminar_inscripto(self, codigo):
        # Eliminamos un inscripto de la tabla a partir de su código
        self.cursor.execute(f"DELETE FROM inscriptos WHERE codigo = {codigo}")
        self.conn.commit()
        return self.cursor.rowcount > 0

    #----------------------------------------------------------------
    def modificar_inscripto(self, codigo, nuevo_nombre, nuevo_correo):
        sql = "UPDATE inscriptos SET nombre = %s, correo = %s WHERE codigo = %s"
        valores = (nuevo_nombre, nuevo_correo, codigo)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0


#--------------------------------------------------------------------
# Cuerpo del programa
#--------------------------------------------------------------------
# Crear una instancia de la clase Newsletter
newsletter = Newsletter(host='localhost', user='root', password='', database='miNewsletter')


# Carpeta para guardar las imagenes
ruta_destino = 'static/img/'


#--------------------------------------------------------------------
@app.route("/inscriptos", methods=["GET"])
def listar_inscriptos():
    inscriptos = newsletter.listar_inscriptos()
    return jsonify(inscriptos)


#--------------------------------------------------------------------
@app.route("/inscriptos/<int:codigo>", methods=["GET"])
def mostrar_inscripto(codigo):
    newsletter.mostrar_inscripto(codigo)
    inscripto = newsletter.consultar_inscripto(codigo)
    if inscripto:
        return jsonify(inscripto)
    else:
        return "inscripto no encontrado", 404


@app.route("/inscriptos", methods=["POST"])
def agregar_inscripto():
    # Recojo los datos del form
    codigo = request.form['codigo']
    nombre = request.form['nombre']
    correo = request.form['correo']
    #precio = request.form['precio']
    #proveedor = request.form['proveedor']  
    #imagen = request.files['imagen']
    #nombre_imagen = secure_filename(imagen.filename)


    #nombre_base, extension = os.path.splitext(nombre_imagen)
    #nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"
    #imagen.save(os.path.join(ruta_destino, nombre_imagen))


    if newsletter.agregar_inscripto(codigo, nombre, correo):
        return jsonify({"mensaje": "inscripto agregado"}), 201
    else:
        return jsonify({"mensaje": "inscripto ya existe"}), 400


@app.route("/inscriptos/<int:codigo>", methods=["DELETE"])
def eliminar_inscripto(codigo):
    # Primero, obtén la información del inscripto para encontrar la imagen
    inscripto = newsletter.consultar_inscripto(codigo)
    if inscripto:
        # Eliminar la imagen asociada si existe
      #  ruta_imagen = os.path.join(ruta_destino, inscripto['imagen_url'])
       # if os.path.exists(ruta_imagen):
        #    os.remove(ruta_imagen)


        # Luego, elimina el inscripto del catálogo
        if newsletter.eliminar_inscripto(codigo):
            return jsonify({"mensaje": "inscripto eliminado"}), 200
        else:
            return jsonify({"mensaje": "Error al eliminar el inscripto"}), 500
    else:
        return jsonify({"mensaje": "inscripto no encontrado"}), 404


@app.route("/inscriptos/<int:codigo>", methods=["PUT"])
def modificar_inscripto(codigo):
    # Recojo los datos del form
    nuevo_nombre = request.form.get("nombre")
    nuevo_correo = request.form.get("correo")
    


    # Procesamiento de la imagen
    #imagen = request.files['imagen']
    #nombre_imagen = secure_filename(imagen.filename)
    #nombre_base, extension = os.path.splitext(nombre_imagen)
    #nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"
    #imagen.save(os.path.join(ruta_destino, nombre_imagen))
    
    # Actualización del inscripto
    if newsletter.modificar_inscripto(codigo, nuevo_nombre, nuevo_correo):
        return jsonify({"mensaje": "inscripto modificado"}), 200
    else:
        return jsonify({"mensaje": "inscripto no encontrado"}), 404


if __name__ == "__main__":
    app.run(debug=True)
