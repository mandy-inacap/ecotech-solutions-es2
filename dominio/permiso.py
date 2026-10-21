from dominio.validaciones import texto_no_vacio


class Permiso:
    def __init__(self, etiqueta, areaModulo):
        self.etiqueta = texto_no_vacio(etiqueta, "La etiqueta del permiso")
        self.areaModulo = texto_no_vacio(areaModulo, "El área o módulo")
