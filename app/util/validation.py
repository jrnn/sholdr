from wtforms.validators import (
    DataRequired,
    Optional,
    Length
)

def max_length(n = 255):
    return Length(
        max = n,
        message = "Max {} characters".format(n)
    )

def not_empty():
    return DataRequired("Cannot be empty")

class RequiredIf(DataRequired):
    """
    Apply 'DataRequired' validator to field only when some other field(s) has a
    certain value, e.g. StringField('', [ RequiredIf(isNew = True) ])
    """
    def __init__(self, message = None, **kwargs):
        super(RequiredIf).__init__()
        self.conds = kwargs
        self.message = message

    def __call__(self, form, field):
        for name, data in self.conds.items():
            other = form._fields.get(name)
            if other.data == data and not field.data:
                DataRequired.__call__(self, form, field)
            Optional()(form, field)
