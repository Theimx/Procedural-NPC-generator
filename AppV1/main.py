import json
from tkinter import *
from tkinter import filedialog, simpledialog
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
import os
import random

def load_user_settings():
    """Charge les paramètres utilisateur depuis un fichier JSON."""
    try:
        with open("user.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"bg_color": "black"}  # Valeur par défaut

def save_user_settings(settings):
    """Sauvegarde les paramètres utilisateur dans un fichier JSON."""
    with open("user.json", "w") as file:
        json.dump(settings, file)

# Fonction pour changer la couleur de fond
def change_bg_color(color):
    screen.configure(bg=color)
    user_settings["bg_color"] = color
    save_user_settings(user_settings)

# Dictionnaire de couleurs par catégorie
color_categories = {
    "Blanc et dérivés": ["white", "snow", "ivory", "linen", "seashell", "floralwhite", "ghostwhite", "honeydew", "azure"],
    "Noir et gris": ["black", "dimgray", "gray", "darkgray", "silver", "lightgray", "gainsboro", "whitesmoke"],
    "Rouge et dérivés": ["red", "darkred", "firebrick", "indianred", "lightcoral", "salmon", "darksalmon", "lightsalmon"],
    "Rose et violet": ["pink", "lightpink", "hotpink", "deeppink", "mediumvioletred", "palevioletred", "purple", "orchid"],
    "Bleu et dérivés": ["blue", "darkblue", "midnightblue", "navy", "royalblue", "dodgerblue", "deepskyblue", "skyblue"],
    "Vert et dérivés": ["green", "darkgreen", "forestgreen", "seagreen", "limegreen", "lime", "mediumseagreen", "springgreen"],
    "Jaune et orange": ["yellow", "gold", "lightyellow", "lemonchiffon", "lightgoldenrodyellow", "papayawhip", "moccasin"],
    "Marron et beige": ["brown", "saddlebrown", "sienna", "chocolate", "peru", "tan", "rosybrown", "goldenrod"],
    "Cyan et turquoise": ["cyan", "darkcyan", "lightcyan", "paleturquoise", "aquamarine", "turquoise", "mediumturquoise"],
}

# Fonction pour créer un nouveau projet
def create_new_project():
    try:
        width = int(simpledialog.askstring("Dimensions", "Entrez la largeur du widget :"))
        height = int(simpledialog.askstring("Dimensions", "Entrez la hauteur du widget :"))

        # Créer le dossier du projet
        project_folder = "project_files"
        if not os.path.exists(project_folder):
            os.makedirs(project_folder)
        face_folder = os.path.join(project_folder, "Face")
        hair_folder = os.path.join(project_folder, "Hair")
        body_folder = os.path.join(project_folder, "Body")
        os.makedirs(face_folder, exist_ok=True)
        os.makedirs(hair_folder, exist_ok=True)
        os.makedirs(body_folder, exist_ok=True)

        # Ajouter un widget représentant le projet
        project_button = Button(screen, text="Projet", bg="lightblue", command=lambda: show_project_menu(project_button, width, height))
        project_button.place(x=300 - width // 2, y=300 - height // 2, width=width, height=height)
    except ValueError:
        showinfo("Erreur", "Veuillez entrer des dimensions valides !")

# Fonction pour afficher le menu d'options pour un projet
def show_project_menu(widget, width, height):
    # Ajouter des boutons au clic sur le widget
    def add_image_to_folder(folder_name):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
        if file_path:
            destination = os.path.join("project_files", folder_name, os.path.basename(file_path))
            os.rename(file_path, destination)

    def generate_image():
        face_folder = os.path.join("project_files", "Face")
        hair_folder = os.path.join("project_files", "Hair")
        body_folder = os.path.join("project_files", "Body")
        face_images = os.listdir(face_folder)
        hair_images = os.listdir(hair_folder)
        body_images = os.listdir(body_folder)

        if not face_images or not hair_images or not body_images:
            showinfo("Erreur", "Les dossiers Face, Hair ou Body sont vides !")
            return

        selected_face = random.choice(face_images)
        selected_hair = random.choice(hair_images)
        selected_body = random.choice(body_images)

        # Afficher les images superposées sur le widget
        face_path = os.path.join(face_folder, selected_face)
        hair_path = os.path.join(hair_folder, selected_hair)
        body_path = os.path.join(body_folder, selected_body)

        face_image = Image.open(face_path).resize((width, height))
        hair_image = Image.open(hair_path).resize((width, height))
        body_image = Image.open(body_path).resize((width, height))

        combined_image = Image.new("RGBA", (width, height))
        combined_image.paste(face_image, (0, 0), face_image.convert("RGBA"))
        combined_image.paste(hair_image, (0, 0), hair_image.convert("RGBA"))
        combined_image.paste(body_image, (0, 0), body_image.convert("RGBA"))

        combined_photo = ImageTk.PhotoImage(combined_image)

        widget.configure(image=combined_photo, text="")
        widget.image = combined_photo  # Garder une référence pour éviter la suppression par le garbage collector

    # Boutons
    face_button = Button(screen, text="Face", command=lambda: add_image_to_folder("Face"))
    face_button.place(x=600, y=100)
    hair_button = Button(screen, text="Hair", command=lambda: add_image_to_folder("Hair"))
    hair_button.place(x=600, y=150)
    body_button = Button(screen, text="Body", command=lambda: add_image_to_folder("Body"))
    body_button.place(x=600, y=200)
    generate_button = Button(screen, text="Generate", command=generate_image)
    generate_button.place(x=600, y=250)

# Charger les paramètres utilisateur
user_settings = load_user_settings()

# Initialiser la fenêtre principale
screen = Tk()
screen.title("Éditeur de calques")
screen.geometry("800x600")
screen.configure(bg=user_settings["bg_color"])

# Barre de menu
menubar = Menu(screen)

# Menu Paramètres
menu_param = Menu(menubar, tearoff=0)

# Sous-menu Personnalisations
menu_colors_main = Menu(menu_param, tearoff=0)

# Sous-menu Thèmes
menu_themes = Menu(menu_colors_main, tearoff=0)

# Ajouter les catégories principales comme sous-menus du menu Thèmes
for category, colors in color_categories.items():
    submenu = Menu(menu_themes, tearoff=0)
    for color in colors:
        submenu.add_command(label=color.capitalize(), command=lambda c=color: change_bg_color(c))
    menu_themes.add_cascade(label=category, menu=submenu)

# Ajouter "Thèmes" dans "Personnalisations"
menu_colors_main.add_cascade(label="Thèmes", menu=menu_themes)

# Ajouter "Personnalisations" dans "Paramètres"
menu_param.add_cascade(label="Personnalisations", menu=menu_colors_main)

# Ajouter "Paramètres" dans la barre de menu
menubar.add_cascade(label="Paramètres", menu=menu_param)

# Menu Fichier
menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Nouveau projet", command=create_new_project)
menu1.add_separator()
menu1.add_command(label="Quitter", command=screen.quit)
menubar.add_cascade(label="Fichier", menu=menu1)

# Associer la barre de menu à la fenêtre
screen.config(menu=menubar)

# Lancer la boucle principale
screen.mainloop()
