from .db import get_videos_after_date, update_user_channel, has_channel
from .logic import get_youtube_channel_from_video_url, get_youtube_channel_username_from_video_url
from datetime import datetime, timedelta

exclude_user_ids = [
    13547823, # Not specified
]

def update_youtube_videos():
    """
    유튜브 영상 정보를 업데이트합니다.
    """
    videos = get_videos_after_date(datetime.now() - timedelta(days=14))
    for video in videos:
        user_id, _, _, video_url, *_ = video
        if has_channel(user_id):
            print(f"User {user_id} already has a channel")
            continue
        else:   
            print(f"User {user_id} does not have a channel")
            if user_id in exclude_user_ids:
                print(f"User {user_id} is in the exclude list")
                continue
            channel_url = get_youtube_channel_from_video_url(video_url)
            channel_username = get_youtube_channel_username_from_video_url(video_url)
            print(f"Channel URL: {channel_url}")
            print(f"Channel Username: {channel_username}")
            update_user_channel(user_id, channel_username, channel_url)

if __name__ == "__main__":
    update_youtube_videos()
