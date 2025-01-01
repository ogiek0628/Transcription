import os
import shutil
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
import moviepy.editor as mp
import whisper
from tkinter import messagebox, Toplevel, Text, Scrollbar, END
import urllib.parse

def transcribe_video(video_path):
    try:
        if not os.path.isfile(video_path):
            messagebox.showerror("Error", "File not found.")
            return

        audio_path = os.path.splitext(video_path)[0] + "_audio.mp3"
        transcription_file = os.path.splitext(video_path)[0] + "_transcription.txt"

        label_status.config(text="Extracting audio...")
        video = mp.VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)

        label_status.config(text="Loading Whisper model...")
        model = whisper.load_model("base")

        label_status.config(text="Transcribing audio...")
        result = model.transcribe(audio_path)
        transcription_text = result["text"]

        with open(transcription_file, "w", encoding="utf-8") as file:
            file.write(transcription_text)

        label_status.config(text="Transcription completed!")
        messagebox.showinfo("Success", f"Transcription saved to:\n{transcription_file}")
        show_transcription(transcription_text)

    except Exception as e:
        label_status.config(text="Error occurred.")
        messagebox.showerror("Error", str(e))

def show_transcription(text):
    transcription_window = Toplevel(app)
    transcription_window.title("Transcription Result")
    transcription_window.geometry("600x400")

    text_widget = Text(transcription_window, wrap="word", font=("Arial", 12))
    scrollbar = Scrollbar(transcription_window, command=text_widget.yview)
    text_widget.config(yscrollcommand=scrollbar.set)

    text_widget.insert(END, text)
    text_widget.config(state="disabled")
    text_widget.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

def handle_drop(event):
    video_path = urllib.parse.unquote(event.data.strip()).replace("{", "").replace("}", "")
    if os.path.isfile(video_path):
        transcribe_video(video_path)
    else:
        messagebox.showerror("Error", "Invalid file. Please drag and drop a valid video file.")

def cleanup_virtual_environment():
    """仮想環境を削除する処理"""
    venv_path = os.path.join(os.getcwd(), 'venv')
    if os.path.exists(venv_path):
        try:
            shutil.rmtree(venv_path)
            print("仮想環境が正常に削除されました。")
        except Exception as e:
            print(f"仮想環境の削除中にエラーが発生しました: {e}")

def on_close():
    """ウィンドウを閉じる際の処理"""
    if messagebox.askokcancel("Quit", "アプリケーションを終了しますか？"):
        cleanup_virtual_environment()
        app.destroy()

app = TkinterDnD.Tk()
app.title("Video Transcription Tool")
app.geometry("500x300")

label_instructions = tk.Label(app, text="Drag and drop your video file here:", font=("Arial", 14))
label_instructions.pack(pady=20)

drop_label = tk.Label(app, text="Drop your video file here", bg="lightgray", relief="ridge", width=40, height=5)
drop_label.pack(pady=20)

label_status = tk.Label(app, text="", font=("Arial", 12), fg="green")
label_status.pack(pady=10)

drop_label.drop_target_register(DND_FILES)
drop_label.dnd_bind('<<Drop>>', handle_drop)

app.protocol("WM_DELETE_WINDOW", on_close)

app.mainloop()
