from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS
from producto import Producto

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Asegúrate de cambiar esto a una clave segura
CORS(app)

@app.route('/')
def home():
    productos = Producto.get_all()
    # Asumiendo que tienes una clase similar para Categoria
    # categorias = Categoria.get_all()
    categorias = []  # Por ahora, dejamos esto vacío
    return render_template('home.html', productos=productos, categorias=categorias)

@app.route('/producto/<int:id>')
def detalle_producto(id):
    producto = Producto.get_by_id(id)
    if producto:
        return render_template('producto.html', producto=producto)
    else:
        return "Producto no encontrado", 404

@app.route('/agregar_al_carrito/<int:id>', methods=['POST'])
def agregar_al_carrito(id):
    if 'carrito' not in session:
        session['carrito'] = []
    
    producto = Producto.get_by_id(id)
    if producto:
        carrito = session['carrito']
        item = next((item for item in carrito if item['id'] == id), None)
        if item:
            item['cantidad'] += 1
        else:
            carrito.append({
                'id': producto.id_producto,
                'nombre': producto.nombre,
                'descripcion': producto.descripcion,
                'precio': float(producto.precio),
                'cantidad': 1
            })
        session['carrito'] = carrito
        return f"<div class='text-green-500'>Producto {producto.nombre} añadido al carrito</div>"
    else:
        return "Producto no encontrado", 404

@app.route('/carrito')
def ver_carrito():
    carrito = session.get('carrito', [])
    total = sum(item['precio'] * item['cantidad'] for item in carrito)
    return render_template('carrito.html', carrito=carrito, total=total)

if __name__ == '__main__':
    app.run(debug=True)