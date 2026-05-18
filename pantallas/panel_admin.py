import customtkinter as ctk
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from assets.styles import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pantallas.dialogs import DialogoRevisarIntercambio, DialogoNotificaciones

# Panel de administracion del sistema
class PanelAdmin(ctk.CTkFrame):
    def __init__(self, master, admin, db_handler, on_logout_callback):
        super().__init__(master, fg_color=LIGHT_GREY)
        self._admin = admin
        self._db = db_handler
        self._on_logout = on_logout_callback
        self._content_frame = None
        self._construir_interfaz()
        self._mostrar_dashboard()

    # Arma la interfaz con sidebar y contenido
    def _construir_interfaz(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        sidebar = ctk.CTkFrame(self, fg_color=ROYAL_BLUE, width=220, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        pf = ctk.CTkFrame(sidebar, fg_color="transparent")
        pf.pack(fill="x", padx=15, pady=(20, 5))
        ctk.CTkLabel(pf, text="", font=(FONT_FAMILY, 40), text_color=WHITE).pack()
        ctk.CTkLabel(pf, text=self._admin.name, font=(FONT_FAMILY, 14, "bold"), text_color=WHITE).pack(pady=(3, 0))
        ctk.CTkLabel(pf, text="Administrador", font=(FONT_FAMILY, 11), text_color="#a0b4d6").pack()
        ctk.CTkFrame(sidebar, fg_color="#003399", height=1).pack(fill="x", padx=15, pady=10)
        from assets.icons import get_icon
        nav = [
            ("layout-dashboard", "Dashboard", self._mostrar_dashboard),
            ("user", "Usuarios", self._mostrar_usuarios),
            ("arrow-right-left", "Intercambios", self._mostrar_intercambios_admin),
            ("triangle-alert", "Aclaraciones", self._mostrar_aclaraciones_admin),
            ("coins", "Ajustar Saldo", self._mostrar_ajustar_saldo),
            ("list", "Servicios", self._mostrar_servicios_admin),
            ("bell", "Notificaciones", self._abrir_notificaciones),
        ]
        for ic, text, cmd in nav:
            ctk.CTkButton(sidebar, image=get_icon(ic, color=WHITE, size=20), text=f" {text}", anchor="w", compound="left", height=38, corner_radius=8, fg_color="transparent", hover_color=ROYAL_BLUE_LIGHT, font=(FONT_FAMILY, 13), text_color=WHITE, command=cmd).pack(fill="x", padx=12, pady=2)
        lf = ctk.CTkFrame(sidebar, fg_color="transparent")
        lf.pack(side="bottom", fill="x", padx=12, pady=15)
        ctk.CTkButton(lf, image=get_icon("log-out", color=WHITE, size=20), text=" Salir", compound="left", height=38, corner_radius=8, fg_color=ACCENT_RED, hover_color="#c82333", font=(FONT_FAMILY, 13, "bold"), text_color=WHITE, command=self._on_logout).pack(fill="x")
        self._content_frame = ctk.CTkScrollableFrame(self, fg_color=LIGHT_GREY, corner_radius=0)
        self._content_frame.grid(row=0, column=1, sticky="nsew")

    def _limpiar(self):
        for w in self._content_frame.winfo_children():
            w.destroy()

    def _abrir_notificaciones(self):
        DialogoNotificaciones(self, self._admin.id, self._db)

    # Dashboard con estadisticas generales
    def _mostrar_dashboard(self):
        self._limpiar()
        from clases.administrador import Administrador
        admin_obj = Administrador(self._admin.id, self._admin.name, self._admin.email, self._admin.password, self._admin.town, 1)
        reporte = admin_obj.generarReporte(self._db)
        ctk.CTkLabel(self._content_frame, text="Dashboard", font=(FONT_FAMILY, 22, "bold"), text_color=TEXT_DARK, anchor="w").pack(fill="x", padx=20, pady=(20, 12))
        sf = ctk.CTkFrame(self._content_frame, fg_color="transparent")
        sf.pack(fill="x", padx=20, pady=(0, 10))
        cards = [
            ("", str(reporte["total_usuarios"]), "Usuarios", ROYAL_BLUE),
            ("", str(reporte["activos"]), "Activos", ACCENT_GREEN),
            ("", str(reporte["total_intercambios"]), "Intercambios", ROYAL_BLUE_LIGHT),
            ("", f"{reporte['total_horas']:.1f} cr", "Créditos", "#0066cc"),
        ]
        for i, (ic, val, lbl, col) in enumerate(cards):
            c = ctk.CTkFrame(sf, fg_color=WHITE, corner_radius=12, height=90)
            c.pack(side="left", expand=True, fill="both", padx=(0 if i == 0 else 5, 0), pady=3)
            c.pack_propagate(False)
            ctk.CTkLabel(c, text=ic, font=(FONT_FAMILY, 22)).pack(pady=(10, 1))
            ctk.CTkLabel(c, text=val, font=(FONT_FAMILY, 18, "bold"), text_color=col).pack()
            ctk.CTkLabel(c, text=lbl, font=(FONT_FAMILY, 10), text_color=TEXT_SECONDARY).pack()
        chart_frame = ctk.CTkFrame(self._content_frame, fg_color=WHITE, corner_radius=12)
        chart_frame.pack(fill="x", padx=20, pady=8)
        ctk.CTkLabel(chart_frame, text="  Resumen de Intercambios", font=(FONT_FAMILY, 14, "bold"), text_color=TEXT_DARK, anchor="w").pack(fill="x", padx=15, pady=(12, 3))
        fig = Figure(figsize=(6, 2.5), dpi=100, facecolor=WHITE)
        ax = fig.add_subplot(111)
        labels = ["Aprobados", "Pendientes", "Rechazados"]
        values = [reporte["aprobados"], reporte["pendientes"], reporte["rechazados"]]
        colors_bar = ["#28a745", "#fd7e14", "#dc3545"]
        bars = ax.bar(labels, values, color=colors_bar, width=0.5, edgecolor="white", linewidth=1.5)
        for bar, v in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1, str(int(v)), ha="center", va="bottom", fontsize=11, fontweight="bold", color="#333")
        ax.set_facecolor(WHITE)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#ddd")
        ax.spines["bottom"].set_color("#ddd")
        ax.tick_params(colors="#666", labelsize=9)
        fig.tight_layout(pad=1.5)
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="x", padx=10, pady=(0, 12))
        chart2 = ctk.CTkFrame(self._content_frame, fg_color=WHITE, corner_radius=12)
        chart2.pack(fill="x", padx=20, pady=8)
        ctk.CTkLabel(chart2, text="  Servicios por Estado", font=(FONT_FAMILY, 14, "bold"), text_color=TEXT_DARK, anchor="w").pack(fill="x", padx=15, pady=(12, 3))
        fig2 = Figure(figsize=(4, 2.5), dpi=100, facecolor=WHITE)
        ax2 = fig2.add_subplot(111)
        pv = [reporte["disponibles"], reporte["completados"]]
        pl = ["Disponibles", "Completados"]
        pc = [ROYAL_BLUE, ACCENT_GREEN]
        if sum(pv) > 0:
            ax2.pie(pv, labels=pl, colors=pc, autopct="%1.0f%%", startangle=90, textprops={"fontsize": 10, "color": "#333"})
        else:
            ax2.text(0.5, 0.5, "Sin datos", ha="center", va="center", fontsize=13, color="#999")
        fig2.tight_layout(pad=1.5)
        canvas2 = FigureCanvasTkAgg(fig2, chart2)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="x", padx=10, pady=(0, 12))

    def _mostrar_usuarios(self):
        self._limpiar()
        ctk.CTkLabel(self._content_frame, text="Gestión de Usuarios", font=(FONT_FAMILY, 20, "bold"), text_color=TEXT_DARK, anchor="w").pack(fill="x", padx=20, pady=(20, 12))
        usuarios = self._db.leer_usuarios()
        for u in usuarios:
            activo = str(u.get("activo", "1")) == "1"
            card = ctk.CTkFrame(self._content_frame, fg_color=WHITE, corner_radius=10)
            card.pack(fill="x", padx=20, pady=3)
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="x", padx=15, pady=10)
            top = ctk.CTkFrame(inner, fg_color="transparent")
            top.pack(fill="x")
            ctk.CTkLabel(top, text=f"{'' if u['rol'] != 'admin' else ''} {u['name']}", font=(FONT_FAMILY, 13, "bold"), text_color=TEXT_DARK, anchor="w").pack(side="left")
            sc = ACCENT_GREEN if activo else ACCENT_RED
            st = "ACTIVO" if activo else "SUSPENDIDO"
            ctk.CTkLabel(top, text=f" {st} ", font=(FONT_FAMILY, 10, "bold"), text_color=WHITE, fg_color=sc, corner_radius=6).pack(side="right")
            ctk.CTkLabel(inner, text=f"{u['email']}  •  {u['town']}  •  {float(u['saldo_horas']):.1f} cr", font=(FONT_FAMILY, 10), text_color=TEXT_SECONDARY, anchor="w").pack(fill="x", pady=(3, 3))
            if u["rol"] != "admin":
                bf = ctk.CTkFrame(inner, fg_color="transparent")
                bf.pack(fill="x")
                if activo:
                    ctk.CTkButton(bf, text="Suspender", width=85, height=28, corner_radius=6, fg_color=ACCENT_RED, hover_color="#c82333", font=(FONT_FAMILY, 11), text_color=WHITE, command=lambda uid=u["id"]: self.after(10, lambda: self._suspender(uid))).pack(side="right")
                else:
                    ctk.CTkButton(bf, text="Reactivar", width=85, height=28, corner_radius=6, fg_color=ACCENT_GREEN, hover_color="#218838", font=(FONT_FAMILY, 11), text_color=WHITE, command=lambda uid=u["id"]: self.after(10, lambda: self._reactivar(uid))).pack(side="right")

    def _suspender(self, uid):
        from clases.administrador import Administrador
        a = Administrador(self._admin.id, self._admin.name, self._admin.email, self._admin.password, self._admin.town, 1)
        a.suspenderUsuario(self._db, uid)
        self._db.agregar_notificacion(uid, "Cuenta Suspendida", "Tu cuenta ha sido suspendida por un administrador.", "rechazado")
        self._mostrar_usuarios()

    def _reactivar(self, uid):
        from clases.administrador import Administrador
        a = Administrador(self._admin.id, self._admin.name, self._admin.email, self._admin.password, self._admin.town, 1)
        a.reactivarUsuario(self._db, uid)
        self._db.agregar_notificacion(uid, "Cuenta Reactivada", "Tu cuenta ha sido reactivada por un administrador.", "aprobado")
        self._mostrar_usuarios()

    def _mostrar_intercambios_admin(self):
        self._limpiar()
        ctk.CTkLabel(self._content_frame, text="Gestión de Intercambios", font=(FONT_FAMILY, 20, "bold"), text_color=TEXT_DARK, anchor="w").pack(fill="x", padx=20, pady=(20, 12))
        intercambios = self._db.leer_intercambios()
        if not intercambios:
            ctk.CTkLabel(self._content_frame, text="No hay intercambios", font=(FONT_FAMILY, 12), text_color=TEXT_SECONDARY).pack(pady=30)
            return
        for i in intercambios:
            estado = i["estado"]
            ec = ACCENT_ORANGE if estado == "pendiente" else (ACCENT_GREEN if estado == "aprobado" else ACCENT_RED)
            card = ctk.CTkFrame(self._content_frame, fg_color=WHITE, corner_radius=10)
            card.pack(fill="x", padx=20, pady=3)
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="x", padx=15, pady=10)
            top = ctk.CTkFrame(inner, fg_color="transparent")
            top.pack(fill="x")
            ctk.CTkLabel(top, text=f"#{i['id']} — {i['solicitante_nombre']} → {i['proveedor_nombre']}", font=(FONT_FAMILY, 12, "bold"), text_color=TEXT_DARK, anchor="w").pack(side="left")
            ctk.CTkLabel(top, text=f" {estado.upper()} ", font=(FONT_FAMILY, 10, "bold"), text_color=WHITE, fg_color=ec, corner_radius=6).pack(side="right")
            fp = i.get("fecha_propuesta", "")
            hp = i.get("hora_propuesta", "")
            fecha_txt = f"{fp} {hp}" if fp and hp else f"{i['fecha']}"
            ctk.CTkLabel(inner, text=f"{i['horas']} cr  •  {fecha_txt}", font=(FONT_FAMILY, 10), text_color=TEXT_SECONDARY, anchor="w").pack(fill="x", pady=(3, 3))
            bf = ctk.CTkFrame(inner, fg_color="transparent")
            bf.pack(fill="x")
            ctk.CTkButton(bf, text="Revisar", width=80, height=28, corner_radius=6, fg_color=ROYAL_BLUE, hover_color=ROYAL_BLUE_HOVER, text_color=WHITE, font=(FONT_FAMILY, 11, "bold"), command=lambda ii=i: self._abrir_revision(ii)).pack(side="right")

    def _abrir_revision(self, intercambio):
        DialogoRevisarIntercambio(self, intercambio, self._db, self._mostrar_intercambios_admin, es_admin=True, usuario_id=self._admin.id)

    # Formulario para ajustar créditos de usuarios
    def _mostrar_ajustar_saldo(self):
        self._limpiar()
        ctk.CTkLabel(self._content_frame, text="Ajustar Saldo", font=(FONT_FAMILY, 20, "bold"), text_color=TEXT_DARK, anchor="w").pack(fill="x", padx=20, pady=(20, 12))
        card = ctk.CTkFrame(self._content_frame, fg_color=WHITE, corner_radius=12)
        card.pack(fill="x", padx=20, pady=5)
        fi = ctk.CTkFrame(card, fg_color="transparent")
        fi.pack(fill="x", padx=20, pady=20)
        usuarios = self._db.leer_usuarios()
        user_names = [f"{u['id']} - {u['name']}" for u in usuarios if u["rol"] != "admin"]
        ctk.CTkLabel(fi, text="Usuario", font=(FONT_FAMILY, 12, "bold"), text_color=TEXT_DARK, anchor="w").pack(fill="x")
        uc = ctk.CTkComboBox(fi, values=user_names if user_names else ["Sin usuarios"], height=38, corner_radius=8, border_color=BORDER_COLOR, border_width=2, fg_color=LIGHT_GREY, text_color=TEXT_DARK, font=(FONT_FAMILY, 12), button_color=ROYAL_BLUE, button_hover_color=ROYAL_BLUE_HOVER)
        uc.pack(fill="x", pady=(3, 10))
        ctk.CTkLabel(fi, text="Operación", font=(FONT_FAMILY, 12, "bold"), text_color=TEXT_DARK, anchor="w").pack(fill="x")
        tc = ctk.CTkComboBox(fi, values=["Añadir", "Quitar"], height=38, corner_radius=8, border_color=BORDER_COLOR, border_width=2, fg_color=LIGHT_GREY, text_color=TEXT_DARK, font=(FONT_FAMILY, 12), button_color=ROYAL_BLUE, button_hover_color=ROYAL_BLUE_HOVER)
        tc.pack(fill="x", pady=(3, 10))
        ctk.CTkLabel(fi, text="Cantidad (créditos)", font=(FONT_FAMILY, 12, "bold"), text_color=TEXT_DARK, anchor="w").pack(fill="x")
        ce = ctk.CTkEntry(fi, placeholder_text="5.0", height=38, corner_radius=8, border_color=BORDER_COLOR, border_width=2, fg_color=LIGHT_GREY, text_color=TEXT_DARK, font=(FONT_FAMILY, 12))
        ce.pack(fill="x", pady=(3, 10))
        msg = ctk.CTkLabel(fi, text="", font=(FONT_FAMILY, 12))
        msg.pack(pady=5)
        def ajustar():
            sel = uc.get()
            if not sel or sel == "Sin usuarios":
                msg.configure(text="Selecciona un usuario", text_color=ACCENT_RED)
                return
            uid = int(sel.split(" - ")[0])
            tipo = "CREDITO" if tc.get() == "Añadir" else "DEBITO"
            try:
                cant = float(ce.get().strip())
                if cant <= 0:
                    raise ValueError()
            except ValueError:
                msg.configure(text="Cantidad inválida", text_color=ACCENT_RED)
                return
            try:
                from clases.administrador import Administrador
                a = Administrador(self._admin.id, self._admin.name, self._admin.email, self._admin.password, self._admin.town, 1)
                a.ajustarSaldo(self._db, uid, cant, tipo)
                msg.configure(text="Saldo ajustado", text_color=ACCENT_GREEN)
                ce.delete(0, "end")
                signo = "+" if tipo == "CREDITO" else "-"
                self._db.agregar_notificacion(uid, "Ajuste de Saldo", f"Un administrador ha ajustado tu saldo: {signo}{cant} cr", "info")
            except ValueError as e:
                msg.configure(text=f"{str(e)}", text_color=ACCENT_RED)
        ctk.CTkButton(fi, text="Aplicar Ajuste", height=42, corner_radius=8, fg_color=ROYAL_BLUE, hover_color=ROYAL_BLUE_HOVER, font=(FONT_FAMILY, 14, "bold"), text_color=WHITE, command=ajustar).pack(fill="x")

    def _mostrar_servicios_admin(self):
        self._limpiar()
        ctk.CTkLabel(self._content_frame, text="Servicios", font=(FONT_FAMILY, 20, "bold"), text_color=TEXT_DARK, anchor="w").pack(fill="x", padx=20, pady=(20, 12))
        servicios = self._db.leer_servicios()
        if not servicios:
            ctk.CTkLabel(self._content_frame, text="No hay servicios", font=(FONT_FAMILY, 12), text_color=TEXT_SECONDARY).pack(pady=30)
            return
        for s in servicios:
            ec = ACCENT_GREEN if s["estado"] == "disponible" else TEXT_SECONDARY
            card = ctk.CTkFrame(self._content_frame, fg_color=WHITE, corner_radius=10)
            card.pack(fill="x", padx=20, pady=3)
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="x", padx=15, pady=10)
            top = ctk.CTkFrame(inner, fg_color="transparent")
            top.pack(fill="x")
            ctk.CTkLabel(top, text=s["titulo"], font=(FONT_FAMILY, 13, "bold"), text_color=TEXT_DARK, anchor="w").pack(side="left")
            ctk.CTkLabel(top, text=f" {s['estado'].upper()} ", font=(FONT_FAMILY, 10, "bold"), text_color=WHITE, fg_color=ec, corner_radius=6).pack(side="right")
            ctk.CTkLabel(inner, text=f"{s['proveedor_nombre']}  •  {s['categoria']}  •  {s['horas']} cr", font=(FONT_FAMILY, 10), text_color=TEXT_SECONDARY, anchor="w").pack(fill="x", pady=(3, 0))
            
            bf = ctk.CTkFrame(inner, fg_color="transparent")
            bf.pack(fill="x")
            from pantallas.dialogs import DialogoDetalleServicio
            ctk.CTkButton(bf, text="Ver Detalle", width=80, height=28, corner_radius=6, fg_color=ROYAL_BLUE, hover_color=ROYAL_BLUE_HOVER, text_color=WHITE, font=(FONT_FAMILY, 11, "bold"), command=lambda ss=s: DialogoDetalleServicio(self, ss, self._admin, self._db, lambda x: None)).pack(side="right")

    def _mostrar_aclaraciones_admin(self):
        self._limpiar()
        ctk.CTkLabel(self._content_frame, text="Aclaraciones", font=(FONT_FAMILY, 20, "bold"), text_color=TEXT_DARK, anchor="w").pack(fill="x", padx=20, pady=(20, 12))
        acls = self._db.leer_aclaraciones()
        if not acls:
            ctk.CTkLabel(self._content_frame, text="No hay aclaraciones pendientes", font=(FONT_FAMILY, 12), text_color=TEXT_SECONDARY).pack(pady=30)
            return
        for a in reversed(acls):
            card = ctk.CTkFrame(self._content_frame, fg_color=WHITE, corner_radius=10)
            card.pack(fill="x", padx=20, pady=4)
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="x", padx=15, pady=10)
            
            top = ctk.CTkFrame(inner, fg_color="transparent")
            top.pack(fill="x")
            ctk.CTkLabel(top, text=f"Intercambio #{a['intercambio_id']}", font=(FONT_FAMILY, 13, "bold"), text_color=TEXT_DARK, anchor="w").pack(side="left")
            
            ec = ACCENT_RED if a["estado"] == "abierta" else ACCENT_GREEN
            ctk.CTkLabel(top, text=f" {a['estado'].upper()} ", font=(FONT_FAMILY, 10, "bold"), text_color=WHITE, fg_color=ec, corner_radius=6).pack(side="right")
            
            ctk.CTkLabel(inner, text=f"{a['mensaje']}", font=(FONT_FAMILY, 11), text_color=TEXT_DARK, anchor="w", wraplength=400, justify="left").pack(fill="x", pady=(5, 5))
            ctk.CTkLabel(inner, text=f"Fecha: {a['fecha']}", font=(FONT_FAMILY, 10), text_color=TEXT_SECONDARY, anchor="w").pack(fill="x", pady=(0, 5))
            
            if a["estado"] == "abierta":
                bf = ctk.CTkFrame(inner, fg_color="transparent")
                bf.pack(fill="x")
                def resolver(aid=a["id"]):
                    self._db.actualizar_aclaracion(aid, "resuelta")
                    self._db.agregar_notificacion(a["solicitante_id"], "Aclaración Resuelta", f"Tu aclaración del intercambio #{a['intercambio_id']} fue resuelta.", "info")
                    self._mostrar_aclaraciones_admin()
                ctk.CTkButton(bf, text="Marcar Resuelta", width=120, height=28, corner_radius=6, fg_color=ACCENT_GREEN, hover_color="#218838", text_color=WHITE, font=(FONT_FAMILY, 11, "bold"), command=resolver).pack(side="right")
