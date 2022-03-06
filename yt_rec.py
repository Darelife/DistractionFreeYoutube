import json
import requests
import time
import datetime
import os
from flask import Flask, render_template, request
from threading import Thread

api = "youtubev3_api"

#The developer variable is there to make sure that u don't use up those limited api calls while working on the project.
developer = True #It's a boolean value -> True or False
#developer = True #Developer mode
#developer = False #Client mode

# embed
# <iframe width="560" height="315" src="https://www.youtube.com/embed/{vid_Id}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
#You can play with the width and height though

# vid
# https://www.youtube.com/watch?v={vid_Id}

# to get channel_id
# content="vnd.youtube://www.youtube.com/channel/ - search this in the page source of channels page for channel_id

channelIdList = {
    "Mrbeast6000":"UCX6OQ3DkcsbYNE6H8uQQuVA",
    "Technoblade":"UCFAiFyGs6oDiF1Nf-rRJpZA",
    "Mrwhosetheboss":"UCMiJRAwDNSNzuYeN2uWa0pA",
    "Dave2D":"UCVYamHliCI9rw1tHR1xbkfw",
    "MKBHD":"UCBJycsmduvYEL83R_U4JriQ",
    "MarkRober":"UCY1kMZp36IQSyNx_9h4mpCg",
    # "LaterClips":"UCtVGGeUqfVHOK4Q6nAwYO3g",
    "Veritasium":"UCHnyfMqiRRG1u-2MsSQLbXA",
    # "Tom_Scott":"UCBa659QWEk1AI4Tg--mrJ2A"
}

vids = {}

def get_vids(channelId):
    url = f"https://www.googleapis.com/youtube/v3/search"
    API_KEY = api
    payload = {
        "key":API_KEY,
        "channelId":channelId,
        "part":"snippet,id",
        "order":"date",
        "maxResults":"20"
    }
    r = requests.get(url = url, params=payload)
    data = r.json()
    print(r.url)
    return data

if developer == False:
    for x in channelIdList:
        vids[x] = get_vids(channelIdList[x])
    with open("devdata.json", "w") as f:
        json.dump(vids, f, indent = 2)
elif developer == True:
    with open("devdata.json", "r") as f:
      vids = json.load(f)

vid = {}

for x in vids:
    currentTime = int(time.time())
    for i in (vids[x]["items"]):
        # print(i["snippet"]["title"])
        date = (i["snippet"]["publishTime"][:10])
        timestamp = (int(time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple())))
        if currentTime - timestamp < 604800:

            try:
                vid[x][i["snippet"]["title"]] = currentTime - timestamp
            except:
                vid[x] = {}
                vid[x][i["snippet"]["title"]] = currentTime - timestamp

if developer == False:
    with open("viddata.json", "w") as f:
        json.dump(vid, f, indent = 2)
elif developer == True:
    with open("viddatadev.json", "w") as f:
        json.dump(vid, f, indent = 2)

