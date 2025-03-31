import yt_dlp

def get_youtube_channel_from_video_url(video_url: str) -> str:
    """
    YouTube 영상 URL을 입력받아 채널 URL을 반환합니다.
    
    Args:
        video_url (str): YouTube 영상 URL
        
    Returns:
        str: 채널 URL
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(video_url, download=False)
            channel_url = info.get('channel_url', '')
            return channel_url
        except Exception as e:
            print(f"Error extracting channel URL: {e}")
            return ""

def get_youtube_channel_username_from_video_url(video_url: str) -> str:
    """
    YouTube 영상 URL을 입력받아 채널 사용자명을 반환합니다.
    
    Args:
        video_url (str): YouTube 영상 URL
        
    Returns:
        str: 채널 사용자명
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(video_url, download=False)
            uploader = info.get('uploader', '')
            return uploader
        except Exception as e:
            print(f"Error extracting channel username: {e}")
            return ""


