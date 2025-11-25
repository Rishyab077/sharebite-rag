

# ✅ Import necessary modules from LangChain
from langchain_community.embeddings import SentenceTransformerEmbeddings  # To convert text into vector embeddings
from langchain_community.vectorstores import FAISS  # To store and search embeddings efficiently

# ✅ Step 1: Load text data from a file
# This file contains information about the ShareBite platform
with open("sharebite_info.txt", "r", encoding="utf-8") as f:
    text = f.read()

# ✅ Step 2: Create embeddings for the text
# Embeddings are numerical representations of text for semantic search
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# ✅ Step 3: Create a FAISS vector store using the embeddings
# This allows us to quickly search and retrieve similar text
db = FAISS.from_texts([text], embeddings)

# ✅ Step 4: Save the vector store locally for later use
db.save_local("vectorStore")

# ✅ Confirmation message
print("✅ VectorStore created successfully!")
