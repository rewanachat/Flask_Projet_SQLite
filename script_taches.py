import sqlite3
import os
import sys

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'tasks.sqlite')
SCHEMA_FILE = os.path.join(BASE_DIR, 'schema_taches.sql')

def ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)

def init_db():
    if not os.path.exists(SCHEMA_FILE):
        print("Erreur: schema_taches.sql introuvable dans", BASE_DIR)
        sys.exit(1)
    with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
        sql = f.read()
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(sql)
        conn.commit()
        print("Base initialisée:", DB_PATH)
    except Exception as e:
        print("Erreur lors de l'initialisation:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    ensure_dirs()
    init_db()
