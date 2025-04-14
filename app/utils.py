import os
import subprocess
import whisper
from io import BytesIO
from flask import current_app

ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}

# 許可されるファイル拡張子かどうかをチェック
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 動画ファイルから音声を抽出し、Whisperで文字起こしを行う
def transcribe_video(video_path):
    # 動画ファイル名を取得
    filename_without_extension = os.path.splitext(os.path.basename(video_path))[0]  # 拡張子を取り除いたファイル名

    # Flaskの設定からUPLOAD_FOLDERを取得し、保存先を決定
    upload_folder = current_app.config['UPLOAD_FOLDER']
    
    # メモリ内のバッファに音声データを保存
    audio_buffer = BytesIO()

    try:
        # ffmpegを使用して音声をメモリに抽出
        command = [
            'ffmpeg', 
            '-i', video_path,  # 入力ファイル
            '-vn',             # 動画を無視
            '-acodec', 'libmp3lame',  # MP3形式で音声を保存
            '-ar', '44100',    # サンプリングレート
            '-ac', '2',        # ステレオ
            '-ab', '192k',     # ビットレート
            '-f', 'mp3',       # 出力形式
            'pipe:1'           # 標準出力に出力
        ]
        
        # subprocessでffmpegを実行し、音声データをメモリに保存
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        audio_buffer.write(process.stdout.read())  # 音声データをバッファに保存
        process.stdout.close()
        process.wait()  # コマンドが完了するまで待機

        # Whisper モデルをロードして文字起こし
        model = whisper.load_model("base")
        result = model.transcribe(audio_buffer)  # メモリ内の音声データを直接処理

        # 文字起こし結果をファイルに保存
        transcription_file = os.path.join(upload_folder, filename_without_extension + "_transcription.txt")
        with open(transcription_file, "w", encoding="utf-8") as f:
            f.write(result["text"])

    except Exception as e:
        print(f"Error occurred: {e}")
        raise e  # エラーを再スローして上位で処理させる

    # 文字起こしファイルのパスを返す
    return transcription_file
