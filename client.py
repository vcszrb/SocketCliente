import socket
import os


def enviar_imagem(img="imagem.png", host="localhost", porta=50000):
    if not os.path.exists(img):
        print(f"Erro: o arquivo {img} nao foi encontrado.")
        print("Coloque a imagem na mesma pasta do cliente.py ou informe o caminho completo.")
        return

    print("Tentando conectar ao servidor...")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, porta))

    print("Conectado! Lendo e enviando a imagem...")

    with open(img, "rb") as arquivo:
        dados = arquivo.read()
        s.sendall(dados)

    print("Imagem enviada com sucesso!")
    s.close()


enviar_imagem()
