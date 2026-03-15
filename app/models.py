from datetime import datetime
from . import db

class Boat(db.Model):
    __tablename__ = 'boats'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    boat_type = db.Column(db.String(50))
    displacement = db.Column(db.Float)  # Водоизмещение в тоннах
    build_date = db.Column(db.Date)      # Дата постройки

    # Связи
    trips = db.relationship('Trip', backref='boat', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Boat {self.name}>'

class FishSpecies(db.Model):
    __tablename__ = 'fish_species'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return self.name

class FishingGround(db.Model):
    __tablename__ = 'fishing_grounds'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    # Можно добавить координаты
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    depth = db.Column(db.Float, nullable=True)  # Средняя глубина

    def __repr__(self):
        return self.name

class Trip(db.Model):
    __tablename__ = 'trips'
    id = db.Column(db.Integer, primary_key=True)
    boat_id = db.Column(db.Integer, db.ForeignKey('boats.id'), nullable=False)
    departure_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=False)

    # Связи
    crew = db.relationship('CrewMember', backref='trip', lazy=True, cascade='all, delete-orphan')
    ground_visits = db.relationship('TripGround', backref='trip', lazy=True, cascade='all, delete-orphan')

    @property
    def total_catch(self):
        """Общий вес улова за рейс"""
        total = db.session.query(db.func.sum(Catch.weight))\
            .join(TripGround)\
            .filter(TripGround.trip_id == self.id).scalar()
        return total or 0

    def __repr__(self):
        return f'Trip {self.id} - {self.boat.name} ({self.departure_date.date()})'

class CrewMember(db.Model):
    __tablename__ = 'crew_members'
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.Text)
    position = db.Column(db.String(50))  # Должность

    def __repr__(self):
        return f'{self.full_name} - {self.position}'

class TripGround(db.Model):
    """Посещение банки во время рейса"""
    __tablename__ = 'trip_grounds'
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    ground_id = db.Column(db.Integer, db.ForeignKey('fishing_grounds.id'), nullable=False)
    arrival_date = db.Column(db.DateTime, nullable=False)
    departure_date = db.Column(db.DateTime, nullable=False)
    quality = db.Column(db.String(20))  # отличное, хорошее, плохое

    # Связи
    ground = db.relationship('FishingGround')
    catches = db.relationship('Catch', backref='visit', lazy=True, cascade='all, delete-orphan')

    @property
    def catch_by_species(self):
        """Улов по сортам за это посещение"""
        return {c.species.name: c.weight for c in self.catches}

    def __repr__(self):
        return f'{self.trip} at {self.ground}'

class Catch(db.Model):
    """Улов за время стоянки на банке по сортам"""
    __tablename__ = 'catches'
    id = db.Column(db.Integer, primary_key=True)
    trip_ground_id = db.Column(db.Integer, db.ForeignKey('trip_grounds.id'), nullable=False)
    fish_species_id = db.Column(db.Integer, db.ForeignKey('fish_species.id'), nullable=False)
    weight = db.Column(db.Float, nullable=False)  # Вес улова в кг

    # Связи
    species = db.relationship('FishSpecies')

    def __repr__(self):
        return f'{self.species.name}: {self.weight}kg'