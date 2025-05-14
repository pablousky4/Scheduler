# src/proceso.py
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Proceso:
    pid: str
    duracion: int
    prioridad: int
    tiempo_restante: int = field(init=False)
    tiempo_llegada: int = field(default=0)
    tiempo_inicio: Optional[int] = None
    tiempo_fin: Optional[int] = None

    def __post_init__(self):
        if not self.pid:
            raise ValueError("PID no puede estar vacío")
        if self.duracion <= 0:
            raise ValueError("Duración debe ser un entero positivo")
        self.tiempo_restante = self.duracion
