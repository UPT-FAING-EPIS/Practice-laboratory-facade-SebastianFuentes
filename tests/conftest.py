"""Archivo de configuración para pytest."""

import sys
import os

# Agregar el directorio src al Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
