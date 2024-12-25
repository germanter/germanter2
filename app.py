from flask import Flask,render_template,jsonify
from database import load_data,load_item  
import random
import datetime
                
app = Flask(__name__)

def set_reservation():
    tomorrow=datetime.datetime.now() + datetime.timedelta(days=1)
    tomorrow=tomorrow.strftime("%Y-%m-%d")
    times=['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00']
    time=random.choice(times)
    return [tomorrow,time]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/market')
def market():
    data = load_data()
    return render_template('market.html',data=data)

@app.route('/market/<id>')
def show_item(id):
    data = load_item(id)
    return render_template('show_item.html',data=data)

@app.route('/market/<id>/reservation')
def reservation(id):
    data = load_item(id)
    timeset= set_reservation()
    return render_template('reservation.html',data=data,timeset=timeset)

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(
        host = '0.0.0.0',
        debug = True
    )