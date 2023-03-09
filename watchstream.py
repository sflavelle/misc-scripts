#!/usr/bin/python3

import requests
import streamlink
import yt_dlp
from yt_dlp.utils import DateRange
from datetime import date, datetime, timedelta
import inquirer
from rofi import Rofi
import os
import sys

# Load list of streams to watch
streamlist = []

r = Rofi()
tty = False
today = date.today()
yesterday = today - timedelta(days=1)
ydl_opts = {
        'lazy_playlist': True,
        'quiet': True,
        'simulate': True,
        'playlist_items': '1',
        'daterange': DateRange(yesterday.strftime("%Y%m%d"), today.strftime("%Y%m%d"))
        }


twitchlink = "https://twitch.tv/{}"
youtubelink = "https://youtube.com/{}"
ytvodlink = "https://youtube.com/{}/videos"

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
        case 'ytvod':
            # For a VOD, we fake a 'live' check by instead
            # Returning a video from today
            check = None
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                check = ydl.extract_info(ytvodlink.format(link[1]), download=False)
            if bool(check['entries'][0]):
                streamlist.append(ytvodlink.format(link[1]))
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

url = None
if "/videos" in str(selectedstream['live']):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(str(selectedstream['live']), download=False)
        url = meta['entries'][0]['webpage_url']
        print(url)
    os.execl('/usr/bin/mpv', 'mpv', url)
else:
    os.execl('/usr/bin/streamlink', 'streamlink', str(selectedstream['live']), '720p,480p,best')
