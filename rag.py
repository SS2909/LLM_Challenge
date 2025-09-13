import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

CHROMA_DIR = os.getenv('CHROMA_DIR', './chroma_db')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def get_vectorstore():
    embed = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=embed)
    return vectordb

def query_rag(query: str, k: int = 4) -> str:
    vectordb = get_vectorstore()
    docs = vectordb.similarity_search(query, k=k)
    context = '\n\n'.join([d.page_content for d in docs])
    prompt = f"Use the following context to answer the question. If the answer isn't in the context, say you don't know.\n\nContext:\n{context}\n\nQuestion: {query}\nAnswer:"

    import openai
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model='gpt-4o-mini',
        messages=[{'role':'system','content':'You are an assistant that answers using only provided context.'},
                  {'role':'user','content':prompt}],
        max_tokens=512,
        temperature=0.0
    )
    return response['choices'][0]['message']['content']
