# Root-level app.py for Railway deployment
import sys
import os

# Add the Sentimentnalysis directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Sentimentnalysis'))

# Import and run the actual app
from Sentimentnalysis.src.api import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)