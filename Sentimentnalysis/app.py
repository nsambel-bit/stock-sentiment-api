# Backward compatibility wrapper for the restructured application
# This file maintains compatibility with existing deployment configurations

from src.api import create_app

# Create the Flask app using the new structure
app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
