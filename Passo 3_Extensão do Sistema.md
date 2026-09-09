## Os dados abaixo são as modificações no código, devido alguns erros encontrados e inclusão de ar-condicionado.


## Erro 1: Rótulo Incorreto no Termômetro

Ao inicializar client_temperatura, mensagem de diz: "sensor de presença" no arquivo Cliente_Temperatura.py

<img width="700" height="180" alt="image" src="https://github.com/user-attachments/assets/2d5a729b-bc91-4b97-8306-2a3bcd365f6a" /> 

## Erro 2: Correção do print, inserção do fstring no arquivo DeviceThread.py.

Caso haja um erro de código dos dispositivos, devido a falta de "f(fstring)" em alguns arquivos, a mensagem de erro sai literal sem o nome
do dispositivo.

<img width="700" height="200" alt="image" src="https://github.com/user-attachments/assets/cdbd2797-8e8f-40cf-a281-2067b876c550" />


### Correção: adiciona o caracter f nas mensagens de log e substitui a variavel inexistente device.code por msg.code.

<img width="934" height="49" alt="image" src="https://github.com/user-attachments/assets/cd700635-d56d-4a11-a5df-ae6da3c4bc0d" />

* Mapeamento de Erros por Linha em DeviceThread.py 

- Linha 48: Falta o caractere f antes das aspas no print (faz com que {deviceType} seja impresso como texto literal)
  e possui ponto e vírgula desnecessário ao final.
- Linha 61: Falta o f antes das aspas no print (imprime {device.roomID} e {device.roomName} como texto).
- Linha 78: Chamada sendMessage(...) com "s" minúsculo. Como a função declarada na linha 139 é SendMessage(...),
  isso dispara a exceção NameError: name 'sendMessage' is not defined.
- Linha 79: Falta o f antes das aspas no print (imprime {roomID} como texto).
- Linha 105: Chamada sendMessage(...) com "s" minúsculo (NameError).
- Linha 106: Falta o f antes das aspas no print (imprime {device.ID} e {msg.deviceID} como texto).
- Linha 113: Falta o f antes das aspas e utiliza device.code (atributo inexistente no objeto Device), quando o correto é msg.code.
- Linha 121: Chamada sendMessage(...) com "s" minúsculo (NameError).
- Linha 122: Falta o f antes das aspas no print (imprime {device.ID} e {msg.deviceID} como texto).

  
