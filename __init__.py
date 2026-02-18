from flask import Flask, render_template, request, redirect, url_for, session, g
import os
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# ---------- Configuration base de données ----------
BASE_DIR = os.path.dirname(__file__)
DATABASE = os.path.join(BASE_DIR, 'data', 'tasks.sqlite')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        # s'assurer que le dossier data existe
        os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
# ---------------------------------------------------

def est_authentifie():
    return session.get('authentifie')

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/lecture')
def lecture():
    if not est_authentifie():
        return redirect(url_for('authentification'))
    return "<h2>Bravo, vous êtes authentifié</h2>"

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'password':
            session['authentifie'] = True
            return redirect(url_for('lecture'))
        else:
            return render_template('formulaire_authentification.html', error=True)
    return render_template('formulaire_authentification.html', error=False)

# --------- Routes clients existantes (utilisent database.db) ----------
# Si tu veux garder la table clients dans database.db, laisse ces routes.
# Sinon migre-les vers la nouvelle DB en adaptant le schéma.
@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/consultation/')
def ReadBDD():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/enregistrer_client', methods=['GET'])
def formulaire_client():
    return render_template('formulaire.html')

@app.route('/enregistrer_client', methods=['POST'])
def enregistrer_client():
    nom = request.form['nom']
    prenom = request.form['prenom']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)',
                   (1002938, nom, prenom, "ICI"))
    conn.commit()
    conn.close()
    return redirect('/consultation/')

@app.route("/fiche_nom/<nom>")
def fiche_nom(nom):
    if not session.get("user"):
        return redirect("/auth_user")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients WHERE nom = ?", (nom,))
    data = cur.fetchall()
    conn.close()
    return render_template("fiche_nom.html", data=data)

@app.route("/auth_user", methods=["GET", "POST"])
def auth_user():
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]

        if login == "user" and password == "12345":
            session["user"] = True
            return redirect("/fiche_nom/test")
        else:
            return "Mauvais identifiants"

    return render_template("auth_user.html")

# ---------- Nouvelles routes pour les tâches (TP) ----------
@app.route('/taches')
def lister_taches():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, title, description, due_date, is_done, created_at FROM tasks ORDER BY created_at DESC")
    tasks = cur.fetchall()
    return render_template('taches_liste.html', tasks=tasks)

@app.route('/taches/ajouter', methods=['GET', 'POST'])
def ajouter_tache():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        due_date = request.form.get('due_date')  # optionnel
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks (title, description, due_date) VALUES (?, ?, ?)",
                    (title, description, due_date))
        conn.commit()
        return redirect(url_for('lister_taches'))
    return render_template('taches_ajouter.html')
# -------------------------------------------------------------

# Ne pas exécuter app.run en production WSGI
if __name__ == "__main__":
    app.run(debug=True)
