from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException
from paramiko import SSHException
from getpass import getpass
from datetime import datetime
from os.path import exists
import pyfiglet
from colorama import Fore, Style

class ConnectAndPush:
   
   def __init__(self):

      self.ascii_banner = pyfiglet.figlet_format("SSH con Netmiko\n") # BANNER
      self.archivos_conf = True
      self.clave=getpass('Ingrese la contraseña para todos los dispositivo: ')

      if (exists('/media/facundo/DATA/PROGRAMACION/DATOS/lista-IPs.txt')): # RUTA DONDE ESTA EL PLAYLIST DE HOST
         self.ip_file='/media/facundo/DATA/PROGRAMACION/DATOS/lista-IPs.txt' # RUTA DONDE ESTA EL PLAYLIST DE HOST
      else:
         print(Fore.RED + "La playlist de IP no esta disponible" + Style.RESET_ALL)
         self.archivos_conf = False
      if (exists('/media/facundo/DATA/PROGRAMACION/DATOS/comandos.txt')): # RUTA DONDE ESTA EL ARCHIVO CON LOS COMANDOS
         self.command_file='/media/facundo/DATA/PROGRAMACION/DATOS/comandos.txt' # RUTA DONDE ESTA EL ARCHIVO CON LOS COMANDOS
      else:
         print(Fore.RED + "El archivo de comandos no existe" + Style.RESET_ALL)
         self.archivos_conf = False

   def conectar(self):
      if (self.archivos_conf):
         print(Fore.MAGENTA + self.ascii_banner + "\n" + Style.RESET_ALL)
         equipos=open(self.ip_file)
         fecha = datetime.now().strftime("%Y%m%d")

         for IP in equipos:
            comandos=open(self.command_file)  # VARIABLE QUE CARGA LOS COMANDOS A EJECUTAR
            host = {
               'device_type': 'linux',
               'ip': IP,
               'port': '2233',
               'username': 'ifts24',
               'password': self.clave
            }
            print(Fore.LIGHTGREEN_EX + '\nConectandose a:' + host['ip'] + Style.RESET_ALL, end="")
            print('- - - - - - - - - - - -\n')
            
            try:
               hora = datetime.now().strftime("%H:%M:%S")   # ACTUALIZACION DE HORA
               ssh = ConnectHandler(**host)
               resultado=open('/media/facundo/DATA/PROGRAMACION/RESULTADOS/'+fecha+'-resultados.txt', 'a')
               resultado.write('\n- - - - - - - - - - -\n\n' + hora + ' --> ' + host['ip'])
               for coma in comandos:
                  salida = ssh.send_command(coma)
                  resultado.write('- - -\n' + coma + '\n' + salida + '\n')
                  print('Ejecutando:', coma)
                  print(salida)
                  print("\n- - - - - - - - - -\n")
               ssh.disconnect()
               resultado.close()

            except (NetMikoTimeoutException, NetMikoAuthenticationException, SSHException) as e:
               print(e)
               error=open('/media/facundo/DATA/PROGRAMACION/RESULTADOS/'+fecha+'-errores.txt', 'a')
               error.write('\n- - - - - - - - - - -\n' + hora + ' --> ' + str(e))   #INFORMA TIPO DE ERROR
               error.close()
               continue
      else:
         print('Verifique si los archivos de configuración esten en la carpeta de RESULTADOS.')


if __name__ == '__main__':
   ConnectAndPush().conectar()