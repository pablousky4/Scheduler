# tests/test_repositorio.py
import os
import json
import csv
import pytest
from src.proceso import Proceso
from src.repositorio import RepositorioProcesos

@pytest.fixture
def repo(tmp_path):
    r = RepositorioProcesos()
    r.agregar(Proceso("X",1,1))
    return r

def test_agregar_duplicado(repo):
    with pytest.raises(KeyError):
        repo.agregar(Proceso("X",2,2))

def test_eliminar(repo):
    repo.eliminar("X")
    assert repo.listar() == []

def test_json(tmp_path, repo):
    f = tmp_path/"datos.json"
    repo.guardar_json(str(f))
    nuovo = RepositorioProcesos()
    nuovo.cargar_json(str(f))
    assert nuovo.obtener("X").duracion == 1

def test_csv(tmp_path, repo):
    f = tmp_path/"datos.csv"
    repo.guardar_csv(str(f))
    nuevo = RepositorioProcesos()
    nuevo.cargar_csv(str(f))
    assert nuevo.obtener("X").duracion == 1
