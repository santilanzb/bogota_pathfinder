import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.grid import BogotaGrid
from src.route_optimizer import RouteOptimizer
from src.visualizer import GridVisualizer
from src.location import Location


class PathfinderGUI:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Bogotá Pathfinder - Sistema de Rutas Óptimas")
        self.root.geometry("1400x800")
        self.root.configure(bg='#ecf0f1')
        
        self.grid = BogotaGrid()
        self.optimizer = RouteOptimizer(self.grid)
        self.visualizer = GridVisualizer(self.grid)
        self.current_results = None
        
        self._setup_ui()
        self._display_initial_map()
    
    def _setup_ui(self):
        main_frame = tk.Frame(self.root, bg='#ecf0f1')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        left_panel = tk.Frame(main_frame, bg='#ecf0f1', width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        right_panel = tk.Frame(main_frame, bg='white', relief=tk.RIDGE, borderwidth=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        title = tk.Label(left_panel, text="🏙️ BOGOTÁ PATHFINDER", 
                        font=("Arial", 18, "bold"), bg='#ecf0f1', fg='#2c3e50')
        title.pack(pady=(0, 20))
        
        info_frame = tk.LabelFrame(left_panel, text="📍 Ubicaciones de Origen", 
                                   font=("Arial", 12, "bold"), bg='#ecf0f1', 
                                   fg='#2c3e50', relief=tk.GROOVE, borderwidth=2)
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        javier_info = tk.Label(info_frame, text=f"👨 Javier: {self.grid.javier_home}", 
                              font=("Arial", 10), bg='#ecf0f1', fg='#34495e')
        javier_info.pack(anchor=tk.W, padx=10, pady=5)
        
        andreina_info = tk.Label(info_frame, text=f"👩 Andre\u00edna: {self.grid.andreina_home}", 
                                font=("Arial", 10), bg='#ecf0f1', fg='#34495e')
        andreina_info.pack(anchor=tk.W, padx=10, pady=5)
        
        dest_frame = tk.LabelFrame(left_panel, text="\ud83c\udfaf Establecimientos", 
                                   font=("Arial", 12, "bold"), bg='#ecf0f1', 
                                   fg='#2c3e50', relief=tk.GROOVE, borderwidth=2)
        dest_frame.pack(fill=tk.X, pady=(0, 20))
        
        scroll_container = tk.Frame(dest_frame, bg='#ecf0f1')
        scroll_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=(5, 0))
        
        dest_canvas = tk.Canvas(scroll_container, bg='#ecf0f1', height=180, highlightthickness=0)
        dest_scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=dest_canvas.yview)
        self.dest_scrollable_frame = tk.Frame(dest_canvas, bg='#ecf0f1')
        
        self.dest_scrollable_frame.bind(
            "<Configure>",
            lambda e: dest_canvas.configure(scrollregion=dest_canvas.bbox("all"))
        )
        
        dest_canvas.create_window((0, 0), window=self.dest_scrollable_frame, anchor="nw")
        dest_canvas.configure(yscrollcommand=dest_scrollbar.set)
        
        dest_canvas.pack(side="left", fill="both", expand=True)
        dest_scrollbar.pack(side="right", fill="y")
        
        self.destination_var = tk.StringVar()
        self._update_establishment_list()
        
        btn_frame = tk.Frame(dest_frame, bg='#ecf0f1')
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        add_btn = tk.Button(btn_frame, text="\u2795 Agregar", command=self._add_establishment,
                           font=("Arial", 9, "bold"), bg='#27ae60', fg='white',
                           activebackground='#229954', cursor='hand2', pady=3)
        add_btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        remove_btn = tk.Button(btn_frame, text="\u274c Eliminar", command=self._remove_establishment,
                              font=("Arial", 9, "bold"), bg='#e74c3c', fg='white',
                              activebackground='#c0392b', cursor='hand2', pady=3)
        remove_btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        calc_button = tk.Button(left_panel, text="\ud83d\udd0d Calcular Rutas \u00d3ptimas", 
                               command=self._calculate_routes,
                               font=("Arial", 12, "bold"), bg='#3498db', fg='white',
                               activebackground='#2980b9', activeforeground='white',
                               relief=tk.RAISED, borderwidth=3, cursor='hand2',
                               padx=20, pady=10)
        calc_button.pack(pady=(0, 20))
        
        self.results_frame = tk.LabelFrame(left_panel, text="\ud83d\udcca Resultados", 
                                          font=("Arial", 12, "bold"), bg='#ecf0f1', 
                                          fg='#2c3e50', relief=tk.GROOVE, borderwidth=2)
        self.results_frame.pack(fill=tk.BOTH, expand=True)
        
        scroll_canvas = tk.Canvas(self.results_frame, bg='#ecf0f1', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", command=scroll_canvas.yview)
        self.scrollable_frame = tk.Frame(scroll_canvas, bg='#ecf0f1')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
        )
        
        scroll_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        scroll_canvas.configure(yscrollcommand=scrollbar.set)
        
        scroll_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.graph_frame = right_panel
    
    def _display_initial_map(self):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        fig = self.visualizer.create_figure()
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def _calculate_routes(self):
        destination = self.destination_var.get()
        
        if not destination:
            messagebox.showwarning("Advertencia", "Por favor selecciona un establecimiento")
            return
        
        results = self.optimizer.optimize_routes(destination)
        
        if 'error' in results:
            messagebox.showerror("Error", results['error'])
            return
        
        self.current_results = results
        self._display_results(results)
        self._update_graph(results)
    
    def _display_results(self, results):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        dest_label = tk.Label(self.scrollable_frame, 
                             text=f"\ud83c\udfaf {results['destination']}\\n{results['destination_location']}", 
                             font=("Arial", 11, "bold"), bg='#f39c12', fg='white',
                             relief=tk.RAISED, borderwidth=2, padx=10, pady=8)
        dest_label.pack(fill=tk.X, pady=(5, 15))
        
        javier_frame = tk.Frame(self.scrollable_frame, bg='#3498db', relief=tk.RAISED, borderwidth=2)
        javier_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(javier_frame, text="\ud83d\udc68 JAVIER", font=("Arial", 11, "bold"), 
                bg='#3498db', fg='white').pack(anchor=tk.W, padx=10, pady=(5, 0))
        
        tk.Label(javier_frame, text=f"\u23f1\ufe0f  Tiempo: {results['javier']['time']} minutos", 
                font=("Arial", 9), bg='#3498db', fg='white').pack(anchor=tk.W, padx=10)
        
        tk.Label(javier_frame, text=f"\ud83d\udccd Cuadras: {results['javier']['blocks']}", 
                font=("Arial", 9), bg='#3498db', fg='white').pack(anchor=tk.W, padx=10, pady=(0, 5))
        
        andreina_frame = tk.Frame(self.scrollable_frame, bg='#e74c3c', relief=tk.RAISED, borderwidth=2)
        andreina_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(andreina_frame, text="\ud83d\udc69 ANDRE\u00cdNA", font=("Arial", 11, "bold"), 
                bg='#e74c3c', fg='white').pack(anchor=tk.W, padx=10, pady=(5, 0))
        
        tk.Label(andreina_frame, text=f"\u23f1\ufe0f  Tiempo: {results['andreina']['time']} minutos", 
                font=("Arial", 9), bg='#e74c3c', fg='white').pack(anchor=tk.W, padx=10)
        
        tk.Label(andreina_frame, text=f"\ud83d\udccd Cuadras: {results['andreina']['blocks']}", 
                font=("Arial", 9), bg='#e74c3c', fg='white').pack(anchor=tk.W, padx=10, pady=(0, 5))
        
        sync = results['synchronization']
        sync_frame = tk.Frame(self.scrollable_frame, bg='#2ecc71', relief=tk.RAISED, borderwidth=2)
        sync_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(sync_frame, text="\u23f0 SINCRONIZACI\u00d3N", font=("Arial", 11, "bold"), 
                bg='#2ecc71', fg='white').pack(anchor=tk.W, padx=10, pady=(5, 0))
        
        if sync['first_to_leave'] == 'Ambos':
            sync_text = "\u2705 Ambos salen al mismo tiempo"
        else:
            sync_text = f"\ud83d\udc49 {sync['first_to_leave']} sale primero\\n    ({sync['time_difference']} min antes)"
        
        tk.Label(sync_frame, text=sync_text, font=("Arial", 9), 
                bg='#2ecc71', fg='white').pack(anchor=tk.W, padx=10)
        
        tk.Label(sync_frame, text=f"\ud83d\udd50 Tiempo total: {sync['total_time']} minutos", 
                font=("Arial", 9, "bold"), bg='#2ecc71', fg='white').pack(anchor=tk.W, padx=10, pady=(0, 5))
    
    def _update_graph(self, results):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        fig = self.visualizer.create_figure(results)
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def _update_establishment_list(self):
        for widget in self.dest_scrollable_frame.winfo_children():
            widget.destroy()
        
        for name, location in self.grid.establishments.items():
            rb = tk.Radiobutton(self.dest_scrollable_frame, text=f"{name}\\n    {location}", 
                               variable=self.destination_var, value=name,
                               font=("Arial", 10), bg='#ecf0f1', fg='#2c3e50',
                               selectcolor='#3498db', activebackground='#ecf0f1')
            rb.pack(anchor=tk.W, padx=10, pady=5)
    
    def _add_establishment(self):
        dialog = AddEstablishmentDialog(self.root, self.grid)
        if dialog.result:
            self._update_establishment_list()
            self._display_initial_map()
            # Actualizar la visualización del canvas
            self.dest_scrollable_frame.update_idletasks()
            messagebox.showinfo("\u00c9xito", f"Establecimiento '{dialog.result['name']}' agregado correctamente")
    
    def _remove_establishment(self):
        selected = self.destination_var.get()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un establecimiento para eliminar")
            return
        
        if len(self.grid.establishments) <= 3:
            messagebox.showwarning("Advertencia", "Debe haber al menos 3 establecimientos")
            return
        
        confirm = messagebox.askyesno("Confirmar", f"\u00bfEliminar '{selected}'?")
        if confirm:
            self.grid.remove_establishment(selected)
            self.destination_var.set("")
            self._update_establishment_list()
            self._display_initial_map()
            messagebox.showinfo("\u00c9xito", f"Establecimiento '{selected}' eliminado")


