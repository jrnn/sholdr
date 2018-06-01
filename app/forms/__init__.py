from app.util.util import apply_strip
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
            if apply_strip not in filters:
                filters.append(apply_strip)

            return unbound_field.bind(
                filters = filters,
                form = form,
                **options
            )
