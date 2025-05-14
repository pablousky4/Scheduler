# src/fcfs_scheduler.py
from typing import List
from .scheduler import Scheduler, GanttEntry
from .proceso import Proceso

class FCFSScheduler(Scheduler):
    def planificar(self, procesos: List[Proceso]) -> List[GanttEntry]:
        tiempo = 0
        gantt = []
        for p in procesos:
            p.tiempo_inicio = tiempo
            tiempo += p.duracion
            p.tiempo_fin = tiempo
            gantt.append((p.pid, p.tiempo_inicio, p.tiempo_fin))
        return gantt
