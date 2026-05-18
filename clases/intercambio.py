from datetime import date

# Representa un intercambio entre dos usuarios
class Intercambio:
    def __init__(self, id, servicio_id, solicitante_id, solicitante_nombre, proveedor_id, proveedor_nombre, horas, estado="pendiente", fecha=None):
        self._id = int(id)
        self._servicio_id = int(servicio_id)
        self._solicitante_id = int(solicitante_id)
        self._solicitante_nombre = str(solicitante_nombre)
        self._proveedor_id = int(proveedor_id)
        self._proveedor_nombre = str(proveedor_nombre)
        self._horas = float(horas)
        self._estado = str(estado)
        self._fecha = fecha if fecha else date.today().isoformat()

    @property
    def id(self):
        return self._id

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, value):  # Actualiza el estado del intercambio
        self._estado = str(value)

    def to_dict(self):
        return {
            "id": self._id,
            "servicio_id": self._servicio_id,
            "solicitante_id": self._solicitante_id,
            "solicitante_nombre": self._solicitante_nombre,
            "proveedor_id": self._proveedor_id,
            "proveedor_nombre": self._proveedor_nombre,
            "horas": self._horas,
            "estado": self._estado,
            "fecha": self._fecha,
        }

    def __str__(self):
        return f"Intercambio({self._id}, {self._estado}, {self._horas}h)"