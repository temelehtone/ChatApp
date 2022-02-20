from flask import Flask, render_template, session, url_for, request, redirect, jsonify, flash
from client import Client
from threading import Thread
from datetime import datetime
import time


NAME_KEY = 'name'
CL = 'client'

app = Flask(__name__)
app.secret_key = "helloimteuvo"

clients = []
messages = []

def disconnect():
    global clients
    for client in clients:
        if (session[NAME_KEY] == client.name):
            
            client.disconnect()
            clients.remove(client)
            

@app.route("/login", methods=["POST", "GET"])
def login():
    
    if request.method == "POST":
        for client in clients:
            if request.form["inputName"] == client.name:
                flash("Name already in use!", "info")
                return redirect(url_for("login"))
        session[NAME_KEY] = request.form["inputName"]
        
        return redirect(url_for("home"))
    return render_template("login.html", **{"session": session})


@app.route("/logout")
def logout():
    
    if NAME_KEY in session:
        disconnect()
        session.pop(NAME_KEY, None)
        flash("You have been logged out!", "info")
        
    return redirect(url_for("login"))
    


@app.route("/")
@app.route("/home")
def home():
    global clients
    if NAME_KEY not in session:
        return redirect(url_for("login"))
    
    for c in clients:
        if session[NAME_KEY] == c.name:
            return render_template("index.html", **{"login":True, "session": session})
    client = Client(session[NAME_KEY])
    
    clients.append(client)
    return render_template("index.html", **{"login":True, "session": session})

@app.route("/send_message", methods=["GET"])
def send():
    
    global clients

    msg = request.args.get("val")
    
    for client in clients:
        if (session[NAME_KEY] == client.name):
            client.send_message(msg)
    return "none"

@app.route("/get_messages")
def get_messages():
    return jsonify({"messages": messages})

   
def update_messages():
    global messages
    global clients
    while True:
        time.sleep(0.2) # Update every 200ms
        new_messages = []
        for client in clients:
            new_messages = client.get_messages()
        messages.extend(new_messages) # get any new messages from client 

        
        for msg in new_messages: 
            if msg == "{quit}":
                break


if __name__ == "__main__":
    Thread(target=update_messages).start()
    app.run(debug=True, host="86.50.97.197")
     