from flask import Flask, request, send_from_directory, jsonify, abort
import os

app = Flask(__name__)
PASTA_DOWNLOADS = "Videos_test"

# Garante que PASTA_DOWNLOADS é um diretório
if os.path.exists(PASTA_DOWNLOADS):
    if not os.path.isdir(PASTA_DOWNLOADS):
        os.remove(PASTA_DOWNLOADS)
        os.makedirs(PASTA_DOWNLOADS)
else:
    os.makedirs(PASTA_DOWNLOADS)

@app.route("/")
def index():
    return jsonify({"status": "online", "message": "🟢 Servidor de vídeos online!"})

@app.route("/upload_video", methods=["POST"])
def upload_video():
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    arquivo = request.files["file"]
    if arquivo.filename == "":
        return jsonify({"error": "Nome de arquivo vazio"}), 400

    nome_seguro = os.path.basename(arquivo.filename)
    destino = os.path.join(PASTA_DOWNLOADS, nome_seguro)

    if os.path.exists(destino):
        return jsonify({"error": "Arquivo já existe no servidor"}), 409  # conflito

    try:
        arquivo.save(destino)
        return jsonify({"message": "Arquivo salvo com sucesso", "filename": nome_seguro}), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao salvar arquivo: {str(e)}"}), 500

@app.route("/videos/<path:filename>")
def acessar_video(filename):
    try:
        return send_from_directory(PASTA_DOWNLOADS, filename)
    except FileNotFoundError:
        return jsonify({"error": "Arquivo não encontrado"}), 404

@app.route("/delete_video/<path:filename>", methods=["DELETE"])
def delete_video(filename):
    nome_seguro = os.path.basename(filename)
    caminho = os.path.join(PASTA_DOWNLOADS, nome_seguro)

    if not os.path.exists(caminho):
        return jsonify({"error": "Arquivo não existe"}), 404

    try:
        os.remove(caminho)
        return jsonify({"message": f"Arquivo '{nome_seguro}' excluído com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao excluir arquivo: {str(e)}"}), 500

if __name__ == "__main__":
    # Pode ajustar porta e debug aqui
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), debug=True)
