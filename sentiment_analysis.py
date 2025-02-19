from mistralai import Mistral
import sqlite3
import os
import random
import dotenv
import time
import re

# Charger la clé API depuis un fichier .env 
dotenv.load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")

# Initialiser le client Mistral
client = Mistral(api_key=api_key)

# Connexion à la base de données SQLite
db_path = "tables_test.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Vérifier que la table avis_clients existe (sinon, la créer)
cursor.execute("""
CREATE TABLE IF NOT EXISTS avis_clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_commande INTEGER,
    numero_client INTEGER,
    commentaire TEXT,
    categorie TEXT
)
""")
conn.commit()

# Générer des commentaires avec OpenAI et les stocker en BDD
nb_commentaires = 5  # Nombre de commentaires à générer
dataset = []

model = "mistral-large-latest"

for _ in range(nb_commentaires):
    numero_commande = random.randint(100000, 999999)
    numero_client = random.randint(10000, 99999)

    prompt = """
    Tu es une boutique spécialisée en rénovation de l'habitat.
    Un client partage son avis après avoir été livré suite à sa commande.

    **Objectif** : 
    - Génère **un seul** commentaire client concis (3 phrases maximum).
    - Identifie **le probléme lié à la livraison du colis: livreur irrespectueux, service client absent,..etc**.
    - Fournis une **catégorie précise** qui **décrit le sujet principal** du commentaire. 

    **Format attendu** (ne génère qu’un seul commentaire) :
    - **Commentaire** : "Texte très court (moins de 15 mots)"
    - **Catégorie** : "Sujet principal en 3 mots maximum" 

    Exemple attendu :
    **Commentaire** : "2 colis sur 5 reçus."
    - **Catégorie** : "Colis manquants"
    """

    try:
        print("Envoi de la requête à Mistral...")
        
        response = client.chat.complete(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        print(f"Réponse reçue : {response}")

        content = response.choices[0].message.content if hasattr(response, "choices") and response.choices else ""
        print(f"********Contenu extrait : {content}")

        # Extraction avec regex
       
        matches = re.findall(r'\*\*Commentaire\*\*\s*:\s*"([^"]+)"\s*[-•]\s*\*\*Catégorie\*\*\s*:\s*"([^"]+)"', content, re.DOTALL)

        print(f"Matches trouvés: {matches}")

        if matches:
            for commentaire, categorie in matches:
                dataset.append((numero_commande, numero_client, commentaire, categorie))
        else:
            print("Format de réponse inattendu !")

        # Pause pour éviter l'erreur 429
        time.sleep(2)

    except Exception as e:
        print(f"⚠️Erreur lors de l'appel MistralAI : {e}")

# Insérer les commentaires générés dans la BDD
if dataset:
    print(f"DONNEES INSEREES DANS LA BDD: {dataset}")
    cursor.executemany("INSERT INTO avis_clients (numero_commande, numero_client, commentaire, categorie) VALUES (?, ?, ?, ?)", dataset)
    conn.commit()
    print(f"{len(dataset)} avis clients générés et stockés dans '{db_path}'")
else:
    print("Aucun avis généré, rien à stocker.")

# Fermer la connexion proprement
conn.commit()
conn.close()
print("Connexion SQLite fermée.")
