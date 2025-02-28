from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db 
from sqlalchemy import CheckConstraint

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    funds = db.Column(db.Float, CheckConstraint('funds >= 0', name="funds_check"), default=10000.0, nullable=False)
    retirement_funds = db.Column(db.Float, CheckConstraint('retirement_funds >= 0', name="retirement_funds_check"), default=0.0, nullable=False) 

    def set_password(self, password):
        """Hashes password and stores it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        """Compares hashed password to user-provided password."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"
