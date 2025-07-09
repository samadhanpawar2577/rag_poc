import os

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
        host = os.getenv("DATABRICKS_HOST", "https://dbc-5a435f58-327e.cloud.databricks.com").strip()
        if not host.startswith("https://"):
            host = "https://" + host
        return host

# ---------------------------------------
# 🔑 Auth + Index details
# ---------------------------------------
host = get_workspace_url()
pat_token = os.getenv("DATABRICKS_TOKEN", " ")

index_name = "rag-files.rag-files-schema.docs_idx"
VECTOR_SEARCH_ENDPOINT_NAME = "rag_vector_endpoint"

# ---------------------------------------
# 🧠 LangChain + Vector Search setup
# ---------------------------------------
from databricks.vector_search.client import VectorSearchClient
from langchain_community.vectorstores import DatabricksVectorSearch
from langchain_community.embeddings import DatabricksEmbeddings

embedding_model = DatabricksEmbeddings(endpoint="databricks-gte-large-en")

import os
from databricks.sdk import WorkspaceClient
from databricks.vector_search.client import VectorSearchClient
from langchain_community.vectorstores import DatabricksVectorSearch
from langchain_community.embeddings import DatabricksEmbeddings

# Service Principal credentials
client_id = os.getenv("DATABRICKS_CLIENT_ID")
client_secret = os.getenv("DATABRICKS_CLIENT_SECRET")
host = get_workspace_url()

def get_retriever():
    # Create workspace client with service principal
    w = WorkspaceClient(
        host=host,
        client_id=client_id,
        client_secret=client_secret
    )
    
    # Use the workspace client's auth for vector search
    vsc = VectorSearchClient(workspace_client=w, disable_notice=True)
    
    vs_index = vsc.get_index(
        endpoint_name=VECTOR_SEARCH_ENDPOINT_NAME,
        index_name=index_name
    )
    vectorstore = DatabricksVectorSearch(vs_index, text_column="text", embedding=embedding_model)
    
    return vectorstore.as_retriever()