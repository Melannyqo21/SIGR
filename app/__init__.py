from flask import Flask, redirect, url_for
from app.config import Config
from app.extensions import db, login_manager, csrf
from app.models import User, Category, Dish

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.menu import menu_bp
    from app.routes.orders import orders_bp
    from app.routes.bookings import bookings_bp
    from app.routes.billing import billing_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(billing_bp)

    @app.route("/")
    def index():
        return redirect(url_for("menu.list_menu"))

    with app.app_context():
        db.create_all()
        seed_initial_data()

    return app

def seed_initial_data():
    """Crea usuarios y menú base si la base de datos está vacía."""
    if User.query.count() == 0:
        admin = User(nombre="Administrador General", username="admin", rol="administrador")
        admin.set_password("admin123")
        mesero = User(nombre="Carlos Mesero", username="mesero", rol="mesero")
        mesero.set_password("mesero123")
        cliente = User(nombre="Ana Cliente", username="cliente", rol="cliente")
        cliente.set_password("cliente123")
        db.session.add_all([admin, mesero, cliente])
        db.session.commit()

    if Category.query.count() == 0:
        cat_fuertes = Category(nombre="Platos Fuertes", descripcion="Especialidades de la casa")
        cat_bebidas = Category(nombre="Bebidas", descripcion="Jugos naturales y refrescos")
        cat_postres = Category(nombre="Postres", descripcion="Dulces tradicionales")
        db.session.add_all([cat_fuertes, cat_bebidas, cat_postres])
        db.session.flush()

        platos = [
            Dish(nombre="Bandeja Paisa", descripcion="Plato típico con chicharrón, carne, frijol y aguacate", precio=34000, disponible=True, category_id=cat_fuertes.id),
            Dish(nombre="Lomo al Trapo", descripcion="Lomo de res asado con guarnición de papas rústicas", precio=42000, disponible=True, category_id=cat_fuertes.id),
            Dish(nombre="Limonada de Coco", descripcion="Limonada frappé con crema de coco natural", precio=11000, disponible=True, category_id=cat_bebidas.id),
            Dish(nombre="Cheesecake de Maracuyá", descripcion="Porción de torta de queso con reducción de maracuyá", precio=14000, disponible=True, category_id=cat_postres.id),
        ]
        db.session.add_all(platos)
        db.session.commit()