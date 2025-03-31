"""
FRESHDATA CONNEXION - Module d'authentification
===============================================

Ce script gère l'interface de connexion pour l'application FRESHDATA MONITOR(main.py).
Il permet aux professeurs et aux élèves de se connecter avec des identifiants différents.
"""

# ====== IMPORTATION DES BIBLIOTHÈQUES ======
import sqlite3                                  # Pour l'accès à la base de données
from tkinter import*                            # Pour l'interface graphique
import tkinter as tk                            # Import principal de Tkinter
from tkinter import ttk, messagebox             # Composants avancés et boîtes de dialogue
from PIL import Image, ImageTk                  # Manipulation d'images
import os                                       # Opérations sur le système de fichiers

# ====== IDENTIFIANTS ADMINISTRATEUR ======
# Identifiants prédéfinis pour connexion professeur/admin
prof_id = "admin"
prof_password = "1234"


def connexion():
    """
    Vérifie les identifiants saisis et connecte l'utilisateur
    - Pour les professeurs: vérifie les identifiants fixes
    - Pour les élèves: vérifie les identifiants dans la base de données
    """
    prof_id_verif = ety_id.get()
    prof_password_verif = ety_password.get()

    # Vérification pour les professeurs/administrateurs
    if prof_id_verif == prof_id and prof_password_verif == prof_password:
        # Enregistrement des informations de connexion dans un fichier éphémère
        fichierSauvegarde = open("data/db/userConnect.txt", "a", encoding="utf-8")
        fichierSauvegarde.write("prof")
        fichierSauvegarde.write(';')
        fichierSauvegarde.write("prof")
        fichierSauvegarde.close()
        
        # Ferme la page de connexion et lance l'application principale
        pageConnexion.destroy()
        os.system('python "sources/application.py"')
    else:
        # Vérification que tous les champs sont remplis
        if not ety_id.get() or not ety_password.get():
            return messagebox.showerror('Erreur', 'Il manque une valeur !')
        else:
            # Vérification des identifiants élève dans la base de données
            try:
                connection = sqlite3.connect("data/db/freshdata.db")
                cursor = connection.cursor()
                cursor.execute('SELECT identite, classe FROM authentification WHERE identite = ? AND naissance = ?', 
                              (ety_id.get(), str(ety_password.get())))
                resultats = cursor.fetchall()
                connection.close()
            except:
                return messagebox.showerror('Erreur', 'Erreur de connexion à la base de données')
            
            # Si les données d'authentification récupérée sont vide cela renvoie un message d'erreur
            if resultats == []:
                return messagebox.showerror('Erreur', 'Identifiant ou mot de passe incorrects')
            else:
                # Enregistrement des informations de connexion
                fichierSauvegarde = open("data/db/userConnect.txt", "a", encoding="utf-8")
                fichierSauvegarde.write(resultats[0][0])
                fichierSauvegarde.write(';')
                fichierSauvegarde.write(resultats[0][1])
                fichierSauvegarde.close()
                
                # Ferme la page de connexion et lance l'application principale
                pageConnexion.destroy()
                os.system('python "sources//application.py"')

# ====== CRÉATION DE L'INTERFACE GRAPHIQUE ======
# Configuration de la fenêtre principale
pageConnexion = tk.Tk()
pageConnexion.title("Menu Connexion")
pageConnexion.geometry("350x300")

# Label connexion
lb_connexion = Label(pageConnexion, text="Connexion", font=("Arial", 20))
lb_connexion.pack()

# Champ identifiant
lb_id = Label(pageConnexion, text="Identifiant")
lb_id.pack()
ety_id = Entry(pageConnexion)
ety_id.pack()

# Champ mot de passe
lb_password = Label(pageConnexion, text="Mot de passe")
lb_password.pack()
ety_password = Entry(pageConnexion)
ety_password.pack()

# Bouton de validation
btn_validate = Button(pageConnexion, text="Valider", command=connexion)
btn_validate.pack()

# Chargement et affichage du logo
image_path = "data/image/LEA.jpg"
image = Image.open(image_path)
photo = ImageTk.PhotoImage(image)
lb_image = ttk.Label(pageConnexion, image=photo)
lb_image.image = photo  # Garde une référence pour éviter la suppression par le garbage collector
lb_image.pack()

# Empêche le redimensionnement de la fenêtre
pageConnexion.resizable(False, False)

# Lancement de l'application
pageConnexion.mainloop()