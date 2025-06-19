from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/videos/<path:filename>')
def get_video(filename):
    return send_from_directory('videos', filename)

@app.route('/')
def home():
    return '✅ Servidor de vídeos está no ar!'

if __name__ == '__main__':
    app.run()
