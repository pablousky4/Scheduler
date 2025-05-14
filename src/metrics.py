# src/metrics.py
from typing import List, Tuple
from .proceso import Proceso
from .scheduler import GanttEntry
from src.fcfs_scheduler import FCFSScheduler
from src.scheduler import FCFSScheduler, RoundRobinScheduler
from src.rr_scheduler  import RoundRobinScheduler


def calcular_metricas(procesos: List[Proceso], gantt: List[GanttEntry]):
    # Asumimos tiempo_llegada == 0
    resp = []
    retorno = []
    espera = []
    for p in procesos:
        tr = p.tiempo_inicio - p.tiempo_llegada
        t_ret = p.tiempo_fin - p.tiempo_llegada
        t_esp = t_ret - p.duracion
        resp.append(tr)
        retorno.append(t_ret)
        espera.append(t_esp)
    n = len(procesos)
    return {
        'respuesta_media': sum(resp)/n,
        'retorno_medio': sum(retorno)/n,
        'espera_media': sum(espera)/n
    }
