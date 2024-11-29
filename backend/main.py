from flask import Flask, request, session
from flask_session import Session
from flask_socketio import join_room, leave_room, send, SocketIO, emit
from flask_cors import CORS

from src.LanguageModel import OllamaClient
from src.RAGModel import initialize_db

import os
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")
app.config['SESSION_TYPE'] = 'filesystem'
llm_client = OllamaClient(initialize_db())
CORS(app, resources={r"/*": {"origins": "*"}})

Session(app)
socket = SocketIO(app, manage_session=False, cors_allowed_origins="*", async_handlers=True, async_mode="threading")

@app.route("/", methods=["POST"])
async def home(): 
    if request.method == "POST":
        jurisdictions = list(map(lambda jurisdiction: jurisdiction.replace("_", " "), request.args.getlist("jurisdictions")))
        jurisdictions_room_addr = "chat_room_" + "".join(request.args.getlist("jurisdictions"))
        session[jurisdictions_room_addr] = {"jurisdictions": jurisdictions, "messages": []}
    return f"<p>Hello, World!</p>"

@socket.on("first_event")
def handle_first_event(data): 
    #print(data, "Here")
    response = llm_client.inquire_cities(data["jurisdiction"], data["prompt"])
    #print("Hi")
    socket.emit(event="first_event", data=response)
    #send(response)

if __name__ == "__main__":
    socket.run(app, port=8000, debug=True)
