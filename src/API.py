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

#################################### CLIENTE ####################################

@app.route('/cliente', methods=['POST'])
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
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail})
        else:
            return jsonify({'Cliente creado': dni})
    else:
        jsonify({'ERROR': 'Fallo al intentar conectarse a la base de datos'})

@app.route('/cliente/<dni>', methods=['GET'])
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
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail})
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
                return jsonify({'ERROR': 'No existe el cliente'})
    else:
        jsonify({'ERROR': 'Fallo al intentar conectarse a la base de datos'})

@app.route('/cliente/<dni>', methods=['PUT'])
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
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail})
        else:
            if cliente != None:
                return jsonify({'Cliente actualizado': dni})
            else:
                return jsonify({'ERROR': 'No existe el cliente'})
    else:
        return jsonify({'ERROR': 'No existe el cliente'})

@app.route('/cliente/<dni>', methods=['DELETE'])
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
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail})
        else:
            if cliente != None:
                return jsonify({'Cliente borrado': dni})
            else:
                return jsonify({'ERROR': 'No existe el cliente'})
    else:
        jsonify({'ERROR': 'Fallo al intentar conectarse a la base de datos'})

#################################### SUBSCRIPCIÓN ####################################

@app.route('/subscripcion', methods=['POST'])
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
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail})
        else:
            return jsonify({'Subscripción registrada': dni + '-' + nombre})
    else:
        jsonify({'ERROR': 'Fallo al intentar conectarse a la base de datos'})

@app.route('/subscripcion/<dni>', methods=['GET'])
def leer_subscripcion(dni):
    conn = get_db_connection()
    if conn != None:
        cur = conn.cursor()
        try:
            cur.execute(
                'SELECT nombre '
                'FROM plan '
                'INNER JOIN subscripcion ON subscripcion.id = plan.id '
                'WHERE dni = %s',
                        [dni])
            subscripcion = cur.fetchall()
            cur.close()
            conn.close()
        except psycopg2.Error as err:
            print('Error:', err)
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail})
        else:
            if subscripcion != None:
                return jsonify({'Subscripciones': subscripcion})
            else:
                return jsonify({'ERROR': 'El cliente no tiene ninguna subscripción registrada'})
    else:
        jsonify({'ERROR': 'Fallo al intentar conectarse a la base de datos'})
        

@app.route('/subscripcion', methods=['PUT'])
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
            return jsonify({'ERRORCODE': err.pgcode, 'ERROR': err.diag.message_primary, 'DETAIL': err.diag.message_detail})
        else:
            if subscripcion != None:
                return jsonify({'Subscripcion actualizada': nombre})
            else:
                return jsonify({'ERROR': 'No existe una subscripción con el cliente indicado'})
    else:
        return jsonify({'ERROR': 'No existe una subscripción con el cliente indicado'})