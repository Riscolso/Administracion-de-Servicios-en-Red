"""
Script encargado de todas las funciones relacionadas con protocolos
de red, como FTP y TELNET
"""
from typing import List


def obtenerArchivoConfig(host: str, usuario: str, contra: str, nombreArchivo:str=''):
    """Cliente FTP. Se conecta a un host y obtiene su archivo de configuración
    'startup-config'
    Se crea un archivo, que se guarda en 'Archivos de configuracion'
    """
    try:
        import ftplib
        ftp = ftplib.FTP(host)
        ftp.login(usuario, contra)
        #ftp.retrlines('LIST') #Para mostrar los archivos
        archivo = ''
        if nombreArchivo!='':
            archivo = nombreArchivo
        else:
            archivo = 'startup-config ' + host
        ftp.retrbinary('RETR startup-config', open('./Archivos de configuracion/'+archivo, 'wb').write)
        print("Archivo recibido, checa la carpeta 'Archivos de configuracion' =D")
        ftp.quit()
    except Exception as ex:
        print('Se produjo un error al obtener el archivo de configuración\
            desde el servidor FTP')
        print(ex)

def subirArchivoConfig(host: str, usuario: str, contra: str, nombreArchivo:str=''):
    """Cliente FTP. Se conecta a un host y envía un archivo de configuración"""
    try:
        import ftplib
        #Conectar con el host
        ftp = ftplib.FTP(host)
        #Ingresar
        ftp.login(usuario, contra)
        #ftp.retrlines('LIST') #Para mostrar los archivos
        archivo = './Archivos de configuracion/'
        #En caso de que el arvhio tenga nombre diferente
        if nombreArchivo!='':
            archivo += nombreArchivo
        else:
            archivo += 'startup-config ' + host
        #Abrir el archivo a enviar
        archivoBIN = open(archivo, 'rb')
        #print(archivoBIN.readlines())
        ftp.storbinary('STOR startup-config', archivoBIN)
        print("Archivo enviado =)")
        ftp.quit()
    except Exception as ex:
        print('Se produjo un error al enviar el archivo de configuraciónhacia el servidor FTP')
        print(ex)

def ejecutarComandoTelnet(host: str, usuario: str, contra: str, comandos: List[str], mostrarConsola: str= False):
    """Cliente TELNET. se conectar a un servidor Telnet de un router
    y genera los comandos dados
    https://docs.python.org/3.8/library/telnetlib.html
    """
    import telnetlib
    try:
        tn = telnetlib.Telnet(host)
        tn.read_until(b"User: ")
        tn.write(usuario.encode('ascii') + b"\n")
        if contra:
            #Al parecer tiene que hacer el write con la constraseña de getpass
            #Por que sí no, el muy especial no funciona
            tn.read_until(b"Password: ")
            tn.write(contra.encode('ascii') + b"\n")
        tn.write(b"enable\r")
        #Yo sé que solo se ejecuta un solo comando en la práctica, pero chanzón y sirve después xD
        for comando in comandos:
            tn.write(comando.encode('ascii') + b"\r")
        tn.write(b"exit\r")
        if mostrarConsola:
            print(tn.read_all())
        else:
            print('Se mandó el comando con éxito (Y)')
    except Exception as ex:
        print('Se produjo un error al enviar el archivo de configuraciónhacia el servidor FTP')
        print(ex)