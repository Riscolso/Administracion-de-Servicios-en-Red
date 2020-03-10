from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import Agente
def crearPDF(agente: Agente):
    """Recibe una clase de tipo agente y genera un reporte pdf con la
    información de esta"""
    try:
        c = canvas.Canvas("Reporte - "+agente.ip)
        text = c.beginText(240, 820)
        text.setFont("Helvetica-Bold", 15)
        text.textLine("Reporte de agente")
        c.drawImage("img/"+agente.so+".jpg", 450, 710, width=75, height=75)

        text.setTextOrigin(20, 789)
        text.setFont('Times-Roman', 12)
        text.textLine('Sistema operativo: '+agente.so+'        Versión: '+agente.soVer)
        text.textLine('Ubicación: ' +agente.ubicacion)
        text.textLine('Número de Interfaces: '+ agente.cantinter)
        text.textLine('Tiempo de actividad: '+ agente.time)
        text.textLine('Comunidad: '+agente.comun)
        text.textLine('host : '+agente.ip)
        c.line(0, 800, 595, 800)
        tamx = 250
        tamy = 100
        b = 100
        c.drawImage(agente.ip+"0.png", 20, 600-b, width=tamx, height=tamy)
        c.drawImage(agente.ip+"1.png", 300, 600-b, width=tamx, height=tamy)
        c.drawImage(agente.ip+"2.png", 20, 470-b, width=tamx, height=tamy)
        c.drawImage(agente.ip+"3.png", 300, 470-b, width=tamx, height=tamy)
        c.drawImage(agente.ip+"4.png", 20, 340-b, width=tamx, height=tamy)

        c.drawText(text)
        c.save()
    except Exception as e:
        print('Error al crear el PDF: '+ e)