from flask import flash

error_class = "alert-danger"
success_class = "alert-success"

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

def create_ok(entity):
    return flash(
        "New {} successfully created, hooray!".format(entity),
        success_class
    )

def delete_ok(entity):
    return flash(
        "{} irreversibly obliterated, sayonara!".format(entity.capitalize()),
        success_class
    )

def update_ok(entity):
    return flash(
        "{} information successfully updated!".format(entity.capitalize()),
        success_class
    )
