"""Clase encargada de los método que ejecutarán los hilos en bucle"""
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
        print('Opción 1')
    elif opcion == 2:
        try:
            entrada = 0
            salida = 0
            #i=0
            op = None
            while op!='':
                limpiar()
                print("\t\t\tContabilidad de la red ")
                #i+=1
                print("\t\t\tProtocolo de transporte")
                print("Presiona 'Enter' para salir...")
                print("Tramas TCP")
                print("\tEntrada\t\t\t\t\t" 
                    +str(entrada))
                print("\tSalida\t\t\t\t\t"
                    +str(salida))
                op = timed_input("", timeout=0.4)
                entrada = snmp.consultaSNMP(agente.comun, agente.ip, OIDs["TCPIN"], agente.port)
                salida = snmp.consultaSNMP(agente.comun, agente.ip, OIDs["TCPOUT"], agente.port)
                #sleep(0.5)
        except Exception as e:
            print('El hilo de '+ agente.ip +' se nos adelantó')
            print(str(e))

    else: 
        print('Opción 3')