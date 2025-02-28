from flask import Blueprint, render_template, jsonify, request, session
from extensions import db
from models.user import User
import time
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

retirement_bp = Blueprint("retirement", __name__, url_prefix="/apps/401k")

@retirement_bp.route("/")
def retirement_dashboard():
    if "user" not in session:
        return jsonify({"error": "Not logged in"}), 401
    return render_template("401k.html", username=session["user"])

@retirement_bp.route("/balance")
def get_balance():
    if "user" not in session:
        return jsonify({ "success": False, "error": "Not logged in"}), 401
    
    current_user = User.query.filter_by(username=session["user"]).first()
    if not current_user:
        return jsonify({ "success": False, "error": "User not found"}), 404
            
    return jsonify({ "funds": current_user.funds, "401k_balance": current_user.retirement_funds })

@retirement_bp.route("/contribute", methods=["POST"])
def contribute():
    if "user" not in session:
        return jsonify({"error": "Not logged in"}), 401
        
    data = request.get_json()
    amount = data.get("amount", 0)
    
    username = session["user"]
    current_user: User = User.query.filter_by(username=username).first()
    if not current_user:
        return jsonify({ "success": False, "error": "User not found"}), 404
    
    if amount > current_user.funds:
        return jsonify({
            "message": "Insufficient personal funds for this contribution!", 
            "funds": current_user.funds,
            "401k_balance": current_user.retirement_funds,
        }), 400

    time.sleep(2)

    company_match = amount * 0.5
    total_contribution = amount + company_match

    try:
        db.session.execute(text("UPDATE users SET funds = funds - :amount, retirement_funds = retirement_funds + :total_contribution WHERE username = :username"), {
            "amount": amount,
            "total_contribution": total_contribution,
            "username": username
        })
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "message": "Error processing contribution!", 
            "funds": current_user.funds,
            "401k_balance": current_user.retirement_funds,
        }), 400
        
    return jsonify({
        "message": f"Contributed ${amount}. Employer matched ${company_match}!",
        "funds": current_user.funds,
        "401k_balance": current_user.retirement_funds
    })

@retirement_bp.route("/reset", methods=["POST"])
def reset_account():
    if "user" not in session:
        return jsonify({"error": "Not logged in"}), 401
        

    username = session["user"]
    current_user: User = User.query.filter_by(username=username).first()
    if not current_user:
        return jsonify({ "success": False, "error": "User not found"}), 404
    
    current_user.funds = 10_000
    current_user.retirement_funds = 0
    db.session.commit()

    return jsonify({
        "message": "Account reset successfully!",
        "funds": current_user.funds,
        "401k_balance": current_user.retirement_funds,
    })