from flask import render_template, redirect, url_for, flash, request
from datetime import datetime
from sqlalchemy import func, desc, and_
from . import db
from .models import (Boat, FishSpecies, FishingGround, Trip, 
                     CrewMember, TripGround, Catch)
from .forms import (BoatForm, TripForm, FishingGroundForm, 
                    CatchForm, DateRangeForm, SpeciesGroundForm)
from flask import current_app as app

@app.route('/')
def index():
    """Главная страница"""
    boats_count = Boat.query.count()
    trips_count = Trip.query.count()
    grounds_count = FishingGround.query.count()
    species_count = FishSpecies.query.count()
    
    recent_trips = Trip.query.order_by(Trip.departure_date.desc()).limit(5).all()
    
    return render_template('index.html', 
                         boats_count=boats_count,
                         trips_count=trips_count,
                         grounds_count=grounds_count,
                         species_count=species_count,
                         recent_trips=recent_trips)

# ==================== Пункт 1: Уловы по катерам ====================
@app.route('/boats/catches')
def boats_catches():
    """Для каждого катера вывести даты выхода в море с указанием улова"""
    boats = Boat.query.all()
    result = []
    
    for boat in boats:
        trips_data = []
        for trip in boat.trips:
            # Суммируем вес всего улова за рейс
            total_catch = db.session.query(func.sum(Catch.weight))\
                .join(TripGround)\
                .filter(TripGround.trip_id == trip.id).scalar() or 0
                
            # Детализация по сортам
            catches_by_species = db.session.query(
                FishSpecies.name, 
                func.sum(Catch.weight).label('weight')
            ).select_from(Trip)\
             .join(TripGround)\
             .join(Catch)\
             .join(FishSpecies)\
             .filter(Trip.id == trip.id)\
             .group_by(FishSpecies.id).all()
            
            trips_data.append({
                'departure': trip.departure_date,
                'return': trip.return_date,
                'total_catch': total_catch,
                'catches_by_species': catches_by_species
            })
        
        result.append({
            'boat_name': boat.name,
            'boat_type': boat.boat_type,
            'trips': trips_data
        })
    
    return render_template('boats/catches.html', result=result)

