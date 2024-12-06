import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar
from logic import ajouter_item, supprimer_item, ajouter_element  # Logique métier
from database import get_connection  # Connexion à la base de données


def update_item_list(listbox):
    """Met à jour la liste des items affichée à gauche."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM items ORDER BY name")
    items = cursor.fetchall()
    conn.close()

    listbox.delete(0, tk.END)  # Efface la liste existante
    for item in items:
        listbox.insert(tk.END, item[0])  # Ajoute chaque item

def afficher_recette(item_name, frame):
    """Affiche les matières premières nécessaires dans le cadre central."""
    from logic import obtenir_recette

    recettes = obtenir_recette(item_name)

    # Nettoyer la zone noire
    for widget in frame.winfo_children():
        widget.destroy()

    # Afficher les ingrédients
    for ligne in recettes:
        label = tk.Label(frame, text=ligne, bg="white", font=("Arial", 14))
        label.pack(pady=5)



def start_gui():
    root = tk.Tk()
    root.title("Dofus Craft List")
    root.geometry("1920x1280")  # Définit la taille de la fenêtre
    root.configure(bg="lightgrey")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)

    # **Cadre pour la liste des items**
    frame_left = tk.Frame(root, bg="lightgrey", width=500, height=900)
    frame_left.grid(row=1, column=0, padx=20, pady=20, sticky="n")

    #label_items = tk.Label(frame_left, text="Liste des objets dans la base de données", bg="lightgrey", font=("Arial", 16))
    #label_items.pack(pady=10)

    listbox_items = Listbox(frame_left, width=50, height=40, font=("Arial", 12))
    listbox_items.pack(pady=10)

    scrollbar = Scrollbar(frame_left, orient=tk.VERTICAL, command=listbox_items.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox_items.config(yscrollcommand=scrollbar.set)

    # **Zone centrale pour les détails des ingrédients**
    frame_center = tk.Frame(root, bg="white", width=1000, height=900)
    frame_center.grid(row=1, column=1, sticky="nsew")

    label_placeholder = tk.Label(frame_center, text="Place holder de la liste des items de l'item choisi", bg="white",
                                  font=("Arial", 14), width=120)
    label_placeholder.pack(expand=True, pady=20)

    # **Zone pour les actions**
    frame_top = tk.Frame(root, bg="lightgrey", width=1920, height=180)
    frame_top.grid(row=0, column=0, columnspan=2, pady=10)

    label_entry = tk.Label(frame_top, text="Entrer le nom de l'item", bg="lightgrey", font=("Arial", 14))
    label_entry.pack(pady=10)

    entry_item = tk.Entry(frame_top, width=30, font=("Arial", 14), justify="center")
    entry_item.pack(pady=10)

    label_material = tk.Label(frame_top, text="Matière première", bg="lightgrey", font=("Arial", 14))
    label_material.pack()

    entry_material = tk.Entry(frame_top, width=30, font=("Arial", 14))
    entry_material.pack()

    label_quantity = tk.Label(frame_top, text="Quantité", bg="lightgrey", font=("Arial", 14))
    label_quantity.pack()

    entry_quantity = tk.Entry(frame_top, width=30, font=("Arial", 14))
    entry_quantity.pack()

    btn_add_recipe = tk.Button(frame_top, text=f"Ajouter un élément", font=("Arial", 14), width=20,
                            command=lambda: ajouter_element(
                                listbox_items.get(tk.ACTIVE),
                                entry_material.get(),
                                entry_quantity.get()))
    btn_add_recipe.pack(pady=10)


    # **Boutons**
    btn_add = tk.Button(frame_top, text="Ajouter un item", font=("Arial", 14), width=20,
                        command=lambda: [ajouter_item(entry_item.get()), update_item_list(listbox_items)])
    btn_add.pack(side=tk.LEFT, padx=20, pady=10)

    btn_delete = tk.Button(frame_top, text="Supprimer un item", font=("Arial", 14), width=20,
                           command=lambda: [supprimer_item(entry_item.get()), update_item_list(listbox_items)])
    btn_delete.pack(side=tk.LEFT, padx=20, pady=10)


    def on_item_selected(event):
        try:
            selected_item = listbox_items.get(listbox_items.curselection())
            afficher_recette(selected_item, frame_center)
        except tk.TclError:
            pass

    listbox_items.bind("<<ListboxSelect>>", on_item_selected)

    # Initialisation de la liste des items
    update_item_list(listbox_items)

    root.mainloop()
