from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from sqlalchemy import select

from extensions.sqlalchemy import db
from models import Project, Statut
from forms import ProjectForm

bp = Blueprint("projects", __name__, url_prefix="/projects")

#ce que le dashboard affiche
@bp.route("/dashboard")
@login_required
def dashboard():
    #projet de utilisateur connecter

    stmt = select(Project).where(Project.user_id == current_user.id).order_by(Project.created_at.desc())
    projets = db.session.execute(stmt).scalars().all()

    total = len(projets)
    counts = {s.value: 0 for s in Statut}
    for projet in projets:
        counts[projet.status.value] += 1

    return render_template("dashboard.html", projets=projets, total=total, counts=counts)

#creation d'un nouveaux projet 
@bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    form = ProjectForm()
    if form.validate_on_submit():
        projet = Project(
            title=form.title.data,
            description=form.description.data,
            domain=form.domain.data,
            status=Statut[form.status.data],
            user_id=current_user.id,
        )
        db.session.add(projet)
        db.session.commit()
        flash("Projet créé avec succès.", "success")
        return redirect(url_for("projects.dashboard"))

    return render_template("project_form.html", form=form, titre_page="Nouveau projet")


def verifier_propriete(project_id):
    projet = db.session.get(Project, project_id)
    if projet is None:
        abort(404)
    if projet.user_id != current_user.id:
        #interdire acces
        abort(403)
    return projet


@bp.route("/<int:project_id>/modifier", methods=["GET", "POST"])
@login_required
def modifier(project_id):
    projet = verifier_propriete(project_id)
    form = ProjectForm(obj=projet, status=projet.status.name)

    if form.validate_on_submit():
        projet.title = form.title.data
        projet.description = form.description.data
        projet.domain = form.domain.data
        projet.status = Statut[form.status.data]
        db.session.commit()
        flash("Projet mis à jour.", "success")
        return redirect(url_for("projects.dashboard"))

    return render_template("project_form.html", form=form, titre_page="Modifier le projet")


@bp.route("/<int:project_id>/delete", methods=["POST"])
@login_required
def delete(project_id):
    projet = verifier_propriete(project_id)
    db.session.delete(projet)
    db.session.commit()
    flash("Projet supprimé.", "info")
    return redirect(url_for("projects.dashboard"))