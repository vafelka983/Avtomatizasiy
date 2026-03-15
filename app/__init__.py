from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        from . import routes, models
        db.create_all()
        
        # Создаем начальные данные, если БД пустая
        if models.FishSpecies.query.count() == 0:
            create_initial_data()
    
    return app

def create_initial_data():
    """Создание начальных данных для тестирования"""
    from .models import FishSpecies, FishingGround
    
    # Добавляем сорта рыбы
    species_list = ['Треска', 'Камбала', 'Сельдь', 'Мойва', 'Пикша', 'Окунь']
    for sp in species_list:
        db.session.add(FishSpecies(name=sp))
    
    # Добавляем тестовые банки
    grounds = ['Северная банка', 'Южная банка', 'Восточная отмель', 'Западный склон']
    for gr in grounds:
        db.session.add(FishingGround(name=gr))
    
    db.session.commit()