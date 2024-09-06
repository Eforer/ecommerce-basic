from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_cors import CORS
from producto import Producto
from categoria import Categoria
import io
import csv

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Asegúrate de cambiar esto a una clave segura
CORS(app)

@app.route('/')
def home():
    categoria_id = request.args.get('categoria', type=int)
    categorias = Categoria.get_all()
    if categoria_id:
        productos = Producto.get_by_categoria(categoria_id)
    else:
        productos = Producto.get_all()
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


@app.route('/importar_productos', methods=['GET', 'POST'])
def importar_productos():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and file.filename.endswith('.csv'):
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            csv_input = csv.reader(stream)
            next(csv_input)  # Skip header row
            for row in csv_input:
                nombre, descripcion, precio, stock, categoria_id = row
                Producto.save({
                    'nombre': nombre,
                    'descripcion': descripcion,
                    'precio': float(precio),
                    'stock': int(stock),
                    'id_categoria': int(categoria_id)
                })
            flash('Productos importados exitosamente')
            return redirect(url_for('home'))
    return render_template('importar_productos.html')

if __name__ == '__main__':
    app.run(debug=True)