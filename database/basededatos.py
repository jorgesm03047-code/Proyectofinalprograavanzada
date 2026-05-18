import os
import csv
import shutil
from datetime import datetime

# Manejo de persistencia en archivos CSV
class BaseDeDatos:
    def __init__(self):
        self._data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
        self._usuarios_path = os.path.join(self._data_dir, "usuarios.csv")
        self._servicios_path = os.path.join(self._data_dir, "servicios.csv")
        self._transacciones_path = os.path.join(self._data_dir, "transacciones.csv")
        self._intercambios_path = os.path.join(self._data_dir, "intercambios.csv")
        self._notificaciones_path = os.path.join(self._data_dir, "notificaciones.csv")
        self._valoraciones_path = os.path.join(self._data_dir, "valoraciones.csv")
        self._aclaraciones_path = os.path.join(self._data_dir, "aclaraciones.csv")
        self._inicializar()

    def _inicializar(self):
        os.makedirs(self._data_dir, exist_ok=True)
        if not os.path.exists(self._usuarios_path):
            with open(self._usuarios_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["id", "name", "email", "password", "town", "fechaRegistro", "saldo_horas", "activo", "rol"])
                writer.writerow([1, "Administrador", "admin@timebank.com", "admin123", "Ciudad Central", "2026-01-01", 999.0, 1, "admin"])
                writer.writerow([2, "Juan Pérez", "juan@email.com", "1234", "San José", "2026-05-01", 10.0, 1, "consumidor"])
                writer.writerow([3, "María López", "maria@email.com", "1234", "Heredia", "2026-05-02", 15.0, 1, "consumidor"])
                writer.writerow([4, "Carlos Rojas", "carlos@email.com", "1234", "Alajuela", "2026-05-03", 8.0, 1, "consumidor"])
        if not os.path.exists(self._servicios_path):
            with open(self._servicios_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["id", "proveedor_id", "proveedor_nombre", "titulo", "descripcion", "categoria", "horas", "estado", "fecha"])
                writer.writerow([1, 2, "Juan Pérez", "Clases de Guitarra", "Clases particulares de guitarra acústica nivel básico", "Educación", 2.0, "disponible", "2026-05-01"])
                writer.writerow([2, 3, "María López", "Diseño de Logo", "Diseño profesional de logotipos para emprendimientos", "Diseño", 3.0, "disponible", "2026-05-02"])
                writer.writerow([3, 4, "Carlos Rojas", "Reparación de PC", "Mantenimiento y reparación de computadoras", "Tecnología", 1.5, "disponible", "2026-05-03"])
                writer.writerow([4, 2, "Juan Pérez", "Tutoría de Matemáticas", "Ayuda con álgebra y cálculo universitario", "Educación", 2.5, "disponible", "2026-05-04"])
        if not os.path.exists(self._transacciones_path):
            with open(self._transacciones_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["id", "usuario_id", "tipo", "horas", "saldoAntes", "saldoDespues", "fecha"])
        if not os.path.exists(self._intercambios_path):
            with open(self._intercambios_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["id", "servicio_id", "solicitante_id", "solicitante_nombre", "proveedor_id", "proveedor_nombre", "horas", "estado", "fecha", "fecha_propuesta", "hora_propuesta", "mensaje"])
        if not os.path.exists(self._notificaciones_path):
            with open(self._notificaciones_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["id", "usuario_id", "titulo", "mensaje", "tipo", "leida", "fecha"])

    def _leer_csv(self, path):
        if not os.path.exists(path):
            return []
        with open(path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)

    # Escribe datos al CSV usando archivo temporal
    def _escribir_csv(self, path, datos, fieldnames):
        tmp_path = path + ".tmp"
        with open(tmp_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(datos)
        shutil.move(tmp_path, path)

    def leer_usuarios(self):
        return self._leer_csv(self._usuarios_path)

    def leer_servicios(self):
        return self._leer_csv(self._servicios_path)

    def leer_transacciones(self):
        return self._leer_csv(self._transacciones_path)

    def leer_intercambios(self):
        return self._leer_csv(self._intercambios_path)

    def agregar_usuario(self, usuario_dict):
        usuarios = self.leer_usuarios()
        for u in usuarios:
            if u["email"] == usuario_dict["email"]:
                raise ValueError("El correo ya está registrado")
        fieldnames = ["id", "name", "email", "password", "town", "fechaRegistro", "saldo_horas", "activo", "rol"]
        usuarios.append({k: usuario_dict.get(k, "") for k in fieldnames})
        self._escribir_csv(self._usuarios_path, usuarios, fieldnames)

    def agregar_servicio(self, servicio_dict):
        servicios = self.leer_servicios()
        fieldnames = ["id", "proveedor_id", "proveedor_nombre", "titulo", "descripcion", "categoria", "horas", "estado", "fecha"]
        servicios.append({k: servicio_dict.get(k, "") for k in fieldnames})
        self._escribir_csv(self._servicios_path, servicios, fieldnames)

    def agregar_transaccion(self, transaccion_dict):
        transacciones = self.leer_transacciones()
        fieldnames = ["id", "usuario_id", "tipo", "horas", "saldoAntes", "saldoDespues", "fecha"]
        transacciones.append({k: transaccion_dict.get(k, "") for k in fieldnames})
        self._escribir_csv(self._transacciones_path, transacciones, fieldnames)

    def agregar_intercambio(self, intercambio_dict):
        intercambios = self.leer_intercambios()
        fieldnames = ["id", "servicio_id", "solicitante_id", "solicitante_nombre", "proveedor_id", "proveedor_nombre", "horas", "estado", "fecha", "fecha_propuesta", "hora_propuesta", "mensaje"]
        intercambios.append({k: intercambio_dict.get(k, "") for k in fieldnames})
        self._escribir_csv(self._intercambios_path, intercambios, fieldnames)

    def buscar_usuario_por_email(self, email):
        usuarios = self.leer_usuarios()
        for u in usuarios:
            if u["email"] == email:
                return u
        return None

    def buscar_usuario_por_id(self, usuario_id):
        usuarios = self.leer_usuarios()
        for u in usuarios:
            if int(u["id"]) == int(usuario_id):
                return u
        return None

    def actualizar_saldo(self, usuario_id, nuevo_saldo):
        usuarios = self.leer_usuarios()
        for u in usuarios:
            if int(u["id"]) == int(usuario_id):
                u["saldo_horas"] = str(float(nuevo_saldo))
                break
        fieldnames = ["id", "name", "email", "password", "town", "fechaRegistro", "saldo_horas", "activo", "rol"]
        self._escribir_csv(self._usuarios_path, usuarios, fieldnames)

    def actualizar_estado_usuario(self, usuario_id, activo):
        usuarios = self.leer_usuarios()
        for u in usuarios:
            if int(u["id"]) == int(usuario_id):
                u["activo"] = "1" if activo else "0"
                break
        fieldnames = ["id", "name", "email", "password", "town", "fechaRegistro", "saldo_horas", "activo", "rol"]
        self._escribir_csv(self._usuarios_path, usuarios, fieldnames)

    def actualizar_intercambio(self, intercambio_id, nuevo_estado):
        intercambios = self.leer_intercambios()
        for i in intercambios:
            if int(i["id"]) == int(intercambio_id):
                i["estado"] = nuevo_estado
                break
        fieldnames = ["id", "servicio_id", "solicitante_id", "solicitante_nombre", "proveedor_id", "proveedor_nombre", "horas", "estado", "fecha", "fecha_propuesta", "hora_propuesta", "mensaje"]
        self._escribir_csv(self._intercambios_path, intercambios, fieldnames)

    def actualizar_servicio_estado(self, servicio_id, nuevo_estado):
        servicios = self.leer_servicios()
        for s in servicios:
            if int(s["id"]) == int(servicio_id):
                s["estado"] = nuevo_estado
                break
        fieldnames = ["id", "proveedor_id", "proveedor_nombre", "titulo", "descripcion", "categoria", "horas", "estado", "fecha"]
        self._escribir_csv(self._servicios_path, servicios, fieldnames)

    # Transfiere créditos entre dos usuarios
    def transferir_horas(self, de_usuario_id, a_usuario_id, horas):
        usuarios = self.leer_usuarios()
        de_usuario = None
        a_usuario = None
        for u in usuarios:
            if int(u["id"]) == int(de_usuario_id):
                de_usuario = u
            if int(u["id"]) == int(a_usuario_id):
                a_usuario = u
        if not de_usuario or not a_usuario:
            raise ValueError("Usuario no encontrado para transferencia")
        saldo_de = float(de_usuario["saldo_horas"])
        saldo_a = float(a_usuario["saldo_horas"])
        if saldo_de < horas:
            raise ValueError("Saldo insuficiente para la transferencia")
        nuevo_saldo_de = saldo_de - horas
        nuevo_saldo_a = saldo_a + horas
        de_usuario["saldo_horas"] = str(nuevo_saldo_de)
        a_usuario["saldo_horas"] = str(nuevo_saldo_a)
        fieldnames = ["id", "name", "email", "password", "town", "fechaRegistro", "saldo_horas", "activo", "rol"]
        self._escribir_csv(self._usuarios_path, usuarios, fieldnames)
        from clases.transaccion import Transaccion
        Transaccion.crear(self, int(de_usuario_id), "DEBITO", horas, saldo_de, nuevo_saldo_de)
        Transaccion.crear(self, int(a_usuario_id), "CREDITO", horas, saldo_a, nuevo_saldo_a)

    def obtener_siguiente_id_usuario(self):
        usuarios = self.leer_usuarios()
        if not usuarios:
            return 1
        return max(int(u["id"]) for u in usuarios) + 1

    def eliminar_servicio(self, servicio_id):
        servicios = self.leer_servicios()
        servicios = [s for s in servicios if int(s["id"]) != int(servicio_id)]
        fieldnames = ["id", "proveedor_id", "proveedor_nombre", "titulo", "descripcion", "categoria", "horas", "estado", "fecha"]
        self._escribir_csv(self._servicios_path, servicios, fieldnames)

    def leer_notificaciones(self):
        return self._leer_csv(self._notificaciones_path)

    def agregar_notificacion(self, usuario_id, titulo, mensaje, tipo="info"):
        notifs = self.leer_notificaciones()
        nuevo_id = max([int(n["id"]) for n in notifs], default=0) + 1
        fieldnames = ["id", "usuario_id", "titulo", "mensaje", "tipo", "leida", "fecha"]
        notifs.append({
            "id": nuevo_id,
            "usuario_id": str(usuario_id),
            "titulo": titulo,
            "mensaje": mensaje,
            "tipo": tipo,
            "leida": "0",
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        })
        self._escribir_csv(self._notificaciones_path, notifs, fieldnames)

    def obtener_notificaciones_usuario(self, usuario_id):
        notifs = self.leer_notificaciones()
        return [n for n in notifs if int(n["usuario_id"]) == int(usuario_id)]

    def marcar_notificacion_leida(self, notif_id):
        notifs = self.leer_notificaciones()
        for n in notifs:
            if int(n["id"]) == int(notif_id):
                n["leida"] = "1"
                break
        fieldnames = ["id", "usuario_id", "titulo", "mensaje", "tipo", "leida", "fecha"]
        self._escribir_csv(self._notificaciones_path, notifs, fieldnames)

    def marcar_todas_leidas(self, usuario_id):
        notifs = self.leer_notificaciones()
        for n in notifs:
            if int(n["usuario_id"]) == int(usuario_id):
                n["leida"] = "1"
        fieldnames = ["id", "usuario_id", "titulo", "mensaje", "tipo", "leida", "fecha"]
        self._escribir_csv(self._notificaciones_path, notifs, fieldnames)

    def contar_no_leidas(self, usuario_id):
        notifs = self.obtener_notificaciones_usuario(usuario_id)
        return sum(1 for n in notifs if n["leida"] == "0")

    def leer_valoraciones(self):
        return self._leer_csv(self._valoraciones_path)

    # Guarda valoracion de un usuario a otro
    def agregar_valoracion(self, usuario_evaluado_id, usuario_evaluador_id, estrellas, comentario):
        vals = self.leer_valoraciones()
        nuevo_id = max([int(v["id"]) for v in vals], default=0) + 1
        fieldnames = ["id", "usuario_evaluado_id", "usuario_evaluador_id", "estrellas", "comentario", "fecha"]
        vals.append({
            "id": nuevo_id,
            "usuario_evaluado_id": str(usuario_evaluado_id),
            "usuario_evaluador_id": str(usuario_evaluador_id),
            "estrellas": str(estrellas),
            "comentario": comentario,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        })
        self._escribir_csv(self._valoraciones_path, vals, fieldnames)

    def obtener_valoraciones_usuario(self, usuario_id):
        vals = self.leer_valoraciones()
        return [v for v in vals if int(v["usuario_evaluado_id"]) == int(usuario_id)]

    def leer_aclaraciones(self):
        return self._leer_csv(self._aclaraciones_path)

    def agregar_aclaracion(self, intercambio_id, solicitante_id, proveedor_id, mensaje):
        acls = self.leer_aclaraciones()
        nuevo_id = max([int(a["id"]) for a in acls], default=0) + 1
        fieldnames = ["id", "intercambio_id", "solicitante_id", "proveedor_id", "mensaje", "estado", "fecha"]
        acls.append({
            "id": nuevo_id,
            "intercambio_id": str(intercambio_id),
            "solicitante_id": str(solicitante_id),
            "proveedor_id": str(proveedor_id),
            "mensaje": mensaje,
            "estado": "abierta",
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        })
        self._escribir_csv(self._aclaraciones_path, acls, fieldnames)

    def actualizar_aclaracion(self, aclaracion_id, nuevo_estado):
        acls = self.leer_aclaraciones()
        for a in acls:
            if int(a["id"]) == int(aclaracion_id):
                a["estado"] = nuevo_estado
                break
        fieldnames = ["id", "intercambio_id", "solicitante_id", "proveedor_id", "mensaje", "estado", "fecha"]
        self._escribir_csv(self._aclaraciones_path, acls, fieldnames)

