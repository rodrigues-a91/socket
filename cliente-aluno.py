import socket
import json

mensagem = {'idTurma':'E58',
            'tipo': 'aluno',
            'matricula': '205190110'}

HOST = 'localhost'
PORT = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

data = json.dumps(mensagem)
s.connect((HOST, PORT))
s.sendall(bytes(data, encoding='utf-8'))
dataResposta = s.recv(1024)

print('Mensagem ecoada: ',dataResposta.decode())