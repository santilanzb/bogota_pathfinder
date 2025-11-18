import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.grid import BogotaGrid
from src.route_optimizer import RouteOptimizer
from src.visualizer import GridVisualizer


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
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#ecf0f1')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel izquierdo (controles)
        left_panel = tk.Frame(main_frame, bg='#ecf0f1', width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Panel derecho (gráfico)
        right_panel = tk.Frame(main_frame, bg='white', relief=tk.RIDGE, borderwidth=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Título
        title = tk.Label(left_panel, text="🏙️ BOGOTÁ PATHFINDER", 
                        font=("Arial", 18, "bold"), bg='#ecf0f1', fg='#2c3e50')
        title.pack(pady=(0, 20))
        
        # Información de ubicaciones
        info_frame = tk.LabelFrame(left_panel, text="📍 Ubicaciones de Origen", 
                                   font=("Arial", 12, "bold"), bg='#ecf0f1', 
                                   fg='#2c3e50', relief=tk.GROOVE, borderwidth=2)
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        javier_info = tk.Label(info_frame, text=f"👨 Javier: {self.grid.javier_home}", 
                              font=("Arial", 10), bg='#ecf0f1', fg='#34495e')
        javier_info.pack(anchor=tk.W, padx=10, pady=5)
        
        andreina_info = tk.Label(info_frame, text=f"👩 Andreína: {self.grid.andreina_home}", 
                                font=("Arial", 10), bg='#ecf0f1', fg='#34495e')
        andreina_info.pack(anchor=tk.W, padx=10, pady=5)
        
        # Selección de destino
        dest_frame = tk.LabelFrame(left_panel, text="🎯 Seleccionar Destino", 
                                   font=("Arial", 12, "bold"), bg='#ecf0f1', 
                                   fg='#2c3e50', relief=tk.GROOVE, borderwidth=2)
        dest_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.destination_var = tk.StringVar()
        
        for name, location in self.grid.establishments.items():
            rb = tk.Radiobutton(dest_frame, text=f"{name}\n    {location}", 
                               variable=self.destination_var, value=name,
                               font=("Arial", 10), bg='#ecf0f1', fg='#2c3e50',
                               selectcolor='#3498db', activebackground='#ecf0f1')
            rb.pack(anchor=tk.W, padx=10, pady=5)
        
        # Botón calcular
        calc_button = tk.Button(left_panel, text="🔍 Calcular Rutas Óptimas", 
                               command=self._calculate_routes,
                               font=("Arial", 12, "bold"), bg='#3498db', fg='white',
                               activebackground='#2980b9', activeforeground='white',
                               relief=tk.RAISED, borderwidth=3, cursor='hand2',
                               padx=20, pady=10)
        calc_button.pack(pady=(0, 20))
        
        # Resultados
        self.results_frame = tk.LabelFrame(left_panel, text="📊 Resultados", 
                                          font=("Arial", 12, "bold"), bg='#ecf0f1', 
                                          fg='#2c3e50', relief=tk.GROOVE, borderwidth=2)
        self.results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar para resultados
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
        
        # Frame del gráfico
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
        # Limpiar resultados anteriores
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Destino
        dest_label = tk.Label(self.scrollable_frame, 
                             text=f"🎯 {results['destination']}\n{results['destination_location']}", 
                             font=("Arial", 11, "bold"), bg='#f39c12', fg='white',
                             relief=tk.RAISED, borderwidth=2, padx=10, pady=8)
        dest_label.pack(fill=tk.X, pady=(5, 15))
        
        # Información de Javier
        javier_frame = tk.Frame(self.scrollable_frame, bg='#3498db', relief=tk.RAISED, borderwidth=2)
        javier_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(javier_frame, text="👨 JAVIER", font=("Arial", 11, "bold"), 
                bg='#3498db', fg='white').pack(anchor=tk.W, padx=10, pady=(5, 0))
        
        tk.Label(javier_frame, text=f"⏱️  Tiempo: {results['javier']['time']} minutos", 
                font=("Arial", 9), bg='#3498db', fg='white').pack(anchor=tk.W, padx=10)
        
        tk.Label(javier_frame, text=f"📍 Cuadras: {results['javier']['blocks']}", 
                font=("Arial", 9), bg='#3498db', fg='white').pack(anchor=tk.W, padx=10, pady=(0, 5))
        
        # Información de Andreína
        andreina_frame = tk.Frame(self.scrollable_frame, bg='#e74c3c', relief=tk.RAISED, borderwidth=2)
        andreina_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(andreina_frame, text="👩 ANDREÍNA", font=("Arial", 11, "bold"), 
                bg='#e74c3c', fg='white').pack(anchor=tk.W, padx=10, pady=(5, 0))
        
        tk.Label(andreina_frame, text=f"⏱️  Tiempo: {results['andreina']['time']} minutos", 
                font=("Arial", 9), bg='#e74c3c', fg='white').pack(anchor=tk.W, padx=10)
        
        tk.Label(andreina_frame, text=f"📍 Cuadras: {results['andreina']['blocks']}", 
                font=("Arial", 9), bg='#e74c3c', fg='white').pack(anchor=tk.W, padx=10, pady=(0, 5))
        
        # Sincronización
        sync = results['synchronization']
        sync_frame = tk.Frame(self.scrollable_frame, bg='#2ecc71', relief=tk.RAISED, borderwidth=2)
        sync_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(sync_frame, text="⏰ SINCRONIZACIÓN", font=("Arial", 11, "bold"), 
                bg='#2ecc71', fg='white').pack(anchor=tk.W, padx=10, pady=(5, 0))
        
        if sync['first_to_leave'] == 'Ambos':
            sync_text = "✅ Ambos salen al mismo tiempo"
        else:
            sync_text = f"👉 {sync['first_to_leave']} sale primero\n    ({sync['time_difference']} min antes)"
        
        tk.Label(sync_frame, text=sync_text, font=("Arial", 9), 
                bg='#2ecc71', fg='white').pack(anchor=tk.W, padx=10)
        
        tk.Label(sync_frame, text=f"🕐 Tiempo total: {sync['total_time']} minutos", 
                font=("Arial", 9, "bold"), bg='#2ecc71', fg='white').pack(anchor=tk.W, padx=10, pady=(0, 5))
    
    def _update_graph(self, results):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        fig = self.visualizer.create_figure(results)
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
