from flask import Flask, flash, redirect, request, url_for
from flask_login import LoginManager
from flask_migrate import Migrate
from config import config
from app.models import db

login_manager = LoginManager()
migrate = Migrate()

def create_app(config_name='development'):
    """
    Application factory
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    migrate.init_app(app, db)
    
    # Import models
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        flash('Silakan login terlebih dahulu', 'danger')
        if request.path.startswith('/admin'):
            return redirect(url_for('admin.admin_login', next=request.url))
        return redirect(url_for('auth.login', next=request.url))
    
    # Register blueprints
    from app.routes import home_bp, auth_bp, dashboard_bp, course_bp, admin_bp
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(admin_bp)
    
    return app
