CREATE DATABASE IF NOT EXISTS gamestore_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE gamestore_db;

CREATE TABLE IF NOT EXISTS empleados (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL,
    apellido VARCHAR(80) NOT NULL,
    usuario VARCHAR(40) NOT NULL UNIQUE,
    contrasena VARCHAR(100) NOT NULL,
    rol ENUM('admin', 'vendedor') NOT NULL DEFAULT 'vendedor',
    activo TINYINT(1) NOT NULL DEFAULT 1,
    creado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL,
    apellido VARCHAR(80) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    creado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS videojuegos (
    id_juego INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(120) NOT NULL,
    genero VARCHAR(60),
    plataforma VARCHAR(60),
    precio DECIMAL(8,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    activo TINYINT(1) NOT NULL DEFAULT 1,
    creado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS ventas (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_empleado INT NOT NULL,
    total DECIMAL(10,2) NOT NULL DEFAULT 0,
    fecha_venta DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_venta_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente),

    CONSTRAINT fk_venta_empleado
        FOREIGN KEY (id_empleado)
        REFERENCES empleados(id_empleado)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS detalle_ventas (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_venta INT NOT NULL,
    id_juego INT NOT NULL,
    cantidad INT NOT NULL DEFAULT 1,
    precio_unit DECIMAL(8,2) NOT NULL,

    CONSTRAINT fk_detalle_venta
        FOREIGN KEY (id_venta)
        REFERENCES ventas(id_venta),

    CONSTRAINT fk_detalle_juego
        FOREIGN KEY (id_juego)
        REFERENCES videojuegos(id_juego)
) ENGINE=InnoDB;

INSERT INTO empleados (
    nombre,
    apellido,
    usuario,
    contrasena,
    rol
)
VALUES
(
    'Carlos',
    'Ramírez',
    'admin',
    'admin123',
    'admin'
),
(
    'Laura',
    'Mendoza',
    'laura',
    'vend123',
    'vendedor'
),
(
    'Pedro',
    'Soto',
    'pedro',
    'vend123',
    'vendedor'
);

INSERT INTO clientes (
    nombre,
    apellido,
    email,
    telefono
)
VALUES
(
    'Ana',
    'García',
    'ana.garcia@mail.com',
    '6561110001'
),
(
    'Luis',
    'Torres',
    'luis.torres@mail.com',
    '6561110002'
),
(
    'María',
    'Pérez',
    'maria.perez@mail.com',
    '6561110003'
),
(
    'Jorge',
    'Díaz',
    'jorge.diaz@mail.com',
    '6561110004'
);

INSERT INTO videojuegos (
    titulo,
    genero,
    plataforma,
    precio,
    stock
)
VALUES
(
    'The Legend of Zelda: TOTK',
    'Aventura',
    'Nintendo Switch',
    1199.00,
    15
),
(
    'God of War Ragnarök',
    'Acción',
    'PlayStation 5',
    1099.00,
    10
),
(
    'Elden Ring',
    'RPG',
    'PC',
    899.00,
    20
),
(
    'FIFA 25',
    'Deportes',
    'Xbox Series X',
    799.00,
    8
),
(
    'Minecraft',
    'Sandbox',
    'PC',
    399.00,
    50
),
(
    'Hollow Knight',
    'Metroidvania',
    'PC',
    149.00,
    30
);

INSERT INTO ventas (
    id_cliente,
    id_empleado,
    total
)
VALUES
(
    1,
    1,
    1199.00
),
(
    2,
    2,
    899.00
),
(
    3,
    1,
    1898.00
);

INSERT INTO detalle_ventas (
    id_venta,
    id_juego,
    cantidad,
    precio_unit
)
VALUES
(
    1,
    1,
    1,
    1199.00
),
(
    2,
    3,
    1,
    899.00
),
(
    3,
    2,
    1,
    1099.00
),
(
    3,
    4,
    1,
    799.00
);