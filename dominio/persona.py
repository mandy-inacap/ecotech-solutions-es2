from abc import ABC, abstractmethod

from dominio.validaciones import correo_valido, entero_positivo, texto_no_vacio


class Persona(ABC):
    """«abstract» Persona: datos de contacto comunes (los hereda Empleado)."""

    def __init__(self, idPersona, nombreCompleto, direccionParticular, telefonoContacto, correoElectronico):
        self.__idPersona = entero_positivo(idPersona, "El id")                  # -idPersona
        self._nombreCompleto = texto_no_vacio(nombreCompleto, "El nombre")      # #nombreCompleto
        self._direccionParticular = direccionParticular or ""                   # #direccionParticular
        self._telefonoContacto = telefonoContacto or ""                         # #telefonoContacto
        self._correoElectronico = correo_valido(correoElectronico)              # #correoElectronico

    @property
    def idPersona(self):
        return self.__idPersona

    @property
    def nombreCompleto(self):
        return self._nombreCompleto

    @property
    def direccionParticular(self):
        return self._direccionParticular

    @property
    def telefonoContacto(self):
        return self._telefonoContacto

    @property
    def correoElectronico(self):
        return self._correoElectronico

    def actualizarContacto(self, direccion, telefono, correo):
        # Primero valida; solo si el correo es válido se modifican los atributos
        correo = correo_valido(correo)
        self._direccionParticular = direccion or ""
        self._telefonoContacto = telefono or ""
        self._correoElectronico = correo
        return True

    @abstractmethod
    def descripcion(self):
        """Cada subclase concreta define cómo se describe."""

    def __str__(self):
        return self.descripcion()
