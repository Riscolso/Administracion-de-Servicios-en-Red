"""
Archivo para la clase Agente y sus funcinalidades"""
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
from Hilo import hiloActualizar

CPU = ['1.3.6.1.2.1.25.3.3.1.2.196608',
'1.3.6.1.2.1.25.3.3.1.2.196609',
'1.3.6.1.2.1.25.3.3.1.2.196610',
'1.3.6.1.2.1.25.3.3.1.2.196611'
]
        
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
            hilo1 = threading.Thread(args = (self,), target=hiloActualizar)
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
        if self.edo == 'up': #Chanzón y el agente esta caído, y pues no queremos eso
            h = threading.Thread(args = (self, opcion), target=hiloContabilizar)
            h.start()
            #Esperar hasta que el hilo termine
            h.join()
