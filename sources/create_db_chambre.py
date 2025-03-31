import sqlite3
#fonction qui permet de creer la table chambre dans la base de données
def creer():
    connection = sqlite3.connect("data/db/freshdata.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS chambre(date DATETIME NOT NULL,numero_chambre TEXT NOT NULL, temperature FLOAT NOT NULL, prenom TEXT NOT NULL, classe TEXT NOT NULL)")
    connection.commit()
    connection.close()

creer()