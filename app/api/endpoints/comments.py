from typing import Optional, List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from app.controllers.comment_controller import create_comment, get_all_comments_by_image_id, \
    update_comment_by_comment_id, get_comment_by_comment_id
from app.controllers.image_controller import get_image_by_image_id
from app.core.dependencies.deps import get_user_id_from_token
from app.models.comment_model import CommentModel
from app.models.image_model import ImageModel
from app.schemas.comment_schema import CommentSchemaBasic, CommentCreateSchema, CommentUpdateSchema, CommentIdSchema
from app.schemas.image_schema import ImageIdSchema

router = APIRouter()


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=CommentSchemaBasic
)
async def post_comment_(
        comment: CommentCreateSchema = Depends(),
        user_id_logged: str = Depends(get_user_id_from_token),
):
    """
    This route allows you to register a comment for a given image.
    """
    image_target: Optional[ImageModel] = await get_image_by_image_id(
        image_id=comment.image_id,
        status=1
    )

    if not image_target:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image Not Found"
        )

    try:
        comment: CommentModel = await create_comment(
            content=comment.content,
            image_id=comment.image_id,
            owner=int(user_id_logged),
            last_change_owner=int(user_id_logged)
        )
        return comment

    except IntegrityError as error:
        error_msg: str = error.args[0]
        output_error: str = ""
        if "foreign key constraint" in error_msg:
            if "image_id" in error_msg:
                output_error = "Image Not Found"
        else:
            output_error = "Unknown Error. Contact Support"

        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=output_error
        )


@router.patch(
    path="/{comment_id}",
    status_code=status.HTTP_200_OK,
    response_model=Optional[CommentSchemaBasic]
)
async def update_comment_by_comment_id_(
        comment_id: CommentIdSchema,
        comment: CommentUpdateSchema = Depends(),
        user_id_logged: str = Depends(get_user_id_from_token),
):
    """
    This route allows you to update the content
    or status of a comment registered in the database.
    """
    comment_target: Optional[CommentModel] = await get_comment_by_comment_id(
        comment_id=comment_id
    )

    if not comment_target:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Comment Not Found"
        )

    if comment.content is not None:
        if comment_target.owner != int(user_id_logged):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot update the content of another user's comment"
            )

    if comment.status == 0:
        if (
                comment_target.owner != int(user_id_logged)
                and
                int(user_id_logged) not in [1, 2]
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot delete another user's comment"
            )

    comment_updated: Optional[CommentModel] = await update_comment_by_comment_id(
        comment_id=comment_id,
        last_change_owner=int(user_id_logged),
        content=comment.content,
        status=comment.status
    )

    return comment_updated


@router.get(
    path="/by-image/{image_id}",
    status_code=status.HTTP_200_OK,
    response_model=Optional[List[CommentSchemaBasic]]
)
async def get_all_comments_by_image_id_(
        image_id: ImageIdSchema,
        user_id_logged: str = Depends(get_user_id_from_token),
):
    """
    This route allows you to search all registered
    comments for a given image through the image ID.
    The target image must be active in the database.
    """
    image_target: Optional[ImageModel] = await get_image_by_image_id(
        image_id=image_id,
        status=1
    )

    if not image_target:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image Not Found"
        )

    comments: Optional[List[CommentModel]] = await get_all_comments_by_image_id(
        image_id=image_id,
        status=1
    )

    if not comments:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Comments Not Found"
        )
    return comments
