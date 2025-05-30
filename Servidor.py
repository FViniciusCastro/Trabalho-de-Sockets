import socket

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor.bind(('0.0.0.0',12345)) #substituir o 0.0.0.0 pelo IP do servidor

servidor.listen(1)
print("aguardendo conexão")

conn, addr = servidor.accept()
print("conectado por ", addr)
dados = conn.recv(1024).decode()
print("recebido ", dados)
conn.sendall("mensagem recebida ". encode())

conn.close

