import os
import moviepy.editor as mp
import whisper

ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}

# 許可されるファイル拡張子かどうかをチェック
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 動画ファイルから音声を抽出し、Whisperで文字起こしを行う
def transcribe_video(video_path):
    # 音声ファイルの保存パス
    audio_path = os.path.splitext(video_path)[0] + "_audio.mp3"
    transcription_file = os.path.splitext(video_path)[0] + "_transcription.txt"

    # 動画から音声を抽出
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

    # Whisper モデルをロードして文字起こし
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)

    return result