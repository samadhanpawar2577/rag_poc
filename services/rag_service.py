# services/rag_service.py
from config.config import get_retriever
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatDatabricks

TEMPLATE = """You are an assistant who is helping a user with their questions.
Use the following pieces of context to answer the question at the end:
{context}
Question: {question}
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
