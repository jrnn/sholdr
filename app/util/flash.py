"""
    This module collects all flashed messages in one place. The rationale for
    doing so is that many of the messages are recyclable in several places, and
    also that it helps simplify the code in blueprints a little bit.
"""

from flask import flash

error_class = "alert-danger"
success_class = "alert-success"

def create_ok(entity):
    return flash(
        "New {} successfully created, long may they live!".format(entity),
        success_class
    )

def delete_ok(entity):
    return flash(
        "{} irreversibly obliterated, sayonara!".format(entity.capitalize()),
        success_class
    )

def incorrect_type(entity):
    return flash(
        "Incorrect {} type. Stop messing with the address bar!".format(entity),
        error_class
    )

def invalid_input():
    return flash(
        "Check your inputs, Sahib. Something's not right.",
        error_class
    )

def login_error():
    return flash(
        "Something wrong with your credentials, hombre. CAPS LOCK maybe?",
        error_class
    )

def login_ok():
    return flash(
        "You are now logged in. Go wreak some havoc you handsome beast!",
        success_class
    )

def logout_ok():
    return flash(
        "You are now logged out. Hope to see you soon, muchaho!",
        success_class
    )

def update_ok(entity):
    return flash(
        "{} information successfully updated, hooray!".format(entity.capitalize()),
        success_class
    )
