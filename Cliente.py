import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('0.0.0.0',12345)) #substituir o 0.0.0.0 pelo IP do servidor
cliente.sendall("mensagem".encode())

resposta = cliente.recv(1024).decode()
print("resposta do servidor: ", resposta)

cliente.close()

