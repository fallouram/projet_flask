from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from forms import LoginForm, RegistrationForm
from services.authentification import AuthentificationService
from helper.exceptions import UtilisateurIntrouvable, MotDePassIncorrect, MdpEmailEXIST

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("projects.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        try:
            AuthentificationService.connect_user(form.identifiant.data, form.password.data)
            flash("Connexion réussie.", "success")
            return redirect(url_for("projects.dashboard"))
        except UtilisateurIntrouvable:
            flash("Aucun utilisateur avec cet identifiant.", "danger")
        except MotDePassIncorrect:
            flash("Mot de passe incorrect.", "danger")

    return render_template("login.html", form=form)


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("projects.dashboard"))

    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            AuthentificationService.register_user(form.username.data, form.email.data, form.password.data)
            flash("Compte créé avec succès, vous pouvez vous connecter.", "success")
            return redirect(url_for("auth.login"))
        except MdpEmailEXIST:
            flash("Ce nom d'utilisateur ou cet email est déjà utilisé.", "danger")

    return render_template("register.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    AuthentificationService.deconnect_user()
    flash("Vous avez été déconnecté.", "info")
    return redirect(url_for("auth.login"))