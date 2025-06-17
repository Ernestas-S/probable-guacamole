# Importing necessary modules
from flask import Flask  # Flask is a micro web framework for building web applications
from middleware.sanitizer import sanitize_request  # Custom middleware to sanitize incoming requests
from routes.vulnerable import vuln  # Importing the 'vuln' blueprint from the 'routes.vulnerable' module
from routes.secure import secure  # Importing the 'secure' blueprint from the 'routes.secure' module

# Initializing the Flask application
app = Flask(__name__)  # Creates an instance of the Flask application

# Applying middleware
sanitize_request(app, allowed_tags=[], allowed_attrs={})
# The `sanitize_request` function is applied to the app to sanitize incoming requests
# `allowed_tags` and `allowed_attrs` specify which HTML tags and attributes are allowed

# Registering blueprints
app.register_blueprint(vuln, url_prefix='/vulnerable')
# Registers the 'vuln' blueprint under the '/vulnerable' URL prefix
# This means all routes defined in the 'vuln' blueprint will be accessible under '/vulnerable'

app.register_blueprint(secure, url_prefix='/secure')
# Registers the 'secure' blueprint under the '/secure' URL prefix
# This means all routes defined in the 'secure' blueprint will be accessible under '/secure'

# Running the application
if __name__ == '__main__':
    app.run(debug=True)
# This block ensures the application runs only when the script is executed directly
# The `debug=True` option enables debug mode, which provides detailed error messages and auto-reloads the server on code changes