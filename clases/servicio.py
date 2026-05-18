from datetime import date

# Modelo de servicio publicado en la plataforma
class Servicio:
    def __init__(self, id, proveedor_id, proveedor_nombre, titulo, descripcion, categoria, horas, estado="disponible", fecha=None):
        self._id = int(id)
        self._proveedor_id = int(proveedor_id)
        self._proveedor_nombre = str(proveedor_nombre)
        self._titulo = str(titulo)
        self._descripcion = str(descripcion)
        self._categoria = str(categoria)
        self._horas = float(horas)
        self._estado = str(estado)
        self._fecha = fecha if fecha else date.today().isoformat()

    @property
    def id(self):
        return self._id

    @property
    def proveedor_id(self):
        return self._proveedor_id

    @property
    def titulo(self):
        return self._titulo

    @property
    def descripcion(self):
        return self._descripcion

    @property
    def categoria(self):
        return self._categoria

    @property
    def horas(self):
        return self._horas

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, value):
        self._estado = str(value)

    # Serializa el servicio a diccionario para CSV
    def to_dict(self):
        return {
            "id": self._id,
            "proveedor_id": self._proveedor_id,
            "proveedor_nombre": self._proveedor_nombre,
            "titulo": self._titulo,
            "descripcion": self._descripcion,
            "categoria": self._categoria,
            "horas": self._horas,
            "estado": self._estado,
            "fecha": self._fecha,
        }

    def __str__(self):
        return f"Servicio({self._id}, {self._titulo}, {self._horas}h)"
