import sqlite3
import os
import pytest

from database.db_manager import (
    asignar_adeudo,
    quitar_adeudo,
    verificar_adeudo,
    obtener_estado_adeudo,
    DB_PATH
)


@pytest.fixture
def setup_db(tmp_path, monkeypatch):
    """
    Crea una base de datos temporal para las pruebas.
    """
    temp_db = tmp_path / "test.db"

    # Reemplazar temporalmente DB_PATH por la base temporal
    monkeypatch.setattr("database.db_manager.DB_PATH", str(temp_db))

    # Crear tabla usuarios
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            expediente TEXT UNIQUE,
            carrera TEXT,
            adeudo INTEGER DEFAULT 0
        )
    """)

    # Insertar un usuario de prueba
    cursor.execute("""
        INSERT INTO usuarios (username, expediente, carrera, adeudo)
        VALUES ('Juan Perez', '12345', 'Sistemas', 0)
    """)

    conn.commit()
    conn.close()

    return str(temp_db)


def test_asignar_adeudo(setup_db):
    expediente = "12345"

   
    asignar_adeudo(expediente)

    
    assert verificar_adeudo(expediente) is True
    assert obtener_estado_adeudo(expediente) == 1


def test_quitar_adeudo(setup_db):
    expediente = "12345"

   
    asignar_adeudo(expediente)

    
    quitar_adeudo(expediente)

    
    assert verificar_adeudo(expediente) is False
    assert obtener_estado_adeudo(expediente) == 0


def test_verificar_adeudo(setup_db):
    expediente = "12345"

    
    assert verificar_adeudo(expediente) is False

    
    asignar_adeudo(expediente)

    assert verificar_adeudo(expediente) is True


def test_obtener_estado_adeudo(setup_db):
    expediente = "12345"

    
    assert obtener_estado_adeudo(expediente) == 0

    asignar_adeudo(expediente)

   
    assert obtener_estado_adeudo(expediente) == 1
