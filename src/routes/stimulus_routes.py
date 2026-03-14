from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from src.datalayer import get_db
from src.datalayer.model.db import TestItem
from src.datalayer.repository import TestItemRepository
from src.middleware.auth import verify_jwt_token

router = APIRouter(prefix="/admin/stimuli", tags=["Stimuli Management"])


# Request/Response models
class TestItemCreate(BaseModel):
    test_type: str  # "spr" or "gj"
    item_type: str  # "sentence", "word", etc.
    content: str
    sentence_id: Optional[int] = None
    word_position: Optional[int] = None
    is_grammatical: Optional[bool] = None
    condition: Optional[str] = None
    notes: Optional[str] = None


class TestItemUpdate(BaseModel):
    content: Optional[str] = None
    sentence_id: Optional[int] = None
    word_position: Optional[int] = None
    is_grammatical: Optional[bool] = None
    condition: Optional[str] = None
    is_active: Optional[bool] = None
    notes: Optional[str] = None


class TestItemResponse(BaseModel):
    id: str
    test_type: str
    item_type: str
    content: str
    sentence_id: Optional[int]
    word_position: Optional[int]
    is_grammatical: Optional[bool]
    condition: Optional[str]
    is_active: bool
    notes: Optional[str]
    created_at: str
    updated_at: str


@router.get("", response_model=List[TestItemResponse])
async def get_all_items(
    db = Depends(get_db),
    token: dict = Depends(verify_jwt_token),
):
    """Get all test items"""
    repo = TestItemRepository(db)
    items = await repo.get_all()
    return [
        TestItemResponse(
            id=item.id,
            test_type=item.test_type,
            item_type=item.item_type,
            content=item.content,
            sentence_id=item.sentence_id,
            word_position=item.word_position,
            is_grammatical=item.is_grammatical,
            condition=item.condition,
            is_active=item.is_active,
            notes=item.notes,
            created_at=item.created_at.isoformat(),
            updated_at=item.updated_at.isoformat(),
        )
        for item in items
    ]


@router.get("/type/{test_type}", response_model=List[TestItemResponse])
async def get_items_by_type(
    test_type: str,
    db = Depends(get_db),
    token: dict = Depends(verify_jwt_token),
):
    """Get test items by type (spr or gj)"""
    if test_type not in ["spr", "gj"]:
        raise HTTPException(status_code=400, detail="Invalid test_type")

    repo = TestItemRepository(db)
    items = await repo.find_by_test_type(test_type)
    return [
        TestItemResponse(
            id=item.id,
            test_type=item.test_type,
            item_type=item.item_type,
            content=item.content,
            sentence_id=item.sentence_id,
            word_position=item.word_position,
            is_grammatical=item.is_grammatical,
            condition=item.condition,
            is_active=item.is_active,
            notes=item.notes,
            created_at=item.created_at.isoformat(),
            updated_at=item.updated_at.isoformat(),
        )
        for item in items
    ]


@router.get("/{item_id}", response_model=TestItemResponse)
async def get_item(
    item_id: str,
    db = Depends(get_db),
    token: dict = Depends(verify_jwt_token),
):
    """Get a specific test item"""
    repo = TestItemRepository(db)
    item = await repo.get_by_id(item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return TestItemResponse(
        id=item.id,
        test_type=item.test_type,
        item_type=item.item_type,
        content=item.content,
        sentence_id=item.sentence_id,
        word_position=item.word_position,
        is_grammatical=item.is_grammatical,
        condition=item.condition,
        is_active=item.is_active,
        notes=item.notes,
        created_at=item.created_at.isoformat(),
        updated_at=item.updated_at.isoformat(),
    )


@router.post("", response_model=TestItemResponse, status_code=201)
async def create_item(
    request: TestItemCreate,
    db = Depends(get_db),
    token: dict = Depends(verify_jwt_token),
):
    """Create a new test item"""
    try:
        item = TestItem.create(
            test_type=request.test_type,
            item_type=request.item_type,
            content=request.content,
            sentence_id=request.sentence_id,
            word_position=request.word_position,
            is_grammatical=request.is_grammatical,
            condition=request.condition,
            notes=request.notes,
        )

        repo = TestItemRepository(db)
        await repo.save(item)

        return TestItemResponse(
            id=item.id,
            test_type=item.test_type,
            item_type=item.item_type,
            content=item.content,
            sentence_id=item.sentence_id,
            word_position=item.word_position,
            is_grammatical=item.is_grammatical,
            condition=item.condition,
            is_active=item.is_active,
            notes=item.notes,
            created_at=item.created_at.isoformat(),
            updated_at=item.updated_at.isoformat(),
        )
    except Exception as e:
        print(f"Error creating item: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{item_id}", response_model=TestItemResponse)
async def update_item(
    item_id: str,
    request: TestItemUpdate,
    db = Depends(get_db),
    token: dict = Depends(verify_jwt_token),
):
    """Update a test item"""
    try:
        repo = TestItemRepository(db)
        item = await repo.get_by_id(item_id)

        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        # Update fields
        if request.content is not None:
            item.content = request.content
        if request.sentence_id is not None:
            item.sentence_id = request.sentence_id
        if request.word_position is not None:
            item.word_position = request.word_position
        if request.is_grammatical is not None:
            item.is_grammatical = request.is_grammatical
        if request.condition is not None:
            item.condition = request.condition
        if request.is_active is not None:
            item.is_active = request.is_active
        if request.notes is not None:
            item.notes = request.notes

        item.updated_at = datetime.utcnow()
        await repo.save(item)

        return TestItemResponse(
            id=item.id,
            test_type=item.test_type,
            item_type=item.item_type,
            content=item.content,
            sentence_id=item.sentence_id,
            word_position=item.word_position,
            is_grammatical=item.is_grammatical,
            condition=item.condition,
            is_active=item.is_active,
            notes=item.notes,
            created_at=item.created_at.isoformat(),
            updated_at=item.updated_at.isoformat(),
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating item: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{item_id}", status_code=204)
async def delete_item(
    item_id: str,
    db = Depends(get_db),
    token: dict = Depends(verify_jwt_token),
):
    """Delete a test item"""
    try:
        repo = TestItemRepository(db)
        exists = await repo.exists(item_id)

        if not exists:
            raise HTTPException(status_code=404, detail="Item not found")

        await repo.delete_by_id(item_id)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting item: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{item_id}/status", response_model=TestItemResponse)
async def toggle_status(
    item_id: str,
    is_active: bool,
    db = Depends(get_db),
    token: dict = Depends(verify_jwt_token),
):
    """Toggle item active status"""
    try:
        repo = TestItemRepository(db)
        item = await repo.toggle_active(item_id, is_active)

        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        return TestItemResponse(
            id=item.id,
            test_type=item.test_type,
            item_type=item.item_type,
            content=item.content,
            sentence_id=item.sentence_id,
            word_position=item.word_position,
            is_grammatical=item.is_grammatical,
            condition=item.condition,
            is_active=item.is_active,
            notes=item.notes,
            created_at=item.created_at.isoformat(),
            updated_at=item.updated_at.isoformat(),
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error toggling status: {e}")
        raise HTTPException(status_code=500, detail=str(e))
