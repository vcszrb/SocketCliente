import socket
import hashlib
from pathlib import Path


def verificar_tipo_imagem(imagem):
    if imagem.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"

    if imagem.startswith(b"\xff\xd8\xff"):
        return ".jpg"

    return None


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 50000))
s.listen(1)

print("=== SERVIDOR AGUARDANDO CONEXAO ===")

conexao, endereco = s.accept()
print(f"Conectado por: {endereco}")

conteudo_imagem = []

while True:
    dados = conexao.recv(4096)

    if not dados:
        break

    conteudo_imagem.append(dados)

imagem_completa = b"".join(conteudo_imagem)

if imagem_completa:
    extensao = verificar_tipo_imagem(imagem_completa)

    if extensao is None:
        print("Erro: o arquivo recebido nao e PNG nem JPG.")
    else:
        hash_nome = hashlib.md5(imagem_completa).hexdigest()
        nome_arquivo = f"{hash_nome}{extensao}"

        pasta_imagens = Path.home() / "Pictures"
        pasta_imagens.mkdir(parents=True, exist_ok=True)

        caminho_final = pasta_imagens / nome_arquivo

        with open(caminho_final, "wb") as arquivo:
            arquivo.write(imagem_completa)

        print("\nSUCESSO!")
        print(f"Imagem salva em: {caminho_final}")
else:
    print("Nenhum dado foi recebido.")

conexao.close()
s.close()
