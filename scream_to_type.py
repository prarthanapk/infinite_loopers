import sounddevice as sd
import numpy as np
import tkinter as tk
import threading
import time

# 🐔 Funny meme text (Cluck Norris story)
text = """Once upon a time in the town of Eggville, lived a chicken named Cluck Norris. Cluck wasn’t just any chicken — he wore sunglasses at night and had over 2 million followers on CluckTok.

But there was one thing Cluck had never done.

He had never crossed the road.

Every morning, he’d stare at it.
Every evening, he’d chicken out.

Until one dramatic Tuesday, Cluck stood at the edge and declared:

“TODAY… I CROSS!”

The townsfolk gathered. Even the cows brought popcorn.

He took one step.

A squirrel ran by and scared him. He screamed, laid an egg, and fainted.

He tried again. A leaf blew across the road. Another egg. More fainting.

After 17 failed attempts and 34 emergency omelets, Cluck had a revelation.

“Why cross the road… when I can order delivery?”

And so, the chicken never crossed the road.
But he did invent EggDash, the fastest omelet delivery service in history.

And that, children, is how laziness changed the world."""

# Globals
index = 0
volume_level = 0

# 🎨 Tkinter UI setup
root = tk.Tk()
root.title("Scream to Type 🎤")
root.geometry("800x600")
root.configure(bg="#3c112d")

message_label = tk.Label(root, text="Make some noise to start typing!", font=("Poppins", 16), bg="#38144a", fg="white")
message_label.pack(pady=10)

text_display = tk.Text(root, height=15, width=80, font=("Poppins", 12), bg="#D2BCD1", fg="black", wrap="word")
text_display.pack(pady=20)

volume_canvas = tk.Canvas(root, width=600, height=20, bg="#4F324E", highlightthickness=0)
volume_canvas.pack(pady=10)

# 🎤 Audio callback to calculate volume
def audio_callback(indata, frames, time_info, status):
    global volume_level
    if status:
        print(status)
    volume_norm = np.linalg.norm(indata) * 10
    volume_level = min(volume_norm, 1)  # Clamp to [0, 1]

# 🖋 Typing loop based on volume
def typing_loop():
    global index
    while index < len(text):
        vol = volume_level
        update_volume_meter(vol)
        if vol > 0.05:
            speed = 5 if vol > 0.3 else (2 if vol > 0.1 else 1)
            message_label.config(text="Yes! I hear your passion!")
            for _ in range(speed):
                if index < len(text):
                    text_display.insert(tk.END, text[index])
                    text_display.see(tk.END)
                    index += 1
        else:
            message_label.config(text="I can't hear your passion... scream louder!")
        time.sleep(0.05)

# 🎚 Update volume meter color
def update_volume_meter(vol):
    volume_canvas.delete("all")
    color = "red" if vol > 0.5 else ("yellow" if vol > 0.2 else "green")
    volume_canvas.create_rectangle(0, 0, vol * 600, 20, fill=color, outline="")

# 🎧 Start microphone stream in a separate thread
def start_audio():
    with sd.InputStream(callback=audio_callback, channels=1, samplerate=44100):
        typing_loop()

# Run audio processing in a thread so Tkinter doesn't freeze
threading.Thread(target=start_audio, daemon=True).start()

# Start Tkinter event loop
root.mainloop()
