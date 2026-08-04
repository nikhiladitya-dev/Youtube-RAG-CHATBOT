from dataclasses import dataclass
from langchain_core.documents import Document
from app.models.document_models import OffsetMap

@dataclass
class ProcessedDocument:
    document: Document
    offset_map: list[OffsetMap]