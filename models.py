from datetime import datetime, timezone
from typing import List

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum as SqlEnum
from extensions.sqlalchemy import db


import enum

class Statut(enum.Enum):
    EN_ATTENTE = "En attente"
    EN_COURS = "En cours"
    TERMINE = "Terminé"





class User(UserMixin,db.Model):
    __tablename__='user'
    id:Mapped[int]=mapped_column(primary_key=True)
    username:Mapped[str]=mapped_column(String(100),unique=True)
    email:Mapped[str]=mapped_column(String(100),unique=True)
    password_hash:Mapped[str]=mapped_column(String(300))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    projects:Mapped[List["Project"]]=db.relationship(back_populates="user")


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Project(db.Model):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(Text)
    domain: Mapped[str] = mapped_column(String(100))
    status: Mapped[Statut] = mapped_column(SqlEnum(Statut), default=Statut.EN_ATTENTE)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = db.relationship(back_populates="projects")