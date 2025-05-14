# src/gui.py
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from .proceso import Proceso
from .repositorio import RepositorioProcesos
from .fcfs_scheduler import FCFSScheduler
from .rr_scheduler import RoundRobinScheduler
from .metrics import calcular_metricas

class SchedulerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scheduler GUI")
        self.geometry("600x400")
        self.resizable(False, False)
        self.repo = RepositorioProcesos()
        self.setup_ui()

    def setup_ui(self):
        # Estilos
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TButton', padding=6, relief='flat', font=('Arial', 10))
        style.configure('TLabel', font=('Arial', 10))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Treeview', font=('Arial', 10), rowheight=24)

        # Frame procesos
        fr_proc = ttk.Frame(self, padding=10)
        fr_proc.pack(fill='x')
        ttk.Label(fr_proc, text="Procesos", style='Header.TLabel').pack(anchor='w')
        cols = ('PID','Dur','Pri','Rest')
        self.tree = ttk.Treeview(fr_proc, columns=cols, show='headings')
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=100, anchor='center')
        self.tree.pack(fill='x', pady=5)

        # Botones
        fr_btn = ttk.Frame(self, padding=10)
        fr_btn.pack(fill='x')
        ttk.Button(fr_btn, text="Agregar", command=self.add_proceso).pack(side='left', padx=5)
        ttk.Button(fr_btn, text="FCFS", command=self.run_fcfs).pack(side='left', padx=5)
        ttk.Button(fr_btn, text="Round-Robin", command=self.run_rr).pack(side='left', padx=5)
        ttk.Button(fr_btn, text="Guardar JSON", command=self.save_json).pack(side='left', padx=5)
        ttk.Button(fr_btn, text="Cargar JSON", command=self.load_json).pack(side='left', padx=5)

        # Output Gantt y métricas
        fr_out = ttk.Frame(self, padding=10)
        fr_out.pack(fill='both', expand=True)
        ttk.Label(fr_out, text="Salida", style='Header.TLabel').pack(anchor='w')
        self.txt = tk.Text(fr_out, height=8, font=('Consolas',10))
        self.txt.pack(fill='both', expand=True, pady=5)

    def refresh_tree(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for p in self.repo.listar():
            self.tree.insert('', 'end', values=(p.pid, p.duracion, p.prioridad, p.tiempo_restante))

    def add_proceso(self):
        pid = simpledialog.askstring("PID","Identificador del proceso:", parent=self)
        if not pid: return
        try:
            dur = simpledialog.askinteger("Duración","Duración (unidades):", parent=self, minvalue=1)
            pri = simpledialog.askinteger("Prioridad","Prioridad (menor más urgente):", parent=self, minvalue=0)
            p = Proceso(pid, dur, pri)
            self.repo.agregar(p)
            self.refresh_tree()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run_fcfs(self):
        gantt = FCFSScheduler().planificar(self.repo.listar())
        mets = calcular_metricas(self.repo.listar(), gantt)
        self.display_output(gantt, mets)

    def run_rr(self):
        q = simpledialog.askinteger("Quantum","Quantum (unidades):", parent=self, minvalue=1)
        if not q: return
        try:
            gantt = RoundRobinScheduler(q).planificar(self.repo.listar())
            mets = calcular_metricas(self.repo.listar(), gantt)
            self.display_output(gantt, mets)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_json(self):
        nombre = simpledialog.askstring("Guardar JSON","Nombre de fichero (sin .json):", parent=self)
        if not nombre: return
        self.repo.guardar_json(nombre)
        messagebox.showinfo("Guardado", f"Guardado en data/{nombre}.json")

    def load_json(self):
        nombre = simpledialog.askstring("Cargar JSON","Nombre de fichero (sin .json):", parent=self)
        if not nombre: return
        try:
            self.repo.cargar_json(nombre)
            self.refresh_tree()
            messagebox.showinfo("Cargado", f"Cargado desde data/{nombre}.json")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_output(self, gantt, metrics):
        self.txt.delete('1.0', tk.END)
        self.txt.insert(tk.END, f"Diagrama de Gantt: {gantt}\n")
        self.txt.insert(tk.END, f"Métricas: {metrics}\n")

if __name__ == '__main__':
    # Asegurar carpeta data en proyecto raíz
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_dir = os.path.join(root_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)

    app = SchedulerApp()
    app.mainloop()
