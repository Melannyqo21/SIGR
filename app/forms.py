from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, FloatField, IntegerField, BooleanField, DateField
from wtforms.validators import DataRequired, NumberRange, Length

class LoginForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired()])

class UserForm(FlaskForm):
    nombre = StringField("Nombre Completo", validators=[DataRequired(), Length(max=100)])
    username = StringField("Usuario", validators=[DataRequired(), Length(max=50)])
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(min=4)])
    rol = SelectField("Rol", choices=[
        ("administrador", "Administrador"),
        ("mesero", "Mesero"),
        ("cliente", "Cliente")
    ], validators=[DataRequired()])

class CategoryForm(FlaskForm):
    nombre = StringField("Nombre Categoría", validators=[DataRequired(), Length(max=80)])
    descripcion = StringField("Descripción", validators=[Length(max=200)])

class DishForm(FlaskForm):
    nombre = StringField("Nombre del Plato", validators=[DataRequired(), Length(max=100)])
    descripcion = StringField("Descripción", validators=[DataRequired(), Length(max=255)])
    precio = FloatField("Precio ($)", validators=[DataRequired(), NumberRange(min=100)])
    category_id = SelectField("Categoría", coerce=int, validators=[DataRequired()])
    disponible = BooleanField("Disponible para la venta", default=True)

class BookingForm(FlaskForm):
    cliente_nombre = StringField("Nombre del Cliente", validators=[DataRequired(), Length(max=100)])
    contacto = StringField("Teléfono / Contacto", validators=[DataRequired(), Length(max=100)])
    fecha = DateField("Fecha", validators=[DataRequired()])
    hora = StringField("Hora (HH:MM)", validators=[DataRequired(), Length(max=10)])
    personas = IntegerField("Cantidad de Personas", validators=[DataRequired(), NumberRange(min=1, max=50)])

class CashClosureForm(FlaskForm):
    fecha = DateField("Fecha de Cierre", validators=[DataRequired()])
    observaciones = StringField("Observaciones", validators=[Length(max=255)])