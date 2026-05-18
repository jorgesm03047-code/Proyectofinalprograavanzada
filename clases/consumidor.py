import os
import csv
from datetime import date
from clases.usuario import Usuario

# Hereda de Usuario, representa al consumidor regular
class Consumidor(Usuario):
    def __init__(self, id, name, email, password, town, fechaRegistro=None, saldo_horas=10.0, activo=True, rol="consumidor"):
        super().__init__(id, name, email, password, town, fechaRegistro, saldo_horas, activo, rol)

    def registrar(self, db_handler):
        db_handler.agregar_usuario(self.to_dict())

    # Publica un nuevo servicio en la plataforma
    def publicarServicio(self, db_handler, titulo, descripcion, categoria, horas):
        servicios = db_handler.leer_servicios()
        nuevo_id = max([int(s["id"]) for s in servicios], default=0) + 1
        servicio = {
            "id": nuevo_id,
            "proveedor_id": self._id,
            "proveedor_nombre": self._name,
            "titulo": titulo,
            "descripcion": descripcion,
            "categoria": categoria,
            "horas": float(horas),
            "estado": "disponible",
            "fecha": date.today().isoformat(),
        }
        db_handler.agregar_servicio(servicio)
        return servicio

    # Solicita un intercambio por un servicio existente
    def aplicarAIntercambio(self, db_handler, servicio_id):
        servicios = db_handler.leer_servicios()
        servicio = None
        for s in servicios:
            if int(s["id"]) == int(servicio_id):
                servicio = s
                break
        if not servicio:
            raise ValueError("Servicio no encontrado")
        if servicio["estado"] != "disponible":
            raise ValueError("Servicio no disponible")
        if int(servicio["proveedor_id"]) == self._id:
            raise ValueError("No puedes aplicar a tu propio servicio")
        horas = float(servicio["horas"])
        if self._saldo_horas < horas:
            raise ValueError("Saldo insuficiente")
        intercambios = db_handler.leer_intercambios()
        nuevo_id = max([int(i["id"]) for i in intercambios], default=0) + 1
        intercambio = {
            "id": nuevo_id,
            "servicio_id": servicio_id,
            "solicitante_id": self._id,
            "solicitante_nombre": self._name,
            "proveedor_id": servicio["proveedor_id"],
            "proveedor_nombre": servicio["proveedor_nombre"],
            "horas": horas,
            "estado": "pendiente",
            "fecha": date.today().isoformat(),
        }
        db_handler.agregar_intercambio(intercambio)
        return intercambio