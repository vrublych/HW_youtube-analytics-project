import os
import isodate
from datetime import timedelta
from googleapiclient.discovery import build

api_key: str = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)

class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        playlists = youtube.playlists().list(id=self.playlist_id, part='contentDetails,snippet', maxResults=50).execute()
        self.title = playlists['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        self.video_response = self.get_video_response()

    def get_video_response(self):
        """
        Получение информации о видео в плейлисте.
        """
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,part='contentDetails',maxResults=50).execute()
        video_ids = [
            video['contentDetails']['videoId']
            for video in playlist_videos.get('items', [])
        ]
        video_response = []
        if video_ids:
            video_response = youtube.videos().list(
                part='contentDetails,statistics',
                id=','.join(video_ids)
            ).execute().get('items', [])
        return video_response

    @property
    def total_duration(self):
        """
        Вычисление общей продолжительности видео в плейлисте.
        """
        durations = (
            isodate.parse_duration(video['contentDetails']['duration'])
            for video in self.video_response
        )
        total_duration = sum(durations, timedelta())
        return total_duration

    def show_best_video(self):
        """
        Возвращает ссылку на видео с наибольшим количеством лайков.
        """
        max_likes = 0
        best_video = None
        for video in self.get_video_response():
            likes = int(video['statistics']['likeCount'])
            if likes > max_likes:
                max_likes = likes
                best_video = video
        if best_video is not None:
            return f"https://youtu.be/{best_video['id']}"
