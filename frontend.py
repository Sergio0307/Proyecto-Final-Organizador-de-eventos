# frontend.py - VERSIÓN COMPLETA CON ESTRELLA EN CALENDARIO
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import backend
from datetime import datetime
from tkcalendar import Calendar

class AplicacionEventos:
    def __init__(self, gestor_datos, logica_negocio):
        self.gestor = gestor_datos
        self.logica = logica_negocio
        
        self.window = tk.Tk()
        self.window.title("🎬 CINE EVENTOS PRO - Organizador De Eventos Cinematográficos")
        
        self.ancho_pantalla = self.window.winfo_screenwidth()
        self.alto_pantalla = self.window.winfo_screenheight()
        
        self.ancho_ventana = int(self.ancho_pantalla * 0.9)
        self.alto_ventana = int(self.alto_pantalla * 0.9)
        
        pos_x = (self.ancho_pantalla - self.ancho_ventana) // 2
        pos_y = (self.alto_pantalla - self.alto_ventana) // 2
        
        self.window.geometry(f"{self.ancho_ventana}x{self.alto_ventana}+{pos_x}+{pos_y}")
        self.window.resizable(True, True)
        self.window.configure(bg="#1a1a2e")
        self.window.attributes("-alpha", 0.95)
        
        try:
            self.window.iconbitmap('icon.ico')
        except:
            pass
        
        self.window.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
        
        self.window.bind("9", self.toggle_fullscreen)
        self.window.bind("<Key-9>", self.toggle_fullscreen)
        self.window.bind("<KP_9>", self.toggle_fullscreen)
        self.window.bind("<Escape>", self.exit_fullscreen)
        
        self.titulo_font = ("Arial", 20, "bold")
        self.subtitulo_font = ("Arial", 14)
        self.texto_font = ("Arial", 11)
        self.boton_font = ("Arial", 12, "bold")
        
        self.cargar_imagen_fondo()
        self.guardado_automatico()
        self.mostrar_pantalla_inicial()
    
    def cargar_imagen_fondo(self):
        try:
            imagen = Image.open("newcinema.jpg")  
            imagen = imagen.resize((self.ancho_ventana, self.alto_ventana), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(imagen)
        except FileNotFoundError:
            print("Imagen no encontrada, usando fondo blanco")
            self.bg_image = None
    
    def limpiar_pantalla(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        if hasattr(self, 'bg_image') and self.bg_image:
            self.fondo = tk.Label(self.window, image=self.bg_image)
            self.fondo.place(x=0, y=0, relwidth=1, relheight=1)
    
    def mostrar_pantalla_inicial(self):
        self.limpiar_pantalla()
        
        frame_principal = tk.Frame(self.window, bg="white", relief="raised", bd=3)
        frame_principal.place(relx=0.5, rely=0.5, anchor="center", width=800, height=400)
        
        label_titulo = tk.Label(frame_principal, 
            text="🎬 CINE EVENTOS PRO 🎬", 
            font=("Arial", 20, "bold italic"), 
            bg="white", fg="darkblue")
        label_titulo.pack(pady=30)
        
        label_subtitulo = tk.Label(frame_principal, 
            text="Welcome to our Company dedicated to organizing events\ndevoted to Cinema par Excellence", 
            font=("Arial", 14), 
            bg="white", fg="black", justify="center")
        label_subtitulo.pack(pady=10)
        
        ttk.Separator(frame_principal, orient='horizontal').pack(fill='x', pady=20, padx=20)
        
        label_central = tk.Label(frame_principal, 
            text="Join us to create unforgettable cinematic experiences!", 
            font=("Arial", 14, "italic"), 
            bg="white", fg="darkred")
        label_central.pack(pady=20)
        
        boton_continuar = tk.Button(frame_principal, 
            text='START YOUR JOURNEY 🚀', 
            font=("Arial", 16, "bold"), 
            bg="#4CAF50", fg="white", 
            relief='raised',
            bd=3,
            width=25,
            height=2,
            command=self.mostrar_menu_principal)
        boton_continuar.pack(pady=30)
    
    def mostrar_menu_principal(self):
        self.limpiar_pantalla()
        
        frame_menu = tk.Frame(self.window, bg="white", relief="raised", bd=3)
        frame_menu.place(relx=0.5, rely=0.5, anchor="center", width=900, height=500)
        
        titulo_menu = tk.Label(frame_menu,
            text="📋 MAIN MENU - EVENT ORGANIZER",
            font=("Arial", 20, "bold"),
            bg="white", fg="darkblue",
            relief="groove",
            bd=2,
            padx=20,
            pady=10)
        titulo_menu.pack(pady=20)
        
        frame_botones = tk.Frame(frame_menu, bg="white")
        frame_botones.pack(pady=40, padx=50, fill="both", expand=True)
        
        botones_menu = [
            ("🎬 RESOURCE MANAGEMENT", self.mostrar_gestion_recursos),
            ("👥 STAFF MANAGEMENT", self.mostrar_gestion_personal),
            ("📊 SCENE PRODUCTION", self.mostrar_produccion_escenas),
            ("📅 PRODUCTION CALENDAR", self.mostrar_calendario_produccion),
            ("📈 EVENT STATISTICS", self.mostrar_estadisticas),
            ("⚙️ SETTINGS", self.mostrar_configuracion),
            ("🚪 EXIT", self.cerrar_aplicacion)
        ]
        
        for texto, comando in botones_menu:
            boton = tk.Button(frame_botones,
                text=texto,
                font=("Arial", 12, "bold"),
                bg="#2196F3",
                fg="white",
                relief="raised",
                bd=2,
                width=30,
                height=2,
                command=comando)
            boton.pack(pady=8)
    
    def mostrar_gestion_recursos(self):
        self.limpiar_pantalla()
        
        frame_principal = tk.Frame(self.window, bg="white", relief="raised", bd=3)
        frame_principal.place(relx=0.5, rely=0.5, anchor="center", width=1000, height=600)
        
        titulo = tk.Label(frame_principal,
            text="📦 RESOURCE MANAGEMENT",
            font=("Arial", 18, "bold"),
            bg="white", fg="darkgreen")
        titulo.pack(pady=15)
        
        frame_contenedor = tk.Frame(frame_principal, bg="white")
        frame_contenedor.pack(pady=10, padx=10, fill="both", expand=True)
        
        canvas = tk.Canvas(frame_contenedor, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_contenedor, orient="vertical", command=canvas.yview)
        frame_lista = tk.Frame(canvas, bg="white")
        
        frame_lista.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame_lista, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        tk.Label(frame_lista, text="RESOURCE", 
                font=("Arial", 12, "bold"), bg="lightgray", 
                width=50, anchor="w", relief="raised", bd=1).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        tk.Label(frame_lista, text="QUANTITY", 
                font=("Arial", 12, "bold"), bg="lightgray", 
                width=20, relief="raised", bd=1).grid(row=0, column=1, padx=5, pady=5)
        
        recursos = self.gestor.obtener_recursos()
        
        for i, (recurso, cantidad) in enumerate(recursos.items()):
            color_fondo = "#f0f0f0" if i % 2 == 0 else "#ffffff"
            
            tk.Label(frame_lista, text=recurso,
                    font=("Arial", 11), bg=color_fondo, 
                    width=50, anchor="w", relief="groove", bd=1).grid(
                    row=i+1, column=0, padx=5, pady=3, sticky="w")
            tk.Label(frame_lista, text=f"{cantidad} units",
                    font=("Arial", 11, "bold"), bg=color_fondo, 
                    fg="darkgreen", relief="groove", bd=1).grid(
                    row=i+1, column=1, padx=5, pady=3)
        
        frame_lista.grid_columnconfigure(0, weight=1)
        frame_lista.grid_columnconfigure(1, weight=0)
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        frame_botones = tk.Frame(frame_principal, bg="white")
        frame_botones.pack(pady=15)
        
        botones = [
            ("➕ Add Resource", "#4CAF50", self.agregar_recurso),
            ("➖ Remove Resource", "#F44336", self.eliminar_recurso),
            ("🔄 Refresh", "#FF9800", self.mostrar_gestion_recursos),
            ("⬅️ Back to Menu", "#607D8B", self.mostrar_menu_principal)
        ]
        
        for texto, color, comando in botones:
            tk.Button(frame_botones, text=texto,
                     font=("Arial", 11, "bold"),
                     bg=color, fg="white",
                     relief="raised",
                     bd=2,
                     padx=15,
                     pady=8,
                     command=comando).pack(side="left", padx=10)
    
    def mostrar_gestion_personal(self):
        self.limpiar_pantalla()
        
        frame_principal = tk.Frame(self.window, bg="white", relief="raised", bd=3)
        frame_principal.place(relx=0.5, rely=0.5, anchor="center", width=1000, height=600)
        
        titulo = tk.Label(frame_principal,
            text="👥 STAFF MANAGEMENT",
            font=("Arial", 18, "bold"),
            bg="white", fg="darkred")
        titulo.pack(pady=15)
        
        frame_contenedor = tk.Frame(frame_principal, bg="white")
        frame_contenedor.pack(pady=10, padx=10, fill="both", expand=True)
        
        canvas = tk.Canvas(frame_contenedor, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_contenedor, orient="vertical", command=canvas.yview)
        frame_lista = tk.Frame(canvas, bg="white")
        
        frame_lista.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame_lista, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        tk.Label(frame_lista, text="POSITION", 
                font=("Arial", 12, "bold"), bg="lightgray", 
                width=50, anchor="w", relief="raised", bd=1).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        tk.Label(frame_lista, text="STAFF", 
                font=("Arial", 12, "bold"), bg="lightgray", 
                width=20, relief="raised", bd=1).grid(row=0, column=1, padx=5, pady=5)
        
        personal = self.gestor.obtener_personal()
        
        for i, (puesto, cantidad) in enumerate(personal.items()):
            color_fondo = "#f0f0f0" if i % 2 == 0 else "#ffffff"
            
            tk.Label(frame_lista, text=puesto,
                    font=("Arial", 11), bg=color_fondo, 
                    width=50, anchor="w", relief="groove", bd=1).grid(
                    row=i+1, column=0, padx=5, pady=3, sticky="w")
            tk.Label(frame_lista, text=f"{cantidad} people",
                    font=("Arial", 11, "bold"), bg=color_fondo, 
                    fg="darkred", relief="groove", bd=1).grid(
                    row=i+1, column=1, padx=5, pady=3)
        
        frame_lista.grid_columnconfigure(0, weight=1)
        frame_lista.grid_columnconfigure(1, weight=0)
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        frame_botones = tk.Frame(frame_principal, bg="white")
        frame_botones.pack(pady=15)
        
        botones = [
            ("➕ Hire Staff", "#4CAF50", self.agregar_personal),
            ("➖ Dismiss Staff", "#F44336", self.eliminar_personal),
            ("🔄 Refresh", "#FF9800", self.mostrar_gestion_personal),
            ("⬅️ Back to Menu", "#607D8B", self.mostrar_menu_principal)
        ]
        
        for texto, color, comando in botones:
            tk.Button(frame_botones, text=texto,
                     font=("Arial", 11, "bold"),
                     bg=color, fg="white",
                     relief="raised",
                     bd=2,
                     padx=15,
                     pady=8,
                     command=comando).pack(side="left", padx=10)
    
    def mostrar_calendario_produccion(self):
        """Pantalla: Calendario de Producción con estrellas ⭐"""
        self.limpiar_pantalla()
        
        frame_principal = tk.Frame(self.window, bg="white", relief="raised", bd=3)
        frame_principal.place(relx=0.5, rely=0.5, anchor="center", width=1200, height=700)
        
        titulo = tk.Label(frame_principal,
            text="📅 PRODUCTION CALENDAR",
            font=("Arial", 20, "bold"),
            bg="white", fg="#2E86C1")
        titulo.pack(pady=15)
        
        frame_contenido = tk.Frame(frame_principal, bg="white")
        frame_contenido.pack(pady=10, padx=10, fill="both", expand=True)
        
        frame_calendario = tk.Frame(frame_contenido, bg="white", relief="groove", bd=2)
        frame_calendario.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        tk.Label(frame_calendario, text="📅 Select Date", 
                font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        
        self.calendar = Calendar(frame_calendario, 
                                selectmode='day',
                                year=datetime.now().year,
                                month=datetime.now().month,
                                day=datetime.now().day,
                                date_pattern='yyyy-mm-dd',
                                font=("Arial", 10))
        self.calendar.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Configurar marcadores de estrellas para días con producciones
        self.actualizar_marcadores_calendario()
        
        # Actualizar marcadores cuando cambia el mes
        try:
            self.calendar.bind("<<CalendarMonthChanged>>", lambda e: self.actualizar_marcadores_calendario())
        except:
            pass
        
        frame_botones_calendario = tk.Frame(frame_calendario, bg="white")
        frame_botones_calendario.pack(pady=10)
        
        tk.Button(frame_botones_calendario, text="➕ Add New Production",
                 font=("Arial", 11, "bold"),
                 bg="#27AE60", fg="white",
                 command=self.agregar_produccion).pack(side="left", padx=5)
        
        tk.Button(frame_botones_calendario, text="📋 View Day Productions",
                 font=("Arial", 11),
                 bg="#3498DB", fg="white",
                 command=self.ver_producciones_dia).pack(side="left", padx=5)
        
        tk.Button(frame_botones_calendario, text="📅 Go to Today",
                 font=("Arial", 11),
                 bg="#F39C12", fg="white",
                 command=self.ir_a_hoy).pack(side="left", padx=5)
        
        frame_detalles = tk.Frame(frame_contenido, bg="white", relief="groove", bd=2)
        frame_detalles.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        tk.Label(frame_detalles, text="📊 Production Details", 
                font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        
        self.frame_info_dia = tk.Frame(frame_detalles, bg="white")
        self.frame_info_dia.pack(pady=10, padx=10, fill="both", expand=True)
        
        tk.Label(self.frame_info_dia, 
                text="Select a date to view or add productions",
                font=("Arial", 12), 
                bg="white", fg="gray").pack(expand=True)
        
        frame_botones = tk.Frame(frame_principal, bg="white")
        frame_botones.pack(pady=15)
        
        botones = [
            ("🗓️ View Month Productions", "#9B59B6", self.ver_producciones_mes),
            ("📊 Production Statistics", "#F39C12", self.ver_estadisticas_produccion),
            ("🔄 Refresh Calendar", "#FF9800", self.mostrar_calendario_produccion),
            ("⬅️ Back to Menu", "#607D8B", self.mostrar_menu_principal)
        ]
        
        for texto, color, comando in botones:
            tk.Button(frame_botones, text=texto,
                     font=("Arial", 11),
                     bg=color, fg="white",
                     relief="raised",
                     bd=2,
                     padx=10,
                     pady=5,
                     command=comando).pack(side="left", padx=5)
    
    def actualizar_marcadores_calendario(self):
        """Actualiza las estrellas ⭐ en el calendario para días con producciones"""
        producciones = self.gestor.obtener_producciones()
        
        try:
            self.calendar.calevent_remove('all')
        except:
            pass
        
        for fecha, prods in producciones.items():
            try:
                año, mes, dia = map(int, fecha.split('-'))
                fecha_obj = datetime(año, mes, dia)
                
                # Una estrella por día (solo una producción por día)
                self.calendar.calevent_create(fecha_obj, '⭐', 'has_production')
                
            except Exception as e:
                print(f"Error al marcar fecha {fecha}: {e}")
        
        self.calendar.tag_config('has_production', background='#FF6B6B', foreground='white')
    
    def ir_a_hoy(self):
        hoy = datetime.now()
        self.calendar.selection_set(hoy)
        self.ver_producciones_dia()
    
    def ver_producciones_dia(self):
        fecha_seleccionada = self.calendar.get_date()
        
        for widget in self.frame_info_dia.winfo_children():
            widget.destroy()
        
        producciones = self.gestor.obtener_producciones_por_fecha(fecha_seleccionada)
        
        if not producciones:
            tk.Label(self.frame_info_dia, 
                    text=f"No productions scheduled for {fecha_seleccionada}",
                    font=("Arial", 12), 
                    bg="white", fg="gray").pack(expand=True)
            return
        
        tk.Label(self.frame_info_dia, 
                text=f"Productions for {fecha_seleccionada}",
                font=("Arial", 14, "bold"), 
                bg="white", fg="#2E86C1").pack(pady=10)
        
        frame_lista_container = tk.Frame(self.frame_info_dia, bg="white")
        frame_lista_container.pack(fill="both", expand=True, pady=5)
        
        canvas = tk.Canvas(frame_lista_container, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_lista_container, orient="vertical", command=canvas.yview)
        frame_lista = tk.Frame(canvas, bg="white")
        
        frame_lista.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame_lista, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        for i, prod in enumerate(producciones):
            color_fondo = "#E8F4F8" if i % 2 == 0 else "#FFFFFF"
            
            frame_prod = tk.Frame(frame_lista, bg=color_fondo, relief="groove", bd=1)
            frame_prod.pack(fill="x", pady=5, padx=5)
            
            tk.Label(frame_prod, 
                    text=f"🎬 {prod.get('titulo', 'Production')}",
                    font=("Arial", 12, "bold"), 
                    bg=color_fondo, anchor="w").pack(fill="x", padx=10, pady=5)
            
            tk.Label(frame_prod, 
                    text=f"Scene: {prod.get('escena', 'Not specified')}",
                    font=("Arial", 10), 
                    bg=color_fondo, anchor="w").pack(fill="x", padx=10)
            
            tk.Label(frame_prod, 
                    text=f"Duration: {prod.get('duracion_horas', 0)} hours",
                    font=("Arial", 10), 
                    bg=color_fondo, anchor="w").pack(fill="x", padx=10)
            
            tk.Label(frame_prod, 
                    text=f"Status: {prod.get('estado', 'programada')}",
                    font=("Arial", 10), 
                    bg=color_fondo, fg=self.obtener_color_estado(prod.get('estado')),
                    anchor="w").pack(fill="x", padx=10, pady=5)
            
            frame_botones_prod = tk.Frame(frame_prod, bg=color_fondo)
            frame_botones_prod.pack(fill="x", padx=10, pady=5)
            
            tk.Button(frame_botones_prod, text="👁️ View Details",
                     font=("Arial", 9),
                     bg="#3498DB", fg="white",
                     command=lambda p=prod: self.ver_detalles_produccion(p)).pack(side="left", padx=2)
            
            tk.Button(frame_botones_prod, text="✏️ Edit",
                     font=("Arial", 9),
                     bg="#F39C12", fg="white",
                     command=lambda p=prod: self.editar_produccion(p)).pack(side="left", padx=2)
            
            tk.Button(frame_botones_prod, text="❌ Delete",
                     font=("Arial", 9),
                     bg="#E74C3C", fg="white",
                     command=lambda p=prod: self.eliminar_produccion(p)).pack(side="left", padx=2)
    
    def obtener_color_estado(self, estado):
        colores = {
            'programada': '#3498DB',
            'en_progreso': '#F39C12',
            'completada': '#27AE60',
            'cancelada': '#E74C3C'
        }
        return colores.get(estado, '#95A5A6')
    
    def agregar_produccion(self, fecha=None):
        if fecha is None:
            fecha_seleccionada = self.calendar.get_date()
        else:
            fecha_seleccionada = fecha
            año, mes, dia = map(int, fecha_seleccionada.split('-'))
            self.calendar.selection_set(datetime(año, mes, dia))
        
        dialogo = tk.Toplevel(self.window)
        dialogo.title(f"Add Production - {fecha_seleccionada}")
        dialogo.geometry("1100x750")
        dialogo.configure(bg="white")
        dialogo.transient(self.window)
        dialogo.grab_set()
        
        ventana_ancho = 1100
        ventana_alto = 750
        pos_x = (self.window.winfo_screenwidth() - ventana_ancho) // 2
        pos_y = (self.window.winfo_screenheight() - ventana_alto) // 2
        dialogo.geometry(f"{ventana_ancho}x{ventana_alto}+{pos_x}+{pos_y}")
        
        tk.Label(dialogo, text=f"🎬 ADD NEW PRODUCTION\nDate: {fecha_seleccionada}", 
                font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        
        frame_principal_scroll = tk.Frame(dialogo, bg="white")
        frame_principal_scroll.pack(fill="both", expand=True, padx=20, pady=10)
        
        canvas = tk.Canvas(frame_principal_scroll, bg="white", highlightthickness=0)
        scrollbar_y = ttk.Scrollbar(frame_principal_scroll, orient="vertical", command=canvas.yview)
        scrollbar_x = ttk.Scrollbar(frame_principal_scroll, orient="horizontal", command=canvas.xview)
        frame_form = tk.Frame(canvas, bg="white")
        
        frame_form.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame_form, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        
        self.titulo_var = tk.StringVar()
        self.escena_var = tk.StringVar()
        self.duracion_var = tk.IntVar(value=8)
        
        tk.Label(frame_form, text="Production Title:", 
                font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=(10,5))
        entry_titulo = tk.Entry(frame_form, textvariable=self.titulo_var, 
                               font=("Arial", 11), width=80)
        entry_titulo.pack(fill="x", pady=5)
        entry_titulo.focus_set()
        
        tk.Label(frame_form, text="Select Scene:", 
                font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=(10,5))
        
        escenas_disponibles = self.gestor.obtener_escenas()
        if escenas_disponibles:
            self.escena_var.set(escenas_disponibles[0])
            combobox_escena = ttk.Combobox(frame_form, textvariable=self.escena_var,
                                          values=escenas_disponibles, state="readonly",
                                          font=("Arial", 11), width=77)
            combobox_escena.pack(fill="x", pady=5)
            combobox_escena.bind("<<ComboboxSelected>>", 
                                lambda e: self.actualizar_colores_validacion(frame_form, fecha_seleccionada))
        
        tk.Label(frame_form, text="Duration (hours):", 
                font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=(10,5))
        spinbox_duracion = tk.Spinbox(frame_form, from_=1, to=24, 
                                     textvariable=self.duracion_var,
                                     font=("Arial", 11), width=10)
        spinbox_duracion.pack(anchor="w", pady=5)
        
        tk.Label(frame_form, text="Description:", 
                font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=(10,5))
        text_descripcion = tk.Text(frame_form, font=("Arial", 11), 
                                  height=4, width=80)
        text_descripcion.pack(fill="x", pady=5)
        
        # RECURSOS
        frame_recursos_container = tk.LabelFrame(frame_form, text="📦 RESOURCES REQUIRED", 
                                                  font=("Arial", 12, "bold"), bg="white", fg="#2E86C1")
        frame_recursos_container.pack(fill="both", expand=True, pady=15)
        
        canvas_recursos = tk.Canvas(frame_recursos_container, bg="white", highlightthickness=0, height=200)
        scrollbar_recursos = ttk.Scrollbar(frame_recursos_container, orient="vertical", command=canvas_recursos.yview)
        frame_recursos = tk.Frame(canvas_recursos, bg="white")
        
        frame_recursos.bind("<Configure>", lambda e: canvas_recursos.configure(scrollregion=canvas_recursos.bbox("all")))
        canvas_recursos.create_window((0, 0), window=frame_recursos, anchor="nw")
        canvas_recursos.configure(yscrollcommand=scrollbar_recursos.set)
        
        canvas_recursos.pack(side="left", fill="both", expand=True)
        scrollbar_recursos.pack(side="right", fill="y")
        
        recursos_disponibles = self.gestor.obtener_recursos()
        self.vars_recursos = {}
        self.widgets_recursos = {}
        
        for recurso in recursos_disponibles.keys():
            frame_recurso = tk.Frame(frame_recursos, bg="white", relief="groove", bd=1)
            frame_recurso.pack(fill="x", padx=10, pady=3)
            
            label_recurso = tk.Label(frame_recurso, text=recurso, 
                                    font=("Arial", 10), bg="white", width=50, anchor="w")
            label_recurso.pack(side="left", padx=10)
            
            var_cantidad = tk.IntVar(value=0)
            self.vars_recursos[recurso] = var_cantidad
            
            spinbox_cantidad = tk.Spinbox(frame_recurso, from_=0, 
                                         to=recursos_disponibles[recurso],
                                         textvariable=var_cantidad,
                                         font=("Arial", 10), width=8,
                                         command=lambda r=recurso, f=frame_form, d=fecha_seleccionada: 
                                                self.actualizar_colores_validacion(f, d))
            spinbox_cantidad.pack(side="left", padx=10)
            
            label_max = tk.Label(frame_recurso, 
                                text=f"/ {recursos_disponibles[recurso]}",
                                font=("Arial", 9), bg="white", fg="gray")
            label_max.pack(side="left")
            
            self.widgets_recursos[recurso] = {
                'frame': frame_recurso,
                'label': label_recurso,
                'spinbox': spinbox_cantidad,
                'label_max': label_max
            }
        
        # PERSONAL
        frame_personal_container = tk.LabelFrame(frame_form, text="👥 STAFF REQUIRED", 
                                                  font=("Arial", 12, "bold"), bg="white", fg="#9B59B6")
        frame_personal_container.pack(fill="both", expand=True, pady=15)
        
        canvas_personal = tk.Canvas(frame_personal_container, bg="white", highlightthickness=0, height=200)
        scrollbar_personal = ttk.Scrollbar(frame_personal_container, orient="vertical", command=canvas_personal.yview)
        frame_personal = tk.Frame(canvas_personal, bg="white")
        
        frame_personal.bind("<Configure>", lambda e: canvas_personal.configure(scrollregion=canvas_personal.bbox("all")))
        canvas_personal.create_window((0, 0), window=frame_personal, anchor="nw")
        canvas_personal.configure(yscrollcommand=scrollbar_personal.set)
        
        canvas_personal.pack(side="left", fill="both", expand=True)
        scrollbar_personal.pack(side="right", fill="y")
        
        personal_disponible = self.gestor.obtener_personal()
        self.vars_personal = {}
        self.widgets_personal = {}
        
        for puesto in personal_disponible.keys():
            frame_puesto = tk.Frame(frame_personal, bg="white", relief="groove", bd=1)
            frame_puesto.pack(fill="x", padx=10, pady=3)
            
            label_puesto = tk.Label(frame_puesto, text=puesto, 
                                   font=("Arial", 10), bg="white", width=50, anchor="w")
            label_puesto.pack(side="left", padx=10)
            
            var_cantidad = tk.IntVar(value=0)
            self.vars_personal[puesto] = var_cantidad
            
            spinbox_cantidad = tk.Spinbox(frame_puesto, from_=0, 
                                         to=personal_disponible[puesto],
                                         textvariable=var_cantidad,
                                         font=("Arial", 10), width=8,
                                         command=lambda p=puesto, f=frame_form, d=fecha_seleccionada: 
                                                self.actualizar_colores_validacion(f, d))
            spinbox_cantidad.pack(side="left", padx=10)
            
            label_max = tk.Label(frame_puesto, 
                                text=f"/ {personal_disponible[puesto]}",
                                font=("Arial", 9), bg="white", fg="gray")
            label_max.pack(side="left")
            
            self.widgets_personal[puesto] = {
                'frame': frame_puesto,
                'label': label_puesto,
                'spinbox': spinbox_cantidad,
                'label_max': label_max
            }
        
        self.frame_mensaje_validacion = tk.Frame(frame_form, bg="white")
        self.frame_mensaje_validacion.pack(fill="x", pady=10)
        
        frame_botones_dialogo = tk.Frame(frame_form, bg="white")
        frame_botones_dialogo.pack(pady=20)
        
        self.boton_guardar = tk.Button(frame_botones_dialogo, text="💾 Save Production",
                                       font=("Arial", 11, "bold"),
                                       bg="#27AE60", fg="white",
                                       state="disabled",
                                       command=lambda: self.procesar_produccion_guardar(
                                           fecha_seleccionada, dialogo, text_descripcion))
        self.boton_guardar.pack(side="left", padx=10)
        
        tk.Button(frame_botones_dialogo, text="✖️ Cancel",
                 font=("Arial", 11),
                 bg="#95A5A6", fg="white",
                 command=dialogo.destroy).pack(side="left", padx=10)
        
        self.actualizar_colores_validacion(frame_form, fecha_seleccionada)
    
    def actualizar_colores_validacion(self, frame_form, fecha_seleccionada):
        escena = self.escena_var.get()
        
        recursos_seleccionados = {}
        for recurso, var in self.vars_recursos.items():
            cantidad = var.get()
            if cantidad > 0:
                recursos_seleccionados[recurso] = cantidad
        
        personal_seleccionado = {}
        for puesto, var in self.vars_personal.items():
            cantidad = var.get()
            if cantidad > 0:
                personal_seleccionado[puesto] = cantidad
        
        es_valida, errores, estados = self.logica.validar_produccion(
            escena, recursos_seleccionados, personal_seleccionado)
        
        for recurso, widget_dict in self.widgets_recursos.items():
            estado = estados['recursos'].get(recurso, 'opcional')
            label = widget_dict['label']
            spinbox = widget_dict['spinbox']
            
            if estado == 'obligatorio_falta':
                label.config(bg="#FFF3CD", fg="#856404")
                spinbox.config(bg="#FFF3CD")
            elif estado == 'obligatorio_cumplido':
                label.config(bg="#D4EDDA", fg="#155724")
                spinbox.config(bg="#D4EDDA")
            elif estado == 'prohibido':
                label.config(bg="#F8D7DA", fg="#721C24")
                spinbox.config(bg="#F8D7DA", state="disabled")
            else:
                label.config(bg="white", fg="black")
                spinbox.config(bg="white", state="normal")
        
        for puesto, widget_dict in self.widgets_personal.items():
            estado = estados['personal'].get(puesto, 'opcional')
            label = widget_dict['label']
            spinbox = widget_dict['spinbox']
            
            if estado == 'obligatorio_falta':
                label.config(bg="#FFF3CD", fg="#856404")
                spinbox.config(bg="#FFF3CD")
            elif estado == 'obligatorio_cumplido':
                label.config(bg="#D4EDDA", fg="#155724")
                spinbox.config(bg="#D4EDDA")
            elif estado == 'prohibido':
                label.config(bg="#F8D7DA", fg="#721C24")
                spinbox.config(bg="#F8D7DA", state="disabled")
            elif estado == 'conflicto':
                label.config(bg="#F8D7DA", fg="#721C24")
                spinbox.config(bg="#F8D7DA")
            else:
                label.config(bg="white", fg="black")
                spinbox.config(bg="white", state="normal")
        
        for widget in self.frame_mensaje_validacion.winfo_children():
            widget.destroy()
        
        if es_valida:
            tk.Label(self.frame_mensaje_validacion, 
                    text="✅ All requirements met! Ready to save.",
                    font=("Arial", 11, "bold"), bg="white", fg="#27AE60").pack()
            self.boton_guardar.config(state="normal", bg="#27AE60")
        else:
            tk.Label(self.frame_mensaje_validacion, 
                    text="❌ Cannot save production. Fix the following issues:",
                    font=("Arial", 11, "bold"), bg="white", fg="#E74C3C").pack()
            
            for error in errores[:5]:
                tk.Label(self.frame_mensaje_validacion, 
                        text=f"  • {error}",
                        font=("Arial", 10), bg="white", fg="#E74C3C", anchor="w").pack(fill="x")
            
            self.boton_guardar.config(state="disabled", bg="#95A5A6")
    
    def procesar_produccion_guardar(self, fecha_seleccionada, dialogo, text_descripcion):
        titulo = self.titulo_var.get().strip()
        escena = self.escena_var.get()
        duracion = self.duracion_var.get()
        descripcion = text_descripcion.get("1.0", tk.END).strip()
        
        if not titulo:
            messagebox.showerror("Error", "Please enter a production title")
            return
        
        recursos_utilizados = {}
        for recurso, var in self.vars_recursos.items():
            cantidad = var.get()
            if cantidad > 0:
                recursos_utilizados[recurso] = cantidad
        
        personal_asignado = {}
        for puesto, var in self.vars_personal.items():
            cantidad = var.get()
            if cantidad > 0:
                personal_asignado[puesto] = cantidad
        
        if self.gestor.existe_produccion_en_fecha(fecha_seleccionada):
            prod_existente = self.gestor.obtener_produccion_existente_en_fecha(fecha_seleccionada)
            titulo_existente = prod_existente.get('titulo', 'Desconocido')
            messagebox.showerror("Error - Date Conflict", 
                f"❌ Cannot add production on {fecha_seleccionada}\n\n"
                f"⚠️ Already exists: '{titulo_existente}'\n\n"
                f"📌 Only ONE production allowed per day.")
            return
        
        conflictos = self.logica.verificar_conflictos_recursos(
            fecha_seleccionada, recursos_utilizados, personal_asignado)
        
        if conflictos:
            messagebox.showerror("Resource Conflicts", 
                "Cannot save:\n\n" + "\n".join(conflictos))
            return
        
        produccion_data = {
            'titulo': titulo,
            'escena': escena,
            'duracion_horas': duracion,
            'descripcion': descripcion,
            'recursos_utilizados': recursos_utilizados,
            'personal_asignado': personal_asignado,
            'fecha_creacion': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        costo = self.logica.calcular_costo_produccion(produccion_data)
        produccion_data['costo_estimado'] = costo
        
        produccion_id = self.gestor.agregar_produccion(fecha_seleccionada, produccion_data)
        
        if produccion_id:
            messagebox.showinfo("Success", 
                f"✅ '{titulo}' added!\n\n📅 {fecha_seleccionada}\n💰 ${costo:,.2f}\n"
                f"📦 {sum(recursos_utilizados.values())} resources\n👥 {sum(personal_asignado.values())} staff")
            self.actualizar_marcadores_calendario()
            dialogo.destroy()
            self.ver_producciones_dia()
        else:
            messagebox.showerror("Error", "Could not add production")
    
    def ver_detalles_produccion(self, produccion):
        dialogo = tk.Toplevel(self.window)
        dialogo.title(f"🎬 {produccion.get('titulo', 'Details')}")
        dialogo.geometry("800x600")
        dialogo.configure(bg="white")
        dialogo.transient(self.window)
        dialogo.grab_set()
        dialogo.geometry(f"800x600+{self.window.winfo_x()+100}+{self.window.winfo_y()+50}")
        
        frame_container = tk.Frame(dialogo, bg="white")
        frame_container.pack(pady=10, padx=20, fill="both", expand=True)
        
        canvas = tk.Canvas(frame_container, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_container, orient="vertical", command=canvas.yview)
        frame_contenido = tk.Frame(canvas, bg="white")
        
        frame_contenido.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame_contenido, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        tk.Label(frame_contenido, text=f"🎬 {produccion.get('titulo', 'Production')}",
                font=("Arial", 18, "bold"), bg="white", fg="#2E86C1").pack(pady=15)
        
        frame_info = tk.Frame(frame_contenido, bg="white", relief="groove", bd=2)
        frame_info.pack(fill="x", pady=10, padx=10)
        
        tk.Label(frame_info, text="📅 DATE:", font=("Arial", 12, "bold"), 
                bg="white").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        tk.Label(frame_info, text=produccion.get('fecha', 'Unknown'), 
                font=("Arial", 12, "bold"), bg="white", fg="#E74C3C").grid(row=0, column=1, sticky="w", padx=10, pady=5)
        
        fields = [
            ("🎭 Scene:", produccion.get('escena', 'Not specified')),
            ("⏱️ Duration:", f"{produccion.get('duracion_horas', 0)} hours"),
            ("💰 Cost:", f"${produccion.get('costo_estimado', 0):,.2f}"),
            ("📝 Status:", produccion.get('estado', 'programada')),
            ("🆔 ID:", produccion.get('id', 'Unknown'))
        ]
        for i, (l, v) in enumerate(fields, 1):
            tk.Label(frame_info, text=l, font=("Arial", 11, "bold"), 
                    bg="white").grid(row=i, column=0, sticky="w", padx=10, pady=3)
            tk.Label(frame_info, text=v, font=("Arial", 11), 
                    bg="white").grid(row=i, column=1, sticky="w", padx=10, pady=3)
        
        if produccion.get('recursos_utilizados'):
            tk.Label(frame_contenido, text="\n📦 RESOURCES:", 
                    font=("Arial", 12, "bold"), bg="white").pack(anchor="w", padx=10)
            fr = tk.Frame(frame_contenido, bg="#F8F9F9", relief="groove", bd=1)
            fr.pack(fill="x", pady=5, padx=10)
            for r, c in produccion['recursos_utilizados'].items():
                tk.Label(fr, text=f"  • {r}: {c} units", font=("Arial", 10), 
                        bg="#F8F9F9").pack(anchor="w", padx=10, pady=2)
        
        if produccion.get('personal_asignado'):
            tk.Label(frame_contenido, text="\n👥 STAFF:", 
                    font=("Arial", 12, "bold"), bg="white").pack(anchor="w", padx=10)
            fp = tk.Frame(frame_contenido, bg="#F4ECF7", relief="groove", bd=1)
            fp.pack(fill="x", pady=5, padx=10)
            for p, c in produccion['personal_asignado'].items():
                tk.Label(fp, text=f"  • {p}: {c} people", font=("Arial", 10), 
                        bg="#F4ECF7").pack(anchor="w", padx=10, pady=2)
        
        tk.Label(frame_contenido, text="\n📝 DESCRIPTION:", 
                font=("Arial", 12, "bold"), bg="white").pack(anchor="w", padx=10)
        fd = tk.Frame(frame_contenido, bg="#F8F9F9", relief="groove", bd=1)
        fd.pack(fill="x", pady=5, padx=10)
        text_desc = tk.Text(fd, font=("Arial", 10), height=5, wrap="word", bg="#F8F9F9")
        text_desc.insert("1.0", produccion.get('descripcion', 'No description'))
        text_desc.config(state="disabled")
        text_desc.pack(pady=10, padx=10)
        
        frame_botones = tk.Frame(dialogo, bg="white")
        frame_botones.pack(pady=15)
        
        tk.Button(frame_botones, text="📅 Calendar", bg="#3498DB", fg="white",
                 command=lambda: self.ver_en_calendario(produccion)).pack(side="left", padx=5)
        tk.Button(frame_botones, text="✅ Complete", bg="#27AE60", fg="white",
                 command=lambda: self.marcar_completada(produccion)).pack(side="left", padx=5)
        tk.Button(frame_botones, text="🗑️ Delete", bg="#E74C3C", fg="white",
                 command=lambda: self.eliminar_produccion(produccion)).pack(side="left", padx=5)
        tk.Button(frame_botones, text="Close", bg="#95A5A6", fg="white",
                 command=dialogo.destroy).pack(side="left", padx=5)
    
    def editar_produccion(self, produccion):
        messagebox.showinfo("Edit", f"Edit '{produccion.get('titulo')}' - Coming soon")
    
    def eliminar_produccion(self, produccion):
        if messagebox.askyesno("Confirm", f"Delete '{produccion.get('titulo')}'?"):
            if self.gestor.eliminar_produccion(produccion.get('fecha'), produccion.get('id')):
                messagebox.showinfo("Success", "Deleted")
                self.actualizar_marcadores_calendario()
                self.ver_producciones_dia()
    
    def marcar_completada(self, produccion):
        if messagebox.askyesno("Confirm", f"Mark '{produccion.get('titulo')}' as completed?"):
            if self.gestor.actualizar_produccion(produccion.get('fecha'), produccion.get('id'), {'estado': 'completada'}):
                messagebox.showinfo("Success", "Marked as completed")
                self.actualizar_marcadores_calendario()
                self.ver_producciones_dia()
    
    def ver_producciones_mes(self):
        ahora = datetime.now()
        prods = self.gestor.obtener_producciones_por_mes(ahora.year, ahora.month)
        if not prods:
            messagebox.showinfo("Month", f"No productions in {ahora.year}-{ahora.month:02d}")
            return
        dialogo = tk.Toplevel(self.window)
        dialogo.title(f"Productions {ahora.year}-{ahora.month:02d}")
        dialogo.geometry("800x600")
        dialogo.configure(bg="white")
        
        tk.Label(dialogo, text=f"📅 {ahora.year}-{ahora.month:02d}", 
                font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        
        frame = tk.Frame(dialogo, bg="white")
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(frame, bg="white")
        scroll = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        interior = tk.Frame(canvas, bg="white")
        
        interior.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=interior, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        
        total = 0
        for fecha in sorted(prods.keys()):
            tk.Label(interior, text=f"\n📅 {fecha}", font=("Arial", 12, "bold"), 
                    bg="white").pack(anchor="w")
            for p in prods[fecha]:
                total += 1
                frm = tk.Frame(interior, bg="#F8F9F9", relief="groove", bd=1)
                frm.pack(fill="x", pady=3, padx=10)
                tk.Label(frm, text=f"  • {p.get('titulo')}", font=("Arial", 10), 
                        bg="#F8F9F9").pack(anchor="w", padx=10, pady=3)
                tk.Label(frm, text=f"    Scene: {p.get('escena')} | {p.get('duracion_horas')}h | {p.get('estado')}", 
                        font=("Arial", 9), bg="#F8F9F9", fg="gray").pack(anchor="w", padx=10)
        
        tk.Label(interior, text=f"\nTotal: {total}", font=("Arial", 11, "bold"), 
                bg="white").pack(pady=10)
        tk.Button(dialogo, text="Close", command=dialogo.destroy).pack(pady=10)
    
    def ver_estadisticas_produccion(self):
        stats = self.logica.obtener_estadisticas_produccion()
        dialogo = tk.Toplevel(self.window)
        dialogo.title("Production Statistics")
        dialogo.geometry("500x400")
        dialogo.configure(bg="white")
        
        tk.Label(dialogo, text="📊 PRODUCTION STATISTICS", 
                font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        
        frame = tk.Frame(dialogo, bg="white")
        frame.pack(fill="both", expand=True, padx=30, pady=10)
        
        items = [
            ("Total Productions", stats['total_producciones'], "#3498DB"),
            ("Completed", stats['completadas'], "#27AE60"),
            ("Scheduled", stats['programadas'], "#F39C12"),
            ("Total Cost", f"${stats['costo_total']:,.2f}", "#9B59B6"),
            ("Average Cost", f"${stats['costo_promedio']:,.2f}", "#E74C3C")
        ]
        for n, v, c in items:
            frm = tk.Frame(frame, bg="white", relief="ridge", bd=1)
            frm.pack(fill="x", pady=5)
            tk.Label(frm, text=n, font=("Arial", 11), bg="white", width=18, 
                    anchor="w").pack(side="left", padx=10, pady=8)
            tk.Label(frm, text=str(v), font=("Arial", 12, "bold"), 
                    bg="white", fg=c).pack(side="right", padx=10)
        
        tk.Button(dialogo, text="Close", command=dialogo.destroy).pack(pady=15)
    
    def mostrar_produccion_escenas(self):
        self.limpiar_pantalla()
        
        frame_principal = tk.Frame(self.window, bg="white", relief="raised", bd=3)
        frame_principal.place(relx=0.5, rely=0.5, anchor="center", width=1000, height=600)
        
        titulo = tk.Label(frame_principal,
            text="🎬 SCENE PRODUCTION",
            font=("Arial", 18, "bold"),
            bg="white", fg="purple")
        titulo.pack(pady=15)
        
        escenas = self.gestor.obtener_escenas()
        
        frame_contenedor = tk.Frame(frame_principal, bg="white")
        frame_contenedor.pack(pady=10, padx=10, fill="both", expand=True)
        
        canvas = tk.Canvas(frame_contenedor, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_contenedor, orient="vertical", command=canvas.yview)
        frame_contenido = tk.Frame(canvas, bg="white")
        
        frame_contenido.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame_contenido, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        tk.Label(frame_contenido, text="AVAILABLE SCENES:", 
                font=("Arial", 12, "bold"), bg="white").pack(anchor="w", pady=10)
        
        for i, escena in enumerate(escenas):
            frame_escena = tk.Frame(frame_contenido, bg="#f9f7f7", relief="groove", bd=1)
            frame_escena.pack(fill="x", pady=5, padx=5)
            
            tk.Label(frame_escena, text=f"{i+1}. {escena}",
                    font=("Arial", 11), bg="#f9f7f7", anchor="w", 
                    width=70, wraplength=600).pack(side="left", padx=10)
            
            tk.Button(frame_escena, text="❌", 
                     font=("Arial", 8),
                     bg="#FF5252", fg="white",
                     command=lambda idx=i: self.eliminar_escena(idx)).pack(side="right")
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        frame_botones = tk.Frame(frame_principal, bg="white")
        frame_botones.pack(pady=15)
        
        tk.Button(frame_botones, text="➕ Add New Scene",
                 font=("Arial", 11),
                 bg="#4CAF50", fg="white",
                 command=self.agregar_escena).pack(side="left", padx=5)
        
        tk.Button(frame_botones, text="📅 Go to Calendar",
                 font=("Arial", 11),
                 bg="#2E86C1", fg="white",
                 command=self.mostrar_calendario_produccion).pack(side="left", padx=5)
        
        tk.Button(frame_botones, text="⬅️ Back to Menu",
                 font=("Arial", 11),
                 bg="#607D8B", fg="white",
                 command=self.mostrar_menu_principal).pack(side="left", padx=10)
    
    def mostrar_estadisticas(self):
        self.limpiar_pantalla()
        
        frame_principal = tk.Frame(self.window, bg="white", relief="raised", bd=3)
        frame_principal.place(relx=0.5, rely=0.5, anchor="center", width=900, height=500)
        
        titulo = tk.Label(frame_principal,
            text="📈 EVENT STATISTICS",
            font=("Arial", 18, "bold"),
            bg="white", fg="#FF5722")
        titulo.pack(pady=15)
        
        recursos = self.gestor.obtener_recursos()
        personal = self.gestor.obtener_personal()
        escenas = self.gestor.obtener_escenas()
        
        frame_contenido = tk.Frame(frame_principal, bg="white")
        frame_contenido.pack(pady=10, padx=20, fill="both", expand=True)
        
        total_recursos = sum(recursos.values())
        total_personal = sum(personal.values())
        total_escenas = len(escenas)
        
        stats = [
            ("Total Resources", total_recursos, "#4CAF50"),
            ("Total Staff", total_personal, "#2196F3"),
            ("Available Scenes", total_escenas, "#9C27B0"),
            ("Resource Types", len(recursos), "#FF9800"),
            ("Staff Positions", len(personal), "#F44336")
        ]
        
        for nombre, valor, color in stats:
            frame_stat = tk.Frame(frame_contenido, bg="white", relief="groove", bd=2)
            frame_stat.pack(fill="x", pady=8, padx=10)
            tk.Label(frame_stat, text=nombre, 
                    font=("Arial", 12), bg="white", width=25, anchor="w").pack(side="left", padx=10)
            tk.Label(frame_stat, text=str(valor), 
                    font=("Arial", 14, "bold"), bg="white", fg=color).pack(side="right", padx=10)
        
        frame_botones = tk.Frame(frame_principal, bg="white")
        frame_botones.pack(pady=15)
        
        tk.Button(frame_botones, text="🔄 Refresh Stats",
                 font=("Arial", 11),
                 bg="#FF9800", fg="white",
                 command=self.mostrar_estadisticas).pack(side="left", padx=5)
        
        tk.Button(frame_botones, text="⬅️ Back to Menu",
                 font=("Arial", 11),
                 bg="#607D8B", fg="white",
                 command=self.mostrar_menu_principal).pack(side="left", padx=10)
    
    def mostrar_configuracion(self):
        self.limpiar_pantalla()
        
        frame_principal = tk.Frame(self.window, bg="white", relief="raised", bd=3)
        frame_principal.place(relx=0.5, rely=0.5, anchor="center", width=900, height=500)
        
        titulo = tk.Label(frame_principal,
            text="⚙️ SYSTEM SETTINGS",
            font=("Arial", 18, "bold"),
            bg="white", fg="brown")
        titulo.pack(pady=15)
        
        frame_contenido = tk.Frame(frame_principal, bg="white")
        frame_contenido.pack(pady=10, padx=20, fill="both", expand=True)
        
        opciones = [
            ("Interface Theme", "Configure visual theme"),
            ("System Language", "Select language"),
            ("Auto-save", "Enable/disable auto-save"),
            ("Notifications", "Configure alerts"),
            ("Automatic Backup", "Backup settings")
        ]
        
        for opcion, descripcion in opciones:
            frame_opcion = tk.Frame(frame_contenido, bg="white", relief="groove", bd=1)
            frame_opcion.pack(fill="x", pady=6, padx=10)
            tk.Label(frame_opcion, text=opcion,
                    font=("Arial", 12, "bold"), bg="white", width=20, anchor="w").pack(side="left", padx=10)
            tk.Label(frame_opcion, text=descripcion,
                    font=("Arial", 10), bg="white", fg="gray").pack(side="left", padx=10)
            tk.Button(frame_opcion, text="Configure",
                     font=("Arial", 10),
                     bg="#607D8B", fg="white").pack(side="right", padx=10)
        
        frame_botones = tk.Frame(frame_principal, bg="white")
        frame_botones.pack(pady=15)
        
        tk.Button(frame_botones, text="💾 Save Settings",
                 font=("Arial", 11),
                 bg="#795548", fg="white",
                 command=self.guardar_configuracion).pack(side="left", padx=5)
        
        tk.Button(frame_botones, text="⬅️ Back to Menu",
                 font=("Arial", 11),
                 bg="#607D8B", fg="white",
                 command=self.mostrar_menu_principal).pack(side="left", padx=10)
    
    # ========== CRUD ==========
    
    def agregar_recurso(self):
        from tkinter import simpledialog
        nombre = simpledialog.askstring("Add Resource", "Resource name:")
        if not nombre:
            return
        cantidad = simpledialog.askinteger("Add Quantity", "Quantity:")
        if cantidad is None:
            return
        if self.gestor.agregar_recurso(nombre, cantidad):
            messagebox.showinfo("Success", f"✅ '{nombre}' added ({cantidad} units)")
            self.mostrar_gestion_recursos()
    
    def eliminar_recurso(self):
        from tkinter import simpledialog
        recursos = self.gestor.obtener_recursos()
        if not recursos:
            messagebox.showwarning("Warning", "No resources")
            return
        nombre = simpledialog.askstring("Remove Resource", "Resource name:")
        if nombre and nombre in recursos:
            if messagebox.askyesno("Confirm", f"Remove '{nombre}'?"):
                if self.gestor.eliminar_recurso(nombre):
                    messagebox.showinfo("Success", f"'{nombre}' removed")
                    self.mostrar_gestion_recursos()
        elif nombre:
            messagebox.showerror("Error", f"'{nombre}' not found")
    
    def agregar_personal(self):
        from tkinter import simpledialog
        puesto = simpledialog.askstring("Hire Staff", "Position name:")
        if not puesto:
            return
        cantidad = simpledialog.askinteger("Add Staff", "Number:")
        if cantidad is None:
            return
        if self.gestor.agregar_personal(puesto, cantidad):
            messagebox.showinfo("Success", f"✅ '{puesto}' hired ({cantidad} people)")
            self.mostrar_gestion_personal()
    
    def eliminar_personal(self):
        from tkinter import simpledialog
        personal = self.gestor.obtener_personal()
        if not personal:
            messagebox.showwarning("Warning", "No staff")
            return
        puesto = simpledialog.askstring("Dismiss Staff", "Position:")
        if puesto and puesto in personal:
            if messagebox.askyesno("Confirm", f"Dismiss '{puesto}'?"):
                if self.gestor.eliminar_personal(puesto):
                    messagebox.showinfo("Success", f"'{puesto}' dismissed")
                    self.mostrar_gestion_personal()
        elif puesto:
            messagebox.showerror("Error", f"'{puesto}' not found")
    
    def agregar_escena(self):
        from tkinter import simpledialog
        nueva = simpledialog.askstring("Add Scene", "Scene description:")
        if nueva:
            if self.gestor.agregar_escena(nueva):
                messagebox.showinfo("Success", f"✅ '{nueva}' added")
                self.mostrar_produccion_escenas()
    
    def eliminar_escena(self, idx):
        escenas = self.gestor.obtener_escenas()
        if 0 <= idx < len(escenas):
            if messagebox.askyesno("Confirm", f"Remove '{escenas[idx]}'?"):
                if self.gestor.eliminar_escena(idx):
                    messagebox.showinfo("Success", "Scene removed")
                    self.mostrar_produccion_escenas()
    
    def producir_escena(self, tipo):
        messagebox.showinfo("Production", self.logica.producir_escena(tipo))
    
    def ver_en_calendario(self, prod):
        self.mostrar_calendario_produccion()
        try:
            a,m,d = map(int, prod.get('fecha','2024-01-01').split('-'))
            self.calendar.selection_set(datetime(a,m,d))
            self.ver_producciones_dia()
        except:
            pass
    
    def eliminar_produccion_desde_calendario(self, prod):
        if messagebox.askyesno("Confirm", f"Delete '{prod.get('titulo')}'?\nResources will be restored."):
            if self.gestor.eliminar_produccion(prod.get('fecha'), prod.get('id')):
                messagebox.showinfo("Success", "Deleted & resources restored")
                self.actualizar_marcadores_calendario()
                self.ver_producciones_dia()
    
    def guardar_configuracion(self):
        self.gestor.guardar_todo()
        messagebox.showinfo("Settings", "Saved")
    
    def guardado_automatico(self):
        try:
            self.gestor.guardar_todo()
            print("Auto-save completed")
        except Exception as e:
            print(f"Auto-save error: {e}")
        self.window.after(300000, self.guardado_automatico)
    
    def toggle_fullscreen(self, event=None):
        self.window.attributes('-fullscreen', not self.window.attributes('-fullscreen'))
        return "break"
    
    def exit_fullscreen(self, event=None):
        self.window.attributes('-fullscreen', False)
        return "break"
    
    def cerrar_aplicacion(self):
        self.gestor.guardar_todo()
        self.window.quit()
    
    def ejecutar(self):
        self.window.mainloop()