import sqlite3
from datetime import date

from dominio import Credencial, Departamento, Empleado, Perfil, RegistroNoEncontradoError
from repositorio.base_repo import BaseRepositorio

_COLUMNAS = ("e.id_persona, e.nombre_completo, e.direccion, e.telefono, e.correo, "
             "e.sueldo_base, e.fecha_ingreso, d.codigo_depto, d.nombre_depto")
_BASE_SELECT = (f"SELECT {_COLUMNAS} FROM empleado e "
                "LEFT JOIN departamento d ON d.codigo_depto = e.codigo_depto ")


class EmpleadoRepositorio(BaseRepositorio):
    """CRUD de Empleado y operaciones con su Credencial. Todo el SQL usa parámetros (?)."""

    @staticmethod
    def _fila_a_empleado(fila, deptos=None):
        """Único punto donde una fila (tupla) de la BD se transforma en un objeto Empleado."""
        empleado = Empleado(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5],
                            date.fromisoformat(fila[6]))
        if fila[7] is not None:
            deptos = deptos if deptos is not None else {}
            depto = deptos.setdefault(fila[7], Departamento(fila[7], fila[8]))
            empleado.cambiarDepartamento(depto)
        return empleado

    @staticmethod
    def _parametros(empleado):
        depto = empleado.departamento.codigoDepto if empleado.departamento else None
        return (empleado.idPersona, empleado.nombreCompleto, empleado.direccionParticular,
                empleado.telefonoContacto, empleado.correoElectronico, empleado.sueldoBase,
                empleado.fechaIngreso.isoformat(), depto)

    _SQL_INSERT = ("INSERT INTO empleado (id_persona, nombre_completo, direccion, telefono, correo, "
                   "sueldo_base, fecha_ingreso, codigo_depto) VALUES (?, ?, ?, ?, ?, ?, ?, ?)")

    def guardar(self, empleado):
        self._ejecutar(self._SQL_INSERT, self._parametros(empleado))

    def obtener_por_id(self, id_persona):
        filas = self._consultar(_BASE_SELECT + "WHERE e.id_persona = ? AND e.activo = 1", (id_persona,))
        if not filas:
            raise RegistroNoEncontradoError(f"No existe un empleado activo con id {id_persona}.")
        return self._fila_a_empleado(filas[0])

    def buscar_por_nombre(self, nombre):
        """Búsqueda exacta por nombre. El valor viaja como parámetro, nunca dentro del texto SQL."""
        filas = self._consultar(_BASE_SELECT + "WHERE e.nombre_completo = ? AND e.activo = 1", (nombre,))
        deptos = {}
        return [self._fila_a_empleado(f, deptos) for f in filas]

    def listar_activos(self):
        filas = self._consultar(_BASE_SELECT + "WHERE e.activo = 1 ORDER BY e.id_persona")
        deptos = {}
        return [self._fila_a_empleado(f, deptos) for f in filas]

    def actualizar(self, empleado):
        depto = empleado.departamento.codigoDepto if empleado.departamento else None
        cursor = self._ejecutar(
            "UPDATE empleado SET nombre_completo = ?, direccion = ?, telefono = ?, correo = ?, "
            "sueldo_base = ?, codigo_depto = ? WHERE id_persona = ? AND activo = 1",
            (empleado.nombreCompleto, empleado.direccionParticular, empleado.telefonoContacto,
             empleado.correoElectronico, empleado.sueldoBase, depto, empleado.idPersona))
        if cursor.rowcount == 0:
            raise RegistroNoEncontradoError(f"No existe un empleado activo con id {empleado.idPersona}.")

    def eliminar(self, id_persona):
        # Borrado lógico: el empleado se conserva en la BD pero deja de aparecer en los listados
        cursor = self._ejecutar("UPDATE empleado SET activo = 0 WHERE id_persona = ? AND activo = 1",
                                (id_persona,))
        if cursor.rowcount == 0:
            raise RegistroNoEncontradoError(f"No existe un empleado activo con id {id_persona}.")

    def registrar_con_credencial(self, empleado, credencial):
        """Operación atómica: o se guardan el empleado Y su credencial, o no se guarda nada."""
        conn = self._bd.conexion
        try:
            conn.execute(self._SQL_INSERT, self._parametros(empleado))            # 1ª escritura
            conn.execute("INSERT INTO credencial (nombre_usuario, clave_cifrada, habilitada, perfil, id_persona) "
                         "VALUES (?, ?, ?, ?, ?)",                                 # 2ª escritura
                         (credencial.nombreUsuario, credencial.claveCifrada,
                          int(credencial.habilitada), credencial.perfil.etiqueta, empleado.idPersona))
            conn.commit()                                                          # todo salió bien
        except sqlite3.Error as error:
            conn.rollback()                                                        # deshace la 1ª escritura
            raise self.traducir_error(error) from error

    def obtener_credencial(self, nombre_usuario):
        filas = self._consultar(
            "SELECT c.nombre_usuario, c.clave_cifrada, c.habilitada, c.perfil, c.id_persona "
            "FROM credencial c WHERE c.nombre_usuario = ?", (nombre_usuario,))
        if not filas:
            raise RegistroNoEncontradoError(f"No existe el usuario '{nombre_usuario}'.")
        usuario, clave_cifrada, habilitada, perfil, id_persona = filas[0]
        empleado = self.obtener_por_id(id_persona)
        return Credencial(empleado, usuario, clave_cifrada, Perfil(perfil),
                          habilitada=bool(habilitada), ya_cifrada=True)
