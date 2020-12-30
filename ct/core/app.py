from flask import Flask

from ct import db

def create_app(app=None):
    # if not app:
    # app = Flask('ct')
    app = Flask(__name__)
    config_app(app)
    setup_db(app)
    # _register_blueprints(app)
    return app

def setup_db(app):
    # these settings should not be configurable in the config file so we
    # set them after loading the config file
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
    # ensure all models are imported even if not referenced from already-imported modules
    # import_all_models(app.import_name)
    db.init_app(app)

def config_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'