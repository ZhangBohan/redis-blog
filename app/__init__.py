from config import config
from flask import Flask
from redis import StrictRedis

redis = StrictRedis(decode_responses=True)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # init here
    redis = StrictRedis(host='localhost', port=6379, db=0)

    # BluePrint

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .blog import blog as blog_blueprint
    app.register_blueprint(blog_blueprint, url_prefix='/blog')
    return app
