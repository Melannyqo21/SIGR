from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app.models import Category, Dish
from app.forms import CategoryForm, DishForm
from app.decorators import role_required
from app.extensions import db

menu_bp = Blueprint("menu", __name__, url_prefix="/menu")

@menu_bp.route("/", methods=["GET"])
@login_required
def list_menu():
    categories = Category.query.all()
    dishes = Dish.query.filter_by(activo=True).order_by(Dish.category_id, Dish.nombre).all()
    cat_form = CategoryForm()
    dish_form = DishForm()
    dish_form.category_id.choices = [(c.id, c.nombre) for c in categories]
    return render_template(
        "menu.html",
        categories=categories,
        dishes=dishes,
        cat_form=cat_form,
        dish_form=dish_form
    )

@menu_bp.route("/category/new", methods=["POST"])
@login_required
@role_required("administrador")
def create_category():
    form = CategoryForm()
    if form.validate_on_submit():
        if Category.query.filter_by(nombre=form.nombre.data).first():
            flash("La categoría ya existe.", "warning")
        else:
            cat = Category(nombre=form.nombre.data, descripcion=form.descripcion.data)
            db.session.add(cat)
            db.session.commit()
            flash("Categoría creada correctamente.", "success")
    return redirect(url_for("menu.list_menu"))

@menu_bp.route("/dish/new", methods=["POST"])
@login_required
@role_required("administrador")
def create_dish():
    categories = Category.query.all()
    form = DishForm()
    form.category_id.choices = [(c.id, c.nombre) for c in categories]
    if form.validate_on_submit():
        dish = Dish(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            precio=form.precio.data,
            category_id=form.category_id.data,
            disponible=form.disponible.data,
            activo=True
        )
        db.session.add(dish)
        db.session.commit()
        flash("Plato registrado en el menú.", "success")
    else:
        flash("Error al validar los datos del plato.", "danger")
    return redirect(url_for("menu.list_menu"))

@menu_bp.route("/dish/<int:dish_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("administrador")
def edit_dish(dish_id):
    dish = db.session.get(Dish, dish_id)
    if not dish or not dish.activo:
        flash("Plato no encontrado.", "danger")
        return redirect(url_for("menu.list_menu"))

    categories = Category.query.all()
    form = DishForm(obj=dish)
    form.category_id.choices = [(c.id, c.nombre) for c in categories]

    if form.validate_on_submit():
        dish.nombre = form.nombre.data
        dish.descripcion = form.descripcion.data
        dish.precio = form.precio.data
        dish.category_id = form.category_id.data
        dish.disponible = form.disponible.data
        db.session.commit()
        flash("Plato actualizado correctamente.", "success")
        return redirect(url_for("menu.list_menu"))

    return render_template("dish_edit.html", form=form, dish=dish)

@menu_bp.route("/dish/<int:dish_id>/deactivate", methods=["POST"])
@login_required
@role_required("administrador")
def deactivate_dish(dish_id):
    dish = db.session.get(Dish, dish_id)
    if dish:
        dish.activo = False
        db.session.commit()
        flash(f"Plato '{dish.nombre}' desactivado del menú.", "info")
    return redirect(url_for("menu.list_menu"))