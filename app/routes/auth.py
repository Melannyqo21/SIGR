from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.models import User
from app.forms import LoginForm, UserForm
from app.services import create_user
from app.decorators import role_required
from app.extensions import db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, activo=True).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash(f"Bienvenido, {user.nombre} ({user.rol}).", "success")
            return redirect(url_for("menu.list_menu"))
        flash("Usuario o contraseña incorrectos.", "danger")
    return render_template("login.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión correctamente.", "info")
    return redirect(url_for("auth.login"))

@auth_bp.route("/users", methods=["GET", "POST"])
@login_required
@role_required("administrador")
def manage_users():
    form = UserForm()
    if form.validate_on_submit():
        try:
            create_user(
                nombre=form.nombre.data,
                username=form.username.data,
                password=form.password.data,
                rol=form.rol.data
            )
            flash("Usuario registrado exitosamente.", "success")
            return redirect(url_for("auth.manage_users"))
        except ValueError as e:
            flash(str(e), "danger")

    users = User.query.order_by(User.id.asc()).all()
    return render_template("users.html", users=users, form=form)

@auth_bp.route("/users/<int:user_id>/toggle", methods=["POST"])
@login_required
@role_required("administrador")
def toggle_user(user_id):
    user = db.session.get(User, user_id)
    if user and user.username != "admin":
        user.activo = not user.activo
        db.session.commit()
        flash(f"Estado del usuario {user.username} actualizado.", "info")
    return redirect(url_for("auth.manage_users"))