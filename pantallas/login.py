import customtkinter as ctk
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from assets.styles import *

# Vista de inicio de sesion
class LoginView(ctk.CTkFrame):
    def __init__(self, master, on_login_callback, on_register_callback):
        super().__init__(master, fg_color=ROYAL_BLUE)
        self._on_login = on_login_callback
        self._on_register = on_register_callback
        self._error_label = None
        self._construir_interfaz()

    def _construir_interfaz(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=0, column=0)

        header_frame = ctk.CTkFrame(container, fg_color="transparent")
        header_frame.pack(pady=(0, 10))

        icon_label = ctk.CTkLabel(
            header_frame,
            text="",
            font=(FONT_FAMILY, 52),
            text_color=WHITE,
        )
        icon_label.pack()

        title = ctk.CTkLabel(
            header_frame,
            text="t-bank",
            font=(FONT_FAMILY, 36, "bold"),
            text_color=WHITE,
        )
        title.pack()

        subtitle = ctk.CTkLabel(
            header_frame,
            text="Banco de Tiempo Comunitario",
            font=(FONT_FAMILY, 14),
            text_color="#a0b4d6",
        )
        subtitle.pack(pady=(0, 5))

        card = ctk.CTkFrame(
            container,
            fg_color=WHITE,
            corner_radius=20,
            width=420,
        )
        card.pack(padx=40, pady=10)

        card_inner = ctk.CTkFrame(card, fg_color="transparent")
        card_inner.pack(expand=True, fill="both", padx=40, pady=30)

        login_title = ctk.CTkLabel(
            card_inner,
            text="Iniciar Sesión",
            font=(FONT_FAMILY, 22, "bold"),
            text_color=TEXT_DARK,
        )
        login_title.pack(pady=(0, 5))

        login_sub = ctk.CTkLabel(
            card_inner,
            text="Ingresa tus credenciales para continuar",
            font=(FONT_FAMILY, 12),
            text_color=TEXT_SECONDARY,
        )
        login_sub.pack(pady=(0, 20))

        email_label = ctk.CTkLabel(
            card_inner,
            text="Correo Electrónico",
            font=(FONT_FAMILY, 13, "bold"),
            text_color=TEXT_DARK,
            anchor="w",
        )
        email_label.pack(fill="x")

        self._email_entry = ctk.CTkEntry(
            card_inner,
            placeholder_text="tu@correo.com",
            height=42,
            corner_radius=10,
            border_color=BORDER_COLOR,
            border_width=2,
            fg_color=LIGHT_GREY,
            text_color=TEXT_DARK,
            placeholder_text_color=TEXT_SECONDARY,
            font=(FONT_FAMILY, 13),
        )
        self._email_entry.pack(fill="x", pady=(5, 12))

        pass_label = ctk.CTkLabel(
            card_inner,
            text="Contraseña",
            font=(FONT_FAMILY, 13, "bold"),
            text_color=TEXT_DARK,
            anchor="w",
        )
        pass_label.pack(fill="x")

        self._password_entry = ctk.CTkEntry(
            card_inner,
            placeholder_text="••••••••",
            show="•",
            height=42,
            corner_radius=10,
            border_color=BORDER_COLOR,
            border_width=2,
            fg_color=LIGHT_GREY,
            text_color=TEXT_DARK,
            placeholder_text_color=TEXT_SECONDARY,
            font=(FONT_FAMILY, 13),
        )
        self._password_entry.pack(fill="x", pady=(5, 5))

        self._error_label = ctk.CTkLabel(
            card_inner,
            text="",
            font=(FONT_FAMILY, 12),
            text_color=ACCENT_RED,
        )
        self._error_label.pack(pady=(2, 2))

        login_btn = ctk.CTkButton(
            card_inner,
            text="Ingresar",
            height=44,
            corner_radius=10,
            fg_color=ROYAL_BLUE,
            hover_color=ROYAL_BLUE_HOVER,
            font=(FONT_FAMILY, 15, "bold"),
            text_color=WHITE,
            command=self._intentar_login,
        )
        login_btn.pack(fill="x", pady=(5, 10))

        self._password_entry.bind("<Return>", lambda e: self._intentar_login())

        separator_frame = ctk.CTkFrame(card_inner, fg_color="transparent")
        separator_frame.pack(fill="x", pady=5)

        left_line = ctk.CTkFrame(separator_frame, fg_color=BORDER_COLOR, height=1)
        left_line.pack(side="left", expand=True, fill="x", padx=(0, 10))
        or_label = ctk.CTkLabel(separator_frame, text="o", font=(FONT_FAMILY, 12), text_color=TEXT_SECONDARY)
        or_label.pack(side="left")
        right_line = ctk.CTkFrame(separator_frame, fg_color=BORDER_COLOR, height=1)
        right_line.pack(side="left", expand=True, fill="x", padx=(10, 0))

        register_btn = ctk.CTkButton(
            card_inner,
            text="Crear Cuenta Nueva",
            height=42,
            corner_radius=10,
            fg_color="transparent",
            hover_color=LIGHT_GREY,
            border_color=ROYAL_BLUE,
            border_width=2,
            font=(FONT_FAMILY, 14, "bold"),
            text_color=ROYAL_BLUE,
            command=self._mostrar_registro,
        )
        register_btn.pack(fill="x", pady=(5, 0))

        footer = ctk.CTkLabel(
            container,
            text="© 2026 t-bank — Todos los derechos reservados",
            font=(FONT_FAMILY, 11),
            text_color="#7a8bb5",
        )
        footer.pack(pady=(15, 0))

    def _intentar_login(self):
        email = self._email_entry.get().strip()
        password = self._password_entry.get().strip()
        if not email or not password:
            self._error_label.configure(text="Completa todos los campos")
            return
        self._error_label.configure(text="")
        self._on_login(email, password)

    def mostrar_error(self, mensaje):
        if self._error_label:
            self._error_label.configure(text=f"{mensaje}")

    def _mostrar_registro(self):
        self._on_register()

