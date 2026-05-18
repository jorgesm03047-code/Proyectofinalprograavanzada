import customtkinter as ctk
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.basededatos import BaseDeDatos
from clases.usuario import Usuario
from clases.consumidor import Consumidor
from clases.administrador import Administrador
from pantallas.login import LoginView, RegisterView
from pantallas.panel_usuario import PanelUsuario
from pantallas.panel_admin import PanelAdmin
from assets.styles import *
from datetime import date

# Clase principal de la aplicación
class TimeBankApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("t-bank — Banco de Tiempo")
        self.geometry("430x760")
        self.minsize(380, 600)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self._db = BaseDeDatos()
        self._usuario_actual = None
        self._vista_actual = None
        self._mostrar_login()

    def _limpiar_vista(self):
        if self._vista_actual:
            # Libera cualquier grab activo antes de destruir la vista
            try:
                self._vista_actual.grab_release()
            except Exception:
                pass
            self._vista_actual.destroy()
            self._vista_actual = None

    def _mostrar_login(self):
        self._limpiar_vista()
        self._usuario_actual = None
        self._vista_actual = LoginView(self, self._intentar_login, self._mostrar_registro)
        self._vista_actual.pack(fill="both", expand=True)
        # Fuerza el foco a la ventana raiz para que los campos respondan
        self.after(100, lambda: self.focus_force())

    def _mostrar_registro(self):
        self._limpiar_vista()
        self._vista_actual = RegisterView(self, self._registrar_usuario, self._mostrar_login)
        self._vista_actual.pack(fill="both", expand=True)

    # Validacion de credenciales del usuario
    def _intentar_login(self, email, password):
        datos = self._db.buscar_usuario_por_email(email)
        if not datos:
            self._vista_actual.mostrar_error("Usuario no encontrado")
            return
        if datos["password"] != password:
            self._vista_actual.mostrar_error("Contraseña incorrecta")
            return
        if str(datos.get("activo", "1")) == "0":
            self._vista_actual.mostrar_error("Tu cuenta está suspendida")
            return
        if datos["rol"] == "admin":
            self._usuario_actual = Administrador(
                datos["id"], datos["name"], datos["email"], datos["password"],
                datos["town"], 1, None, datos["fechaRegistro"],
                datos["saldo_horas"], datos["activo"], datos["rol"],
            )
            self._mostrar_panel_admin()
        else:
            self._usuario_actual = Consumidor(
                datos["id"], datos["name"], datos["email"], datos["password"],
                datos["town"], datos["fechaRegistro"], datos["saldo_horas"],
                datos["activo"], datos["rol"],
            )
            self._mostrar_panel_usuario()

    # Registro de nuevo usuario en la base de datos
    def _registrar_usuario(self, name, email, password, town):
        existente = self._db.buscar_usuario_por_email(email)
        if existente:
            self._vista_actual.mostrar_error("El correo ya está registrado")
            return
        nuevo_id = self._db.obtener_siguiente_id_usuario()
        consumidor = Consumidor(nuevo_id, name, email, password, town)
        consumidor.registrar(self._db)
        self._usuario_actual = consumidor
        self._mostrar_panel_usuario()

    def _mostrar_panel_usuario(self):
        self._limpiar_vista()
        self._vista_actual = PanelUsuario(self, self._usuario_actual, self._db, self._mostrar_login)
        self._vista_actual.pack(fill="both", expand=True)

    def _mostrar_panel_admin(self):
        self._limpiar_vista()
        self._vista_actual = PanelAdmin(self, self._usuario_actual, self._db, self._mostrar_login)
        self._vista_actual.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = TimeBankApp()
    app.mainloop()
