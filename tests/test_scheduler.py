# tests/test_scheduler.py
import pytest
from src.proceso import Proceso
from src.scheduler import FCFSScheduler, RoundRobinScheduler

def make_procs():
    return [Proceso("A",3,1), Proceso("B",2,1), Proceso("C",1,1)]

def test_fcfs():
    procs = make_procs()
    gantt = FCFSScheduler().planificar(procs)
    assert gantt == [("A",0,3),("B",3,5),("C",5,6)]

def test_rr():
    procs = make_procs()
    rr = RoundRobinScheduler(2)
    gantt = rr.planificar(procs)
    # Primer ciclo: A(0-2), B(2-4), C(4-5)
    # Quedan A(1), B(0), C(0) → A(5-6)
    assert gantt == [("A",0,2),("B",2,4),("C",4,5),("A",5,6)]

def test_rr_invalid_quantum():
    with pytest.raises(ValueError):
        RoundRobinScheduler(0)
