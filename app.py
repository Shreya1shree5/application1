# Import Flask framework and render_template function
from flask import Flask, render_template
# Import os module for handling environment variables
import os

# Create a Flask application instance
app = Flask(__name__)

# Define route for the home page
@app.route('/')
def home():
    # Render and return the home.html template when root URL is accessed
    return render_template('home.html')

# Check if script is being run directly (not imported)
if __name__ == '__main__':
    # Retrieve host from environment variable, default to localhost if not set
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    
    # Retrieve port from environment variable, convert to integer, default to 5000
    port = int(os.getenv('FLASK_PORT', 5000))
    
    # Start the Flask development server with specified host and port
    app.run(host=host, port=port)