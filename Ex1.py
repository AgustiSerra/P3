from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import subprocess
from pydub import AudioSegment
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
import ffmpeg

ffmpeg_extract_subclip("bbb.mp4", 0, 60, targetname = "bbbcut.mp4")

command = "ffmpeg -i bbbcut.mp4 -ab 160k -ac 2 -ar 44100 -vn audiobbbcut.mp3"
subprocess.call(command, shell=True)

sound = AudioSegment.from_mp3("audiobbbcut.mp3")
sound = sound.set_channels(1)
sound.export("audiobbbcutmono.mp3", format="mp3")

#path = "file's path"
# Read the audio file and set the sampling rate <default=44100>
song = AudioSegment.from_mp3("audiobbbcut.mp3").set_frame_rate(22050)
# Export the file to the specified path by bitrate of 32k, here is to directly overwrite the original file.
song.export("audiobbbcutlowbr.mp3", format='mp3', bitrate='1k')

command2 = "ffmpeg -i bbbcut.mp4 -i Subtitles.srt -c copy -c:s mov_text bbbcutsub.mp4"
subprocess.call(command2, shell=True)

sound1 = AudioSegment.from_mp3("audiobbbcutlowbr.mp3")
sound2 = AudioSegment.from_mp3("audiobbbcutmono.mp3")

louder = sound1 + 6

overlay = louder.overlay(sound2, position=0)
file_handle = overlay.export("mixaudios.mp3", format="mp3")

command3 = "ffmpeg -i bbbcut.mp4 -i mixaudios.mp3 -c copy finalcutwithoutsubs.mp4"
subprocess.call(command3, shell=True)

command4 = "ffmpeg -i finalcutwithoutsubs.mp4 -i Subtitles.srt -c copy -c:s mov_text finalcut.mp4"
subprocess.call(command4, shell=True)
