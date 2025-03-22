import socket
import threading

MAX_CLIENTS = 10
active_clients = 0
lock = threading.Lock()

def process_request(client_socket, addr):
    global active_clients

    with lock:
        if active_clients >= MAX_CLIENTS:
            client_socket.send("Servidor cheio. Tente novamente mais tarde.".encode())
            client_socket.close()
            return

        active_clients += 1

    print(f"Cliente {addr} conectado. Clientes ativos: {active_clients}")
    client_socket.send("Conectado ao servidor. Você pode enviar operações.".encode())

    while True:
        try:
            request = client_socket.recv(1024).decode()
            if not request:
                break

            print(f"Recebido de {addr}: {request}")

            if request.lower() == "sair":
                print(f"Cliente {addr} solicitou desconexão.")
                break

            try:
                result = eval(request)
                response = f"Resultado: {result}"
            except Exception as e:
                response = f"Erro: {str(e)}"

            client_socket.send(response.encode())
        except ConnectionResetError:
            break

    with lock:
        active_clients -= 1

    print(f"Cliente {addr} desconectado. Clientes ativos: {active_clients}")
    client_socket.close()

def start_server(host='0.0.0.0', port=12345):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Servidor ouvindo em {host}:{port}")

    while True:
        client_socket, addr = server.accept()

        with lock:
            if active_clients >= MAX_CLIENTS:
                print(f"Servidor cheio! Recusando conexão de {addr}.")
                client_socket.send("Servidor cheio. Tente novamente mais tarde.".encode())
                client_socket.close()
                continue

        client_thread = threading.Thread(target=process_request, args=(client_socket, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()