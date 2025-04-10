from cryptography.fernet import Fernet, InvalidToken
from flask import Flask, render_template

app = Flask(__name__)

# 🏠 Route d'accueil
@app.route('/')
def hello_world():
    return render_template('hello.html')

# 🔒 Route de chiffrement avec clé personnalisée
@app.route('/encrypt/<string:valeur>/<string:cle>')
def encryptage(valeur, cle):
    try:
        fernet = Fernet(cle.encode())  # Crée l'objet Fernet avec la clé fournie
        token = fernet.encrypt(valeur.encode())
        return f"🔐 Valeur chiffrée : <br><code>{token.decode()}</code>"
    except Exception as e:
        return f"❌ Erreur lors du chiffrement : {str(e)}"

# 🔓 Route de déchiffrement avec clé personnalisée
@app.route('/decrypt/<string:valeur>/<string:cle>')
def decryptage(valeur, cle):
    try:
        fernet = Fernet(cle.encode())
        texte_dechiffre = fernet.decrypt(valeur.encode()).decode()
        return f"🔓 Valeur déchiffrée : <b>{texte_dechiffre}</b>"
    except InvalidToken:
        return "❌ Clé invalide ou texte chiffré incorrect."
    except Exception as e:
        return f"❌ Erreur lors du déchiffrement : {str(e)}"

# 🚀 Lancement local
if __name__ == "__main__":
    app.run(debug=True)
