import sys
import os

# Set the path to the application directory
sys.path.insert(0, os.path.dirname(__file__))

# Import the creates_app factory
from app import create_app

# Create the application object for the WSGI server
application = create_app()
