# ✅ Import Flask for API creation
from flask import Flask, request, jsonify
# ✅ Import the RAG engine function that generates answers
from rag_engine import get_answer

# ✅ Initialize Flask app
app = Flask(__name__)

# ---------------------------
# ✅ API endpoint: /ask
# Users can send a question and get an AI-generated answer
# ---------------------------
@app.route("/ask", methods=["POST"])
def ask_question():
    try:
        # ✅ Get JSON data from request
        data = request.get_json(force=True)
        query = data.get("query", "").strip()  # Extract the query

        # ✅ Handle empty queries
        if not query:
            return jsonify({"error": "Missing query"}), 400

        # ✅ Log the user's query
        print(f"🧠 User Query: {query}")

        # ✅ Get AI answer using RAG engine
        answer = get_answer(query)

        # ✅ Log the AI answer
        print(f"💬 AI Answer: {answer}")

        # ✅ Send the answer back as JSON
        return jsonify({"answer": answer})

    except Exception as e:
        # ✅ Handle errors and return error message
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500


# ✅ Run the Flask app
# host="0.0.0.0" makes it accessible from other devices on the network
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
