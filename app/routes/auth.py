from flask import (
    Blueprint,
    redirect,
    url_for,
    render_template,
    flash,
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user,
)

from app.forms.auth_forms import (
    RegistrationForm,
    LoginForm,
)

from app.services.auth_service import AuthService
from app.services.audit_service import AuditService

auth_bp = Blueprint(
    "auth",
    __name__,
)


# -----------------------------------------
# Home
# -----------------------------------------
@auth_bp.route("/")
def home():

    return redirect(
        url_for("auth.login")
    )


# -----------------------------------------
# Login
# -----------------------------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = AuthService.authenticate(
            form.email.data,
            form.password.data,
        )

        if user:

            login_user(user)

            # Audit Log
            AuditService.log(
                user_id=user.id,
                action="Login",
            )

            flash(
                "Login Successful",
                "success",
            )

            return redirect(
                url_for("dashboard.dashboard")
            )

        flash(
            "Invalid Email or Password",
            "danger",
        )

    return render_template(
        "login.html",
        form=form,
    )


# -----------------------------------------
# Register
# -----------------------------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():

        user = AuthService.register_user(
            form.full_name.data,
            form.email.data,
            form.password.data,
        )

        if user:

            flash(
                "Registration Successful",
                "success",
            )

            return redirect(
                url_for("auth.login")
            )

        flash(
            "Email Already Exists",
            "warning",
        )

    return render_template(
        "register.html",
        form=form,
    )


# -----------------------------------------
# Logout
# -----------------------------------------
@auth_bp.route("/logout")
@login_required
def logout():

    # Audit Log
    AuditService.log(
        user_id=current_user.id,
        action="Logout",
    )

    logout_user()

    flash(
        "Logged Out Successfully",
        "info",
    )

    return redirect(
        url_for("auth.login")
    )