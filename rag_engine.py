# ✅ Import necessary libraries
import os
from dotenv import load_dotenv  # For loading environment variables
from langchain_community.embeddings import SentenceTransformerEmbeddings  # For creating text embeddings
from langchain_community.vectorstores import FAISS  # For storing and searching embeddings
from langchain.text_splitter import CharacterTextSplitter  # To split large text into smaller chunks
from langchain.chains import RetrievalQA  # RAG chain for question answering
from langchain.llms import HuggingFacePipeline  # To use Hugging Face models as LLMs
from transformers import pipeline  # Hugging Face pipelines for model inference

# === Load environment variables ===
# Loads the .env file to get API tokens and other secrets
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
print("🔐 Loaded HF Token:", hf_token[:10], "...")  # Display first 10 characters for confirmation

# === Step 1: Create or Load Vector Store ===
def build_or_load_vectorstore():
    # Create embeddings object
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    if os.path.exists("vectorStore"):
        # ✅ If vector store already exists, load it
        print("✅ Loading existing vector store...")
        db = FAISS.load_local("vectorStore", embeddings, allow_dangerous_deserialization=True)
    else:
        # 🧠 If vector store doesn't exist, create from text file
        print("🧠 Creating new vector store from sharebite_info.txt...")
        with open("sharebite_info.txt", "r", encoding="utf-8") as f:
            text = f.read()

        # Split text into smaller chunks for better retrieval
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        texts = text_splitter.split_text(text)

        # Create FAISS vector store from text embeddings
        db = FAISS.from_texts(texts, embeddings)
        db.save_local("vectorStore")  # Save for future use
        print("✅ Vector store created and saved!")

    return db  # Return vector store object

# === Step 2: Load RAG Engine ===
def load_rag_engine():
    db = build_or_load_vectorstore()  # Load or build vector store
    # Create retriever to fetch top 3 similar chunks
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    return retriever

# === Step 3: Function to Get AI Answers ===
def get_answer(query):
    try:
        print("🔍 Inside get_answer()")
        print(f"Query: {query}")

        # ✅ Create embeddings (needed to load vector store)
        embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

        # ✅ Load existing vector store
        print("✅ Loading existing vector store...")
        vectorstore = FAISS.load_local("vectorStore", embeddings, allow_dangerous_deserialization=True)

        # ✅ Create retriever to fetch relevant text chunks
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

        # ✅ Initialize Hugging Face model (Flan-T5)
        print("🧩 Initializing Hugging Face model...")
        pipe = pipeline(
            "text2text-generation",
            model="google/flan-t5-large",
            tokenizer="google/flan-t5-large",
            max_length=512,
            temperature=0.3
        )
        model = HuggingFacePipeline(pipeline=pipe)

        # ✅ Create Retrieval-Augmented Generation (RAG) chain
        print("⚙️ Creating retrieval chain...")
        qa_chain = RetrievalQA.from_chain_type(
            llm=model,  # LLM to generate answers
            retriever=retriever,  # To fetch relevant chunks
            chain_type="stuff"  # Method to combine retrieved text
        )

        # ✅ Run the query through the RAG chain
        print("🚀 Running query through QA chain...")
        result = qa_chain.run(query)
        print("✅ Query executed successfully.")
        return result  # Return AI-generated answer

    except Exception as e:
        print(f"❌ Error inside get_answer(): {e}")
        return "Error while generating answer."

# === Step 4: Manual Test ===
if __name__ == "__main__":
    # Run a simple console test to ask questions
    while True:
        query = input("\nAsk me: ")
        if query.lower() in ["exit", "quit"]:
            break
        print(f"\n🤖 AI Assistant: {get_answer(query)}")
