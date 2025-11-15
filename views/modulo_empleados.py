"""
Módulo de Gestión de Empleados - CRUD Completo
Sistema JP Business Solutions
Versión: 2.0
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.config_db import Database
from datetime import datetime

class GestionEmpleados:
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Gestión de Empleados - JP Business Solutions")
        self.ventana.geometry("1300x750")
        self.ventana.configure(bg="#F5F5F5")

        self.empleados = []
        self.empleado_seleccionado = None

        self.crear_interfaz()
        self.cargar_empleados()

    def crear_interfaz(self):
        # Header
        header = tk.Frame(self.ventana, bg="#007BFF", height=70)
        header.pack(fill=tk.X)

        titulo = tk.Label(
            header,
            text="GESTIÓN DE EMPLEADOS",
            font=("Segoe UI", 16, "bold"),
            bg="#007BFF",
            fg="white"
        )
        titulo.pack(pady=20)

        # Contenedor principal
        main_container = tk.Frame(self.ventana, bg="#F5F5F5")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Panel izquierdo - Formulario
        panel_izq = tk.Frame(main_container, bg="white", relief=tk.RAISED, bd=2)
        panel_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        tk.Label(
            panel_izq,
            text="Datos del Empleado",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#007BFF"
        ).pack(pady=10)

        # Frame para campos
        form_frame = tk.Frame(panel_izq, bg="white")
        form_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Campos del formulario
        self.crear_campo(form_frame, "DNI:", 0)
        self.entry_dni = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.entry_dni.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.crear_campo(form_frame, "Nombres:", 1)
        self.entry_nombres = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.entry_nombres.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.crear_campo(form_frame, "Apellido Paterno:", 2)
        self.entry_ap_paterno = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.entry_ap_paterno.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.crear_campo(form_frame, "Apellido Materno:", 3)
        self.entry_ap_materno = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.entry_ap_materno.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        self.crear_campo(form_frame, "Fecha Nacimiento:", 4)
        self.entry_fecha_nac = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.entry_fecha_nac.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        self.entry_fecha_nac.insert(0, "YYYY-MM-DD")

        self.crear_campo(form_frame, "Dirección:", 5)
        self.entry_direccion = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.entry_direccion.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

        self.crear_campo(form_frame, "Distrito:", 6)
        self.entry_distrito = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.entry_distrito.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

        self.crear_campo(form_frame, "Teléfono:", 7)
        self.entry_telefono = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.entry_telefono.grid(row=7, column=1, padx=10, pady=5, sticky="ew")

        self.crear_campo(form_frame, "Email:", 8)
        self.entry_email = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.entry_email.grid(row=8, column=1, padx=10, pady=5, sticky="ew")

        self.crear_campo(form_frame, "Cargo:", 9)
        self.entry_cargo = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.entry_cargo.grid(row=9, column=1, padx=10, pady=5, sticky="ew")

        self.crear_campo(form_frame, "Área:", 10)
        self.entry_area = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.entry_area.grid(row=10, column=1, padx=10, pady=5, sticky="ew")

        self.crear_campo(form_frame, "Fecha Ingreso:", 11)
        self.entry_fecha_ing = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.entry_fecha_ing.grid(row=11, column=1, padx=10, pady=5, sticky="ew")
        self.entry_fecha_ing.insert(0, datetime.now().strftime("%Y-%m-%d"))

        self.crear_campo(form_frame, "Salario (S/):", 12)
        self.entry_salario = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.entry_salario.grid(row=12, column=1, padx=10, pady=5, sticky="ew")

        self.crear_campo(form_frame, "Estado:", 13)
        self.combo_estado = ttk.Combobox(
            form_frame,
            values=["ACTIVO", "INACTIVO", "VACACIONES", "LICENCIA"],
            state="readonly",
            font=("Arial", 10),
            width=28
        )
        self.combo_estado.set("ACTIVO")
        self.combo_estado.grid(row=13, column=1, padx=10, pady=5, sticky="ew")

        # Botones de acción
        btn_frame = tk.Frame(panel_izq, bg="white")
        btn_frame.pack(pady=15)

        btn_style = {
            "font": ("Segoe UI", 10, "bold"),
            "width": 12,
            "cursor": "hand2",
            "bd": 0,
            "relief": "flat"
        }

        btn_nuevo = tk.Button(
            btn_frame,
            text="Nuevo",
            bg="#28A745",
            fg="white",
            command=self.nuevo_empleado,
            **btn_style
        )
        btn_nuevo.grid(row=0, column=0, padx=5)

        btn_guardar = tk.Button(
            btn_frame,
            text="Guardar",
            bg="#007BFF",
            fg="white",
            command=self.guardar_empleado,
            **btn_style
        )
        btn_guardar.grid(row=0, column=1, padx=5)

        btn_actualizar = tk.Button(
            btn_frame,
            text="Actualizar",
            bg="#FFC107",
            fg="black",
            command=self.actualizar_empleado,
            **btn_style
        )
        btn_actualizar.grid(row=0, column=2, padx=5)

        btn_eliminar = tk.Button(
            btn_frame,
            text="Eliminar",
            bg="#DC3545",
            fg="white",
            command=self.eliminar_empleado,
            **btn_style
        )
        btn_eliminar.grid(row=0, column=3, padx=5)

        # Panel derecho - Lista de empleados
        panel_der = tk.Frame(main_container, bg="white", relief=tk.RAISED, bd=2)
        panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(
            panel_der,
            text="Lista de Empleados",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#007BFF"
        ).pack(pady=10)

        # Buscador
        search_frame = tk.Frame(panel_der, bg="white")
        search_frame.pack(pady=5, padx=10, fill=tk.X)

        tk.Label(
            search_frame,
            text="Buscar:",
            font=("Arial", 10),
            bg="white"
        ).pack(side=tk.LEFT, padx=5)

        self.entry_buscar = tk.Entry(search_frame, font=("Arial", 10))
        self.entry_buscar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.entry_buscar.bind('<KeyRelease>', self.buscar_empleado)

        btn_refresh = tk.Button(
            search_frame,
            text="↻",
            font=("Arial", 12, "bold"),
            bg="#007BFF",
            fg="white",
            command=self.cargar_empleados,
            cursor="hand2",
            width=3
        )
        btn_refresh.pack(side=tk.RIGHT, padx=5)

        # Tabla de empleados
        tree_frame = tk.Frame(panel_der, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "DNI", "Nombres", "Cargo", "Área", "Salario", "Estado"),
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            height=18
        )

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        # Configurar columnas
        self.tree.heading("ID", text="ID")
        self.tree.heading("DNI", text="DNI")
        self.tree.heading("Nombres", text="Nombres Completos")
        self.tree.heading("Cargo", text="Cargo")
        self.tree.heading("Área", text="Área")
        self.tree.heading("Salario", text="Salario")
        self.tree.heading("Estado", text="Estado")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("DNI", width=100, anchor="center")
        self.tree.column("Nombres", width=200)
        self.tree.column("Cargo", width=120)
        self.tree.column("Área", width=100)
        self.tree.column("Salario", width=90, anchor="center")
        self.tree.column("Estado", width=90, anchor="center")

        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Event: Seleccionar empleado
        self.tree.bind('<<TreeviewSelect>>', self.seleccionar_empleado)

    def crear_campo(self, parent, texto, fila):
        label = tk.Label(
            parent,
            text=texto,
            font=("Arial", 10, "bold"),
            bg="white",
            anchor="e"
        )
        label.grid(row=fila, column=0, padx=10, pady=5, sticky="e")

    def cargar_empleados(self):
        """Carga todos los empleados desde la base de datos"""
        try:
            self.tree.delete(*self.tree.get_children())

            conn = Database.conectar()
            cursor = conn.cursor()

            query = """
                SELECT
                    id_empleado,
                    dni,
                    CONCAT(nombres, ' ', apellido_paterno, ' ', apellido_materno) AS nombre_completo,
                    cargo,
                    area,
                    CONCAT('S/ ', FORMAT(salario, 2)) AS salario,
                    estado
                FROM empleado
                ORDER BY id_empleado DESC
            """

            cursor.execute(query)
            self.empleados = cursor.fetchall()

            for empleado in self.empleados:
                tags = ('activo',) if empleado[6] == 'ACTIVO' else ('inactivo',)
                self.tree.insert("", tk.END, values=empleado, tags=tags)

            self.tree.tag_configure('activo', foreground='green')
            self.tree.tag_configure('inactivo', foreground='red')

            cursor.close()

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar empleados: {str(e)}")

    def buscar_empleado(self, event=None):
        """Busca empleados por DNI o Nombre"""
        busqueda = self.entry_buscar.get().upper()

        self.tree.delete(*self.tree.get_children())

        for empleado in self.empleados:
            if busqueda in str(empleado[1]).upper() or busqueda in str(empleado[2]).upper():
                tags = ('activo',) if empleado[6] == 'ACTIVO' else ('inactivo',)
                self.tree.insert("", tk.END, values=empleado, tags=tags)

    def seleccionar_empleado(self, event=None):
        """Carga los datos del empleado seleccionado en el formulario"""
        seleccion = self.tree.selection()
        if not seleccion:
            return

        item = self.tree.item(seleccion[0])
        valores = item['values']

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            query = "SELECT * FROM empleado WHERE id_empleado = %s"
            cursor.execute(query, (valores[0],))

            empleado = cursor.fetchone()
            cursor.close()

            if empleado:
                self.empleado_seleccionado = empleado[0]
                self.entry_dni.delete(0, tk.END)
                self.entry_dni.insert(0, empleado[1])
                self.entry_nombres.delete(0, tk.END)
                self.entry_nombres.insert(0, empleado[2])
                self.entry_ap_paterno.delete(0, tk.END)
                self.entry_ap_paterno.insert(0, empleado[3])
                self.entry_ap_materno.delete(0, tk.END)
                self.entry_ap_materno.insert(0, empleado[4])
                self.entry_fecha_nac.delete(0, tk.END)
                self.entry_fecha_nac.insert(0, str(empleado[5]) if empleado[5] else "")
                self.entry_direccion.delete(0, tk.END)
                self.entry_direccion.insert(0, empleado[6] or "")
                self.entry_distrito.delete(0, tk.END)
                self.entry_distrito.insert(0, empleado[7] or "")
                self.entry_telefono.delete(0, tk.END)
                self.entry_telefono.insert(0, empleado[11] or "")
                self.entry_email.delete(0, tk.END)
                self.entry_email.insert(0, empleado[12] or "")
                self.entry_cargo.delete(0, tk.END)
                self.entry_cargo.insert(0, empleado[13] or "")
                self.entry_area.delete(0, tk.END)
                self.entry_area.insert(0, empleado[14] or "")
                self.entry_fecha_ing.delete(0, tk.END)
                self.entry_fecha_ing.insert(0, str(empleado[15]) if empleado[15] else "")
                self.entry_salario.delete(0, tk.END)
                self.entry_salario.insert(0, str(empleado[16]) if empleado[16] else "")
                self.combo_estado.set(empleado[17])

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar empleado: {str(e)}")

    def nuevo_empleado(self):
        """Limpia el formulario para un nuevo empleado"""
        self.empleado_seleccionado = None
        self.entry_dni.delete(0, tk.END)
        self.entry_nombres.delete(0, tk.END)
        self.entry_ap_paterno.delete(0, tk.END)
        self.entry_ap_materno.delete(0, tk.END)
        self.entry_fecha_nac.delete(0, tk.END)
        self.entry_fecha_nac.insert(0, "YYYY-MM-DD")
        self.entry_direccion.delete(0, tk.END)
        self.entry_distrito.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_cargo.delete(0, tk.END)
        self.entry_area.delete(0, tk.END)
        self.entry_fecha_ing.delete(0, tk.END)
        self.entry_fecha_ing.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_salario.delete(0, tk.END)
        self.combo_estado.set("ACTIVO")
        self.entry_dni.focus()

    def validar_dni(self, dni):
        """Valida que el DNI tenga 8 dígitos"""
        return len(dni) == 8 and dni.isdigit()

    def validar_edad(self, fecha_nac):
        """Valida que el empleado sea mayor de 18 años"""
        try:
            if fecha_nac == "YYYY-MM-DD":
                return True
            fecha = datetime.strptime(fecha_nac, "%Y-%m-%d")
            edad = (datetime.now() - fecha).days / 365.25
            return edad >= 18
        except:
            return False

    def guardar_empleado(self):
        """Guarda un nuevo empleado"""
        # Validaciones
        if not self.entry_dni.get() or not self.entry_nombres.get():
            messagebox.showwarning("Advertencia", "DNI y Nombres son obligatorios")
            return

        if not self.validar_dni(self.entry_dni.get()):
            messagebox.showwarning("Advertencia", "El DNI debe tener exactamente 8 dígitos")
            return

        if not self.validar_edad(self.entry_fecha_nac.get()):
            messagebox.showwarning("Advertencia", "El empleado debe ser mayor de 18 años")
            return

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            query = """
                CALL sp_insertar_empleado(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            fecha_nac = None if self.entry_fecha_nac.get() == "YYYY-MM-DD" else self.entry_fecha_nac.get()

            valores = (
                self.entry_dni.get(),
                self.entry_nombres.get(),
                self.entry_ap_paterno.get(),
                self.entry_ap_materno.get(),
                fecha_nac,
                self.entry_direccion.get(),
                self.entry_distrito.get(),
                "",  # provincia
                "",  # departamento
                self.entry_telefono.get(),
                self.entry_email.get(),
                self.entry_cargo.get(),
                self.entry_area.get(),
                self.entry_fecha_ing.get(),
                float(self.entry_salario.get()) if self.entry_salario.get() else 0,
                ""   # observaciones
            )

            cursor.execute(query, valores)
            conn.commit()
            cursor.close()

            messagebox.showinfo("Éxito", "Empleado guardado correctamente")
            self.cargar_empleados()
            self.nuevo_empleado()

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar empleado: {str(e)}")

    def actualizar_empleado(self):
        """Actualiza un empleado existente"""
        if not self.empleado_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un empleado para actualizar")
            return

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            query = """
                CALL sp_actualizar_empleado(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            valores = (
                self.empleado_seleccionado,
                self.entry_dni.get(),
                self.entry_nombres.get(),
                self.entry_ap_paterno.get(),
                self.entry_ap_materno.get(),
                self.entry_direccion.get(),
                self.entry_telefono.get(),
                self.entry_email.get(),
                self.entry_cargo.get(),
                self.entry_area.get(),
                float(self.entry_salario.get()) if self.entry_salario.get() else 0,
                self.combo_estado.get(),
                ""   # observaciones
            )

            cursor.execute(query, valores)
            conn.commit()
            cursor.close()

            messagebox.showinfo("Éxito", "Empleado actualizado correctamente")
            self.cargar_empleados()

        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar empleado: {str(e)}")

    def eliminar_empleado(self):
        """Elimina (desactiva) un empleado"""
        if not self.empleado_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un empleado para eliminar")
            return

        confirmacion = messagebox.askyesno(
            "Confirmar",
            "¿Está seguro de desactivar este empleado?"
        )

        if not confirmacion:
            return

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            query = "CALL sp_eliminar_empleado(%s)"
            cursor.execute(query, (self.empleado_seleccionado,))
            conn.commit()
            cursor.close()

            messagebox.showinfo("Éxito", "Empleado desactivado correctamente")
            self.cargar_empleados()
            self.nuevo_empleado()

        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar empleado: {str(e)}")
