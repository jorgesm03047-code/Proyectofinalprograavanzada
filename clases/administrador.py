import os
import csv
from datetime import date
from clases.usuario import Usuario

# Administrador con permisos elevados
class Administrador(Usuario):
    def __init__(self, id, name, email, password, town, nivelAcceso=1, fechaNombramiento=None,
                 fechaRegistro=None, saldo_horas=10.0, activo=True, rol="admin"):
        super().__init__(id, name, email, password, town, fechaRegistro, saldo_horas, activo, rol)
        self._nivelAcceso = int(nivelAcceso)
        self._fechaNombramiento = fechaNombramiento if fechaNombramiento else date.today().isoformat()

    @property
    def nivelAcceso(self):
        return self._nivelAcceso

    @property
    def fechaNombramiento(self):
        return self._fechaNombramiento

    def validarIntercambio(self, db_handler, intercambio_id, aprobado=True):
        intercambios = db_handler.leer_intercambios()
        intercambio = None
        for i in intercambios:
            if int(i["id"]) == int(intercambio_id):
                intercambio = i
                break
        if not intercambio:
            raise ValueError("Intercambio no encontrado")
        if intercambio["estado"] != "pendiente":
            raise ValueError("Este intercambio ya fue procesado")
        if aprobado:
            horas = float(intercambio["horas"])
            solicitante_id = int(intercambio["solicitante_id"])
            proveedor_id = int(intercambio["proveedor_id"])
            db_handler.transferir_horas(solicitante_id, proveedor_id, horas)
            db_handler.actualizar_intercambio(intercambio_id, "aprobado")
            servicio_id = int(intercambio["servicio_id"])
            db_handler.actualizar_servicio_estado(servicio_id, "completado")
        else:
            db_handler.actualizar_intercambio(intercambio_id, "rechazado")

    def suspenderUsuario(self, db_handler, usuario_id):
        db_handler.actualizar_estado_usuario(usuario_id, False)

    def reactivarUsuario(self, db_handler, usuario_id):
        db_handler.actualizar_estado_usuario(usuario_id, True)

    # Ajusta el saldo de créditos de un usuario
    def ajustarSaldo(self, db_handler, usuario_id, cantidad, tipo="CREDITO"):
        usuarios = db_handler.leer_usuarios()
        usuario = None
        for u in usuarios:
            if int(u["id"]) == int(usuario_id):
                usuario = u
                break
        if not usuario:
            raise ValueError("Usuario no encontrado")
        saldo_antes = float(usuario["saldo_horas"])
        if tipo == "CREDITO":
            nuevo_saldo = saldo_antes + float(cantidad)
        else:
            nuevo_saldo = saldo_antes - float(cantidad)
            if nuevo_saldo < 0:
                raise ValueError("El saldo no puede quedar negativo")
        db_handler.actualizar_saldo(usuario_id, nuevo_saldo)
        from clases.transaccion import Transaccion
        Transaccion.crear(db_handler, int(usuario_id), tipo, float(cantidad), saldo_antes, nuevo_saldo)

    # Genera reporte estadístico general
    def generarReporte(self, db_handler):
        usuarios = db_handler.leer_usuarios()
        intercambios = db_handler.leer_intercambios()
        servicios = db_handler.leer_servicios()
        total_usuarios = len(usuarios)
        activos = sum(1 for u in usuarios if str(u.get("activo", "1")) == "1")
        inactivos = total_usuarios - activos
        total_intercambios = len(intercambios)
        aprobados = sum(1 for i in intercambios if i["estado"] == "aprobado")
        pendientes = sum(1 for i in intercambios if i["estado"] == "pendiente")
        rechazados = sum(1 for i in intercambios if i["estado"] == "rechazado")
        total_servicios = len(servicios)
        disponibles = sum(1 for s in servicios if s["estado"] == "disponible")
        completados = sum(1 for s in servicios if s["estado"] == "completado")
        total_horas = sum(float(i["horas"]) for i in intercambios if i["estado"] == "aprobado")
        return {
            "total_usuarios": total_usuarios,
            "activos": activos,
            "inactivos": inactivos,
            "total_intercambios": total_intercambios,
            "aprobados": aprobados,
            "pendientes": pendientes,
            "rechazados": rechazados,
            "total_servicios": total_servicios,
            "disponibles": disponibles,
            "completados": completados,
            "total_horas": total_horas,
        }

    def resolverDisputa(self, db_handler, intercambio_id, decision):
        if decision == "revertir":
            intercambios = db_handler.leer_intercambios()
            intercambio = None
            for i in intercambios:
                if int(i["id"]) == int(intercambio_id):
                    intercambio = i
                    break
            if not intercambio:
                raise ValueError("Intercambio no encontrado")
            if intercambio["estado"] == "aprobado":
                horas = float(intercambio["horas"])
                db_handler.transferir_horas(int(intercambio["proveedor_id"]), int(intercambio["solicitante_id"]), horas)
                db_handler.actualizar_intercambio(intercambio_id, "revertido")
        elif decision == "cerrar":
            db_handler.actualizar_intercambio(intercambio_id, "disputa_cerrada")

    def to_dict(self):
        data = super().to_dict()
        data["nivelAcceso"] = self._nivelAcceso
        data["fechaNombramiento"] = self._fechaNombramiento
        return data
