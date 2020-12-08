#importing the necessary libraries for using certain functions
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import subprocess
from pydub import AudioSegment
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
import ffmpeg

path = "/Users/agustiserra/Desktop/bbb.mp4"
ffmpeg_extract_subclip(path, 0, 60, targetname = "bbbcut.mp4")  #function that cuts the first minut of the video

command = "ffmpeg -i bbbcut.mp4 -ab 160k -ac 2 -ar 44100 -vn audiobbbcut.mp3"   #extraction of the audio of the video
subprocess.call(command, shell=True)    #necessary line for executing ffmpeg commands

#it sets just one channel for the extracted audio, converting it to mono
sound = AudioSegment.from_mp3("audiobbbcut.mp3")
sound = sound.set_channels(1)
sound.export("audiobbbcutmono.mp3", format="mp3")

# Read the audio file and set the sampling rate <default=44100>
song = AudioSegment.from_mp3("audiobbbcut.mp3").set_frame_rate(22050)
# Export the file by bitrate of 1k (lower bitrate)
song.export("audiobbbcutlowbr.mp3", format='mp3', bitrate='1k')

command2 = "ffmpeg -i bbbcut.mp4 -i Subtitles.srt -c copy -c:s mov_text bbbcutsub.mp4"  #adds the subtitltes from a .srt to the 1 min video
subprocess.call(command2, shell=True)

#saves the 2 audios into variables for a later sum
sound1 = AudioSegment.from_mp3("audiobbbcutlowbr.mp3")
sound2 = AudioSegment.from_mp3("audiobbbcutmono.mp3")

#adds dBs for hearing better the lower bitrate one
louder = sound1 + 6

#overlays the 2 audios creating just one with the combination of both
overlay = louder.overlay(sound2, position=0)
file_handle = overlay.export("mixaudios.mp3", format="mp3")

#replaces the original audio of the 1 min video with the mixed audio
command3 = "ffmpeg -i bbbcut.mp4 -i mixaudios.mp3 -c:v copy -map 0:v:0 -map 1:a:0 finalcutwithoutsubs.mp4"
subprocess.call(command3, shell=True)

#adds subtitles to the mixed audio 1 min video
command4 = "ffmpeg -i finalcutwithoutsubs.mp4 -i Subtitles.srt -c copy -c:s mov_text finalcut.mp4"
subprocess.call(command4, shell=True)
