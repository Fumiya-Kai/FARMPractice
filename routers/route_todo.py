from fastapi import APIRouter
from fastapi import Request, Response, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_csrf_protect import CsrfProtect
from database import db_create_todo, db_get_todos, db_get_single_todo, db_update_todo, db_delete_todo
from schemas import Todo, TodoBody, SuccessMsg
from starlette.status import HTTP_201_CREATED
from typing import List
from auth_utils import AuthJwtCsrf

router = APIRouter()
auth = AuthJwtCsrf()

@router.post("/api/todo", response_model=Todo)
async def create_todo(request: Request, response: Response, data: TodoBody, csrf_protect: CsrfProtect = Depends()):
  new_token = auth.verify_csrf_update_jwt(request, csrf_protect, request.headers)
  todo = jsonable_encoder(data)
  res = await db_create_todo(todo)
  response.status_code = HTTP_201_CREATED
  response.set_cookie(key="access_token", value=f"Bearer {new_token}", httponly=True, samesite="none", secure=True)
  if res:
    return res
  raise HTTPException(status_code=404, detail="Create task failed")

@router.get("/api/todos", response_model=List[Todo])
async def get_todos(request: Request):
  auth.verify_jwt(request)
  todos = await db_get_todos()
  return todos

@router.get("/api/todos/{id}", response_model=Todo)
async def get_single_todo(id: str, request: Request, response: Response):
  new_token, _ = auth.verify_update_jwt(request)
  todo = await db_get_single_todo(id)
  response.set_cookie(key="access_token", value=f"Bearer {new_token}", httponly=True, samesite="none", secure=True)
  if todo:
    return todo
  raise HTTPException(status_code=404, detail=f"Task of ID:{id} doesn't exist")

@router.put("/api/todos/{id}", response_model=Todo)
async def update_todo(id: str, data: TodoBody, request: Request, response: Response, csrf_protect: CsrfProtect = Depends()):
  new_token = auth.verify_csrf_update_jwt(request, csrf_protect, request.headers)
  todo = jsonable_encoder(data)
  updated_todo = await db_update_todo(id, todo)
  response.set_cookie(key="access_token", value=f"Bearer {new_token}", httponly=True, samesite="none", secure=True)
  if updated_todo:
    return updated_todo
  raise HTTPException(status_code=404, detail="Update task failed")

@router.delete("/api/todos/{id}", response_model=SuccessMsg)
async def update_todo(id: str, request: Request, response: Response, csrf_protect: CsrfProtect = Depends()):
  new_token = auth.verify_csrf_update_jwt(request, csrf_protect, request.headers)
  deleted_todo = await db_delete_todo(id)
  response.set_cookie(key="access_token", value=f"Bearer {new_token}", httponly=True, samesite="none", secure=True)
  if deleted_todo:
    return {"message": "Successfully deleted"}
  raise HTTPException(status_code=404, detail="Delete task failed")