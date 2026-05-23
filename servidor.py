import socket
import os
import hashlib

print("SERVIDOR INICIOU")

HOST = "0.0.0.0"
PORT = 5000

PASTA_IMAGENS = os.path.expanduser("~/Pictures/")
os.makedirs(PASTA_IMAGENS, exist_ok=True)

print("A imagem será salva em:", PASTA_IMAGENS)

def receber_tudo(conexao, tamanho):
    dados = b""

    while len(dados) < tamanho:
        pacote = conexao.recv(tamanho - len(dados))

        if not pacote:
            break

        dados += pacote

    return dados

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORT))
    servidor.listen(1)

    print(f"Servidor aguardando conexão na porta {PORT}...")

    conexao, endereco = servidor.accept()

    with conexao:
        print("Cliente conectado:", endereco)

        tamanho_bytes = receber_tudo(conexao, 8)
        tamanho_imagem = int.from_bytes(tamanho_bytes, byteorder="big")

        print("Tamanho esperado:", tamanho_imagem, "bytes")

        imagem = receber_tudo(conexao, tamanho_imagem)

        print("Tamanho recebido:", len(imagem), "bytes")

        hash_nome = hashlib.sha256(imagem).hexdigest()
        caminho_arquivo = os.path.join(PASTA_IMAGENS, hash_nome + ".png")

        with open(caminho_arquivo, "wb") as arquivo:
            arquivo.write(imagem)

        print("Imagem salva com sucesso em:")
        print(caminho_arquivo)

        conexao.sendall(b"Imagem recebida com sucesso")