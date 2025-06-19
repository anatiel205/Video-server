import os
from flask import Flask, send_from_directory, abort

app = Flask(__name__)

# Pasta onde estão os vídeos
PASTA_VIDEOS = "videos.gitkeep"

@app.route("/")
def home():
    return "🟢 Servidor de Vídeos Online!"

@app.route("/videos/<path:filename>")
def serve_video(filename):
    # Proteção simples para evitar acesso fora da pasta
    if ".." in filename or filename.startswith("/"):
        abort(400)
    caminho_video = os.path.join(PASTA_VIDEOS, filename)
    if not os.path.isfile(caminho_video):
        abort(404)
    return send_from_directory(PASTA_VIDEOS, filename)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    # IMPORTANTE: rodar com host 0.0.0.0 para ser acessível externamente
    app.run(host="0.0.0.0", port=port)
