from flask import Flask, request, session
from flask_session import Session
from flask_socketio import join_room, leave_room, send, SocketIO

import os
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
socket = SocketIO(app, manage_session=False)

@app.route("/", methods=["POST"])
def home(): 
    if request.method == "POST":
        jurisdictions = request.args.getlist("jurisdictions")
        print(jurisdictions)
    return f"<p>Hello, World!</p>"


if __name__ == "__main__":
    socket.run(app, port=8000, debug=True)
    session["chatbox-jurisdiction-topics"] = []
