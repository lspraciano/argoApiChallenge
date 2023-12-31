from typing import List, Optional

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic.networks import EmailStr
from sqlalchemy.exc import IntegrityError

from app.controllers.user_controller import get_user_by_id, create_user, get_all_users, \
    update_user_by_id, authenticate_user
from app.core.dependencies.deps import get_user_id_from_token, admin_authorization
from app.core.email.email_manager import send_email_async
from app.core.security.jwt_token_manager import get_access_token
from app.core.security.password_manager import generate_password, validate_password_string
from app.models.user_model import UserModel
from app.schemas.user_schema import UserSchemaBasic, UserSchemaCreate, \
    UserSchemaUpdate, UserSchemaUpdatePassword, UserAuthentication, UserIdSchema

router = APIRouter()


@router.get(
    path="",
    response_model=List[Optional[UserSchemaBasic]]
)
async def get_all_users_(
        user_id_logged: str = Depends(get_user_id_from_token),
        admin_user=Depends(admin_authorization)
):
    """
    This route allows to list all database users
    """
    users: Optional[List[UserModel]] = await get_all_users()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Users Not Found"
        )
    return users


@router.get(
    path="/{user_id}",
    response_model=Optional[UserSchemaBasic]
)
async def get_user_by_user_id_(
        user_id: UserIdSchema,
        user_id_logged: str = Depends(get_user_id_from_token),
        admin_user=Depends(admin_authorization)
):
    """
    This route allows you to list a database user through its ID
    """
    user: Optional[UserModel] = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User Not Found"
        )
    return user


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=UserSchemaBasic
)
async def create_new_user_(
        user: UserSchemaCreate,
        user_id_logged: str = Depends(get_user_id_from_token),
        admin_user=Depends(admin_authorization)
):
    """
    This route will create a new user in the database. This user
    will receive a temporary password in the email registered to him.
    """
    try:
        password: str = await generate_password()
        new_user: Optional[UserModel] = await create_user(
            name=user.name,
            email=user.email,
            password=password,
            last_change_owner=int(user_id_logged)
        )

        await send_email_async(
            subject="Your New Password",
            email_to=[f"{user.email}"],
            body=f"Your new password is: {password}"
        )
        return new_user

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="That email address is already in use."
        )


@router.post(
    path="/authentication",
    status_code=status.HTTP_200_OK,
    response_model=UserAuthentication
)
async def authenticate_user_(
        form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    This route allows a user registered in the database to
    obtain an access token.
    """
    user: Optional[UserModel] = await authenticate_user(
        email=EmailStr(form_data.username),
        password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong Username or Password"
        )

    if user.status == 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Deactivated User"
        )

    return {
        "access_token": get_access_token(
            sub=str(user.id)
        ),
        "token_type": "bearer",
        "user_email": user.email,
        "user_id": user.id
    }


@router.patch(
    path="/{user_id}",
    response_model=UserSchemaBasic
)
async def update_user_by_user_id_(
        user_id: UserIdSchema,
        user_target: UserSchemaUpdate,
        user_id_logged: str = Depends(get_user_id_from_token),
        admin_user=Depends(admin_authorization)
):
    """
    This route allows you to update a user's record through their ID.
    """
    if (user_target.status == 0) and (user_id == int(user_id_logged)):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="You Can't Disable Yourself"
        )

    try:
        user_updated: Optional[UserModel] = await update_user_by_id(
            user_id=user_id,
            name=user_target.name,
            email=user_target.email,
            status=user_target.status,
            last_change_owner=int(user_id_logged)
        )

        if not user_updated:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User Not Found"
            )
        return user_updated

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="That email address is already in use."
        )


@router.patch(
    path="/password/reset/{user_id}",
    response_model=UserSchemaBasic
)
async def reset_user_password_by_user_id_(
        user_id: UserIdSchema,
        user_id_logged: str = Depends(get_user_id_from_token),
        admin_user=Depends(admin_authorization)
):
    """
    This route allows resetting the password of a user registered
    in the database. The generated password is sent to the target
    user's registration email.
    """
    new_password: str = await generate_password()

    user_updated: Optional[UserModel] = await update_user_by_id(
        user_id=user_id,
        password=new_password,
        last_change_owner=int(user_id_logged)
    )
    if not user_updated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User Not Found"
        )

    await send_email_async(
        subject="Your New Password",
        email_to=[f"{user_updated.email}"],
        body=f"Your new password is: {new_password}"
    )
    return user_updated


@router.patch(
    path="/password/update/{user_id}",
    response_model=UserSchemaBasic
)
async def update_password_(
        user_id: UserIdSchema,
        user: UserSchemaUpdatePassword,
        user_id_logged: str = Depends(get_user_id_from_token)
):
    """
    This route allows the user to change his password. The new
    password must contain at least 8 characters, uppercase
    letters, special characters and numbers.
    """
    if user_id != int(user_id_logged):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="You Cannot Change Another User's Password"
        )

    if not validate_password_string(
            user.new_password
    ):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Password must contain at least 8 characters, capital letters, number and special character"
        )

    user_updated: Optional[UserModel] = await update_user_by_id(
        user_id=user_id,
        password=user.new_password,
        last_change_owner=int(user_id_logged)
    )
    return user_updated
