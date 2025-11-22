import os
import subprocess
from create_audio import convert_text_to_speech
import time

def create_audio(folder):
   print("Creating Audio for folder: ", folder)
   with open(f"user_uploads/{folder}/description.txt") as f:
      text = f.read()
   print(text, folder)
   convert_text_to_speech(text, folder)
   print("Audio file generated")


def create_reel(folder):
      print("Creating reel for folder: ", folder)
      command = f'''ffmpeg -f concat -safe 0 -i user_uploads/{folder}/input.txt -i user_uploads/{folder}/audio.wav -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p static/reels/{folder}.mp4'''
      subprocess.run(command, shell = True, check = True)
      print("Video file generated")


if __name__ == "__main__":
   while True:
      print("Generating New Reels...")
      with open("reels_info.txt", "r") as f:
         folders_completed = f.readlines()

      folders_completed = [f.strip() for f in folders_completed]
      print("Folders completed: ", folders_completed)
      folders = os.listdir("user_uploads")
      for folder in folders:
         if folder not in folders_completed:
            # Convert audio from text
            create_audio(folder)

            # Create Reel using audio and images
            create_reel(folder)

            with open("reels_info.txt", "a") as f:
                  f.write(folder + "\n")
      
      time.sleep(5)