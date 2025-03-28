"""
FRESHDATA MONITOR - Application de suivi des températures
=======================================================

Cette application permet de :
- Surveiller les températures des chambres froides
- Enregistrer et visualiser les données
- Gérer les accès utilisateurs
- Archiver les données d'hygiène
"""
# ====== IMPORTATION DES BIBLIOTHÈQUES =======
import tkinter as tk                                  # Bibliothèque pour l'interface graphique
from tkinter import ttk, messagebox                   # Composants avancés et boîtes de dialogue
from PIL import Image, ImageTk                        # Manipulation d'images
import os                                             # Opérations sur le système de fichiers
from pathlib import Path                              # Gestion avancée des chemins de fichiers
import matplotlib.pyplot as plt                       # Création de graphiques
import datetime                                       # Manipulation des dates et heures
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Intégration des graphiques dans Tkinter
import sqlite3                                        # Accès à la base de données SQLite
from tkinter import filedialog as fd                  # Boîtes de dialogue pour sélection de fichiers
import csv                                            # Manipulation des fichiers CSV

# ====== INITIALISATION DES VARIABLES DE DATE =======
# Obtenir le mois en cours
current_month = datetime.datetime.now().strftime("%B").capitalize()
current_date = str(datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S"))
#print(current_date)


# ====== CONFIGURATION DE LA FENÊTRE PRINCIPALE =======
root = tk.Tk()
root.title("FRESHDATA MONITOR")
root.geometry("1080x720")


# ====== CHARGEMENT DES ICÔNES =======
image_menu_icon = tk.PhotoImage(file="data/image/Menu.png")
image_home_icon = tk.PhotoImage(file="data/image/Home.png")
image_chart_icon = tk.PhotoImage(file="data/image/Graph.png")
image_check_icon = tk.PhotoImage(file="data/image/Check.png")
image_settings_icon = tk.PhotoImage(file="data/image/Settings.png")
image_logout_icon = tk.PhotoImage(file="data/image/Logout.png")
image_lea_icon = tk.PhotoImage(file="data/image/LEA.jpg")
image_package_icon = tk.PhotoImage(file="data/image/Package.png")
image_info_icon = tk.PhotoImage(file="data/image/Alert.png")
image_X_icon = tk.PhotoImage(file="data/image/X.png")


# ====== DÉFINITION DES FONCTIONS =======    
def switch_indicatation(indicator_lb, page):
    """
    pre: indicator_lb est un label de couleur blanche, page est une fonction
    post: change la couleur de l'indicateur et affiche la page correspondante
    """
    
    # Réinitialise tous les indicateurs à la couleur du menu
    btn_home_indicator.configure(bg=menu_bar_colour)
    btn_chart_indicator.configure(bg=menu_bar_colour)
    btn_package_indicator.configure(bg=menu_bar_colour)
    btn_check_indicator.configure(bg=menu_bar_colour)
    btn_logout_indicator.configure(bg=menu_bar_colour)
    btn_settings_indicator.configure(bg=menu_bar_colour)
    btn_info_indicator.configure(bg=menu_bar_colour)
    
    # permet de changer la couleur de l'indicateur en blanc
    indicator_lb.configure(bg="white")

    # Réduit le menu si étendu
    if menu_bar_frame.winfo_width() == 400:
        reduce_menu_bar()
        
    # Nettoie la page actuelle avant d'afficher la nouvelle
    for frame in page_frame.winfo_children():
        frame.destroy()
    
    # Affiche la nouvelle page
    page()


def extend_menu_bar():
    """Étend la barre de menu latérale"""
    menu_bar_frame.configure(width=400)
    btn_menu_icon.config(image=image_X_icon)
    btn_menu_icon.config(command=reduce_menu_bar)
    
def reduce_menu_bar():
    """Réduit la barre de menu latérale"""
    menu_bar_frame.configure(width=75)
    btn_menu_icon.config(image=image_menu_icon)
    btn_menu_icon.config(command=extend_menu_bar)

def home_page():
    """Affiche la page d'accueil avec l'image principale"""
    home_page_fm = tk.Frame(page_frame)
    
    # Chargement et affichage de l'image d'accueil
    image_path = "data/image/fdm.jpg"
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)
    lb_image = ttk.Label(home_page_fm, image=photo)
    lb_image.image = photo  # Garde une référence pour éviter la suppression par le garbage collector
    lb_image.pack()
    home_page_fm.pack(fill=tk.BOTH, expand=True)

