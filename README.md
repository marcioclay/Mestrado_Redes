# Mestrado de Computação Aplicada

Repositório acadêmico desenvolvido para a disciplina de **Redes de Computadores** (PPComp / Ifes), focado na documentação, correção de falhas  e expansão de um sistema cliente-servidor baseado em sockets TCP.

---

## 1. Fundamentos de Sockets TCP e Tratamento de Buffer

O sistema utiliza a arquitetura orientada a conexão do protocolo **TCP (Transmission Control Protocol)** sobre a camada de transporte. Diferente do UDP, o TCP garante entrega confiável, ordenação de pacotes e controle de fluxo, operando através de um fluxo contínuo de bytes.

### O Papel do Buffer TCP e a Fragmentação de Mensagens
No protocolo TCP, **não existe o conceito de limites de mensagens **. Isso significa que uma chamada de envio (`send()`) em uma extremidade não garante uma correspondência direta e exclusiva com uma chamada de recebimento (`recv()`) na outra extremidade. 
* **Efeito de Agrupamento (*Nagling* / Empacotamento):** Vencendo a janela de transmissão, múltiplos pequenos envios realizados pelo cliente podem ser agrupados pelo sistema operacional em um único pacote TCP recebido de uma só vez.
* **Efeito de Fragmentação (*Splitting*):** Mensagens longas podem ser divididas em segmentos menores devido à MTU (*Maximum Transmission Unit*) da rede.

### Como o Código Trata o Buffer
Para contornar essa característica do protocolo TCP, a aplicação implementa uma classe utilitária de buffer (`Message.py` / `ClientUtil.py`). O sistema acumula os bytes recebidos em uma string/buffer interno e extrai os dados com base no tamanho fixo ou delimitadores do protocolo de aplicação, garantindo que pacotes fragmentados ou colados sejam interpretados corretamente antes de alimentar a máquina de estados.

---

## 2. Arquitetura e Diagramas de Fluxo

O sistema adota um modelo **Cliente/Servidor Multithread**, onde a central de controle gerencia conexões concorrentes e o estado de múltiplos ambientes residenciais[cite: 32].

### Papéis das Threads na Arquitetura
1. **Thread Principal do Servidor (`Server.py`):** Responsável por abrir o socket de escuta (*listen*) na porta TCP configurada e aguardar novas conexões de clientes em um loop contínuo (*accept*). A cada nova conexão, uma nova thread dedicada é instanciada.
2. **Threads de Dispositivos (`DeviceThread.py`):** Instanciadas de forma independente para cada cliente conectado. Gerenciam o ciclo de vida do dispositivo (registro, seleção de ambiente e escuta de eventos).
3. **Thread de Controle Geral (`GeneralControl.py`):** Gerencia a lógica de negócio global e o roteamento de eventos entre sensores e atuadores utilizando filas de mensagens thread-safe (`queue.Queue`).

### Fluxo de Comunicação via Filas (*Queues*)
* Quando um sensor (ex: **Termômetro** ou **Sensor de Presença**) envia uma leitura, a `DeviceThread` intercepta o dado e o deposita na fila central (`controlQueue`)[cite: 21, 30].
* A `GeneralControl` retira o item da fila, identifica o ambiente de destino (`roomID`) e despacha o comando para a lista de filas específicas do atuador correspondente (`lampQueueList`)[cite: 21, 28].
* O atuador (ex: **Lâmpada** ou **Ar-Condicionado**) retira o comando de sua fila local e executa a alteração física de estado[cite: 2, 3, 30].

---

## 3. O Protocolo de Comunicação

O protocolo de aplicação define a estrutura binária e o sequenciamento das mensagens trocadas entre clientes e servidor[cite: 32]. Cada mensagem possui campos com tamanhos múltiplos de 1 byte[cite: 32]:
* **Código da Mensagem (1 byte):** Identifica a operação (ex: Registro, Listagem, Seleção, Envio de Sensor, Acionamento).
* **Data e Hora:** Carimbo temporal para registro de logs e histórico.
* **ID do Dispositivo:** Identificador único atribuído pelo servidor após o registro no ambiente.

### Tabela de Códigos de Mensagens
| Código | Tipo / Função | Descrição |
| :--- | :--- | :--- |
| `2` | `MSG_REGISTRO` | Enviado pelo cliente informando seu tipo ao conectar. |
| `3` | `MSG_LISTA_AMBIENTES` | Servidor envia o dicionário de cômodos disponíveis. |
| `4` | `MSG_SELECIONA_AMBIENTE` | Cliente informa o ID do cômodo onde está instalado. |
| `5` | `MSG_SENSOR` | Envio de leituras contínuas (temperatura ou presença). |
| `6` | `MSG_LAMPADA` / Atuador | Comando de acionamento enviado pelo servidor ao atuador. |

---

## 4. Roteiro Detalhado de Testes

### Inicialização do Servidor
1. Abra o terminal na raiz do projeto e execute[cite: 11]:
   ```bash
   python Server.py
