class TranscriptError(Exception):
    """Base exception for transcript related errors."""

class InvalidYouTubeUrlError(TranscriptError):
    """Raised when the supplied URL is invalid."""

class TranscriptUnavailableError(TranscriptError):
    """Raised when no transcript is available."""

class TranscriptDisabledError(TranscriptError):
    """Raised when transcripts are disabled."""

class UnsupportedLanguageError(TranscriptError):
    """Raised when no suitable transcript language exists."""