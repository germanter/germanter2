from flask_login import login_user,UserMixin
from application.database import get_user_with_id
from application import login_manager
import random,datetime
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

def set_reservation():
    tomorrow=datetime.datetime.now() + datetime.timedelta(days=1)
    tomorrow=tomorrow.strftime("%Y-%m-%d")
    times=['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00']
    time=random.choice(times)
    return [tomorrow,time]