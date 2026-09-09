#####################################################
#                                                   #
# Título do trabalho: Trabalho de Sockets           #
# Disciplina: Redes de Computadores PPComp          #
# Módulo: Cliente Ar-Condicionado Inteligente      #
#                                                   #
#####################################################

from Config import *
from Message import *
from ClientUtil import *
import socket

deviceID = None

if __name__ == '__main__':
    print('Inicializando cliente: Ar-Condicionado Inteligente...')
    try:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        destination = (SERVIDOR, PORTA)
        connection.connect(destination)
    except:
        print(f'Falha ao tentar se conectar com o servidor {SERVIDOR} porta {PORTA}')
        exit()

    device = Device(connection, NUM_AR_CONDICIONADO)
    roomDict = ClientRegister(device)
    
    if roomDict is not None:
        deviceID, roomID, roomName = SelectRoom(device, roomDict)
        if deviceID is not None:
            while True:
                print(f'\n==> Ambiente [{roomID}] {roomName}')
                print('Aguardando comandos de climatização do servidor...')
                msg = ReceiveMessage(connection, device)
                
                if msg is not None and msg.code in (MSG_LAMPADA, MSG_ATUADOR):
                    print('Comando de climatização recebido do servidor!')
                    print('#####################################')
                    if msg.action == AR_LIGADO:
                        print('        AR-CONDICIONADO LIGADO [REFRIGERANDO]')
                    elif msg.action == AR_DESLIGADO:
                        print('        AR-CONDICIONADO DESLIGADO')
                    else:
                        print(f'Ação inválida: {msg.action}')
                    print('#####################################')
                    
                    # Confirma a execução para o servidor
                    msg_resp = MessageStatus()
                    connection.send(msg_resp.pack(deviceID, ACAO_EXECUTADA))
                else:
                    print('Mensagem inválida ou desconexão.')
                    break

        connection.close()
