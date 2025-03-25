from flask import Blueprint, render_template, request, jsonify, send_file, current_app
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os
from .utils import allowed_file, transcribe_video

# Blueprintの作成
main = Blueprint('main', __name__)

# ホームページ
@main.route('/')
def index():
    return render_template('index.html')

# ファイルアップロードと文字起こし処理
@main.route('/upload', methods=['POST'])
def upload_file():
    try:
        # アップロード処理
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if file and allowed_file(file.filename):
            # アップロードファイルの保存
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # 文字起こし処理
            transcription_file = transcribe_video(file_path)

            return jsonify({"message": "Transcription completed", "transcription_file": transcription_file})

    except RequestEntityTooLarge:
        return jsonify({"error": "File is too large. The maximum allowed size is 200MB."}), 413

# 文字起こしファイルのダウンロード
@main.route('/download/<filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)