class AddEstablishmentDialog:
    
    def __init__(self, parent, grid):
        self.result = None
        self.grid = grid
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Agregar Establecimiento")
        self.dialog.geometry("400x250")
        self.dialog.configure(bg='#ecf0f1')
        self.dialog.resizable(False, False)
        
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_widgets()
        parent.wait_window(self.dialog)
    
    def _create_widgets(self):
        title = tk.Label(self.dialog, text="\ud83c\udfea Nuevo Establecimiento",
                        font=("Arial", 14, "bold"), bg='#ecf0f1', fg='#2c3e50')
        title.pack(pady=(15, 20))
        
        input_frame = tk.Frame(self.dialog, bg='#ecf0f1')
        input_frame.pack(padx=20, fill=tk.X)
        
        tk.Label(input_frame, text="Nombre:", font=("Arial", 10, "bold"),
                bg='#ecf0f1', fg='#2c3e50').grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = tk.Entry(input_frame, font=("Arial", 10), width=25)
        self.name_entry.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(input_frame, text="Calle (50-55):", font=("Arial", 10, "bold"),
                bg='#ecf0f1', fg='#2c3e50').grid(row=1, column=0, sticky=tk.W, pady=5)
        self.calle_entry = tk.Entry(input_frame, font=("Arial", 10), width=25)
        self.calle_entry.grid(row=1, column=1, pady=5, padx=10)
        
        tk.Label(input_frame, text="Carrera (10-15):", font=("Arial", 10, "bold"),
                bg='#ecf0f1', fg='#2c3e50').grid(row=2, column=0, sticky=tk.W, pady=5)
        self.carrera_entry = tk.Entry(input_frame, font=("Arial", 10), width=25)
        self.carrera_entry.grid(row=2, column=1, pady=5, padx=10)
        
        btn_frame = tk.Frame(self.dialog, bg='#ecf0f1')
        btn_frame.pack(pady=20)
        
        ok_btn = tk.Button(btn_frame, text="\u2705 Agregar", command=self._ok,
                          font=("Arial", 10, "bold"), bg='#27ae60', fg='white',
                          activebackground='#229954', cursor='hand2',
                          padx=20, pady=5)
        ok_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(btn_frame, text="\u274c Cancelar", command=self._cancel,
                              font=("Arial", 10, "bold"), bg='#95a5a6', fg='white',
                              activebackground='#7f8c8d', cursor='hand2',
                              padx=20, pady=5)
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def _ok(self):
        name = self.name_entry.get().strip()
        calle_str = self.calle_entry.get().strip()
        carrera_str = self.carrera_entry.get().strip()
        
        if not name:
            messagebox.showerror("Error", "El nombre no puede estar vac\u00edo")
            return
        
        if name in self.grid.establishments:
            messagebox.showerror("Error", f"Ya existe un establecimiento llamado '{name}'")
            return
        
        try:
            calle = int(calle_str)
            carrera = int(carrera_str)
        except ValueError:
            messagebox.showerror("Error", "Calle y Carrera deben ser n\u00fameros")
            return
        
        if not (self.grid.calle_min <= calle <= self.grid.calle_max):
            messagebox.showerror("Error", f"La calle debe estar entre {self.grid.calle_min} y {self.grid.calle_max}")
            return
        
        if not (self.grid.carrera_min <= carrera <= self.grid.carrera_max):
            messagebox.showerror("Error", f"La carrera debe estar entre {self.grid.carrera_min} y {self.grid.carrera_max}")
            return
        
        # Verificar si la ubicación ya está ocupada
        location = Location(calle, carrera)
        if self.grid.is_location_occupied(location):
            # Identificar qué está ocupando esa ubicación
            if location == self.grid.javier_home:
                messagebox.showerror("Error", f"La ubicación Calle {calle} con Carrera {carrera} está ocupada por la casa de Javier")
            elif location == self.grid.andreina_home:
                messagebox.showerror("Error", f"La ubicación Calle {calle} con Carrera {carrera} está ocupada por la casa de Andreína")
            else:
                # Buscar el nombre del establecimiento en esa ubicación
                for est_name, est_loc in self.grid.establishments.items():
                    if est_loc == location:
                        messagebox.showerror("Error", f"La ubicación Calle {calle} con Carrera {carrera} ya está ocupada por '{est_name}'")
                        break
            return
        
        if self.grid.add_establishment(name, calle, carrera):
            self.result = {'name': name, 'calle': calle, 'carrera': carrera}
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", "No se pudo agregar el establecimiento")
    
    def _cancel(self):
        self.dialog.destroy()
