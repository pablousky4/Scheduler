# src/main.py
import sys
from src.proceso import Proceso
from src.repositorio import RepositorioProcesos
from src.scheduler import FCFSScheduler, RoundRobinScheduler
from src.metrics import calcular_metricas

def menu():
    repo = RepositorioProcesos()
    while True:
        print("\n1) Agregar proceso\n2) Listar procesos\n3) Ejecutar FCFS\n4) Ejecutar RR\n5) Guardar JSON\n6) Cargar JSON\n7) Salir")
        opt = input("> ").strip()
        if opt=='1':
            pid = input("PID: "); d=int(input("Duración: ")); pr=int(input("Prioridad: "))
            repo.agregar(Proceso(pid,d,pr))
        elif opt=='2':
            for p in repo.listar():
                print(vars(p))
        elif opt=='3':
            sched = FCFSScheduler()
            gantt = sched.planificar(repo.listar())
            print("Gantt:", gantt)
            print(calcular_metricas(repo.listar(), gantt))
        elif opt=='4':
            q = int(input("Quantum: "))
            sched = RoundRobinScheduler(q)
            gantt = sched.planificar(repo.listar())
            print("Gantt:", gantt)
            print(calcular_metricas(repo.listar(), gantt))
        elif opt=='5':
            repo.guardar_json(input("Ruta JSON: "))
        elif opt=='6':
            repo.cargar_json(input("Ruta JSON: "))
        elif opt=='7':
            sys.exit()
        else:
            print("Opción inválida")

if __name__=='__main__':
    menu()
