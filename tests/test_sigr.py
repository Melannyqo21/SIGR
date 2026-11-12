import pytest
from datetime import date
from app import create_app
from app.config import TestConfig
from app.extensions import db
from app.models import Dish, Order, Sale, Booking
from app.services import create_order_with_items, update_order_status, perform_daily_closure

@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_auth_login_and_roles(client):
    """Verifica inicio de sesión correcto y protección de rutas por rol."""
    res = client.post("/auth/login", data={"username": "cliente", "password": "cliente123"}, follow_redirects=True)
    assert res.status_code == 200

    res_forbidden = client.get("/billing/")
    assert res_forbidden.status_code == 403

def test_menu_crud_and_deactivation(client):
    """Verifica creación y desactivación lógica de platos por el administrador."""
    client.post("/auth/login", data={"username": "admin", "password": "admin123"}, follow_redirects=True)
    res = client.post("/menu/dish/new", data={
        "nombre": "Cazuela de Mariscos",
        "descripcion": "Cazuela cremosa con leche de coco",
        "precio": 38000,
        "category_id": 1,
        "disponible": True
    }, follow_redirects=True)
    assert res.status_code == 200
    plato = Dish.query.filter_by(nombre="Cazuela de Mariscos").first()
    assert plato is not None

    client.post(f"/menu/dish/{plato.id}/deactivate", follow_redirects=True)
    assert plato.activo is False

def test_order_creation_and_automatic_sale(client):
    """Verifica cálculo de subtotales/totales, entrega de pedido, venta única y cierre de caja."""
    with client.application.app_context():
        plato = Dish.query.first()
        order = create_order_with_items("Pedro Perez", 5, [(plato.id, 2)])
        assert order.total == plato.precio * 2

        update_order_status(order.id, "entregado")
        ventas = Sale.query.filter_by(order_id=order.id).all()
        assert len(ventas) == 1
        assert ventas[0].monto == order.total

        update_order_status(order.id, "entregado")
        assert Sale.query.filter_by(order_id=order.id).count() == 1

        cierre = perform_daily_closure(date.today(), user_id=1, observaciones="Cierre test")
        assert cierre.total_ingresos == order.total
        assert cierre.total_pedidos == 1

def test_booking_lifecycle(client):
    """Verifica registro y actualización de estado de una reserva."""
    client.post("/auth/login", data={"username": "mesero", "password": "mesero123"}, follow_redirects=True)
    client.post("/bookings/", data={
        "cliente_nombre": "Laura Gomez",
        "contacto": "3001234567",
        "fecha": "2026-11-20",
        "hora": "20:00",
        "personas": 4
    }, follow_redirects=True)
    reserva = Booking.query.filter_by(cliente_nombre="Laura Gomez").first()
    assert reserva is not None
    assert reserva.estado == "pendiente"

    client.post(f"/bookings/{reserva.id}/status", data={"estado": "confirmada"}, follow_redirects=True)
    assert reserva.estado == "confirmada"