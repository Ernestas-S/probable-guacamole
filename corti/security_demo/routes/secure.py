# Importing necessary modules
from flask import Blueprint, request, render_template_string
# - Blueprint: Used to modularize the application into components
# - request: Provides access to incoming request data (e.g., query parameters)
# - render_template_string: Renders a string as an HTML template

# Creating a Blueprint instance for the "secure" routes
secure = Blueprint('secure', __name__)
# The 'secure' blueprint groups related routes under a common namespace

@secure.route('/greet')
def greet_secure():
    """
    A route that greets the user by name

    Behavior:
        - Accepts a query parameter `name` from the request
        - If `name` is not provided, defaults to "Guest"
        - Dynamically generates an HTML response using the provided name

    Returns:
        str: A rendered HTML string containing a greeting message
    """
    # Retrieve the 'name' query parameter from the request, defaulting to "Guest" if not provided
    name = request.args.get('name', 'Guest')

    # Define an HTML template with the greeting message
    template = f"<h1>Hello, {name}!</h1>"

    # Render the template and return it as the response
    return render_template_string(template)