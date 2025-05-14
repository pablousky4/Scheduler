# src/scheduler.py
from abc import ABC, abstractmethod
from typing import List, Tuple
from .proceso import Proceso

GanttEntry = Tuple[str, int, int]

class Scheduler(ABC):
    @abstractmethod
    def planificar(self, procesos: List[Proceso]) -> List[GanttEntry]:
        ...

class FCFSScheduler(Scheduler):
    def planificar(self, procesos):
        tiempo = 0
        gantt = []
        for p in procesos:
            p.tiempo_inicio = tiempo
            tiempo += p.duracion
            p.tiempo_fin = tiempo
            gantt.append((p.pid, p.tiempo_inicio, p.tiempo_fin))
        return gantt

class RoundRobinScheduler(Scheduler):
    def __init__(self, quantum: int):
        if quantum <= 0:
            raise ValueError("Quantum debe ser positivo")
        self.quantum = quantum

    def planificar(self, procesos):
        tiempo = 0
        gantt = []
        queue = procesos.copy()
        while queue:
            p = queue.pop(0)
            if p.tiempo_inicio is None:
                p.tiempo_inicio = tiempo
            ejecutado = min(self.quantum, p.tiempo_restante)
            tiempo += ejecutado
            p.tiempo_restante -= ejecutado
            gantt.append((p.pid, tiempo - ejecutado, tiempo))
            if p.tiempo_restante > 0:
                queue.append(p)
            else:
                p.tiempo_fin = tiempo
        return gantt
