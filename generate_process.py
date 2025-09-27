import os
from text_to_audio import text_to_speech_file
import time
from moviepy_reel_generator import create_reel


def text_to_audio(folder):
    print("TTA - ", folder)
    with open(f"user_uploads/{folder}/desc.txt") as f:
        text = f.read()
    print(text, folder)     
    text_to_speech_file(text, folder)

# def create_reel(folder):
#     command=""
#     print("CR - ", folder)


if __name__ == "__main__":
    while True:
        print("Processing queue...")
        with open("done.txt", 'r') as f:
            done_folder = f.readlines()

        done_folder = [f.strip() for f in done_folder]
        folders = os.listdir("user_uploads")
        for folder in folders:    
            if folder not in done_folder:
                text_to_audio(folder) # Generate the audio.mp3 from desc.txt
                create_reel(folder) # Generate reel with the images and audio.mp3 in the folder
                with open("done.txt", "a") as f:
                    f.write(folder + "\n")
        time.sleep(4)                