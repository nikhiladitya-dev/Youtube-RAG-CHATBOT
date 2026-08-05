from urllib.parse import urlparse, parse_qs


def extract_video_id(url: str) -> str:
    """
    Extract the YouTube video ID from a supported YouTube URL.
    Supported formats:https://www.youtube.com/watch?v=XXXX (or) https://youtu.be/XXXX
    """
    parsed = urlparse(url)
    if parsed.hostname == "youtu.be":
        return parsed.path[1:]

    if parsed.hostname in (
        "www.youtube.com",
        "youtube.com",
        "m.youtube.com",
    ):
        return parse_qs(parsed.query)["v"][0]

    raise ValueError("Invalid YouTube URL.")

VALID_YOUTUBE_DOMAINS = { "youtube.com","www.youtube.com","m.youtube.com","youtu.be","www.youtu.be",}

def is_valid_youtube_url(
    url: str,
) -> bool:
    
    # Validate whether the given URL belongs to YouTube.
    try:
        parsed = urlparse(url)
        return parsed.netloc.lower() in VALID_YOUTUBE_DOMAINS

    except Exception:
        return False
