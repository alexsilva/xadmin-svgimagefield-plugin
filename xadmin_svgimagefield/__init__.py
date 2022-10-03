from django import forms
from xadmin.views import BaseAdminPlugin

from .svgimagefield import SVGAndImageFormField


class SVGAndImagePlugin(BaseAdminPlugin):
    """Plugin that adds support for svg images"""
    has_svgimagefield = True
    exclude_svgimagefield = ()

    def init_request(self, *args, **kwargs):
        return self.has_svgimagefield

    def formfield_for_dbfield(self, formfield, db_field, **kwargs):
        if isinstance(formfield, forms.ImageField) and \
                db_field.name not in self.exclude_svgimagefield:
            attrs = self.admin_view.get_field_attrs(db_field, **kwargs)
            # It inherits from existing classes in order to maintain attributes and styles.
            form_class = attrs.get('form_class', formfield.__class__)

            # new form-class
            attrs['form_class'] = SVGAndImageFormField.new_class(form_class)

            formfield = db_field.formfield(**dict(attrs, **kwargs))
        return formfield
