import os
from flask import Flask, render_template, request, send_file, jsonify
from flask_cors import CORS
import moviepy.editor as mp
import whisper
from werkzeug.utils import secure_filename


app = Flask(__name__)
CORS(app)


# 動画ファイルのアップロード先
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'mov', 'avi', 'mkv'}


# 許可される拡張子を確認する関数
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# 動画の文字起こし処理する関数
def transcribe_video(video_path):
    audio_path = os.path.splitext(video_path)[0] + "_audio.mp3"
    transcription_file = os.path.splitext(video_path)[0] + "_transcription.txt"

    # 動画から音声を抽出、文字起こししてファイルに保存
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    transcription_text = result["text"]
    with open(transcription_file, "w", encoding="utf-8") as file:
        file.write(transcription_text)
    
    return transcription_file


# ホームページ（ファイルアップロードフォーム）
@app.route('/')
def index():
    return render_template('index.html')


# 動画ファイルをアップロードして文字起こしする関数
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # 文字起こし処理し、ダウンロード用のリンクを表示
        transcription_file = transcribe_video(file_path)
        return jsonify({"message": "Transcription completed", "transcription_file": transcription_file})

    return jsonify({"error": "Invalid file format"}), 400


# 文字起こしファイルをダウンロード
@app.route('/download/<filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
