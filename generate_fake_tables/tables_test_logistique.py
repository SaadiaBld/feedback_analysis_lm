import sqlite3
import random
from datetime import datetime, timedelta

# Connexion à la base de données
conn = sqlite3.connect("/home/utilisateur/Documents/devia_2425/llm_poc/test_sentence_transformer/tables_test.db")
cursor = conn.cursor()

# Création de la table commandes_clients
cursor.execute('''
    CREATE TABLE IF NOT EXISTS commandes_clients (
        numero_commande VARCHAR(20) PRIMARY KEY,
        type_produit TEXT,
        rayon TEXT,
        entrepot TEXT,
        date_commande DATE,
        date_promesse DATE,
        date_reelle_livraison DATE,
        transporteur TEXT,
        type_messagerie TEXT,
        montant_commande REAL,
        departement_client TEXT
    )
''')

# Données possibles
produits = ["Peinture", "Carrelage", "Outillage", "Sanitaire", "Électricité", "Menuiserie", "Revêtement sol", "Chauffage"]
rubriques = {"Peinture": "Décoration", "Carrelage": "Matériaux", "Outillage": "Outillage", "Sanitaire": "Plomberie", "Électricité": "Électricité", "Menuiserie": "Menuiserie", "Revêtement sol": "Sol", "Chauffage": "Chauffage"}
entrepots = ["Réau", "Oignies", "Dourges 1", "Dourges 2", "Valence", "Évry", "Loudéac"]
transporteurs = ["DHL", "Colissimo", "Geodis", "TNT", "UPS"]
types_messagerie = ["Express", "Colis standard", "XXL"]
departements = ["75", "77", "78", "91", "92", "93", "94", "95"]

# Numéros de commande fournis
numeros_commandes = [
    "945119", "585650", "776911", "956747", "541818", "427938", "906314", "906250", "980027", "911542", 
    "519143", "921692", "700116", "439897", "412942", "785838", "728875", "165855", "836731", "248827", 
    "722776", "386418", "203066", "433532", "266630", "967558", "724276", "973574", "982306", "633682", 
    "719938", "985817", "607526", "905138", "811271", "562929", "395302", "733953", "234274", "922992", 
    "621235", "557938", "890526", "457537", "159946", "365953", "641524", "272704", "373670", "476294", "757236"
]

# Génération de données avec des dates de livraison dans la même semaine
base_date = datetime(2025, 2, 10)  # Lundi de la semaine choisie

data = []
for num in numeros_commandes:
    produit = random.choice(produits)
    rayon = rubriques[produit]
    entrepot = random.choice(entrepots)
    date_commande = base_date - timedelta(days=random.randint(3, 10))  # Commande passée avant la semaine
    date_promesse = base_date + timedelta(days=random.randint(1, 3))  # Livraison prévue au début de la semaine
    date_reelle_livraison = base_date + timedelta(days=random.randint(3, 6))  # Livraison effective cette semaine
    transporteur = random.choice(transporteurs)
    type_messagerie = random.choice(types_messagerie)
    montant_commande = round(random.uniform(50, 2000), 2)
    departement_client = random.choice(departements)
    
    data.append((num, produit, rayon, entrepot, date_commande.strftime('%Y-%m-%d'),
                 date_promesse.strftime('%Y-%m-%d'), date_reelle_livraison.strftime('%Y-%m-%d'),
                 transporteur, type_messagerie, montant_commande, departement_client))

# Insertion dans la base de données
cursor.executemany('''
    INSERT INTO commandes_clients (numero_commande, type_produit, rayon, entrepot, date_commande, date_promesse, date_reelle_livraison, transporteur, type_messagerie, montant_commande, departement_client)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', data)

# Commit et fermeture
conn.commit()
conn.close()

print("Table commandes_clients créée et remplie avec succès !")
