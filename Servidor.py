import socket
import requests
import json     


HOST = '0.0.0.0'  
PORT = 5000       # Porta do servidor 


API_KEY = "" # <-- Insira a chave aqui, vá na plataforma do gemini e crie e cole aqui

def consulta_gemini(mensagem):
    """
    Consulta a API do Google Gemini para obter uma resposta a uma mensagem.

    Args:
        mensagem (str): A mensagem do usuário a ser enviada ao modelo Gemini.

    Returns:
        str: A resposta gerada pelo modelo Gemini ou uma mensagem de erro.
    """
    try:
       
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

        #JSON.
        headers = {
            "Content-Type": "application/json"
        }


        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": mensagem}
                    ]
                }
            ]
        }


        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        response.raise_for_status() 

        data = response.json()
        

        if data.get('candidates') and len(data['candidates']) > 0 and \
           data['candidates'][0].get('content') and \
           data['candidates'][0]['content'].get('parts') and \
           len(data['candidates'][0]['content']['parts']) > 0:
            return data['candidates'][0]['content']['parts'][0]['text'].strip()
        else:

            print(f"DEBUG: Resposta completa da API: {data}") # Ajuda na depuração
            return "Erro: Resposta inesperada da API do Gemini. Verifique os logs do servidor."

    except requests.exceptions.RequestException as e:

        return f"Erro de requisição da API do Gemini: {e}"
    except json.JSONDecodeError:

        return "Erro: Não foi possível decodificar a resposta JSON da API do Gemini."
    except Exception as e:

        return f"Erro inesperado ao consultar o Gemini: {e}"

print(f'[*] Servidor Chatbot iniciado em {HOST}:{PORT}')
print('[*] Aguardando conexão do cliente...')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

    server_socket.bind((HOST, PORT))

    server_socket.listen(1)


    conn, addr = server_socket.accept()
    with conn: 
        print(f'[+] Cliente conectado: {addr}')
        while True:

            data = conn.recv(1024)
            if not data:
                # Se não houver dados o cliente desconectou
                print(f'[-] Cliente {addr} desconectou.')
                break # Sai do loop
            
            #Pra string UTF-8
            mensagem_cliente = data.decode('utf-8')
            print(f'Cliente ({addr}): {mensagem_cliente}')


            resposta_servidor = consulta_gemini(mensagem_cliente)

            conn.sendall(resposta_servidor.encode('utf-8'))
            print(f'Servidor: {resposta_servidor}')

print('[*] Servidor encerrado.')