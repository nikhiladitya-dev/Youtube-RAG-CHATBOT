import json
from pathlib import Path
from datetime import datetime
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    NoTranscriptFound,
    TranscriptsDisabled,
)
from app.core.config import TRANSCRIPT_DIR
from app.core.exceptions import (
    TranscriptUnavailableError,
)
from app.core.logger import logger
from app.models.document_models import (
    TranscriptDocument,
    TranscriptSegment,
)
from app.utils.youtube_utils import extract_video_id

class TranscriptService:
    def _load_cached_transcript(
        self,
        video_id: str,
    ) -> TranscriptDocument | None:

        file_path = TRANSCRIPT_DIR / f"{video_id}.json"

        if not file_path.exists():
            return None

        logger.info("Cached transcript found. Loading from disk...")

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        metadata = data["metadata"]

        segments = [
            TranscriptSegment(**segment)
            for segment in data["segments"]
        ]

        return TranscriptDocument(
            video_id=metadata["video_id"],
            video_url=metadata["video_url"],
            language=metadata["language"],
            language_code=metadata["language_code"],
            is_generated=metadata["is_generated"],
            segment_count=metadata["segment_count"],
            created_at=datetime.fromisoformat(
                metadata["created_at"]
            ),
            segments=segments,
        )

    def fetch_transcript(self, youtube_url: str) -> TranscriptDocument:
        """
        Fetch the best available transcript for a YouTube video.
        """

        logger.info("Extracting Video ID...")

        video_id = extract_video_id(youtube_url)
        cached_document = self._load_cached_transcript(video_id)

        if cached_document is not None:
            return cached_document
        transcript_list = self._get_transcript_list(video_id)

        transcript = self._select_best_transcript(transcript_list)

        document = self._build_document(
            transcript,
            youtube_url,
            video_id,
        )

        logger.info("Transcript successfully created.")

        return document
    
    def _get_transcript_list(self, video_id: str):

        logger.info("Searching available transcripts...")

        try:
            api = YouTubeTranscriptApi()
            return api.list(video_id)

        except TranscriptsDisabled:
            logger.error("Transcripts are disabled.")

            raise TranscriptUnavailableError(
                "Transcripts are disabled for this video."
            )

        except Exception as e:
            logger.error(str(e))

            raise TranscriptUnavailableError(
                "Unable to fetch transcript list."
            )

    def _select_best_transcript(self, transcript_list):

        logger.info("Selecting best transcript...")

        transcripts = list(transcript_list)

        logger.info(f"{len(transcripts)} transcript(s) found.")

        for transcript in transcripts:
            if (
                transcript.language_code == "en"
                and not transcript.is_generated
            ):
                logger.info("Using manual English transcript.")
                return transcript
        for transcript in transcripts:

            if transcript.language_code == "en":

                logger.warning(
                    "Using generated English transcript."
                )

                return transcript
            
        for transcript in transcripts:

            if not transcript.is_generated:

                logger.warning(
                    f"English unavailable. Falling back to "
                    f"{transcript.language}."
                )

                return transcript
            
        if transcripts:

            logger.warning(
                f"Using generated {transcripts[0].language} transcript."
            )

            return transcripts[0]
        raise TranscriptUnavailableError(
            "No transcript available."
        )
    def _build_document(
        self,
        transcript,
        youtube_url,
        video_id,
    ) -> TranscriptDocument:
        
        transcript_data = transcript.fetch()
        segments = [

            TranscriptSegment(
                text=item.text,
                start=item.start,
                duration=item.duration,
            )

            for item in transcript_data

        ]
        logger.info(
            f"Downloaded {len(segments)} transcript segments."
        )
        return TranscriptDocument(

            video_id=video_id,

            video_url=youtube_url,

            language=transcript.language,

            language_code=transcript.language_code,

            is_generated=transcript.is_generated,

            segment_count=len(segments),

            created_at=datetime.utcnow(),

            segments=segments,

        )

    
    def save_transcript(
        self,
        transcript: TranscriptDocument,
    ):
        if not isinstance(transcript, TranscriptDocument):
            raise TypeError(
                "Expected a TranscriptDocument instance."
            )

        TRANSCRIPT_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path = (
            Path(TRANSCRIPT_DIR)
            / f"{transcript.video_id}.json"
        )
        payload = {
            "metadata": {

                "video_id": transcript.video_id,
                "video_url": transcript.video_url,
                "language": transcript.language,
                "language_code": transcript.language_code,
                "is_generated": transcript.is_generated,
                "segment_count": transcript.segment_count,
                "created_at": transcript.created_at.isoformat(),
            },
            "segments": [
                segment.model_dump()
                for segment in transcript.segments
            ],
        }
        with open(
            file_path,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                payload,
                file,
                indent=4,
                ensure_ascii=False,
            )
        logger.info(
            f"Transcript saved at {file_path}"
        )
    

    