#YouTube Data Scraping using YouTube Data API
import json
import urllib.request

import pandas as pd
import os

#This API KEY will not work for you. 
#Go to https://console.developers.google.com/ and sign in with your mail id and click on 'create project'
#Now click on 'create credentials' and then click on 'API KEY'. Copy & Paste the API KEY below in place of my API KEY
api_key = 'AIzaSyC-YxJcWp2rdkt4m8qmZ3vR4l_AFTfTqo0'

df = pd.read_csv(os.path.join('Youtube URLs.csv'))

def extract_id(url: str):
    return url[url.index('=')+1:]

video_ids = []
for url in list(df['YoutubeURL']):
    video_ids.append(extract_id(url))
df["video_ids"] = video_ids

Views = []
Likes = []
Dislikes = []
Comments = []
Title = []
uploadDate = []

def extract_views(data):
    return int(data['items'][0]['statistics']['viewCount'])

def extract_likes(data):
    return int(data['items'][0]['statistics']['likeCount'])

def extract_dislikes(data):
    return int(data['items'][0]['statistics']['dislikeCount'])

def extract_date(data):
    return data['items'][0]['snippet']['publishedAt'][:data['items'][0]['snippet']['publishedAt'].index('T')]

def extract_comments(data):
    try:
        return int(data['items'][0]['statistics']['commentCount'])
    except:
        return 'comments section is disabled'
    
def extract_title(data):
    return data['items'][0]['snippet']['title']

for link_id in df['video_ids']:
    video_id = link_id
    api_url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={api_key}&part=snippet,statistics&fields=items(id,snippet,statistics)'
    json_url = urllib.request.urlopen(api_url)
    data = json.loads(json_url.read())
    Views.append(extract_views(data))
    Likes.append(extract_likes(data))
    Dislikes.append(extract_dislikes(data))
    Comments.append(extract_comments(data))
    uploadDate.append(extract_date(data))
    Title.append(extract_title(data))   

df['Title'] = Title
df['Upload Date'] = uploadDate
df['Views'] = Views
df['Likes'] = Likes
df['Dislikes'] = Dislikes
df['No. of Comments'] = Comments

df.index += 1
Output_data=df.drop('video_ids',axis=1)
Output_data.to_csv('Extracted YouTube Data.csv',index=False)