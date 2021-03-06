from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_mail import Mail
from flask_migrate import Migrate
import app.flask_whooshalchemy as w
from flask_cors import CORS


db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    CORS(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)


    from app.models import Project
    w.whoosh_index(app, Project)

    from app.models import User
    w.whoosh_index(app, User)
    #import and register blueprints here
    from app.api import api
    app.register_blueprint(api, url_prefix='/v1')
    
    from app.api import apib
    app.register_blueprint(apib)

    return app

from app.models import User,Project

