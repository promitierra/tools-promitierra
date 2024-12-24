"""
Test configuration module.
"""
import os
import sys
from pathlib import Path

# Add src directory to Python path
src_path = str(Path(__file__).parent.parent)
sys.path.insert(0, src_path)
