import tkinter as tk
from tkinter import filedialog, messagebox
import os
import ffmpeg

def compress_video(input_path, output_path):
    try:
        # Resize video to 480p and re-encode with even dimensions
        (
            ffmpeg
            .input(input_path)
            .output(output_path, vf='scale=trunc(oh*a/2)*2:480', vcodec='libx264', acodec='aac', strict='experimental')
            .overwrite_output()
            .run()
        )
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Compression failed:\n{e}")
        return False

def select_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Video files", "*.mp4 *.mov *.avi *.mkv *.webm"), ("All files", "*.*")]
    )
    if file_path:
        input_var.set(file_path)

def compress():
    input_path = input_var.get()
    if not input_path or not os.path.exists(input_path):
        messagebox.showwarning("Warning", "Please select a valid video file.")
        return

    # Create output path
    base, ext = os.path.splitext(input_path)
    output_path = f"{base}_480p{ext}"

    # Compress the video
    success = compress_video(input_path, output_path)
    if success:
        messagebox.showinfo("Success", f"Video compressed successfully:\n{output_path}")

# GUI setup
root = tk.Tk()
root.title("Video Compressor to 480p")
root.geometry("500x150")
root.resizable(False, False)

input_var = tk.StringVar()

tk.Label(root, text="Input Video File:").pack(pady=5)
tk.Entry(root, textvariable=input_var, width=60).pack(pady=5)
tk.Button(root, text="Browse", command=select_file).pack(pady=5)
tk.Button(root, text="Compress to 480p", command=compress).pack(pady=10)

root.mainloop()
