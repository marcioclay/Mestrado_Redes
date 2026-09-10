#####################################################
<<<<<<< HEAD
#                                                   #
# Título do trabalho: Trabalho de Sockets           #
# Disciplina: Redes de Computadores PPComp 2026     #
# Módulo: Cliente Ar-Condicionado Inteligente       #
#                                                   #
=======
#													#
# Título do trabalho: Trabalho de Sockets			#
#		  Disciplina: Redes de Computadores PPComp	#
#													#
>>>>>>> 2889c31914bb79de38b657edc64e93e35324afad
#####################################################

from Config import *
from Message import *
from ClientUtil import *
import socket

deviceID = None

####################
# Inicializando... #
####################
if __name__ == '__main__':
    print('Inicializando cliente: Ar-Condicionado...')
    try:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        destination = (SERVIDOR, PORTA)
        connection.connect(destination)
    except:
        print(f'Falha ao tentar se conectar com o servidor {SERVIDOR} porta {PORTA}')
        exit()
    device = Device(connection, NUM_AR_CONDICIONADO)
    roomDict = ClientRegister(device)
    if roomDict != None:
        deviceID, roomID, roomName = SelectRoom(device, roomDict)

        # Evita exibição de caracteres nulos \x00
        roomNameClean = roomName.replace('\x00', '').strip() if roomName else ""

        if deviceID != None:
            while True:
                print(f'\n==> Ambiente [{roomID}] {roomNameClean}')
                msg = ReceiveMessage(connection, device)

                if (msg.code == MSG_LAMPADA):
                    print('Acionamento recebido do servidor!!!')
                    print('#####################################')
                    if msg.action == 23:
                        print('      AR-CONDICIONADO: SET 23°C')
                    elif msg.action == 0:
                        print('      AR-CONDICIONADO: DESLIGADO')
                    else:
                        print(f'      Ação recebida: {msg.action}')
                    print('#####################################')
                    msg = MessageStatus()
                    connection.send(msg.pack(deviceID, ACAO_EXECUTADA))
                else:
                    print('Mensagem inválida code:', msg.code)
        connection.close()
