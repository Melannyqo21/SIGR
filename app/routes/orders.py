from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Order, Dish
from app.services import create_order_with_items, update_order_status
from app.decorators import role_required

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")

@orders_bp.route("/", methods=["GET"])
@login_required
def list_orders():
    dishes = Dish.query.filter_by(activo=True, disponible=True).all()
    if current_user.rol == "cliente":
        orders = Order.query.filter_by(cliente_id=current_user.id).order_by(Order.fecha_creacion.desc()).all()
    else:
        orders = Order.query.order_by(Order.fecha_creacion.desc()).all()
    return render_template("orders.html", orders=orders, dishes=dishes)

@orders_bp.route("/new", methods=["POST"])
@login_required
def create_order():
    cliente_nombre = request.form.get("cliente_nombre", "").strip()
    mesa = request.form.get("mesa", type=int)

    if not cliente_nombre or not mesa:
        flash("Debes indicar el nombre del cliente y el número de mesa.", "warning")
        return redirect(url_for("orders.list_orders"))

    dish_ids = request.form.getlist("dish_id")
    cantidades = request.form.getlist("cantidad")

    items_data = []
    for d_id, cant in zip(dish_ids, cantidades):
        if cant and int(cant) > 0:
            items_data.append((int(d_id), int(cant)))

    try:
        mesero_id = current_user.id if current_user.rol in ["mesero", "administrador"] else None
        cliente_id = current_user.id if current_user.rol == "cliente" else None
        order = create_order_with_items(
            cliente_nombre=cliente_nombre,
            mesa=mesa,
            items_data=items_data,
            mesero_id=mesero_id,
            cliente_id=cliente_id
        )
        flash(f"Pedido #{order.id} registrado por un total de ${order.total:,.0f}.", "success")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("orders.list_orders"))

@orders_bp.route("/<int:order_id>/status", methods=["POST"])
@login_required
@role_required("administrador", "mesero")
def change_status(order_id):
    nuevo_estado = request.form.get("estado")
    try:
        order = update_order_status(order_id, nuevo_estado)
        flash(f"Pedido #{order.id} actualizado a '{order.estado}'.", "info")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("orders.list_orders"))