def enregistrer(ety_value_temp, cbx_choice_chart_save):
    """
    pre: ety_value_temp est un champ de saisie, cbx_choice_chart_save est une combobox
    post: enregistre les données de température dans la base de données
    """


    # Récupère les informations de l'utilisateur connecté
    fichierSauvegarde = open("data/db/userConnect.txt","r",encoding="utf-8")
    contenu = fichierSauvegarde.readlines()[0].split(';')
        
    # Vérifie que les champs sont remplis
    if not ety_value_temp.get() or not cbx_choice_chart_save.get():
        return (messagebox.showerror('Erreur', 'Il manque une valeur !'))
    
    # Convertit la température en float
    try:
        temperature = float(ety_value_temp.get())
    except ValueError:
        return (messagebox.showerror("Erreur","Il faut entrer un chiffre/nombre dans température"))
    else:
        # Enregistre les données dans la base de données
        connection = sqlite3.connect("data/db/freshdata.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO chambre VALUES (?,?,?,?,?)",(current_date,cbx_choice_chart_save.get(),ety_value_temp.get(),contenu[0],contenu[1]))
        connection.commit()
        connection.close()

        # Vérifications des seuils de température selon la chambre
        if cbx_choice_chart_save.get() == "Chambre 1 - Légumes":
            if temperature > 7:
                messagebox.showwarning("Attention", "Attention, la température est trop élevée !")
            elif temperature < 0:
                messagebox.showwarning("Attention","Attention, la température est trop basse !")
        elif cbx_choice_chart_save.get() == "Chambre 2 - BOF/POISSON/VIANDE":
            if temperature > 3:
                messagebox.showwarning("Attention", "Attention, la température est trop élevée !")
            elif temperature < 0:
                messagebox.showwarning("Attention","Attention, la température est trop basse !")
        elif cbx_choice_chart_save.get() == "Chambre 3 - Produits finis":
            if temperature > 3:
                messagebox.showwarning("Attention", "Attention, la température est trop élevée !")
            elif temperature < 0:
                messagebox.showwarning("Attention","Attention, la température est trop basse !")
        else:
            if temperature < -18:
                messagebox.showwarning("Attention", "Attention, la température est trop froide !")
            elif temperature > 0:
                messagebox.showwarning("Attention","Attention, la température est trop élevée !")   
        messagebox.showinfo("Succès", "Données enregistrées avec succès") 

def delete_last_entry():
    """Supprime la dernière entrée de température dans la base de données"""
    try:
        connection = sqlite3.connect("data/db/freshdata.db")
        cursor = connection.cursor()
        # Récupérer la dernière entrée pour vérification
        cursor.execute("SELECT date, numero_chambre, temperature, prenom, classe FROM chambre ORDER BY date DESC LIMIT 1")
        last_entry = cursor.fetchone()
        
        if last_entry:
            confirm_delete = messagebox.askokcancel("Suppression", 
                    f"Voulez-vous vraiment supprimer la dernière entrée ?\n\nDate: {last_entry[0]}\nChambre: {last_entry[1]}\nTempérature: {last_entry[2]}°C")
            
            if confirm_delete:
                cursor.execute("DELETE FROM chambre WHERE rowid = (SELECT MAX(rowid) FROM chambre)")
                connection.commit()
                messagebox.showinfo("Succès", "Dernière entrée supprimée avec succès")
        else:
            messagebox.showinfo("Info", "Aucune entrée à supprimer")
            
        connection.close()
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la suppression : {str(e)}")

