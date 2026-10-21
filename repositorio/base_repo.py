import sqlite3

from dominio.excepciones import ErrorBaseDatos, RegistroDuplicadoError


class BaseRepositorio:
    """Lógica común a todos los repositorios: ejecutar SQL parametrizado y traducir errores.
    Los repositorios hijos solo escriben su SQL (siempre con marcadores ?)."""

    def __init__(self, bd):
        self._bd = bd

    @staticmethod
    def traducir_error(error):
        """Convierte una excepción cruda de sqlite3 en una excepción del negocio."""
        if isinstance(error, sqlite3.IntegrityError):
            if "UNIQUE" in str(error) or "PRIMARY KEY" in str(error):
                return RegistroDuplicadoError("Ya existe un registro con esos datos únicos.")
            return ErrorBaseDatos(f"Se violó una regla de integridad: {error}")
        return ErrorBaseDatos(f"Error de base de datos: {error}")

    def _ejecutar(self, sql, parametros=()):
        conn = self._bd.conexion
        try:
            cursor = conn.execute(sql, parametros)
            conn.commit()
            return cursor
        except sqlite3.Error as error:
            conn.rollback()
            raise self.traducir_error(error) from error

    def _consultar(self, sql, parametros=()):
        try:
            return self._bd.conexion.execute(sql, parametros).fetchall()
        except sqlite3.Error as error:
            raise self.traducir_error(error) from error
