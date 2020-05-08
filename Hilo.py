"""Clase encargada de los método que ejecutarán los hilos en bucle"""
"""
TODO: Optimizar el código del hilo de contabilizar
"""
import selectors, sys
from time import sleep
import Agente
from typing import Dict
import SNMPInfo as snmp
from Main import limpiar
import rrdtool


OIDs={
    "ifInUcastPkts" : '1.3.6.1.2.1.2.2.1.11.1',
    "ipRoutingFwdNetBroadcast" : '1.3.6.1.2.1.4.3.0',
    "icmpOutEchos": '1.3.6.1.2.1.5.21.0',
    "tcpInSegs" : '1.3.6.1.2.1.6.10.0',
    "udpInDatagrams": '1.3.6.1.2.1.7.1.0',
    "RAMTOTAL" : '8.40.1.232 1.3.6.1.2.1.25.2.3.1.5.5.0',
    "RAMLIBRELINUX" : '1.3.6.1.4.1.2021.4.15.0',
    "RAMUSA" : '1.3.6.1.2.1.25.2.3.1.6.5.0',
    "RAMTOTALLINUX" : '1.3.6.1.4.1.2021.4.5.0',
    "RAMDISQUEUSADA" : '1.3.6.1.4.1.2021.4.6.0',
    "DISCOUSADO" : '1.3.6.1.2.1.25.2.3.1.6.36',
    "DISCOTOTAL" : '1.3.6.1.2.1.25.2.3.1.5.36',
    "TCPIN" : "1.3.6.1.2.1.6.10.0",
    "TCPOUT" : "1.3.6.1.2.1.6.11.0",
    #"udpInDatagrams" : "1.3.6.1.2.1.7.1.0",
    "udpOutDatagrams" : "1.3.6.1.2.1.7.4.0",
    "SCTP" : "1.3.6.1.2.1.104",
    "tcpConnectionEntry" : "1.3.6.1.2.1.6.19.1",
    "tcpConnTable": "1.3.6.1.2.1.6.13.1.4",
    "udpLocalPort" : "1.3.6.1.2.1.7.5.1.2",
    "ANCHODEBANDA" : "1.3.6.1.2.1.2.2.1.5"
}

def timed_input(prompt="", timeout=13):
    sel = selectors.DefaultSelector()
    sel.register(sys.stdin, selectors.EVENT_READ, input)

    respuesta = None
    print(prompt, end="")
    events = sel.select(timeout=timeout)
    if events:
        respuesta = input()
    return respuesta

def hiloActualizar(clase: Agente):
    """Función que hace de hilo, encargado de obtener el valor de las tramas unicast
    Paquetes unicast que ha recibido una interfaz
    Paquetes recibidos a protocolos IPv4, incluyendo los que tienen errores.
    Mensajes ICMP echo que ha enviado el agente
    Segmentos recibidos, incluyendo los que se han recibido con errores.
    Datagramas entregados a usuarios UDP"""
    global OIDs
    try:
        while clase.ence:
            uni = int(snmp.consultaSNMP(clase.comun, clase.ip, OIDs["ifInUcastPkts"], clase.port))
            ips = int(snmp.consultaSNMP(clase.comun, clase.ip, OIDs["ipRoutingFwdNetBroadcast"], clase.port))
            #Esta depreciado, pero funciona en Windows, no en Linux
            icmp = int(snmp.consultaSNMP(clase.comun, clase.ip, OIDs["icmpOutEchos"], clase.port))
            #Funciona en Linux, no en windows... De hecho ni siquiera existe xD
            #icmp = int(snmp.consultaSNMP(clase.comun, clase.ip, '1.3.6.1.2.1.5.30.1.4.1.8', clase.port))
            segs = int(snmp.consultaSNMP(clase.comun, clase.ip, OIDs["tcpInSegs"], clase.port))
            udp = int(snmp.consultaSNMP(clase.comun, clase.ip, OIDs["udpInDatagrams"], clase.port))
            valor = "N:" + str(uni) + ':' + str(ips) + ':' + str(icmp) + ':' + str(segs) + ':' + str(udp)
            rrdtool.update(clase.ip+'.rrd', valor)
            #print('Valor:', valor)
            #rrdtool.dump(clase.ip+'.rrd',clase.ip+'.xml')
            
            #Toda la siguiente parte debe ser arreglada, por que nunca funcó para Windows jajajaja ay :'C 
            """
            #Monitorear el CPU
            # carga_CPU = int(snmp.consultaSNMP(clase.comun, clase.ip, CPU[0], clase.port))
            # valorcpu = "N:" + str(carga_CPU)
            # print (valorcpu)
            # rrdtool.update(RUTARRD+clase.ip+ "CPU"+".rrd", valorcpu)
            # rf.graficarCPU(clase)
            
            for i in range(len(CPU)):
                temp(clase, i)
            #Monitorear RAM
            
            
            TOTAL_RAM = int(snmp.consultaSNMP(clase.comun, clase.ip, RAMTOTAL, clase.port))
            RAM_usa = int(snmp.consultaSNMP(clase.comun, clase.ip, RAMUSA, clase.port))
            ram = porcentaje(TOTAL_RAM, RAM_usa)
            ram = "N:" + str(ram)
            #print (ram)
            rrdtool.update(RUTARRD+clase.ip+ "RAM"+".rrd", ram)
            rf.graficarRAM(clase)
            
            #Monitorear HDD
            #Monitorear RAM
            TOTAL_HDD = int(snmp.consultaSNMP(clase.comun, clase.ip, RAMTOTAL, clase.port))
            HDD_libre = int(snmp.consultaSNMP(clase.comun, clase.ip, RAMLIBRELINUX, clase.port))
            hdd = porcentaje(TOTAL_HDD, HDD_libre)
            hdd = "N:" + str(hdd)
            #print (hdd)
            rrdtool.update(RUTARRD+clase.ip+ "HDD"+".rrd", hdd)
            rf.graficarHDD(clase)
            
            #rrdtool.dump(RUTARRD+clase.ip+ "CPU"+".rrd",'trend.xml')
            """
            sleep(clase.actu)
    except Exception as e:
        print('El hilo del agente '+ clase.ip +' acaba de estirar la pata =(')
        print(str(e))


