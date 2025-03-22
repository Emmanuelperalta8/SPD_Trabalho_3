import socket

def start_client(server_host='127.0.0.1', server_port=12345):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_host, server_port))

    initial_msg = client.recv(1024).decode()
    if "Servidor cheio" in initial_msg:
        print(f"⚠️ {initial_msg}")
        client.close()
        return

    print(initial_msg)

    client_address = client.getsockname()
    print(f"Conectado ao servidor como {client_address}. Digite operações matemáticas (ou 'sair' para encerrar).")

    while True:
        operation = input("Digite a operação: ")
        if operation.lower() == 'sair':
            client.send(operation.encode())
            break

        client.send(operation.encode())
        response = client.recv(1024).decode()
        print(f"Servidor: {response}")

    print(f"Cliente {client_address} desconectado.")
    client.close()

if __name__ == "__main__":
    start_client()