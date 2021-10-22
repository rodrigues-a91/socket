import socket
import json


with open('./cliente-professor.json', 'r', encoding='utf8') as f:
    mensagem = json.load(f)

mensagem['tipo'] = 'professor'

HOST = 'localhost'
PORT = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

data = json.dumps(mensagem)
s.connect((HOST, PORT))
s.sendall(bytes(data, encoding='utf-8'))
dataResposta = s.recv(1024)

print('Mensagem ecoada: ',dataResposta.decode())