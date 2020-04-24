# Provides context to import pyspades from testing module when not installed in site-packages

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pyspades