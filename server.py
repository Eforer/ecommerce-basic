from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
import pymysql
import os

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
db_config = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'password'),
    'database': os.environ.get('DB_NAME', 'ecommerce_db'),
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    return pymysql.connect(**db_config)

@app.route('/')
def home():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM producto')
            productos = cursor.fetchall()
        
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM categoria')
            categorias = cursor.fetchall()
    finally:
        connection.close()
    
    return render_template('home.html', productos=productos, categorias=categorias)

@app.route('/producto/<int:id>')
def detalle_producto(id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM producto WHERE id_producto = %s', (id,))
            producto = cursor.fetchone()
        if producto:
            return render_template('producto.html', producto=producto)
        else:
            return "Producto no encontrado", 404
    finally:
        connection.close()

@app.route('/agregar_al_carrito/<int:id>', methods=['POST'])
def agregar_al_carrito(id):
    # Aquí iría la lógica para agregar al carrito
    # Por ahora, solo devolvemos un mensaje de éxito
    return f"<div class='text-green-500'>Producto {id} añadido al carrito</div>"

if __name__ == '__main__':
    app.run(debug=True)