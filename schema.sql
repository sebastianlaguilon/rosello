-- Esquema base para Fumigadora Rosello
-- MySQL 8+ recomendado. Charset/Collation utf8mb4.
CREATE DATABASE IF NOT EXISTS fumigadora_rosello CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE fumigadora_rosello;

CREATE TABLE IF NOT EXISTS productores (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre     VARCHAR(120) NOT NULL,
  telefono   VARCHAR(40),
  localidad  VARCHAR(120),
  cuit       VARCHAR(20)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS campos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  productor_id INT NOT NULL,
  nombre     VARCHAR(120) NOT NULL,
  localidad  VARCHAR(120),
  CONSTRAINT fk_campos_productor FOREIGN KEY (productor_id) REFERENCES productores(id)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS lotes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  campo_id   INT NOT NULL,
  nombre     VARCHAR(120) NOT NULL,
  superficie DECIMAL(10,2),
  CONSTRAINT fk_lotes_campo FOREIGN KEY (campo_id) REFERENCES campos(id)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ordenes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  productor_id INT NOT NULL,
  lote_id      INT NOT NULL,
  fecha DATE NOT NULL,
  hectareas DECIMAL(10,2) NOT NULL,
  CONSTRAINT fk_ordenes_productor FOREIGN KEY (productor_id) REFERENCES productores(id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_ordenes_lote FOREIGN KEY (lote_id) REFERENCES lotes(id)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ordenes_productos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  orden_id INT NOT NULL,
  nombre   VARCHAR(120) NOT NULL,
  unidad   ENUM('litros','gramos') NOT NULL,
  cantidad DECIMAL(10,2) NOT NULL,
  CONSTRAINT fk_op_orden FOREIGN KEY (orden_id) REFERENCES ordenes(id)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
