import os
import psycopg2
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_db_connection():
    try:
        conn = psycopg2.connect(host = os.getenv('DB_URL'),
                                database = os.getenv('DB_NAME'),
                                user = os.getenv('DB_USERNAME'),
                                password = os.getenv('DB_PASSWORD'))
    except psycopg2.Error as err:
        print('Fallo al intentar conectarse a la base de datos!')
        print('Error:', err)
        return None
    else:
        print('Se ha conectado a la base de datos con éxito!')
        return conn

#################################### Clientes ####################################

@app.route('/clientes', methods=['POST'])
def crear_client():
    conn = get_db_connection()
    if conn != None:
        cur = conn.cursor()
        dni = request.json['DNI']
        nombre = request.json['Nombre']
        apellidos = request.json['Apellidos']
        correo = request.json['Correo']
        telefono = request.json['Telefono']
        try:
            cur.execute('INSERT INTO cliente '
                        'VALUES (%s, %s, %s, %s, %s)', 
                        [dni, nombre, apellidos, correo, telefono])
            conn.commit()
            cur.close()
            conn.close()
        except psycopg2.Error as err:
            print('Error:', err)
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail}), 500
        else:
            return jsonify({'Cliente creado': dni}), 201
    else:
        jsonify({'ERROR': 'Fallo al intentar conectarse a la base de datos'}), 502

@app.route('/clientes/<dni>', methods=['GET'])
def leer_cliente(dni):
    conn = get_db_connection()
    if conn != None:
        cur = conn.cursor()
        try:
            cur.execute('SELECT * '
                        'FROM cliente '
                        'WHERE dni = %s',
                        [dni])
            cliente = cur.fetchone()
            cur.close()
            conn.close()
        except psycopg2.Error as err:
            print('Error:', err)
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail}), 500
        else:
            if cliente != None:
                return jsonify({
                        'DNI': cliente[0],
                        'Nombre': cliente[1],
                        'Apellidos': cliente[2],
                        'Correo': cliente[3],
                        'Telefono': cliente[4]
                        })
            else:
                return jsonify({'ERROR': 'No existe el cliente'}), 404
    else:
        jsonify({'ERROR': 'Fallo al intentar conectarse a la base de datos'}), 502

@app.route('/clientes/<dni>', methods=['PUT'])
def actualizar_cliente(dni):
    conn = get_db_connection()
    if conn != None:
        cur = conn.cursor()
        try:
            nombre = request.json['Nombre']
            apellidos = request.json['Apellidos']
            correo = request.json['Correo']
            telefono = request.json['Telefono']

            cur.execute('UPDATE cliente '
                        'SET nombre = %s, apellidos = %s, correo = %s, telefono = %s '
                        'WHERE dni = %s'
                        'RETURNING dni',
                        [nombre, apellidos, correo, telefono, dni])
            cliente = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()
        except psycopg2.Error as err:
            print('Error:', err)
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail}), 500
        else:
            if cliente != None:
                return jsonify({'Cliente actualizado': dni}), 201
            else:
                return jsonify({'ERROR': 'No existe el cliente'}), 404
    else:
        return jsonify({'ERROR': 'Fallo al intentar conectarse a la base de datos'}), 502

@app.route('/clientes/<dni>', methods=['DELETE'])
def eliminar_cliente(dni):
    conn = get_db_connection()
    if conn != None:
        cur = conn.cursor()
        try:
            cur.execute('DELETE FROM cliente '
                        'WHERE dni = %s '
                        'RETURNING dni',
                        [dni])
            cliente = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()
        except psycopg2.Error as err:
            print('Error:', err)
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail}), 500
        else:
            if cliente != None:
                return jsonify({'Cliente borrado': dni}), 200
            else:
                return jsonify({'ERROR': 'No existe el cliente'}), 404
    else:
        jsonify({'ERROR': 'Fallo al intentar conectarse a la base de datos'}), 502

#################################### Subscripciones ####################################

@app.route('/subscripciones', methods=['POST'])
def crear_subscripcion():
    conn = get_db_connection()
    if conn != None:
        cur = conn.cursor()
        dni = request.json['DNI']
        nombre = request.json['Nombre']
        f_vencimiento = request.json['F_Venc']
        try:
            cur.execute('INSERT INTO SUBSCRIPCION '
                        'VALUES ((SELECT ID FROM PLAN WHERE NOMBRE = %s), %s, NOW(), %s)', 
                        [nombre, dni , f_vencimiento])
            conn.commit()
            cur.close()
            conn.close()
        except psycopg2.Error as err:
            print('Error:', err)
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail}), 500
        else:
            return jsonify({'Subscripción registrada': dni + '-' + nombre}), 201
    else:
        jsonify({'ERROR': 'Fallo al intentar conectarse a la base de datos'}), 502

