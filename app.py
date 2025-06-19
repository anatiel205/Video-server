import os
from flask import Flask, send_from_directory, abort

app = Flask(__name__)

PASTA_VIDEOS = "videos.gitkeep"

@app.route("/")
def home():
    return "Servidor de Vídeos Online!"

@app.route("/videos/<path:filename>")
def serve_video(filename):
    if ".." in filename or filename.startswith("/"):
        abort(400)  # evitar path traversal
    caminho = os.path.join(PASTA_VIDEOS, filename)
    if not os.path.isfile(caminho):
        abort(404)
    return send_from_directory(PASTA_VIDEOS, filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Pega a porta do ambiente ou default 5000
    app.run(host="0.0.0.0", port=port)
