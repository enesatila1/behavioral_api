from typing import List, Optional
from firebase_admin.firestore_async import AsyncClient
from ..model.db.test_item import TestItem
from ._firestore_base_repository import FirestoreBaseRepository


class TestItemRepository(FirestoreBaseRepository[TestItem]):
    """Repository for test items/stimuli"""

    def __init__(self, db: AsyncClient):
        super().__init__(db, TestItem, "test_items")

    async def find_by_test_type(self, test_type: str) -> List[TestItem]:
        """Find all test items by test type (spr or gj)"""
        return await self.find_by(test_type=test_type)

    async def find_active_by_test_type(self, test_type: str) -> List[TestItem]:
        """Find active test items by test type"""
        items = await self.find_by(test_type=test_type)
        return [item for item in items if item.is_active]

    async def find_by_sentence_id(self, sentence_id: int) -> List[TestItem]:
        """Find all items belonging to a specific sentence (SPR)"""
        items = await self.get_all()
        return [item for item in items if item.sentence_id == sentence_id]

    async def find_by_item_type(self, item_type: str) -> List[TestItem]:
        """Find all items of a specific type (sentence, word, etc.)"""
        return await self.find_by(item_type=item_type)

    async def toggle_active(self, item_id: str, is_active: bool) -> Optional[TestItem]:
        """Toggle the active status of an item"""
        item = await self.get_by_id(item_id)
        if item:
            item.is_active = is_active
            from datetime import datetime
            item.updated_at = datetime.utcnow()
            await self.save(item)
        return item
