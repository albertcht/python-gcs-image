"""Add the lib directory to the path, so you can use libraries."""

import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
