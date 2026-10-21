from dominio.validaciones import entero_positivo, fecha_valida, texto_no_vacio


class Proyecto:
    """Recibe ParticipacionProyecto y consume ParteDiario (composición: sin proyecto no hay parte)."""

    def __init__(self, codigoProyecto, tituloProyecto, resumen, fechaLanzamiento):
        self.__codigoProyecto = entero_positivo(codigoProyecto, "El código del proyecto")
        self.tituloProyecto = texto_no_vacio(tituloProyecto, "El título del proyecto")
        self.resumen = resumen or ""
        self.fechaLanzamiento = fecha_valida(fechaLanzamiento, "La fecha de lanzamiento")
        self.__participaciones = []
        self.__partes = []

    @property
    def codigoProyecto(self):
        return self.__codigoProyecto

    @property
    def participaciones(self):
        return tuple(self.__participaciones)

    @property
    def partes(self):
        return tuple(self.__partes)

    def _agregar_participacion(self, participacion):
        self.__participaciones.append(participacion)

    def _agregar_parte(self, parte):
        self.__partes.append(parte)

    def totalHorasInvertidas(self):
        return sum(p.horasImputadas for p in self.__partes)
