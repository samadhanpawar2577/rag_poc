import os
import requests

# ---------------------------------------
# ✅ Load env vars if running locally
# ---------------------------------------
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Optional: only needed for local .env support

# ---------------------------------------
# ✅ Dynamically detect Databricks workspace URL
# ---------------------------------------
def get_workspace_url():
    try:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.getOrCreate()
        return "https://" + spark.conf.get("spark.databricks.workspaceUrl")
    except Exception:
        host = os.getenv("DATABRICKS_HOST", "").strip()
        if not host.startswith("https://"):
            host = "https://" + host
        return host

# ---------------------------------------
# 🔑 OAuth Token using Service Principal
# ---------------------------------------
def get_oauth_token():
    client_id = os.getenv("DATABRICKS_CLIENT_ID")
    client_secret = os.getenv("DATABRICKS_CLIENT_SECRET")
    if not all([client_id, client_secret]):
        raise Exception("❌ Missing DATABRICKS_CLIENT_ID or DATABRICKS_CLIENT_SECRET.")

    token_url = f"{host}/oidc/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "all-apis"
    }

    response = requests.post(token_url, data=data)
    if response.status_code != 200:
        raise Exception(f"❌ Failed to get token: {response.text}")
    
    return response.json()["access_token"]


# ---------------------------------------
# 🌐 Host + Index config
# ---------------------------------------
host = get_workspace_url()

index_name = "rag-files.rag-files-schema.docs_idx"
VECTOR_SEARCH_ENDPOINT_NAME = "rag_vector_endpoint"

# ---------------------------------------
# 🧠 LangChain + Vector Search setup
# ---------------------------------------
from databricks.vector_search.client import VectorSearchClient
from langchain_community.vectorstores import DatabricksVectorSearch
from langchain_community.embeddings import DatabricksEmbeddings

embedding_model = DatabricksEmbeddings(endpoint="databricks-gte-large-en")

def get_retriever():
    vsc = VectorSearchClient(
        workspace_url=host,
        personal_access_token=get_oauth_token(),  # ✅ Use OAuth token here
        disable_notice=True
    )
    vs_index = vsc.get_index(
        endpoint_name=VECTOR_SEARCH_ENDPOINT_NAME,
        index_name=index_name
    )
    vectorstore = DatabricksVectorSearch(
        vs_index,
        text_column="text",
        embedding=embedding_model
    )
    return vectorstore.as_retriever()
