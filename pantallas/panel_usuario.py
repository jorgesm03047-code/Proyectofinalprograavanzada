import customtkinter as ctk
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from assets.styles import *
from pantallas.dialogs import DialogoSolicitar, DialogoRevisarIntercambio, DialogoNotificaciones, DialogoDetalleServicio

# Panel principal del consumidor
class PanelUsuario(ctk.CTkFrame):
    def __init__(self, master, usuario, db_handler, on_logout_callback):
        super().__init__(master, fg_color=LIGHT_GREY)
        self._usuario = usuario
        self._db = db_handler
        self._on_logout = on_logout_callback
        self._content_frame = None
        self._balance_label = None
        self._notif_badge = None
        self._construir_interfaz()
        self._mostrar_inicio()

    def _refrescar_usuario(self):
        datos = self._db.buscar_usuario_por_id(self._usuario.id)
        if datos:
            self._usuario.saldo_horas = float(datos["saldo_horas"])

    # Construye la barra lateral y el area de contenido
    def _construir_interfaz(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        sidebar = ctk.CTkFrame(self, fg_color=ROYAL_BLUE, width=220, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        pf = ctk.CTkFrame(sidebar, fg_color="transparent")
        pf.pack(fill="x", padx=15, pady=(20, 5))
        ctk.CTkLabel(pf, text="", font=(FONT_FAMILY, 40), text_color=WHITE).pack()
        ctk.CTkLabel(pf, text=self._usuario.name, font=(FONT_FAMILY, 14, "bold"), text_color=WHITE).pack(pady=(3, 0))
        ctk.CTkLabel(pf, text="Consumidor", font=(FONT_FAMILY, 11), text_color="#a0b4d6").pack()
        bc = ctk.CTkFrame(sidebar, fg_color=ROYAL_BLUE_LIGHT, corner_radius=10)
        bc.pack(fill="x", padx=15, pady=(10, 15))
        ctk.CTkLabel(bc, text="Tu Saldo", font=(FONT_FAMILY, 11), text_color="#a0b4d6").pack(pady=(8, 0))
        self._balance_label = ctk.CTkLabel(bc, text=f"{self._usuario.consultarSaldo():.1f} créditos", font=(FONT_FAMILY, 24, "bold"), text_color=WHITE)
        self._balance_label.pack(pady=(0, 8))
        ctk.CTkFrame(sidebar, fg_color="#003399", height=1).pack(fill="x", padx=15, pady=3)
        from assets.icons import get_icon
        nav_items = [
            ("house", "Inicio", self._mostrar_inicio),
            ("list", "Servicios", self._mostrar_servicios),
            ("plus", "Publicar", self._mostrar_publicar),
            ("arrow-right-left", "Intercambios", self._mostrar_intercambios),
            ("calendar", "Historial", self._mostrar_historial),
            ("bell", "Notificaciones", self._abrir_notificaciones),
        ]
        for ic, text, cmd in nav_items:
            img = get_icon(ic, color=WHITE, size=20)
            if "Notificaciones" in text:
                btn_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
                btn_frame.pack(fill="x", padx=12, pady=2)
                btn = ctk.CTkButton(btn_frame, image=img, text=f" {text}", anchor="w", compound="left", height=38, corner_radius=8, fg_color="transparent", hover_color=ROYAL_BLUE_LIGHT, font=(FONT_FAMILY, 13), text_color=WHITE, command=cmd)
                btn.pack(side="left", fill="x", expand=True)
                self._notif_badge = ctk.CTkLabel(btn_frame, text="", font=(FONT_FAMILY, 11, "bold"), text_color=WHITE, fg_color=ACCENT_RED, corner_radius=10, width=25, height=20)
            else:
                btn = ctk.CTkButton(sidebar, image=img, text=f" {text}", anchor="w", compound="left", height=38, corner_radius=8, fg_color="transparent", hover_color=ROYAL_BLUE_LIGHT, font=(FONT_FAMILY, 13), text_color=WHITE, command=cmd)
                btn.pack(fill="x", padx=12, pady=2)
        self._actualizar_badge()
        lf = ctk.CTkFrame(sidebar, fg_color="transparent")
        lf.pack(side="bottom", fill="x", padx=12, pady=15)
        ctk.CTkButton(lf, image=get_icon("log-out", color=WHITE, size=20), text=" Salir", compound="left", height=38, corner_radius=8, fg_color=ACCENT_RED, hover_color="#c82333", font=(FONT_FAMILY, 13, "bold"), text_color=WHITE, command=self._on_logout).pack(fill="x")
        self._content_frame = ctk.CTkScrollableFrame(self, fg_color=LIGHT_GREY, corner_radius=0)
        self._content_frame.grid(row=0, column=1, sticky="nsew")

    def _actualizar_badge(self):
        count = self._db.contar_no_leidas(self._usuario.id)
        if count > 0:
            self._notif_badge.configure(text=f" {count} ")
            self._notif_badge.pack(side="right", padx=(0, 10))
        else:
            self._notif_badge.pack_forget()

    def _limpiar(self):
        for w in self._content_frame.winfo_children():
            w.destroy()

    def _actualizar_saldo_display(self):
        self._refrescar_usuario()
        if self._balance_label:
            self._balance_label.configure(text=f"{self._usuario.consultarSaldo():.1f} créditos")
        self._actualizar_badge()

    def _abrir_notificaciones(self):
        DialogoNotificaciones(self, self._usuario.id, self._db)
        self.after(500, self._actualizar_badge)

    def _mostrar_inicio(self):
        self._limpiar()
        self._refrescar_usuario()
        self._actualizar_saldo_display()
        ctk.CTkLabel(self._content_frame, text=f"¡Hola, {self._usuario.name}!", font=(FONT_FAMILY, 22, "bold"), text_color=TEXT_DARK, anchor="w").pack(fill="x", padx=20, pady=(20, 3))
        ctk.CTkLabel(self._content_frame, text="Bienvenido a tu panel de t-bank", font=(FONT_FAMILY, 12), text_color=TEXT_SECONDARY, anchor="w").pack(fill="x", padx=20, pady=(0, 15))
        servicios = self._db.leer_servicios()
        mis_servicios = [s for s in servicios if int(s["proveedor_id"]) == self._usuario.id]
        intercambios = self._db.leer_intercambios()
        mis_inter = [i for i in intercambios if int(i["solicitante_id"]) == self._usuario.id or int(i["proveedor_id"]) == self._usuario.id]
        notifs = self._db.contar_no_leidas(self._usuario.id)
        sf = ctk.CTkFrame(self._content_frame, fg_color="transparent")
        sf.pack(fill="x", padx=20, pady=(0, 15))
        stats = [
            ("", f"{self._usuario.consultarSaldo():.1f}", "Créditos", ROYAL_BLUE),
            ("", str(len(mis_servicios)), "Servicios", ROYAL_BLUE_LIGHT),
            ("", str(len(mis_inter)), "Intercambios", "#0066cc"),
            ("", str(notifs), "Alertas", ACCENT_ORANGE if notifs > 0 else TEXT_SECONDARY),
        ]
        for i, (ic, val, lbl, col) in enumerate(stats):
            c = ctk.CTkFrame(sf, fg_color=WHITE, corner_radius=12, height=90)
            c.pack(side="left", expand=True, fill="both", padx=(0 if i == 0 else 5, 0), pady=3)
            c.pack_propagate(False)
            ctk.CTkLabel(c, text=ic, font=(FONT_FAMILY, 22)).pack(pady=(10, 1))
            ctk.CTkLabel(c, text=val, font=(FONT_FAMILY, 18, "bold"), text_color=col).pack()
            ctk.CTkLabel(c, text=lbl, font=(FONT_FAMILY, 10), text_color=TEXT_SECONDARY).pack()
        ctk.CTkLabel(self._content_frame, text="Servicios Disponibles", font=(FONT_FAMILY, 16, "bold"), text_color=TEXT_DARK, anchor="w").pack(fill="x", padx=20, pady=(8, 8))
        disponibles = [s for s in servicios if s["estado"] == "disponible" and int(s["proveedor_id"]) != self._usuario.id]
        if not disponibles:
            ctk.CTkLabel(self._content_frame, text="No hay servicios disponibles", font=(FONT_FAMILY, 12), text_color=TEXT_SECONDARY).pack(pady=20)
        else:
            for s in disponibles[:6]:
                self._crear_card_servicio(s)

    # Crea una tarjeta visual para cada servicio
    def _crear_card_servicio(self, servicio, mostrar_aplicar=True):
        card = ctk.CTkFrame(self._content_frame, fg_color=WHITE, corner_radius=10)
        card.pack(fill="x", padx=20, pady=4)
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=15, pady=12)
        top = ctk.CTkFrame(inner, fg_color="transparent")
        top.pack(fill="x")
        ctk.CTkLabel(top, text=servicio["titulo"], font=(FONT_FAMILY, 14, "bold"), text_color=TEXT_DARK, anchor="w").pack(side="left")
        ctk.CTkLabel(top, text=f" {servicio['categoria']} ", font=(FONT_FAMILY, 10), text_color=WHITE, fg_color=ROYAL_BLUE, corner_radius=6).pack(side="right")
        ctk.CTkLabel(top, text=f" {servicio['horas']} cr ", font=(FONT_FAMILY, 11, "bold"), text_color=ROYAL_BLUE, fg_color="#e8edf5", corner_radius=6).pack(side="right", padx=(0, 5))
        ctk.CTkLabel(inner, text=servicio["descripcion"], font=(FONT_FAMILY, 11), text_color=TEXT_SECONDARY, anchor="w", wraplength=400).pack(fill="x", pady=(3, 5))
        bottom = ctk.CTkFrame(inner, fg_color="transparent")
        bottom.pack(fill="x")
        
        vals = self._db.obtener_valoraciones_usuario(servicio['proveedor_id'])
        if vals:
            avg = sum([int(v['estrellas']) for v in vals]) / len(vals)
            stars = "" * int(round(avg))
        else:
            stars = "Nuevo"
            
        ctk.CTkLabel(bottom, text=f"{servicio['proveedor_nombre']} ({stars})  •  {servicio['fecha']}", font=(FONT_FAMILY, 10), text_color=TEXT_SECONDARY, anchor="w").pack(side="left")
        if mostrar_aplicar and servicio["estado"] == "disponible":
            ctk.CTkButton(bottom, text="Ver", width=55, height=28, corner_radius=6, fg_color=LIGHT_GREY, hover_color=BORDER_COLOR, text_color=TEXT_DARK, font=(FONT_FAMILY, 11), command=lambda s=servicio: self._ver_detalle(s)).pack(side="right", padx=(5, 0))
            ctk.CTkButton(bottom, text="Solicitar", width=85, height=28, corner_radius=6, fg_color=ROYAL_BLUE, hover_color=ROYAL_BLUE_HOVER, text_color=WHITE, font=(FONT_FAMILY, 11, "bold"), command=lambda s=servicio: self._abrir_solicitar(s)).pack(side="right")

    def _ver_detalle(self, servicio):
        DialogoDetalleServicio(self, servicio, self._usuario, self._db, self._abrir_solicitar)

    def _abrir_solicitar(self, servicio):
        def on_complete():
            self._actualizar_saldo_display()
            self._mostrar_inicio()
        DialogoSolicitar(self, servicio, self._usuario, self._db, on_complete)

    def _mostrar_servicios(self):
        self._limpiar()
        self._refrescar_usuario()
        ctk.CTkLabel(self._content_frame, text="Todos los Servicios", font=(FONT_FAMILY, 20, "bold"), text_color=TEXT_DARK, anchor="w").pack(fill="x", padx=20, pady=(20, 12))
        servicios = self._db.leer_servicios()
        disponibles = [s for s in servicios if s["estado"] == "disponible"]
        if not disponibles:
            ctk.CTkLabel(self._content_frame, text="No hay servicios disponibles", font=(FONT_FAMILY, 12), text_color=TEXT_SECONDARY).pack(pady=30)
        else:
            for s in disponibles:
                show = int(s["proveedor_id"]) != self._usuario.id
                self._crear_card_servicio(s, mostrar_aplicar=show)

    def _mostrar_publicar(self):
        self._limpiar()
        ctk.CTkLabel(self._content_frame, text="Publicar Servicio", font=(FONT_FAMILY, 20, "bold"), text_color=TEXT_DARK, anchor="w").pack(fill="x", padx=20, pady=(20, 12))
        card = ctk.CTkFrame(self._content_frame, fg_color=WHITE, corner_radius=12)
        card.pack(fill="x", padx=20, pady=5)
        fi = ctk.CTkFrame(card, fg_color="transparent")
        fi.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(fi, text="Título", font=(FONT_FAMILY, 12, "bold"), text_color=TEXT_DARK, anchor="w").pack(fill="x")
        titulo_e = ctk.CTkEntry(fi, placeholder_text="Ej: Clases de programación", height=38, corner_radius=8, border_color=BORDER_COLOR, border_width=2, fg_color=LIGHT_GREY, text_color=TEXT_DARK, font=(FONT_FAMILY, 12))
        titulo_e.pack(fill="x", pady=(3, 10))
        ctk.CTkLabel(fi, text="Descripción", font=(FONT_FAMILY, 12, "bold"), text_color=TEXT_DARK, anchor="w").pack(fill="x")
        desc_e = ctk.CTkTextbox(fi, height=80, corner_radius=8, border_color=BORDER_COLOR, border_width=2, fg_color=LIGHT_GREY, text_color=TEXT_DARK, font=(FONT_FAMILY, 12))
        desc_e.pack(fill="x", pady=(3, 10))
        row = ctk.CTkFrame(fi, fg_color="transparent")
        row.pack(fill="x", pady=(0, 10))
        cf = ctk.CTkFrame(row, fg_color="transparent")
        cf.pack(side="left", expand=True, fill="x", padx=(0, 5))
        ctk.CTkLabel(cf, text="Categoría", font=(FONT_FAMILY, 12, "bold"), text_color=TEXT_DARK, anchor="w").pack(fill="x")
        cats = ["Educación", "Tecnología", "Diseño", "Hogar", "Salud", "Transporte", "Otro"]
        cat_c = ctk.CTkComboBox(cf, values=cats, height=38, corner_radius=8, border_color=BORDER_COLOR, border_width=2, fg_color=LIGHT_GREY, text_color=TEXT_DARK, font=(FONT_FAMILY, 12), button_color=ROYAL_BLUE, button_hover_color=ROYAL_BLUE_HOVER)
        cat_c.pack(fill="x", pady=(3, 0))
        hf = ctk.CTkFrame(row, fg_color="transparent")
        hf.pack(side="left", expand=True, fill="x")
        ctk.CTkLabel(hf, text="Créditos a cobrar", font=(FONT_FAMILY, 12, "bold"), text_color=TEXT_DARK, anchor="w").pack(fill="x")
        horas_e = ctk.CTkEntry(hf, placeholder_text="2.0", height=38, corner_radius=8, border_color=BORDER_COLOR, border_width=2, fg_color=LIGHT_GREY, text_color=TEXT_DARK, font=(FONT_FAMILY, 12))
        horas_e.pack(fill="x", pady=(3, 0))
        msg = ctk.CTkLabel(fi, text="", font=(FONT_FAMILY, 12))
        msg.pack(pady=5)
        def publicar():
            t = titulo_e.get().strip()
            d = desc_e.get("1.0", "end").strip()
            c = cat_c.get()
            h = horas_e.get().strip()
            if not all([t, d, c, h]):
                msg.configure(text="Completa todos los campos", text_color=ACCENT_RED)
                return
            try:
                hf2 = float(h)
                if hf2 <= 0:
                    raise ValueError()
            except ValueError:
                msg.configure(text="Horas inválidas", text_color=ACCENT_RED)
                return
            from clases.consumidor import Consumidor
            con = Consumidor(self._usuario.id, self._usuario.name, self._usuario.email, self._usuario.password, self._usuario.town, self._usuario.fechaRegistro, self._usuario.saldo_horas)
            con.publicarServicio(self._db, t, d, c, hf2)
            msg.configure(text="Servicio publicado", text_color=ACCENT_GREEN)
            titulo_e.delete(0, "end")
            desc_e.delete("1.0", "end")
            horas_e.delete(0, "end")
        ctk.CTkButton(fi, text="Publicar Servicio", height=42, corner_radius=8, fg_color=ROYAL_BLUE, hover_color=ROYAL_BLUE_HOVER, font=(FONT_FAMILY, 14, "bold"), text_color=WHITE, command=publicar).pack(fill="x")

    # Muestra intercambios separados en pestañas
    def _mostrar_intercambios(self):
        self._limpiar()
        self._refrescar_usuario()
        self._actualizar_saldo_display()
        ctk.CTkLabel(self._content_frame, text="Mis Intercambios", font=(FONT_FAMILY, 20, "bold"), text_color=TEXT_DARK, anchor="w").pack(fill="x", padx=20, pady=(20, 12))
        
        tabview = ctk.CTkTabview(self._content_frame, fg_color=WHITE, text_color=TEXT_DARK, segmented_button_selected_color=ROYAL_BLUE, segmented_button_selected_hover_color=ROYAL_BLUE_HOVER)
        tabview.pack(fill="both", expand=True, padx=20, pady=5)
        
        tab_solicitados = tabview.add("Solicitados")
        tab_ofrecidos = tabview.add("Ofrecidos")
        
        intercambios = self._db.leer_intercambios()
        solicitados = [i for i in intercambios if int(i["solicitante_id"]) == self._usuario.id]
        ofrecidos = [i for i in intercambios if int(i["proveedor_id"]) == self._usuario.id]
        
        def render_list(parent_frame, inter_list):
            if not inter_list:
                ctk.CTkLabel(parent_frame, text="No hay intercambios", font=(FONT_FAMILY, 12), text_color=TEXT_SECONDARY).pack(pady=30)
                return
            for inter in inter_list:
                estado = inter["estado"]
                ec = ACCENT_GREEN if estado == "aprobado" else (ACCENT_ORANGE if estado == "pendiente" else ACCENT_RED)
                ei = "" if estado == "aprobado" else ("" if estado == "pendiente" else "")
                card = ctk.CTkFrame(parent_frame, fg_color=LIGHT_GREY, corner_radius=10)
                card.pack(fill="x", padx=10, pady=4)
                inner = ctk.CTkFrame(card, fg_color="transparent")
                inner.pack(fill="x", padx=15, pady=12)
                top = ctk.CTkFrame(inner, fg_color="transparent")
                top.pack(fill="x")
                es_solicitante = int(inter["solicitante_id"]) == self._usuario.id
                role_text = "Solicitaste a" if es_solicitante else "Te solicitó"
                other = inter["proveedor_nombre"] if es_solicitante else inter["solicitante_nombre"]
                ctk.CTkLabel(top, text=f"{role_text}: {other}", font=(FONT_FAMILY, 13, "bold"), text_color=TEXT_DARK, anchor="w").pack(side="left")
                ctk.CTkLabel(top, text=f" {ei} {estado.upper()} ", font=(FONT_FAMILY, 10, "bold"), text_color=WHITE, fg_color=ec, corner_radius=6).pack(side="right")
                fp = inter.get("fecha_propuesta", "")
                hp = inter.get("hora_propuesta", "")
                fecha_txt = f"{fp} {hp}" if fp and hp else f"{inter['fecha']}"
                ctk.CTkLabel(inner, text=f"{inter['horas']} cr  •  {fecha_txt}", font=(FONT_FAMILY, 11), text_color=TEXT_SECONDARY, anchor="w").pack(fill="x", pady=(3, 3))
                bottom = ctk.CTkFrame(inner, fg_color="transparent")
                bottom.pack(fill="x")
                ctk.CTkButton(bottom, text="Ver Detalle", width=100, height=28, corner_radius=6, fg_color=WHITE, border_color=BORDER_COLOR, border_width=1, hover_color=BORDER_COLOR, text_color=TEXT_DARK, font=(FONT_FAMILY, 11), command=lambda i=inter: self._ver_intercambio(i)).pack(side="right")
                if estado == "pendiente" and not es_solicitante:
                    ctk.CTkButton(bottom, text="Revisar", width=80, height=28, corner_radius=6, fg_color=ACCENT_GREEN, hover_color="#218838", text_color=WHITE, font=(FONT_FAMILY, 11, "bold"), command=lambda i=inter: self._revisar_intercambio(i)).pack(side="right", padx=(0, 5))

        render_list(tab_solicitados, solicitados)
        render_list(tab_ofrecidos, ofrecidos)

    def _ver_intercambio(self, inter):
        DialogoRevisarIntercambio(self, inter, self._db, lambda: (self._actualizar_saldo_display(), self._mostrar_intercambios()), es_admin=False, usuario_id=self._usuario.id)

    def _revisar_intercambio(self, inter):
        DialogoRevisarIntercambio(self, inter, self._db, lambda: (self._actualizar_saldo_display(), self._mostrar_intercambios()), es_admin=False, usuario_id=self._usuario.id)

    def _mostrar_historial(self):
        self._limpiar()
        self._refrescar_usuario()
        self._actualizar_saldo_display()
        ctk.CTkLabel(self._content_frame, text="Historial", font=(FONT_FAMILY, 20, "bold"), text_color=TEXT_DARK, anchor="w").pack(fill="x", padx=20, pady=(20, 12))
        historial = self._usuario.verHistorial()
        if not historial:
            ctk.CTkLabel(self._content_frame, text="No hay transacciones", font=(FONT_FAMILY, 12), text_color=TEXT_SECONDARY).pack(pady=30)
            return
        for t in reversed(historial):
            tipo = t["tipo"]
            ic = "" if tipo == "CREDITO" else ""
            col = ACCENT_GREEN if tipo == "CREDITO" else ACCENT_RED
            signo = "+" if tipo == "CREDITO" else "-"
            card = ctk.CTkFrame(self._content_frame, fg_color=WHITE, corner_radius=10)
            card.pack(fill="x", padx=20, pady=3)
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="x", padx=15, pady=10)
            top = ctk.CTkFrame(inner, fg_color="transparent")
            top.pack(fill="x")
            ctk.CTkLabel(top, text=f"{ic} {tipo}", font=(FONT_FAMILY, 13, "bold"), text_color=TEXT_DARK, anchor="w").pack(side="left")
            ctk.CTkLabel(top, text=f"{signo}{t['horas']} cr", font=(FONT_FAMILY, 14, "bold"), text_color=col).pack(side="right")
            ctk.CTkLabel(inner, text=f"Saldo: {t['saldoAntes']} cr → {t['saldoDespues']} cr  •  {t['fecha']}", font=(FONT_FAMILY, 10), text_color=TEXT_SECONDARY, anchor="w").pack(fill="x", pady=(2, 0))
