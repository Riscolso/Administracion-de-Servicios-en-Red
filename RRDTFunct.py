#!Python3
"""Clase encargada de todo lo relacionado con RRDTOOL
...
O eso se supone, a menos que haya funciones en otros scrips que se me
hayan olvidado mudar aquí
TODO: Generalizar la función crearBDRRD
"""

import rrdtool
import Agente
import sys
import rrdtool
from Notify import send_alert_attached
import time

#Ruta en donde se guardan y se buscan los RRD del proyecto
RUTARRD = 'RRDs/'
RUTAGRA = 'Graficas/'

#Pa' evitar que se envien muchos mensajes :V
ENVIO = True


def crearBDRRDCPU(agente: Agente):
    """Crea un Base de datos de RRDTOOL para un agente proporcionado"""
    try:
        rrdtool.create(RUTARRD+agente.ip+ "CPU"+".rrd",
                            "--start",'N',
                            "--step",'60',
                            "DS:CPUload:GAUGE:600:U:U",
                            #"DS:RAMload:GAUGE:601:U:U",
                            "RRA:AVERAGE:0.5:1:24",
                            #"RRA:AVERAGE:0.5:1:24")
    except Exception as e:
        print('Error al crear la BD RRDTool: ' + str(e))
        return None



def graficar(agente: Agente):
    """Gráfica una BD de RRDTOOL
    Usa la calse de Email para enviar un correo
    en caso de pasar un umbral"""
    global ENVIO
    ultima_lectura = int(rrdtool.last(RUTARRD+agente.ip+"CPU.rrd"))
    tiempo_final = ultima_lectura
    tiempo_inicial = tiempo_final - 600
    #Umbral superior de CPU
    UMBRALCPU = 25

    ret = rrdtool.graphv( RUTAGRA+"deteccion.png",
                     "--start",str(tiempo_inicial),
                     "--end",str(tiempo_final),
                     "--vertical-label=Cpu load",
                    '--lower-limit', '0',
                    '--upper-limit', '100',
                     "DEF:cargaCPU="+RUTARRD+"localhostCPU.rrd:CPUload:AVERAGE",

                     "CDEF:umbral=cargaCPU,"+str(UMBRALCPU)+",LT,0,cargaCPU,IF",
                     "VDEF:cargaMAX=cargaCPU,MAXIMUM",
                     "VDEF:cargaMIN=cargaCPU,MINIMUM",
                     "VDEF:cargaSTDEV=cargaCPU,STDEV",
                     "VDEF:cargaLAST=cargaCPU,LAST",
                     "AREA:cargaCPU#00FF00:Carga del CPU",
                     "AREA:umbral#FF9F00:Carga CPU mayor que "+str(UMBRALCPU),
                     "HRULE:25#FF0000:Umbral - Oh, no",
                     "PRINT:cargaLAST:%6.2lf",
                     "GPRINT:cargaMIN:%6.2lf %SMIN",
                     "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                     "GPRINT:cargaLAST:%6.2lf %SLAST" )
    #Obtener el último valor de la gráfica.                
    ultimo_valor=float(ret['print[0]'])
    print('Último valor '+ str(ultimo_valor))
    if (ultimo_valor>UMBRALCPU and ENVIO):
        print('El agente '+agente.ip+' se está quemando, corre!!! D=')
        ENVIO = False
        send_alert_attached("Sobrepasa Umbral línea base")