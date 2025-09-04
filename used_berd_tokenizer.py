from flask import Flask, request, jsonify
import json
import uuid
import os
from datetime import datetime
from transformers import BertTokenizer
from sentence_transformers import SentenceTransformer, util
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('wordnet')



app = Flask(__name__)

# Load tokenizer once
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = SentenceTransformer('all-MiniLM-L6-v2')
lemmatizer = WordNetLemmatizer()
# Base dataset
BASE_FILE = "hr_assistant_dataset.json"
def load_base_data():
    if not os.path.exists(BASE_FILE) or os.path.getsize(BASE_FILE) == 0:
        raise FileNotFoundError(f"{BASE_FILE} missing or empty")
    with open(BASE_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)["intents"]
        except json.JSONDecodeError:
            raise ValueError(f"{BASE_FILE} is corrupted, fix JSON formatting")

base_data = load_base_data()

# Additional dataset for new users & queries
ADD_FILE = "add_data.json"
if not os.path.exists(ADD_FILE) or os.path.getsize(ADD_FILE) == 0:
    with open(ADD_FILE, "w", encoding="utf-8") as f:
        json.dump({"users": [], "intents": [], "conversations": []}, f, indent=4)

def load_add_data():
    if not os.path.exists(ADD_FILE) or os.path.getsize(ADD_FILE) == 0:
        return {"users": [], "intents": [], "conversations": []}
    try:
        with open(ADD_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Reset if corrupted
        return {"users": [], "intents": [], "conversations": []}

def save_add_data(data):
    # Ensure structure is always complete
    if "users" not in data: data["users"] = []
    if "intents" not in data: data["intents"] = []
    if "conversations" not in data: data["conversations"] = []
    with open(ADD_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)



# Preprocessing: lowercase + lemmatize
def preprocess(text):
    tokens = word_tokenize(text.lower())
    lemmatized = [lemmatizer.lemmatize(tok) for tok in tokens]
    return ' '.join(lemmatized)



def find_response(input_text, intents):
    input_text = input_text.lower()
    # Direct tag match
    for intent in intents:
        if input_text == intent["tag"].lower():
            return intent["responses"]
    # Pattern match
    for intent in intents:
        for pattern in intent["patterns"]:
            if input_text == pattern.lower():
                # Optional: log tokens
                tokens = tokenizer.tokenize(pattern)
                input_ids = tokenizer.encode(pattern, add_special_tokens=True)
                print(f"Pattern: {pattern} → Tokens: {tokens} → IDs: {input_ids}")
                return intent["responses"]
    return None

@app.route("/get_response", methods=["POST"])
def get_response_route():
    data = request.get_json(force=True)

    input_text = data.get("input_text")
    if not input_text:
        return jsonify({"error": "Please provide 'input_text'."}), 400

    add_data = load_add_data()

    # Generate/reuse user_id
    user_id = data.get("user_id", str(uuid.uuid4()))

    # Ensure user exists
    user = next((u for u in add_data["users"] if u["user_id"] == user_id), None)
    if not user:
        add_data["users"].append({
            "user_id": user_id,
            "created_on": str(datetime.now())
        })

    # Search in datasets
    response = find_response(input_text, base_data) or \
               find_response(input_text, add_data["intents"])

    if not response:
        # Create new intent
        new_tag = str(uuid.uuid4())[:8]
        add_data["intents"].append({
            "tag": new_tag,
            "patterns": [input_text],
            "responses": ["Response not available yet. (Recorded for training)"],
            "created_by": user_id,
            "created_on": str(datetime.now())
        })
        save_add_data(add_data)
        return jsonify({
            "response": ["I don’t know that yet, but I’ve saved it for learning."],
            "new_intent": new_tag,
            "user_id": user_id
        })

    # Save conversation
    add_data.setdefault("conversations", [])
    add_data["conversations"].append({
        "user_id": user_id,
        "query": input_text,
        "response": response,
        "timestamp": str(datetime.now())
    })
    save_add_data(add_data)

    return jsonify({"response": response, "user_id": user_id})

if __name__ == "__main__":
    app.run(debug=True)
