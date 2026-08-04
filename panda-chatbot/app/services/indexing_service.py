class IndexingService:

    def __init__(
        self,
        transcript_service: TranscriptService,
        document_processor: DocumentProcessor,
        vector_store_service: VectorStoreService,
    ):
        self.transcript_service = transcript_service
        self.document_processor = document_processor
        self.vector_store_service = vector_store_service

    def index_video(
        self,
        video_url: str,
    ):
        logger.info("Starting video indexing...")

        transcript = self.transcript_service.fetch_transcript( video_url)
        documents = self.document_processor.process( transcript)
        self.vector_store_service.add_documents( documents)
        logger.info("Video indexed successfully.")

        return {
            "video_id": transcript.video_id,
            "chunks": len(documents),
        }

    def reindex_video(
        self,video_url: str,
    ):
        self.vector_store_service.delete_collection()
        return self.index_video(video_url)