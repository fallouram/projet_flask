from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from models import Statut

class LoginForm(FlaskForm):
    identifiant = StringField("Email ou nom d'utilisateur", validators=[DataRequired()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("Se connecter")


class RegistrationForm(FlaskForm):  
    username = StringField("Nom d'utilisateur", validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Mot de passe", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirmer le mot de passe",
        validators=[DataRequired(), EqualTo("password", message="Les mots de passe ne correspondent pas.")]
    )
    submit = SubmitField("Créer mon compte")




class ProjectForm(FlaskForm):
    title = StringField("Titre", validators=[DataRequired(), Length(max=150)])
    domain = StringField("Domaine", validators=[DataRequired(), Length(max=100)])
    description = TextAreaField("Description", validators=[DataRequired()])
    status = SelectField(
        "Statut",
        choices=[(s.name, s.value) for s in Statut],
        validators=[DataRequired()]
    )
    submit = SubmitField("Enregistrer")