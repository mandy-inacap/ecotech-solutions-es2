from dominio.excepciones import DatoInvalidoError


class ParteDiario:
    """Jornada registrada por un Empleado en un Proyecto (composición con Proyecto)."""

    def __init__(self, folio, empleado, proyecto, jornada, horasImputadas, detalleActividad=""):
        self.__folio = folio                       # -folio : int
        self.empleado = empleado
        self.proyecto = proyecto
        self.jornada = jornada
        self.horasImputadas = horasImputadas
        self.detalleActividad = detalleActividad
        if not self.esJornadaValida():             # validación antes de guardarse
            raise DatoInvalidoError("Las horas imputadas deben estar entre 0 y 24.")
        proyecto._agregar_parte(self)

    @property
    def folio(self):
        return self.__folio

    def esJornadaValida(self):
        return isinstance(self.horasImputadas, (int, float)) and 0 < self.horasImputadas <= 24
