# coding: utf-8
import socket
from ast import literal_eval
import threading
from datetime import datetime

ENCODE = "UTF-8"
MAX_BYTES = 65535
PORT = 5000            # Porta que o servidor escuta
HOST = ''              # Endereco IP do Servidor

def server():
    #Abrindo uma porta UDP
    orig = (HOST, PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(orig)
    clientes = {}
    while True:
        #recebi dados
        data, address = sock.recvfrom(MAX_BYTES)
 
        #Criação de thread orientada a objeto
        tratador = ThreadTratador(sock,clientes, data, address)
        tratador.start()

class ThreadTratador(threading.Thread):

    def __init__(self, sock,clientes, data, address):
        threading.Thread.__init__(self)
        self.sock = sock
        self.data = data
        self.address = address
        self.clientes = clientes
    def run(self):
        self.__tratar_conexao(self.sock,self.clientes ,self.data, self.address)

    def __tratar_conexao(self, sock, clientes, data, address):
        
        text = data.decode(ENCODE)

       
        #{"acao": "registro", "id":"Alessandra"}
        #"acao": "envio", "payload":"Hi","destino":"c1"}
        mensagem = literal_eval(text)
        
        if "acao" in mensagem.keys():
        
            if mensagem["acao"] == "registro":
        
                # 1. Registrar Cliente
        
                id = mensagem["id"]
        
                clientes[id] = address

                text = 'Usuário logado com sucesso!'
                
                print(clientes)
                data = text.encode(ENCODE)

                sock.sendto(data, address)


            if mensagem["acao"] == "envio":

                # 2. Enviar mensagem
        
                payload = mensagem["payload"]
        
                destino = mensagem["destino"] 
        
                data = payload.encode(ENCODE)
        
                sock.sendto(data, clientes[destino])

                
            """text = "Sucesso"
            data = text.encode(ENCODE)
            sock.sendto(data, clientes[destino])"""
        #Envia resposta
        #text = "Quantidade de bytes enviados: " + str(len(data))
server()      


