"""
    This module defines a customized WTForm base class that trims surrounding
    whitespace from all fields.
"""

from app.util.util import apply_strip
from flask_wtf import FlaskForm



class CustomBaseForm(FlaskForm):
    class Meta:
        def bind_field(self, form, unbound_field, options):
            filters = unbound_field.kwargs.get("filters", [])
            if apply_strip not in filters:
                filters.append(apply_strip)

            return unbound_field.bind(
                filters = filters,
                form = form,
                **options
            )
