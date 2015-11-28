from config import config
from flask import Flask


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .blog import blog as blog_blueprint
    app.register_blueprint(blog_blueprint, url_prefix='/blog')
    return app
