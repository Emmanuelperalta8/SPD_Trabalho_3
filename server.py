import socket
import multiprocessing  # Usado para criar processos paralelos e compartilhar variáveis entre eles

MAX_CLIENTS = 5  # Limite de clientes simultâneos

# Variável compartilhada entre processos para contar quantos clientes estão ativos
active_clients = multiprocessing.Value('i', 0)  # 'i' = inteiro

# Lock para evitar condições de corrida ao modificar active_clients
lock = multiprocessing.Lock()

# Função que será executada para cada cliente conectado
def process_request(client_socket, addr):
    global active_clients

    # Verifica se o servidor está cheio
    with lock:
        if active_clients.value >= MAX_CLIENTS:
            client_socket.send("Servidor cheio. Tente novamente mais tarde.".encode())
            client_socket.close()
            return
        active_clients.value += 1  # Incrementa a contagem de clientes ativos

    print(f"Cliente {addr} conectado. Clientes ativos: {active_clients.value}")
    client_socket.send("Conectado ao servidor. Você pode enviar operações.".encode())

    # Loop principal de comunicação com o cliente
    while True:
        try:
            request = client_socket.recv(1024).decode()  # Recebe a mensagem do cliente
            if not request:
                break  # Se não receber nada, encerra o loop

            print(f"Recebido de {addr}: {request}")

            if request.lower() == "sair":
                print(f"Cliente {addr} solicitou desconexão.")
                break  # Se o cliente digitar "sair", encerra o loop

            try:
                # Avalia a expressão matemática com segurança, sem permitir funções perigosas
                result = eval(request, {"__builtins__": None}, {})  # Ambiente restrito sem funções internas
                response = f"Resultado: {result}"
            except Exception as e:
                response = f"Erro: {str(e)}"  # Se der erro de sintaxe, etc.

            client_socket.send(response.encode())  # Envia o resultado de volta
        except ConnectionResetError:
            break  # Cliente desconectou de forma abrupta
        except Exception as e:
            print(f"Erro durante a comunicação com {addr}: {e}")
            break

    # Quando cliente sai, atualiza a contagem de clientes ativos
    with lock:
        active_clients.value -= 1

    print(f"Cliente {addr} desconectado. Clientes ativos: {active_clients.value}")
    client_socket.close()

# Função principal que inicia o servidor
def start_server(host='0.0.0.0', port=12345):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria o socket do servidor
    server.bind((host, port))  # Liga o socket a um IP e porta
    server.listen(5)  # Começa a ouvir por conexões
    print(f"Servidor ouvindo em {host}:{port}")

    while True:
        client_socket, addr = server.accept()  # Aceita uma nova conexão

        # Verifica se há espaço para mais um cliente
        with lock:
            if active_clients.value >= MAX_CLIENTS:
                print(f"Servidor cheio! Recusando conexão de {addr}.")
                client_socket.send("Servidor cheio. Tente novamente mais tarde.".encode())
                client_socket.close()
                continue

        # Cria um novo processo para lidar com o cliente
        client_process = multiprocessing.Process(target=process_request, args=(client_socket, addr))
        client_process.start()

# Inicia o servidor se o script for executado diretamente
if __name__ == "__main__":
    start_server()
