from application import app
from flask import render_template,jsonify,redirect,url_for,flash
from application.database import load_data,load_item,insert_user,get_user_with_email,get_user_with_id,insert_res
from application.forms import signup as signupform
from application.forms import login as loginform
from flask_bcrypt import check_password_hash
from flask_login import login_user,login_required,current_user,logout_user
from application import bcrypt
from application.models import User,set_reservation


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
