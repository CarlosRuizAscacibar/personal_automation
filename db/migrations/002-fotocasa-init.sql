CREATE TABLE IF NOT EXISTS fotocasa (
    id VARCHAR(36) PRIMARY KEY,
    url VARCHAR(500),
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP NULL,
    label_slider VARCHAR(500) NULL,
    price VARCHAR(500) NULL,
    direccion VARCHAR(500) NULL,
    titulo VARCHAR(500) NULL,
    descripcion VARCHAR(500) NULL,
    habitaciones VARCHAR(500) NULL,
    banios VARCHAR(500) NULL,
    m2 VARCHAR(500) NULL,
    eur_m2 DOUBLE NULL,
    aditional_info VARCHAR(5000) NULL
);


