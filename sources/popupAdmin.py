"""
FRESHDATA ADMIN CONNEXION - Module d'authentification administrateur
===================================================================

Ce programme est appelé par main.py et permet de vérifier
les identifiants administrateur avant d'accéder aux menu admin.
"""

# ====== IMPORTATION DES BIBLIOTHÈQUES ======
import tkinter as tk                        # Interface graphique principale
from tkinter import messagebox              # Boîtes de dialogue

# ====== IDENTIFIANTS ADMINISTRATEUR ======
# Identifiants prédéfinis pour l'accès administrateur
prof_id = "admin"
prof_password = "1234"

def verifier_identifiants():
    """
    Vérifie les identifiants de connexion administrateur.
    
    Compare les identifiants entrés avec les identifiants admin prédéfinis.
    Si la vérification réussit, cela  ferme la fenêtre de connexion.
    Sinon, affiche un message d'erreur.
    """
    prof_id_verif = ety_id.get()
    prof_password_verif = ety_password.get()

    # Vérification des identifiants
    if prof_id_verif == prof_id and prof_password_verif == prof_password:
        root.destroy()  # Ferme la fenêtre si les identifiants sont corrects
    else:
        messagebox.showerror("Erreur", "Identifiant ou mot de passe incorrects")

# ====== CRÉATION DE L'INTERFACE GRAPHIQUE ======
# Configuration de la fenêtre principale
root = tk.Tk()
root.title("Connexion Administrateur")
root.geometry("400x300")

# Champ identifiant
lb_id = tk.Label(root, text="Identifiant :")
lb_id.pack(pady=5)

ety_id = tk.Entry(root)
ety_id.pack(pady=5)

# Champ mot de passe (masqué avec des *)
lb_password = tk.Label(root, text="Mot de passe :")
lb_password.pack(pady=5)

ety_password = tk.Entry(root, show="*")  # Le caractère "*" masque le mot de passe
ety_password.pack(pady=5)

# Bouton de connexion
btn_connect = tk.Button(root, text="Se connecter", command=verifier_identifiants)
btn_connect.pack(pady=20)

# ====== LANCEMENT DE L'APPLICATION ======
root.mainloop()