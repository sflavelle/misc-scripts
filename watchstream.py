#!/usr/bin/python3

import requests
import streamlink
import inquirer
from rofi import Rofi
import os
import sys

# Load list of streams to watch
streamlist = []

r = Rofi()
tty = False

twitchlink = "https://twitch.tv/{}"
youtubelink = "https://youtube.com/{}"

conf = open("/home/lily/.config/livestreams.conf", "r")
if sys.stdin and sys.stdin.isatty():
    tty = True
    print("Seeing who's live...")
else:
    r.status("Seeing who's live, please wait...")
for l in conf:
    link = l.split(" ")
    link[1] = link[1].strip()
    match link[0]:
        case 'twitch':
            check = streamlink.streams(twitchlink.format(link[1]))
            if bool(check):
                streamlist.append(twitchlink.format(link[1]))
        case 'youtube':
            check = streamlink.streams(youtubelink.format(link[1]))
            if bool(check):
                streamlist.append(youtubelink.format(link[1]))
# Select from List
if sys.stdin and sys.stdin.isatty():
    # Running in a terminal, use inquirer
    livestreams = [
        inquirer.List('live',
                      message="Here's who's live right now. Pick one to watch",
                      choices=streamlist,
                      ),
        ]

    selectedstream = inquirer.prompt(livestreams)
else:
    selectedstream,selectedindex = r.select('Pick a live stream to watch:', streamlist)

if tty:
    os.execl('/usr/bin/streamlink', 'streamlink', str(selectedstream['live']), '720p,480p,best')
else:
    os.spawnl('/usr/bin/streamlink', 'streamlink', str(selectedstream['live']), '720p,480p,best')
