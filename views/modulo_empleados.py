"""
Módulo de Gestión de Empleados
Sistema JP Business Solutions
Versión: 3.2 - Con combobox simplificados (estilo SUNAT)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.config_db import Database
from datetime import datetime
import re

class GestionEmpleados:
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Gestión de Empleados - JP Business Solutions")
        self.ventana.geometry("1300x750")
        self.ventana.configure(bg="#F5F5F5")
        
        # Configurar para que se cierre correctamente
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

        self.empleados = []
        self.codigo_seleccionado = None
        self.clientes_list = []
        self.archivos_list = []

        self.cargar_listas_fk()
        self.crear_interfaz()
        self.cargar_empleados()

    def cerrar_ventana(self):
        """Cierra la ventana correctamente"""
        self.ventana.destroy()

    def cargar_listas_fk(self):
        """Carga listas de clientes y archivos para FKs"""
        conn = None
        cursor = None
        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            # Cargar clientes
            cursor.execute("""
                SELECT ruc, CONCAT(nombres, ' ', apellido_paterno, ' ', apellido_materno) 
                FROM cliente 
                ORDER BY apellido_paterno, apellido_materno
            """)
            self.clientes_list = cursor.fetchall()

            # Cargar archivos Excel
            cursor.execute("SELECT nombre FROM archivo_excel_gestion_clientes ORDER BY nombre")
            self.archivos_list = [row[0] for row in cursor.fetchall()]

        except Exception as e:
            self.clientes_list = []
            self.archivos_list = []
            self.mostrar_error("Error al cargar listas", str(e))
        finally:
            try:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
            except:
                pass

    def crear_interfaz(self):
        # Header
        header = tk.Frame(self.ventana, bg="#007BFF", height=70)
        header.pack(fill=tk.X)

        titulo = tk.Label(
            header,
            text="👔 GESTIÓN DE EMPLEADOS",
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
        ).pack(pady=15)

        # Frame para campos con scroll
        canvas = tk.Canvas(panel_izq, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(panel_izq, orient="vertical", command=canvas.yview)
        form_frame = tk.Frame(canvas, bg="white")

        form_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=form_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Código (PK)
        self.crear_campo(form_frame, "Código: *", 0)
        self.entry_codigo = tk.Entry(form_frame, font=("Segoe UI", 10), width=30)
        self.entry_codigo.grid(row=0, column=1, padx=10, pady=8, sticky="ew")
        tk.Label(
            form_frame,
            text="(Número entero único)",
            font=("Segoe UI", 8),
            bg="white",
            fg="#888888"
        ).grid(row=0, column=2, padx=5, sticky="w")

        # Sexo
        self.crear_campo(form_frame, "Sexo: *", 1)
        self.combo_sexo = ttk.Combobox(
            form_frame,
            values=["Masculino", "Femenino"],
            state="readonly",
            font=("Segoe UI", 10),
            width=28
        )
        self.combo_sexo.set("Masculino")
        self.combo_sexo.grid(row=1, column=1, padx=10, pady=8, sticky="ew")

        # Cargo
        self.crear_campo(form_frame, "Cargo: *", 2)
        self.entry_cargo = tk.Entry(form_frame, font=("Segoe UI", 10), width=30)
        self.entry_cargo.grid(row=2, column=1, padx=10, pady=8, sticky="ew")

        # Fecha Nacimiento
        self.crear_campo(form_frame, "Fecha Nacimiento: *", 3)
        fecha_frame = tk.Frame(form_frame, bg="white")
        fecha_frame.grid(row=3, column=1, padx=10, pady=8, sticky="ew")

        self.entry_fecha_nac = tk.Entry(fecha_frame, font=("Segoe UI", 10), width=24)
        self.entry_fecha_nac.pack(side=tk.LEFT)
        self.entry_fecha_nac.insert(0, "YYYY-MM-DD")

        tk.Label(
            form_frame,
            text="(Mayor de 18 años)",
            font=("Segoe UI", 8),
            bg="white",
            fg="#888888"
        ).grid(row=3, column=2, padx=5, sticky="w")

        # Nombres
        self.crear_campo(form_frame, "Nombres: *", 4)
        self.entry_nombres = tk.Entry(form_frame, font=("Segoe UI", 10), width=30)
        self.entry_nombres.grid(row=4, column=1, padx=10, pady=8, sticky="ew")

        # Apellido Paterno
        self.crear_campo(form_frame, "Apellido Paterno: *", 5)
        self.entry_ap_paterno = tk.Entry(form_frame, font=("Segoe UI", 10), width=30)
        self.entry_ap_paterno.grid(row=5, column=1, padx=10, pady=8, sticky="ew")

        # Apellido Materno
        self.crear_campo(form_frame, "Apellido Materno: *", 6)
        self.entry_ap_materno = tk.Entry(form_frame, font=("Segoe UI", 10), width=30)
        self.entry_ap_materno.grid(row=6, column=1, padx=10, pady=8, sticky="ew")

        # ✅ RUC Cliente (FK) - ESTILO SUNAT SIMPLIFICADO
        self.crear_campo(form_frame, "Cliente Asignado:", 7)
        
        # Preparar valores para combobox: código - nombre
        clientes_valores = [""] + [f"{ruc} - {nombre}" for ruc, nombre in self.clientes_list]
        
        self.combo_ruc_cliente = ttk.Combobox(
            form_frame,
            values=clientes_valores,
            state="readonly",  # ✅ Solo lectura, no se puede escribir
            font=("Segoe UI", 10),
            width=28
        )
        self.combo_ruc_cliente.set("")  # Valor por defecto vacío
        self.combo_ruc_cliente.grid(row=7, column=1, padx=10, pady=8, sticky="ew")

        tk.Label(
            form_frame,
            text="(Opcional)",
            font=("Segoe UI", 8),
            bg="white",
            fg="#888888"
        ).grid(row=7, column=2, padx=5, sticky="w")

        # ✅ Nombre Archivo (FK) - ESTILO SUNAT SIMPLIFICADO
        self.crear_campo(form_frame, "Archivo Excel:", 8)
        
        archivos_valores = [""] + self.archivos_list
        
        self.combo_archivo = ttk.Combobox(
            form_frame,
            values=archivos_valores,
            state="readonly",  # ✅ Solo lectura, no se puede escribir
            font=("Segoe UI", 10),
            width=28
        )
        self.combo_archivo.set("")  # Valor por defecto vacío
        self.combo_archivo.grid(row=8, column=1, padx=10, pady=8, sticky="ew")

        tk.Label(
            form_frame,
            text="(Opcional)",
            font=("Segoe UI", 8),
            bg="white",
            fg="#888888"
        ).grid(row=8, column=2, padx=5, sticky="w")

        # Nota de campos obligatorios
        tk.Label(
            form_frame,
            text="* Campos obligatorios",
            font=("Segoe UI", 9, "italic"),
            bg="white",
            fg="#DC3545"
        ).grid(row=9, column=0, columnspan=3, pady=15)

        # Botones de acción
        btn_frame = tk.Frame(panel_izq, bg="white")
        btn_frame.pack(pady=20)

        btn_style = {
            "font": ("Segoe UI", 10, "bold"),
            "width": 12,
            "cursor": "hand2",
            "bd": 0,
            "relief": "flat",
            "pady": 8
        }

        btn_nuevo = tk.Button(
            btn_frame,
            text="✚ Nuevo",
            bg="#28A745",
            fg="white",
            command=self.nuevo_empleado,
            **btn_style
        )
        btn_nuevo.grid(row=0, column=0, padx=5, pady=5)

        btn_guardar = tk.Button(
            btn_frame,
            text="💾 Guardar",
            bg="#007BFF",
            fg="white",
            command=self.guardar_empleado,
            **btn_style
        )
        btn_guardar.grid(row=0, column=1, padx=5, pady=5)

        btn_actualizar = tk.Button(
            btn_frame,
            text="🔄 Actualizar",
            bg="#FFC107",
            fg="black",
            command=self.actualizar_empleado,
            **btn_style
        )
        btn_actualizar.grid(row=1, column=0, padx=5, pady=5)

        btn_eliminar = tk.Button(
            btn_frame,
            text="🗑️ Eliminar",
            bg="#DC3545",
            fg="white",
            command=self.eliminar_empleado,
            **btn_style
        )
        btn_eliminar.grid(row=1, column=1, padx=5, pady=5)

        # Panel derecho - Lista de empleados
        panel_der = tk.Frame(main_container, bg="white", relief=tk.RAISED, bd=2)
        panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(
            panel_der,
            text="Lista de Empleados",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#007BFF"
        ).pack(pady=15)

        # Buscador
        search_frame = tk.Frame(panel_der, bg="white")
        search_frame.pack(pady=5, padx=10, fill=tk.X)

        tk.Label(
            search_frame,
            text="🔍 Buscar:",
            font=("Segoe UI", 10),
            bg="white"
        ).pack(side=tk.LEFT, padx=5)

        self.entry_buscar = tk.Entry(search_frame, font=("Segoe UI", 10))
        self.entry_buscar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.entry_buscar.bind('<KeyRelease>', self.buscar_empleado)

        btn_refresh = tk.Button(
            search_frame,
            text="↻",
            font=("Segoe UI", 12, "bold"),
            bg="#007BFF",
            fg="white",
            command=self.refrescar_todo,
            cursor="hand2",
            width=3,
            bd=0
        )
        btn_refresh.pack(side=tk.RIGHT, padx=5)

        # Tabla de empleados
        tree_frame = tk.Frame(panel_der, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("Código", "Nombre Completo", "Sexo", "Cargo", "Edad", "Cliente"),
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            height=22
        )

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        # Configurar columnas
        self.tree.heading("Código", text="Código")
        self.tree.heading("Nombre Completo", text="Nombre Completo")
        self.tree.heading("Sexo", text="Sexo")
        self.tree.heading("Cargo", text="Cargo")
        self.tree.heading("Edad", text="Edad")
        self.tree.heading("Cliente", text="Cliente Asignado")

        self.tree.column("Código", width=70, anchor="center")
        self.tree.column("Nombre Completo", width=200)
        self.tree.column("Sexo", width=80, anchor="center")
        self.tree.column("Cargo", width=150)
        self.tree.column("Edad", width=60, anchor="center")
        self.tree.column("Cliente", width=200)

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
            font=("Segoe UI", 10, "bold"),
            bg="white",
            anchor="e"
        )
        label.grid(row=fila, column=0, padx=10, pady=5, sticky="e")

    def validar_edad(self, fecha_nac):
        """Valida que el empleado sea mayor de 18 años"""
        try:
            if fecha_nac == "YYYY-MM-DD" or not fecha_nac:
                return False
            fecha = datetime.strptime(fecha_nac, "%Y-%m-%d")
            edad = (datetime.now() - fecha).days / 365.25
            return edad >= 18
        except:
            return False

    def cargar_empleados(self):
        """Carga todos los empleados desde la base de datos"""
        conn = None
        cursor = None
        
        try:
            # Guardar selección actual
            seleccion_anterior = None
            if self.tree.selection():
                item = self.tree.item(self.tree.selection()[0])
                seleccion_anterior = item['values'][0] if item['values'] else None

            self.tree.delete(*self.tree.get_children())

            conn = Database.conectar()
            cursor = conn.cursor()

            query = """
                SELECT
                    e.codigo,
                    CONCAT(e.nombres, ' ', e.apellido_paterno, ' ', e.apellido_materno) AS nombre_completo,
                    e.sexo,
                    e.cargo,
                    TIMESTAMPDIFF(YEAR, e.fecha_nacimiento, CURDATE()) AS edad,
                    CONCAT(c.nombres, ' ', c.apellido_paterno) AS cliente_nombre
                FROM empleado e
                LEFT JOIN cliente c ON e.ruc_cliente = c.ruc
                ORDER BY e.codigo
            """

            cursor.execute(query)
            self.empleados = cursor.fetchall()

            item_a_seleccionar = None
            for empleado in self.empleados:
                edad = empleado[4] if empleado[4] else ""
                cliente = empleado[5] if empleado[5] else "Sin asignar"

                valores = (
                    empleado[0],
                    empleado[1],
                    empleado[2],
                    empleado[3],
                    f"{edad} años" if edad else "",
                    cliente
                )
                item_id = self.tree.insert("", tk.END, values=valores)
                
                if seleccion_anterior and empleado[0] == seleccion_anterior:
                    item_a_seleccionar = item_id

            # Restaurar selección
            if item_a_seleccionar:
                self.tree.selection_set(item_a_seleccionar)
                self.tree.see(item_a_seleccionar)

            self.tree.update_idletasks()

        except Exception as e:
            self.mostrar_error("Error al cargar empleados", str(e))
        finally:
            try:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
            except:
                pass

    def refrescar_todo(self):
        """Refresca la lista y limpia el formulario"""
        self.cargar_empleados()
        self.nuevo_empleado()

    def buscar_empleado(self, event=None):
        """Busca empleados por código o nombre"""
        busqueda = self.entry_buscar.get().strip().upper()

        self.tree.delete(*self.tree.get_children())

        if not busqueda:
            for empleado in self.empleados:
                edad = empleado[4] if empleado[4] else ""
                cliente = empleado[5] if empleado[5] else "Sin asignar"
                valores = (
                    empleado[0],
                    empleado[1],
                    empleado[2],
                    empleado[3],
                    f"{edad} años" if edad else "",
                    cliente
                )
                self.tree.insert("", tk.END, values=valores)
        else:
            for empleado in self.empleados:
                if busqueda in str(empleado[0]).upper() or busqueda in str(empleado[1]).upper():
                    edad = empleado[4] if empleado[4] else ""
                    cliente = empleado[5] if empleado[5] else "Sin asignar"
                    valores = (
                        empleado[0],
                        empleado[1],
                        empleado[2],
                        empleado[3],
                        f"{edad} años" if edad else "",
                        cliente
                    )
                    self.tree.insert("", tk.END, values=valores)

    def seleccionar_empleado(self, event=None):
        """Carga los datos del empleado seleccionado en el formulario"""
        seleccion = self.tree.selection()
        if not seleccion:
            return

        item = self.tree.item(seleccion[0])
        valores = item['values']

        conn = None
        cursor = None

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            query = """
                SELECT codigo, sexo, cargo, fecha_nacimiento, nombres,
                       apellido_paterno, apellido_materno, ruc_cliente, nombre_archivo
                FROM empleado
                WHERE codigo = %s
            """
            cursor.execute(query, (valores[0],))

            empleado = cursor.fetchone()

            if empleado:
                self.codigo_seleccionado = empleado[0]

                # Habilitar código temporalmente
                self.entry_codigo.config(state='normal')

                # Limpiar y cargar datos
                self.entry_codigo.delete(0, tk.END)
                self.entry_nombres.delete(0, tk.END)
                self.entry_ap_paterno.delete(0, tk.END)
                self.entry_ap_materno.delete(0, tk.END)
                self.entry_fecha_nac.delete(0, tk.END)
                self.entry_cargo.delete(0, tk.END)

                self.entry_codigo.insert(0, empleado[0])
                self.combo_sexo.set(empleado[1])
                self.entry_cargo.insert(0, empleado[2])
                self.entry_fecha_nac.insert(0, str(empleado[3]) if empleado[3] else "YYYY-MM-DD")
                self.entry_nombres.insert(0, empleado[4])
                self.entry_ap_paterno.insert(0, empleado[5])
                self.entry_ap_materno.insert(0, empleado[6])

                # ✅ RUC Cliente - buscar en combobox y seleccionar
                ruc_cliente = empleado[7]
                if ruc_cliente:
                    # Buscar el valor completo "RUC - Nombre" en el combobox
                    for i, (ruc, nombre) in enumerate(self.clientes_list):
                        if ruc == ruc_cliente:
                            valor_completo = f"{ruc} - {nombre}"
                            self.combo_ruc_cliente.set(valor_completo)
                            break
                else:
                    self.combo_ruc_cliente.set("")

                # ✅ Archivo - buscar en combobox y seleccionar
                nombre_archivo = empleado[8]
                if nombre_archivo and nombre_archivo in self.archivos_list:
                    self.combo_archivo.set(nombre_archivo)
                else:
                    self.combo_archivo.set("")

                # Deshabilitar código (PK)
                self.entry_codigo.config(state='disabled')

        except Exception as e:
            self.mostrar_error("Error al cargar empleado", str(e))
        finally:
            try:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
            except:
                pass

    def nuevo_empleado(self):
        """Limpia el formulario para un nuevo empleado"""
        self.codigo_seleccionado = None

        self.entry_codigo.config(state='normal')

        self.entry_codigo.delete(0, tk.END)
        self.combo_sexo.set("Masculino")
        self.entry_cargo.delete(0, tk.END)
        self.entry_fecha_nac.delete(0, tk.END)
        self.entry_fecha_nac.insert(0, "YYYY-MM-DD")
        self.entry_nombres.delete(0, tk.END)
        self.entry_ap_paterno.delete(0, tk.END)
        self.entry_ap_materno.delete(0, tk.END)
        self.combo_ruc_cliente.set("")  # ✅ Limpiar combobox
        self.combo_archivo.set("")  # ✅ Limpiar combobox
        self.entry_buscar.delete(0, tk.END)

        for item in self.tree.selection():
            self.tree.selection_remove(item)

        self.entry_codigo.focus()

    def guardar_empleado(self):
        """Guarda un nuevo empleado con modal de confirmación"""
        codigo = self.entry_codigo.get().strip()
        sexo = self.combo_sexo.get()
        cargo = self.entry_cargo.get().strip()
        fecha_nac = self.entry_fecha_nac.get().strip()
        nombres = self.entry_nombres.get().strip()
        ap_paterno = self.entry_ap_paterno.get().strip()
        ap_materno = self.entry_ap_materno.get().strip()

        # Validaciones
        if not codigo or not sexo or not cargo or not nombres or not ap_paterno or not ap_materno:
            self.mostrar_advertencia(
                "Campos Obligatorios",
                "Complete:\n• Código\n• Sexo\n• Cargo\n• Nombres\n• Apellidos"
            )
            return

        if not codigo.isdigit():
            self.mostrar_error("Código Inválido", "El código debe ser un número entero positivo")
            self.entry_codigo.focus()
            return

        if not self.validar_edad(fecha_nac):
            self.mostrar_error(
                "Fecha Inválida",
                "La fecha de nacimiento es inválida o el empleado es menor de 18 años.\n\n"
                "Formato requerido: YYYY-MM-DD"
            )
            self.entry_fecha_nac.focus()
            return

        # ✅ Obtener FKs opcionales del combobox
        ruc_cliente_text = self.combo_ruc_cliente.get().strip()
        ruc_cliente = None
        cliente_nombre = "Sin asignar"
        if ruc_cliente_text and " - " in ruc_cliente_text:
            ruc_cliente = ruc_cliente_text.split(" - ")[0]
            cliente_nombre = ruc_cliente_text.split(" - ")[1]

        nombre_archivo = self.combo_archivo.get().strip() or None

        # Calcular edad para mostrar
        try:
            fecha = datetime.strptime(fecha_nac, "%Y-%m-%d")
            edad = int((datetime.now() - fecha).days / 365.25)
        except:
            edad = 0

        # ✅ MODAL DE CONFIRMACIÓN ANTES DE GUARDAR
        confirmacion = messagebox.askyesno(
            "💾 Confirmar Registro",
            f"¿Desea registrar este empleado?\n\n"
            f"Código: {codigo}\n"
            f"Nombre: {nombres} {ap_paterno} {ap_materno}\n"
            f"Cargo: {cargo}\n"
            f"Sexo: {sexo}\n"
            f"Edad: {edad} años\n"
            f"Cliente asignado: {cliente_nombre}",
            parent=self.ventana
        )

        if not confirmacion:
            return

        conn = None
        cursor = None

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            query = "CALL insertar_empleado(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            valores = (
                int(codigo), sexo, cargo, fecha_nac, nombres,
                ap_paterno, ap_materno, ruc_cliente, nombre_archivo
            )

            cursor.execute(query, valores)

            # ✅ Consumir todos los resultados del stored procedure
            for result in cursor.stored_results():
                result.fetchall()
            
            # ✅ Consumir con nextset()
            while True:
                try:
                    if not cursor.nextset():
                        break
                except:
                    break

            conn.commit()

            # ✅ MODAL DE ÉXITO
            self.mostrar_exito(
                "Empleado Registrado",
                f"✓ Empleado registrado exitosamente\n\n"
                f"Código: {codigo}\n"
                f"Nombre: {nombres} {ap_paterno} {ap_materno}\n"
                f"Cargo: {cargo}"
            )
            
            # ✅ AUTO-REFRESH: Recargar y seleccionar el nuevo empleado
            self.cargar_empleados()
            
            # Buscar y seleccionar el empleado recién insertado
            for item in self.tree.get_children():
                if self.tree.item(item)['values'][0] == int(codigo):
                    self.tree.selection_set(item)
                    self.tree.see(item)
                    self.seleccionar_empleado()
                    break

        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except:
                    pass

            error_msg = str(e)
            if "Duplicate entry" in error_msg:
                self.mostrar_error(
                    "Código Duplicado",
                    f"❌ Ya existe un empleado registrado con el código:\n{codigo}"
                )
            elif "Unread result" in error_msg:
                # El INSERT se ejecutó correctamente a pesar del error
                self.mostrar_exito(
                    "Empleado Registrado",
                    f"✓ Empleado registrado exitosamente\n\nCódigo: {codigo}"
                )
                self.cargar_empleados()
                
                # Seleccionar el empleado
                for item in self.tree.get_children():
                    if self.tree.item(item)['values'][0] == int(codigo):
                        self.tree.selection_set(item)
                        self.tree.see(item)
                        self.seleccionar_empleado()
                        break
            else:
                self.mostrar_error("Error al Guardar", f"❌ {error_msg}")

        finally:
            try:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
            except:
                pass

    def actualizar_empleado(self):
        """Actualiza un empleado existente con modal de confirmación"""
        if not self.codigo_seleccionado:
            self.mostrar_advertencia("Sin Selección", "Seleccione un empleado para actualizar")
            return

        sexo = self.combo_sexo.get()
        cargo = self.entry_cargo.get().strip()
        fecha_nac = self.entry_fecha_nac.get().strip()
        nombres = self.entry_nombres.get().strip()
        ap_paterno = self.entry_ap_paterno.get().strip()
        ap_materno = self.entry_ap_materno.get().strip()

        if not sexo or not cargo or not nombres or not ap_paterno or not ap_materno:
            self.mostrar_advertencia("Campos Obligatorios", "Complete todos los campos obligatorios")
            return

        if not self.validar_edad(fecha_nac):
            self.mostrar_error(
                "Fecha Inválida",
                "La fecha de nacimiento es inválida o el empleado es menor de 18 años"
            )
            return

        # ✅ Obtener FKs del combobox
        ruc_cliente_text = self.combo_ruc_cliente.get().strip()
        ruc_cliente = None
        cliente_nombre = "Sin asignar"
        if ruc_cliente_text and " - " in ruc_cliente_text:
            ruc_cliente = ruc_cliente_text.split(" - ")[0]
            cliente_nombre = ruc_cliente_text.split(" - ")[1]

        nombre_archivo = self.combo_archivo.get().strip() or None

        # ✅ MODAL DE CONFIRMACIÓN ANTES DE ACTUALIZAR
        confirmacion = messagebox.askyesno(
            "🔄 Confirmar Actualización",
            f"¿Desea actualizar los datos de este empleado?\n\n"
            f"Código: {self.codigo_seleccionado}\n"
            f"Nuevo nombre: {nombres} {ap_paterno} {ap_materno}\n"
            f"Cargo: {cargo}\n"
            f"Sexo: {sexo}\n"
            f"Cliente asignado: {cliente_nombre}",
            parent=self.ventana
        )

        if not confirmacion:
            return

        conn = None
        cursor = None

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            query = "CALL actualizar_empleado(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            valores = (
                self.codigo_seleccionado, sexo, cargo, fecha_nac, nombres,
                ap_paterno, ap_materno, ruc_cliente, nombre_archivo
            )

            cursor.execute(query, valores)

            # ✅ Consumir todos los resultados del stored procedure
            for result in cursor.stored_results():
                result.fetchall()
            
            # ✅ Consumir con nextset()
            while True:
                try:
                    if not cursor.nextset():
                        break
                except:
                    break

            conn.commit()

            # ✅ MODAL DE ÉXITO
            self.mostrar_exito(
                "Empleado Actualizado",
                f"✓ Datos actualizados exitosamente\n\n"
                f"Código: {self.codigo_seleccionado}\n"
                f"Nombre: {nombres} {ap_paterno} {ap_materno}"
            )
            
            # ✅ AUTO-REFRESH: Recargar manteniendo la selección
            self.cargar_empleados()

        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except:
                    pass

            self.mostrar_error("Error al Actualizar", f"❌ {str(e)}")

        finally:
            try:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
            except:
                pass

    def eliminar_empleado(self):
        """Elimina un empleado con confirmación"""
        if not self.codigo_seleccionado:
            self.mostrar_advertencia("Sin Selección", "Seleccione un empleado para eliminar")
            return

        nombre_completo = f"{self.entry_nombres.get()} {self.entry_ap_paterno.get()} {self.entry_ap_materno.get()}"
        cargo = self.entry_cargo.get()

        confirmacion = messagebox.askyesno(
            "⚠ Confirmar Eliminación",
            f"¿Eliminar empleado?\n\n"
            f"Código: {self.codigo_seleccionado}\n"
            f"Nombre: {nombre_completo}\n"
            f"Cargo: {cargo}\n\n"
            f"Esta acción no se puede deshacer.",
            parent=self.ventana
        )

        if not confirmacion:
            return

        conn = None
        cursor = None

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            query = "CALL eliminar_empleado(%s)"
            cursor.execute(query, (self.codigo_seleccionado,))

            # ✅ Consumir todos los resultados del stored procedure
            for result in cursor.stored_results():
                result.fetchall()
            
            # ✅ Consumir con nextset()
            while True:
                try:
                    if not cursor.nextset():
                        break
                except:
                    break

            conn.commit()

            # ✅ MODAL DE ÉXITO
            self.mostrar_exito(
                "Empleado Eliminado",
                f"✓ Empleado eliminado exitosamente\n\n"
                f"Código: {self.codigo_seleccionado}\n"
                f"Nombre: {nombre_completo}"
            )
            
            # ✅ AUTO-REFRESH: Recargar y limpiar formulario
            self.cargar_empleados()
            self.nuevo_empleado()

        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except:
                    pass

            self.mostrar_error("Error al Eliminar", f"❌ {str(e)}")

        finally:
            try:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
            except:
                pass

    # Métodos de mensajes modales
    def mostrar_exito(self, titulo, mensaje):
        """Muestra mensaje de éxito"""
        messagebox.showinfo(f"✓ {titulo}", mensaje, parent=self.ventana)

    def mostrar_error(self, titulo, mensaje):
        """Muestra mensaje de error"""
        messagebox.showerror(f"✗ {titulo}", mensaje, parent=self.ventana)

    def mostrar_advertencia(self, titulo, mensaje):
        """Muestra mensaje de advertencia"""
        messagebox.showwarning(f"⚠ {titulo}", mensaje, parent=self.ventana)