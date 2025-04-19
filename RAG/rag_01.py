# from langchain_community.document_loaders import PyPDFLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from pathlib import Path
# from langchain_openai import OpenAIEmbeddings
# from openai import api_key
# from langchain_qdrant import QdrantVectorStore

# pdf_path = Path(__file__).parent / "communication.pdf"

# loader = PyPDFLoader(file_path=pdf_path)

# # create a list of pages
# docs = loader.load()

# # splitters
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# split_docs = text_splitter.split_documents(documents= docs)

# # embedder
# embedding = OpenAIEmbeddings(model="text-embedding-3-large")
# api_key = "api key here "

# # vector_store = QdrantVectorStore.from_documents(
# #     documents=[],
# #     collection_name="rag",
# #     embedding=embedding,
# #     url="http://localhost:6333"
# # )

# # vector_store.add_documents(documents=split_docs)
# # print('Injection done ')

# # retiver
# retriver = QdrantVectorStore.from_existing_collection(
#     collection_name="rag",
#     embedding=embedding,
#     url="http://localhost:6333"
# )

# relevant_chunk =  retriver.similarity_search(
#     query = "what is Assignment 2 about which is Written Group Report ?"
# )

# SYSTEM_PROMPT = """ You are an helpful AI Assistant who responds basis on the available context.
# Context: {relevant_chunk}
# """
# # print("DOCS",len(docs))
# # print("SPLIT_DOCS",len(split_docs))
# # print(docs[15])

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv

# Load environment variables (store API keys safely)
load_dotenv()

pdf_path = Path(__file__).parent / "communication.pdf"

# Load PDF
loader = PyPDFLoader(file_path=str(pdf_path))
docs = loader.load()

# Split text
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
split_docs = text_splitter.split_documents(documents=docs)

# Initialize embeddings
embedding = OpenAIEmbeddings(model="text-embedding-3-large")

# Initialize Qdrant (uncomment to store documents)
vector_store = QdrantVectorStore.from_documents(
    documents=split_docs,
    collection_name="rag",
    embedding=embedding,
    url="http://localhost:6333"
)
print("Documents injected into Qdrant.")

# Retriever
retriever = QdrantVectorStore.from_existing_collection(
    collection_name="rag",
    embedding=embedding,
    url="http://localhost:6333"
)

# Search
query = "Explain the Group Report assignment in BUS709"
relevant_chunks = retriever.similarity_search(query=query, k=3)  # Get top 3 chunks

for chunk in relevant_chunks:
    print(f"Page: {chunk.metadata['page'] + 1}")  # PDF pages are 0-indexed
    print(chunk.page_content)
    print("---")