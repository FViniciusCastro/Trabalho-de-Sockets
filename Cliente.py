import socket


HOST = ''    # Coloque seu IP
PORT = 5000  # Porta do servidor

print(f'[*] Tentando conectar ao servidor {HOST}:{PORT}...')


try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print('[+] Conectado ao servidor.')

        while True:
            mensagem_usuario = input("Você: ")

            if mensagem_usuario.lower() in ["sair", "quit", "exit"]:
                print("[*] Encerrando a conexão...")
                break

            client_socket.sendall(mensagem_usuario.encode('utf-8'))

            data = client_socket.recv(1024)
            if not data:
                print("[-] Servidor desconectou inesperadamente.")
                break
            
            resposta_servidor = data.decode('utf-8')
            print(f"Servidor: {resposta_servidor}")

except ConnectionRefusedError:
    print(f"[!] Erro: A conexão foi recusada. Verifique se o servidor está rodando em {HOST}:{PORT}.")
except socket.gaierror:
    print(f"[!] Erro: O endereço IP '{HOST}' não é válido ou não foi encontrado.")
except Exception as e:
    print(f"[!] Ocorreu um erro inesperado: {e}")
finally:
    print("[*] Conexão fechada.")
