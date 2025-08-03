import json
from pymongo import MongoClient

# Conectarse a MongoDB local
client = MongoClient("mongodb://localhost:27017/")

# Crear base de datos y colección
db = client["base_unificada"]
collection = db["noticias"]

# Limpiar colección si ya existía (opcional)
collection.drop()

# Leer e insertar documentos
with open("Noticias_Mundiales.json", "r", encoding="utf-8") as f:
    batch = []
    batch_size = 500  # Ajusta según necesidad

    for i, line in enumerate(f):
        try:
            data = json.loads(line)
            # Puedes validar o transformar el campo "date" si lo necesitas
            batch.append(data)

            if len(batch) >= batch_size:
                collection.insert_many(batch)
                batch = []

        except Exception as e:
            print(f"❌ Error en línea {i}: {e}")

    if batch:
        collection.insert_many(batch)

print("✅ Datos migrados correctamente a MongoDB.")
