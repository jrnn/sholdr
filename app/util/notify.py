"""
    This module collects all flashed messages in one place, most of which are
    recyclable in several places.
"""

from flask import flash

error_class = "alert-danger"
success_class = "alert-success"

def cancel_ok(entity):
    return flash(
        "%s put out of commission permanently, happy retirement!" % entity.capitalize(),
        success_class
    )

def create_ok(entity):
    return flash(
        "New %s successfully created, long may they live!" % entity,
        success_class
    )

def delete_ok(entity):
    return flash(
        "%s irreversibly obliterated, sayonara!" % entity.capitalize(),
        success_class
    )

def delete_error(entity, tied_to):
    return flash(
        "This %s is tied to a %s and cannot be deleted!" % (entity, tied_to),
        error_class
    )

def has_been_canceled(entity):
    return flash(
        "This %s has already been canceled, leave it be!" % entity,
        error_class
    )

def incorrect_type(entity):
    return flash(
        "Incorrect %s type. Stop messing with the address bar!" % entity,
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
        "%s information successfully updated, hooray!" % entity.capitalize(),
        success_class
    )
