"""Archivo para la clase Agente y sus funcinalidades"""
"""
TODO: Descomentiza todo lo del hilo 'actualizar', que no lo estás usando para esta practica xD
TODO: Aguas, checa monitorizar() creo que genera multiples hilos jajajaja
"""
import SNMPInfo as snmp
import threading 
from time import sleep
from time import time
from PDF import crearPDF
from RRDTFunct import RUTARRD
import RRDTFunct as rf
import rrdtool
from Hilo import hiloContabilizar

#Practica 3
#cambiar el nombre a TCPIN/OUT
OIDs={
    "TCPIN" : "1.3.6.1.2.1.6.10.0",
    "TCPOUT" : "1.3.6.1.2.1.6.11.0",
    "udpInDatagrams" : "1.3.6.1.2.1.7.1.0",
    "udpOutDatagrams" : "1.3.6.1.2.1.7.4.0",
    "SCTP" : "1.3.6.1.2.1.104",
    "tcpConnectionEntry" : "1.3.6.1.2.1.6.19.1",
    "tcpConnTable": "1.3.6.1.2.1.6.13.1.4",
    "udpLocalPort" : "1.3.6.1.2.1.7.5.1.2",
    "ANCHODEBANDA" : "1.3.6.1.2.1.2.2.1.5"
}

#1.3.6.1.2.1.25.2.2.0
RAMTOTAL = '8.40.1.232 1.3.6.1.2.1.25.2.3.1.5.5.0'
RAMUSA = '1.3.6.1.2.1.25.2.3.1.6.5.0'
RAMTOTALLINUX = '1.3.6.1.4.1.2021.4.5.0'
RAMLIBRELINUX = '1.3.6.1.4.1.2021.4.15.0'
RAMDISQUEUSADA = '1.3.6.1.4.1.2021.4.6.0'
DISCOUSADO = '1.3.6.1.2.1.25.2.3.1.6.36'
DISCOTOTAL = '1.3.6.1.2.1.25.2.3.1.5.36'
CPU = ['1.3.6.1.2.1.25.3.3.1.2.196608',
'1.3.6.1.2.1.25.3.3.1.2.196609',
'1.3.6.1.2.1.25.3.3.1.2.196610',
'1.3.6.1.2.1.25.3.3.1.2.196611'
]

def porcentajeRAMUsada(t:int, l:int) -> float:
    """A partir de la RAM total y la RAM libre (kb), obtiene 
    el porcentaje usado"""
    t = t/1048576 #convertir a GB
    #t = round(t, 3) 
    dif = t - (l/1048576) #Convertir a GB
    return round((dif*100)/t, 2) #Porcentaje de float con 2 decimales

def porcentaje(t:int, l:int):
    return round((l*100)/t, 2)

def temp(clase, n):
    """Luego arreglo todo esto... neta! xD"""
    carga_CPU = int(snmp.consultaSNMP(clase.comun, clase.ip, CPU[n], clase.port))
    valorcpu = "N:" + str(carga_CPU)
    #print (valorcpu)
    rrdtool.update(RUTARRD+clase.ip+ "CPU"+str(n)+".rrd", valorcpu)
    #print('LLego')
    rf.graficarCPU(clase, n)


def actualizar(clase):
    """Función que hace de hilo, encargado de obtener el valor de las tramas unicast
    Paquetes unicast que ha recibido una interfaz
    Paquetes recibidos a protocolos IPv4, incluyendo los que tienen errores.
    Mensajes ICMP echo que ha enviado el agente
    Segmentos recibidos, incluyendo los que se han recibido con errores.
    Datagramas entregados a usuarios UDP"""
    global RAMTOTAL, RAMLIBRELINUX, RAMDISQUEUSADA, DISCOUSADO, DISCOTOTAL,CPU
    try:
        while clase.ence:
            uni = int(snmp.consultaSNMP(clase.comun, clase.ip, '1.3.6.1.2.1.2.2.1.11.1', clase.port))
            ips = int(snmp.consultaSNMP(clase.comun, clase.ip, '1.3.6.1.2.1.4.3.0', clase.port))
            #Esta depreciado, pero funciona en Windows, no en Linux
            icmp = int(snmp.consultaSNMP(clase.comun, clase.ip, '1.3.6.1.2.1.5.21.0', clase.port))
            #Funciona en Linux, no en windows... De hecho ni siquiera existe xD
            #icmp = int(snmp.consultaSNMP(clase.comun, clase.ip, '1.3.6.1.2.1.5.30.1.4.1.8', clase.port))
            segs = int(snmp.consultaSNMP(clase.comun, clase.ip, '1.3.6.1.2.1.6.10.0', clase.port))
            udp = int(snmp.consultaSNMP(clase.comun, clase.ip, '1.3.6.1.2.1.7.1.0', clase.port))
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
        
