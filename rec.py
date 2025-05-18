from flask import Flask, request, jsonify
import json
import re
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ----------- 1. Charger les données et prétraitement -----------
with open("parsed.jl", "r", encoding="utf-8") as f:
    data = [json.loads(line) for line in f]

texts = [d["content"] for d in data]
addresses = [d["address"] for d in data]
ratings = [int(d["rating"]) for d in data]
hotels = [d["hotel"] for d in data]

# ----------- 2. TF-IDF Vectorization -----------
vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(texts)

# ----------- 3. KNN Model -----------
knn = NearestNeighbors(n_neighbors=10, metric="cosine")
knn.fit(X)

# ----------- 4. Extraction de localisation -----------
def extract_location(message, addresses):
    locations = set()
    for address in addresses:
        words = re.split(r"[,_\s]+", address.lower())
        for word in words:
            if word in message.lower():
                locations.add(word)
    return list(locations)

# ----------- 5. Réponses types pour un chatbot -----------
greetings = ["👋 Bonjour ! Comment puis-je vous aider ?", "Salut 👋", "Coucou ! 😊", "Hello, que puis-je faire pour vous aujourd’hui ?", "Salut ! C’est un bon jour pour voyager ! ✈️"]
thanks = ["Avec plaisir ! 😊", "De rien !", "N’hésitez pas si vous avez d'autres questions.", "Je suis ravi d’avoir pu vous aider."]
farewells = ["À bientôt ! 👋", "Bonne journée ! 🌞", "Prenez soin de vous, à la prochaine !", "Au revoir et bon voyage ! 🧳"]
infos = ["Je suis un assistant qui recommande des hôtels selon votre message 📍", "Envoyez-moi votre destination ou vos préférences, et je vous propose des hôtels 🏨", "Je peux vous suggérer des hôtels selon l’endroit et ce que vous cherchez 🗺️"]

# ----------- 6. Endpoint Flask pour recommandation -----------
@app.route("/recommend", methods=["POST"])
def recommend_hotels():
    data = request.get_json()

    # Vérification de la présence et du type du champ "message"
    message = data.get("message") if data else ""
    if not isinstance(message, str):
        return jsonify({"message": "❗Le champ 'message' doit être une chaîne de caractères."}), 400

    user_input = message.strip().lower()

    if not user_input:
        return jsonify({"message": "❗Veuillez fournir un message pour obtenir des recommandations."}), 400

    # ----- Réponses aléatoires selon intentions -----
    if any(word in user_input for word in ["bonjour", "salut", "coucou", "hello"]):
        return jsonify({"message": random.choice(greetings)})

    if any(word in user_input for word in ["merci", "thanks","je t'aime", "thx"]):
        return jsonify({"message": random.choice(thanks)})

    if any(word in user_input for word in ["au revoir", "bye", "à bientôt"]):
        return jsonify({"message": random.choice(farewells)})

    if any(word in user_input for word in ["c'est quoi", "qui es-tu", "service", "tu fais quoi"]):
        return jsonify({"message": random.choice(infos)})

    # ----- Recherche d'hôtels sinon -----
    localisation_extraite = extract_location(user_input, addresses)
    X_msg = vectorizer.transform([user_input])
    distances, indices = knn.kneighbors(X_msg)

    results = []
    for i in indices[0]:
        if any(loc in addresses[i].lower() for loc in localisation_extraite):
            results.append({
                "hotel": hotels[i].replace("_", " "),
                "address": addresses[i].replace("_", " "),
                "rating": ratings[i],
                "score": round(1 - distances[0][list(indices[0]).index(i)], 3),
                "description": texts[i][:300] + "..."
            })

    results = sorted(results, key=lambda x: (-x["rating"], -x["score"]))
    top3 = results[:3]

    if top3:
        intro_choices = [
            "📌 Voici quelques hôtels que je vous recommande :",
            "🏨 J’ai trouvé ceci pour vous :",
            "🧭 Hôtels recommandés pour votre recherche :"
        ]
        footer_choices = [
            "Souhaitez-vous autre chose ? 😊",
            "Je peux chercher plus si vous voulez !",
            "Une autre destination en tête ? 🗺️"
        ]
        return jsonify({
            "message": random.choice(intro_choices),
            "recommandations": top3,
            "footer": random.choice(footer_choices)
        })
    else:
        return jsonify({
            "message": "❌ Désolé, je n’ai trouvé aucun hôtel correspondant à votre recherche."
        })

# ----------- Lancer le serveur Flask -----------
if __name__ == "__main__":
    app.run(port=3300, debug=True)
