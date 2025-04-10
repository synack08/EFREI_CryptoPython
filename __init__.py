from cryptography.fernet import Fernet, InvalidToken
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Page d'accueil
@app.route('/')
def hello_world():
    return render_template('hello.html')# Génère une clé à chaque démarrage du serveur (pour test rapide)
key = Fernet.generate_key()
f = Fernet(key)

# Route de chiffrement simple avec la clé générée ci-dessus
@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    valeur_bytes = valeur.encode()
    token = f.encrypt(valeur_bytes)
    return f"Valeur encryptée : {token.decode()}<br>Clé utilisée : {key.decode()}"

# Route de décryptage avec clé fournie par l'utilisateur (POST)
@app.route('/decrypt/', methods=['POST'])
def decrypt_api():
    data = request.get_json()

    # Vérifie la présence des paramètres
    if not data or 'encrypted_text' not in data or 'key' not in data:
        return jsonify({
            "error": "Champs requis : 'encrypted_text' et 'key'"
        }), 400

    encrypted_text = data['encrypted_text']
    user_key = data['key']

    try:
        user_fernet = Fernet(user_key.encode())
        decrypted = user_fernet.decrypt(encrypted_text.encode()).decode()
        return jsonify({"decrypted_text": decrypted})
    except InvalidToken:
        return jsonify({"error": "Clé invalide ou texte chiffré incorrect."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