# ==================== Пункт 2: Добавление выхода катера ====================
@app.route('/trips/add', methods=['GET', 'POST'])
def add_trip():
    """Добавление нового рейса с командой"""
    form = TripForm()
    
    # Заполняем select с катерами
    form.boat_id.choices = [(b.id, f"{b.name} ({b.boat_type})") for b in Boat.query.all()]
    
    if form.validate_on_submit():
        try:
            # Создаем рейс
            new_trip = Trip(
                boat_id=form.boat_id.data,
                departure_date=form.departure_date.data,
                return_date=form.return_date.data
            )
            db.session.add(new_trip)
            db.session.flush()  # Получаем ID рейса
            
            # Добавляем членов команды
            for crew_data in form.crew.data:
                if crew_data.get('full_name'):  # Проверяем, что имя не пустое
                    member = CrewMember(
                        trip_id=new_trip.id,
                        full_name=crew_data['full_name'],
                        position=crew_data['position'],
                        address=crew_data.get('address', '')
                    )
                    db.session.add(member)
            
            db.session.commit()
            flash('Рейс успешно добавлен!', 'success')
            return redirect(url_for('trips_list'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при добавлении рейса: {str(e)}', 'danger')
    
    return render_template('trips/add.html', form=form)

@app.route('/trips')
def trips_list():
    """Список всех рейсов"""
    trips = Trip.query.order_by(Trip.departure_date.desc()).all()
    return render_template('trips/list.html', trips=trips)

# ==================== Пункт 3: Максимальный улов по сортам ====================
@app.route('/reports/max-catch-per-species', methods=['GET', 'POST'])
def max_catch_per_species():
    """Для интервала дат вывести для каждого сорта список катеров с наибольшим уловом"""
    form = DateRangeForm()
    results = []
    
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        
        # Подзапрос: суммарный улов каждого катера по каждому сорту за период
        subq = db.session.query(
            Catch.fish_species_id,
            Boat.id.label('boat_id'),
            Boat.name.label('boat_name'),
            func.sum(Catch.weight).label('total_catch')
        ).join(TripGround, Catch.trip_ground_id == TripGround.id)\
         .join(Trip, TripGround.trip_id == Trip.id)\
         .join(Boat, Trip.boat_id == Boat.id)\
         .filter(Trip.departure_date.between(start_date, end_date))\
         .group_by(Catch.fish_species_id, Boat.id).subquery()
        
        # Ранжируем катера по улову внутри каждого сорта
        ranked = db.session.query(
            subq.c.fish_species_id,
            subq.c.boat_name,
            subq.c.total_catch,
            func.rank().over(
                partition_by=subq.c.fish_species_id, 
                order_by=subq.c.total_catch.desc()
            ).label('rank')
        ).subquery()
        
        # Выбираем только лучшие (rank=1)
        results = db.session.query(
            FishSpecies.name.label('species_name'),
            ranked.c.boat_name,
            ranked.c.total_catch
        ).join(FishSpecies, FishSpecies.id == ranked.c.fish_species_id)\
         .filter(ranked.c.rank == 1)\
         .order_by(FishSpecies.name).all()
    
    return render_template('reports/max_catch_per_species.html', form=form, results=results)

# ==================== Пункт 4: Средний улов по банкам ====================
@app.route('/reports/ground-avg-catch', methods=['GET', 'POST'])
def ground_avg_catch():
    """Для интервала дат вывести список банок со средним уловом"""
    form = DateRangeForm()
    results = []
    
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        
        results = db.session.query(
            FishingGround.name,
            func.count(distinct(Trip.id)).label('trips_count'),
            func.avg(Catch.weight).label('avg_catch'),
            func.sum(Catch.weight).label('total_catch')
        ).join(TripGround, FishingGround.id == TripGround.ground_id)\
         .join(Catch, TripGround.id == Catch.trip_ground_id)\
         .join(Trip, TripGround.trip_id == Trip.id)\
         .filter(Trip.departure_date.between(start_date, end_date))\
         .group_by(FishingGround.id)\
         .order_by(func.avg(Catch.weight).desc()).all()
    
    return render_template('reports/ground_avg_catch.html', form=form, results=results)

# ==================== Пункт 5: Добавление новой банки ====================
@app.route('/grounds/add', methods=['GET', 'POST'])
def add_ground():
    """Добавление новой банки"""
    form = FishingGroundForm()
    
    if form.validate_on_submit():
        try:
            ground = FishingGround(
                name=form.name.data,
                latitude=form.latitude.data,
                longitude=form.longitude.data,
                depth=form.depth.data
            )
            db.session.add(ground)
            db.session.commit()
            flash('Банка успешно добавлена!', 'success')
            return redirect(url_for('grounds_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при добавлении банки: {str(e)}', 'danger')
    
    return render_template('grounds/add.html', form=form)

@app.route('/grounds')
def grounds_list():
    """Список всех банок"""
    grounds = FishingGround.query.all()
    return render_template('grounds/list.html', grounds=grounds)

# ==================== Пункт 6: Катера с уловом выше среднего ====================
@app.route('/grounds/<int:ground_id>/boats-above-avg')
def boats_above_avg(ground_id):
    """Для заданной банки вывести катера с уловом выше среднего"""
    ground = FishingGround.query.get_or_404(ground_id)
    
    # Вычисляем средний улов по этой банке за все время
    avg_subq = db.session.query(
        func.avg(Catch.weight).label('avg_weight')
    ).join(TripGround)\
     .filter(TripGround.ground_id == ground_id).subquery()
    
    # Находим катера, у которых был улов на этой банке выше среднего
    boats_data = db.session.query(
        Boat.id,
        Boat.name,
        Boat.boat_type,
        Trip.departure_date,
        Catch.weight.label('catch_weight')
    ).join(Trip, Boat.id == Trip.boat_id)\
     .join(TripGround, Trip.id == TripGround.trip_id)\
     .join(Catch, TripGround.id == Catch.trip_ground_id)\
     .filter(TripGround.ground_id == ground_id)\
     .filter(Catch.weight > avg_subq.c.avg_weight)\
     .order_by(Catch.weight.desc()).all()
    
    return render_template('grounds/boats_above_avg.html', 
                         ground=ground, 
                         boats_data=boats_data)

# ==================== Пункт 7: Сорта рыбы и рейсы ====================
@app.route('/reports/species-trips')
def species_trips():
    """Вывести список сортов рыбы и для каждого список рейсов с уловом"""
    species_list = FishSpecies.query.all()
    data = []
    
    for species in species_list:
        trips_info = db.session.query(
            Trip.id,
            Trip.departure_date,
            Trip.return_date,
            Boat.name.label('boat_name'),
            func.sum(Catch.weight).label('total_weight'),
            func.count(distinct(TripGround.ground_id)).label('grounds_visited')
        ).join(TripGround, Trip.id == TripGround.trip_id)\
         .join(Catch, TripGround.id == Catch.trip_ground_id)\
         .join(Boat, Trip.boat_id == Boat.id)\
         .filter(Catch.fish_species_id == species.id)\
         .group_by(Trip.id, Boat.name)\
         .order_by(Trip.departure_date.desc()).all()
        
        if trips_info:  # Добавляем только если есть улов этого сорта
            data.append({
                'species': species.name,
                'trips': trips_info
            })
    
    return render_template('reports/species_trips.html', data=data)

# ==================== Пункт 8: Добавление улова ====================
@app.route('/catches/add', methods=['GET', 'POST'])
def add_catch():
    """Для выбранного рейса и банки добавить данные о сорте и количестве рыбы"""
    form = CatchForm()
    
    # Заполняем выпадающие списки
    form.trip_id.choices = [(t.id, f"Рейс #{t.id} - {t.boat.name} ({t.departure_date.strftime('%d.%m.%Y')})") 
                           for t in Trip.query.order_by(Trip.departure_date.desc()).all()]
    form.ground_id.choices = [(g.id, g.name) for g in FishingGround.query.all()]
    form.species_id.choices = [(s.id, s.name) for s in FishSpecies.query.all()]
    
    if form.validate_on_submit():
        try:
            # Проверяем, что указанная банка посещалась в этом рейсе
            trip_ground = TripGround.query.filter_by(
                trip_id=form.trip_id.data,
                ground_id=form.ground_id.data
            ).first()
            
            # Если банка не посещалась, создаем запись о посещении
            if not trip_ground:
                trip_ground = TripGround(
                    trip_id=form.trip_id.data,
                    ground_id=form.ground_id.data,
                    arrival_date=datetime.now(),
                    departure_date=datetime.now(),
                    quality='хорошее'
                )
                db.session.add(trip_ground)
                db.session.flush()
            
            # Добавляем улов
            catch = Catch(
                trip_ground_id=trip_ground.id,
                fish_species_id=form.species_id.data,
                weight=form.weight.data
            )
            db.session.add(catch)
            db.session.commit()
            
            flash('Улов успешно добавлен!', 'success')
            return redirect(url_for('trip_detail', trip_id=form.trip_id.data))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при добавлении улова: {str(e)}', 'danger')
    
    return render_template('catches/add.html', form=form)

@app.route('/trips/<int:trip_id>')
def trip_detail(trip_id):
    """Детальная информация о рейсе"""
    trip = Trip.query.get_or_404(trip_id)
    return render_template('trips/detail.html', trip=trip)

# ==================== Пункт 9: Изменение характеристик катера ====================
@app.route('/boats/<int:boat_id>/edit', methods=['GET', 'POST'])
def edit_boat(boat_id):
    """Редактирование данных катера"""
    boat = Boat.query.get_or_404(boat_id)
    form = BoatForm(obj=boat)
    
    if form.validate_on_submit():
        try:
            boat.name = form.name.data
            boat.boat_type = form.boat_type.data
            boat.displacement = form.displacement.data
            boat.build_date = form.build_date.data
            
            db.session.commit()
            flash('Данные катера обновлены!', 'success')
            return redirect(url_for('boats_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при обновлении: {str(e)}', 'danger')
    
    return render_template('boats/edit.html', form=form, boat=boat)

# ==================== Пункт 10: Добавление нового катера ====================
@app.route('/boats/add', methods=['GET', 'POST'])
def add_boat():
    """Добавление нового катера"""
    form = BoatForm()
    
    if form.validate_on_submit():
        try:
            boat = Boat(
                name=form.name.data,
                boat_type=form.boat_type.data,
                displacement=form.displacement.data,
                build_date=form.build_date.data
            )
            db.session.add(boat)
            db.session.commit()
            flash('Катер успешно добавлен!', 'success')
            return redirect(url_for('boats_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при добавлении: {str(e)}', 'danger')
    
    return render_template('boats/add.html', form=form)

@app.route('/boats')
def boats_list():
    """Список всех катеров"""
    boats = Boat.query.all()
    return render_template('boats/list.html', boats=boats)

# ==================== Пункт 11: Рейсы по сорту и банке ====================
@app.route('/reports/species-ground-catch', methods=['GET', 'POST'])
def species_ground_catch():
    """Для указанного сорта рыбы и банки вывести список рейсов с количеством улова"""
    form = SpeciesGroundForm()
    
    # Заполняем выпадающие списки
    form.species_id.choices = [(s.id, s.name) for s in FishSpecies.query.all()]
    form.ground_id.choices = [(g.id, g.name) for g in FishingGround.query.all()]
    
    results = []
    selected_species = None
    selected_ground = None
    
    if form.validate_on_submit():
        species_id = form.species_id.data
        ground_id = form.ground_id.data
        
        selected_species = FishSpecies.query.get(species_id)
        selected_ground = FishingGround.query.get(ground_id)
        
        results = db.session.query(
            Trip.id,
            Trip.departure_date,
            Trip.return_date,
            Boat.name.label('boat_name'),
            Catch.weight
        ).join(TripGround, Trip.id == TripGround.trip_id)\
         .join(Catch, TripGround.id == Catch.trip_ground_id)\
         .join(Boat, Trip.boat_id == Boat.id)\
         .filter(TripGround.ground_id == ground_id)\
         .filter(Catch.fish_species_id == species_id)\
         .order_by(Trip.departure_date.desc()).all()
    
    return render_template('reports/species_ground_catch.html', 
                         form=form, 
                         results=results,
                         species=selected_species,
                         ground=selected_ground)

# Дополнительные маршруты для удаления
@app.route('/boats/<int:boat_id>/delete', methods=['POST'])
def delete_boat(boat_id):
    """Удаление катера"""
    boat = Boat.query.get_or_404(boat_id)
    try:
        db.session.delete(boat)
        db.session.commit()
        flash('Катер удален!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при удалении: {str(e)}', 'danger')
    return redirect(url_for('boats_list'))

@app.route('/trips/<int:trip_id>/delete', methods=['POST'])
def delete_trip(trip_id):
    """Удаление рейса"""
    trip = Trip.query.get_or_404(trip_id)
    try:
        db.session.delete(trip)
        db.session.commit()
        flash('Рейс удален!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при удалении: {str(e)}', 'danger')
    return redirect(url_for('trips_list'))