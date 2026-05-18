import os
import sys
import csv
from datetime import date, datetime

# Clase base para todos los usuarios del sistema
class Usuario:
    _CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "usuarios.csv")
    _TRANS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "transacciones.csv")

    def __init__(self, id, name, email, password, town, fechaRegistro=None, saldo_horas=10.0, activo=True, rol="consumidor"):
        self._id = int(id)
        self._name = str(name)
        self._email = str(email)
        self._password = str(password)
        self._town = str(town)
        self._fechaRegistro = fechaRegistro if fechaRegistro else date.today().isoformat()
        self._saldo_horas = float(saldo_horas)
        self._activo = bool(int(activo)) if isinstance(activo, str) else bool(activo)
        self._rol = str(rol)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = str(value)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = str(value)

    @property
    def password(self):
        return self._password

    @property
    def town(self):
        return self._town

    @town.setter
    def town(self, value):
        self._town = str(value)

    @property
    def fechaRegistro(self):
        return self._fechaRegistro

    @property
    def saldo_horas(self):
        return self._saldo_horas

    @saldo_horas.setter
    def saldo_horas(self, value):
        self._saldo_horas = float(value)

    @property
    def activo(self):
        return self._activo

    @activo.setter
    def activo(self, value):
        self._activo = bool(value)

    @property
    def rol(self):
        return self._rol

    # Retorna el saldo disponible del usuario
    def consultarSaldo(self):
        return self._saldo_horas

    def verHistorial(self):
        if not os.path.exists(self._TRANS_PATH):
            return []
        historial = []
        with open(self._TRANS_PATH, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if int(row["usuario_id"]) == self._id:
                    historial.append(row)
        return historial

    # Convierte los datos del usuario a diccionario
    def to_dict(self):
        return {
            "id": self._id,
            "name": self._name,
            "email": self._email,
            "password": self._password,
            "town": self._town,
            "fechaRegistro": self._fechaRegistro,
            "saldo_horas": self._saldo_horas,
            "activo": 1 if self._activo else 0,
            "rol": self._rol,
        }

    def __str__(self):
        return f"Usuario({self._id}, {self._name}, {self._email}, Saldo: {self._saldo_horas}h)"

    def __repr__(self):
        return self.__str__()