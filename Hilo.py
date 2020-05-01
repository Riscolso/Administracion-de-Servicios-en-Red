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

def timed_input(prompt="", timeout=13):
    sel = selectors.DefaultSelector()
    sel.register(sys.stdin, selectors.EVENT_READ, input)

    respuesta = None
    print(prompt, end="")
    events = sel.select(timeout=timeout)
    if events:
        respuesta = input()
    return respuesta


def hiloContabilizar(agente: Agente, opcion: int, OIDs: Dict[str, str]):
    """Un hilo encargado de mostrar en pantalla la contibilización de Tramas"""
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
                direcciones = []
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
        print('Opción 3')