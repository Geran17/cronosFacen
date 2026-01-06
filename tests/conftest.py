import sys
from pathlib import Path
import uuid

# Agregar el directorio raíz al path de Python
sys.path.insert(0, str(Path(__file__).parent.parent))


def generate_unique_suffix():
    """Genera un sufijo único para valores que tienen restricciones UNIQUE."""
    return str(uuid.uuid4())[:8]
