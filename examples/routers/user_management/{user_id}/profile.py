from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def get_user_profile(user_id: str):
    return {
        "message": f"Get profile for user {user_id}"
    } 