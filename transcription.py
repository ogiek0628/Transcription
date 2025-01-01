import os
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
import moviepy.editor as mp
import whisper
from tkinter import messagebox, Toplevel, Text, Scrollbar, END
import urllib.parse

def transcribe_video(video_path):
    try:
        # 動画ファイルの確認
        if not os.path.isfile(video_path):
            messagebox.showerror("Error", "File not found.")
            return

        # 保存ファイル名の設定
        audio_path = os.path.splitext(video_path)[0] + "_audio.mp3"
        transcription_file = os.path.splitext(video_path)[0] + "_transcription.txt"

        # 動画から音声を抽出
        label_status.config(text="Extracting audio...")
        video = mp.VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)

        # Whisperモデルをロード
        label_status.config(text="Loading Whisper model...")
        model = whisper.load_model("base")

        # 音声ファイルを文字起こし
        label_status.config(text="Transcribing audio...")
        result = model.transcribe(audio_path)
        transcription_text = result["text"]

        # 文字起こし結果を保存
        with open(transcription_file, "w", encoding="utf-8") as file:
            file.write(transcription_text)

        label_status.config(text="Transcription completed!")
        messagebox.showinfo("Success", f"Transcription saved to:\n{transcription_file}")

        # 文字起こし結果を表示
        show_transcription(transcription_text)

    except Exception as e:
        label_status.config(text="Error occurred.")
        messagebox.showerror("Error", str(e))

def show_transcription(text):
    """文字起こし結果を新しいウィンドウで表示"""
    transcription_window = Toplevel(app)
    transcription_window.title("Transcription Result")
    transcription_window.geometry("600x400")

    # テキストウィジェットとスクロールバー
    text_widget = Text(transcription_window, wrap="word", font=("Arial", 12))
    scrollbar = Scrollbar(transcription_window, command=text_widget.yview)
    text_widget.config(yscrollcommand=scrollbar.set)

    text_widget.insert(END, text)
    text_widget.config(state="disabled")  # 編集不可に設定
    text_widget.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

# ドラッグ＆ドロップされた動画ファイルを処理
def handle_drop(event):
    # パスをデコードして正規化
    video_path = urllib.parse.unquote(event.data.strip()).replace("{", "").replace("}", "")
    print(f"Normalized path: {video_path}")  # デバッグ用

    if os.path.isfile(video_path):
        print(f"Processing file: {video_path}")
        transcribe_video(video_path)
    else:
        print(f"Error: Invalid path: {video_path}")
        messagebox.showerror("Error", "Invalid file. Please drag and drop a valid video file.")

# GUI設定
app = TkinterDnD.Tk()  # TkinterDnDを使用したTkウィンドウ
app.title("Video Transcription Tool")
app.geometry("500x300")

label_instructions = tk.Label(app, text="Drag and drop your video file here:", font=("Arial", 14))
label_instructions.pack(pady=20)

# ドラッグ＆ドロップの対象ラベル
drop_label = tk.Label(app, text="Drop your video file here", bg="lightgray", relief="ridge", width=40, height=5)
drop_label.pack(pady=20)

# ステータスラベル
label_status = tk.Label(app, text="", font=("Arial", 12), fg="green")
label_status.pack(pady=10)

# ドラッグ＆ドロップ機能を有効化
drop_label.drop_target_register(DND_FILES)
drop_label.dnd_bind('<<Drop>>', handle_drop)

app.mainloop()
