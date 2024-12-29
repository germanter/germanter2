from dotenv import load_dotenv
import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

### secure
load_dotenv() 

#app sys          
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('key')
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from application import routes

