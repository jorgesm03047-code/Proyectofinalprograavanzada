import customtkinter as ctk
import calendar
from datetime import date, datetime, timedelta
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from assets.styles import *

# Dialogo para agendar un intercambio
class DialogoSolicitar(ctk.CTkToplevel):
    def __init__(self, master, servicio, usuario, db_handler, on_complete):
        super().__init__(master)
        self.title("Solicitar Servicio")
        self.geometry("420x620")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self._servicio = servicio
        self._usuario = usuario
        self._db = db_handler
        self._on_complete = on_complete
        self._selected_day = None
        self._current_month = date.today().month
        self._current_year = date.today().year
        self._day_buttons = []
        self._calendar_frame = None
        self._construir()
        self.after(100, lambda: self.focus_force())

    def _construir(self):
        main = ctk.CTkScrollableFrame(self, fg_color=WHITE)
        main.pack(fill="both", expand=True)
        ctk.CTkLabel(main, text="Agendar Intercambio", font=(FONT_FAMILY, 20, "bold"), text_color=ROYAL_BLUE).pack(pady=(15, 5))
        info = ctk.CTkFrame(main, fg_color=LIGHT_GREY, corner_radius=12)
        info.pack(fill="x", padx=20, pady=8)
        ctk.CTkLabel(info, text=self._servicio["titulo"], font=(FONT_FAMILY, 16, "bold"), text_color=TEXT_DARK).pack(padx=15, pady=(10, 2))
        ctk.CTkLabel(info, text=f"{self._servicio['proveedor_nombre']}  •  {self._servicio['horas']}h", font=(FONT_FAMILY, 12), text_color=TEXT_SECONDARY).pack(padx=15, pady=(0, 10))
        ctk.CTkLabel(main, text="Selecciona una fecha:", font=(FONT_FAMILY, 13, "bold"), text_color=TEXT_DARK, anchor="w").pack(fill="x", padx=25, pady=(10, 5))
        self._calendar_container = ctk.CTkFrame(main, fg_color=WHITE, corner_radius=12, border_color=BORDER_COLOR, border_width=1)
        self._calendar_container.pack(fill="x", padx=20, pady=5)
        
        self._nav_frame = ctk.CTkFrame(self._calendar_container, fg_color="transparent")
        self._nav_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        self._dias_header = ctk.CTkFrame(self._calendar_container, fg_color="transparent")
        self._dias_header.pack(fill="x", padx=10)
        for d in ["Lu", "Ma", "Mi", "Ju", "Vi", "Sa", "Do"]:
            ctk.CTkLabel(self._dias_header, text=d, width=40, font=(FONT_FAMILY, 11, "bold"), text_color=TEXT_SECONDARY).pack(side="left", expand=True)
            
        self._calendar_frame = ctk.CTkFrame(self._calendar_container, fg_color="transparent")
        self._calendar_frame.pack(fill="x", pady=(0, 5))
        
        self._actualizar_nav()
        self._dibujar_calendario()
        ctk.CTkLabel(main, text="Hora preferida:", font=(FONT_FAMILY, 13, "bold"), text_color=TEXT_DARK, anchor="w").pack(fill="x", padx=25, pady=(10, 5))
        time_frame = ctk.CTkFrame(main, fg_color="transparent")
        time_frame.pack(fill="x", padx=20)
        horas_vals = [f"{h:02d}" for h in range(7, 22)]
        self._hora_combo = ctk.CTkComboBox(time_frame, values=horas_vals, width=80, height=38, corner_radius=10, border_color=BORDER_COLOR, border_width=2, fg_color=LIGHT_GREY, text_color=TEXT_DARK, font=(FONT_FAMILY, 13), button_color=ROYAL_BLUE, button_hover_color=ROYAL_BLUE_HOVER)
        self._hora_combo.set("09")
        self._hora_combo.pack(side="left", padx=(0, 5))
        ctk.CTkLabel(time_frame, text=":", font=(FONT_FAMILY, 16, "bold"), text_color=TEXT_DARK).pack(side="left")
        mins_vals = ["00", "15", "30", "45"]
        self._min_combo = ctk.CTkComboBox(time_frame, values=mins_vals, width=80, height=38, corner_radius=10, border_color=BORDER_COLOR, border_width=2, fg_color=LIGHT_GREY, text_color=TEXT_DARK, font=(FONT_FAMILY, 13), button_color=ROYAL_BLUE, button_hover_color=ROYAL_BLUE_HOVER)
        self._min_combo.set("00")
        self._min_combo.pack(side="left", padx=(5, 0))
        ctk.CTkLabel(main, text="Mensaje (opcional):", font=(FONT_FAMILY, 13, "bold"), text_color=TEXT_DARK, anchor="w").pack(fill="x", padx=25, pady=(10, 5))
        self._msg_entry = ctk.CTkTextbox(main, height=70, corner_radius=10, border_color=BORDER_COLOR, border_width=2, fg_color=LIGHT_GREY, text_color=TEXT_DARK, font=(FONT_FAMILY, 12))
        self._msg_entry.pack(fill="x", padx=20, pady=(0, 5))
        self._error_label = ctk.CTkLabel(main, text="", font=(FONT_FAMILY, 12), text_color=ACCENT_RED)
        self._error_label.pack(pady=3)
        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(5, 15))
        ctk.CTkButton(btn_frame, text="Cancelar", height=40, corner_radius=10, fg_color="transparent", border_color=BORDER_COLOR, border_width=2, text_color=TEXT_SECONDARY, font=(FONT_FAMILY, 13), hover_color=LIGHT_GREY, command=lambda: self.after(10, self.destroy)).pack(side="left", expand=True, fill="x", padx=(0, 5))
        ctk.CTkButton(btn_frame, text="Confirmar Solicitud", height=40, corner_radius=10, fg_color=ROYAL_BLUE, hover_color=ROYAL_BLUE_HOVER, text_color=WHITE, font=(FONT_FAMILY, 13, "bold"), command=lambda: self.after(10, self._confirmar)).pack(side="left", expand=True, fill="x", padx=(5, 0))

    def _actualizar_nav(self):
        for w in self._nav_frame.winfo_children():
            w.destroy()
        ctk.CTkButton(self._nav_frame, text="◀", width=35, height=30, corner_radius=8, fg_color=LIGHT_GREY, hover_color=BORDER_COLOR, text_color=TEXT_DARK, font=(FONT_FAMILY, 14), command=lambda: self.after(10, self._mes_anterior)).pack(side="left")
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        ctk.CTkLabel(self._nav_frame, text=f"{meses[self._current_month - 1]} {self._current_year}", font=(FONT_FAMILY, 14, "bold"), text_color=TEXT_DARK).pack(side="left", expand=True)
        ctk.CTkButton(self._nav_frame, text="▶", width=35, height=30, corner_radius=8, fg_color=LIGHT_GREY, hover_color=BORDER_COLOR, text_color=TEXT_DARK, font=(FONT_FAMILY, 14), command=lambda: self.after(10, self._mes_siguiente)).pack(side="right")

    def _dibujar_calendario(self):
        for w in self._calendar_frame.winfo_children():
            w.destroy()
        self._day_buttons = []
        cal = calendar.monthcalendar(self._current_year, self._current_month)
        for week in cal:
            row = ctk.CTkFrame(self._calendar_frame, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=1)
            for day in week:
                if day == 0:
                    ctk.CTkLabel(row, text="", width=40, height=32).pack(side="left", expand=True)
                else:
                    today = date.today()
                    d = date(self._current_year, self._current_month, day)
                    is_past = d < today
                    is_selected = self._selected_day == d
                    fg = ROYAL_BLUE if is_selected else ("transparent" if not is_past else "transparent")
                    tc = WHITE if is_selected else (BORDER_COLOR if is_past else TEXT_DARK)
                    btn = ctk.CTkButton(row, text=str(day), width=40, height=32, corner_radius=8, fg_color=fg, hover_color=ROYAL_BLUE_LIGHT, text_color=tc, font=(FONT_FAMILY, 12), command=lambda dd=d: self.after(10, self._seleccionar_dia, dd) if dd >= today else None)
                    btn.pack(side="left", expand=True)
                    if is_past:
                        btn.configure(state="disabled")
                    self._day_buttons.append(btn)

    def _seleccionar_dia(self, d):
        self._selected_day = d
        self._dibujar_calendario()

    def _mes_anterior(self):
        if self._current_month == 1:
            self._current_month = 12
            self._current_year -= 1
        else:
            self._current_month -= 1
        self._actualizar_nav()
        self._dibujar_calendario()

    def _mes_siguiente(self):
        if self._current_month == 12:
            self._current_month = 1
            self._current_year += 1
        else:
            self._current_month += 1
        self._actualizar_nav()
        self._dibujar_calendario()

    def _confirmar(self):
        if not self._selected_day:
            self._error_label.configure(text="Selecciona una fecha")
            return
        hora = f"{self._hora_combo.get()}:{self._min_combo.get()}"
        mensaje = self._msg_entry.get("1.0", "end").strip()
        horas_serv = float(self._servicio["horas"])
        if self._usuario.saldo_horas < horas_serv:
            self._error_label.configure(text="Saldo insuficiente")
            return
        if int(self._servicio["proveedor_id"]) == self._usuario.id:
            self._error_label.configure(text="No puedes solicitar tu propio servicio")
            return
        intercambios = self._db.leer_intercambios()
        nuevo_id = max([int(i["id"]) for i in intercambios], default=0) + 1
        intercambio = {
            "id": nuevo_id,
            "servicio_id": self._servicio["id"],
            "solicitante_id": self._usuario.id,
            "solicitante_nombre": self._usuario.name,
            "proveedor_id": self._servicio["proveedor_id"],
            "proveedor_nombre": self._servicio["proveedor_nombre"],
            "horas": horas_serv,
            "estado": "pendiente",
            "fecha": date.today().isoformat(),
            "fecha_propuesta": self._selected_day.isoformat(),
            "hora_propuesta": hora,
            "mensaje": mensaje,
        }
        self._db.agregar_intercambio(intercambio)
        self._db.agregar_notificacion(
            self._servicio["proveedor_id"],
            "📥 Nueva solicitud de intercambio",
            f"{self._usuario.name} quiere '{self._servicio['titulo']}' el {self._selected_day.strftime('%d/%m/%Y')} a las {hora}. Mensaje: {mensaje if mensaje else 'Sin mensaje'}",
            "solicitud"
        )
        self._on_complete()
        self.destroy()

