import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import FishSpecies, FishingGround, Boat

@pytest.fixture
def app():
    """Создает тестовое Flask приложение"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['LOGIN_DISABLED'] = True
    app.config['SERVER_NAME'] = 'localhost'
    app.config['APPLICATION_ROOT'] = '/'
    app.config['PREFERRED_URL_SCHEME'] = 'http'
    
    return app

@pytest.fixture
def client(app):
    """Тестовый клиент Flask"""
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            create_test_data()
        yield client
        with app.app_context():
            db.drop_all()

def create_test_data():
    """Создает тестовые данные в БД"""
    if FishSpecies.query.count() == 0:
        species = ['треска', 'минтай', 'сельдь', 'камбала']
        for s in species:
            db.session.add(FishSpecies(name=s))
    
    if FishingGround.query.count() == 0:
        grounds = [
            {'name': 'Северная банка', 'latitude': 60.5, 'longitude': 40.2},
            {'name': 'Южная отмель', 'latitude': 55.3, 'longitude': 38.7}
        ]
        for g in grounds:
            db.session.add(FishingGround(**g))
    
    db.session.commit()

@pytest.fixture
def sample_boat(client):
    """Создает тестовый катер"""
    response = client.post('/boats/add', data={
        'name': 'Морской волк',
        'boat_type': 'Траулер',
        'displacement': 250.5,
        'build_date': '2020-03-15'
    }, follow_redirects=True)
    
    if response.status_code == 200:
        boat = Boat.query.filter_by(name='Морской волк').first()
        return {'id': boat.id} if boat else None
    return None

@pytest.fixture
def sample_ground(client):
    """Создает тестовую банку"""
    response = client.post('/grounds/add', data={
        'name': 'Медвежья банка',
        'latitude': 56.5,
        'longitude': 42.3,
        'depth': 120
    }, follow_redirects=True)
    
    if response.status_code == 200:
        ground = FishingGround.query.filter_by(name='Медвежья банка').first()
        return {'id': ground.id} if ground else None
    return None

@pytest.fixture
def sample_trip(client, sample_boat):
    """Создает тестовый рейс"""
    if not sample_boat:
        return None
    
    response = client.post('/trips/add', data={
        'boat_id': sample_boat['id'],
        'departure_date': '2025-03-01T10:00',
        'return_date': '2025-03-10T18:00',
        'crew-0-full_name': 'Иван Петров',
        'crew-0-position': 'капитан',
        'crew-0-address': 'ул. Морская 1',
        'crew-1-full_name': 'Петр Сидоров',
        'crew-1-position': 'боцман',
        'crew-1-address': 'ул. Рыбацкая 5'
    }, follow_redirects=True)
    
    if response.status_code == 200:
        from app.models import Trip
        trip = Trip.query.filter_by(boat_id=sample_boat['id']).first()
        return {'id': trip.id} if trip else None
    return None

@pytest.fixture(autouse=True)
def _push_request_context(app):
    """Принудительно создаёт контекст запроса"""
    ctx = app.test_request_context()
    ctx.push()
    yield
    ctx.pop()