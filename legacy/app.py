import os
import flask.json
from flask import Flask, render_template, request, redirect, url_for, flash, session
try:
    from flask.json import JSONEncoder
except ImportError:
    import json
    class JSONEncoder(json.JSONEncoder):
        pass
    flask.json.JSONEncoder = JSONEncoder

# Deep Monkeypatch for flask-mongoengine + Flask 3.0
import flask_mongoengine.json
flask_mongoengine.json.override_json_encoder = lambda app: None

from flask_mongoengine import MongoEngine
from flask_login import LoginManager, login_required
from models import db
from dotenv import load_dotenv

load_dotenv(override=True)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'won-solutions-secret-123')
    
    # MongoDB Configuration
    mongodb_uri = os.getenv('MONGODB_URI')
    if not mongodb_uri:
        app.logger.error("MONGODB_URI not found in environment!")
        # Fallback logic if needed, but for now we expect it
    
    app.config['MONGODB_SETTINGS'] = {
        'host': mongodb_uri
    }

    # Manual MongoDB Connection to bypass broken init_app in flask-mongoengine + Flask 3.0
    from mongoengine import connect
    connect(host=mongodb_uri)
    # db.init_app(app)  <-- This is what crashes with Flask 3.0

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        try:
            return User.objects(pk=user_id).first()
        except:
            return None

    # Global context for settings
    @app.context_processor
    def inject_settings():
        from models import CompanyMaster
        try:
            settings = CompanyMaster.objects().first()
        except Exception:
            settings = None
        return dict(system_settings=settings)

    # Register Blueprints
    from routes.auth import auth as auth_blueprint
    from routes.inventory import inventory as inventory_blueprint
    from routes.pos import pos_bp as pos_blueprint
    from routes.reports import reports as reports_blueprint
    from routes.crm import crm as crm_blueprint
    from routes.settings import settings_bp as settings_blueprint
    from routes.financials import financials as financials_blueprint
    from routes.backup import backup_bp as backup_blueprint
    from routes.compliance import compliance_bp as compliance_blueprint
    
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(inventory_blueprint)
    app.register_blueprint(pos_blueprint)
    app.register_blueprint(reports_blueprint)
    app.register_blueprint(crm_blueprint)
    app.register_blueprint(settings_blueprint)
    app.register_blueprint(financials_blueprint)
    app.register_blueprint(backup_blueprint)
    app.register_blueprint(compliance_blueprint)

    from datetime import datetime

    @app.route('/')
    @login_required
    def index():
        from models import Sale, Expense, Product
        from datetime import date, datetime as dt
        
        today_start = dt.combine(date.today(), dt.min.time())
        today_end = dt.combine(date.today(), dt.max.time())
        
        # MongoDB aggregation or simple sum
        sales_today = sum(s.total_amount for s in Sale.objects(created_at__gte=today_start, created_at__lte=today_end))
        expenses_today = sum(e.amount for e in Expense.objects(created_at__gte=today_start, created_at__lte=today_end))
        
        # Low stock count
        low_stock_count = Product.objects(stock_qty__lte=0).count() # Placeholder logic, will refine
        
        recent_sales = Sale.objects().order_by('-created_at').limit(5)
        
        return render_template('dashboard.html', 
                               now=datetime.now(),
                               sales_today=sales_today,
                               expenses_today=expenses_today,
                               low_stock_count=low_stock_count,
                               recent_sales=recent_sales)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