def chart_page():
    """Affiche la page des graphiques pour visualiser les températures"""
    
    # Création du frame principal
    chart_page_fm = tk.Frame(page_frame)
    chart_page_fm.pack(fill=tk.BOTH, expand=True)

    # Création des conteneurs
    fm_contenair = tk.Frame(chart_page_fm, bg="#a6c7de")
    fm_contenair.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Frame pour le graphique
    fm_chart = tk.Frame(chart_page_fm, bg="white")
    fm_chart.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    # Frame pour la saisie des valeurs
    fm_entry_value = tk.LabelFrame(fm_contenair, text="Entrez une valeur", bg="#a6c7de")
    fm_entry_value.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=5)

    # Frame pour le choix du graphique
    fm_graph_choice = tk.LabelFrame(fm_contenair, text="Sélection de la période de temps", bg="#a6c7de")
    fm_graph_choice.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=5)

    # Création des widgets pour la saisie des valeurs
    lb_entry_value = tk.Label(fm_entry_value, text="Température :", font=("Bold", 10), bg="#a6c7de")
    lb_entry_value.pack(side=tk.LEFT, padx=15)

    ety_value_temp = tk.Entry(fm_entry_value)
    ety_value_temp.pack(side=tk.LEFT, padx=15)

    lb_choice_chart = tk.Label(fm_entry_value, text="Choix de la chambre froide :", font=("Bold", 10), bg="#a6c7de")
    lb_choice_chart.pack(side=tk.LEFT, padx=15)

    # Valeurs disponibles dans la combobox
    cbx_values=["Chambre 1 - Légumes", "Chambre 2 - BOF/POISSON/VIANDE", "Chambre 3 - Produits finis", "Chambre 4 - Congélateur"]

    cbx_choice_chart_save = ttk.Combobox(fm_entry_value, values=cbx_values)
    cbx_choice_chart_save.pack(side=tk.LEFT, padx=15)

    # Bouton 
    btn_save_value = tk.Button(fm_entry_value, text="Enregistrer", font=("Bold", 10), bg="#a6c7de", 
                              command=lambda: enregistrer(ety_value_temp, cbx_choice_chart_save))
    btn_save_value.pack(side=tk.LEFT, padx=15)

    btn_delete_last_entry = tk.Button(fm_entry_value, text="Supprimer dernière entrée", font=("Bold", 10), bg="#a6c7de", 
                                     command=delete_last_entry)
    btn_delete_last_entry.pack(side=tk.LEFT, padx=15)

    # Widgets pour le choix du graphique
    lb_test = tk.Label(fm_graph_choice, text="Choix du graphique à afficher", font=("Bold", 10), bg="#a6c7de")
    lb_test.pack(side=tk.LEFT, fill=tk.BOTH, padx=15)

    cbx_choice_chart = ttk.Combobox(fm_graph_choice, values=cbx_values)
    cbx_choice_chart.pack(side=tk.LEFT, padx=15)

    btn_graph_choice_validate = tk.Button(fm_graph_choice, text="Valider", font=("Bold", 10), bg="#a6c7de", 
                                         command=lambda: update_graph(cbx_choice_chart, canvas, fm_chart))
    btn_graph_choice_validate.pack(side=tk.LEFT, padx=15)

    # Configuration initiale du graphique(vide)
    title_chart = "Température Frigo"

    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot(111)
    ax.set_title(title_chart)
    ax.set_xlabel('Date')
    ax.set_ylabel('Température (°C)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    ax.grid(True)
    canvas = FigureCanvasTkAgg(fig, master=fm_chart)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    
def update_graph(cbx_choice_chart, canvas, fm_chart):
    """
    pre: cbx_choice_chart_save est une combobox contenant la chambre sélectionnée, canvas la zone de dessin du graphique, fm_chart est le frame contenant le graphique
    post:  Met à jour le graphique avec les données de la chambre sélectionnée
    """
   
    # Récupérer les données de la base pour la chambre sélectionnée
    connection = sqlite3.connect("data/db/freshdata.db")
    cursor = connection.cursor()
    cursor.execute("SELECT date, temperature FROM chambre WHERE numero_chambre = ? ORDER BY date", (cbx_choice_chart.get(),))
    data = cursor.fetchall()
    connection.close()

    # Vérifier si des données existent
    if not data:
        messagebox.showinfo("Info", "Aucune donnée disponible pour cette chambre")
        return
    
    # Nettoyer le frame du graphique
    for widget in fm_chart.winfo_children():
        widget.destroy()
    
    # Préparer les données pour le graphique
    dates = [datetime.datetime.strptime(row[0], "%Y-%m-%d  %H:%M:%S").date() for row in data]
    temperatures = [float(row[1]) for row in data]

    # Créer le nouveau graphique
    title_chart = "Température Frigo"

    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot(111)  
    ax.plot(dates, temperatures, marker='o')
    ax.set_title(title_chart)
    ax.set_xlabel('Date')
    ax.set_ylabel('Température (°C)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    ax.grid(True)
    canvas = FigureCanvasTkAgg(fig, master=fm_chart)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def package_page():
    """Affiche la page de gestion des stocks (fonctionnalité future)"""
    package_page_fm = tk.Frame(page_frame)
    lb_package = tk.Label(package_page_fm, text="Stock (Prochainement)", font=("Bold", 20))
    lb_package.place(x=380, y=300)
    package_page_fm.pack(fill=tk.BOTH, expand=True)

def check_page():
    """Affiche la page de gestion des tâches et du ménage (fonctionnalité future)"""
    check_page_fm = tk.Frame(page_frame)
    lb_check = tk.Label(check_page_fm, text="Tâche & Ménage (Prochainement)", font=("Bold", 20))
    lb_check.place(x=320, y=300)
    check_page_fm.pack(fill=tk.BOTH, expand=True)

def select_file():
    """Ouvre une boîte de dialogue pour sélectionner un fichier CSV d'élèves"""
    filetypes = [('csv files', '*.csv')]
    filename = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
      
    if not filename:  # Si aucun fichier n'est sélectionné
        messagebox.showerror('Erreur', 'Aucun fichier sélectionné')
        return
            
    messagebox.showinfo(title='Selected File', message="La liste d'élèves a été importée avec succès")
    print(filename)
    csv_files_create(filename)

def csv_files_create(filename):
    """
    pre: filename est le chemin du fichier CSV à traiter
    post: Traite le fichier CSV sélectionné et l'importe dans la base de données
    """
    
    # Lecture du fichier CSV
    with open(filename, 'r') as fichier_csv:
        Lecteur_csv = csv.reader(fichier_csv, delimiter=';')
        listeClasse = []
        for ligne in Lecteur_csv:
            listeClasse.append(ligne[0])
            listeClasse.append(ligne[1].replace('/', ''))
            listeClasse.append(ligne[3])
        
    try:
        # Connexion à la base de données et création de la table si nécessaire
        connection = sqlite3.connect("data/db/freshdata.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS authentification(identite TEXT NOT NULL, classe TEXT NOT NULL, naissance TEXT NOT NULL)")
    except:
        return messagebox.showerror('Erreur', 'Erreur de connexion à la base de données')
    
    # Insertion des données dans la base
    for i in range(3, len(listeClasse), 3):
        cursor.execute("INSERT INTO authentification VALUES(?,?,?)", (listeClasse[i], listeClasse[i+2], listeClasse[i+1]))
    connection.commit()
    connection.close()

def settings_page():
    """Ouvre la page des paramètres administrateur"""
    try:
        os.system('python "sources/popupAdmin.py"')
    except:
        return messagebox.showerror('Erreur', 'Erreur de connexion au fichier de connexion')
    settings_page_fm = tk.Frame(page_frame)
    
    settings_page_fm.pack(fill=tk.BOTH, expand=True)

    open_button = ttk.Button(settings_page_fm, text='Open a File', command=select_file)
    open_button.pack(expand=True)

def info_page():
    """Affiche la page d'informations sur l'application"""
    info_page_fm = tk.Frame(page_frame)
    lb_info = tk.Label(info_page_fm, text="Projet développé suite à la demande du LEA Robert Doisneau -\n Lycée d'Enseignement Adapté (Saint-Lô) permettant d'assurer\n le suivi des températures des chambres froides de la cuisine\n et d'avoir une application pour centraliser et archiver les\n données d'hygiène relatives à la cuisine.\n\n\nDéveloppé par:\n Ewald Lemarchant\nElouan Guillon\nRaphael Le Provot\n Année : 2024/2025", font=("Bold", 20))
    lb_info.place(x=220, y=120)
    info_page_fm.pack(fill=tk.BOTH, expand=True)
    
    # Ajout des logos
    image_path_LEA = "data/image/LEA.jpg"
    image_LEA = Image.open(image_path_LEA)
    photo_LEA = ImageTk.PhotoImage(image_LEA)
    image_label_LEA = ttk.Label(info_page_fm, image=photo_LEA)
    image_label_LEA.image = photo_LEA
    image_label_LEA.place(x=100, y=550)
    
    image_path_CC = "data/image/curiecorot.png"
    image_CC = Image.open(image_path_CC)
    photo_CC = ImageTk.PhotoImage(image_CC)
    image_label_CC = ttk.Label(info_page_fm, image=photo_CC)
    image_label_CC.image = photo_CC
    image_label_CC.place(x=520, y=550)

def on_closing():
    """Gère la fermeture de l'application avec confirmation"""
    verification = messagebox.askokcancel("Déconnexion", "Voulez-vous vraiment vous déconnecter ?")
    if verification == True:
        try:
            os.remove("data/db/userConnect.txt")
        except:
            pass
        root.destroy()
    else:
        return

# ====== CONFIGURATION DU MENU LATÉRAL =======
# Couleur du menu de gauche
menu_bar_colour = "#383838"

# Paramètres de base du menu de gauche
menu_bar_frame = tk.Frame(root, bg=menu_bar_colour)
menu_bar_frame.pack(side=tk.LEFT, fill=tk.Y)
menu_bar_frame.pack_propagate(flag=False)
menu_bar_frame.configure(width=75)

# Frame pour les pages
page_frame = tk.Frame(root)
page_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
home_page()  # Affiche la page d'accueil par défaut

# ====== CRÉATION DES BOUTONS DU MENU =======
# Bouton menu 
btn_menu_icon = tk.Button(menu_bar_frame, image=image_menu_icon, bg=menu_bar_colour,
                      bd=0, activebackground=menu_bar_colour,
                      command=extend_menu_bar)

# Bouton accueil
btn_home_icon = tk.Button(menu_bar_frame, image=image_home_icon, bg=menu_bar_colour,
                      bd=0, activebackground=menu_bar_colour,
                      command=lambda: switch_indicatation(indicator_lb=btn_home_indicator,
                                                          page=home_page))

# Bouton graphique
btn_chart_icon = tk.Button(menu_bar_frame, image=image_chart_icon, bg=menu_bar_colour,
                      bd=0, activebackground=menu_bar_colour,
                      command=lambda: switch_indicatation(indicator_lb=btn_chart_indicator,
                                                          page=chart_page))

# Bouton stock
btn_package_icon = tk.Button(menu_bar_frame, image=image_package_icon, bg=menu_bar_colour,
                      bd=0, activebackground=menu_bar_colour,
                      command=lambda: switch_indicatation(indicator_lb=btn_package_indicator,
                                                          page=package_page))

# Bouton information
btn_info_icon = tk.Button(menu_bar_frame, image=image_info_icon, bg=menu_bar_colour,
                      bd=0, activebackground=menu_bar_colour,
                      command=lambda: switch_indicatation(indicator_lb=btn_info_indicator,
                                                          page=info_page))

# Bouton déconnexion
btn_logout_icon = tk.Button(menu_bar_frame, image=image_logout_icon, bg=menu_bar_colour,
                                bd=0, activebackground=menu_bar_colour,
                                command=on_closing)

# Bouton paramètres
btn_settings_icon = tk.Button(menu_bar_frame, image=image_settings_icon, bg=menu_bar_colour,
                                bd=0, activebackground=menu_bar_colour,
                                command=lambda: switch_indicatation(indicator_lb=btn_settings_indicator,
                                                          page=settings_page))

# Bouton tâches et ménage
btn_check_icon = tk.Button(menu_bar_frame, image=image_check_icon, bg=menu_bar_colour,
                                bd=0, activebackground=menu_bar_colour,
                                command=lambda: switch_indicatation(indicator_lb=btn_check_indicator,
                                                          page=check_page))

# ====== INDICATEURS DE SÉLECTION =======
# Création des indicateurs visuels pour chaque bouton
btn_home_indicator = tk.Label(menu_bar_frame, bg="white")
btn_home_indicator.place(x=3, y=100, height=50, width=3)

btn_check_indicator = tk.Label(menu_bar_frame, bg=menu_bar_colour)
btn_check_indicator.place(x=3, y=180, height=50, width=3)

btn_chart_indicator = tk.Label(menu_bar_frame, bg=menu_bar_colour)
btn_chart_indicator.place(x=3, y=260, height=50, width=3)

btn_package_indicator = tk.Label(menu_bar_frame, bg=menu_bar_colour)
btn_package_indicator.place(x=3, y=340, height=50, width=3)

btn_logout_indicator = tk.Label(menu_bar_frame, bg=menu_bar_colour)
btn_logout_indicator.place(x=3, y=500, height=50, width=3)

btn_settings_indicator = tk.Label(menu_bar_frame, bg=menu_bar_colour)
btn_settings_indicator.place(x=3, y=580, height=50, width=3)

btn_info_indicator = tk.Label(menu_bar_frame, bg=menu_bar_colour)
btn_info_indicator.place(x=3, y=660, height=50, width=3)

# ====== LABELS DU MENU ÉTENDU =======
# Création des labels de texte pour le menu en mode étendu
home_page_lb = tk.Label(menu_bar_frame, text="Accueil", bg=menu_bar_colour, fg="white",
                        font=("Bold", 18), anchor=tk.W)
home_page_lb.place(x=85, y=100, width=160, height=50)
home_page_lb.bind("<Button-1>", lambda e: switch_indicatation(indicator_lb=btn_home_indicator,
                                                              page=home_page))

check_page_lb = tk.Label(menu_bar_frame, text="Tâche & Ménage", bg=menu_bar_colour, fg="white",
                        font=("Bold", 18), anchor=tk.W)
check_page_lb.place(x=85, y=180, width=250, height=50)
check_page_lb.bind("<Button-1>", lambda e: switch_indicatation(indicator_lb=btn_check_indicator,
                                                                     page=check_page))

chart_page_lb = tk.Label(menu_bar_frame, text="Graphique", bg=menu_bar_colour, fg="white",
                        font=("Bold", 18), anchor=tk.W)
chart_page_lb.place(x=85, y=260, width=250, height=50)
chart_page_lb.bind("<Button-1>", lambda e: switch_indicatation(indicator_lb=btn_chart_indicator,
                                                                   page=chart_page))

package_page_lb = tk.Label(menu_bar_frame, text="Stock", bg=menu_bar_colour, fg="white",
                        font=("Bold", 18), anchor=tk.W)
package_page_lb.place(x=85, y=340, width=200, height=50)
package_page_lb.bind("<Button-1>", lambda e: switch_indicatation(indicator_lb=btn_package_indicator,
                                                                 page=package_page))

logout_page_lb = tk.Label(menu_bar_frame, text="Déconnexion", bg=menu_bar_colour, fg="white",
                        font=("Bold", 18), anchor=tk.W)
logout_page_lb.place(x=85, y=500, width=200, height=50)
logout_page_lb.bind("<Button-1>", lambda e: on_closing())

settings_page_lb = tk.Label(menu_bar_frame, text="Paramètres", bg=menu_bar_colour, fg="white",
                        font=("Bold", 18), anchor=tk.W)
settings_page_lb.place(x=85, y=580, width=200, height=50)
settings_page_lb.bind("<Button-1>", lambda e: switch_indicatation(indicator_lb=btn_settings_indicator,
                                                                  page=settings_page))

info_page_lb = tk.Label(menu_bar_frame, text="Info", bg=menu_bar_colour, fg="white",
                        font=("Bold", 18), anchor=tk.W)
info_page_lb.place(x=85, y=660, width=200, height=50)
info_page_lb.bind("<Button-1>", lambda e: switch_indicatation(indicator_lb=btn_info_indicator,
                                                             page=info_page))

# ====== PLACEMENT DES BOUTONS =======
btn_menu_icon.place(x=9, y=10)
btn_home_icon.place(x=9, y=100)
btn_check_icon.place(x=9, y=180)
btn_chart_icon.place(x=9, y=260)
btn_package_icon.place(x=9, y=340)
btn_logout_icon.place(x=9, y=500)
btn_settings_icon.place(x=9, y=580)
btn_info_icon.place(x=9, y=660)

# ====== GESTIONNAIRE DE FERMETURE =======
# Configuration de l'événement de fermeture de la fenêtre
root.protocol("WM_DELETE_WINDOW", on_closing)

# ====== LANCEMENT DE L'APPLICATION =======
root.mainloop()