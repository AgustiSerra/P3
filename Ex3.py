import os
import subprocess

#these command lines gets the video codec of the file (v=0)
command = "ffprobe -v error -select_streams v:0 -show_entries stream=codec_name " \
      "-of default=noprint_wrappers=1:nokey=1 " + "bbb.mp4"
v_codec = subprocess.check_output(command, shell=True)  #necessary line for executing the command line
v_codec = v_codec.decode("utf-8")

#these command lines gets the audio codec of the file (a=0)
command = "ffprobe -v error -select_streams a:0 -show_entries stream=codec_name " \
      "-of default=noprint_wrappers=1:nokey=1 " + "bbb.mp4"
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
