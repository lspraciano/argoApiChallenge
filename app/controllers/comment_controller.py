from typing import Optional, List

from sqlalchemy.engine.result import Result
from sqlalchemy.future import select
from sqlalchemy.sql import Select

from app.core.database.database import async_session
from app.models.comment_model import CommentModel


async def create_comment(
        content: str,
        image_id: int,
        owner: int,
        last_change_owner
) -> CommentModel:
    comment: CommentModel = CommentModel(
        content=content,
        image_id=image_id,
        owner=owner,
        last_change_owner=last_change_owner
    )

    async with async_session() as session:
        session.add(comment)
        await session.commit()
        await session.refresh(comment)
        return comment


async def get_comment_by_comment_id(
        comment_id: int
) -> Optional[CommentModel]:
    async with async_session() as session:
        query: Select = select(CommentModel).where(
            CommentModel.id == comment_id,
        )
        result: Result = await session.execute(query)
        comment: Optional[CommentModel] = result.scalars().unique().one_or_none()
    return comment


async def update_comment_by_comment_id(
        comment_id: int,
        last_change_owner: int,
        content: Optional[int] = None,
        status: Optional[int] = None,
) -> Optional[CommentModel]:
    async with async_session() as session:
        comment_target: Optional[CommentModel] = await get_comment_by_comment_id(
            comment_id=comment_id
        )

        if not comment_target:
            return

        if content is not None:
            comment_target.content = content

        if status is not None:
            comment_target.status = status

        async with async_session() as session:
            session.add(comment_target)
            await session.commit()
            return comment_target


async def get_all_comments_by_image_id(
        image_id: int,
        status: int
) -> Optional[List[CommentModel]]:
    async with async_session() as session:
        query: Select = select(CommentModel).where(
            CommentModel.image_id == image_id,
            CommentModel.status == status,
        )
        result: Result = await session.execute(query)
        comment: Optional[List[CommentModel]] = list(result.scalars().unique().all())
    return comment