# Dialogo de revision de intercambio
class DialogoRevisarIntercambio(ctk.CTkToplevel):
    def __init__(self, master, intercambio, db_handler, on_complete, es_admin=False, usuario_id=None):
        super().__init__(master)
        self.title("Revisar Intercambio")
        self.geometry("420x520")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self._inter = intercambio
        self._db = db_handler
        self._on_complete = on_complete
        self._es_admin = es_admin
        self._uid = usuario_id
        self._construir()
        self.after(100, lambda: self.focus_force())

    def _construir(self):
        main = ctk.CTkScrollableFrame(self, fg_color=WHITE)
        main.pack(fill="both", expand=True)
        ctk.CTkLabel(main, text="Detalle del Intercambio", font=(FONT_FAMILY, 20, "bold"), text_color=ROYAL_BLUE).pack(pady=(15, 10))
        card = ctk.CTkFrame(main, fg_color=LIGHT_GREY, corner_radius=12)
        card.pack(fill="x", padx=20, pady=5)
        items = [
            ("Solicitante", f"{self._inter['solicitante_nombre']}"),
            ("Proveedor", f"{self._inter['proveedor_nombre']}"),
            ("Horas", f"{self._inter['horas']} cr"),
            ("Fecha Solicitud", f"{self._inter['fecha']}"),
        ]
        fp = self._inter.get("fecha_propuesta", "")
        hp = self._inter.get("hora_propuesta", "")
        if fp:
            items.append(("Fecha Propuesta", f"{fp}"))
        if hp:
            items.append(("Hora Propuesta", f"{hp}"))
        for label, value in items:
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=4)
            ctk.CTkLabel(row, text=label, font=(FONT_FAMILY, 12, "bold"), text_color=TEXT_SECONDARY, anchor="w", width=120).pack(side="left")
            ctk.CTkLabel(row, text=value, font=(FONT_FAMILY, 13), text_color=TEXT_DARK, anchor="w").pack(side="left", expand=True, fill="x")
        msg = self._inter.get("mensaje", "")
        if msg:
            ctk.CTkLabel(main, text="Mensaje:", font=(FONT_FAMILY, 13, "bold"), text_color=TEXT_DARK, anchor="w").pack(fill="x", padx=25, pady=(10, 3))
            msg_box = ctk.CTkFrame(main, fg_color=LIGHT_GREY, corner_radius=10)
            msg_box.pack(fill="x", padx=20, pady=(0, 5))
            ctk.CTkLabel(msg_box, text=msg, font=(FONT_FAMILY, 12), text_color=TEXT_DARK, wraplength=340, anchor="w", justify="left").pack(padx=15, pady=10, fill="x")
        estado = self._inter["estado"]
        if estado == "pendiente":
            es_solicitante = False
            if self._uid is not None:
                es_solicitante = (int(self._inter["solicitante_id"]) == int(self._uid))
            
            ctk.CTkLabel(main, text="¿Qué deseas hacer?", font=(FONT_FAMILY, 14, "bold"), text_color=TEXT_DARK).pack(pady=(15, 10))
            self._motivo_label = ctk.CTkLabel(main, text="Motivo (opcional):", font=(FONT_FAMILY, 12, "bold"), text_color=TEXT_DARK, anchor="w")
            self._motivo_entry = ctk.CTkEntry(main, placeholder_text="Escribe un motivo...", height=38, corner_radius=10, border_color=BORDER_COLOR, border_width=2, fg_color=LIGHT_GREY, text_color=TEXT_DARK, font=(FONT_FAMILY, 12))
            self._motivo_label.pack(fill="x", padx=25, pady=(0, 3))
            self._motivo_entry.pack(fill="x", padx=20, pady=(0, 10))
            btn_frame = ctk.CTkFrame(main, fg_color="transparent")
            btn_frame.pack(fill="x", padx=20, pady=(0, 15))
            
            if es_solicitante and not self._es_admin:
                ctk.CTkButton(btn_frame, text="Cancelar Solicitud", height=42, corner_radius=10, fg_color=ACCENT_RED, hover_color="#c82333", text_color=WHITE, font=(FONT_FAMILY, 13, "bold"), command=lambda: self.after(10, self._rechazar)).pack(side="left", expand=True, fill="x", padx=(0, 5))
            else:
                ctk.CTkButton(btn_frame, text="Rechazar", height=42, corner_radius=10, fg_color=ACCENT_RED, hover_color="#c82333", text_color=WHITE, font=(FONT_FAMILY, 13, "bold"), command=lambda: self.after(10, self._rechazar)).pack(side="left", expand=True, fill="x", padx=(0, 5))
                ctk.CTkButton(btn_frame, text="Aprobar", height=42, corner_radius=10, fg_color=ACCENT_GREEN, hover_color="#218838", text_color=WHITE, font=(FONT_FAMILY, 13, "bold"), command=lambda: self.after(10, self._aprobar)).pack(side="left", expand=True, fill="x", padx=(5, 0))
        else:
            ec = ACCENT_GREEN if estado == "aprobado" else ACCENT_RED
            ctk.CTkLabel(main, text=f"Estado: {estado.upper()}", font=(FONT_FAMILY, 16, "bold"), text_color=ec).pack(pady=15)
            if estado == "aprobado" and not self._es_admin and self._uid is not None:
                btn_frame = ctk.CTkFrame(main, fg_color="transparent")
                btn_frame.pack(fill="x", padx=20, pady=(0, 15))
                ctk.CTkButton(btn_frame, text="Valorar", height=35, corner_radius=8, fg_color="#fca311", hover_color="#e0920d", text_color=WHITE, font=(FONT_FAMILY, 12, "bold"), command=lambda: self.after(10, self._abrir_valoracion)).pack(side="left", expand=True, fill="x", padx=(0, 5))
                ctk.CTkButton(btn_frame, text="Aclaración", height=35, corner_radius=8, fg_color=ACCENT_RED, hover_color="#c82333", text_color=WHITE, font=(FONT_FAMILY, 12, "bold"), command=lambda: self.after(10, self._abrir_aclaracion)).pack(side="left", expand=True, fill="x", padx=(5, 0))

            ctk.CTkButton(main, text="Cerrar", height=40, corner_radius=10, fg_color=ROYAL_BLUE, hover_color=ROYAL_BLUE_HOVER, text_color=WHITE, font=(FONT_FAMILY, 13, "bold"), command=lambda: self.after(10, self.destroy)).pack(padx=20, fill="x", pady=(0, 15))

    def _abrir_valoracion(self):
        DialogoValoracion(self.master, self._inter, self._uid, self._db)

    def _abrir_aclaracion(self):
        DialogoAclaracion(self.master, self._inter, self._uid, self._db)

    def _aprobar(self):
        if self._es_admin:
            from clases.administrador import Administrador
            a = Administrador(1, "Admin", "", "", "", 1)
            try:
                a.validarIntercambio(self._db, self._inter["id"], True)
            except ValueError:
                pass
        else:
            horas = float(self._inter["horas"])
            self._db.transferir_horas(
                int(self._inter["solicitante_id"]),
                int(self._inter["proveedor_id"]),
                horas
            )
            self._db.actualizar_intercambio(self._inter["id"], "aprobado")
            self._db.actualizar_servicio_estado(int(self._inter["servicio_id"]), "completado")
        fp = self._inter.get("fecha_propuesta", "")
        hp = self._inter.get("hora_propuesta", "")
        fecha_info = f" para el {fp} a las {hp}" if fp and hp else ""
        self._db.agregar_notificacion(
            self._inter["solicitante_id"],
            "Intercambio Aprobado",
            f"Tu solicitud con {self._inter['proveedor_nombre']} ha sido aprobada{fecha_info}. Se han transferido {self._inter['horas']} cr.",
            "aprobado"
        )
        self._db.agregar_notificacion(
            self._inter["proveedor_id"],
            "Intercambio Confirmado",
            f"Has aprobado el intercambio con {self._inter['solicitante_nombre']}{fecha_info}. Se han transferido {self._inter['horas']} cr.",
            "aprobado"
        )
        self._on_complete()
        self.destroy()

    def _rechazar(self):
        motivo = self._motivo_entry.get().strip() if hasattr(self, '_motivo_entry') else ""
        if self._es_admin:
            from clases.administrador import Administrador
            a = Administrador(1, "Admin", "", "", "", 1)
            try:
                a.validarIntercambio(self._db, self._inter["id"], False)
            except ValueError:
                pass
        else:
            self._db.actualizar_intercambio(self._inter["id"], "rechazado")
        motivo_txt = f" Motivo: {motivo}" if motivo else ""
        self._db.agregar_notificacion(
            self._inter["solicitante_id"],
            "Intercambio Rechazado",
            f"Tu solicitud con {self._inter['proveedor_nombre']} fue rechazada.{motivo_txt}",
            "rechazado"
        )
        self._on_complete()
        self.destroy()