# Vista de registro de nuevos usuarios
class RegisterView(ctk.CTkFrame):
    def __init__(self, master, on_register_callback, on_back_callback):
        super().__init__(master, fg_color=ROYAL_BLUE)
        self._on_register = on_register_callback
        self._on_back = on_back_callback
        self._error_label = None
        self._construir_interfaz()

    def _construir_interfaz(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=0, column=0)

        header_frame = ctk.CTkFrame(container, fg_color="transparent")
        header_frame.pack(pady=(0, 10))

        icon_label = ctk.CTkLabel(header_frame, text="", font=(FONT_FAMILY, 42), text_color=WHITE)
        icon_label.pack()

        title = ctk.CTkLabel(header_frame, text="Registro", font=(FONT_FAMILY, 30, "bold"), text_color=WHITE)
        title.pack()

        card = ctk.CTkFrame(container, fg_color=WHITE, corner_radius=20, width=450)
        card.pack(padx=40, pady=10)

        card_inner = ctk.CTkFrame(card, fg_color="transparent")
        card_inner.pack(expand=True, fill="both", padx=40, pady=25)

        fields = [
            ("Nombre Completo", "Tu nombre completo"),
            ("Correo Electrónico", "tu@correo.com"),
            ("Contraseña", "••••••••"),
            ("Ciudad / Localidad", "Tu ciudad"),
            ("Colonia", "Tu colonia o barrio"),
        ]
        self._entries = {}
        for label_text, placeholder in fields:
            lbl = ctk.CTkLabel(card_inner, text=label_text, font=(FONT_FAMILY, 13, "bold"), text_color=TEXT_DARK, anchor="w")
            lbl.pack(fill="x")
            show = "•" if "Contraseña" in label_text else ""
            entry = ctk.CTkEntry(
                card_inner, placeholder_text=placeholder, height=40, corner_radius=10,
                border_color=BORDER_COLOR, border_width=2, fg_color=LIGHT_GREY,
                text_color=TEXT_DARK, placeholder_text_color=TEXT_SECONDARY,
                font=(FONT_FAMILY, 13), show=show if show else None,
            )
            if not show:
                entry.configure(show="")
            entry.pack(fill="x", pady=(3, 10))
            self._entries[label_text] = entry

        self._error_label = ctk.CTkLabel(card_inner, text="", font=(FONT_FAMILY, 12), text_color=ACCENT_RED)
        self._error_label.pack(pady=(0, 5))

        register_btn = ctk.CTkButton(
            card_inner, text="Registrarse", height=44, corner_radius=10,
            fg_color=ROYAL_BLUE, hover_color=ROYAL_BLUE_HOVER,
            font=(FONT_FAMILY, 15, "bold"), text_color=WHITE,
            command=self._intentar_registro,
        )
        register_btn.pack(fill="x", pady=(0, 8))

        back_btn = ctk.CTkButton(
            card_inner, text="← Volver al Login", height=40, corner_radius=10,
            fg_color="transparent", hover_color=LIGHT_GREY,
            border_color=ROYAL_BLUE, border_width=2,
            font=(FONT_FAMILY, 13, "bold"), text_color=ROYAL_BLUE,
            command=self._on_back,
        )
        back_btn.pack(fill="x")

    def _intentar_registro(self):
        name = self._entries["Nombre Completo"].get().strip()
        email = self._entries["Correo Electrónico"].get().strip()
        password = self._entries["Contraseña"].get().strip()
        town = self._entries["Ciudad / Localidad"].get().strip()
        colonia = self._entries["Colonia"].get().strip()
        if not all([name, email, password, town, colonia]):
            self._error_label.configure(text="Completa todos los campos")
            return
        if "@" not in email:
            self._error_label.configure(text="Correo electrónico inválido")
            return
        if len(password) < 4:
            self._error_label.configure(text="La contraseña debe tener al menos 4 caracteres")
            return
        self._error_label.configure(text="")
        # Concatenamos ciudad y colonia para el campo town
        self._on_register(name, email, password, f"{town}, {colonia}")

    def mostrar_error(self, mensaje):
        if self._error_label:
            self._error_label.configure(text=f"{mensaje}")
