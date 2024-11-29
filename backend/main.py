from flask import Flask, request, session
from flask_session import Session
from flask_socketio import SocketIO, emit
from flask_cors import CORS

from src.LanguageModel import OllamaClient
from src.RAGModel import initialize_db

import os
import os
from dotenv import load_dotenv
import logging

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")
app.config['SESSION_TYPE'] = 'filesystem'
llm_client = OllamaClient(initialize_db())
CORS(app, resources={r"/*": {"origins": "*"}})

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format='%(asctime)s - %(levelname)s - %(message)s',  # Set the format for log messages
    handlers=[
        logging.FileHandler("./backend_app.log"),  # Log to a file with the desired name
        logging.StreamHandler()  # Also log to console
    ]
)

Session(app)

socket = SocketIO(
    app=app, 
    manage_session=False, 
    cors_allowed_origins="*", 
    async_handlers=True, 
    async_mode="threading" # enables multithreading to prevent llm queries from blocking. 
)

@app.route("/", methods=["POST"])
async def home(): 
    if request.method == "POST":
        jurisdictions = list(map(lambda jurisdiction: jurisdiction.replace("_", " "), request.args.getlist("jurisdictions")))
        jurisdictions_room_addr = "chat_room_" + "".join(request.args.getlist("jurisdictions"))
        session[jurisdictions_room_addr] = {"jurisdictions": jurisdictions, "messages": []}
    return f"<p>Hello, World!</p>"

@socket.on("query_llm")
def handle_query(data): 
    try:
        response = llm_client.inquire_on_jurisdictions(data["jurisdiction"], data["prompt"])
        emit("llm_response", response) # emit the llm's response to the client. 
    except Exception as e:
        logging.error(f"Error in async_query: {str(e)}")
        emit("error", {"error": str(e)}) # emit an error to the client's side. 
    
if __name__ == "__main__":
    socket.run(app, port=8000, debug=True)
