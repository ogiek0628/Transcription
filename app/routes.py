from flask import Blueprint, render_template, request, jsonify, send_file, current_app
from werkzeug.utils import secure_filename
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
            transcription_filename = os.path.basename(transcription_file)

            return jsonify({
                "message": "Transcription completed",
                "transcription_file": transcription_filename 
            })

    except RequestEntityTooLarge:
        return jsonify({"error": "File is too large. The maximum allowed size is 200MB."}), 413



@main.route('/download/<filename>')
def download_file(filename):
    try:
        # ファイルのフルパスを作成
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        print(f"File path: {file_path}")

        # ファイルが存在するか確認してから送信し、ダウンロード後にファイル削除
        if os.path.exists(file_path):
            response = send_file(file_path, as_attachment=True)
            
            video_file_path = file_path.replace("_transcription.txt", ".mp4")  # 動画ファイルのパス
            audio_file_path = video_file_path.replace(".mp4", "_audio.mp3")  # 音声ファイルのパス

            os.remove(file_path)  # テキストファイル
            os.remove(audio_file_path)  # 音声ファイル
            os.remove(video_file_path)  # 動画ファイル
            
            print(f"Deleted files: {file_path}, {audio_file_path}, {video_file_path}")
            return response
        else:
            return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

