from dominio.reporte import Reporte


class ReportePDF(Reporte):
    def exportar(self, contenido):
        # Esqueleto: encabezado PDF + texto. Una librería de PDF real queda como mejora futura.
        return b"%PDF-1.4\n% " + contenido.encode("utf-8") + b"\n%%EOF"
