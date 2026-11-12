#!/usr/bin/env python3
"""
Seed initial sample data into the database.
Runs seamlessly both inside Docker (`docker compose exec api python -m scripts.seed`)
and locally against SQLite/PostgreSQL.
"""

import asyncio
import logging
from sqlalchemy import select

from app.database import AsyncSessionLocal, create_tables
from app.models.item import Item

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed")

DEFAULT_ITEMS = [
    {"name": "Alpha Service", "description": "Core authentication and routing service"},
    {"name": "Beta Pipeline", "description": "Asynchronous market data transformation worker"},
    {"name": "Gamma Dispatcher", "description": "PubSub notification dispatcher"},
]


async def seed():
    logger.info("Ensuring database tables exist...")
    await create_tables()

    async with AsyncSessionLocal() as session:
        for it in DEFAULT_ITEMS:
            existing = await session.execute(select(Item).where(Item.name == it["name"]))
            if not existing.scalars().first():
                item = Item(name=it["name"], description=it["description"])
                session.add(item)
                logger.info("Seeding: %s", it["name"])
            else:
                logger.info("Already exists: %s", it["name"])
        await session.commit()
    logger.info("Seeding completed successfully.")


if __name__ == "__main__":
    asyncio.run(seed())
