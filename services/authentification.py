

from flask_login import login_user,logout_user
from sqlalchemy import select,or_
from extensions.sqlalchemy import db

from helper.exceptions import UtilisateurIntrouvable , MotDePassIncorrect,MdpEmailEXIST
from models import User


class AuthentificationService:

    @classmethod
  
    def connect_user(cls,identifiant,password):
    
# identifiant : peut être un email OU un username#

        stmt=select(User).where(
        or_(User.email ==identifiant, User.username ==identifiant)
    )
        user_in_database = db.session.execute(stmt).scalar_one_or_none()

        if not user_in_database:
            raise UtilisateurIntrouvable("Aucun utilisateur avec cet identifiant")

        if not user_in_database.check_password(password):
            raise MotDePassIncorrect("Mot de passe incorrect")

        login_user(user_in_database)


#inscrire une nouveau etudiant
    @classmethod
    def register_user(cls,username,email,password):
        stmt=select(User).where(
            or_(User.email==email , User.username==username)
        )
        register_in_user=db.session.execute(stmt).scalar_one_or_none()
        
        if register_in_user :
            raise MdpEmailEXIST("cette cette Etudiant existe deja")
        
        user=User(username=username , email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

#deconnect un utilisateur
    @classmethod
    def deconnect_user(cls):
       logout_user()
