import pandas as pd
import mysql.connector

# 1. Leer el archivo CSV
df = pd.read_csv("CSV\Covid_Analisis.csv")

# 2. Convertir fechas al formato correcto
df["Fecha_Creación"] = pd.to_datetime(df["Fecha_Creación"], errors="coerce").dt.date

# 3. Conectar a MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="noticias_mundiales"
)
cursor = conn.cursor()

# 4. Crear la tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS analisis_covid (
    usuario VARCHAR(255),
    fecha_creacion DATE,
    comentario TEXT,
    polaridad FLOAT,
    sentimiento VARCHAR(50)
);
""")
conn.commit()

# 5. Insertar los datos
sql_insert = """
INSERT INTO analisis_covid (usuario, fecha_creacion, comentario, polaridad, sentimiento)
VALUES (%s, %s, %s, %s, %s)
"""

for _, row in df.iterrows():
    valores = (
        row["Usuario"],
        row["Fecha_Creación"],
        row["Comentario"],
        float(row["Polaridad"]) if pd.notnull(row["Polaridad"]) else None,
        row["Sentimiento"]
    )
    cursor.execute(sql_insert, valores)

# 6. Confirmar e informar
conn.commit()
cursor.close()
conn.close()
print("✅ CSV 'Analisis_Covid.csv' migrado correctamente a la tabla 'analisis_covid' en MySQL.")
