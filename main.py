#!/usr/bin/env python3
# main.py
import os
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)
import sys
from src.proceso import Proceso
from src.repositorio import RepositorioProcesos
from src.metrics import calcular_metricas
from src.fcfs_scheduler import FCFSScheduler
from src.rr_scheduler  import RoundRobinScheduler


def menu():
    repo = RepositorioProcesos()
    while True:
        print("\n1) Agregar proceso\n2) Listar procesos\n3) Ejecutar FCFS\n4) Ejecutar RR\n5) Guardar JSON\n6) Cargar JSON\n7) Salir")
        opt = input("> ").strip()
        if opt == '1':
            pid = input("PID: ")
            d = int(input("Duración: "))
            pr = int(input("Prioridad: "))
            repo.agregar(Proceso(pid, d, pr))
        elif opt == '2':
            for p in repo.listar():
                print(f"PID={p.pid}  Dur={p.duracion}  Pri={p.prioridad}  Rest={p.tiempo_restante}")
        elif opt == '3':
            sched = FCFSScheduler()
            gantt = sched.planificar(repo.listar())
            print("Diagrama de Gantt:", gantt)
            print("Métricas:", calcular_metricas(repo.listar(), gantt))
        elif opt == '4':
            q = int(input("Quantum: "))
            sched = RoundRobinScheduler(q)
            gantt = sched.planificar(repo.listar())
            print("Diagrama de Gantt:", gantt)
            print("Métricas:", calcular_metricas(repo.listar(), gantt))
        elif opt == '5':
            nombre = input("Nombre de fichero para guardar (sin .json): ").strip()
            repo.guardar_json(nombre)
            print(f"→ Guardado en data/{nombre}.json")

        elif opt == '6':
            nombre = input("Nombre de fichero para cargar (sin .json): ").strip()
            repo.cargar_json(nombre)
            print(f"→ Cargado desde data/{nombre}.json")
        elif opt == '7':
            print("Saliendo...")
            sys.exit(0)
        else:
            print("Opción inválida, inténtalo de nuevo.")

if __name__ == '__main__':
    menu()
