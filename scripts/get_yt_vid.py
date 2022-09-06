# Imports
import urllib.request
import pytube
from pytube import YouTube

# Where Save Videos
save_path = '/Users/ckg-files/Music/YouTube-Music'

# Get Video & Art
# link of the video to be downloaded 
link = input("Paste Link Here- ")

try:
    # Instantiate YouTube Object with each link
    yt = YouTube(link) 

except:
    print("CONNECTION ERROR!!!  \n \n \n ") #to handle exception 


# Music File Name
define_filename = input("Set Filename Manually? (Y/N)- ")

if define_filename != "N":
    name_to_save = input("What title would you like to save as? (without extension)\n--> ")
    yt.title = name_to_save


# Title from YT
vid_title = yt.title

#l = yt.vid_info
#vid_thumbnail = yt.thumbnail_url

#yt.streams.filter(only_audio=True) #To check diff file formats (Variety of kbs & mp4 or webms)


try:
    # Itags & Corresponding Extension (see git for full list)
    # GitHub Page- https://gist.github.com/sidneys/7095afe4da4ae58694d128b1034e01e2
    # 251 = .webm (Generally Works)
    # 37 = .mp4 (1080p)
    # 136 = .mp4 (780p)
    
    vid = yt.streams.get_by_itag(136)
    vid.download(save_path)

    print("File Saved Successfully! \n\n")

except:
    print("File not saved") 
    pass


# setting filename and image URL
filename = f"{vid_title} -- Album Art"

# calling urlretrieve function to get thumbnail art
#urllib.request.urlretrieve(vid_thumbnail, save_path+filename)
#urllib.request.urlretrieve(vid_thumbnail, f'/Users/ckg-files/Music/Album Art/{filename}') # old method


