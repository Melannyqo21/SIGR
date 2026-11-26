from flask import Flask, redirect, url_for
from sqlalchemy.exc import IntegrityError
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
    """Crea usuarios y menú base de forma idempotente."""
    try:
        usuarios = [
            ("Administrador General", "admin", "admin123", "administrador"),
            ("Carlos Mesero", "mesero", "mesero123", "mesero"),
            ("Ana Cliente", "cliente", "cliente123", "cliente"),
        ]
        for nombre, username, password, rol in usuarios:
            if not User.query.filter_by(username=username).first():
                user = User(nombre=nombre, username=username, rol=rol, activo=True)
                user.set_password(password)
                db.session.add(user)
        db.session.commit()

        categorias = [
            ("Platos Fuertes", "Especialidades de la casa"),
            ("Bebidas", "Jugos naturales y refrescos"),
            ("Postres", "Dulces tradicionales"),
        ]
        for nombre, descripcion in categorias:
            if not Category.query.filter_by(nombre=nombre).first():
                db.session.add(Category(nombre=nombre, descripcion=descripcion))
        db.session.commit()

        cat_fuertes = Category.query.filter_by(nombre="Platos Fuertes").first()
        cat_bebidas = Category.query.filter_by(nombre="Bebidas").first()
        cat_postres = Category.query.filter_by(nombre="Postres").first()

        platos = [
            (
                "Bandeja Paisa",
                "Plato típico con chicharrón, carne, frijol y aguacate",
                34000,
                cat_fuertes,
            ),
            (
                "Lomo al Trapo",
                "Lomo de res asado con guarnición de papas rústicas",
                42000,
                cat_fuertes,
            ),
            (
                "Limonada de Coco",
                "Limonada frappé con crema de coco natural",
                11000,
                cat_bebidas,
            ),
            (
                "Cheesecake de Maracuyá",
                "Porción de torta de queso con reducción de maracuyá",
                14000,
                cat_postres,
            ),
        ]
        for nombre, descripcion, precio, categoria in platos:
            if categoria and not Dish.query.filter_by(nombre=nombre).first():
                db.session.add(
                    Dish(
                        nombre=nombre,
                        descripcion=descripcion,
                        precio=precio,
                        disponible=True,
                        activo=True,
                        category_id=categoria.id,
                    )
                )
        db.session.commit()
    except IntegrityError:
        db.session.rollback()