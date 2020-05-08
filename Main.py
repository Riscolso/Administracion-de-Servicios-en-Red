#!Python3
"""
Práctica de Administración de Servicios en Red
TODO: Volver la variable de contraseña, privada xD
TODO: Cambiar color a las gráficas xD
TODO: Usar variables CPU RAM Y HDD en la clase Agente
TODO: Organizar los archivos en carpetas
TODO: Mover las funciones de RRDTOOL al archivo RRDFunct
TODO: Manejo de excepciones.... O usar None
TODO: Borrar imagenes
TODO: Validaciones(Versión SNMP)
TODO: Monitorizar si el agente está ON u OFF y modificar su variable dinámicamente
TODO: Qué hacer si un agente se caé a media moniterización?
TODO: Usar inyección de dependencias para organizar el código, que se está volviendo muy desorganizado xD
TODO: Agregar opción de eliminar todos los agentes.
"""
from typing import List, Generic, Dict, Any
import Agente
from RRDTFunct import crearBDRRD
from time import sleep
import threading
import os
import Protocolos

#Lista de agentes que se monitorean
agentes = []


def limpiar():
    """Limpia la consola, Windows/Linux"""
    if os.name == "posix": #Linux
       os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos": #Windows
       os.system ("cls")

def salvarEstructura(est: Generic, nom: str) -> Any:
    """Salva una estructura en un archivo plk"""
    from pickle import dump
    n = nom+'.plk'
    output = open(n, 'wb')
    dump(est, output, -1)
    output.close()
    
def cargarEstructura(fname):
    """Carga una estrutura a partir de una archivo plk"""
    from pickle import load
    n = fname+'.plk'
    f = open(n, 'rb')
    est = load(f)
    f.close()
    return est

def resumen():
    """Muestra un resumen de la monitarización"""
    print('Número de agentes: ',  len(agentes))
    i = 0
    for agente in agentes:
        agente.obtenerInfoInterfaces()
        print('Agente ', i)
        print('\tIP: ', agente.ip)
        print('\tEstado: ', agente.edo)
        print('\tInterfaces Disponibles: ', agente.dispointer)
        print('\tDisponibilidad de interfaces: ', agente.inter)
        print('\n')
        i+=1
    
def agregar():
    """Agrega un agente al monitoreo"""
    limpiar()
    print('\t\tAgregar dispositivo')
    age = Agente.Agente()
    print('Inserte el nombre del host o dirección IP: ')
    age.ip = input()
    print('Inserte la versión de SNMP; 1 o 2: ')
    age.snmpver = input()
    print('Inserte el nombre de la comunidad: ')
    age.comun = input()
    print('Inserte el número de puerto: ')
    age.port = input()
    #Crear rrd para empezar a monitorear
    age.crearRRDTOOL()
    #BD para los CPU
    """
    crearBDRRD(age, 'CPU0')
    #BD para los CPU
    crearBDRRD(age, 'CPU1')
    #BD para los CPU
    crearBDRRD(age, 'CPU2')
    #BD para los CPU
    crearBDRRD(age, 'CPU3')

    #BD para la RAM
    crearBDRRD(age, 'RAM')
    #BD para la HDD
    crearBDRRD(age, 'HDD')
    """
    #Registrar agente
    agentes.append(age)
    #Persistencia
    salvarEstructura(agentes, 'agentes')

def eliminar(indi: int):
    """Elimina un elemento de la lista de agentes dado un índice"""
    from os import remove
    global agentes
    print('Seguro? s/n')
    o = input()
    if (o =='s' or o == 'S'):
        #Apagar el hilo de monitoreo
        agentes[indi].ence = False
        sleep(agentes[indi].actu) #para que le le tiempo al hilo a detenerse... Ya sé que es medio ñero apagarlo así
        #Pero es la solución más rápida sin hacer tanta cosa de sincronización
        #Borar los archivos relacionados con el agente
        try:
            remove(agentes[indi].ip+".rrd")
            remove(agentes[indi].ip+".xml")
        except Exception as ex:
            print("Error con los archivos rrd y/o xml", ex)
        #En caso de que sea el último agente... F
        if len(agentes) == 1:
            agentes = []
            try:
                remove('agentes.plk')
            except Exception as ex:
                print("El archivo de agentes ya había sido eliminado antes", ex)
        else: 
            agentes.pop(indi)
            salvarEstructura(agentes, 'agentes')

def mostrarAgentes(n:str='Agentes'):
    """Muestra los agentes almacenados"""
    print("\t"+n+" Disponibles\n")
    i=0
    for a in agentes:
        print(str(i)+".-"+a.ip)
        i+=1
    print("")

def menuMonitorear():
    """Muestra menú de monitoreo así como ejecuta la opción ingresada"""
    print('Seleccione el agente que desea monitorear: ')
    ag = input()
    print('¿Por cuál tipo de atributo quiere monitorear?')
    print('1.-Dirección IP\
        2.-Protocolo de Transporte TCP/UDP/SCPT\
            3.-Número de puerto')
    op = input()
    agentes[int(ag)].contabilizar(int(op))

def menuRouters():
    ag = input('Seleccione el Router: ')
    print("1.-Generar el archivo de configuracion del router\
                \n2.-Extraer el archivo de configuración del router\
                \n3.-Mandar archivo de configuración al router")
    op = input("Router: ")
    if(op == '1'):
        pass
    elif(op == '2'):
        usu = input("Usuario: ")
        contra = input("Contraseña: ")
        Protocolos.obtenerArchivoConfig(agentes[ag].ip, usu, contra)
    elif(op == '3'):
        pass
    else:
        print('Seleccione una opción válida')


if __name__ == '__main__':
    agentes = []
    try:
        agentes = cargarEstructura('agentes')
    except FileNotFoundError:
        print('\nNo existen agentes aún\n')
    while(True):
        print('\n\t\t\tInformación SNMP\n')
        if agentes == []:
            print('No hay agentes en la lista ')
        else:
            #Checar que los agentes funcionen y empezarlos a monitorizar, sí que sí.
            for agente in agentes:
                agente.obtenerEstado()
                agente.monitorear()
        print('1.-Agregar Dispositivo\
            \n2.-Eliminar Dispositivo\
            \n3.-Resumen\
            \n4.-Reportes\
            \n5.-Contabilidad de Red\
            \n6.-Opciones para Routers\
            \n7.-Salir\n')
        op = input("Opción: ")
        if(op == '1'):
            agregar()
        elif(op == '2'):
            print('Ingresa el número del agente que quieres fusilar')
            mostrarAgentes()
            eliminar(int(input()))
        elif(op == '3'):
            resumen()
            input()
        elif(op == '4'):
            limpiar()
            mostrarAgentes()
            print('Ingresa el número del agente que quieres un reporte :)')
            ag = input()
            print('Número de minutos hacia atrás a partir de ahora?:')
            agentes[int(ag)].crearReporte(int(input()))
            input()
        elif(op == '5'):
            limpiar()
            mostrarAgentes()
            menuMonitorear()
        elif(op == '6'):
            limpiar()
            mostrarAgentes('Routers')
            menuRouters()
        elif(op == '7'):
            print('Cerrando conexiones...')
            #Aplicando la Ñera por que no hay método para matar hilos eggsDe
            for agente in agentes:
                agente.ence = False
            exit()
        limpiar()