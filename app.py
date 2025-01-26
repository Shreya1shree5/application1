from flask import Flask, render_template # Import Flask framework and render_template function
import os # Import os module for handling environment variables

app = Flask(__name__) # Create a Flask application instance


@app.route('/') # Define route for the home page
def home():
    return render_template('home.html') # Render and return the home.html template when root URL is accessed


if __name__ == '__main__': # Check if script is being run directly (not imported)
    # Use environment variables with secure defaults
    host = os.getenv('FLASK_HOST', '127.0.0.1')  # Default to localhost # Retrieve host from environment variable, default to localhost if not set
    port = int(os.getenv('FLASK_PORT', 5000))  # Retrieve port from environment variable, convert to integer, default to 5000
    app.run(host=host, port=port)  # Start the Flask development server with specified host and port
    
