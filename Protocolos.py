"""
Script encargado de todas las funciones relacionadas con protocolos
de red, como FTP y TELNET
"""

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
