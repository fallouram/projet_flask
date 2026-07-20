from flask_migrate import Migrate
from .sqlalchemy import db


# instanciation de Flask-Migrate
migrate = Migrate(db)
