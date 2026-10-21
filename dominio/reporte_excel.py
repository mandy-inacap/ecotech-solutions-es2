from dominio.reporte import Reporte


class ReporteExcel(Reporte):
    def exportar(self, contenido):
        # Esqueleto: texto tabulado que Excel puede abrir. Un .xlsx real queda como mejora futura.
        return contenido.replace("  - ", "\t").encode("utf-8")
