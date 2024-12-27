from flask import Flask,render_template,jsonify,request,redirect,url_for,flash
from database import load_data,load_item,insert_application
import random
import datetime
from forms import signup as signupform
from flask_bcrypt import Bcrypt
                
app = Flask(__name__)
app.config['SECRET_KEY'] = '15546c327b3b7e35dbe0379cc9a745ad888fd86d4ebbbbae7694001ee85951e4'
bcrypt = Bcrypt(app)

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

@app.route('/signup',methods=['POST','GET'])
def signup():
    form = signupform()
    if form.validate_on_submit():
        data = [form.name.data,form.email.data,form.password1.data]
        pw_hash = bcrypt.generate_password_hash(data[2])
        if bcrypt.check_password_hash(pw_hash, data[2]):
            data[2] = pw_hash
            dupcheck = insert_application(data)
            if dupcheck != None:
                if 1062 in dupcheck:   ### brainstorm
                    flash('THIS EMAIL IS ALREADY USED!')
            else:
                flash('YOU HAVE SIGNED UP')
                return redirect(url_for("market"))
        else:
            print('FAILED SIGNUP ATTEMPT!')
        
    elif form.errors != {}:   ### excellence 
        for error in form.errors.values():
            for i in range(len(error)):
                if error[i] == 'Field must be equal to password1.':
                    error[i] = "Password confirmation does not match"
            
            for msg in error:
                flash(msg)
                
    return render_template('signup.html',form=form)

@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(
        host = '0.0.0.0',
        debug = True
    )