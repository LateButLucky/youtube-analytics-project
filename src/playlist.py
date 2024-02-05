import os
import datetime
import isodate
from googleapiclient.discovery import build


class PlayList:

    def __init__(self, playlist_id):
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.playlist_id = playlist_id
        self.playlist_info = youtube.playlists().list(id=playlist_id, part='contentDetails, snippet').execute()
        self.playlist_videos = youtube.playlistItems().list(playlistId=playlist_id, part='contentDetails, snippet',
                                                            maxResults=50).execute()
        video_ids = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        video_response = youtube.videos().list(part='contentDetails,statistics', id=','.join(video_ids)).execute()
        self.video_response = video_response
        self.title = self.playlist_info['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @property
    def total_duration(self):
        total_duration_playlist = datetime.timedelta()
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration_playlist += datetime.timedelta(seconds=duration.total_seconds())
        print(total_duration_playlist)
        return total_duration_playlist

    def show_best_video(self):
        max_like_count = 0
        best_video_url = ''
        for video in self.video_response['items']:
            like_count = int(video['statistics'].get('likeCount', 0))
            if like_count > max_like_count:
                max_like_count = like_count
                best_video_url = video['id']
        print(f"https://youtu.be/{best_video_url}")
        return f"https://youtu.be/{best_video_url}"
