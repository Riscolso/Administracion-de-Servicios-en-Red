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
ENVIO = [True, True, True]




def crearBDRRD(agente: Agente, tipo:str):
    """Crea un Base de datos de RRDTOOL para un agente proporcionado"""
    try:
        rrdtool.create(RUTARRD+agente.ip+tipo+".rrd",
                            "--start",'N',
                            "--step",'60',
                            "DS:"+tipo+"load:GAUGE:600:U:U",
                            #"DS:RAMload:GAUGE:601:U:U",
                            #"RRA:AVERAGE:0.5:1:24",
                            "RRA:AVERAGE:0.5:1:24"
                            )
    except Exception as e:
        print('Error al crear la BD RRDTool: ' + str(e))
        return None



def graficarCPU(agente: Agente):
    """Gráfica una BD de RRDTOOL
    Usa la calse de Email para enviar un correo
    en caso de pasar un umbral"""
    global ENVIO
    UMBRALCPUMED = 9
    UMBRALCPU = 10
    ultima_lectura = int(rrdtool.last(RUTARRD+agente.ip+"CPU.rrd"))
    tiempo_final = ultima_lectura
    tiempo_inicial = tiempo_final - 600
    try:
        ret = rrdtool.graphv( RUTAGRA+"CPU.png",
                        "--start",str(tiempo_inicial),
                        "--end",str(tiempo_final),
                        "--vertical-label=Cpu load",
                        '--lower-limit', '0',
                        '--upper-limit', '100',
                        "DEF:cargaCPU="+RUTARRD+agente.ip+"CPU.rrd:CPUload:AVERAGE",

                        "CDEF:umbral1=cargaCPU,"+str(UMBRALCPU)+",LT,0,cargaCPU,IF",
                        "CDEF:umbral=cargaCPU,"+str(UMBRALCPUMED)+",LT,0,cargaCPU,IF",
                        
                        
                        "VDEF:cargaMAX=cargaCPU,MAXIMUM",
                        "VDEF:cargaMIN=cargaCPU,MINIMUM",
                        "VDEF:cargaSTDEV=cargaCPU,STDEV",
                        "VDEF:cargaLAST=cargaCPU,LAST",
                        "AREA:cargaCPU#00FF00:Carga Normal del CPU",

                        
                        "AREA:umbral#FF9F00:Carga CPU mayor que "+str(UMBRALCPUMED),
                        "AREA:umbral1#FF0000:Carga CPU mayor que "+str(UMBRALCPU),

                        "HRULE:"+str(UMBRALCPU)+"#FF0000:Umbral - Oh, no "+str(UMBRALCPU),
                        "PRINT:cargaLAST:%6.2lf",
                        "GPRINT:cargaMIN:%6.2lf %SMIN",
                        "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                        "GPRINT:cargaLAST:%6.2lf %SLAST" )
        #Obtener el último valor de la gráfica.                
        ultimo_valor=float(ret['print[0]'])
        #print('Último valor '+ str(ultimo_valor))
        if (ultimo_valor>UMBRALCPU and ENVIO[0]):
            print('El CPU del agente '+agente.ip+' se está quemando, corre!!! D=')
            ENVIO[0] = False
            #send_alert_attached("Sobrepasa Umbral línea base CPU", "CPU.png")
    except Exception as e:
        print('Error al momento de graficar CPU: '+ str(e))

def graficarRAM(agente: Agente):
    """Gráfica una BD de RRDTOOL
    Usa la calse de Email para enviar un correo
    en caso de pasar un umbral"""
    global ENVIO
    UMBRAL_RAM = 10
    UMBRAL_RAMMED = 9
    ultima_lectura = int(rrdtool.last(RUTARRD+agente.ip+"RAM.rrd"))
    tiempo_final = ultima_lectura
    tiempo_inicial = tiempo_final - 600
    try:
        ret = rrdtool.graphv( RUTAGRA+"RAM.png",
                        "--start",str(tiempo_inicial),
                        "--end",str(tiempo_final),
                        "--vertical-label=RAM load",
                        '--lower-limit', '0',
                        '--upper-limit', '100',
                        "DEF:carga="+RUTARRD+agente.ip+"RAM.rrd:RAMload:AVERAGE",

                        "CDEF:umbral1=carga,"+str(UMBRAL_RAM)+",LT,0,carga,IF",
                        "CDEF:umbral=carga,"+str(UMBRAL_RAMMED)+",LT,0,carga,IF",


                        "VDEF:cargaMAX=carga,MAXIMUM",
                        "VDEF:cargaMIN=carga,MINIMUM",
                        "VDEF:cargaSTDEV=carga,STDEV",
                        "VDEF:cargaLAST=carga,LAST",
                        "AREA:carga#00FF00:Carga de la RAM",
                        "AREA:umbral#FF9F00:Carga RAM mayor que "+str(UMBRAL_RAM),

                        "AREA:umbral#FF9F00:Carga RAM mayor que "+str(UMBRAL_RAMMED),
                        "AREA:umbral1#FF0000:Carga RAM mayor que "+str(UMBRAL_RAM),

                        "HRULE:"+str(UMBRAL_RAM)+"#FF0000:Umbral - Oh, no "+str(UMBRAL_RAM),
                        "PRINT:cargaLAST:%6.2lf",
                        "GPRINT:cargaMIN:%6.2lf %SMIN",
                        #"GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                        "GPRINT:cargaLAST:%6.2lf %SLAST" )
        #Obtener el último valor de la gráfica.                
        ultimo_valor=float(ret['print[0]'])
        #print('Último valor '+ str(ultimo_valor))
        if (ultimo_valor>UMBRAL_RAM and ENVIO[1]):
            print('La RAM del agente '+agente.ip+' se está quemando, corre!!! D=')
            ENVIO[1] = False
            #send_alert_attached("Sobrepasa Umbral línea base RAM", "RAM.png")
    except Exception as e:
        print('Error al momento de graficar RAM: '+ str(e))

def graficarHDD(agente: Agente):
    """Gráfica una BD de RRDTOOL
    Usa la calse de Email para enviar un correo
    en caso de pasar un umbral"""
    global ENVIO
    UMBRAL_HDD = 10
    UMBRAL_HDDMED = 9
    ultima_lectura = int(rrdtool.last(RUTARRD+agente.ip+"HDD.rrd"))
    tiempo_final = ultima_lectura
    tiempo_inicial = tiempo_final - 600
    try:
        ret = rrdtool.graphv( RUTAGRA+"HDD.png",
                        "--start",str(tiempo_inicial),
                        "--end",str(tiempo_final),
                        "--vertical-label=HDD load",
                        '--lower-limit', '0',
                        '--upper-limit', '100',
                        "DEF:carga="+RUTARRD+agente.ip+"HDD.rrd:HDDload:AVERAGE",

                        "CDEF:umbral1=carga,"+str(UMBRAL_HDD)+",LT,0,carga,IF",
                        "CDEF:umbral=carga,"+str(UMBRAL_HDDMED)+",LT,0,carga,IF",


                        "VDEF:cargaMAX=carga,MAXIMUM",
                        "VDEF:cargaMIN=carga,MINIMUM",
                        "VDEF:cargaSTDEV=carga,STDEV",
                        "VDEF:cargaLAST=carga,LAST",
                        "AREA:carga#00FF00:Carga de la HDD",
                        "AREA:umbral#FF9F00:Carga HDD mayor que "+str(UMBRAL_HDD),

                        "AREA:umbral#FF9F00:Carga HDD mayor que "+str(UMBRAL_HDDMED),
                        "AREA:umbral1#FF0000:Carga HDD mayor que "+str(UMBRAL_HDD),

                        "HRULE:"+str(UMBRAL_HDD)+"#FF0000:Umbral - Oh, no "+str(UMBRAL_HDD),
                        "PRINT:cargaLAST:%6.2lf",
                        "GPRINT:cargaMIN:%6.2lf %SMIN",
                        #"GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                        "GPRINT:cargaLAST:%6.2lf %SLAST" )
        #Obtener el último valor de la gráfica.                
        ultimo_valor=float(ret['print[0]'])
        #print('Último valor '+ str(ultimo_valor))
        if (ultimo_valor>UMBRAL_HDD and ENVIO[2]):
            print('El HDD del agente '+agente.ip+' se está quemando, corre!!! D=')
            ENVIO[2] = False
            #send_alert_attached("Sobrepasa Umbral línea base HDD", "HDD.png")
    except Exception as e:
        print('Error al momento de graficar HDD: '+ str(e))