@app.route('/subscripciones/<dni>', methods=['GET'])
def leer_subscripcion(dni):
    conn = get_db_connection()
    if conn != None:
        cur = conn.cursor()
        try:
            cur.execute(
                'SELECT nombre, fecha_vencimiento '
                'FROM plan '
                'INNER JOIN subscripcion ON subscripcion.id = plan.id '
                'WHERE dni = %s',
                        [dni])
            subscripcion = cur.fetchall()
            cur.close()
            conn.close()
        except psycopg2.Error as err:
            print('Error:', err)
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail}), 500
        else:
            if subscripcion != None:
                return jsonify({'Subscripciones': subscripcion}), 200
            else:
                return jsonify({'ERROR': 'El cliente no tiene ninguna subscripción registrada'}), 404
    else:
        jsonify({'ERROR': 'Fallo al intentar conectarse a la base de datos'}), 502
        

@app.route('/subscripciones', methods=['PUT'])
def actualizar_subscripcion():
    conn = get_db_connection()
    if conn != None:
        cur = conn.cursor()
        try:
            dni = request.json['DNI']
            nombre = request.json['Nombre']
            f_vencimiento = request.json['F_Venc']

            cur.execute('UPDATE subscripcion '
                        'SET FECHA_VENCIMIENTO = %s '
                        'WHERE id = (SELECT ID FROM PLAN WHERE NOMBRE = %s) AND dni = %s '
                        'RETURNING FECHA_VENCIMIENTO, DNI',
                        [f_vencimiento, nombre, dni])
            subscripcion = cur.fetchone()       
            conn.commit()
            cur.close()
            conn.close()
        except psycopg2.Error as err:
            print('Error:', err)
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail}), 500
        else:
            if subscripcion != None:
                return jsonify({'Subscripcion actualizada': nombre}), 201
            else:
                return jsonify({'ERROR': 'No existe una subscripción con el cliente indicado'}), 404
    else:
        return jsonify({'ERROR': 'Fallo al intentar conectarse a la base de datos'}), 502

####### No es necesario la operación DELETE ya que todas las subscripciones deben ser registradas una vez se realice el pago.
####### Aunque estén caducadas, no interesa que se eliminen.

#################################### Empleados ####################################

@app.route('/empleados', methods=['POST'])
def registrar_empleado():
    conn = get_db_connection()
    if conn != None:
        cur = conn.cursor()
        nombre = request.json['Nombre']
        apellidos = request.json['Apellidos']
        dni = request.json['DNI']
        correo = request.json['Correo']
        telefono = request.json['Telefono']
        salario = request.json['Salario']
        tipo = request.json['Tipo']
        try:
            cur.execute('INSERT INTO EMPLEADO '
                        'VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                        [dni, nombre, apellidos, correo, telefono, salario, tipo])
            conn.commit()
            cur.close()
            conn.close()
        except psycopg2.Error as err:
            print('Error:', err)
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail}), 500
        else:
            return jsonify({'Empleado registrado': nombre}), 201
    else:
        return jsonify({'ERROR': 'Fallo al intentar conectarse a la base de datos'}), 502

@app.route('/empleados/<dni>', methods=['GET'])
def datos_empleado(dni):
    conn = get_db_connection()
    if conn != None:
        cur = conn.cursor()
        try:
            cur.execute(
                'SELECT * '
                'FROM empleado '
                'WHERE dni = %s',
                        [dni])
            empleado = cur.fetchall()
            cur.close()
            conn.close()
        except psycopg2.Error as err:
            print('Error:', err)
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail}), 500
        else:
            if empleado != None:
                return jsonify({'Empleado': empleado}), 200
            else:
                return jsonify({'ERROR': 'No existe ningún empleado registrado con el DNI indicado.'}), 404
    else:
        return jsonify({'ERROR': 'Fallo al intentar conectarse a la base de datos'}), 502
        

