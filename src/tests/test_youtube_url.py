from update_youtube.logic import get_youtube_channel_from_video_url, get_youtube_channel_username

def test_get_youtube_channel_from_video_url():
    """
    This function test can be run using the following command:
    
    pytest tests/test_youtube_url.py::test_get_youtube_channel_from_video_url -v
    """
    video_urls = (
        "https://www.youtube.com/embed/JpnNFe1k9zA?feature=shared",
        "https://www.youtube.com/embed/Vns6cAtpQ8w"
    )
    channel_urls = (
        "https://www.youtube.com/channel/UCbqe7u7_489e5zs8Bj6NdFQ",
        "https://www.youtube.com/channel/UCbWZkdwVQDY4jcLvRB9UtLQ"
    )
    for video_url, channel_url in zip(video_urls, channel_urls):
        assert get_youtube_channel_from_video_url(video_url) == channel_url

def test_get_youtube_channel_username():
    """
    This function test can be run using the following command:
    
    pytest tests/test_youtube_url.py::test_get_youtube_channel_username -v
    """
    video_urls = (
        "https://www.youtube.com/embed/JpnNFe1k9zA?feature=shared",
        "https://www.youtube.com/embed/Vns6cAtpQ8w"
    )
    usernames = (
        "みじん子ちゃんねる。MizinkoCh.",
        "kkbn"
    )
    for video_url, username in zip(video_urls, usernames):
        assert get_youtube_channel_username(video_url) == username

