import json
from tkinter import *
from tkinter.messagebox import showinfo

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
    print("Données sauvegardées :", settings)  # Debug

def change_bg_color(color):
    """Change la couleur de fond de l'application et sauvegarde le choix."""
    screen.configure(bg=color)
    user_settings["bg_color"] = color
    save_user_settings(user_settings)

# Charger les paramètres utilisateur
user_settings = load_user_settings()

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

# Initialiser la fenêtre principale
screen = Tk()
screen.title("Éditeur de calques")
screen.geometry("600x600")
screen.configure(bg=user_settings["bg_color"])  # Charger la couleur sauvegardée

# Barre de menu
menubar = Menu(screen)

# Menu Paramètres
menu_param = Menu(menubar, tearoff=0)

# Sous-menu Personnalisations
menu_colors_main = Menu(menu_param, tearoff=0)

# Sous-menu Thèmes (ajouté après Personnalisations)
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

# Menu Fichier
menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Créer", command=lambda: showinfo("Alerte", "Bravo!"))
menu1.add_command(label="Editer", command=lambda: showinfo("Alerte", "Bravo!"))
menu1.add_separator()
menu1.add_command(label="Quitter", command=screen.quit)
menubar.add_cascade(label="Fichier", menu=menu1)

menubar.add_cascade(label="Paramètres", menu=menu_param)

# Associer la barre de menu à la fenêtre
screen.config(menu=menubar)

# Lancer la boucle principale
screen.mainloop()
