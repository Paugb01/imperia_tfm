#!/bin/bash

# Using psql to check the readiness of PostgreSQL server instead of pg_isready
until psql -U postgres -d postgres -c '\l' > /dev/null 2>&1; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

# Execute the initial SQL file to create tables
echo "Executing SQL script to create tables..."
psql -U postgres -d postgres -f /docker-entrypoint-initdb.d/imperia_db.sql

# Import data from CSV files into respective tables
echo "Importing data from CSV files..."

# Import data into 'puntos_de_venta' table
psql -U postgres -d postgres -c "\COPY punto_venta FROM '/docker-entrypoint-initdb.d/caracteristicas_puntos_de_venta.csv' WITH CSV HEADER;"

# Import data into 'productos' table
psql -U postgres -d postgres -c "\COPY productos FROM '/docker-entrypoint-initdb.d/caracteristicas_productos.csv' WITH CSV HEADER;"

# Import data into 'clientes' table
psql -U postgres -d postgres -c "\COPY clientes FROM '/docker-entrypoint-initdb.d/caracteristicas_clientes.csv' WITH CSV HEADER;"

echo "Data import complete."
