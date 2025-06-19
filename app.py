import os
from flask import Flask, request, send_from_directory, abort, jsonify

# --- Configurações ---
PASTA_DOWNLOADS = "Videos_test"
PORTA = int(os.environ.get("PORT", 10000))

# --- Inicialização do app Flask ---
app = Flask(__name__)

# --- Garantir que a pasta de vídeos existe ---
os.makedirs(PASTA_DOWNLOADS, exist_ok=True)

# --- Rota inicial ---
@app.route("/")
def home():
    return "🎥 Servidor de Vídeos está Online!"

# --- Rota para servir vídeos publicamente ---
@app.route("/videos/<path:filename>")
def serve_video(filename):
    if ".." in filename or filename.startswith("/"):
        abort(400)  # evitar tentativa de acesso indevido
    caminho = os.path.join(PASTA_DOWNLOADS, filename)
    if not os.path.isfile(caminho):
        abort(404)
    return send_from_directory(PASTA_DOWNLOADS, filename)

# --- Rota para upload de vídeos via POST (usada pelo bot) ---
@app.route("/upload_video", methods=["POST"])
def upload_video():
    if "file" not in request.files:
        return jsonify({"error": "Arquivo não enviado"}), 400

    arquivo = request.files["file"]
    filename = arquivo.filename

    if not filename.lower().endswith(".mp4"):
        return jsonify({"error": "Apenas arquivos mp4 são aceitos"}), 400

    try:
        os.makedirs(PASTA_DOWNLOADS, exist_ok=True)
        destino = os.path.join(PASTA_DOWNLOADS, filename)
        arquivo.save(destino)
        print(f"✅ Vídeo salvo com sucesso: {destino}")
        return jsonify({"message": "Upload realizado com sucesso"}), 200
    except Exception as e:
        print(f"[❌] Erro ao salvar o vídeo: {e}")
        return jsonify({"error": "Erro interno ao salvar o vídeo"}), 500

# --- Execução ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORTA)
