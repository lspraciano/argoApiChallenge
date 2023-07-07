from fastapi import APIRouter

from app.schemas.users_schema import UserSchemaBasic

router = APIRouter()


@router.get(
    path="",
    response_model=UserSchemaBasic
)
async def get_all_users_():
    """
    Esta é a primeira rota. Apenas para teste
    """

    return {
        "id": 1,
        "name": "Lucas",
        "email": "lspraciano@gmail.com",
        "status": 1
    }
