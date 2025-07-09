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
    # In Databricks App Services, DATABRICKS_HOST is automatically available
    host = os.getenv("DATABRICKS_HOST", "").strip()
    if not host:
        # Fallback to Spark detection for notebooks
        try:
            from pyspark.sql import SparkSession
            spark = SparkSession.builder.getOrCreate()
            return "https://" + spark.conf.get("spark.databricks.workspaceUrl")
        except Exception:
            raise Exception("❌ Unable to detect Databricks workspace URL")
    
    if not host.startswith("https://"):
        host = "https://" + host
    return host

# ---------------------------------------
# 🔑 OAuth Token using Service Principal
# ---------------------------------------
# Updated config.py with better error handling
import os
import requests
import streamlit as st

def get_oauth_token():
    client_id = os.getenv("DATABRICKS_CLIENT_ID")
    client_secret = os.getenv("DATABRICKS_CLIENT_SECRET")
    
    # Debug: Check if credentials are available
    st.write(f"Debug: Client ID present: {bool(client_id)}")
    st.write(f"Debug: Client Secret present: {bool(client_secret)}")
    
    if not all([client_id, client_secret]):
        raise Exception("❌ Missing DATABRICKS_CLIENT_ID or DATABRICKS_CLIENT_SECRET environment variables")

    host = get_workspace_url()
    token_url = f"{host}/oidc/token"
    
    st.write(f"Debug: Token URL: {token_url}")
    
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "all-apis"
    }

    try:
        response = requests.post(token_url, data=data)
        st.write(f"Debug: OAuth response status: {response.status_code}")
        st.write(f"Debug: OAuth response: {response.text}")
        
        if response.status_code != 200:
            raise Exception(f"❌ Failed to get OAuth token: {response.text}")
        
        return response.json()["access_token"]
    except Exception as e:
        st.error(f"OAuth request exception: {str(e)}")
        raise Exception(f"❌ OAuth token request failed: {str(e)}")

# ---------------------------------------
# 🌐 Configuration
# ---------------------------------------
host = get_workspace_url()
index_name = os.getenv("VECTOR_SEARCH_INDEX_NAME", "rag-files.rag-files-schema.docs_idx")
VECTOR_SEARCH_ENDPOINT_NAME = os.getenv("VECTOR_SEARCH_ENDPOINT_NAME", "rag_vector_endpoint")

# ---------------------------------------
# 🧠 LangChain + Vector Search setup
# ---------------------------------------
from databricks.vector_search.client import VectorSearchClient
from langchain_community.vectorstores import DatabricksVectorSearch
from langchain_community.embeddings import DatabricksEmbeddings

embedding_model = DatabricksEmbeddings(endpoint="databricks-gte-large-en")

def get_retriever():
    """Get the vector search retriever for RAG"""
    try:
        vsc = VectorSearchClient(
            workspace_url=host,
            personal_access_token=get_oauth_token(),  # OAuth token
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
    
    except Exception as e:
        raise Exception(f"❌ Failed to initialize retriever: {str(e)}")

# ---------------------------------------
# 🔧 Validation function
# ---------------------------------------
def validate_config():
    """Validate that all required configurations are available"""
    required_vars = [
        "DATABRICKS_CLIENT_ID",
        "DATABRICKS_CLIENT_SECRET"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise Exception(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
    
    # Test OAuth token
    try:
        token = get_oauth_token()
        if not token:
            raise Exception("❌ Failed to obtain OAuth token")
    except Exception as e:
        raise Exception(f"❌ OAuth configuration invalid: {str(e)}")
    
    return True