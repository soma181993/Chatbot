# Chatbot
README description you can use for your HR Assistant project 👇

🤖 HR Assistant

HR Assistant is an intelligent chatbot built with Python Flask, BERT-based Transformers, and a Streamlit frontend. It helps employees interact with HR services such as leave applications, policy queries, and payroll-related questions. The backend stores data in a lightweight JSON database for easy extensibility.

🚀 Features

Conversational AI powered by BERT / Sentence Transformers for semantic matching.

Preprocessing with tokenization, lemmatization, and similarity checks for accurate responses.

Flask API backend that handles queries and returns context-aware responses.

Streamlit frontend providing a user-friendly chat interface.

JSON-based database to manage users, intents, and conversation history without needing SQL.

Self-learning mode: If no response is found, the assistant stores the query for future training.

🛠️ Tech Stack

Frontend: Streamlit

Backend: Flask (REST API)

AI/ML: BERT Tokenizer, Sentence Transformers (all-MiniLM-L6-v2)

NLP: NLTK for preprocessing (tokenization & lemmatization)

Database: JSON files (hr_assistant_dataset.json, add_data.json)

📂 Project Structure
├── app.py                # Flask backend
├── frontend.py           # Streamlit frontend
├── hr_assistant_dataset.json   # Base HR intents and responses
├── add_data.json         # User-specific intents and conversation logs
├── requirements.txt      # Dependencies
└── README.md             # Project documentation

⚙️ How It Works

User sends a query from Streamlit UI.

Query is sent to Flask API (/get_response).

Text is preprocessed (lowercased + lemmatized).

Assistant searches for matching intent in base dataset or user-added dataset.

If a match is found → return response.

If not found → save query in add_data.json for admin training.

📦 Installation & Setup

Clone the repo:

git clone https://github.com/your-repo/hr-assistant.git
cd hr-assistant


Create and activate virtual environment:

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows


Install dependencies:

pip install -r requirements.txt


Run the Flask backend:

python app.py


Run the Streamlit frontend:

streamlit run frontend.py


Open http://localhost:8501
 to chat with HR Assistant.

✅ Example Queries

"I want to apply for leave"

"What is the HR policy on work from home?"

"How can I check my payroll?"

🔮 Future Improvements

Add authentication and user profiles.

Store data in SQLite / PostgreSQL instead of JSON.

Integrate approval workflows (e.g., leave approval by managers).

Deploy on cloud (AWS / Azure / GCP).
