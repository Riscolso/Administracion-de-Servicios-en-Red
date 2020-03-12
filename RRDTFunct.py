#!Python3
"""Clase encargada de todo lo relacionado con RRDTOOL
...
O eso se supone, a menos que haya funciones en otros scrips que se me
hayan olvidado mudar aquí
TODO: Generalizar la función crearBDRRD
"""

import rrdtool
import Agente

#Ruta en donde se guardan y se buscan los RRD del proyecto
RUTARRD = 'RRDs/'


def crearBDRRDCPU(agente: Agente):
    """Crea un Base de datos de RRDTOOL para un agente proporcionado"""
    try:
        rrdtool.create(RUTARRD+agente.ip+ "CPU"+".rrd",
                            "--start",'N',
                            "--step",'60',
                            "DS:CPUload:GAUGE:600:U:U",
                            "RRA:AVERAGE:0.5:1:24")
    except Exception as e:
        print('Error al crear la BD RRDTool: ' + str(e))
        return None