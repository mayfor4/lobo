import os
import sqlite3
import pytest
from database.db_manager import (
    DB_PATH,
    buscar_materiales,
    restar_material,
    devolver_material,
    obtener_almacen_por_material
)

# -------------------------
# FIXTURE: Base de datos temporal
# -------------------------
@pytest.fixture
def setup_db(tmp_path, monkeypatch):
    """
    Crea una base de datos temporal con la tabla 'inventario' para pruebas.
    """
    test_db = tmp_path / "test.db"

    monkeypatch.setattr("database.db_manager.DB_PATH", str(test_db))

    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()

    # Crear tabla inventario
    cursor.execute("""
        CREATE TABLE inventario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_material TEXT UNIQUE,
            almacen TEXT,
            cantidad_total INTEGER DEFAULT 0,
            cantidad_en_uso INTEGER DEFAULT 0,
            cantidad_disponible INTEGER DEFAULT 0
        );
    """)

    # Inserción de datos de prueba
    cursor.execute("""
        INSERT INTO inventario (nombre_material, almacen, cantidad_total, cantidad_en_uso, cantidad_disponible)
        VALUES 
        ('Arduino', 'LabElectrónica', 10, 2, 8),
        ('Multímetro', 'LabElectrónica', 5, 1, 4),
        ('Probeta', 'LabQuímica', 20, 5, 15);
    """)

    conn.commit()
    conn.close()

    return test_db


# -------------------------
# TEST 1: Buscar materiales
# -------------------------
def test_buscar_materiales(setup_db):
    resultados = buscar_materiales("Ardu")
    assert "Arduino" in resultados
    assert len(resultados) == 1


# -------------------------
# TEST 2: Restar material
# -------------------------
def test_restar_material(setup_db):
    restar_material("Arduino", cantidad=2)

    conn = sqlite3.connect(setup_db)
    cursor = conn.cursor()
    cursor.execute("SELECT cantidad_en_uso, cantidad_disponible FROM inventario WHERE nombre_material=?", ("Arduino",))
    en_uso, disponible = cursor.fetchone()
    conn.close()

    assert en_uso == 4      
    assert disponible == 6  


# -------------------------
# TEST 3: Devolver material
# -------------------------
def test_devolver_material(setup_db):
    devolver_material("Multímetro", cantidad=1)

    conn = sqlite3.connect(setup_db)
    cursor = conn.cursor()
    cursor.execute("SELECT cantidad_en_uso, cantidad_disponible FROM inventario WHERE nombre_material=?", ("Multímetro",))
    en_uso, disponible = cursor.fetchone()
    conn.close()

    assert en_uso == 0     
    assert disponible == 5  


# -------------------------
# TEST 4: Obtener almacén por material
# -------------------------
def test_obtener_almacen_por_material(setup_db):
    assert obtener_almacen_por_material("Arduino") == "LabElectrónica"
    assert obtener_almacen_por_material("Probeta") == "LabQuímica"
    assert obtener_almacen_por_material("Inexistente") == "Desconocido"
