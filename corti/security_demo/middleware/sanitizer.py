# Importing necessary modules
import bleach  # Bleach is a library for sanitizing and cleaning HTML input
from flask import request  # Flask's request object provides access to incoming request data

def sanitize_request(app, allowed_tags=None, allowed_attrs=None):
    """
    Attaches a middleware to the Flask app to sanitize incoming request data

    Parameters:
        app (Flask): The Flask application instance
        allowed_tags (list): A list of allowed HTML tags for sanitization. Defaults to an empty list
        allowed_attrs (dict): A dictionary of allowed HTML attributes for sanitization. Defaults to an empty dictionary

    Behavior:
        - Sanitizes query parameters, form data, and path parameters for routes in the "secure" blueprint
        - Uses the `bleach.clean` function to remove disallowed HTML tags and attributes
    """
    # Set default values for allowed_tags and allowed_attrs if not provided
    allowed_tags = allowed_tags or []
    allowed_attrs = allowed_attrs or {}

    @app.before_request
    def _sanitize():
        """
        A Flask `before_request` hook that sanitizes incoming request data
        This function is executed before every request to the app
        """
        # Only sanitize routes in the "secure" blueprint
        if request.blueprint != 'secure':
            return

        # Sanitize query parameters
        for key, val in request.args.items():
            if isinstance(val, str):  # Ensure the value is a string before sanitizing
                request.args = request.args.copy()  # Create a mutable copy of the query parameters
                request.args[key] = bleach.clean(val, tags=allowed_tags, attributes=allowed_attrs)

        # Sanitize form data
        for key, val in request.form.items():
            if isinstance(val, str):  # Ensure the value is a string before sanitizing
                request.form = request.form.copy()  # Create a mutable copy of the form data
                request.form[key] = bleach.clean(val, tags=allowed_tags, attributes=allowed_attrs)

        # Sanitize path parameters
        for key, val in (request.view_args or {}).items():
            if isinstance(val, str):  # Ensure the value is a string before sanitizing
                request.view_args[key] = bleach.clean(val, tags=allowed_tags, attributes=allowed_attrs)