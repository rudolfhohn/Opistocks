"""
Configuration file
Axel Fahy - 21.04.2017
"""
import os

# Debug mode
DEBUG = True

# Port number
PORT = 8080

# Application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Number of threads
THREADS_PER_PAGE = 4

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

