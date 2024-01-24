import json
from functools import wraps
from typing import Callable, Type

from flask import Response
from flask_wtf import FlaskForm


def validate_input(form_class: Type[FlaskForm]) -> Callable:
    """
    This method makes sure that the required parameters are sent
    and that they are valid
    :param form_class:
    :return:
    """

    def decorator(view_func: Callable) -> Callable:
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            form = form_class(meta={"csrf": False})  # Disable CSRF for JSON requests

            if not form.validate():
                errors = {field.name: field.errors for field in form if field.errors}
                return Response(
                    json.dumps({"message": "Invalid input", "errors": errors}, indent=2),
                    400,
                    headers={"Content-Type": "application/json"},
                )

            return view_func(*args, **kwargs)

        return wrapper

    return decorator
