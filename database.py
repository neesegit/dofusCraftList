import sqlite3

DB_NAME = "dofus.db"

def init_db():
    """Initialise la base de données et crée les tables si elles n'existent pas."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Table des items
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """)

    # Table des recettes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recettes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER NOT NULL,
        material_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY(item_id) REFERENCES items(id),
        FOREIGN KEY(material_id) REFERENCES items(id)
    )
    """)

    # Table de l'inventaire
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventaire (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY(item_id) REFERENCES items(id)
    )
    """)

    conn.commit()
    conn.close()

def get_connection():
    """Renvoie une connexion à la base de données."""
    return sqlite3.connect(DB_NAME)

def ajouter_recette(item_name, material_name, quantity):
    """Ajoute une recette liant un item à ses matières premières."""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Récupérer les IDs de l'item et de la matière première
        cursor.execute("SELECT id FROM items WHERE name = ?", (item_name,))
        item_id = cursor.fetchone()

        cursor.execute("SELECT id FROM items WHERE name = ?", (material_name,))
        material_id = cursor.fetchone()

        if not item_id or not material_id:
            raise ValueError("Item ou matière première introuvable.")

        # Insérer la relation dans la table des recettes
        cursor.execute("""
            INSERT INTO recettes (item_id, material_id, quantity)
            VALUES (?, ?, ?)
        """, (item_id[0], material_id[0], quantity))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        raise ValueError("Cette recette existe déjà.")
    finally:
        conn.close()


def obtenir_recette(item_name):
    """Récupère les matières premières nécessaires pour un item donné."""
    conn = get_connection()
    cursor = conn.cursor()

    # Récupérer l'ID de l'item
    cursor.execute("SELECT id FROM items WHERE name = ?", (item_name,))
    item_id = cursor.fetchone()

    if not item_id:
        conn.close()
        return []

    # Récupérer les recettes associées
    cursor.execute("""
        SELECT i.name, r.quantity
        FROM recettes r
        JOIN items i ON r.material_id = i.id
        WHERE r.item_id = ?
    """, (item_id[0],))
    recettes = cursor.fetchall()
    conn.close()

    return recettes

