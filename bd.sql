-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS ecommerce_db;
USE ecommerce_db;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS USUARIO (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    direccion TEXT NOT NULL
);

-- Tabla de categorías
CREATE TABLE IF NOT EXISTS CATEGORIA (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- Tabla de productos
CREATE TABLE IF NOT EXISTS PRODUCTO (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    descripcion TEXT(100) NOT NULL,
    stock INT NOT NULL,
    id_categoria INT,
    FOREIGN KEY (id_categoria) REFERENCES CATEGORIA(id_categoria)
);

-- Tabla de métodos de pago
CREATE TABLE IF NOT EXISTS METODO_PAGO (
    id_metodo_pago INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,
    proveedor VARCHAR(100),
    numero_cuenta VARCHAR(50),
    fecha_expiracion DATE,
    id_usuario INT,
    FOREIGN KEY (id_usuario) REFERENCES USUARIO(id_usuario)
);

-- Tabla de órdenes
CREATE TABLE IF NOT EXISTS ORDEN (
    id_orden INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    estado VARCHAR(50) NOT NULL,
    id_usuario INT,
    id_metodo_pago INT,
    FOREIGN KEY (id_usuario) REFERENCES USUARIO(id_usuario),
    FOREIGN KEY (id_metodo_pago) REFERENCES METODO_PAGO(id_metodo_pago)
);

-- Tabla de detalles de orden
CREATE TABLE IF NOT EXISTS DETALLE_ORDEN (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    cantidad INT NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    id_orden INT,
    id_producto INT,
    FOREIGN KEY (id_orden) REFERENCES ORDEN(id_orden),
    FOREIGN KEY (id_producto) REFERENCES PRODUCTO(id_producto)
);

-- Tabla de entrega
CREATE TABLE IF NOT EXISTS ENTREGA (
    id_entrega INT AUTO_INCREMENT PRIMARY KEY,
    fecha_envio DATE,
    fecha_entrega_estimada DATE,
    fecha_entrega_real DATE,
    estado_entrega VARCHAR(50) NOT NULL,
    direccion_entrega TEXT NOT NULL,
    id_orden INT UNIQUE,
    FOREIGN KEY (id_orden) REFERENCES ORDEN(id_orden)
);

-- Índices para mejorar el rendimiento
CREATE INDEX idx_usuario_email ON USUARIO(email);
CREATE INDEX idx_producto_nombre ON PRODUCTO(nombre);
CREATE INDEX idx_orden_fecha ON ORDEN(fecha);
CREATE INDEX idx_orden_usuario ON ORDEN(id_usuario);
CREATE INDEX idx_detalle_orden ON DETALLE_ORDEN(id_orden, id_producto);

-- Insertar algunas categorías de ejemplo
INSERT INTO CATEGORIA (nombre) VALUES 
('Electrónicos'),
('Ropa'),
('Hogar'),
('Libros');

INSERT INTO PRODUCTO (nombre, precio, descripcion, stock, id_categoria) VALUES
('Smartphone XYZ', 599.99, 'Teléfono inteligente de última generación con cámara de alta resolución', 50, 1),
('Laptop ABC', 999.99, 'Laptop potente para trabajo y entretenimiento', 30, 1),
('Camiseta Cool', 29.99, 'Camiseta de algodón con diseño moderno', 100, 2),
('Pantalón Casual', 49.99, 'Pantalón cómodo para uso diario', 75, 2),
('Lámpara LED', 39.99, 'Lámpara de escritorio con luz LED ajustable', 60, 3),
('Set de Ollas', 89.99, 'Juego de ollas de acero inoxidable de alta calidad', 40, 3),
('Libro de Programación', 59.99, 'Guía completa para aprender programación desde cero', 80, 4),
('Novela Bestseller', 24.99, 'Emocionante novela de misterio y suspense', 120, 4);