class DialogoNotificaciones(ctk.CTkToplevel):
    def __init__(self, master, usuario_id, db_handler):
        super().__init__(master)
        self.title("Notificaciones")
        self.geometry("420x500")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self._uid = usuario_id
        self._db = db_handler
        self._construir()
        self.after(100, lambda: self.focus_force())

    def _construir(self):
        main = ctk.CTkScrollableFrame(self, fg_color=WHITE)
        main.pack(fill="both", expand=True)
        top = ctk.CTkFrame(main, fg_color="transparent")
        top.pack(fill="x", padx=20, pady=(15, 10))
        ctk.CTkLabel(top, text="Notificaciones", font=(FONT_FAMILY, 20, "bold"), text_color=ROYAL_BLUE).pack(side="left")
        ctk.CTkButton(top, text="Marcar todas leídas", width=140, height=30, corner_radius=8, fg_color=LIGHT_GREY, hover_color=BORDER_COLOR, text_color=TEXT_SECONDARY, font=(FONT_FAMILY, 11), command=lambda: self.after(10, self._marcar_todas)).pack(side="right")
        notifs = self._db.obtener_notificaciones_usuario(self._uid)
        if not notifs:
            ctk.CTkLabel(main, text="No tienes notificaciones", font=(FONT_FAMILY, 14), text_color=TEXT_SECONDARY).pack(pady=40)
            return
        for n in reversed(notifs):
            leida = n["leida"] == "1"
            tipo = n.get("tipo", "info")
            if tipo == "aprobado":
                border_c = ACCENT_GREEN
            elif tipo == "rechazado":
                border_c = ACCENT_RED
            elif tipo == "solicitud":
                border_c = ACCENT_ORANGE
            else:
                border_c = ROYAL_BLUE
            bg = WHITE if leida else "#f0f4ff"
            card = ctk.CTkFrame(main, fg_color=bg, corner_radius=10, border_color=border_c, border_width=2 if not leida else 0)
            card.pack(fill="x", padx=15, pady=4)
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="x", padx=12, pady=10)
            ctk.CTkLabel(inner, text=n["titulo"], font=(FONT_FAMILY, 13, "bold"), text_color=TEXT_DARK, anchor="w").pack(fill="x")
            ctk.CTkLabel(inner, text=n["mensaje"], font=(FONT_FAMILY, 11), text_color=TEXT_SECONDARY, anchor="w", wraplength=340, justify="left").pack(fill="x", pady=(3, 2))
            ctk.CTkLabel(inner, text=n["fecha"], font=(FONT_FAMILY, 10), text_color=BORDER_COLOR, anchor="e").pack(fill="x")

    def _marcar_todas(self):
        self._db.marcar_todas_leidas(self._uid)
        for w in self.winfo_children():
            w.destroy()
        self._construir()

