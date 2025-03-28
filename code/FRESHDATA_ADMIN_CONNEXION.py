#Ce programme est appelée par FRESHDATA_MONITOR
import tkinter as tk
from tkinter import messagebox


prof_id = "admin"
prof_password = "1234"

def verifier_identifiants():
    """
    Vérifie les identifiants de connexion administrateur.
    
    Compare les identifiants entrés avec les identifiants admin prédéfinis.
    Si la vérification réussit, ferme la fenêtre de connexion.
    Sinon, affiche un message d'erreur.
    """
    prof_id_verif = ety_id.get()
    prof_password_verif = ety_password.get()

    if prof_id_verif == prof_id and prof_password_verif == prof_password:
        root.destroy()
    else:
        messagebox.showerror("Erreur", "Identifiant ou mot de passe incorrect")

# Configuration de la fenêtre principale
root = tk.Tk()
root.title("Connexion Administrateur")
root.geometry("400x300")

# Création des éléments de l'interface
lb_id = tk.Label(root, text="Identifiant :")
lb_id.pack(pady=5)

ety_id = tk.Entry(root)
ety_id.pack(pady=5)

lb_password = tk.Label(root, text="Mot de passe :")
lb_password.pack(pady=5)

ety_password = tk.Entry(root, show="*")
ety_password.pack(pady=5)

btn_connect = tk.Button(root, text="Se connecter", command=verifier_identifiants)
btn_connect.pack(pady=20)

# Lancement de l'application
root.mainloop()