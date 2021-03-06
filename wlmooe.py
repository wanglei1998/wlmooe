from flask import Flask
from apps.cms.views import bp as cms_bp
from apps.front.views import bp as front_bp
from apps.common.views import bp as common_bp
from apps.ueditor import bp as ueditor_bp
from exts import db,mail
import config
from flask_wtf import CSRFProtect

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(cms_bp)
    app.register_blueprint(front_bp)
    app.register_blueprint(common_bp)
    app.register_blueprint(ueditor_bp)
    # 将db注册到app中
    db.init_app(app)
    mail.init_app(app)
    CSRFProtect(app)
    return app




if __name__ == '__main__':
    app = create_app()
    app.run(port=5000)
