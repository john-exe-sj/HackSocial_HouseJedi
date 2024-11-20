from flask import Flask
from src.LanguageModel import OllamaClient
from src.RAGModel import split_documents, get_embedding_model, get_relevant_documents, is_directory_empty, initialize_db

app = Flask(__name__)
llm_client = OllamaClient()
db = initialize_db()

@app.route("/")
def hello(): 
    return "<p>Hello, World!</p>"

if __name__ == "__main__": 
    app.run(debug=True, port=8000)
