# import de la bibliotheque Flask et des fonctions utilitaires
import json
from extensions.sqlalchemy import db
from extensions.migrations import migrate
from extensions.authentification import login_manager
from flask import Flask
from auth.routes import bp as auth_bp
from projects.routes import bp as project_bp
from flask import Flask, render_template

# définition de l'instance de l'application
app=Flask(__name__)
# configuration de l'application à partir du fichier config.json
app.config.from_file("config.json",load=json.load)
# initialisation de l'extension SQLAlchemy
db.init_app(app)
# initialisation de l'extension Flask-Migrate
migrate.init_app(app,db)
# initialisation de l'extension Flask-Login
login_manager.init_app(app)
# Configuration de la route par défaut pour la page de connexion
login_manager.login_view="auth.login"
login_manager.login_message="veuillez vous conecter"
# Connecter les blueprints des différents modules à l'instance de l'app
app.register_blueprint(auth_bp)
app.register_blueprint(project_bp)

@app.errorhandler(403)
def forbidden(error):
    return render_template("erreur403.html"), 403


@app.errorhandler(404)
def not_found(error):
    return render_template("erreur404.html"), 404
