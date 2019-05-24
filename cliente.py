import socket
from datetime import datetime
import threading
from ast import literal_eval

import time

ENCODE = "UTF-8"
HOST = 'localhost'   # Endereço IP do Servidor
PORT =  5000         # Porta que o Servidor esta
MAX_BYTES = 65535    # Quantidade de Bytes a serem ser recebidos

def cliente():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Inicializar um socket UDP

    dest = (HOST, PORT)                                     # Define IP de origem e Porta de destino  

    print('================== SEJA BEM VINDO AO CHAT ========================')

    print('======================== MENU ====================================')
    
    print('1- Digite R para se registrar;')

    print('2 - Digite E para envio de mesagens;')

    print('==================================================================')

    data = ""    
    
    choice = input('Digite R para se registrar: ')        

    if choice == 'R':
        
        id= input('Digite seu id : ')

        text = {'acao': 'registro', 'id':id}

        text = str(text)

        #mensagem = literal_eval(text)    

        #mensagem = str(mensagem)
        data = text.encode(ENCODE)

        sock.sendto(data, dest)
        
        data, dest = sock.recvfrom(MAX_BYTES)
      
        data = data.decode(ENCODE)

        print(data) 

    choice = input('Digite C  para consultar os clientes logados ')        

    if choice == 'C':

        text = {'acao': 'consulta'}
        text = str(text)
        
        data = text.encode(ENCODE)
        sock.sendto(data, dest)
        
        data, dest = sock.recvfrom(MAX_BYTES)
      
        data = data.decode(ENCODE)

        print(data) 


    while True:    
      
        choice = input('Digite E  para enviar mensagem: ')        

        text = ''

       
        if choice == 'E':

                        
            mensagem = input('Digite a mensagem a qual você deseja enviar: ')

            destino = input('Digite o id do destino: ')

            text = {'acao': 'envio', 'payload': mensagem, 'destino': destino}

            text = str(text)

            data = text.encode(ENCODE)
        
            sock.sendto(data, dest)

            escuta = Listen(sock, data,dest)
            escuta.start()

            escuta.join()

        
class Listen(threading.Thread):
    def __init__(self, sock, data, dest):
        threading.Thread.__init__(self)
        self.sock = sock
        self.data = data
        self.dest = dest
    
    def run(self):
        self.__escuta(self.sock,self.data,self.dest)
    
    def __escuta(self,sock,data,dest):
        
        data, dest = sock.recvfrom(MAX_BYTES)
        data = data.decode(ENCODE)
        print('Resposta',data)


cliente()
