from math import floor

def seconds_to_timestamp(
    seconds: float,
) -> str:
    # Convert seconds into HH:MM:SS format.
    total_seconds = floor(seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return (f"{hours:02d}:" f"{minutes:02d}:" f"{seconds:02d}" )

def format_timestamp_range(
    start: float,
    end: float,
) -> str:
    
    # Format a timestamp range.

    return (f"{seconds_to_timestamp(start)}" f" - " f"{seconds_to_timestamp(end)}" )