from flask import Flask,render_template
from database import load_data     
                
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/market')
def market():
    data = load_data()
    return render_template('market.html',data=data)

if __name__ == '__main__':
    app.run(
        host = '0.0.0.0',
        debug = True
    )