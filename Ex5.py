#importing the necessary libraries for using certain functions
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import subprocess
import os
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

def finalcut(file):
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

def codecs(file):
    video = file

    #these command lines gets the video codec of the file (v=0)
    command = "ffprobe -v error -select_streams v:0 -show_entries stream=codec_name " \
        "-of default=noprint_wrappers=1:nokey=1 " + video
    v_codec = subprocess.check_output(command, shell=True)  #necessary line for executing the command line
    v_codec = v_codec.decode("utf-8")

    #these command lines gets the audio codec of the file (a=0)
    command = "ffprobe -v error -select_streams a:0 -show_entries stream=codec_name " \
        "-of default=noprint_wrappers=1:nokey=1 " + video
    a_codec = subprocess.check_output(command, shell=True)  #necessary line for executing the command line
    a_codec = a_codec.decode("utf-8")

    #necessary for the "equals" inside the ifs
    v_codec = v_codec[:len(v_codec) - 1]
    a_codec = a_codec[:len(a_codec) - 1]

    #this ifs check first the kind of video codec and then the audio codec for being able to say with which the container is compatible
    if (v_codec == "mpeg2") or (v_codec == "h264"):
        if a_codec == "mp3":
            print("compatible with DVB, DTMB")
        if a_codec == "aac":
            print("compatible with DVB, ISDB, DTMB")
        if a_codec == "ac3":
            print("compatible with DVB, ATSC, DTMB")
    elif (v_codec == "avs") or (v_codec == "avs+"):
        if ((a_codec == "dra") or (a_codec == "aac")
                or (a_codec == "ac3") or (a_codec == "mp2") or (a_codec == "mp3")):
            print("compatible with DTMB")
    else:
        print("ERROR")  #prints error if it is not compatible with anyone

def main():
    container("bbb.mp4")    #just change here the name of the file
    codecs("finalcut.mp4")

main()