class Agente():
    """Contiene información relacionada con un agrente así como métodos para conseguir la información
    SNMP a partir de una IP, versión, comunidad y puerto"""
    ip = '' #Dirección IP o host name
    snmpver = '' #Versión de SNMP
    comun = '' #Comunidad
    port = '' #Puerto
    edo = 'down' #Estado 
    cantinter = '' #Cantidad de interfaces
    dispointer = 0 #Cantidad de interfaces disponibles
    inter = {} #Diccionario de Interfaces y su disponibilidad
    so = '' #Sistema Operativo
    soVer = '' #Versión del SO
    ubicacion = '' #Ubicación
    time = '' #Tiempo desde el último reinicio
    #Tiempo que debe pasar para actualizar los datos del agente
    actu = 0 #(segs)
    ence = False #Determina si un hilo sigue enviando peticiones o nel pastel

    def __init__(self):
        self.so = ''
        self.soVer = ''
        self.ubicacion = ''
        self.time = ''
        self.edo = 'down'
        self.actu = 1
        self.ence = False
        self.dispointer = 0
        self.inter = {}
        self.cantinter = ''

    def upODown(self, num: str) -> str:
        """Cambia un número por un estado
        1 - up
        2 - down"""
        if(num == '1'):
            return 'up'
        else:
            return 'down'

    
    def obtenerEstado(self):
        """Obtiene el estado del agente mendiante SNMP... Y ya que esta de paso y para
        no malgastar recursos, el número de puertos también :P """
        #Obtener la interfaces
        self.cantinter = snmp.consultaSNMP(self.comun, self.ip, '1.3.6.1.2.1.2.1.0', self.port)
        if self.cantinter: #En caso de que el agente esté disponible
            self.edo = 'up'
            self.ence = True #Establecer que el hilo de monitoreo puede empezar a ... monitorear xD
        else: #En caso de que no esté disponible solo informa
            print('El agente con IP ' + self.ip, 'no está funcionando. (F)')
    
    def obtenerInfoInterfaces(self):
        """Le da valor a las variables dispointer e inter del agente"""
        if self.edo == 'up': #Chanzón y el agente esta caído, y pues no queremos eso
            #Obtener la disponibilidad de puertos
            for i in range(1,int(self.cantinter)+1):
                #Obtiene el nombre de la interface y la usa como clave en un diccionario
                clave = str(snmp.consultaSNMP(self.comun, self.ip, '1.3.6.1.2.1.2.2.1.2.'+str(i), self.port))
                if len(clave)>20:
                    clave = bytes.fromhex(clave[2:]).decode('utf-8')[:-4]
                #Obtiene la disponibilidad de la interface y le asigna up o down según sea el caso
                self.inter[clave] = self.upODown(snmp.consultaSNMP(
                    self.comun, self.ip, '1.3.6.1.2.1.2.2.1.8.'+str(i), self.port))
                #Verificar si está disponible o no para actualizar el contador
                if self.inter[clave] == 'up':
                    self.dispointer += 1

    def obtenerSO(self):
        """Obtiene el nombre y la versión del SO del agente por medio de SNMP"""
        aux = snmp.consultaSNMP(self.comun, self.ip, '1.3.6.1.2.1.1.1.0', self.port, True)
        if aux.find('#')!=-1: #Si es linux
            if(aux.find("Ubuntu")>0): #En caso de ser Ubuntu
                soaux = aux.split()[5]
                ''.join(soaux)
                self.so = soaux[soaux.find('-')+1:]
            else:#En caso de ser una distro de Linux no reconocida
                self.so = aux.split()[2]
            self.soVer = aux.split()[4]
        else: #Si es windows
            self.so = aux.split()[14]
            self.soVer = aux.split()[16]

    def obtenerUbicacion(self):
        """Obtiene la ubicación mediante snmp"""
        aux = snmp.consultaSNMP(self.comun, self.ip, '1.3.6.1.2.1.1.6.0', self.port, True)
        aux = aux.split('=')
        self.ubicacion = aux[-1]

    def obtenerTiempo(self):
        """Obtiene el tiempo desde el último reinicio del sistema SNMP"""
        num = snmp.consultaSNMP(self.comun, self.ip, '1.3.6.1.2.1.1.3.0', self.port)
        num = int(num)/100 # Centesimas de segundo -> segundos
        dias = num//86400
        hor = (num - (dias*86400))//3600
        minu=int((num-(hor*3600))//60)
        seg=num-((hor*3600)+(minu*60))
        self.time = str(int(dias))+ ' días '+ str(int(hor))+':'+ str(int(minu))+':'+str(int(seg))

    def monitorear(self):
        """Hilo encargado de actualizar la información del agente
        cada cierto tiempo... o eso diría si puediera serializar una clase heredada de hilo
        jajajaja, en fin, ya quedó como una función afuera xD"""
        if self.edo == 'up': #Chanzón y el agente esta caído, y pues no queremos eso
            hilo1 = threading.Thread(args = (self,), target=actualizar)
            hilo1.start()

    def crearRRDTOOL(self):
        """Crea una ammmm... 'Base de datos' de rrdtool para el monitoreo del agente"""
        #https://oss.oetiker.ch/rrdtool/doc/rrdcreate.en.html
        try:
            #Cada 50 segs va a tener un valor y s esobreescriben a los 24
            rrdtool.create(self.ip+'.rrd',
                "--start", 'N', #Inicial al momento de crear el archivo
                "--step",'3',
                "DS:unicast:COUNTER:600:U:U", #10->3 Segs para recibir datos, o si no 'Desconocido'
                "DS:ip:COUNTER:600:U:U",
                "DS:icmp:COUNTER:601:U:U",
                "DS:segs:COUNTER:602:U:U",
                "DS:udp:COUNTER:603:U:U",
                "RRA:AVERAGE:0.5:6:700", #Promedio de c/5 valores, sobreescribe cada 24
                "RRA:AVERAGE:0.5:5:700",
                "RRA:AVERAGE:0.5:5:700",
                "RRA:AVERAGE:0.5:5:700",
                "RRA:AVERAGE:0.5:5:700"
            )
        except Exception as ex:
            print('Super F al crear el rrd: ', ex)

    def crearReporte(self, t: int):
        """Crea un reporte en pdf en la carpeta de ejecución con información del
        agent"""
        #Encabezado
        #Nombre y versión del SO
        self.obtenerSO()
        #print('Ver: ', self.soVer)
        #Ubicación
        self.obtenerUbicacion()
        #print('Localización: ', self.ubicacion)
        #No. Interfaces
        #print('Interfaces: ',self.cantinter)
        #Tiempo de actividad
        self.obtenerTiempo()
        #print('Tiempo de actividad: ', self.time)
        #Comunidad
        #print('Comunidad: ', self.comun)
        #Ip
        #print('IP: ', self.ip)
        t = t*60 #Convertir a segundos
        t = time()- t #Restar los segundos ingresados al tiempo posix actual
        t = int(t)
        snmp.graficar(self.ip, t)
        crearPDF(self)
        print('Busca en la carpeta el PDF ;D ')
    
    def contabilizar(self, opcion: int, puerto: int = 0):
        """Realiza el monitoreo de tramas con base a una opción
        1.-Dirección IP 
        2.-Protocolo de transporte
        3.-Número de puerto
        En caso de ser No.Puerto, especificarlo"""
        global OIDs
        if self.edo == 'up': #Chanzón y el agente esta caído, y pues no queremos eso
            h = threading.Thread(args = (self, opcion, OIDs), target=hiloContabilizar)
            h.start()
            #Esperar hasta que el hilo termine
            h.join()
