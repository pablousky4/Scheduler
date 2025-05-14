# tests/test_cli.py
import pytest
import sys
import main  # main.py en la raíz


def test_cli_flow(monkeypatch, capsys):
    # Secuencia de opciones para el flujo:
    # 1) Agregar P1, 1) Agregar P2, 2) Listar, 3) Ejecutar FCFS, 7) Salir
    inputs = [
        '1', 'P1', '3', '1',  # agregar proceso P1
        '1', 'P2', '2', '2',  # agregar proceso P2
        '2',                   # listar procesos
        '3',                   # ejecutar FCFS
        '7',                   # salir
    ]
    inputs_iter = iter(inputs)

    def fake_input(prompt=''):
        try:
            return next(inputs_iter)
        except StopIteration:
            pytest.skip("No hay más inputs definidos")

    def fake_exit(code=0):
        raise SystemExit(code)

    # Parchar builtins.input y sys.exit
    monkeypatch.setattr('builtins.input', fake_input)
    monkeypatch.setattr(sys, 'exit', fake_exit)

    # Ejecutar el menú y capturar SystemExit
    with pytest.raises(SystemExit) as exit_exc:
        main.menu()

    # Capturar salida estándar
    captured = capsys.readouterr()
    out = captured.out

    # Verificaciones
    # Debe salir con código 0
    assert exit_exc.value.code == 0

    # La lista debe mencionar P1 y P2
    assert 'P1' in out and 'P2' in out

    # Debe mostrar diagrama de Gantt con P1 y P2 en orden correcto
    assert "('P1', 0, 3)" in out
    assert "('P2', 3, 5)" in out

    # Debe mostrar métricas: respuesta_media, retorno_medio y espera_media
    assert 'Métricas' in out
    assert 'respuesta_media' in out
    assert 'retorno_medio' in out
    assert 'espera_media' in out
