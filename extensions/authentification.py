from flask_login import LoginManager
from models import User
from extensions.sqlalchemy import db

# Instanciation de l'extension Flask-Login
login_manager=LoginManager()


#obligatoire pour que Flask-Login sache appeler la fonction
@login_manager.user_loader
#retrouver un utiisateur à partir de son id stocké en session
def load_user(user_id):
    return db.session.get(User,int(user_id))