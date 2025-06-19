from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)
PASTA_DOWNLOADS = "Videos_test"

# Garante que PASTA_DOWNLOADS é um diretório, não um arquivo
if os.path.exists(PASTA_DOWNLOADS):
    if not os.path.isdir(PASTA_DOWNLOADS):
        os.remove(PASTA_DOWNLOADS)  # remove se for arquivo
        os.makedirs(PASTA_DOWNLOADS)
else:
    os.makedirs(PASTA_DOWNLOADS)

@app.route("/")
def index():
    return "🟢 Servidor de vídeos online!"

@app.route("/upload_video", methods=["POST"])
def upload_video():
    if "file" not in request.files:
        return "Nenhum arquivo enviado", 400

    arquivo = request.files["file"]
    if arquivo.filename == "":
        return "Nome de arquivo vazio", 400

    nome_seguro = os.path.basename(arquivo.filename)
    destino = os.path.join(PASTA_DOWNLOADS, nome_seguro)
    try:
        arquivo.save(destino)
        return "Arquivo salvo com sucesso", 200
    except Exception as e:
        return f"Erro ao salvar arquivo: {e}", 500

@app.route("/videos/<path:filename>")
def acessar_video(filename):
    return send_from_directory(PASTA_DOWNLOADS, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
