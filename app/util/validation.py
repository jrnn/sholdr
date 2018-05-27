from wtforms import validators

def max_length(n = 255):
    return validators.Length(
        max = n,
        message = "Max {} characters".format(n)
    )

def not_empty():
    return validators.DataRequired("Cannot be empty")
