from datetime import date, datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Sale, CashClosure
from app.forms import CashClosureForm
from app.services import perform_daily_closure
from app.decorators import role_required

billing_bp = Blueprint("billing", __name__, url_prefix="/billing")

@billing_bp.route("/", methods=["GET"])
@login_required
@role_required("administrador")
def dashboard():
    fecha_filtro_str = request.args.get("fecha", date.today().isoformat())
    try:
        fecha_filtro = datetime.strptime(fecha_filtro_str, "%Y-%m-%d").date()
    except ValueError:
        fecha_filtro = date.today()

    ventas_fecha = Sale.query.filter_by(fecha=fecha_filtro).order_by(Sale.fecha_hora.desc()).all()
    ingresos_fecha = round(sum(v.monto for v in ventas_fecha), 2)
    cantidad_pedidos = len(ventas_fecha)

    cierres = CashClosure.query.order_by(CashClosure.fecha_cierre.desc()).all()

    form = CashClosureForm(fecha=fecha_filtro)
    return render_template(
        "billing.html",
        ventas=ventas_fecha,
        fecha_filtro=fecha_filtro,
        ingresos_fecha=ingresos_fecha,
        cantidad_pedidos=cantidad_pedidos,
        cierres=cierres,
        form=form
    )

@billing_bp.route("/close", methods=["POST"])
@login_required
@role_required("administrador")
def close_cash():
    form = CashClosureForm()
    if form.validate_on_submit():
        try:
            cierre = perform_daily_closure(
                fecha_cierre=form.fecha.data,
                user_id=current_user.id,
                observaciones=form.observaciones.data
            )
            flash(
                f"Cierre de caja realizado para {cierre.fecha}: {cierre.total_pedidos} pedidos por ${cierre.total_ingresos:,.0f}.",
                "success"
            )
        except ValueError as e:
            flash(str(e), "warning")
    return redirect(url_for("billing.dashboard"))