def hiloContabilizar(agente: Agente, opcion: int):
    """Un hilo encargado de mostrar en pantalla la contibilización de Tramas"""
    global OIDs
    if opcion == 1:
        try:
            direcciones = []
            #i=0
            op = None
            while op!='':
                limpiar()
                print("\t\t\tContabilidad de la red ")
                #i+=1
                print("\t\t\tCantidad de tramas de direcciones IP\n")
                print("Dirección IP \t\t\t\t\tCantidad de tramas actuales")
                for direccion in set(direcciones):
                    #Este if es solo para dar estílo xD
                    aux = direccion
                    if len(direccion)<10:
                        aux += '      ' 
                    print(aux+'\t\t\t\t\t'+str(direcciones.count(direccion)))
                print("\nPresiona 'Enter' para salir...")
                direcciones = snmp.snmpwalk(agente.comun, agente.ip, OIDs["tcpConnTable"], agente.port)
                op = timed_input("", timeout=0.5)
                #sleep(0.2)
        except Exception as e:
            print('El hilo de '+ agente.ip +' se nos adelantó')
            print(str(e))
    elif opcion == 2:
        try:
            entradaTCP = 0
            salidaTCP = 0
            entradaUDP = 0
            salidaUDP = 0
            entradasSCTP = 0
            salidaSCTP = 0
            #i=0
            op = None
            while op!='':
                limpiar()
                print("\t\t\tContabilidad de la red ")
                #i+=1
                print("\tProtocolo de transporte- Cantidad de Tramas hasta el momento\n")
                
                print("Tramas TCP")
                print("\tEntrada\t\t\t\t\t" 
                    +str(entradaTCP))
                print("\tSalida\t\t\t\t\t"
                    +str(salidaTCP))
                print("Tramas UDP")
                print("\tEntrada\t\t\t\t\t" 
                    +str(entradaUDP))
                print("\tSalida\t\t\t\t\t"
                    +str(salidaUDP))
                print("Tramas SCTP")
                print("\tEntrada\t\t\t\t\t" 
                    +str(entradasSCTP))
                print("\tSalida\t\t\t\t\t"
                    +str(salidaSCTP))
                print("\nPresiona 'Enter' para salir...")
                entradaTCP = snmp.consultaSNMP(agente.comun, agente.ip, OIDs["TCPIN"], agente.port)
                salidaTCP = snmp.consultaSNMP(agente.comun, agente.ip, OIDs["TCPOUT"], agente.port)
                entradaUDP = snmp.consultaSNMP(agente.comun, agente.ip, OIDs["udpInDatagrams"], agente.port)
                salidaUDP = snmp.consultaSNMP(agente.comun, agente.ip, OIDs["udpOutDatagrams"], agente.port)
                #En un agente puede no haber tramas SCTP
                if snmp.snmpwalk(agente.comun, agente.ip, OIDs["SCTP"], agente.port) == []:
                    salidaSCTP = "N/A"
                    entradasSCTP = "N/A"
                op = timed_input("", timeout=0.4)
                #sleep(0.2)
        except Exception as e:
            print('El hilo de '+ agente.ip +' se nos adelantó')
            print(str(e))

    else: 
        try:
            puertos = []
            #i=0
            op = None
            while op!='':
                limpiar()
                print("\t\t\tContabilidad de la red ")
                #i+=1
                print("\t\t\tNúmeros de puertos\n")
                print("Número de puerto \t\t\tCantidad de comunicaciones actuales hacia el puerto")
                for puerto in set(puertos):
                    #Este if es solo para dar estílo xD
                    print(puerto+'\t\t\t\t\t'+str(puertos.count(puerto)))
                print("\nPresiona 'Enter' para salir...")
                puertos = snmp.snmpwalk(agente.comun, agente.ip, OIDs["udpLocalPort"], agente.port)
                op = timed_input("", timeout=0.5)
                #sleep(0.2)
        except Exception as e:
            print('El hilo de '+ agente.ip +' se nos adelantó')
            print(str(e))


# def porcentajeRAMUsada(t:int, l:int) -> float:
#     """A partir de la RAM total y la RAM libre (kb), obtiene 
#     el porcentaje usado"""
#     t = t/1048576 #convertir a GB
#     #t = round(t, 3) 
#     dif = t - (l/1048576) #Convertir a GB
#     return round((dif*100)/t, 2) #Porcentaje de float con 2 decimales

# def porcentaje(t:int, l:int):
#     return round((l*100)/t, 2)

# def temp(clase, n):
#     """Luego arreglo todo esto... neta! xD"""
#     carga_CPU = int(snmp.consultaSNMP(clase.comun, clase.ip, CPU[n], clase.port))
#     valorcpu = "N:" + str(carga_CPU)
#     #print (valorcpu)
#     rrdtool.update(RUTARRD+clase.ip+ "CPU"+str(n)+".rrd", valorcpu)
#     #print('LLego')
#     rf.graficarCPU(clase, n)

