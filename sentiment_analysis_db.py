#ANALYSE DES SENTIMENTS SUR COMMENTAIRES DISPONIBLES DANS BDD

import sqlite3
from transformers import pipeline
import torch

# Charger le modèle de classification
pipe = pipeline("text-classification", model="tabularisai/multilingual-sentiment-analysis")

# Connexion à la base de données SQLite
db_path = "/home/utilisateur/Documents/devia_2425/llm_poc/test_mistral/tables_test_mistralai.db"  # Chemin de la base de données
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# ajouter les colonnes sentiment et score à la table avis_clients si elles n'existent pas
try:
    cursor.execute("ALTER TABLE avis_clients ADD COLUMN sentiment TEXT")
except sqlite3.OperationalError:
    pass

try:
    cursor.execute("ALTER TABLE avis_clients ADD COLUMN probabilite REAL")
except sqlite3.OperationalError:
    pass


# Récupérer les commentaires de la table 'avis_clients'
cursor.execute("SELECT commentaire FROM avis_clients")
commentaires = cursor.fetchall()  # Liste de tuples [(comment1,), (comment2,), ...]

#stocker les mise à jour
updates = []

# Traiter les commentaires
for commentaire_tuple in commentaires: #les commentaires sont exraits sous forme de tuples, on va les extraire pour les traiter, la methode pipe attend un string
    commentaire =commentaire_tuple[0]

    # Analyser le sentiment du commentaire
    result = pipe(commentaire)
    sentiment = result[0]['label']  # Le label du sentiment (ex: 'positive', 'negative', etc.)
    probabilite = result[0]['score']  # Score de confiance

    # Ajouter à la liste des mises à jour
    updates.append((sentiment, probabilite, commentaire))

# Appliquer toutes les mises à jour en une fois
cursor.executemany("UPDATE avis_clients SET sentiment = ?, probabilite = ? WHERE commentaire = ?", updates)

conn.commit()
conn.close()
print("Analyse des sentiments terminée. Verifier la table")
