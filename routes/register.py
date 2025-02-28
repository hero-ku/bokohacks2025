from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models.user import User
from extensions import db

register_bp = Blueprint("register", __name__)

NON_SPECIAL_CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

@register_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        captcha_response = request.form.get("captcha")
        stored_captcha = session.get("captcha_text")

        if not stored_captcha or captcha_response.upper() != stored_captcha:
            flash("Invalid CAPTCHA. Please try again.", "error")
            return redirect(url_for("register.register"))

        session.pop("captcha_text", None)

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Please choose a different one.", "error")
            return redirect(url_for("register.register"))
        
        should_flash = False

        if len(password) < 8:
            should_flash = True
            flash("Password must be at least 8 characters long.", "error")
        if not any(char.isdigit() for char in password):
            should_flash = True
            flash("Password must contain at least one digit.", "error")
        if not any(char.isupper() for char in password):
            should_flash = True
            flash("Password must contain at least one uppercase letter.", "error")
        if not any(char not in NON_SPECIAL_CHARACTERS for char in password):
            should_flash = True
            flash("Password must contain at least one special character.", "error")

        if should_flash:
            return redirect(url_for("register.register"))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("login.login"))

    return render_template("register.html")

