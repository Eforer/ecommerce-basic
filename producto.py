from mysqlconnection import connectToMySQL

class Producto:
    def __init__(self, data):
        self.id_producto = data['id_producto']
        self.nombre = data['nombre']
        self.descripcion = data['descripcion']
        self.precio = data['precio']
        self.stock = data['stock']
        self.categoria_id = data['id_categoria']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM PRODUCTO;"
        resultados = connectToMySQL('ecommerce_db').query_db(query)
        productos = []
        for producto in resultados:
            productos.append(cls(producto))
        return productos

    @classmethod
    def get_by_id(cls, id_producto):
        query = "SELECT * FROM PRODUCTO WHERE id_producto = %(id)s;"
        data = {'id': id_producto}
        resultados = connectToMySQL('ecommerce_db').query_db(query, data)
        if resultados:
            return cls(resultados[0])
        return None

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO PRODUCTO (nombre, descripcion, precio, stock, id_categoria) 
        VALUES (%(nombre)s, %(descripcion)s, %(precio)s, %(stock)s, %(id_categoria)s);
        """
        return connectToMySQL('ecommerce_db').query_db(query, data)

    @classmethod
    def update(cls, data):
        query = """
        UPDATE PRODUCTO 
        SET nombre = %(nombre)s, descripcion = %(descripcion)s, precio = %(precio)s, 
            stock = %(stock)s, id_categoria = %(id_categoria)s 
        WHERE id_producto = %(id_producto)s;
        """
        return connectToMySQL('ecommerce_db').query_db(query, data)

    @classmethod
    def delete(cls, id_producto):
        query = "DELETE FROM PRODUCTO WHERE id_producto = %(id)s;"
        data = {'id': id_producto}
        return connectToMySQL('ecommerce_db').query_db(query, data)