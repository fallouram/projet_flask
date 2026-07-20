from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# db ne veut pas dire "base de données" mais c'est une instance de SQLAlchemy
db = SQLAlchemy(model_class=Base)