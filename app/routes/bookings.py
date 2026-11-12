from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Booking
from app.forms import BookingForm
from app.extensions import db
from app.decorators import role_required

bookings_bp = Blueprint("bookings", __name__, url_prefix="/bookings")

@bookings_bp.route("/", methods=["GET", "POST"])
@login_required
def list_bookings():
    form = BookingForm()
    if form.validate_on_submit():
        booking = Booking(
            cliente_nombre=form.cliente_nombre.data,
            contacto=form.contacto.data,
            fecha=form.fecha.data,
            hora=form.hora.data,
            personas=form.personas.data,
            estado="pendiente",
            user_id=current_user.id
        )
        db.session.add(booking)
        db.session.commit()
        flash("Reserva registrada correctamente.", "success")
        return redirect(url_for("bookings.list_bookings"))

    if current_user.rol == "cliente":
        bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.fecha.desc()).all()
    else:
        bookings = Booking.query.order_by(Booking.fecha.desc(), Booking.hora.asc()).all()

    return render_template("bookings.html", bookings=bookings, form=form)

@bookings_bp.route("/<int:booking_id>/status", methods=["POST"])
@login_required
@role_required("administrador", "mesero")
def update_booking(booking_id):
    booking = db.session.get(Booking, booking_id)
    nuevo_estado = request.form.get("estado")
    estados_validos = ["pendiente", "confirmada", "cancelada", "atendida"]
    if booking and nuevo_estado in estados_validos:
        booking.estado = nuevo_estado
        db.session.commit()
        flash(f"Reserva #{booking.id} actualizada a '{nuevo_estado}'.", "info")
    return redirect(url_for("bookings.list_bookings"))