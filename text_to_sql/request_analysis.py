#une fois que les fausses tables sont crées, on peut commencer à construire un modele de nlp qui va
#analyser des requetes d'utilisateur pour les transformer en requetes sql
from langchain_mistralai.chat_models import ChatMistralAI
from langchain.schema import HumanMessage
import os, dotenv, sqlite3, re

# Charger la clé API depuis un fichier .env 
dotenv.load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")

# Initialiser Mistral AI
llm = ChatMistralAI(model="mistral-large-latest", api_key=api_key)

# Prompt pour guider Mistral à générer du SQL
prompt_template = """
Tu es un assistant SQL. Convertis la question en requête SQL compatible avec SQLite.
Assure-toi que la requête est bien formatée et évite les erreurs.

### Question :
{user_question}

### Table 'avis_clients_new' :
- numero_commande (VARCHAR)
- numero_client (INT)
- note (INT)
- commentaire (TEXT)
- categorie (TEXT)
- sentiment (TEXT)
- probabilite (REAL)

### Table 'commandes_clients' :
- numero_commande (VARCHAR)
- type_produit (TEXT)
- rayon (TEXT)
- entrepot (TEXT)
- date_commande (DATE)
- date_promesse (DATE)
- date_reelle_livraison (DATE)
- transporteur (TEXT)
- type_messagerie (TEXT)
- montant_commande (REAL)
- departement_client (VARCHAR)

Génère uniquement la requête SQL, sans explication ni formatage supplémentaire.
"""

def clean_sql_query(sql_query):
    """nettoyer la requet sql genereee par llm pour qu'elle soit utilisable par sqlite"""
    return re.sub(r"```sql|```", "", sql_query).strip()
    print('****', sql_query)

# Fonction pour générer une requête SQL à partir d'une question utilisateur
def generate_sql_query(user_question):
    prompt = prompt_template.format(user_question=user_question)
    response = llm.invoke([HumanMessage(content=prompt)])

    sql_query = response.content.strip()
    sql_query = clean_sql_query(sql_query)  # Suppression des balises Markdown
    return sql_query
    

# Connexion à SQLite
db_path = "../test_sentence_transformer/tables_test.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Fonction sécurisée pour exécuter une requête SQL
def execute_sql_query(sql_query):
    try:
        cursor.execute(sql_query)
        result = cursor.fetchall()
        return result
    except sqlite3.Error as e:
        return f"❌ Erreur SQL : {e}"

# Fonction pour convertir le résultat SQL en texte compréhensible
def format_sql_results(sql_results, user_question):
    if isinstance(sql_results, str) and sql_results.startswith("❌"):
        return sql_results  # Retourner directement l'erreur
    if not sql_results:
        return "Aucun résultat trouvé pour cette requête."
    
    # Demander à Mistral d’expliquer les résultats
    prompt = f"Explique les résultats suivants en réponse à la question '{user_question}' : {sql_results}"
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()

# 🔍 Tester avec une première question
question = "Quels sont les retards de livraison cette semaine ?"
sql_query = generate_sql_query(question)

print("\nRequête SQL générée :")
print(sql_query)

sql_results = execute_sql_query(sql_query)

print("\nRésultats :")
print(sql_results)

response_text = format_sql_results(sql_results, question)

print("\nRéponse en langage naturel :")
print(response_text)

# Interface interactive
while True:
    user_question = input("\n❓ Pose ta question (ou tape 'exit' pour quitter) : ")
    if user_question.lower() == "exit":
        break
    
    sql_query = generate_sql_query(user_question)
    sql_results = execute_sql_query(sql_query)
    response_text = format_sql_results(sql_results, user_question)
    
    print("\nRequête SQL générée :")
    print(sql_query)
    print("\nRésultats :")
    print(sql_results)
    print("\nRéponse :")
    print(response_text)

conn.close()