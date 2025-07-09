# services/rag_service.py
from config.config import get_retriever
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatDatabricks

TEMPLATE = """
You are a knowledgeable assistant helping to answer user questions based only on the provided context.

Instructions:
- Use only the information in the context below to answer the question.
- If the context does not contain enough information, reply with "The answer is not available in the provided context."
- Be concise and accurate in your response.
- Do not make assumptions or hallucinate information.

Context:
{context}

Question:
{question}

Answer:
"""

prompt = PromptTemplate(template=TEMPLATE, input_variables=["context", "question"])

chat_model = ChatDatabricks(endpoint="databricks-llama-4-maverick", max_tokens=200)

qa_chain = RetrievalQA.from_chain_type(
    llm=chat_model,
    chain_type="stuff",
    retriever=get_retriever(),
    chain_type_kwargs={"prompt": prompt}
)

def answer_question(query: str):
    return qa_chain.invoke({"query": query})
