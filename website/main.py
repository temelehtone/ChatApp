from flask import Flask, render_template, session, url_for, request, redirect, jsonify, flash
from client import Client
from threading import Thread
import time
from flask_sqlalchemy import SQLAlchemy




NAME_KEY = 'name'

app = Flask(__name__)
app.secret_key = "helloimteuvo"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app) # Database

class Messages(db.Model): # Table for database
    _id = db.Column("id", db.Integer, primary_key=True)
    message = db.Column(db.String(150))

    def __init__(self, msg):
        self.message = msg    

all_messages = Messages.query.all()
messages = [msg.message for msg in all_messages]

clients = []

def disconnect(): # Disconnects client
    global clients
    for client in clients:
        if (session[NAME_KEY] == client.name):
            
            client.disconnect()
            clients.remove(client) # Removes client from list
            # Appends the left message to global messages
            message = f"SERVER:{session[NAME_KEY]} has left the chat...:{time.strftime('%H:%M:%S')}"
            messages.append(message)
            
            

@app.route("/login", methods=["POST", "GET"])
def login():
    # Handles the login
    if request.method == "POST": # Takes the client name from frontend
        for client in clients:
            if request.form["inputName"] == client.name:
                flash("Name already in use!", "info")
                return redirect(url_for("login"))
        session[NAME_KEY] = request.form["inputName"]
        
        return redirect(url_for("home")) # Redirects client to chat page
    return render_template("login.html", **{"session": session})


@app.route("/logout")
def logout():
    # Handles the logout
    if NAME_KEY in session:
        disconnect()
        session.pop(NAME_KEY, None)
        flash("You have been logged out!", "info")
        
    return redirect(url_for("login"))
    


@app.route("/")
@app.route("/home")
def home():
    # Chat page
    global clients
    if NAME_KEY not in session:
        return redirect(url_for("login"))
    
    for c in clients:
        if session[NAME_KEY] == c.name:
            return render_template("index.html", **{"login":True, "session": session})
    client = Client(session[NAME_KEY])
    
    clients.append(client) # Appends client to the global client list
    return render_template("index.html", **{"login":True, "session": session})

@app.route("/send_message", methods=["GET"])
def send():
    # Takes messages from frontend and sends them to server
    global clients

    msg = request.args.get("val")
    
    for client in clients:
        if session[NAME_KEY] == client.name:
            client.send_message(msg)
    return "none"

@app.route("/get_messages")
def get_messages():
    # Sends the messages and session name to the frontend
    return jsonify({"messages": messages, "name":session[NAME_KEY]})

   
def update_messages():
    # Gets any new messages from server
    global clients
    global messages
    while True:
        time.sleep(0.2) # Update every 200ms
        new_messages = []
        for client in clients: # get any new messages from client
            new_messages = client.get_messages()
            
        messages.extend(new_messages)       
        for msg in new_messages:
            if msg == "{quit}":
                break
            if msg[0:6] != "SERVER":
                # Adds the new messages to the database
                db.session.add(Messages(msg))
                db.session.commit()


if __name__ == "__main__":
    
    Thread(target=update_messages).start() # Starts thread that updates messages constantly from server
    app.run()
     