from datetime import date
from app.extensions import db
from app.models import User, Category, Dish, Order, OrderItem, Booking, Sale, CashClosure

def create_user(nombre, username, password, rol):
    if User.query.filter_by(username=username).first():
        raise ValueError("El nombre de usuario ya está registrado.")
    user = User(nombre=nombre, username=username, rol=rol, activo=True)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

def create_order_with_items(cliente_nombre, mesa, items_data, mesero_id=None, cliente_id=None):
    """
    items_data: lista de tuplas (dish_id, cantidad)
    Calcula subtotales y el total del pedido validando disponibilidad.
    """
    if not items_data:
        raise ValueError("El pedido debe contener al menos un plato.")

    order = Order(
        cliente_nombre=cliente_nombre,
        mesa=mesa,
        estado="pendiente",
        mesero_id=mesero_id,
        cliente_id=cliente_id,
        total=0.0
    )
    db.session.add(order)
    db.session.flush()

    total_acumulado = 0.0
    for dish_id, cantidad in items_data:
        dish = db.session.get(Dish, int(dish_id))
        if not dish or not dish.activo or not dish.disponible:
            raise ValueError("El plato seleccionado no está disponible.")
        if int(cantidad) <= 0:
            continue
        subtotal = round(dish.precio * int(cantidad), 2)
        item = OrderItem(
            order_id=order.id,
            dish_id=dish.id,
            cantidad=int(cantidad),
            precio_unitario=dish.precio,
            subtotal=subtotal
        )
        db.session.add(item)
        total_acumulado += subtotal

    if total_acumulado <= 0:
        db.session.rollback()
        raise ValueError("Las cantidades seleccionadas deben ser mayores a cero.")

    order.total = round(total_acumulado, 2)
    db.session.commit()
    return order

def update_order_status(order_id, nuevo_estado):
    estados_validos = ["pendiente", "en preparación", "listo", "entregado"]
    if nuevo_estado not in estados_validos:
        raise ValueError("Estado de pedido no válido.")

    order = db.session.get(Order, int(order_id))
    if not order:
        raise ValueError("Pedido no encontrado.")

    order.estado = nuevo_estado

    if nuevo_estado == "entregado":
        existing_sale = Sale.query.filter_by(order_id=order.id).first()
        if not existing_sale:
            nueva_venta = Sale(
                order_id=order.id,
                monto=order.total,
                fecha=date.today()
            )
            db.session.add(nueva_venta)

    db.session.commit()
    return order

def perform_daily_closure(fecha_cierre, user_id, observaciones=""):
    """Agrupa las ventas sin cerrar de una fecha y genera el cierre de caja."""
    ventas_pendientes = Sale.query.filter_by(fecha=fecha_cierre, closure_id=None).all()
    if not ventas_pendientes:
        raise ValueError("No existen ventas pendientes de cierre para la fecha seleccionada.")

    total_ingresos = round(sum(v.monto for v in ventas_pendientes), 2)
    total_pedidos = len(ventas_pendientes)

    cierre = CashClosure(
        fecha=fecha_cierre,
        total_pedidos=total_pedidos,
        total_ingresos=total_ingresos,
        observaciones=observaciones,
        cerrado_por_id=user_id
    )
    db.session.add(cierre)
    db.session.flush()

    for venta in ventas_pendientes:
        venta.closure_id = cierre.id

    db.session.commit()
    return cierre