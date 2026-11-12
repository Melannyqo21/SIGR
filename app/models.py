from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), nullable=False)  # administrador, mesero, cliente
    activo = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    descripcion = db.Column(db.String(200))
    dishes = db.relationship("Dish", backref="category", lazy=True)

class Dish(db.Model):
    __tablename__ = "dishes"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    disponible = db.Column(db.Boolean, default=True)
    activo = db.Column(db.Boolean, default=True)  # Eliminación lógica
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    cliente_nombre = db.Column(db.String(100), nullable=False)
    mesa = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(25), default="pendiente")  # pendiente, en preparación, listo, entregado
    total = db.Column(db.Float, default=0.0)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    cliente_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    mesero_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    items = db.relationship("OrderItem", backref="order", cascade="all, delete-orphan", lazy=True)
    sale = db.relationship("Sale", backref="order", uselist=False, lazy=True)
    mesero = db.relationship("User", foreign_keys=[mesero_id])

class OrderItem(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    dish_id = db.Column(db.Integer, db.ForeignKey("dishes.id"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    dish = db.relationship("Dish")

class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    cliente_nombre = db.Column(db.String(100), nullable=False)
    contacto = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.String(10), nullable=False)
    personas = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(20), default="pendiente")  # pendiente, confirmada, cancelada, atendida
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

class CashClosure(db.Model):
    __tablename__ = "cash_closures"
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    total_pedidos = db.Column(db.Integer, nullable=False)
    total_ingresos = db.Column(db.Float, nullable=False)
    observaciones = db.Column(db.String(255))
    cerrado_por_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    fecha_cierre = db.Column(db.DateTime, default=datetime.now)

    cerrado_por = db.relationship("User")
    sales = db.relationship("Sale", backref="closure", lazy=True)

class Sale(db.Model):
    __tablename__ = "sales"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), unique=True, nullable=False)
    monto = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.Date, default=date.today, nullable=False)
    fecha_hora = db.Column(db.DateTime, default=datetime.now)
    closure_id = db.Column(db.Integer, db.ForeignKey("cash_closures.id"), nullable=True)