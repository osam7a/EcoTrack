from flask import Flask, render_template, redirect, request
from flask_cors import CORS
from datetime import datetime
from .utils import log
from calendar import month_name

app = Flask(__name__)
CORS(app)

info = {
    "name": "John Doe",
    "district": "Ajman",
    "data": {
        "labels": ["January", "", "February", "", "March", "", "April", "", "May", "", "June", "", "July", "", "August", "", "September", "", "October", "", "November", "", "December"],
        "data": [800, 835, 815, 865, 855, 862, 880, 918, 910, 930, 920, 942, 955, 950, 940, 1218, 1255, 1280, 1260, 1295, 1380, 1375, 1355, 1390],
        "events": {
            "January " + str(datetime.now().year): [],
            "February " + str(datetime.now().year): [],
            "March " + str(datetime.now().year): [],
            "April " + str(datetime.now().year): [("New TV", (3,5))],
            "May " + str(datetime.now().year): [],
            "June " + str(datetime.now().year): [],
            "July " + str(datetime.now().year): [],
            "August " + str(datetime.now().year): [("New AC", (850, 1200))],
            "September " + str(datetime.now().year): [],
            "October " + str(datetime.now().year): [],
            "November " + str(datetime.now().year): [("New Fridge", (65, 79))],
            "December " + str(datetime.now().year): []
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

@app.post('/log_event')
async def log_event():
    data = request.json
    print(data)
    event = data["event"]
    date = data["date"]
    log(f"EVENT LOG - {event} on {date}")
    date = month_name[datetime.strptime(date, "%Y-%m-%d").month] + " " + str(datetime.strptime(date, "%Y-%m-%d").year)

    info["data"]["events"][date].append((event, (80,120)))
    return "300"

@app.post('/delete_event')
async def delete_event():
    data = request.json
    event = data["event"]
    
    for date in info["data"]["events"]:
        for e in info["data"]["events"][date]:
            if e[0] == event:
                info["data"]["events"][date].remove(e)
                return "300"
    return "404"