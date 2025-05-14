# src/repositorio.py
import json
import csv
from typing import List
from .proceso import Proceso

class RepositorioProcesos:
    def __init__(self):
        self._procesos = {}

    def agregar(self, p: Proceso):
        if p.pid in self._procesos:
            raise KeyError(f"Proceso {p.pid} ya existe")
        self._procesos[p.pid] = p

    def listar(self) -> List[Proceso]:
        return list(self._procesos.values())

    def eliminar(self, pid: str):
        if pid not in self._procesos:
            raise KeyError(f"No existe proceso {pid}")
        del self._procesos[pid]

    def obtener(self, pid: str) -> Proceso:
        return self._procesos[pid]

    def guardar_json(self, ruta: str):
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump([vars(p) for p in self.listar()], f, ensure_ascii=False, indent=2)

    def cargar_json(self, ruta: str):
        with open(ruta, encoding='utf-8') as f:
            datos = json.load(f)
        self._procesos.clear()
        for d in datos:
            p = Proceso(d['pid'], d['duracion'], d['prioridad'])
            p.tiempo_restante = d.get('tiempo_restante', p.duracion)
            p.tiempo_llegada = d.get('tiempo_llegada', 0)
            p.tiempo_inicio = d.get('tiempo_inicio')
            p.tiempo_fin = d.get('tiempo_fin')
            self._procesos[p.pid] = p

    def guardar_csv(self, ruta: str):
        with open(ruta, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['pid','duracion','prioridad','tiempo_restante','tiempo_llegada','tiempo_inicio','tiempo_fin'])
            for p in self.listar():
                writer.writerow([p.pid,p.duracion,p.prioridad,p.tiempo_restante,p.tiempo_llegada,p.tiempo_inicio,p.tiempo_fin])

    def cargar_csv(self, ruta: str):
        with open(ruta, encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            self._procesos.clear()
            for row in reader:
                p = Proceso(row['pid'], int(row['duracion']), int(row['prioridad']))
                p.tiempo_restante = int(row['tiempo_restante'])
                p.tiempo_llegada = int(row['tiempo_llegada'])
                p.tiempo_inicio = None if row['tiempo_inicio']=='' else int(row['tiempo_inicio'])
                p.tiempo_fin    = None if row['tiempo_fin']==''    else int(row['tiempo_fin'])
                self._procesos[p.pid] = p
