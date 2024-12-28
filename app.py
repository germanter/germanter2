from flask import Flask,render_template,jsonify,redirect,url_for,flash,request
from database import load_data,load_item,insert_user,get_user_with_email,get_user_with_id,insert_res
import random
import datetime
from forms import signup as signupform
from forms import login as loginform
from flask_bcrypt import Bcrypt,check_password_hash
from flask_login import LoginManager,login_user,login_required,UserMixin,current_user,logout_user
from dotenv import load_dotenv
import os

### secure
load_dotenv() 

#app sys          
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('key')
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

#login sys
@login_manager.user_loader
def load_user(user_id):
    attempted_user = get_user_with_id(user_id)
    user = User(
        attempted_user['id'],
        attempted_user['name'],
        attempted_user['email']
        )
    return user

class User(UserMixin):
    def __init__(self,id,name,email):
        self.id=id
        self.name=name
        self.email = email

#market logic
def set_reservation():
    tomorrow=datetime.datetime.now() + datetime.timedelta(days=1)
    tomorrow=tomorrow.strftime("%Y-%m-%d")
    times=['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00']
    time=random.choice(times)
    return [tomorrow,time]

#routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/market')
@login_required
def market():
    print(current_user.is_authenticated)
    data = load_data()
    return render_template('market.html',data=data)


x = False

@app.route('/market/<id>')
def show_item(id):
    data = load_item(id)
    return render_template('show_item.html',data=data)


@app.route('/market/<id>/reservation',)
def reservation(id):
    data = load_item(id)
    dupcheck = insert_res(current_user.id,id)
    print(dupcheck)
    if dupcheck !=None:
        if 1062 == dupcheck[0]:
            flash('You have already made a reservation for this car')
            return redirect(url_for('show_item',id=id))
        else:
            flash('Something went wrong')
            return redirect(url_for('show_item',id=id))

    else:
        timeset= set_reservation()
        return render_template(
            'reservation.html',
            data=data,
            timeset=timeset)
            
@app.route('/signup',methods=['POST','GET'])

def signup():
    form = signupform()
    if form.errors:
        print(form.errors)
    if form.validate_on_submit():
        data = [form.name.data,form.email.data,form.password1.data]
        pw_hash = bcrypt.generate_password_hash(data[2])
        try:
            data[2] = pw_hash
            dupcheck = insert_user(data)
            if dupcheck != None:
                if 1062 in dupcheck:   ### brainstorm
                    flash('This email is already used!')
            else:
                user_data = get_user_with_email(data[1])
                user_join = User(user_data['id'],user_data['name'],user_data['email'])
                login_user(user_join)
                flash('You have signed up')
                return redirect(url_for("market"))
        except:
            print('FAILED SIGNUP ATTEMPT!')
        
    elif form.errors != {}:   ### excellence 
        for error in form.errors.values():
            for i in range(len(error)):
                if error[i] == 'Field must be equal to password1.':
                    error[i] = "Password confirmation does not match"
            
            for msg in error:
                flash(msg)
                
    return render_template('signup.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form = loginform()
    if form.validate_on_submit():
        attempted_user = [form.email.data,form.password.data]
        user_data = get_user_with_email(attempted_user[0])
        if user_data != None:
            if check_password_hash(user_data['password'],attempted_user[1]):
                user_attempt = User(user_data['id'], user_data['name'], user_data['email'])
                login_user(user_attempt)
                name = user_data['name']
                flash(f'You logged in as {name}')
                return redirect(url_for('market'))
            else:
                flash('Account not found!')
        else:
            flash('Account not found!')

    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have logged out')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(
        host = '0.0.0.0',
        # debug = True  ### deactivate on push
    )