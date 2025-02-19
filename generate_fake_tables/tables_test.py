#SCRIPT POUR CREER TABLES FICTIVES

import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('/home/utilisateur/Documents/devia_2425/llm_poc/tables_test.db')
cursor = conn.cursor()

# Create table test
cursor.execute('''
CREATE TABLE IF NOT EXISTS test (
    numero_client INT,
    numero_commande VARCHAR(20),
    date_commande DATE,
    produit VARCHAR(100),
    type_produit VARCHAR(50),
    rayon_appartenance VARCHAR(50),
    montant_commande REAL,
    transporteur_btoc VARCHAR(50),
    date_prevue_livraison DATE,
    date_effective_livraison DATE,
    date_prise_en_charge_entrepot DATE,
    entrepot_expedition VARCHAR(50),
    type_livraison VARCHAR(50),
    tracking_etape VARCHAR(255),
    date_evenement_tracking TIMESTAMP
)
''')

# Create table avis_clients
cursor.execute('''
CREATE TABLE IF NOT EXISTS avis_clients (
    numero_commande VARCHAR(20),
    numero_client INT,
    note INT CHECK (note BETWEEN 1 AND 5),
    commentaire TEXT,
    categorie TEXT
)
''')
print("Tables created successfully")

# # Insert data into table test
# cursor.executemany('''
#                    INSERT INTO test VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', [
#     (1001, 'CMD001', '2024-02-01', 'Parquet chêne massif', 'Revêtement sol', 'Matériaux', 1200.50, 'DHL', '2024-02-05', '2024-02-06', '2024-02-02', 'Entrepôt Paris', 'Express', 'Colis expédié', '2024-02-02 14:30:00'),
#     (1002, 'CMD002', '2024-02-03', 'Peinture murale blanche', 'Peinture', 'Décoration', 85.90, 'UPS', '2024-02-08', '2024-02-08', '2024-02-04', 'Entrepôt Lyon', 'Standard', 'Colis en cours de livraison', '2024-02-08 09:00:00'),
#     (1003, 'CMD003', '2024-02-05', 'Porte en bois massif', 'Menuiserie', 'Construction', 850.00, 'Chronopost', '2024-02-10', '2024-02-14', '2024-02-06', 'Entrepôt Marseille', 'Express', 'Colis en retard', '2024-02-13 18:45:00'),
#     (1004, 'CMD004', '2024-02-07', 'Évier en inox', 'Plomberie', 'Cuisine', 199.99, 'FedEx', '2024-02-12', '2024-02-11', '2024-02-08', 'Entrepôt Lille', 'Standard', 'Colis livré', '2024-02-11 16:45:00'),
#     (1005, 'CMD005', '2024-02-09', 'Spot LED encastrable', 'Éclairage', 'Décoration', 249.99, 'DHL', '2024-02-14', None, '2024-02-10', 'Entrepôt Bordeaux', 'Express', 'Colis en attente de livraison', '2024-02-13 08:30:00'),
#     (1006, 'CMD006', '2024-02-10', 'Carrelage grès cérame', 'Revêtement sol', 'Matériaux', 149.99, 'Chronopost', '2024-02-14', '2024-02-15', '2024-02-11', 'Entrepôt Marseille', 'Express', 'Colis endommagé', '2024-02-15 10:30:00'),
#     (1007, 'CMD007', '2024-02-10', 'Radiateur électrique', 'Chauffage', 'Maison', 29.99, 'Chronopost', '2024-02-14', '2024-02-16', '2024-02-12', 'Entrepôt Marseille', 'Standard', 'Retard de livraison', '2024-02-16 12:00:00')])

# cursor.executemany('''
#                    INSERT INTO avis_clients VALUES (?,?,?,?)''', [
#                     ('CMD001', 1001, 5, 'Livraison rapide et produit conforme, très satisfait !'),
#                     ('CMD002', 1002, 4, 'Peinture de qualité, mais emballage légèrement endommagé.'),
#                     ('CMD004', 1004, 3, 'Évier conforme mais rayé à la réception.'),
#                     ('CMD005', 1005, 5, 'Très bon éclairage LED, service de livraison impeccable.'),
#                     ('CMD003', 1003, 2, 'Livraison très en retard, inacceptable !'),
#                     ('CMD006', 1006, 1, 'Carrelage arrivé cassé, très déçu !'),
#                     ('CMD007', 1007, 2, 'Livraison en retard, mauvaise expérience.')])





# Commit changes and close the connection
conn.commit()
conn.close()
print("données insérées avec succés")
