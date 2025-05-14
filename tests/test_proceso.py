# tests/test_proceso.py
import pytest
from src.proceso import Proceso

def test_creacion_valida():
    p = Proceso("P1", 5, 1)
    assert p.pid == "P1"
    assert p.tiempo_restante == 5

def test_duracion_invalida():
    with pytest.raises(ValueError):
        Proceso("P2", 0, 1)

def test_pid_vacio():
    with pytest.raises(ValueError):
        Proceso("", 3, 1)
