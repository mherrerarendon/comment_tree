from flask import Flask

from ct import db

def create_app():
    app = Flask(__name__)
    config_app(app)
    setup_db(app)
    register_blueprints(app)
    return app

def setup_db(app):
    # these settings should not be configurable in the config file so we
    # set them after loading the config file
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
    db.init_app(app)

def config_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

def register_blueprints(app):
    from ct.blueprints import threads
    from ct.blueprints import notifications
    app.register_blueprint(threads.bp)
    app.register_blueprint(notifications.bp)
