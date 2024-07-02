-- Drop existing tables to prevent conflicts during creation
DROP TABLE IF EXISTS punto_venta;
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS clientes;

-- Create the 'clientes' table
CREATE TABLE clientes (
    Cliente VARCHAR(10) PRIMARY KEY,       -- Customer ID
    Facturación_Total DECIMAL(15, 2),      -- Total billing
    Canal_de_Ventas VARCHAR(10),           -- Sales channel
    Numero_Puntos_de_Venta INT,            -- Number of points of sale
    Región VARCHAR(20),                    -- Region
    Segmento VARCHAR(10),                  -- Segment
    Antigüedad INT                         -- Age or tenure
);

-- Create the 'pos' (points of sale) table
CREATE TABLE punto_venta (
    Cliente VARCHAR(10),                  -- Customer identifier
    Punto_de_Venta INT,                   -- Point of sale identifier, primary key
    Población_500m INT,                   -- Population within 500m
    Población_2km INT,                    -- Population within 2km
    Puntos_de_Venta_Cercanos INT,         -- Nearby points of sale
    Aparcamiento VARCHAR(2),              -- Parking availability 'Sí' or 'No'
    Accesibilidad VARCHAR(10),            -- Accessibility level 'Baja', 'Media', 'Alta'
    Horas_Operación VARCHAR(10),          -- Operating hours '8-21', etc.
    Tipo_Zona VARCHAR(15),                -- Type of area 'Residencial', 'Comercial'
    CONSTRAINT fk_cliente FOREIGN KEY (Cliente) REFERENCES clientes (Cliente)
);


-- Create the 'products' table
CREATE TABLE productos (
    Id_Producto VARCHAR(10) PRIMARY KEY,   -- Product ID
    Familia VARCHAR(20),                   -- Product family
    Subfamilia VARCHAR(20),                -- Product subfamily
    Formato VARCHAR(20),                   -- Product format
    Precio DECIMAL(10, 2),                 -- Price
    Margen DECIMAL(4, 2),                  -- Margin
    Cliente_Objetivo VARCHAR(50),          -- Target customer
    Color VARCHAR(20),                     -- Product color
    Material VARCHAR(20),                  -- Product material
    Peso FLOAT,                            -- Product weight
    Tamaño VARCHAR(20),                    -- Product size
    Marca VARCHAR(20),                     -- Brand
    País_Origen VARCHAR(50),               -- Country of origin
    Ventas_Base INT                        -- Base sales
);
