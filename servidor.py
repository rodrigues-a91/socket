import socket
import json
from time import strftime, gmtime

HOST = 'localhost'
PORT = 50000
chamadaAberta = False
listaPresenca = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
print('Aguardando conexão')


while True:
    conexao, endereco = s.accept()
    print('Conectado em', endereco)

    data = conexao.recv(1024)

    if data != None:
        data = json.loads(data.decode('utf-8'))
        if data['tipo'] == 'professor':
            if data['acao'] == 'iniciar':
                if chamadaAberta:
                    resposta = 'A chamada já foi iniciada'
                    conexao.sendall(str.encode(resposta))
                else:
                    chamadaAberta = True
                    resposta = 'Chamada Iniciada'
                    horaAtual = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    conexao.sendall(str.encode(resposta + ' Horario: ' + horaAtual))
            if data['acao'] == 'fechar':
                if chamadaAberta:
                    chamadaAberta = False
                    resposta = 'Chamada Fechada'
                    horaAtual = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    conexao.sendall(str.encode(resposta + ' Horario: ' + horaAtual + ' \n Lista de alunos presentes: ' + str(listaPresenca)))
                else:
                    resposta = 'A chamada já está fechada'
                    conexao.sendall(str.encode(resposta))
                    
                    
        
        elif data['tipo'] == 'aluno':
            if chamadaAberta:
                listaPresenca.append(data['matricula'])
                print('chamada aberta')
            else:
                print('chamada fechada')
       