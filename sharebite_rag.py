# ✅ Import the function to get answers from the RAG engine
from rag_engine import get_answer

# === Simple console loop to ask ShareBite AI questions ===
while True:
    # Ask user to input a question
    query = input("Ask ShareBite AI: ")

    # Exit the loop if user types "exit" or "quit"
    if query.lower() in ["exit", "quit"]:
        break

    # Get AI-generated answer from RAG engine
    answer = get_answer(query)

    # Display the AI answer in the console
    print("🤖", answer)
