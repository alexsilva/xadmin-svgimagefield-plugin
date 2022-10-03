import sys
import xml.etree.cElementTree as et
from io import BytesIO

from django.core.exceptions import ValidationError
from django.forms import ImageField as DjangoImageField
from django.utils import six


class SVGAndImageFormField(DjangoImageField):

    @classmethod
    def new_class(cls, *bases):
        """Creates a new self class that inherits from bases"""
        bases = (cls,) + bases
        return type(cls.__name__, bases, {})

    def to_python(self, data):
        """
        Checks that the temp_file-upload field data contains a valid image (GIF, JPG,
        PNG, possibly others -- whatever the Python Imaging Library supports).
        """
        f = super(DjangoImageField, self).to_python(data)
        if f is None:
            return None

        from PIL import Image

        # We need to get a temp_file object for Pillow. We might have a path or we might
        # have to read the data into memory.
        if hasattr(data, 'temporary_file_path'):
            temp_file = data.temporary_file_path()
        else:
            if hasattr(data, 'read'):
                temp_file = BytesIO(data.read())
            else:
                temp_file = BytesIO(data['content'])

        try:
            # load() could spot a truncated JPEG, but it loads the entire
            # image in memory, which is a DoS vector. See #3848 and #18520.
            image = Image.open(temp_file)
            # verify() must be called immediately after the constructor.
            image.verify()

            # Annotating so subclasses can reuse it for their own validation
            f.image = image
            # Pillow doesn't detect the MIME type of all formats. In those
            # cases, content_type will be None.
            f.content_type = Image.MIME.get(image.format)
        except Exception:
            # add a workaround to handle svg images
            if not self.is_svg(temp_file):
                # Pillow doesn't recognize it as an image.
                six.reraise(ValidationError, ValidationError(
                    self.error_messages['invalid_image'],
                    code='invalid_image',
                ), sys.exc_info()[2])
        if hasattr(f, 'seek') and callable(f.seek):
            f.seek(0)
        return f

    @staticmethod
    def is_svg(f):
        """
        Check if provided file is svg
        """
        f.seek(0)
        tag = None
        try:
            for event, el in et.iterparse(f, ('start',)):
                tag = el.tag
                break
        except et.ParseError:
            pass
        return tag == '{http://www.w3.org/2000/svg}svg'
