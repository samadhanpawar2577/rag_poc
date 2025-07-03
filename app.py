import streamlit as st
from utils.file_utils import upload_to_unity_catalog
# from utils.db_utils import insert_file_metadata, insert_page_text, insert_chunk
# from utils.text_utils import extract_text_by_page
# from utils.chunking_utils import chunk_text
# from utils.embedding_utils import get_embeddings, similarity_search
# from utils.inference_utils import get_llm_response
import uuid

st.title("RAG Pipeline on Databricks")

uploaded_files = st.file_uploader("Upload File(s)", accept_multiple_files=True, type=["pdf", "txt"])
query = st.text_input("Ask a question about the uploaded files")

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_id, stored_path = upload_to_unity_catalog(uploaded_file)
        # insert_file_metadata(file_id, stored_path)
        
        # pages = extract_text_by_page(uploaded_file)
        # for page_id, text in enumerate(pages):
        #     insert_page_text(file_id, page_id, text)
        #     chunks = chunk_text(text)
        #     for chunk_id, chunk in enumerate(chunks):
        #         emb = get_embeddings(chunk)
        #         insert_chunk(file_id, page_id, chunk_id, chunk, emb)
        st.write("File uploaded and processed successfully. You can now ask questions about the content.")      

# if query:
#     context = similarity_search(query)
#     result = get_llm_response(query, context)
#     st.write("\n### Answer")
#     st.write(result)