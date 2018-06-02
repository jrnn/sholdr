"""
    This somewhat trivial module just houses bcrypt operations, possibly also
    something else authentication-related in the future(?)
"""

from app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

def checkPassword(password, pw_hash):
    return bcrypt.check_password_hash(pw_hash, password)

def hashPassword(password):
    return bcrypt.generate_password_hash(password).decode("utf-8")