class DialogoDetalleServicio(ctk.CTkToplevel):
    def __init__(self, master, servicio, usuario, db_handler, on_solicitar):
        super().__init__(master)
        self.title("Detalle del Servicio")
        self.geometry("420x450")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self._servicio = servicio
        self._usuario = usuario
        self._db = db_handler
        self._on_solicitar = on_solicitar
        self._construir()
        self.after(100, lambda: self.focus_force())

    def _construir(self):
        main = ctk.CTkScrollableFrame(self, fg_color=WHITE)
        main.pack(fill="both", expand=True)
        cat_colors = {"Educación": "#4361ee", "Tecnología": "#3a0ca3", "Diseño": "#f72585", "Hogar": "#4cc9f0", "Salud": "#06d6a0", "Transporte": "#fca311", "Otro": "#8d99ae"}
        cat = self._servicio.get("categoria", "Otro")
        cat_color = cat_colors.get(cat, ROYAL_BLUE)
        header = ctk.CTkFrame(main, fg_color=cat_color, corner_radius=0, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text=self._servicio["titulo"], font=(FONT_FAMILY, 20, "bold"), text_color=WHITE).pack(expand=True)
        info_card = ctk.CTkFrame(main, fg_color=LIGHT_GREY, corner_radius=12)
        info_card.pack(fill="x", padx=20, pady=15)
        vals = self._db.obtener_valoraciones_usuario(self._servicio['proveedor_id'])
        if vals:
            avg = sum([int(v['estrellas']) for v in vals]) / len(vals)
            stars = "" * int(round(avg))
        else:
            stars = "Nuevo"
            
        items = [
            ("Proveedor", f"{self._servicio['proveedor_nombre']} ({stars})"),
            ("Categoría", f"{cat}"),
            ("Créditos", f"{self._servicio['horas']} cr"),
            ("Estado", f"{'' if self._servicio['estado'] == 'disponible' else ''} {self._servicio['estado'].capitalize()}"),
            ("Publicado", f"{self._servicio['fecha']}"),
        ]
        for label, value in items:
            row = ctk.CTkFrame(info_card, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=4)
            ctk.CTkLabel(row, text=label, font=(FONT_FAMILY, 12, "bold"), text_color=TEXT_SECONDARY, width=100, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=value, font=(FONT_FAMILY, 13), text_color=TEXT_DARK, anchor="w").pack(side="left", expand=True, fill="x")
        ctk.CTkLabel(main, text="Descripción", font=(FONT_FAMILY, 14, "bold"), text_color=TEXT_DARK, anchor="w").pack(fill="x", padx=25, pady=(5, 5))
        desc_box = ctk.CTkFrame(main, fg_color=LIGHT_GREY, corner_radius=10)
        desc_box.pack(fill="x", padx=20, pady=(0, 10))
        ctk.CTkLabel(desc_box, text=self._servicio["descripcion"], font=(FONT_FAMILY, 12), text_color=TEXT_DARK, wraplength=340, anchor="w", justify="left").pack(padx=15, pady=10, fill="x")
        if self._servicio["estado"] == "disponible" and int(self._servicio["proveedor_id"]) != self._usuario.id:
            ctk.CTkButton(main, text="Agendar y Solicitar", height=44, corner_radius=10, fg_color=ROYAL_BLUE, hover_color=ROYAL_BLUE_HOVER, text_color=WHITE, font=(FONT_FAMILY, 15, "bold"), command=lambda: self.after(10, self._abrir_solicitar)).pack(fill="x", padx=20, pady=(5, 15))
        else:
            ctk.CTkButton(main, text="Cerrar", height=40, corner_radius=10, fg_color=LIGHT_GREY, hover_color=BORDER_COLOR, text_color=TEXT_SECONDARY, font=(FONT_FAMILY, 13), command=lambda: self.after(10, self.destroy)).pack(fill="x", padx=20, pady=(5, 15))

    def _abrir_solicitar(self):
        self.destroy()
        self._on_solicitar(self._servicio)

