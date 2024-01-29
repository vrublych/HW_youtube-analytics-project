import isodate
from datetime import timedelta
from src.channel import Channel

youtube = Channel.get_service()

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
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id, part='contentDetails', maxResults=50).execute()
        video_ids = [video['contentDetails']['videoId'] for video in playlist_videos.get('items', [])]
        video_response = []
        if video_ids:
            video_response = youtube.videos().list(part='contentDetails,statistics', id=','.join(video_ids)).execute().get('items', [])
        return video_response

    @property
    def total_duration(self):
        """
        Вычисление общей продолжительности видео в плейлисте.
        """
        return sum((isodate.parse_duration(video['contentDetails']['duration']) for video in self.video_response),
                   timedelta())

    def show_best_video(self):
        """
        Определение лучшего видео в плейлисте на основе количества лайков.
        """
        videos_with_statistics = [video for video in self.video_response if 'statistics' in video]
        if not videos_with_statistics:
            return None
        best_video = max(videos_with_statistics, key=lambda video: int(video['statistics'].get('likeCount', 0)))
        return f"https://youtu.be/{best_video['id']}"