@app.route('/empleados/<dni>', methods=['PUT'])
def actualizar_empleado(dni):
    conn = get_db_connection()
    if conn != None:
        cur = conn.cursor()
        try:
            nombre = request.json['Nombre']
            apellidos = request.json['Apellidos']
            correo = request.json['Correo']
            telefono = request.json['Telefono']
            salario = request.json['Salario']
            tipo = request.json['Tipo']

            cur.execute('UPDATE empleado '
                        'SET NOMBRE = %s, APELLIDOS = %s, CORREO = %s, TELEFONO = %s, SALARIO = %s, TIPO = %s '
                        'WHERE DNI = %s '
                        'RETURNING NOMBRE',
                        [nombre, apellidos, correo, telefono, salario, tipo, dni])
            empleado = cur.fetchone()       
            conn.commit()
            cur.close()
            conn.close()
        except psycopg2.Error as err:
            print('Error:', err)
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail}), 500
        else:
            if empleado != None:
                return jsonify({'Datos del empleado actualizados': nombre}), 201
            else:
                return jsonify({'ERROR': 'No existe ningún empleado registrado con el DNI indicado.'}), 404
    else:
        return jsonify({'ERROR': 'Fallo al intentar conectarse a la base de datos'}), 502

@app.route('/empleados/<dni>', methods=['DELETE'])
def eliminar_empleado(dni):
    conn = get_db_connection()
    if conn != None:
        cur = conn.cursor()
        try:
            cur.execute('DELETE FROM empleado '
                        'WHERE dni = %s '
                        'RETURNING dni',
                        [dni])
            empleado = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()
        except psycopg2.Error as err:
            print('Error:', err)
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail}), 500
        else:
            if empleado != None:
                return jsonify({'Empleado borrado': dni}), 200
            else:
                return jsonify({'ERROR': 'No existe ningún empleado registrado con el DNI indicado.'}), 404
    else:
        return jsonify({'ERROR': 'Fallo al intentar conectarse a la base de datos'}), 502


#################################### Encargados ####################################

@app.route('/encargados', methods=['POST'])
def registrar_encargado():
    conn = get_db_connection()
    if conn != None:
        cur = conn.cursor()
        nombre = request.json['Nombre']
        apellidos = request.json['Apellidos']
        dni = request.json['DNI']
        correo = request.json['Correo']
        telefono = request.json['Telefono']
        salario = request.json['Salario']
        try:
            cur.execute('INSERT INTO ENCARGADO '
                        'VALUES (%s, %s, %s, %s, %s, %s)', 
                        [dni, nombre, apellidos, correo, telefono, salario])
            conn.commit()
            cur.close()
            conn.close()
        except psycopg2.Error as err:
            print('Error:', err)
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail}), 500
        else:
            return jsonify({'Encargado registrado': nombre}), 201
    else:
        return jsonify({'ERROR': 'Fallo al intentar conectarse a la base de datos'}), 502

@app.route('/encargados/<dni>', methods=['GET'])
def datos_encargado(dni):
    conn = get_db_connection()
    if conn != None:
        cur = conn.cursor()
        try:
            cur.execute(
                'SELECT * '
                'FROM encargado '
                'WHERE dni = %s',
                        [dni])
            encargado = cur.fetchall()
            cur.close()
            conn.close()
        except psycopg2.Error as err:
            print('Error:', err)
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail}), 500
        else:
            if encargado != None:
                return jsonify({'Encargado': encargado}), 200
            else:
                return jsonify({'ERROR': 'No existe ningún encargado registrado con el DNI indicado.'}), 404
    else:
        jsonify({'ERROR': 'Fallo al intentar conectarse a la base de datos'}), 502
        

@app.route('/encargados/<dni>', methods=['PUT'])
def actualizar_encargado(dni):
    conn = get_db_connection()
    if conn != None:
        cur = conn.cursor()
        try:
            nombre = request.json['Nombre']
            apellidos = request.json['Apellidos']
            correo = request.json['Correo']
            telefono = request.json['Telefono']
            salario = request.json['Salario']

            cur.execute('UPDATE encargado '
                        'SET NOMBRE = %s, APELLIDOS = %s, CORREO = %s, TELEFONO = %s, SALARIO = %s'
                        'WHERE DNI = %s '
                        'RETURNING NOMBRE',
                        [nombre, apellidos, correo, telefono, salario, dni])
            encargado = cur.fetchone()       
            conn.commit()
            cur.close()
            conn.close()
        except psycopg2.Error as err:
            print('Error:', err)
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail}), 500
        else:
            if encargado != None:
                return jsonify({'Datos del encargado actualizados': nombre}), 201
            else:
                return jsonify({'ERROR': 'No existe ningún encargado registrado con el DNI indicado.'}), 404
    else:
        return jsonify({'ERROR': 'Fallo al intentar conectarse a la base de datos'}), 502

