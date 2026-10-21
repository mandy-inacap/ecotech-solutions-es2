from dominio.validaciones import texto_no_vacio


class Perfil:
    """Perfil agrupa 1..* Permisos (composición: los permisos viven dentro del perfil)."""

    def __init__(self, etiqueta):
        self.etiqueta = texto_no_vacio(etiqueta, "La etiqueta del perfil")
        self.__permisos = []

    @property
    def permisos(self):
        return tuple(self.__permisos)

    def incluirPermiso(self, p):
        if p in self.__permisos:
            return False
        self.__permisos.append(p)
        return True
