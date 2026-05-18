import os
import csv
from datetime import datetime

# Registro de movimientos de créditos
class Transaccion:
    _CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "transacciones.csv")

    def __init__(self, id, usuario_id, tipo, horas, saldoAntes, saldoDespues, fecha=None):
        self._id = int(id)
        self._usuario_id = int(usuario_id)
        self._tipo = str(tipo)
        self._horas = float(horas)
        self._saldoAntes = float(saldoAntes)
        self._saldoDespues = float(saldoDespues)
        self._fecha = fecha if fecha else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def id(self):
        return self._id

    @property
    def usuario_id(self):
        return self._usuario_id

    @property
    def tipo(self):
        return self._tipo

    @property
    def horas(self):
        return self._horas

    @property
    def saldoAntes(self):
        return self._saldoAntes

    @property
    def saldoDespues(self):
        return self._saldoDespues

    @property
    def fecha(self):
        return self._fecha

    def registrar(self, db_handler):
        data = self.to_dict()
        db_handler.agregar_transaccion(data)

    def revertir(self, db_handler):
        transacciones = db_handler.leer_transacciones()
        nuevo_id = max([int(t["id"]) for t in transacciones], default=0) + 1
        tipo_revertido = "CREDITO" if self._tipo == "DEBITO" else "DEBITO"
        saldo_actual = self._saldoDespues
        if tipo_revertido == "CREDITO":
            nuevo_saldo = saldo_actual + self._horas
        else:
            nuevo_saldo = saldo_actual - self._horas
        reversion = Transaccion(nuevo_id, self._usuario_id, tipo_revertido, self._horas, saldo_actual, nuevo_saldo)
        reversion.registrar(db_handler)
        db_handler.actualizar_saldo(self._usuario_id, nuevo_saldo)
        return reversion

    def to_dict(self):
        return {
            "id": self._id,
            "usuario_id": self._usuario_id,
            "tipo": self._tipo,
            "horas": self._horas,
            "saldoAntes": self._saldoAntes,
            "saldoDespues": self._saldoDespues,
            "fecha": self._fecha,
        }

    @classmethod
    def crear(cls, db_handler, usuario_id, tipo, horas, saldo_antes, saldo_despues):  # Metodo de fabrica
        transacciones = db_handler.leer_transacciones()
        nuevo_id = max([int(t["id"]) for t in transacciones], default=0) + 1
        t = cls(nuevo_id, usuario_id, tipo, horas, saldo_antes, saldo_despues)
        t.registrar(db_handler)
        return t

    def __str__(self):
        return f"Transaccion({self._id}, {self._tipo}, {self._horas}h, {self._fecha})"