# Ventana para dejar valoracion con estrellas
class DialogoValoracion(ctk.CTkToplevel):
    def __init__(self, master, inter, uid, db_handler):
        super().__init__(master)
        self.title("Valorar Usuario")
        self.geometry("380x350")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self._inter = inter
        self._uid = uid
        self._db = db_handler
        self._construir()

    def _construir(self):
        main = ctk.CTkFrame(self, fg_color=WHITE)
        main.pack(fill="both", expand=True)
        es_solic = (int(self._inter["solicitante_id"]) == self._uid)
        otro_nombre = self._inter["proveedor_nombre"] if es_solic else self._inter["solicitante_nombre"]
        otro_id = self._inter["proveedor_id"] if es_solic else self._inter["solicitante_id"]
        
        ctk.CTkLabel(main, text=f"Valorar a {otro_nombre}", font=(FONT_FAMILY, 16, "bold"), text_color=TEXT_DARK).pack(pady=(20, 10))
        
        ctk.CTkLabel(main, text="Estrellas (1 a 5):", font=(FONT_FAMILY, 12, "bold"), text_color=TEXT_DARK).pack(pady=(10, 0))
        self._estrellas = ctk.CTkComboBox(main, values=["5", "4", "3", "2", "1"], width=80)
        self._estrellas.set("5")
        self._estrellas.pack(pady=5)
        
        ctk.CTkLabel(main, text="Comentario:", font=(FONT_FAMILY, 12, "bold"), text_color=TEXT_DARK).pack(pady=(10, 0))
        self._comentario = ctk.CTkTextbox(main, height=60, width=300)
        self._comentario.pack(pady=5)
        
        def guardar():
            self._db.agregar_valoracion(otro_id, self._uid, int(self._estrellas.get()), self._comentario.get("1.0", "end").strip())
            self.destroy()
            
        ctk.CTkButton(main, text="Guardar Valoración", fg_color=ACCENT_GREEN, hover_color="#218838", text_color=WHITE, font=(FONT_FAMILY, 12, "bold"), command=guardar).pack(pady=20)

