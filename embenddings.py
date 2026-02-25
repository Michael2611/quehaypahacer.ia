from sentence_transformers import SentenceTransformer, util
import torch

lugares = [
    {
        "nombre": "Sendero Natural Tauramena",
        "municipio": "Tauramena",
        "descripcion": "Lugar tranquilo rodeado de naturaleza ideal para descansar y caminar."
    },
    {
        "nombre": "Rafting Río Upía",
        "municipio": "Tauramena",
        "descripcion": "Experiencia de aventura extrema en el río con mucha adrenalina."
    },
    {
        "nombre": "Parque La Iguana",
        "municipio": "Yopal",
        "descripcion": "Espacio natural perfecto para relajarse en familia."
    }
]

municipios = ["tauramena", "yopal", "trinidad"]

# Cargar modelo semántico ligero
model = SentenceTransformer('all-MiniLM-L6-v2')

# Crear embeddings solo de los lugares flitrados
descripciones = [lugar["descripcion"] for lugar in lugares]
embeddings_lugares = model.encode(descripciones, convert_to_tensor=True)

print("Embedding generados")

def detectar_municipio(texto):
    text = texto.lower()
    for municipio in municipios:
        if municipio in texto:
            return municipio
    return None

def recomendar(texto_usuario):
    texto = texto_usuario.lower()
    municipio_detectado = detectar_municipio(texto)

    #Filtrar municipio
    if municipio_detectado:
        indices_filtrados  = [
            i for i, lugar in enumerate(lugares)
            if lugar["municipio"].lower() == municipio_detectado
        ]
    else:
        indices_filtrados = list(range(len(lugares)))

    if not indices_filtrados:
        return []

    # Embedding del usuario
    embedding_usuario = model.encode(texto_usuario, convert_to_tensor=True)

    # Comparar con embendding filtrados
    embeddings_filtrados = embeddings_lugares[indices_filtrados]

    # Calcular similitud coseno
    similitudes = util.cos_sim(embedding_usuario, embeddings_filtrados)[0]

    resultados = []

    for i, score in enumerate(similitudes):
        lugar_real = lugares[indices_filtrados[i]]
        resultados.append((float(score), lugar_real))

    # Ordenar por mayor similitud
    resultados.sort(key=lambda x: x[0], reverse=True)

    return resultados[:3]  # Top 3

print(recomendar("Estoy muy estresado y quiero algo natural en Tauramena"))