import re

from rest_framework.exceptions import ValidationError


class NoSpecialCharactersValidator:
    """Validator to check if a string does not contain specific special characters."""

    regex = r'%,*+='

    def __call__(self, value):
        name = value.get('name','') # get name from request, default value is empty string
        if re.search(self.regex, name):
            raise ValidationError(
                "The name should not contain any of the following special characters: '%', ',', '*', '+', '=' ."
            )
