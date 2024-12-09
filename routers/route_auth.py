from fastapi import APIRouter
from fastapi import Request, Response
from fastapi.encoders import jsonable_encoder
from schemas import UserBody, SuccessMsg, UserInfo
from database import (
  db_signup
)
from auth_utils import AuthJwtCsrf

router = APIRouter()
auth = AuthJwtCsrf()

@router.post("/api/register", response_model=UserInfo)
async def signup(user: UserBody):
  user = jsonable_encoder(user)
  new_user = await db_signup(user)
  return new_user