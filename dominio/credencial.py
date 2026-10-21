from dominio.excepciones import DatoInvalidoError
from dominio.gestor_cifrado import GestorCifrado
from dominio.validaciones import texto_no_vacio


class Credencial:
    """Credencial de un Empleado (0..1), habilitada por un Perfil. Usa GestorCifrado."""

    def __init__(self, empleado, nombreUsuario, clave, perfil, habilitada=True, ya_cifrada=False):
        self.__nombreUsuario = texto_no_vacio(nombreUsuario, "El nombre de usuario")
        if ya_cifrada:
            self.__claveCifrada = clave                          # viene desde la BD (ya es un hash)
        else:
            clave = texto_no_vacio(clave, "La clave")
            if len(clave) < 8:
                raise DatoInvalidoError("La clave debe tener al menos 8 caracteres.")
            self.__claveCifrada = GestorCifrado.encriptar(clave)  # -claveCifrada : str
        self.__habilitada = habilitada                           # -habilitada : bool
        self.empleado = empleado
        self.perfil = perfil
        empleado._vincular_credencial(self)

    @property
    def nombreUsuario(self):
        return self.__nombreUsuario

    @property
    def claveCifrada(self):
        """Solo lectura: es el hash, nunca la clave en texto plano."""
        return self.__claveCifrada

    @property
    def habilitada(self):
        return self.__habilitada

    def validarAcceso(self, clave):
        return self.__habilitada and GestorCifrado.validar(clave, self.__claveCifrada)

    def actualizarClave(self, actual, nueva):
        if not self.validarAcceso(actual):
            return False
        self.__claveCifrada = GestorCifrado.encriptar(nueva)
        return True
