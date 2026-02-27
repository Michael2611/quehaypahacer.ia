# recomendacion.py
from database import get_connection
from sentence_transformers import SentenceTransformer, util
import torch

def obtener_lugares_desde_bd():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # Diccionarios en lugar de tuplas
    query = """
        SELECT 
            l.id,
            l.nombre,
            l.descripcion,
            l.popularidad,
            l.latitud,
            l.longitud,
            l.estado,
            m.nombre as municipio,
            GROUP_CONCAT(c.nombre) as categorias
        FROM lugares l
        JOIN municipios m ON l.municipio_id = m.id
        LEFT JOIN categoria_lugar lc ON l.id = lc.lugar_id
        LEFT JOIN categorias c ON lc.categoria_id = c.id
        WHERE l.estado = TRUE
        GROUP BY l.id, m.nombre;
    """
    cursor.execute(query)
    lugares = cursor.fetchall()

    # Convertir categorías de string a lista
    for l in lugares:
        if l["categorias"]:
            l["categorias"] = l["categorias"].split(",")
        else:
            l["categorias"] = []

    cursor.close()
    conn.close()
    return lugares


class MotorRecomendacion:
    def __init__(self, lugares):
        self.lugares = lugares
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.descripciones = [l["descripcion"] for l in lugares]
        self.embeddings_lugares = self.model.encode(
            self.descripciones,
            convert_to_tensor=True
        )

        self.emociones_base = {
            "relajacion": "quiero descansar y desconectarme en un lugar tranquilo",
            "aventura": "quiero vivir algo extremo con adrenalina",
            "familia": "quiero compartir tiempo en familia",
            "exploracion": "quiero caminar y explorar paisajes naturales"
        }
        self.embeddings_emociones = self.model.encode(
            list(self.emociones_base.values()),
            convert_to_tensor=True
        )

        self.categorias_base = {
            "naturaleza": "lugares rodeados de naturaleza y paisajes verdes",
            "aventura": "actividades extremas y llenas de adrenalina",
            "familia": "planes para compartir en familia",
            "senderismo": "caminatas ecológicas y exploración de senderos",
            "tranquilo": "lugares calmados ideales para descansar",
            "rio": "actividades relacionadas con ríos o agua"
        }
        self.embeddings_categorias = self.model.encode(
            list(self.categorias_base.values()),
            convert_to_tensor=True
        )

        print("Embeddings cargados en memoria")

    def detectar_municipio(self, texto):
        texto = texto.lower()
        for lugar in self.lugares:
            if lugar["municipio"].lower() in texto:
                return lugar["municipio"].lower()
        return None

    def detectar_emocion(self, texto_usuario):
        embedding_usuario = self.model.encode(texto_usuario, convert_to_tensor=True)
        similitudes = util.cos_sim(embedding_usuario, self.embeddings_emociones)[0]
        indice = torch.argmax(similitudes).item()
        emocion = list(self.emociones_base.keys())[indice]
        score = float(similitudes[indice])
        return emocion, score

    def detectar_categorias_usuario(self, texto_usuario):
        embedding_usuario = self.model.encode(texto_usuario, convert_to_tensor=True)
        similitudes = util.cos_sim(embedding_usuario, self.embeddings_categorias)[0]

        categorias_detectadas = []
        for i, score in enumerate(similitudes):
            if score > 0.35:  # umbral ajustable
                categorias_detectadas.append(list(self.categorias_base.keys())[i])
        return categorias_detectadas

    def recomendar(self, texto_usuario, top_k=3):
        municipio_detectado = self.detectar_municipio(texto_usuario)

        if municipio_detectado:
            indices = [i for i, l in enumerate(self.lugares) if l["municipio"].lower() == municipio_detectado]
        else:
            indices = list(range(len(self.lugares)))

        if not indices:
            return []

        embedding_usuario = self.model.encode(texto_usuario, convert_to_tensor=True)
        embeddings_filtrados = self.embeddings_lugares[indices]
        similitudes = util.cos_sim(embedding_usuario, embeddings_filtrados)[0]

        emocion_detectada, score_emocion_usuario = self.detectar_emocion(texto_usuario)
        categorias_usuario = self.detectar_categorias_usuario(texto_usuario)

        resultados = []
        for i, score in enumerate(similitudes):
            lugar = self.lugares[indices[i]]
            score_semantico = float(score)
            score_emocion = score_emocion_usuario if emocion_detectada in lugar["categorias"] else 0
            coincidencias = len(set(categorias_usuario) & set(lugar["categorias"]))
            score_categoria = coincidencias * 0.05
            score_popularidad = lugar["popularidad"]

            score_final = 0.7 * score_semantico + 0.2 * score_emocion + 0.1 * score_popularidad + score_categoria
            resultados.append({"lugar": lugar, "score": round(score_final, 3)})

        resultados.sort(key=lambda x: x["score"], reverse=True)
        return resultados[:top_k]