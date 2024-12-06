from tkinter import messagebox
from database import get_connection, ajouter_recette as db_ajouter_recette, obtenir_recette as db_obtenir_recette
import sqlite3

def ajouter_item(item_name):
    """Ajoute un nouvel item à la base de données."""
    if not item_name:
        messagebox.showwarning("Erreur", "Le nom de l'item est vide.")
        return False

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO items (name) VALUES (?)", (item_name,))
        conn.commit()
        messagebox.showinfo("Succès", f"L'item '{item_name}' a été ajouté avec succès.")
        return True
    except sqlite3.IntegrityError:
        messagebox.showwarning("Erreur", f"L'item '{item_name}' existe déjà.")
        return False
    finally:
        conn.close()

def supprimer_item(item_name):
    """Supprime un item et ses associations de la base de données."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Rechercher l'ID de l'item
        cursor.execute("SELECT id FROM items WHERE name = ?", (item_name,))
        item_id = cursor.fetchone()
        if not item_id:
            messagebox.showwarning("Erreur", f"L'item '{item_name}' n'existe pas.")
            return False

        # Supprimer les données associées
        cursor.execute("DELETE FROM recettes WHERE item_id = ? OR material_id = ?", (item_id[0], item_id[0]))
        cursor.execute("DELETE FROM inventaire WHERE item_id = ?", (item_id[0],))
        cursor.execute("DELETE FROM items WHERE id = ?", (item_id[0],))
        conn.commit()

        messagebox.showinfo("Succès", f"L'item '{item_name}' a été supprimé avec succès.")
        return True
    finally:
        conn.close()

def ajouter_element(item_name, material_name, quantity):
    """Ajoute une recette via la logique métier."""
    if not item_name or not material_name or not quantity:
        messagebox.showwarning("Erreur", "Tous les champs doivent être remplis.")
        return False

    try:
        db_ajouter_recette(item_name, material_name, int(quantity))
        messagebox.showinfo("Succès", f"La recette pour '{item_name}' a été ajoutée avec succès.")
        return True
    except ValueError as e:
        messagebox.showwarning("Erreur", str(e))
        return False


def obtenir_recette(item_name):
    """Récupère les ingrédients d'un item et retourne une liste formatée."""
    recettes = db_obtenir_recette(item_name)
    if not recettes:
        return [f"Aucune recette trouvée pour '{item_name}'."]
    return [f"{quantity}x {name}" for name, quantity in recettes]
