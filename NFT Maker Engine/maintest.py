#an app that can take one element of each to combine it to make a character 

# gender : 
# Female : 
#    - hair color 
#    - skin color
#    - eye  color
#
#    -Hair shape/type
#    -face expression
#    -Clothe
# Male : 
#    - hair color 
#    - skin color
#    - eye  color
#
#    -Hair shape/type
#    -face expression
#    -Clothe
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import sqlite3

# Création ou connexion à la base de données SQLite
def init_database():
    conn = sqlite3.connect("images.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            button_id INTEGER NOT NULL,
            file_path TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Fonction pour gérer la sélection d'image
def select_image(button_id):
    file_path = filedialog.askopenfilename(
        title="Sélectionner une image",
        filetypes=[("Fichiers d'image", "*.png *.jpg *.jpeg *.bmp *.gif")]
    )
    if file_path:
        try:
            # Charger l'image pour vérifier ses dimensions
            img = Image.open(file_path)
            if img.size == (512, 512):
                save_to_database(button_id, file_path)
                messagebox.showinfo("Succès", f"L'image a été ajoutée pour le bouton {button_id} !")
            else:
                messagebox.showerror("Erreur", "L'image doit avoir une taille de 512x512 pixels.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir l'image : {e}")

# Enregistrer le chemin de l'image dans la base de données
def save_to_database(button_id, file_path):
    conn = sqlite3.connect("images.db")
    cursor = conn.cursor()
    cursor.execute("REPLACE INTO images (button_id, file_path) VALUES (?, ?)", (button_id, file_path))
    conn.commit()
    conn.close()

# Récupérer les images associées aux boutons
def get_images():
    conn = sqlite3.connect("images.db")
    cursor = conn.cursor()
    cursor.execute("SELECT button_id, file_path FROM images")
    images = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    return images

# Afficher les images superposées
def display_images():
    images = get_images()
    img_objects = []
    canvas.delete("all")  # Effacer les anciennes images du canvas
    for button_id in range(1, 6):
        file_path = images.get(button_id)
        if file_path:
            try:
                img = Image.open(file_path)
                img = img.resize((200, 200))  # Redimensionner pour l'affichage
                img_tk = ImageTk.PhotoImage(img)
                img_objects.append(img_tk)  # Conserver une référence
                canvas.create_image(150, 150, image=img_tk, anchor="center")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de charger l'image du bouton {button_id} : {e}")
    canvas.image_refs = img_objects  # Empêche la suppression des images par le garbage collector

# Interface graphique avec Tkinter
def create_app():
    # Initialiser la base de données
    init_database()

    # Fenêtre principale
    root = tk.Tk()
    root.title("Application d'Images Superposées")

    # Frame pour les boutons à gauche
    left_frame = tk.Frame(root)
    left_frame.pack(side="left", fill="y", padx=10, pady=10)

    # Boutons pour ajouter des images
    for i in range(1, 6):
        button = tk.Button(left_frame, text=f"Ajouter Image ({i})", command=lambda id=i: select_image(id))
        button.pack(pady=5)

    # Bouton pour afficher les images superposées
    display_button = tk.Button(left_frame, text="Afficher Images", command=display_images)
    display_button.pack(pady=10)

    # Canvas pour afficher les images superposées
    global canvas
    canvas = tk.Canvas(root, width=300, height=300, bg="white")
    canvas.pack(expand=True, padx=20, pady=20)

    root.mainloop()

# Lancer l'application
if __name__ == "__main__":
    create_app()
