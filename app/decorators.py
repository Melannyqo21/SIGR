from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user

def role_required(*roles):
    """Restringe el acceso a rutas según el rol del usuario autenticado."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("auth.login"))
            if current_user.rol not in roles:
                flash("No tienes permisos suficientes para realizar esta acción.", "danger")
                return abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator