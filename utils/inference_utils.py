# import requests
# from config import DATABRICKS_ENDPOINT_URL, DATABRICKS_TOKEN

# def get_llm_response(query, context):
#     payload = {
#         "inputs": f"Context: {context}\n\nQuestion: {query}\nAnswer:",
#     }
#     headers = {
#         "Authorization": f"Bearer {DATABRICKS_TOKEN}",
#         "Content-Type": "application/json"
#     }
#     response = requests.post(DATABRICKS_ENDPOINT_URL, headers=headers, json=payload)
#     return response.json().get("result", "No answer found.")
