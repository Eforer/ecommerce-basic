from mysqlconnection import connectToMySQL

class Categoria:
    def __init__(self, data):
        self.id_categoria = data['id_categoria']
        self.nombre = data['nombre']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM CATEGORIA;"
        resultados = connectToMySQL('ecommerce_db').query_db(query)
        categorias = []
        for categoria in resultados:
            categorias.append(cls(categoria))
        return categorias

    @classmethod
    def get_by_id(cls, id_categoria):
        query = "SELECT * FROM CATEGORIA WHERE id_categoria = %(id)s;"
        data = {'id': id_categoria}
        resultado = connectToMySQL('ecommerce_db').query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None

    @classmethod
    def save(cls, data):
        query = "INSERT INTO CATEGORIA (nombre) VALUES (%(nombre)s);"
        return connectToMySQL('ecommerce_db').query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE CATEGORIA SET nombre = %(nombre)s WHERE id_categoria = %(id_categoria)s;"
        return connectToMySQL('ecommerce_db').query_db(query, data)

    @classmethod
    def delete(cls, id_categoria):
        query = "DELETE FROM CATEGORIA WHERE id_categoria = %(id)s;"
        data = {'id': id_categoria}
        return connectToMySQL('ecommerce_db').query_db(query, data)