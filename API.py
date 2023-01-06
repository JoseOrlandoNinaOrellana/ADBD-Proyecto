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
        print('Unable to connect to database!')
        print('Error:', err)
        return None
    else:
        print('Connected!')
        return conn

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
        jsonify({'ERROR': 'Unable to connect to database'})

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
        jsonify({'ERROR': 'Unable to connect to database'})

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
        jsonify({'ERROR': 'Unable to connect to database'})