@app.route('/encargados/<dni>', methods=['DELETE'])
def eliminar_encargado(dni):
    conn = get_db_connection()
    if conn != None:
        cur = conn.cursor()
        try:
            cur.execute('DELETE FROM encargado '
                        'WHERE dni = %s '
                        'RETURNING dni',
                        [dni])
            encargado = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()
        except psycopg2.Error as err:
            print('Error:', err)
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail}), 500
        else:
            if encargado != None:
                return jsonify({'Encargado borrado': dni}), 200
            else:
                return jsonify({'ERROR': 'No existe ningún encargado registrado con el DNI indicado.'}), 404
    else:
        jsonify({'ERROR': 'Fallo al intentar conectarse a la base de datos'}), 502

#################################### Monitores ####################################

@app.route('/monitores/<dni>', methods=['GET'])
def datos_monitor(dni):
    conn = get_db_connection()
    if conn != None:
        cur = conn.cursor()
        try:
            cur.execute(
                'SELECT nombre '
                'FROM monitor_actividad INNER JOIN actividad '
                'ON monitor_actividad.id = actividad.id '
                'WHERE dni = %s',
                        [dni])
            actividad = cur.fetchone()
            cur.close()
            conn.close()
        except psycopg2.Error as err:
            print('Error:', err)
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail}), 500
        else:
            if actividad != None:
                return jsonify({'Actividad': actividad}), 200
            else:
                return jsonify({'ERROR': 'No existe ningún monitor registrado con el DNI indicado.'}), 404
    else:
        jsonify({'ERROR': 'Fallo al intentar conectarse a la base de datos'}), 502

@app.route('/monitores', methods=['POST'])
def asignar_monitor():
    conn = get_db_connection()
    if conn != None:
        cur = conn.cursor()
        dni = request.json['DNI']
        id = request.json['ID']
        try:
            cur.execute('INSERT INTO MONITOR_ACTIVIDAD '
                        'VALUES (%s, %s)', 
                        [dni, id])
            conn.commit()
            cur.close()
            conn.close()
        except psycopg2.Error as err:
            print('Error:', err)
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail}), 500
        else:
            return jsonify({'Monitor asignado': dni}), 201
    else:
        return jsonify({'ERROR': 'Fallo al intentar conectarse a la base de datos'}), 502

@app.route('/monitores/<dni>', methods=['DELETE'])
def eliminar_monitor(dni):
    conn = get_db_connection()
    if conn != None:
        cur = conn.cursor()
        try:
            cur.execute('DELETE FROM MONITOR_ACTIVIDAD '
                        'WHERE dni = %s'
                        'RETURNING dni',
                        [dni])
            monitor = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()
        except psycopg2.Error as err:
            print('Error:', err)
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail}), 500
        else:
            if monitor != None:
                return jsonify({'Monitor borrado': dni}), 200
            else:
                return jsonify({'ERROR': 'No existe ningún monitor registrado con el DNI indicado.'}), 404
    else:
        jsonify({'ERROR': 'Fallo al intentar conectarse a la base de datos'}), 502

#################################### Limpiadores ####################################

@app.route('/limpiadores/<dni>', methods=['GET'])
def datos_limpiador(dni):
    conn = get_db_connection()
    if conn != None:
        cur = conn.cursor()
        try:
            cur.execute(
                'SELECT numero '
                'FROM limpiador_sala '
                'WHERE dni = %s',
                        [dni])
            sala = cur.fetchone()
            cur.close()
            conn.close()
        except psycopg2.Error as err:
            print('Error:', err)
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail}), 500
        else:
            if sala != None:
                return jsonify({'Sala': sala}), 200
            else:
                return jsonify({'ERROR': 'No existe ningún limpiador registrado con el DNI indicado.'}), 404
    else:
        jsonify({'ERROR': 'Fallo al intentar conectarse a la base de datos'}), 502

