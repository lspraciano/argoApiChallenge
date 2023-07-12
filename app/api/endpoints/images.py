import imghdr
from typing import Optional, List

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import StreamingResponse

from app.controllers.image_controller import create_image, get_image_by_image_id, get_all_images, \
    update_images_by_image_id
from app.core.dependencies.deps import get_user_id_from_token, admin_authorization
from app.models.image_model import ImageModel
from app.schemas.image_schema import ImageSchemaBasic, ImageByIdQueryParamsSchema, ImagePostSchema, ImageApprovalSchema, \
    ImageResponse, ImageIdSchema

router = APIRouter()


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=ImageSchemaBasic
)
async def post_image_(
        image: ImagePostSchema = Depends(),
        user_id_logged: str = Depends(get_user_id_from_token),
):
    """
    This route allows registering an image in the database.
    """
    image.image.file.seek(0, 2)
    file_size: int = image.image.file.tell()
    await image.image.seek(0)

    if file_size > 2 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File too large - Max size is 2MB"
        )

    content_type: Optional[str] = image.image.content_type
    if content_type not in ["image/jpeg", "image/png", "image/gif"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type - Please use jpeg, png or gif"
        )

    new_image: ImageModel = await create_image(
        file_data=image.image,
        last_change_owner=int(user_id_logged)
    )
    return new_image


@router.get(
    path="/{image_id}",
    response_model=Optional[ImageSchemaBasic]
)
async def get_image_by_id_image_(
        image_id: ImageIdSchema,
        user_id_logged: str = Depends(get_user_id_from_token),
        admin_user=Depends(admin_authorization)
):
    """
    This route allows you to fetch an image from the
    database by image id.
    """
    image: ImageModel = await get_image_by_image_id(
        image_id=image_id,
    )

    if not image:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image Not Found"
        )
    return image


@router.get(
    path="/",
    response_model=Optional[List[ImageSchemaBasic]]
)
async def get_all_images_(
        images_parameters: ImageByIdQueryParamsSchema = Depends(),
        user_id_logged: str = Depends(get_user_id_from_token),
        admin_user=Depends(admin_authorization)
):
    """
    This route allows you to fetch all images in the database.
    """
    images: Optional[List[ImageModel]] = await get_all_images(
        name=images_parameters.name,
        approved_by=images_parameters.approved_by,
        approved=images_parameters.approved,
    )

    if not images:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Images Not Found"
        )
    return images


@router.get(
    path="/get-file/{image_id}",
    response_class=StreamingResponse,
    response_model=ImageResponse,
    responses={
        200: {
            "content": {
                "image/png": {},
                "image/jpeg": {},
                "image/gif": {}
            },
            "description": "Return an approved image.",
        },
    },
)
async def get_image_file_by_image_id_(
        image_id: ImageIdSchema,
        user_id_logged: str = Depends(get_user_id_from_token),
        admin_user=Depends(admin_authorization)
):
    """
    This route allows you to search for the file referring
    to an image registered in the database through the image id.
    """
    image: ImageModel = await get_image_by_image_id(
        image_id=image_id,
    )

    if not image:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image Not Found"
        )

    media_type: Optional[str] = imghdr.what(None, h=image.file_data)

    return StreamingResponse(
        iter([image.file_data]),
        media_type=f"image/{media_type}"
    )


@router.patch(
    path="/handle-approve",
    response_model=Optional[List[ImageSchemaBasic]]
)
async def handle_approval_images_(
        images_to_update: ImageApprovalSchema,
        user_id_logged: str = Depends(get_user_id_from_token),
        admin_user=Depends(admin_authorization)
):
    """
    This route allows you to approve or disapprove an image.
    """
    images_updated: Optional[List[ImageModel]] = []

    for image_id in images_to_update.images_ids_list:
        image_updated: Optional[ImageModel] = await update_images_by_image_id(
            image_id=image_id,
            approved=images_to_update.approval_result,
            approved_by=int(user_id_logged)
        )
        if image_updated:
            images_updated.append(image_updated)

    if not images_updated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No image has been updated"
        )
    return images_updated


@router.get(
    path="/handle-approve/approved",
    response_model=Optional[List[ImageSchemaBasic]]
)
async def get_all_approved_images_(
        images_to_update: ImageApprovalSchema,
        user_id_logged: str = Depends(get_user_id_from_token),
):
    """
    This route allows you to list all approved images
    that are registered in the database.
    """
    approved_images: Optional[List[ImageModel]] = await get_all_images(
        approved=1,
    )

    if not approved_images:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Images Not Found"
        )
    return approved_images


@router.get(
    path="/handle-approve/approved/get-file/{image_id}",
    response_class=StreamingResponse,
    response_model=ImageResponse,
    responses={
        200: {
            "content": {
                "image/png": {},
                "image/jpeg": {},
                "image/gif": {}
            },
            "description": "Return an approved image.",
        },
    },
)
async def get_approved_image_file_by_image_id_(
        image_id: ImageIdSchema,
        user_id_logged: str = Depends(get_user_id_from_token),
):
    """
    This route allows you to fetch the file of an
    approved image from through the image ID.
    """
    image: ImageModel = await get_image_by_image_id(
        image_id=image_id,
        approved=1
    )

    if not image:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image Not Found"
        )

    media_type: Optional[str] = imghdr.what(None, h=image.file_data)

    return StreamingResponse(
        iter([image.file_data]),
        media_type=f"image/{media_type}"
    )