# Dialogo para levantar aclaracion al admin
class DialogoAclaracion(ctk.CTkToplevel):
    def __init__(self, master, inter, uid, db_handler):
        super().__init__(master)
        self.title("Levantar Aclaración")
        self.geometry("380x300")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self._inter = inter
        self._uid = uid
        self._db = db_handler
        self._construir()

    def _construir(self):
        main = ctk.CTkFrame(self, fg_color=WHITE)
        main.pack(fill="both", expand=True)
        ctk.CTkLabel(main, text="Levantar Aclaración", font=(FONT_FAMILY, 16, "bold"), text_color=ACCENT_RED).pack(pady=(20, 10))
        ctk.CTkLabel(main, text="Explica el problema:", font=(FONT_FAMILY, 12, "bold"), text_color=TEXT_DARK).pack(pady=(10, 0))
        
        self._msg = ctk.CTkTextbox(main, height=100, width=300)
        self._msg.pack(pady=5)
        
        def enviar():
            self._db.agregar_aclaracion(self._inter["id"], self._inter["solicitante_id"], self._inter["proveedor_id"], self._msg.get("1.0", "end").strip())
            self._db.agregar_notificacion("1", "Nueva Aclaración", f"Se ha levantado una aclaración para el intercambio #{self._inter['id']}", "rechazado")
            self.destroy()
            
        ctk.CTkButton(main, text="Enviar a Moderación", fg_color=ACCENT_RED, hover_color="#c82333", text_color=WHITE, font=(FONT_FAMILY, 12, "bold"), command=enviar).pack(pady=20)
