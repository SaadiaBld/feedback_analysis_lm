import streamlit as st
import sqlite3, dotenv
import os
import re, pandas as pd
from langchain_mistralai.chat_models import ChatMistralAI
from langchain.schema import HumanMessage


# Charger la clé API depuis un fichier .env 
dotenv.load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")

llm = ChatMistralAI(model="mistral-large-latest")

# Fonction pour nettoyer la requête SQL générée
def clean_sql_query(sql_query):
    return re.sub(r"```sql|```", "", sql_query).strip()

# Modèle de prompt pour générer la requête SQL
prompt_template = """
Tu es un assistant SQL. Convertis la question en requête SQL compatible avec SQLite.
Assure-toi que la requête est bien formatée et évite les erreurs.

### Question :
{user_question}

### Table 'avis_clients_new' :
- `numero_commande` (VARCHAR) → Identifiant unique de la commande associée à l'avis.
- `numero_client` (INT) → Identifiant du client.
- `note` (INT) → Ne pas utiliser ce champ.
- `commentaire` (TEXT) → Texte écrit par le client sur son expérience.
- `categorie` (TEXT) → Catégorie du commentaire.
- `sentiment` (TEXT) → Classification de l'avis. Valeurs possibles :
  - 'Positive'
  - 'Very Positive'
  - 'Negative'
  - 'Neutral'
- `probabilite` (REAL) → Score de classification du sentiment.

### Table 'commandes_clients' :
Cette table contient les informations sur les commandes passées par les clients.

- `numero_commande` (VARCHAR) → Identifiant unique de la commande.
- `type_produit` (TEXT) → Type de produit commandé.
- `rayon` (TEXT) → Catégorie du produit.
- `entrepot` (TEXT) → Nom de l'entrepôt d'expédition.
- `date_commande` (DATE) → Date à laquelle la commande a été passée.
- `date_promesse` (DATE) → Date de livraison prévue.
- `date_reelle_livraison` (DATE) → Date réelle de livraison.
- `transporteur` (TEXT) → Nom du transporteur ayant livré la commande.
- `type_messagerie` (TEXT) → Mode de livraison.
- `montant_commande` (REAL) → Montant total de la commande.
- `departement_client` (VARCHAR) → Département où réside le client.

**Consignes importantes :**
- **Un avis insatisfaisant correspond aux valeurs `sentiment IN ('Negative', 'Very Negative')`.**
- **Ne jamais utiliser des valeurs de champs non listées ci-dessus.**
- Génère uniquement la requête SQL, sans explication ni formatage supplémentaire.
"""

# Fonction pour générer la requête SQL depuis la question utilisateur
def generate_sql_query(user_question):
    prompt = prompt_template.format(user_question=user_question)
    response = llm.invoke([HumanMessage(content=prompt)])
    sql_query = clean_sql_query(response.content.strip())
    return sql_query

# Fonction pour exécuter la requête SQL sur la base SQLite
def execute_sql_query(sql_query):
    db_path = "../test_sentence_transformer/tables_test.db"  # Mets le bon chemin
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute(sql_query)
        result = cursor.fetchall()
        col_names = [description[0] for description in cursor.description]
        conn.close()

        df= pd.DataFrame(result, columns=col_names)
        return df
    
    except Exception as e:
        conn.close()
        return f"Erreur SQL : {e}"

# Interface utilisateur avec Streamlit
st.title("💬 test")

st.write("Posez une question et obtenez une réponse basée sur la base de données.")


user_question = st.text_input("Posez votre question ici", "")

if st.button("🔍 Analyser"):
    if user_question:
        sql_query = generate_sql_query(user_question)
        st.write("📝 **Requête SQL générée :**")
        st.code(sql_query, language="sql")

        sql_results = execute_sql_query(sql_query)

        if isinstance(sql_results, str):  # Si erreur SQL
            st.error(sql_results)
        else:
            if isinstance(sql_results, str):
                st.error(sql_results)
            else:
                st.write("📊 **Résultats :**")
                st.dataframe(sql_results)
                
 

