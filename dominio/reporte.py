from abc import ABC, abstractmethod
from datetime import date


class Reporte(ABC):
    """«abstract» Reporte. Usa (dependencia) Departamento, Empleado, Proyecto y Credencial."""

    def __init__(self, categoria="general"):
        self._fechaEmision = date.today()    # #fechaEmision : date
        self.categoria = categoria

    def construir(self, departamentos=(), proyectos=(), credenciales=()):
        lineas = [f"Reporte {self.categoria} - {self._fechaEmision}"]
        for d in departamentos:
            lineas.append(f"Departamento {d.nombreDepto}: {len(d.nomina())} empleado(s)")
            lineas += [f"  - {e.nombreCompleto} ({e.antiguedadEnAnios()} años)" for e in d.nomina()]
        for p in proyectos:
            lineas.append(f"Proyecto {p.tituloProyecto}: {p.totalHorasInvertidas()} horas")
        for c in credenciales:
            lineas.append(f"Credencial {c.nombreUsuario} ({'habilitada' if c.habilitada else 'deshabilitada'})")
        return "\n".join(lineas)

    @abstractmethod
    def exportar(self, contenido):
        """Devuelve el reporte como bytes; cada subclase define su formato (polimorfismo)."""
