import sys
import os
from dotenv import load_dotenv

# Add your project path to the sys.path
path = '/home/yourusername/translate-engine'
if path not in sys.path:
    sys.path.append(path)

# Load environment variables
load_dotenv(os.path.join(path, '.env'))

# Import your app from the app module
from app import app as application

# This is important for PythonAnywhere
application.secret_key = os.getenv('SECRET_KEY', 'dev-key-change-this') 