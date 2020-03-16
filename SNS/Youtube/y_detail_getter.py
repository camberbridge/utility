# coding: utf8
import json, config
from datetime import datetime
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

def convert_to_datetime(datetime_str):
    tweet_datetime = datetime.strptime(datetime_str,'%Y-%m-%dT%H:%M:%S.000Z')
    return(tweet_datetime)

def search_video(y_iam, options, target=None):
    video_id = target if target else options.id
    videos_response = y_iam.videos().list(
        part="id,snippet,statistics", 
        id=video_id
    ).execute()
    videos = []

    for result in videos_response.get("items", []):
        videos.append("(%s) [%s] <%6s> %s" % (result["id"],
                                          result["snippet"]["channelId"],
                                          result["statistics"]["viewCount"],
                                          result["snippet"]["title"]))
    print("\n".join(videos), "\n")

def get_video_list(y_iam, options):
    search_response = y_iam.search().list(
        part=options.part,
        channelId=options.channel_id,
        maxResults=options.max_results,
        order=options.order,
        publishedAfter=options.published_after
    ).execute()

    videos = []
    now = datetime.now()

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            y_time = convert_to_datetime(search_result["snippet"]["publishedAt"])

            if y_time.year == now.time and y_time.month == now.month and y_time.day == now.day:
                print(search_result["snippet"]["title"],search_result["id"]["videoId"],search_result["snippet"]["publishedAt"])
            print(search_result["snippet"]["title"],search_video(y_iam=y_iam, options=None, target=search_result["id"]["videoId"]))

def get_comments(y_iam, options):
    print("get_comment")
    comments_res = y_iam.commentThreads().list(
        part="snippet, replies",
        videoId=options.id,
        maxResults=100,
        textFormat="plainText"
    ).execute()

    com_items = []
    while True:
        for result in comments_res.get("items", []):
            try:
                comment = result["snippet"]["topLevelComment"]["snippet"]["textOriginal"].replace("\n", "")
                com_items.append(comment)
                
                comment = result["replies"]["comments"]
                for c in comment:
                    comment = c["snippet"]["textOriginal"].replace("\n", "")
                    com_items.append(comment)
            except:
                pass

        if "nextPageToken" in comments_res:
            pageToken = comments_res["nextPageToken"]
            comments_res = y_iam.commentThreads().list(
                part="snippet,replies",
                videoId=options.id,
                textFormat="plainText",
                maxResults=100
            ).execute()
        else:
            break
    print(len(com_items))

def init():
    AT = config.Y_ACCESS_TOKEN
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=AT)

if __name__ == "__main__":
    y_iam = init()

    argparser.add_argument("--id", help="VideoIDs", default="Sq5QW3YqipM")
    argparser.add_argument("--part", help="Resource property", default="snippet")
    argparser.add_argument("--channel-id", help="Channel ID", default="UCrXUsMBcfTVqwAS7DKg9C0Q")
    argparser.add_argument("--max-results", help="Result max num", default=50)
    argparser.add_argument("--order", help="Sort method", default="date")
    argparser.add_argument("--published-after", help="Date time", default="2019-09-01T00:00:00Z")
    args = argparser.parse_args()

    try:
        #search_video(y_iam, args)
        #get_video_list(y_iam, args)
        get_comments(y_iam, args)
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
