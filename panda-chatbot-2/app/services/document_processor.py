from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.models.document_models import TranscriptDocument
from app.core.logger import logger
from app.models.document_models import (
    TranscriptDocument,
    OffsetMap,
)
from app.models.processing_models import ( ProcessedDocument,)

class DocumentProcessor:

    # Converts transcript documents into retrieval ready langchan documents.

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            add_start_index = True,
        )

    def process(
        self,
        transcript: TranscriptDocument,
    ) -> list[Document]:

        # Convert a transcript into retrieval ready chunked documents.

        logger.info("Starting document processing...")
        processed = self._create_document(transcript)

        chunks = self._chunk_document(processed)

        chunks = self._attach_chunk_metadata(
            chunks,
            processed.offset_map,
        )

        logger.info(f"Generated {len(chunks)} chunks.")
        return chunks

    def _build_offset_map(
        self,
        transcript: TranscriptDocument,
    ) -> tuple[str, list[OffsetMap]]:

        logger.info("Building transcript offset map...")
        merged_text = []
        offset_map = []
        current_position = 0

        for segment in transcript.segments:
            text = segment.text.strip()
            if not text:
                continue

            char_start = current_position
            char_end = char_start + len(text)
            offset_map.append(OffsetMap(
                    char_start=char_start,char_end=char_end,
                    start_time=segment.start,end_time=segment.start + segment.duration,

                ))

            merged_text.append(text)
            merged_text.append("\n\n")
            current_position = char_end + 2
        final_text = "".join(merged_text)
        logger.info(f"Merged transcript into {len(final_text)} characters.")
        return final_text, offset_map

    def _create_document(
        self,
        transcript: TranscriptDocument,
    ) -> ProcessedDocument:

        # Create a single LangChain Document from the transcript while preserving the character-to-timestamp mapping.

        logger.info("Creating merged LangChain document...")

        merged_text, offset_map = self._build_offset_map(
            transcript
        )
        document = Document(
            page_content=merged_text,
            metadata={

                "video_id": transcript.video_id,
                "video_url": transcript.video_url,
                "language": transcript.language,
                "language_code": transcript.language_code,
                "is_generated": transcript.is_generated,
            },

        )
        logger.info("Merged LangChain document created successfully.")
        return ProcessedDocument(document=document,offset_map=offset_map,)

    def _chunk_document(
        self,
        processed: ProcessedDocument,
    ) -> list[Document]:

         # Split the merged transcript into retrieval-ready chunks.

        logger.info("Chunking merged transcript...")
        chunks = self.text_splitter.split_documents([processed.document])
        logger.info( f"Created {len(chunks)} chunks.")
        return chunks

    def _attach_chunk_metadata(
        self,
        chunks: list[Document],
        offset_map: list[OffsetMap],
    ) -> list[Document]:

        logger.info("Attaching timestamp metadata...")

        for chunk_id, chunk in enumerate(chunks):

            chunk_start = chunk.metadata["start_index"]

            chunk_end = (chunk_start + len(chunk.page_content))
            matching_offsets = []
            for offset in offset_map:

                if (
                    offset.char_end >= chunk_start
                    and
                    offset.char_start <= chunk_end
                ):
                    matching_offsets.append(offset)

            if not matching_offsets:
                continue

            start_time = matching_offsets[0].start_time

            end_time = matching_offsets[-1].end_time

            chunk.metadata.update({

                "chunk_id": chunk_id,
                "end_index": chunk_end,
                "start_time": start_time,
                "end_time": end_time,
                "duration": round(  end_time - start_time, 2,),
            })

        logger.info("Timestamp metadata attached successfully.")
        return chunks