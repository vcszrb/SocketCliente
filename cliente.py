import socket
import os

print("CLIENTE INICIOU")

HOST = "127.0.0.1"
PORT = 5000

CAMINHO_IMAGEM = "imagem.png"

print("Pasta atual:", os.getcwd())
print("Procurando imagem em:", os.path.abspath(CAMINHO_IMAGEM))

if not os.path.exists(CAMINHO_IMAGEM):
    print("ERRO: imagem não encontrada.")
    print("A imagem precisa estar na mesma pasta do cliente.py")
    input("Aperte ENTER para sair...")
    exit()

with open(CAMINHO_IMAGEM, "rb") as arquivo:
    imagem = arquivo.read()

print("Imagem encontrada.")
print("Tamanho da imagem:", len(imagem), "bytes")

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        print("Tentando conectar ao servidor...")
        cliente.connect((HOST, PORT))

        print("Conectado ao servidor.")

        cliente.sendall(len(imagem).to_bytes(8, byteorder="big"))
        cliente.sendall(imagem)

        print("Imagem enviada.")

        resposta = cliente.recv(1024)
        print("Resposta do servidor:", resposta.decode())

except ConnectionRefusedError:
    print("ERRO: conexão recusada.")
    print("Verifique se o servidor está aberto antes de rodar o cliente.")

except Exception as erro:
    print("ERRO inesperado:")
    print(erro)

input("Aperte ENTER para sair...")