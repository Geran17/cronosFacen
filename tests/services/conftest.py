import pytest
import os
from src.utilidades.config import RUTA_DB_TEST


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Inicializa la BD de prueba una sola vez para toda la sesión."""
    # Crear el directorio si no existe
    os.makedirs(os.path.dirname(RUTA_DB_TEST), exist_ok=True)

    # Limpiar BD anterior si existe
    if os.path.exists(RUTA_DB_TEST):
        try:
            os.remove(RUTA_DB_TEST)
        except:
            pass

    yield

    # Cleanup después de todos los tests
    if os.path.exists(RUTA_DB_TEST):
        try:
            os.remove(RUTA_DB_TEST)
        except:
            pass


@pytest.fixture
def test_db_path():
    """Retorna la ruta de la BD de prueba para usar en los tests."""
    os.makedirs(os.path.dirname(RUTA_DB_TEST), exist_ok=True)
    return RUTA_DB_TEST
