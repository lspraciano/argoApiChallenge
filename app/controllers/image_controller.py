from typing import Optional, List

from fastapi import UploadFile
from sqlalchemy.engine.result import Result
from sqlalchemy.future import select
from sqlalchemy.sql import Select

from app.core.database.database import async_session
from app.models.image_model import ImageModel


async def create_image(
        file_data: UploadFile,
        last_change_owner: int
) -> ImageModel:
    image: ImageModel = ImageModel(
        name=file_data.filename,
        file_data=await file_data.read(),
        status=1,
        last_change_owner=last_change_owner
    )

    async with async_session() as session:
        session.add(image)
        await session.commit()
        await session.refresh(image)
        return image


async def get_image_by_image_id(
        image_id: int,
        name: Optional[str] = None,
        approved_by: Optional[int] = None,
        approved: Optional[int] = None,
        status: Optional[int] = None,
) -> Optional[ImageModel]:
    async with async_session() as session:
        filter_list: list = []

        if name is not None:
            filter_list.append(
                ImageModel.name == name,
            )

        if approved_by is not None:
            filter_list.append(
                ImageModel.approved_by == approved_by,
            )

        if approved is not None:
            filter_list.append(
                ImageModel.approved == approved,
            )

        if status is not None:
            filter_list.append(
                ImageModel.status == status,
            )

        query: Select = select(ImageModel).where(
            ImageModel.id == image_id,
            *filter_list
        )

        result: Result = await session.execute(query)
        image: Optional[ImageModel] = result.scalars().unique().one_or_none()

    return image


async def get_all_images(
        name: Optional[str] = None,
        approved_by: Optional[int] = None,
        approved: Optional[int] = None,
        status: Optional[int] = None,
) -> Optional[List[ImageModel]]:
    async with async_session() as session:
        filter_list: list = []

        if name is not None:
            filter_list.append(
                ImageModel.name == name,
            )

        if approved_by is not None:
            filter_list.append(
                ImageModel.approved_by == approved_by,
            )

        if approved is not None:
            filter_list.append(
                ImageModel.approved == approved,
            )

        if status is not None:
            filter_list.append(
                ImageModel.status == status,
            )

        query: Select = select(ImageModel).where(*filter_list)
        result: Result = await session.execute(query)
        image: Optional[List[ImageModel]] = list(result.scalars().unique().all())
    return image


async def update_images_by_image_id(
        image_id: int,
        name: Optional[str] = None,
        approved_by: Optional[int] = None,
        approved: Optional[int] = None,
        status: Optional[int] = None,
) -> Optional[ImageModel]:
    image_target: Optional[ImageModel] = await get_image_by_image_id(
        image_id=image_id
    )

    if not image_target:
        return None

    if name is not None:
        image_target.name = name

    if approved_by is not None:
        image_target.approved_by = approved_by

    if approved is not None:
        image_target.approved = approved

    if status is not None:
        image_target.status = status

    async with async_session() as session:
        session.add(image_target)
        await session.commit()
        return image_target
