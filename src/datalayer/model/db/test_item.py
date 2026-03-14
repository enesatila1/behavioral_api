from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class TestItem:
    """Model representing a test stimulus/item (sentence, word, etc.)"""
    id: str  # Firestore doc ID
    test_type: str  # "spr" or "gj"
    item_type: str  # "sentence", "word", "condition", etc.
    content: str  # The actual content (sentence, word, etc.)
    sentence_id: Optional[int] = None  # For SPR: which sentence it belongs to
    word_position: Optional[int] = None  # For SPR: position in sentence
    is_grammatical: Optional[bool] = None  # For GJ: whether sentence is grammatical
    condition: Optional[str] = None  # Experimental condition
    is_active: bool = True  # Whether this item is used in tests
    notes: Optional[str] = None  # Additional notes
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    @staticmethod
    def create(
        test_type: str,
        item_type: str,
        content: str,
        **kwargs
    ) -> "TestItem":
        """Factory method to create a test item"""
        return TestItem(
            id=str(uuid.uuid4()),
            test_type=test_type,
            item_type=item_type,
            content=content,
            sentence_id=kwargs.get("sentence_id"),
            word_position=kwargs.get("word_position"),
            is_grammatical=kwargs.get("is_grammatical"),
            condition=kwargs.get("condition"),
            is_active=kwargs.get("is_active", True),
            notes=kwargs.get("notes"),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

    def to_dict(self):
        """Convert to dictionary for Firestore serialization"""
        data = asdict(self)
        data["created_at"] = self.created_at.isoformat()
        data["updated_at"] = self.updated_at.isoformat()
        return {k: v for k, v in data.items() if v is not None}

    @staticmethod
    def from_dict(data: dict) -> "TestItem":
        """Reconstruct from Firestore document"""
        data = data.copy()
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if isinstance(data.get("updated_at"), str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        return TestItem(**data)
