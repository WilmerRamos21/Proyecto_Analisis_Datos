import json
import mysql.connector

# Conexión inicial sin base de datos
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234"
)
cursor = conn.cursor()

# Crear base de datos si no existe
cursor.execute("CREATE DATABASE IF NOT EXISTS noticias_mundiales;")
cursor.close()
conn.close()

# Reconectar, ahora sí usando la base creada
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="noticias_mundiales"
)
cursor = conn.cursor()

# Crear la tabla
cursor.execute("""
CREATE TABLE IF NOT EXISTS noticias (
    headline TEXT,
    category VARCHAR(255),
    short_description TEXT,
    authors TEXT,
    date DATE
);
""")

# Preparar SQL
sql_insert = """
INSERT INTO noticias (headline, category, short_description, authors, date)
VALUES (%s, %s, %s, %s, %s)
"""

# Insertar por lotes
with open("Noticias_Mundiales.json", "r", encoding="utf-8") as f:
    batch = []
    batch_size = 500  # puedes ajustar

    for i, line in enumerate(f):
        try:
            data = json.loads(line)
            values = (
                data.get("headline"),
                data.get("category"),
                data.get("short_description"),
                data.get("authors"),
                data.get("date")
            )
            batch.append(values)

            if len(batch) >= batch_size:
                cursor.executemany(sql_insert, batch)
                conn.commit()
                batch = []

        except Exception as e:
            print(f"❌ Error en línea {i}: {e}")

    if batch:
        cursor.executemany(sql_insert, batch)
        conn.commit()

cursor.close()
conn.close()
print("✅ Dataset migrado correctamente.")
