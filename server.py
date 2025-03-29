import socket
import multiprocessing

MAX_CLIENTS = 5
active_clients = multiprocessing.Value('i', 0)  # Usamos 'multiprocessing.Value' para compartilhamento seguro
lock = multiprocessing.Lock()

def process_request(client_socket, addr):
    global active_clients

    with lock:
        if active_clients.value >= MAX_CLIENTS:
            client_socket.send("Servidor cheio. Tente novamente mais tarde.".encode())
            client_socket.close()
            return

        active_clients.value += 1

    print(f"Cliente {addr} conectado. Clientes ativos: {active_clients.value}")
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
                # Avaliação segura do comando
                result = eval(request, {"__builtins__": None}, {})  # Ambiente restrito
                response = f"Resultado: {result}"
            except Exception as e:
                response = f"Erro: {str(e)}"

            client_socket.send(response.encode())
        except ConnectionResetError:
            break
        except Exception as e:
            print(f"Erro durante a comunicação com {addr}: {e}")
            break

    with lock:
        active_clients.value -= 1

    print(f"Cliente {addr} desconectado. Clientes ativos: {active_clients.value}")
    client_socket.close()

def start_server(host='0.0.0.0', port=12345):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Servidor ouvindo em {host}:{port}")

    while True:
        client_socket, addr = server.accept()

        with lock:
            if active_clients.value >= MAX_CLIENTS:
                print(f"Servidor cheio! Recusando conexão de {addr}.")
                client_socket.send("Servidor cheio. Tente novamente mais tarde.".encode())
                client_socket.close()
                continue

        # Criar um novo processo para cada cliente
        client_process = multiprocessing.Process(target=process_request, args=(client_socket, addr))
        client_process.start()

if __name__ == "__main__":
    start_server()
