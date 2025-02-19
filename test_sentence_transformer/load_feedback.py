#TESTER L'EXTRACTION DES COMMENTAIRES CLIENTS DE LA BASE DE DONNÉES
import sqlite3
import pandas as pd

# Connexion à la base de données
db_path = "../test_mistral/tables_test_mistralai.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Récupérer les commentaires clients
cursor.execute("SELECT commentaire FROM avis_clients LIMIT 5 OFFSET 10 ")
commentaires = [row[0] for row in cursor.fetchall()]
print(type(commentaires))
print(commentaires[:5])  # Afficher quelques exemples
print("*****")
conn.close()

print(f"Nombre de commentaires récupérés : {len(commentaires)}")
print("Exemple de commentaires :", commentaires[:5])  # Afficher quelques exemples

#TRANSFORMER LES COMMENTAIRES EN VECTEURS
from sentence_transformers import SentenceTransformer

# Charger le modèle SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")

# Transformer les commentaires en vecteurs
embeddings = model.encode(commentaires)
print(embeddings.shape)  # Afficher la taille des vecteurs
for commentaire in commentaires[:5]:
    print('commentaire:', commentaire)
    print('embedding:', model.encode(commentaire))
    print("***")

#CALCULER LES SIMILARITÉS ENTRE LES COMMENTAIRES
similarities = model.similarity(embeddings, embeddings) #calculer les similarités de chaque commentaire avec les autres commentaires
for commentaire, similarity in zip(commentaires[:5], similarities[:5]):
    print('commentaire:', commentaire)
    print('similarités:', similarity)
    print("***")

#Il y a un souci comme on peut le voir dans l'output, des phrases identiques ont des similarités différentes, cf notion pour plus de détails