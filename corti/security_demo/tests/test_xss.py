# Importing necessary modules
import os
import sys

# Inserting the project root (one level up from tests/) into sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# This ensures that the `app` module and other project files can be imported for testing

import pytest  # Pytest is a testing framework for Python
from app import app as flask_app  # Importing the Flask app instance from the main application file

@pytest.fixture
def client():
    """
    A pytest fixture that provides a test client for the Flask application

    Behavior:
        - Configures the Flask app for testing by setting `TESTING = True`
        - Yields a Flask test client that can be used to simulate HTTP requests

    Returns:
        FlaskClient: A test client for the Flask application
    """
    flask_app.config['TESTING'] = True  # Enable testing mode for Flask
    with flask_app.test_client() as client:
        yield client  # Provide the test client to the test functions

def test_vulnerable_endpoint_allows_script_tags(client):
    """
    Test that the vulnerable endpoint (`/vulnerable/greet`) allows raw <script> tags

    Behavior:
        - Sends a GET request to the `/vulnerable/greet` endpoint with a payload containing <script> tags
        - Verifies that the response contains the raw <script> tags, indicating no sanitization

    Assertions:
        - The payload (including <script> tags) is present in the response
        - The <script> tags are not escaped or removed
    """
    payload = "<script>alert('XSS')</script>"  # Malicious payload
    resp = client.get(f"/vulnerable/greet?name={payload}")  # Send the payload as a query parameter
    data = resp.data.decode('utf-8')  # Decode the response data

    # Ensure the <script> tag is still present in the response
    assert payload in data
    # Ensure the <script> tags are not escaped or removed
    assert "<script>" in data and "</script>" in data

def test_secure_endpoint_strips_script_tags(client):
    """
    Test that the secure endpoint (`/secure/greet`) removes <script> tags via Bleach

    Behavior:
        - Sends a GET request to the `/secure/greet` endpoint with a payload containing <script> tags
        - Verifies that the response does not contain <script> tags, indicating proper sanitization
        - Verifies that the inner text of the <script> tag is either present or HTML-escaped

    Assertions:
        - The <script> tags are not present in the response
        - The inner text of the <script> tag is either present as plain text or HTML-escaped
    """
    payload = "<script>alert('XSS')</script>"  # Malicious payload
    resp = client.get(f"/secure/greet?name={payload}")  # Send the payload as a query parameter
    data = resp.data.decode('utf-8')  # Decode the response data

    # Ensure no <script> tags remain in the response.
    assert "<script>" not in data and "</script>" not in data
    # Ensure the inner text of the <script> tag is present or HTML-escaped.
    assert "alert('XSS')" in data or "alert(&#x27;XSS&#x27;)" in data