import pandas as pd
from pymongo import MongoClient
from datetime import datetime

# 1. Leer el CSV
df = pd.read_csv("CSV/Covid_Analisis.csv")

# 2. Asegurar que las fechas estén en formato datetime
df["Fecha_Creación"] = pd.to_datetime(df["Fecha_Creación"], errors="coerce")

# 3. Conectarse a MongoDB local
client = MongoClient("mongodb://localhost:27017/")
db = client["base_unificada"]
collection = db["analisis_covid"]

# 4. Limpiar colección anterior (opcional)
collection.drop()

# 5. Convertir DataFrame a diccionarios y limpiar NaN
records = df.to_dict(orient="records")

# Reemplazar NaN por None y asegurar tipos
for record in records:
    for key, value in record.items():
        if pd.isna(value):
            record[key] = None
    if isinstance(record.get("Fecha_Creación"), pd.Timestamp):
        record["Fecha_Creación"] = record["Fecha_Creación"].to_pydatetime()

# 6. Insertar en MongoDB
collection.insert_many(records)

print("✅ Datos del CSV migrados correctamente a MongoDB (colección 'analisis_covid').")
