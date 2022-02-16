from email import message
from flask import Flask, render_template, session, url_for, request, redirect
from client import Client

NAME_KEY = 'name'

app = Flask(__name__)
app.secret_key = "helloimteuvo"

@app.route("/login", methods=["POST", "GET"])
def login():
    session["messages"] = []
    if request.method == "POST":
        session[NAME_KEY] = request.form["inputName"]
        
        return redirect(url_for("home"))
    return render_template("login.html", **{"session": session})


@app.route("/logout")
def logout():
    #session.pop(NAME_KEY, None)
    return redirect(url_for("login"))


@app.route("/", methods=["POST", "GET"])
@app.route("/home", methods=["POST", "GET"])
def home():
    
    if NAME_KEY not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        session["messages"].extend(request.form["message"])



    return render_template("index.html", **{"login":True, "session": session, "messages": session["messages"]})

#@app.route("/add_msg", methods=["POST", "GET"])
# def run():
    
#         return render_template("index.html", **{"login":True, "session": session, "messages": session["messages"]})
    
#     return render_template("index.html", **{"login":True, "session": session, "messages": session["messages"]})


if __name__ == "__main__":
    app.run(debug=True)