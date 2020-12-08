#importing the necessary libraries for using certain functions
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import subprocess
from pydub import AudioSegment
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
import ffmpeg

def cut_video(file):
    video = file
    ffmpeg_extract_subclip(video, 0, 60, targetname = "cut.mp4")  #function that cuts the first minut of the video

def extract_audio(file):
    command = "ffmpeg -i cut.mp4 -ab 160k -ac 2 -ar 44100 -vn audiocut.mp3"   #extraction of the audio of the video
    subprocess.call(command, shell=True)    #necessary line for executing ffmpeg commands

def monoaudio(file):
    sound = AudioSegment.from_mp3("audiocut.mp3")
    sound = sound.set_channels(1)
    sound.export("audiocutmono.mp3", format="mp3")

def lowerbitrate(file):
    # Read the audio file and set the sampling rate <default=44100>
    song = AudioSegment.from_mp3("audiocut.mp3").set_frame_rate(22050)
    # Export the file by bitrate of 1k (lower bitrate)
    song.export("audiocutlowbr.mp3", format='mp3', bitrate='1k')

def subs(file):
    command2 = "ffmpeg -i cut.mp4 -i Subtitles.srt -c copy -c:s mov_text cutsub.mp4"  #adds the subtitltes from a .srt to the 1 min video
    subprocess.call(command2, shell=True)

def mixaudios(file1, file2):
    #saves the 2 audios into variables for a later sum
    sound1 = AudioSegment.from_mp3("audiocutlowbr.mp3")
    sound2 = AudioSegment.from_mp3("audiocutmono.mp3")

    #adds dBs for hearing better the lower bitrate one
    louder = sound1 + 6

    #overlays the 2 audios creating just one with the combination of both
    overlay = louder.overlay(sound2, position=0)
    file_handle = overlay.export("mixaudios.mp3", format="mp3")

def add_mixaudios(file1, file2):
    #replaces the original audio of the 1 min video with the mixed audio
    command3 = "ffmpeg -i cut.mp4 -i mixaudios.mp3 -c:v copy -map 0:v:0 -map 1:a:0 finalcutwithoutsubs.mp4"
    subprocess.call(command3, shell=True)

def finalcut(file1):
    #adds subtitles to the mixed audio 1 min video
    command4 = "ffmpeg -i finalcutwithoutsubs.mp4 -i Subtitles.srt -c copy -c:s mov_text finalcut.mp4"
    subprocess.call(command4, shell=True)

def container(file):
    video = file

    #calling the previous functions for obtaining the finalcut (mp4 container)
    cut_video(video)
    extract_audio("cut.mp4")
    monoaudio("audiocut.mp3")
    lowerbitrate("audiocut.mp3")
    subs("cut.mp4")
    mixaudios("audiocutlowbr.mp3", "audiocutmono.mp3")
    add_mixaudios("cut.mp4", "finalcutwithoutsubs.mp4")
    finalcut("finalcutwithoutsubs.mp4")

container("bbb.mp4")    #just change here the name of the file
