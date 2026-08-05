from fastapi import APIRouter,HTTPException
from app.core.service_container import container
from app.utils.youtube_utils import is_valid_youtube_url
from app.api.schemas import (
    ProcessVideoRequest,
    ProcessVideoResponse,
)
from app.api.schemas import (
    ChatRequest,
    ChatResponse,
    SourceChunk,
)
import traceback
from app.core.exceptions import (TranscriptUnavailableError,)

router = APIRouter(
    prefix="/api/v1",
    tags=["YouTube RAG"],
)

@router.post(
    "/process-video",
    response_model=ProcessVideoResponse,
)
def process_video(
    request: ProcessVideoRequest,
):
    try:

        if not is_valid_youtube_url(request.url):

            raise HTTPException(
                status_code=400,
                detail="Invalid YouTube URL.",
            )

        # Fetch transcript
        transcript = container.transcript_service.fetch_transcript(request.url)

        #Check if already indexed
        if container.get_vectorstore_service().is_video_indexed(
            transcript.video_id
        ):
            return ProcessVideoResponse(
                status="already_indexed",
                video_id=transcript.video_id,
                chunks=0,
            )

        # Process transcript into chunks
        documents = container.document_processor.process( transcript)

        # Index chunks
        container.get_vectorstore_service().add_documents( documents)
        container.current_video_id = transcript.video_id

        return ProcessVideoResponse(
            status="success",
            video_id=transcript.video_id,
            chunks=len(documents),
        )
    except TranscriptUnavailableError as e:

        raise HTTPException(status_code=404, detail=str(e),)

    except Exception as e:

        raise HTTPException(status_code=500,detail=str(e),)

@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
):

    try:

        response = container.get_chat_service().ask(
            question=request.question,
            video_id=request.video_id,
        )

        sources = [
            SourceChunk(
                timestamp=source["timestamp"],
                start_time=source["start_time"],
                end_time=source["end_time"],
                content=source["content"],
            )
            for source in response["sources"]
        ]

        return ChatResponse(
            answer=response["answer"],
            sources=sources,
        )

    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

@router.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "YouTube RAG Chatbot",
        "version": "1.0.0",
    }
    
