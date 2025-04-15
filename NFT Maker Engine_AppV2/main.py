import json
from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
import os
import random

def load_user_settings():
    try:
        with open("user.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"bg_color": "black"}

def save_user_settings(settings):
    with open("user.json", "w") as file:
        json.dump(settings, file)

def change_bg_color(color):
    screen.configure(bg=color)
    user_settings["bg_color"] = color
    save_user_settings(user_settings)

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

def create_new_project():
    form = Toplevel(screen)
    form.title("Nouveau projet")
    form.geometry("300x150")
    form.grab_set()

    Label(form, text="Largeur :").pack(pady=5)
    width_entry = Entry(form)
    width_entry.pack()

    Label(form, text="Hauteur :").pack(pady=5)
    height_entry = Entry(form)
    height_entry.pack()

    def validate():
        try:
            width = int(width_entry.get())
            height = int(height_entry.get())

            project_folder = "project_files"
            os.makedirs(os.path.join(project_folder, "Face"), exist_ok=True)
            os.makedirs(os.path.join(project_folder, "Hair"), exist_ok=True)
            os.makedirs(os.path.join(project_folder, "Body"), exist_ok=True)

            # Créer le bouton projet
            project_button = Button(screen, text="Projet", bg="lightblue",
                                    command=lambda: show_project_menu(project_button, width, height))
            project_button.place(x=300 - width // 2, y=300 - height // 2, width=width, height=height)

            # Créer le cadre de prévisualisation
            create_image_gallery_frame()

            form.destroy()
        except ValueError:
            showinfo("Erreur", "Veuillez entrer des dimensions valides !")

    Button(form, text="Créer le projet", command=validate).pack(pady=10)

def create_image_gallery_frame():
    global canvas, image_frame, thumbnails, right_frame

    if 'right_frame' in globals() and right_frame.winfo_exists():
        return

    right_frame = Frame(screen, width=300, bg="lightgray")
    right_frame.pack(side=RIGHT, fill=Y)

    canvas = Canvas(right_frame, width=300, bg="lightgray", highlightthickness=0)
    scrollbar = Scrollbar(right_frame, orient=VERTICAL, command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    image_frame = Frame(canvas, bg="lightgray")
    canvas.create_window((0, 0), window=image_frame, anchor="nw")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    thumbnails = []
    refresh_image_gallery()

def show_project_menu(widget, width, height):
    def add_image_to_folder(folder_name):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
        if file_path:
            destination = os.path.join("project_files", folder_name, os.path.basename(file_path))
            os.rename(file_path, destination)
            refresh_image_gallery()  # met à jour l'affichage

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

        face_image = Image.open(os.path.join(face_folder, selected_face)).resize((width, height))
        hair_image = Image.open(os.path.join(hair_folder, selected_hair)).resize((width, height))
        body_image = Image.open(os.path.join(body_folder, selected_body)).resize((width, height))

        combined_image = Image.new("RGBA", (width, height))
        combined_image.paste(face_image, (0, 0), face_image.convert("RGBA"))
        combined_image.paste(hair_image, (0, 0), hair_image.convert("RGBA"))
        combined_image.paste(body_image, (0, 0), body_image.convert("RGBA"))

        combined_photo = ImageTk.PhotoImage(combined_image)
        widget.configure(image=combined_photo, text="")
        widget.image = combined_photo

    Button(screen, text="Face", command=lambda: add_image_to_folder("Face")).place(x=600, y=100)
    Button(screen, text="Hair", command=lambda: add_image_to_folder("Hair")).place(x=600, y=150)
    Button(screen, text="Body", command=lambda: add_image_to_folder("Body")).place(x=600, y=200)
    Button(screen, text="Generate", command=generate_image).place(x=600, y=250)

def refresh_image_gallery():
    for widget in image_frame.winfo_children():
        widget.destroy()

    folders = ["Face", "Hair", "Body"]
    thumbnails.clear()

    row = 0
    col = 0
    for folder in folders:
        folder_path = os.path.join("project_files", folder)
        if os.path.exists(folder_path):
            images = os.listdir(folder_path)
            for image_name in images:
                try:
                    path = os.path.join(folder_path, image_name)
                    img = Image.open(path).resize((64, 64))
                    img_tk = ImageTk.PhotoImage(img)
                    thumbnails.append(img_tk)
                    label = Label(image_frame, image=img_tk, text=folder, compound="top")
                    label.grid(row=row, column=col, padx=5, pady=5)
                    col += 1
                    if col >= 4:
                        col = 0
                        row += 1
                except:
                    continue

    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


def _on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

user_settings = load_user_settings()

screen = Tk()
screen.title("Éditeur de calques")
screen.geometry("1100x600")
screen.configure(bg=user_settings["bg_color"])

menubar = Menu(screen)
menu_param = Menu(menubar, tearoff=0)
menu_colors_main = Menu(menu_param, tearoff=0)
menu_themes = Menu(menu_colors_main, tearoff=0)

for category, colors in color_categories.items():
    submenu = Menu(menu_themes, tearoff=0)
    for color in colors:
        submenu.add_command(label=color.capitalize(), command=lambda c=color: change_bg_color(c))
    menu_themes.add_cascade(label=category, menu=submenu)

menu_colors_main.add_cascade(label="Thèmes", menu=menu_themes)
menu_param.add_cascade(label="Personnalisations", menu=menu_colors_main)
menubar.add_cascade(label="Paramètres", menu=menu_param)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Nouveau projet", command=create_new_project)
menu1.add_separator()
menu1.add_command(label="Quitter", command=screen.quit)
menubar.add_cascade(label="Fichier", menu=menu1)

screen.config(menu=menubar)



screen.mainloop()
