import os
from flask import Flask, request, abort, jsonify, send_from_directory

app = Flask(__name__)

PASTA_VIDEOS = "Videos_test"

@app.route("/")
def home():
    return "Servidor de Vídeos Online!"

@app.route("/videos/<path:filename>")
def serve_video(filename):
    if ".." in filename or filename.startswith("/"):
        abort(400)
    caminho = os.path.join(PASTA_VIDEOS, filename)
    if not os.path.isfile(caminho):
        abort(404)
    return send_from_directory(PASTA_VIDEOS, filename)

# Nova rota para upload de vídeo
@app.route("/upload_video", methods=["POST"])
def upload_video():
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400
    arquivo = request.files["file"]
    if arquivo.filename == "":
        return jsonify({"error": "Nome do arquivo inválido"}), 400
    
    # Segurança: evitar path traversal
    if ".." in arquivo.filename or arquivo.filename.startswith("/"):
        return jsonify({"error": "Nome de arquivo inválido"}), 400

    # Salvar arquivo na pasta dos vídeos
    destino = os.path.join(PASTA_VIDEOS, arquivo.filename)
    arquivo.save(destino)

    return jsonify({"mensagem": "Arquivo enviado com sucesso", "filename": arquivo.filename})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    if not os.path.exists(PASTA_VIDEOS):
        os.makedirs(PASTA_VIDEOS)
    app.run(host="0.0.0.0", port=port)
