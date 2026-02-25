from sentence_transformers import SentenceTransformer, util
import torch

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

        print("Embeddings cargados en memoria 🚀")

    def detectar_municipio(self, texto):
        texto = texto.lower()
        for lugar in self.lugares:
            if lugar["municipio"].lower() in texto:
                return lugar["municipio"].lower()
        return None

    def detectar_emocion(self, texto_usuario):

        embedding_usuario = self.model.encode(
            texto_usuario,
            convert_to_tensor=True
        )

        similitudes = util.cos_sim(
            embedding_usuario,
            self.embeddings_emociones
        )[0]

        indice = torch.argmax(similitudes).item()
        emocion = list(self.emociones_base.keys())[indice]
        score = float(similitudes[indice])

        return emocion, score

    def detectar_categorias_usuario(self, texto_usuario):

        embedding_usuario = self.model.encode(
            texto_usuario,
            convert_to_tensor=True
        )

        similitudes = util.cos_sim(
            embedding_usuario,
            self.embeddings_categorias
        )[0]

        categorias_detectadas = []

        for i, score in enumerate(similitudes):
            if score > 0.35:  # umbral ajustable
                categoria = list(self.categorias_base.keys())[i]
                categorias_detectadas.append(categoria)

        return categorias_detectadas

    def recomendar(self, texto_usuario, top_k=3):

        municipio_detectado = self.detectar_municipio(texto_usuario)

        # Filtrar por municipio
        if municipio_detectado:
            indices = [
                i for i, l in enumerate(self.lugares)
                if l["municipio"].lower() == municipio_detectado
            ]
        else:
            indices = list(range(len(self.lugares)))

        if not indices:
            return []

        embedding_usuario = self.model.encode(
            texto_usuario,
            convert_to_tensor=True
        )

        embeddings_filtrados = self.embeddings_lugares[indices]

        similitudes = util.cos_sim(
            embedding_usuario,
            embeddings_filtrados
        )[0]

        emocion_detectada, score_emocion_usuario = self.detectar_emocion(texto_usuario)
        categorias_usuario = self.detectar_categorias_usuario(texto_usuario)

        resultados = []

        for i, score in enumerate(similitudes):
            lugar = self.lugares[indices[i]]

            # 70% similitud semántica
            score_semantico = float(score)

            # 20% emoción
            score_emocion = 0
            if emocion_detectada in lugar["categorias"]:
                score_emocion = score_emocion_usuario

            # BONUS por categorías detectadas
            coincidencias = len(
                set(categorias_usuario) & set(lugar["categorias"])
            )
            score_categoria = coincidencias * 0.05  # pequeño boost

            # 10% popularidad
            score_popularidad = lugar["popularidad"]

            score_final = (
                0.7 * score_semantico +
                0.2 * score_emocion +
                0.1 * score_popularidad +
                score_categoria
            )

            resultados.append((score_final, lugar))

        resultados.sort(key=lambda x: x[0], reverse=True)

        return resultados[:top_k]

lugares = [ 
        { 
            "nombre": "Sendero Natural Tauramena", 
            "municipio": "Tauramena", 
            "descripcion": "Lugar tranquilo rodeado de naturaleza ideal para descansar y caminar.", 
            "categorias": ["naturaleza", "tranquilo", "senderismo"], 
            "popularidad": 0.8
        }, 
        { 
            "nombre": "Rafting Río Upía", 
            "municipio": "Tauramena", 
            "descripcion": "Experiencia de aventura extrema en el río con mucha adrenalina.", 
            "categorias": ["aventura", "rio"], 
            "popularidad": 0.9 
        }, 
        { 
            "nombre": "Parque La Iguana", 
            "municipio": "Yopal", 
            "descripcion": "Espacio natural perfecto para relajarse en familia.", 
            "categorias": ["naturaleza", "familia"], 
            "popularidad": 0.7 
        }, 
        {
            "nombre": "El Encanto de Guanapalo Reserva Natural", 
            "municipio": "San Luis de Palenque", 
            "descripcion": "Reserva natural llanera enfocada en turismo de naturaleza y tradiciones culturales.", 
            "categorias": ["naturaleza", "tradiciones"], 
            "popularidad": 0.7 
        }, 
        { 
            "nombre": "Parque Temático Historias de Piedra", 
            "municipio": "Yopal", 
            "descripcion": "Lugar rodeado de naturaleza con senderos y esculturas talladas en piedra.", 
            "categorias": ["familia", "senderismo", "naturaleza"], 
            "popularidad": 0.8 
        },
        {
            "nombre": "Centro turístico Valle Verde",
            "municipio": "Aguazul",
            "descripcion": "Lugar apto para que disfrutes de un dia de relajación y descanso, dispone de piscina para estar con tu familia y/o amigos",
            "categorias": ["familia", "piscina", "relajación"],
            "popularidad": 0.80
        },
        {
            "nombre": "Vega Caribeña",
            "municipio": "Tauramena",
            "descripcion": "Un lugar donde podras encontrar comida, piscina, diversión y un lugar para estar en familia y rodeado de naturaleza verde",
            "categorias": ["familia", "piscina", "comida", "naturaleza"],
            "popularidad": 0.85
        }
    ]

if __name__ == "__main__":

    motor = MotorRecomendacion(lugares)

    print("\n=== Sistema de Recomendación Turística Casanare ===")
    print("Escribe tu plan ideal o escribe 'salir' para terminar.\n")

    while True:

        texto_usuario = input("¿Qué te gustaría hacer? -> ")

        if texto_usuario.lower() == "salir":
            print("Gracias por usar el sistema")
            break

        resultados = motor.recomendar(texto_usuario)

        if not resultados:
            print("No encontré recomendaciones para tu búsqueda.\n")
            continue

        print("\nRecomendaciones:\n")

        for score, lugar in resultados:
            print(f"   {lugar['nombre']}")
            print(f"   Municipio: {lugar['municipio']}")
            print(f"   Categorías: {', '.join(lugar['categorias'])}")
            print(f"   Popularidad: {lugar['popularidad']}")
            print(f"   Score: {round(score, 3)}\n")

        print("-" * 50)