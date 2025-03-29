import socket

servidor = '127.0.0.1'

def start_client(server_host=servidor, server_port=12345):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Tenta se conectar ao servidor
    try:
        client.connect((server_host, server_port))
    except ConnectionRefusedError:
        print("Erro: O servidor não está disponível.")
        return
    
    # Recebe a mensagem inicial do servidor (ex: servidor cheio ou mensagem de boas-vindas)
    initial_msg = client.recv(1024).decode()
    
    if "Servidor cheio" in initial_msg:
        print(f"⚠️ {initial_msg}")
        client.close()
        return

    print(initial_msg)

    # Exibe o endereço do cliente
    client_address = client.getsockname()
    print(f"Conectado ao servidor como {client_address}. Digite operações matemáticas (ou 'sair' para encerrar).")

    while True:
        operation = input("Digite a operação: ")
        
        # Se o cliente digitar 'sair', envia a mensagem e encerra a conexão
        if operation.lower() == 'sair':
            client.send(operation.encode())
            print("Desconectando...")
            break

        # Envia a operação para o servidor
        client.send(operation.encode())
        
        # Recebe a resposta do servidor
        response = client.recv(1024).decode()
        print(f"Servidor: {response}")

    print(f"Cliente {client_address} desconectado.")
    client.close()

if __name__ == "__main__":
    start_client()
