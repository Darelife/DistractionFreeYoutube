"""
MIT License

Copyright (c) 2022 itzp

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json
import requests
import time
import datetime
import os
from flask import Flask, render_template, request, make_response
from threading import Thread

api : str = "youtubev3_api"

#The developer variable is there to make sure that u don't use up those limited api calls while working on the project.
developer :bool = True #It's a boolean value -> True or False
#developer = True #Developer mode
#developer = False #Client mode

# embed
# <iframe width="560" height="315" src="https://www.youtube.com/embed/{vid_Id}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
#You can play with the width and height though

# vid
# https://www.youtube.com/watch?v={vid_Id}

# to get channel_id
# content="vnd.youtube://www.youtube.com/channel/ - search this in the page source of channels page for channel_id

channelIdList :dict = {
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

vids :dict = {}

def get_vids(channelId, API_KEY):
    url = f"https://www.googleapis.com/youtube/v3/search"
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

def time_check(timestamp):
    timestamp_now = int(time.time())
    if timestamp_now - timestamp > 604800: #7 days in seconds
        return True
    else:
        return False

def current_time():
  now = datetime.datetime.now()
  time_change = datetime.timedelta(hours=5, minutes=30)
  now += time_change
  current_time = now.strftime("%d-%m-%Y, %H:%M:%S")
  return current_time

# API_KEY = os.environ['API_KEY']
# username = "markrober"
def get_channel_id(username, API_KEY): 
    """
    i might have been entering the wrong usernames or something
    but, this thing only works half of the time
    """
    url = f"https://www.googleapis.com/youtube/v3/channels"   
    payload = {"forUsername":username, "part":"id,snippet", "key":API_KEY}
    channel_id_request = requests.get(url = url, params = payload)
    data = channel_id_request.json()
    channel_id = (data["items"][0]["id"])
    return channel_id

# usernameSearchList = {"Mrbeast6000":"UCX6OQ3DkcsbYNE6H8uQQuVA","Technothepig":"UCFAiFyGs6oDiF1Nf-rRJpZA", "mrwhosetheboss":"", "Dave2D":"UCVYamHliCI9rw1tHR1xbkfw","mkbhd", "markrober","Laterclips"}



channelIdList : dict = {
    "Mrbeast6000":"UCX6OQ3DkcsbYNE6H8uQQuVA",
    "Colin&Samir":"UCamLstJyCa-t5gfZegxsFMw",
    "AliAbdaal":"UCoOae5nYA7VqaXzerajD0lg",
    "Technoblade":"UCFAiFyGs6oDiF1Nf-rRJpZA",
    "Mrwhosetheboss":"UCMiJRAwDNSNzuYeN2uWa0pA",
    "MKBHD":"UCBJycsmduvYEL83R_U4JriQ",
    "SochByMohakMangal":"UCz4a7agVFr1TxU-mpAP8hkw",
    "CorridorCrew":"UCSpFnDQr88xCZ80N-X7t0nQ",
    "MarkRober":"UCY1kMZp36IQSyNx_9h4mpCg",
    "Veritasium":"UCHnyfMqiRRG1u-2MsSQLbXA"
}

# channelIdList = {
#     # "Mrbeast6000":"UCX6OQ3DkcsbYNE6H8uQQuVA"
#     # "Technoblade":"UCFAiFyGs6oDiF1Nf-rRJpZA",
#     "Mrwhosetheboss":"UCMiJRAwDNSNzuYeN2uWa0pA"
#     # "Dave2D":"UCVYamHliCI9rw1tHR1xbkfw",
#     # "MKBHD":"UCBJycsmduvYEL83R_U4JriQ",
#     # "MarkRober":"UCY1kMZp36IQSyNx_9h4mpCg",
#     # "LaterClips":"UCtVGGeUqfVHOK4Q6nAwYO3g"
# }
app :Flask= Flask('')

#vids dictionary's values
if developer == True:
  with open("test.json", "r") as f:
      vids = json.load(f)
if developer == False:
  for i in channelIdList:
      # global vids
      vid = []
      data = get_vids(channelIdList[i], api)
      with open("data.json", "w") as f:
        json.dump(data, f, indent = 2)
      index = 0
      for x in data["items"]:
          time_reg = list((x["snippet"]["publishedAt"])[:10].split("-"))
          dt = datetime.datetime(int(time_reg[0]), int(time_reg[1]), int(time_reg[2]))
          timestamp = int(dt.replace().timestamp())
          if time_check(timestamp) == True:
              break
          
          vid.append([x["id"]["videoId"],timestamp])
          index += 1
      print(type(vid))
      print(str(i))
      vids[i] = vid
  with open("test.json", "w") as f:
    json.dump(vids, f, indent = 2)

@app.route('/')
def study():
  try:
    id = request.cookies.get('defaultVideoId')
    if id == None:
      id = "3f1ShNU877I"
  except: id = "3f1ShNU877I"
  embeds = f'<iframe width="940" height="500" src="https://www.youtube.com/embed/{id}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
  return render_template('yt.html', embeds = embeds)


@app.route('/yt', methods=['GET'])
def search():
    id = request.args.get("s")
    embeds = f'<iframe width="940" height="500" src="https://www.youtube.com/embed/{id}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
    print(id)
    return render_template('yt.html', embeds = embeds)

@app.route('/set', methods=['GET'])
def set():
    # global defaultVideoId
    id = request.args.get("s")
    defaultVideoId = id
    embeds = f'<iframe width="940" height="500" src="https://www.youtube.com/embed/{defaultVideoId}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
    resp = make_response(render_template('yt.html', embeds = embeds))
    resp.set_cookie('defaultVideoId',id) 
    return resp


@app.route('/youtube')
def home_dev():
  embeds = ""
  i = 0
  for x in vids:
    if len(vids[x]) != 0:
      for y in vids[x]:
        i += 1
        embeds += f'<iframe width="940" height="500" src="https://www.youtube.com/embed/{y[0]}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
        if i%1==0:
          embeds += "<br>"
  try:
    # print(jsonify({'ip': request.remote_addr}))
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
      print(request.environ['REMOTE_ADDR'])
    else:
      print(request.environ['HTTP_X_FORWARDED_FOR'])
  except: print("it didn't work")

  return render_template('yt.html', embeds = embeds)


def run():
    app.run(host="0.0.0.0", port=8080)

server = Thread(target=run)
server.start()
if __name__ == '__main__':
    app.run()
        