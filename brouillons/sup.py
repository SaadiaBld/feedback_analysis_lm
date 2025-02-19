#script pour copier données de table fictive avec nouvelle table car erreur de colonne dans la table originale 
# données utilisées pour le poc

import sqlite3

# Connexion à la base de données source (celle contenant 'avis_clients')
source_db_path = "/home/utilisateur/Documents/devia_2425/llm_poc/test_mistral/tables_test_mistralai.db"
source_conn = sqlite3.connect(source_db_path)
source_cursor = source_conn.cursor()

# Connexion à la base de données de destination (où tu veux copier les données)
dest_db_path = "/home/utilisateur/Documents/devia_2425/llm_poc/tables_test.db"
dest_conn = sqlite3.connect(dest_db_path)
dest_cursor = dest_conn.cursor()

# Création de la nouvelle table dans la base destination
dest_cursor.execute('''
    CREATE TABLE IF NOT EXISTS avis_clients_new (
        numero_commande VARCHAR(20),
        numero_client INT,
        note INT,
        commentaire TEXT,
        categorie TEXT,
        sentiment TEXT,
        probabilite REAL
    );
''')

# Récupération des données depuis la base source
source_cursor.execute("SELECT numero_commande, numero_client, note, commentaire, categorie, sentiment, probabilite FROM avis_clients;")
data = source_cursor.fetchall()  # Récupérer toutes les lignes

# Insérer les données dans la table de destination
dest_cursor.executemany('''
    INSERT INTO avis_clients_new (numero_commande, numero_client, note, commentaire, categorie, sentiment, probabilite)
    VALUES (?, ?, ?, ?, ?, ?, ?);
''', data)


# Commit et fermeture des connexions
dest_conn.commit()
source_conn.close()
dest_conn.close()



print("✅ Table copie créée avec succès et données transférées.")
