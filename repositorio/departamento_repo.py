from dominio import Departamento, RegistroNoEncontradoError
from repositorio.base_repo import BaseRepositorio


class DepartamentoRepositorio(BaseRepositorio):
    """CRUD de Departamento. Todo el SQL usa parámetros (?)."""

    @staticmethod
    def _fila_a_departamento(fila):
        return Departamento(fila[0], fila[1])

    def guardar(self, depto):
        self._ejecutar("INSERT INTO departamento (codigo_depto, nombre_depto) VALUES (?, ?)",
                       (depto.codigoDepto, depto.nombreDepto))

    def obtener_por_codigo(self, codigo):
        filas = self._consultar("SELECT codigo_depto, nombre_depto FROM departamento WHERE codigo_depto = ?",
                                (codigo,))
        if not filas:
            raise RegistroNoEncontradoError(f"No existe el departamento con código {codigo}.")
        return self._fila_a_departamento(filas[0])

    def listar(self):
        filas = self._consultar("SELECT codigo_depto, nombre_depto FROM departamento ORDER BY codigo_depto")
        return [self._fila_a_departamento(f) for f in filas]

    def actualizar(self, depto):
        cursor = self._ejecutar("UPDATE departamento SET nombre_depto = ? WHERE codigo_depto = ?",
                                (depto.nombreDepto, depto.codigoDepto))
        if cursor.rowcount == 0:
            raise RegistroNoEncontradoError(f"No existe el departamento con código {depto.codigoDepto}.")

    def eliminar(self, codigo):
        # Borrado físico; los empleados del departamento quedan sin departamento (ON DELETE SET NULL)
        cursor = self._ejecutar("DELETE FROM departamento WHERE codigo_depto = ?", (codigo,))
        if cursor.rowcount == 0:
            raise RegistroNoEncontradoError(f"No existe el departamento con código {codigo}.")
