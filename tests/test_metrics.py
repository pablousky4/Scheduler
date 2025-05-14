# tests/test_metrics.py
from src.proceso import Proceso
from src.scheduler import FCFSScheduler
from src.metrics import calcular_metricas

def test_metricas():
    procs = [Proceso("Z",4,1)]
    gantt = FCFSScheduler().planificar(procs)
    m = calcular_metricas(procs, gantt)
    assert m['respuesta_media'] == 0
    assert m['retorno_medio'] == 4
    assert m['espera_media'] == 0
