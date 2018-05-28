from flask_wtf import FlaskForm

class CustomBaseForm(FlaskForm):
    """
    Customized WTForm base class, defining behavior that is needed in all forms
    to which it is applied. Namely, (1) disable CSRF, and (2) trim surrounding
    whitespace from all values in a form.
    """
    class Meta:
        csrf = False

        def bind_field(self, form, unbound_field, options):
            filters = unbound_field.kwargs.get("filters", [])
            if stripper not in filters:
                filters.append(stripper)

            return unbound_field.bind(
                filters = filters,
                form = form,
                **options
            )

def stripper(s):
    """
    Apply .strip() to given value if applicable.
    """
    if s is not None and hasattr(s, "strip"):
        return s.strip()
    else:
        return s
