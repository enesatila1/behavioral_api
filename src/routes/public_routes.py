from fastapi import APIRouter, Depends
from typing import List
from pydantic import BaseModel
from datalayer import get_db
from datalayer.repository import TestItemRepository

router = APIRouter(prefix="/stimuli", tags=["Public Stimuli"])


class TestItemResponse(BaseModel):
    id: str
    test_type: str
    item_type: str
    content: str
    sentence_id: int | None
    is_grammatical: bool | None
    condition: str | None
    is_active: bool


@router.get("/type/{test_type}", response_model=List[TestItemResponse])
async def get_public_stimuli_by_type(
    test_type: str,
    db=Depends(get_db),
):
    """Get public test stimuli by type (spr or gj) - no authentication required"""
    if test_type not in ["spr", "gj"]:
        return []

    repo = TestItemRepository(db)
    items = await repo.find_by_test_type(test_type)

    return [
        TestItemResponse(
            id=item.id,
            test_type=item.test_type,
            item_type=item.item_type,
            content=item.content,
            sentence_id=item.sentence_id,
            is_grammatical=item.is_grammatical,
            condition=item.condition,
            is_active=item.is_active,
        )
        for item in items
    ]
