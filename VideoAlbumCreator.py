import os
import time
from moviepy.editor import *
import dearpygui.core as dpg
import dearpygui.simple as sdpg
import tkinter as tk
from tkinter import filedialog
from mutagen.mp3 import MP3
from PIL import Image, ImageTk


mp3list = []
resultlist = []
lengthlist = []
videoduration = 0

tracklistWidth = 256

def AddMp3():
    global videoduration
    #global mp3list

    filenames = filedialog.askopenfilenames(title='Select Mp3s', filetypes=[
        (".mp3 files", "*.mp3"), 
        (".WAV files", "*.wav"),
        ("all files","*.*"),
        ])
    
    if not filenames:
        return
        #stops from throwing a "No filename found error"

    for filename in filenames:
    #if the file is a mp3
        audio = MP3(filename)
        mp3list.append(filename)
        videoduration += (audio.info.length)
        lengthlist.append(audio.info.length)
        print(str(len(mp3list)) + " audio objects in tracklist")
        print("video will be " + str(videoduration) + " seconds long")
        result = (os.path.basename(filename))
        resultlist.append(result.rsplit('.',1)[0])
        #mp3listbox(items = result.rsplit('.',1)[0])
        #dpg.configure_item("TracklistBox", items = result.rsplit('.',1)[0])
        #rsplit splits the '.mp3' from the filename 
    dpg.configure_item("##TracklistBox", items = resultlist)

def AddAlbumArt():
    global videoimage
    #get filepath for target image
    art_path = filedialog.askopenfilename(filetypes=((".jpg files", "*.jpg"),(".png files", "*.png"),("all files", "*.*")))
    #pass the  raw file path to the global for use in the video
    videoimage = art_path
    #Delete stock album art image and replace with loaded art file
    dpg.delete_item("AlbumArt")
    dpg.add_image("AlbumArt", art_path, before="Add Art", width=tracklistWidth, height=tracklistWidth)
    dpg.add_spacing(count = 10)
    print(art_path)


def createtracklist():
    #for each item in the listbox
    #write to text files
    #/n timestamp + ' - ' + trackname
    trackstart = 0
    trackindex = 0
    
    previousTrackLength = 0
    f = open("TracklistText.txt", "w")
    for x in mp3list:
        mp3 = MP3(x)
        trackindex += 1

        #Short Algo determines when the previous track ends and the next begins
        if previousTrackLength == 0:
            previousTrackLength = mp3.info.length
            trackstart = 0
        elif previousTrackLength != mp3.info.length:

            trackstart += previousTrackLength
            previousTrackLength = mp3.info.length
        
        #Determines whether or not the runtime is greater than an hour or not
        trackstring = time.gmtime(trackstart)
        if(trackstart < 3600):
            trackstringresult = time.strftime("%M:%S", trackstring)
        else:
            trackstringresult = time.strftime("%H:%M:%S", trackstring)
        #output = SongTitle (0:00)
        print(resultlist[trackindex - 1] + " " + "(" + str(trackstringresult) + ")")
        f.write(resultlist[trackindex - 1] + " " + "(" + str(trackstringresult) + ")\n" )

def upload():
    count = 0
    clipList = []
    audioclipList = []
    createtracklist()
    for mp3 in mp3list:
        count+=1

        audioclip = AudioFileClip(mp3list[count-1])
        #audioclip.set_duration
        audioclipList.append(audioclip)

        if count == len(mp3list):
            print(audioclipList)
            audioclipfinal = concatenate_audioclips(audioclipList)
            clip = ImageClip(videoimage)
            #clip.set_duration(videoduration)
            clip.audio = (audioclipfinal)     
            clip.set_duration(sum(lengthlist)).write_videofile("bigoutput.mp4",  fps=1)
        #yadda yadda yadda

def removemp3Entry():
    #print(dpg.get_value("##TracklistBox"))
    #remove index of listbox get_value from result list and mp3 list
    mp3list.pop(dpg.get_value("##TracklistBox"))
    resultlist.pop(dpg.get_value("##TracklistBox"))
    lengthlist.pop(dpg.get_value("##TracklistBox"))
    #then recreate the list box with configure item 
    dpg.configure_item("##TracklistBox", items = resultlist)
    print(str(sum(lengthlist)) + " sum of lengthlist")
    videoduration = sum(lengthlist)
    print(videoduration)


with sdpg.window("Video Album Generator", autosize=True, no_resize=True, x_pos=0,y_pos=0, no_collapse= True, no_close=True):
    #sdpg.show_style_editor()
    dpg.set_main_window_size(290,860)
    dpg.set_main_window_resizable(False)
    #dpg.add_spacing()
    dpg.set_main_window_title("IPRC VAG")
    dpg.add_image("Logo", "Logo.png")       
    #dpg.add_text("Tracklist")
    dpg.add_listbox(name ="##TracklistBox", width = tracklistWidth, num_items = 10)
    dpg.add_button("Add Audio", callback=AddMp3, width = tracklistWidth,tip="Select .mp3 files to use")
    dpg.add_button("Remove Audio",callback=removemp3Entry, width = tracklistWidth)
    dpg.add_spacing(count = 10)
    dpg.add_text("Album Art")
    dpg.add_image("AlbumArt", "Stock256.png")
    dpg.add_button("Add Art", width = tracklistWidth, callback=AddAlbumArt, tip= "Add/Change image file for album art")
    dpg.add_spacing(count = 10)
    dpg.add_button("Generate Video", width = tracklistWidth, callback=upload, height = 40, tip="Begin creating video album")

            #add_input_text("Input")
            #add_button("Check", callback=callbackbtn, callback_data="some data" )
            #add_button("Press me 2", callback=callback2, callback_data=lambda: get_value("Input")) # calls the lambda and sends result through
            #dpg.set_render_callback(self.__render)
    dpg.start_dearpygui()



