from flask import Flask,render_template,jsonify
from database import load_data,load_item  
                
app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(
        host = '0.0.0.0',
        debug = True
    )