import socket
import json
from time import strftime, gmtime


class Servidor:
    def __init__(self):
        self.HOST = 'localhost'
        self.PORT = 50000
        self.listaDeChamadas = []

    def verificarExistenciaDaChamada(self, turma):
        for chamada in self.listaDeChamadas:
            if chamada['idTurma'] == turma:
                return True

        return False

    def removerDaListaDeChamadas(self, turma):
        indexEncontrado = None
        for index, chamada in enumerate(self.listaDeChamadas):
            if chamada['idTurma'] == turma:
                indexEncontrado = index

        if indexEncontrado != None:
            del(self.listaDeChamadas[indexEncontrado])

    def getChamada(self, turma):
        indexEncontrado = None
        for index, chamada in enumerate(self.listaDeChamadas):
            if chamada['idTurma'] == turma:
                indexEncontrado = index

        if indexEncontrado != None:
            return self.listaDeChamadas[indexEncontrado]
        else:
            return None

    def marcarPresenca(self, data):
        indexEncontrado = None
        for index, chamada in enumerate(self.listaDeChamadas):
            if chamada['idTurma'] == data['idTurma']:
                indexEncontrado = index

        if indexEncontrado != None:
            self.listaDeChamadas[indexEncontrado]['listaPresenca'].append(
                data['matricula'])

    def requisicaoProfessor(self, data, conexao):
        chamadaExiste = self.verificarExistenciaDaChamada(
            data['idTurma'])

        if chamadaExiste and data['acao'] == 'iniciar':
            resposta = 'A chamada já foi iniciada'
            conexao.sendall(str.encode(resposta))

        elif chamadaExiste and data['acao'] == 'fechar':
            chamada = self.getChamada(data['idTurma'])
            self.removerDaListaDeChamadas(
                data['idTurma'])
            resposta = 'Chamada Fechada'
            horaAtual = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            conexao.sendall(str.encode(resposta + ' Horario: ' + horaAtual +
                                       ' \n Lista de alunos presentes: ' + str(chamada['listaPresenca'])))

        elif not chamadaExiste and data['acao'] == 'iniciar':
            chamadaNova = {'idTurma': data['idTurma'], 'listaPresenca': []}
            self.listaDeChamadas.append(chamadaNova)
            resposta = 'Chamada Iniciada'
            horaAtual = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            conexao.sendall(str.encode(
                resposta + ' Horario: ' + horaAtual))

        elif not chamadaExiste and data['acao'] == 'fechar':
            resposta = 'A chamada não foi aberta, ou já foi finalizada'
            conexao.sendall(str.encode(resposta))

    def requisicaoAluno(self, data, conexao):
        chamadaExiste = self.verificarExistenciaDaChamada(
            data['idTurma'])

        if chamadaExiste:
            self.marcarPresenca(data)
            resposta = 'Marcação feita com sucesso'
            horaAtual = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            conexao.sendall(str.encode(resposta + ' Turma: ' +
                                       data['idTurma'] + ' Horario: ' + horaAtual))
        else:
            resposta = 'Marcação não realizada'
            horaAtual = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            conexao.sendall(str.encode(resposta + ' Turma: 0 '
                                       + ' Horario: ' + horaAtual))

    def iniciar(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.HOST, self.PORT))
        s.listen()
        print('Aguardando conexão')

        while True:
            conexao, endereco = s.accept()
            print('Conectado em', endereco)

            data = conexao.recv(1024)

            if data != None:
                data = json.loads(data.decode('utf-8'))

                if data['tipo'] == 'professor':
                    self.requisicaoProfessor(data, conexao)
                elif data['tipo'] == 'aluno':
                    self.requisicaoAluno(data, conexao)


if __name__ == '__main__':
    servidor = Servidor()
    servidor.iniciar()