@app.route('/limpiadores', methods=['POST'])
def asignar_limpiador():
    conn = get_db_connection()
    if conn != None:
        cur = conn.cursor()
        dni = request.json['DNI']
        numero = request.json['Numero']
        try:
            cur.execute('INSERT INTO limpiador_sala '
                        'VALUES (%s, %s)', 
                        [dni, numero])
            conn.commit()
            cur.close()
            conn.close()
        except psycopg2.Error as err:
            print('Error:', err)
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail}), 500
        else:
            return jsonify({'limpiador asignado a la sala': numero}), 201
    else:
        return jsonify({'ERROR': 'Fallo al intentar conectarse a la base de datos'}), 502

@app.route('/limpiadores/<dni>', methods=['DELETE'])
def eliminar_limpiador(dni):
    conn = get_db_connection()
    if conn != None:
        cur = conn.cursor()
        try:
            cur.execute('DELETE FROM limpiador_sala '
                        'WHERE dni = %s'
                        'RETURNING dni',
                        [dni])
            limpiador = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()
        except psycopg2.Error as err:
            print('Error:', err)
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail}), 500
        else:
            if limpiador != None:
                return jsonify({'limpiador borrado': dni}), 200
            else:
                return jsonify({'ERROR': 'No existe ningún limpiador registrado con el DNI indicado.'}), 404
    else:
        jsonify({'ERROR': 'Fallo al intentar conectarse a la base de datos'}), 502

#################################### Actividades ####################################

@app.route('/actividades', methods=['POST'])
def registrar_actividad():
    conn = get_db_connection()
    if conn != None:
        cur = conn.cursor()
        id = request.json['ID']
        nombre = request.json['Nombre']
        plazas = request.json['Plazas']
        numero = request.json['Numero']
        try:
            cur.execute('INSERT INTO actividad '
                        'VALUES (%s, %s, %s, %s)', 
                        [id, nombre, plazas, numero])
            conn.commit()
            cur.close()
            conn.close()
        except psycopg2.Error as err:
            print('Error:', err)
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail}), 500
        else:
            return jsonify({'Actividad registrada': nombre}), 201
    else:
        return jsonify({'ERROR': 'Fallo al intentar conectarse a la base de datos'}), 502

@app.route('/actividades/<id>', methods=['GET'])
def datos_actividad(id):
    conn = get_db_connection()
    if conn != None:
        cur = conn.cursor()
        try:
            cur.execute(
                'SELECT * '
                'FROM actividad '
                'WHERE id = %s',
                        [id])
            actividad = cur.fetchall()
            cur.close()
            conn.close()
        except psycopg2.Error as err:
            print('Error:', err)
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail}), 500
        else:
            if actividad != None:
                return jsonify({'actividad': actividad}), 200
            else:
                return jsonify({'ERROR': 'No existe ninguna actividad registrado con el id indicado.'}), 404
    else:
        jsonify({'ERROR': 'Fallo al intentar conectarse a la base de datos'}), 502
        

@app.route('/actividades/<id>', methods=['PUT'])
def actualizar_actividad(id):
    conn = get_db_connection()
    if conn != None:
        cur = conn.cursor()
        try:
            nombre = request.json['Nombre']
            plazas = request.json['Plazas']
            numero = request.json['Numero']

            cur.execute('UPDATE actividad '
                        'SET NOMBRE = %s, PLAZAS = %s, NUMERO = %s'
                        'WHERE id = %s '
                        'RETURNING NOMBRE',
                        [nombre, plazas, numero, id])
            actividad = cur.fetchone()       
            conn.commit()
            cur.close()
            conn.close()
        except psycopg2.Error as err:
            print('Error:', err)
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail}), 500
        else:
            if actividad != None:
                return jsonify({'Datos actualizados': nombre}), 201
            else:
                return jsonify({'ERROR': 'No existe ninguna actividad registrada con el id indicado.'}), 404
    else:
        return jsonify({'ERROR': 'Fallo al intentar conectarse a la base de datos'}), 502

@app.route('/actividades/<id>', methods=['DELETE'])
def eliminar_actividad(id):
    conn = get_db_connection()
    if conn != None:
        cur = conn.cursor()
        try:
            cur.execute('DELETE FROM actividad '
                        'WHERE id = %s '
                        'RETURNING id',
                        [id])
            actividad = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()
        except psycopg2.Error as err:
            print('Error:', err)
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail}), 500
        else:
            if actividad != None:
                return jsonify({'actividad borrada': id}), 200
            else:
                return jsonify({'ERROR': 'No existe ninguna actividad registrada con el id indicado.'}), 404
    else:
        jsonify({'ERROR': 'Fallo al intentar conectarse a la base de datos'}), 502

