import sqlite3
import os
import tempfile
import pytest

# Importamos la función real
from database.db_manager import validar_usuario


# -----------------------------
# FIXTURE: crea BD temporal
# -----------------------------
@pytest.fixture
def temp_db(monkeypatch):
    # Crear archivo temporal
    db_file = tempfile.NamedTemporaryFile(delete=False)
    db_path = db_file.name
    db_file.close()

    # Crear tablas y datos
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Tabla de admin
    cur.execute("""
        CREATE TABLE administradores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            carrera TEXT
        )
    """)

    # Tabla de usuarios
    cur.execute("""
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            expediente TEXT,
            carrera TEXT
        )
    """)

    # Insertar admin de prueba
    cur.execute("""
        INSERT INTO administradores (username, password, carrera)
        VALUES ('admin_test', '1234', 'Sistemas')
    """)

    # Insertar usuario normal
    cur.execute("""
        INSERT INTO usuarios (username, password, expediente, carrera)
        VALUES ('juan', 'abcd', '20231234', 'Industrial')
    """)

    conn.commit()
    conn.close()

    # Forzar DB_PATH → usar bd temporal
    monkeypatch.setattr("database.db_manager.DB_PATH", db_path)

    yield db_path

    # Limpiar archivo
    os.remove(db_path)


# -----------------------------
# PRUEBAS UNITARIAS
# -----------------------------

def test_login_admin_correcto(temp_db):
    usuario = validar_usuario("admin_test", "1234", "admin")
    assert usuario is not None
    assert usuario["rol"] == "admin"
    assert usuario["carrera"] == "Sistemas"


def test_login_admin_incorrecto(temp_db):
    usuario = validar_usuario("admin_test", "0000", "admin")
    assert usuario is None


def test_login_estudiante_correcto(temp_db):
    usuario = validar_usuario("juan", "abcd", "estudiante")
    assert usuario is not None
    assert usuario["rol"] == "usuario"
    assert usuario["expediente"] == "20231234"


def test_login_estudiante_password_incorrecta(temp_db):
    usuario = validar_usuario("juan", "xxxx", "estudiante")
    assert usuario is None


def test_usuario_no_existe(temp_db):
    usuario = validar_usuario("nadie", "0000", "estudiante")
    assert usuario is None
