# DistractionFreeYoutube
Made it to avoid getting distracted by youtube vids.

# Webpages
video_id -> The id of the video at the end of the url <br>
Eg: In, "https://www.youtube.com/watch?v=abcdefghijk" video_id = "abcdefghijk"<br>
    Or In, "https://youtu.be/abcdefghijk", video_id = "abcdefghijk"

* ### Home Page (/):
    Has a video which you can set using (/set?s={video_id}). The default video is a "study with me" video by "Merve"
* ### Single yt vid (/yt?s={video_id}) :
    If you just happened to receive a particular videos link, and want to watch it without going to the youtube website, you can use this webpage.
* ### Set default video (/set?s={video_id}) :
    If you want to set a different video for your home page, you can use this. It saves the `video_id` in your cookies folder.
* ### Selected content creators (uploaded in the last week only) (/youtube) :
    If you want to watch vids by only some content creators, you will need to edit the dictionary `channelIdList`, in `yt_rec.py`. The steps to get the `channel id's` is in the comments above it. It only shows the videos uploaded by the content creators specified, in the last week.

# Setup
Need to finish writing this part
### **(Required)** Api Key
* Go to `https://console.cloud.google.com/apis/api/youtube.googleapis.com` ,and click on "enable", ![click on "Enable" to enable the YouTube Data API v3](https://github.com/Darelife/DistractionFreeYoutube/blob/main/readmeFiles/enableYoutubeAPI.png) You will then be redirected to a page.
* Go to the credentials tab ![It's below the API info]().
* Create an API KEY
* Place the value of the API in the line below the "importing lines" in `yt_rec.py` in place of the `api` variable. It's a string.
### (optional) Set default home page video
Explained in [the HOMEPAGE subheading in Webpages](###-Home-Page-(/):)
### (optional) If you want to get the limited videos uploaded by your selected content creators