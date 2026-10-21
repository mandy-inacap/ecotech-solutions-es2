from datetime import date

from dominio.persona import Persona
from dominio.validaciones import fecha_valida, numero_positivo


class Empleado(Persona):
    """Empleado ES UNA Persona. Pertenece a un Departamento (agregación)."""

    def __init__(self, idPersona, nombreCompleto, direccionParticular, telefonoContacto,
                 correoElectronico, sueldoBase, fechaIngreso):
        super().__init__(idPersona, nombreCompleto, direccionParticular, telefonoContacto, correoElectronico)
        self.__sueldoBase = numero_positivo(sueldoBase, "El sueldo base")   # -sueldoBase : float
        self.fechaIngreso = fecha_valida(fechaIngreso, "La fecha de ingreso")  # +fechaIngreso : date
        self.__departamento = None
        self.__credencial = None   # 0..1 Credencial

    @property
    def sueldoBase(self):
        return self.__sueldoBase

    @sueldoBase.setter
    def sueldoBase(self, valor):
        self.__sueldoBase = numero_positivo(valor, "El sueldo base")

    @property
    def departamento(self):
        return self.__departamento

    @property
    def credencial(self):
        return self.__credencial

    def _vincular_credencial(self, credencial):
        self.__credencial = credencial

    def antiguedadEnAnios(self):
        hoy = date.today()
        anios = hoy.year - self.fechaIngreso.year
        if (hoy.month, hoy.day) < (self.fechaIngreso.month, self.fechaIngreso.day):
            anios -= 1
        return anios

    def cambiarDepartamento(self, nuevo):
        """Mantiene consistentes ambos lados de la relación Departamento–Empleado."""
        if self.__departamento is nuevo:
            return True
        if self.__departamento is not None:
            self.__departamento._quitar(self)
        self.__departamento = nuevo
        if nuevo is not None:
            nuevo._agregar(self)
        return True

    def descripcion(self):
        depto = self.__departamento.nombreDepto if self.__departamento else "sin departamento"
        return f"[{self.idPersona}] {self._nombreCompleto} <{self._correoElectronico}> - {depto}"
