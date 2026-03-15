from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, DateTimeField, IntegerField, SelectField, FieldList, FormField, TextAreaField
from wtforms.validators import DataRequired, Optional, NumberRange, Length
from datetime import datetime

class BoatForm(FlaskForm):
    name = StringField('Название катера', validators=[DataRequired(), Length(max=100)])
    boat_type = StringField('Тип катера', validators=[Optional(), Length(max=50)])
    displacement = FloatField('Водоизмещение (тонн)', validators=[Optional(), NumberRange(min=0)])
    build_date = DateField('Дата постройки', validators=[Optional()])

class CrewMemberForm(FlaskForm):
    full_name = StringField('ФИО', validators=[DataRequired(), Length(max=150)])
    position = StringField('Должность', validators=[DataRequired(), Length(max=50)])
    address = TextAreaField('Адрес', validators=[Optional()])

class TripForm(FlaskForm):
    boat_id = SelectField('Катер', coerce=int, validators=[DataRequired()])
    departure_date = DateTimeField('Дата и время выхода', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    return_date = DateTimeField('Дата и время возвращения', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    crew = FieldList(FormField(CrewMemberForm), min_entries=1, max_entries=10)

class FishingGroundForm(FlaskForm):
    name = StringField('Название банки', validators=[DataRequired(), Length(max=200)])
    latitude = FloatField('Широта', validators=[Optional()])
    longitude = FloatField('Долгота', validators=[Optional()])
    depth = FloatField('Средняя глубина (м)', validators=[Optional()])

class CatchForm(FlaskForm):
    trip_id = SelectField('Рейс', coerce=int, validators=[DataRequired()])
    ground_id = SelectField('Банка', coerce=int, validators=[DataRequired()])
    species_id = SelectField('Сорт рыбы', coerce=int, validators=[DataRequired()])
    weight = FloatField('Вес улова (кг)', validators=[DataRequired(), NumberRange(min=0.1)])

class DateRangeForm(FlaskForm):
    start_date = DateField('Дата начала', validators=[DataRequired()])
    end_date = DateField('Дата окончания', validators=[DataRequired()])

class SpeciesGroundForm(FlaskForm):
    species_id = SelectField('Сорт рыбы', coerce=int, validators=[DataRequired()])
    ground_id = SelectField('Банка', coerce=int, validators=[DataRequired()])