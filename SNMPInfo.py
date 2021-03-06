#!Python3
"""Clase encargada de todo lo relacionado con SNMP
TODO: Estilizar el manejo de errores de consultaSNMP"""
from pysnmp.hlapi import *
from typing import List, Generic, Dict, Any
import rrdtool


def consultaSNMP(comunidad,host,oid, port:int, raw:bool=False) -> str:
    """Hace una consulta SNMP a un agente de la misma red
    En caso de hacer un error, lo imprime y regresa un False
    Si la badera raw está activada, regresa el texto completo sin procesar"""
    try:
        resultado = False
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                CommunityData(comunidad),
                UdpTransportTarget((host, port)),
                ContextData(),
                ObjectType(ObjectIdentity(oid))))

        if errorIndication:
            #print(errorIndication)
            return ''
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            return ''
        else:
            for varBind in varBinds:
                varB=(' = '.join([x.prettyPrint() for x in varBind]))
                resultado = varB
                if not raw:
                    resultado = resultado.split()[2]
        return resultado
    except:
        #print('F')
        return '' #Para cuando hay error

def snmpwalk(comunidad,host,oid, port:int, raw:bool=False):
    try:
        valor = []
        for (errorIndication,
            errorStatus,
            errorIndex,
            varBinds) in nextCmd(SnmpEngine(), 
                                CommunityData(comunidad),
                                UdpTransportTarget((host, 161)),
                                ContextData(),                                                           
                                ObjectType(ObjectIdentity(oid)),
                                lexicographicMode=False):
            if errorIndication:
                print(errorIndication)
                break
            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
                break
            else:
                for varBind in varBinds:
                    aux = ' = '.join([x.prettyPrint() for x in varBind])
                    #print(aux)
                    if raw:
                        valor+=[aux]
                    else:
                        valor += [aux.split(' ')[-1]]
        return valor
    except Exception as ex:
        print('Error en SNMPWalk', ex)
        return None

    
def graficar(host: str, t:int):
    """Tengo sueño, send hep (esto no es un meme)"""
    try:
        i=0
        for op in ['unicast', 'ip', 'icmp', 'segs', 'udp']:
            rrdtool.graph(host+str(i)+".png",
                            "--start",str(t),
                            "--end","N",
                            "--vertical-label="+op,
                            "DEF:"+op+"="+host+".rrd:"+op+":AVERAGE",
                            "AREA:"+op+"#00FF00:Tramas "+op)
            i+=1
    except Exception as e:
        print('Super EFE ', e)

OIDWALK = '1.3.6.1.2.1.1'
OID = "1.3.6.1.2.1.1.1.0"


#Sección de pruebas rápidas ;D
#aux = snmpwalk('grupo4cv5', 'localhost', OIDWALK, '161')
#print(aux)
#if aux is not None:
#    print(aux)

# aux = consultaSNMP('grupo4cv5', '192.168.0.1', OID, 161, True)
# print('Valor: ', aux)
# aux = aux.split()[2]
# print('Valor: ', aux)