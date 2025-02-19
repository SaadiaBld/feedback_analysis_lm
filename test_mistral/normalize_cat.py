#les commentaires ont été générés et stockés en BDD avec mistral, on va maintenant les analyser pour en extraire les catégories
#on va utiliser la vectorisation pour regrouper les commentaires en catégories similaires 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import sqlite3

db_path = "tables_test.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Récupérer toutes les catégories uniques
cursor.execute("SELECT DISTINCT categorie FROM avis_clients")
categories_brutes = [row[0] for row in cursor.fetchall()]

print("Catégories trouvées :", categories_brutes)

conn.close()

#vectorisation
vectorizer = TfidfVectorizer()

X=vectorizer.fit_transform(categories_brutes)
print(X)

#clustering avec kmeans sur les catégories des commentaires clients 
n_clusters = 9
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X)

#affichage des clusters et des catégories associées 
cluster_mapping = {categories_brutes[i]: clusters[i] for i in range(len(categories_brutes))}

for cat, cluster in cluster_mapping.items():
    print(f"Catégorie : {cat} -> Cluster : {cluster}")
                   
#le clustering a permis de regrouper les catégories similaires en clusters mais il y a des incohérences dans les catégories ex: cluster 0 contient des catégories différentes livraison brutale et livraison en retard
# qui sont deux categories distinctes avec n_clusters, et lorsqu'on diminue les clusters, on a aussi des incohérences
#l’algorithme regroupe les catégories en fonction de leur similarité vectorielle, mais il peut ne pas comprendre les nuances de sens.
