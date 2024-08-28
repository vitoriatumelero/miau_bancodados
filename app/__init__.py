from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY'] = 'uma_chave_secreta_bem_segura'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager(app)
    login_manager.login_view = 'main.login'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import Perfil  # Importação dentro da função para evitar ciclo
        return Perfil.query.get(int(user_id))

    from app.routes import main  # Importação após a criação do `app`
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app
