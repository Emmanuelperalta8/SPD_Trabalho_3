import socket  # Biblioteca para comunicação via rede (TCP/IP)

# IP do servidor (localhost = mesma máquina)
servidor = '127.0.0.1'

# Função principal para iniciar o cliente
def start_client(server_host=servidor, server_port=12345):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um socket TCP

    # Tenta se conectar ao servidor
    try:
        client.connect((server_host, server_port))
    except ConnectionRefusedError:
        print("Erro: O servidor não está disponível.")  # Se o servidor não estiver aceitando conexões
        return

    # Aguarda uma mensagem inicial do servidor (pode ser uma mensagem de boas-vindas ou "Servidor cheio")
    initial_msg = client.recv(1024).decode()

    if "Servidor cheio" in initial_msg:
        print(f"⚠️ {initial_msg}")  # Exibe a mensagem de servidor cheio
        client.close()
        return

    print(initial_msg)  # Mensagem de boas-vindas do servidor

    # Exibe o IP e a porta local do cliente
    client_address = client.getsockname()
    print(f"Conectado ao servidor como {client_address}. Digite operações matemáticas (ou 'sair' para encerrar).")

    while True:
        # Lê a operação matemática que o usuário deseja enviar
        operation = input("Digite a operação: ")

        # Se o usuário quiser sair
        if operation.lower() == 'sair':
            client.send(operation.encode())  # Envia "sair" ao servidor
            print("Desconectando...")
            break  # Sai do loop

        # Envia a operação para o servidor
        client.send(operation.encode())

        # Espera e imprime a resposta do servidor
        response = client.recv(1024).decode()
        print(f"Servidor: {response}")

    # Ao final, informa que o cliente se desconectou e fecha o socket
    print(f"Cliente {client_address} desconectado.")
    client.close()

# Executa a função principal se o script for chamado diretamente
if __name__ == "__main__":
    start_client()
