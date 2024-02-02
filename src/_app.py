from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
from .utils import log

app = Flask(__name__)
CORS(app)

info = {
    "name": "John Doe",
    "district": "Ajman",
    "data": {
        "labels": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        "data": [650, 700, 600, 800, 1000, 1100, 1200, 1050, 1000, 1100, 1575, 1620],
        "events": {
            "January": None,
            "February": None,
            "March": None,
            "April": "New TV",
            "May": None,
            "June": None,
            "July": None,
            "August": None,
            "September": None,
            "October": None,
            "November": "New Fridge",
            "December": None
        }
    }
}

def authorize(hid, pswd):
    if hid == "admin" and pswd == "admin":
        return True
    return False

@app.route('/')
async def login():
    err = request.args.get('err')
    if err == "302":
        return render_template('login.html', error="Invalid credentials, please try again.")
    return render_template('login.html')

@app.route('/main', methods=['POST'])
async def main():
    data = (request.get_data()).decode().split("&")
    hID = data[0].split("=")[1]
    hPW = data[1].split("=")[1]
    log(f"ATTEMPT LOGIN - ID: {hID}, PW: {hPW}")
    if not authorize(hID, hPW):
        return redirect('/?err=302', code=302)
    return render_template('main.html', user_info=info, labels=info["data"]["labels"], data=info["data"]["data"], events=info["data"]["events"])
