from flask import Flask, request, session
from flask_session import Session
from flask_socketio import join_room, leave_room, send, SocketIO

from src.LanguageModel import OllamaClient
from src.RAGModel import initialize_db

import os
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")
app.config['SESSION_TYPE'] = 'filesystem'
app.llm_client = OllamaClient(initialize_db())

Session(app)
socket = SocketIO(app, manage_session=False)

@app.route("/", methods=["POST"])
def home(): 
    if request.method == "POST":
        jurisdictions = list(map(lambda jurisdiction: jurisdiction.replace("_", " "), request.args.getlist("jurisdictions")))
        jurisdictions_room_addr = "chat_room_" + "".join(request.args.getlist("jurisdictions"))
        session[jurisdictions_room_addr] = {"jurisdictions": jurisdictions, "messages": []}
        print(jurisdictions_room_addr)
    return f"<p>Hello, World!</p>"


if __name__ == "__main__":
    socket.run(app, port=8000, debug=True)
