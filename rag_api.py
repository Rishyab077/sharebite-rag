from flask import Flask, request, jsonify
from rag_engine import get_answer

app = Flask(__name__)

# ------------------------------
#  POST /ask   → returns AI answer
# ------------------------------
@app.route("/ask", methods=["POST"])
def ask_question():
    try:
        data = request.get_json(force=True)
        query = data.get("query", "").strip()

        if not query:
            return jsonify({"error": "Missing query"}), 400

        print("🧠 User Query:", query)

        # Call your RAG engine
        answer = get_answer(query)

        print("💬 AI Answer:", answer)

        return jsonify({"answer": answer})

    except Exception as e:
        print("❌ Error in /ask:", e)
        return jsonify({"error": str(e)}), 500


# ------------------------------
#  Run API Server
# ------------------------------
if __name__ == "__main__":
    # Use port 8000 (since your Node backend is calling :8000)
    app.run(host="0.0.0.0", port=8000, debug=True)
