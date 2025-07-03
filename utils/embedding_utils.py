# from sentence_transformers import SentenceTransformer
# import numpy as np
# from config import EMBEDDING_MODEL

# model = SentenceTransformer(EMBEDDING_MODEL)

# _embeddings = []
# _chunks = []


# def get_embeddings(text):
#     return model.encode(text).tolist()

# def similarity_search(query):
#     query_emb = get_embeddings(query)
#     # You would replace this with a vector DB lookup using cosine similarity
#     # For now, use dummy top-k context
#     return "\n".join([chunk for chunk in _chunks[:3]])
