from __future__ import annotations

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemRead

router = APIRouter(prefix="/items", tags=["items"])


@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(payload: ItemCreate, db: AsyncSession = Depends(get_db)):
    """Create a new item in the database."""
    item = Item(name=payload.name, description=payload.description)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router.get("", response_model=List[ItemRead])
async def list_items(skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db)):
    """List items with pagination."""
    result = await db.execute(select(Item).offset(skip).limit(limit))
    return result.scalars().all()


@router.get("/{item_id}", response_model=ItemRead)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve an item by ID."""
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
