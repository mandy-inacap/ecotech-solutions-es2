from datetime import date


class ParticipacionProyecto:
    """Clase de asociación Empleado 1..* – 0..* Proyecto (con fecha de incorporación y vigencia)."""

    def __init__(self, empleado, proyecto, fechaIncorporacion=None):
        self.empleado = empleado
        self.proyecto = proyecto
        self.fechaIncorporacion = fechaIncorporacion or date.today()
        self.__enCurso = True                      # -enCurso : bool
        proyecto._agregar_participacion(self)

    @property
    def enCurso(self):
        return self.__enCurso

    def cerrarParticipacion(self):
        self.__enCurso = False
