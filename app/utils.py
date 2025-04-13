import os
import moviepy.editor as mp
import whisper
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
    
    # 保存先のパスを作成
    audio_path = os.path.join(upload_folder, filename_without_extension + "_audio.mp3")
    transcription_file = os.path.join(upload_folder, filename_without_extension + "_transcription.txt")

    # 動画から音声を抽出（音声のみを抽出して保存）
    video = mp.VideoFileClip(video_path)
    audio = video.audio

    # 音声をMP3形式で保存
    audio.write_audiofile(audio_path, codec='mp3', ffmpeg_params=["-q:a", "0"])

    # Whisper モデルをロードして文字起こし
    model = whisper.load_model("base")  # "base" モデルは、処理が速くて高精度
    result = model.transcribe(audio_path)

    # 文字起こし結果をファイルに保存
    with open(transcription_file, "w", encoding="utf-8") as f:
        f.write(result["text"])

    # 保存したファイルのパスを返す
    return transcription_file
