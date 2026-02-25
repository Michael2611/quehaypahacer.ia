import unicodedata

lugares = [
    {
        "nombre": "Sendero Natural Tauramena",
        "municipio": "Tauramena",
        "tags": ["naturaleza", "tranquilo", "senderismo"]
    },
    {
        "nombre": "Rafting Río Upía",
        "municipio": "Tauramena",
        "tags": ["aventura", "rio", "extremo"]
    },
    {
        "nombre": "Parque La Iguana",
        "municipio": "Yopal",
        "tags": ["naturaleza", "familia", "tranquilo"]
    },
]

intenciones = {
    "naturaleza": ["naturaleza", "natural", "bosque", "verde", "ecologico"],
    "tranquilo": ["tranquilo", "relax", "relajar", "descansar", "paz", "silencio"],
    "aventura": ["aventura", "adrenalina", "extremo", "emocion"],
    "rio": ["rio", "agua", "cascada", "quebrada"]
}

emociones = {
    "estresado": ["estresado", "cansado", "agotado", "abrumado"],
    "feliz": ["feliz", "emocionado", "contento"],
    "aburrido": ["aburrido", "sin planes", "sin nada que hacer"],
    "aventurero": ["adrenalina", "emocion fuerte", "riesgo"]
}

emocion_a_categoria = {
    "estresado": ["tranquilo", "naturaleza"],
    "feliz": ["aventura", "rio"],
    "aburrido": ["aventura"],
    "aventurero": ["aventura", "extremo"]
}

def limpiar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto)
    texto = texto.encode('ascii', 'ignore').decode('utf-8')
    return texto

municipios = ["tauramena","trinidad","yopal"]

def detectar_municipio(texto):
    for municipio in municipios:
        if municipio in texto:
            return municipio
    return None

def detectar_intenciones(texto):
    categorias_detectadas = set()

    for categoria, palabras in intenciones.items():
        for palabra in palabras:
            if palabra in texto:
                categorias_detectadas.add(categoria)

    return categorias_detectadas

def detectar_emocion(texto):
    for emocion, palabras in emociones.items():
        for palabra in palabras:
            if palabra in texto:
                return emocion
    return None

def recomendar(texto_usuario):
    texto = limpiar_texto(texto_usuario)

    municipio_detectado = detectar_municipio(texto)
    categorias_usuario = detectar_intenciones(texto)
    emocion_detectada = detectar_emocion(texto)

    recomendaciones = []

    for lugar in lugares:

        if municipio_detectado:
            if limpiar_texto(lugar["municipio"]) != municipio_detectado:
                continue

        coincidencias = 0

        # Coincidencia por intención
        for tag in lugar["tags"]:
            if tag in categorias_usuario:
                coincidencias += 1

        # 🔥 BONUS por emoción
        if emocion_detectada:
            categorias_emocion = emocion_a_categoria.get(emocion_detectada, [])
            for tag in lugar["tags"]:
                if tag in categorias_emocion:
                    coincidencias += 1  # suma punto extra

        if coincidencias > 0:
            recomendaciones.append((coincidencias, lugar))

    recomendaciones.sort(key=lambda x: x[0], reverse=True)

    return [lugar for _, lugar in recomendaciones]

print(recomendar("Estoy algo estresado y quiero descansar en Tauramena"))