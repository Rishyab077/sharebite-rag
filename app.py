from flask import Flask
from rag_api import app as rag_app  # Import your Flask app from rag_api.py

app = rag_app  # Use your RAG API Flask app

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Use Render's dynamic port
    app.run(host="0.0.0.0", port=port)
