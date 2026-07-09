from flask import Blueprint
from flask import redirect
from flask import url_for
from flask import render_template
from flask import flash

from flask_login import (
    login_user,
    logout_user,
    login_required,
)

from app.forms.auth_forms import (
    RegistrationForm,
    LoginForm,
)

from app.services.auth_service import AuthService

auth_bp = Blueprint(
    "auth",
    __name__,
)


@auth_bp.route("/")
def home():

    return redirect(
        url_for("auth.login")
    )


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


@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("auth.login")
    )