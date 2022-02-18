from flask import Flask, render_template, session, url_for, request, redirect, jsonify
from client import Client
from threading import Thread
from datetime import datetime

NAME_KEY = 'name'

app = Flask(__name__)
app.secret_key = "helloimteuvo"

client = None
messages = []

def disconnect():
    global client
    if client:
        client.disconnect()

@app.route("/login", methods=["POST", "GET"])
def login():
    disconnect()
    if request.method == "POST":
        session[NAME_KEY] = request.form["inputName"]
        
        return redirect(url_for("home"))
    return render_template("login.html", **{"session": session})


@app.route("/logout")
def logout():
    if NAME_KEY in session:
        
        session.pop(NAME_KEY, None)
        
    return redirect(url_for("login"))
    


@app.route("/")
@app.route("/home")
def home():
    global client
    if NAME_KEY not in session:
        return redirect(url_for("login"))
    
    
    client = Client(session[NAME_KEY])
    return render_template("index.html", **{"login":True, "session": session})

@app.route("/send_message", methods=["GET"])
def send():
    
    global client

    msg = request.args.get("val")
    if client:
        client.send_message(msg)
    return "none"

@app.route("/get_messages")
def get_messages():
    return jsonify({"messages": messages})

   
def update_messages():
    global messages
    while True:
        time.sleep(0.1) # Update every 100ms
        if not client: continue
        new_messages = client.get_messages() # get any new messages from client 
        for m in new_messages:
            m += f":{datetime.now().strftime('%H:%M:%S')}"
        messages.extend(new_messages) # add to local list of messages
        
        for msg in new_messages: 
            if msg == "{quit}":
                break


if __name__ == "__main__":
    Thread(target=update_messages).start()
    app.run(debug=True, host="86.50.97.197")
     