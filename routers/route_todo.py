from fastapi import APIRouter
from fastapi import Request, Response, HTTPException
from fastapi.encoders import jsonable_encoder
from database import db_create_todo, db_get_todos, db_get_single_todo, db_update_todo
from schemas import Todo, TodoBody
from starlette.status import HTTP_201_CREATED
from typing import List

router = APIRouter()

@router.post("/api/todo", response_model=Todo)
async def create_todo(request: Request, response: Response, data: TodoBody):
  todo = jsonable_encoder(data)
  res = await db_create_todo(todo)
  response.status_code = HTTP_201_CREATED
  if res:
    return res
  raise HTTPException(status_code=404, detail="Create task failed")

@router.get("/api/todos", response_model=List[Todo])
async def get_todos():
  todos = await db_get_todos()
  return todos

@router.get("/api/todos/{id}", response_model=Todo)
async def get_single_todo(id: str):
  todo = await db_get_single_todo(id)
  if todo:
    return todo
  raise HTTPException(status_code=404, detail=f"Task of ID:{id} doesn't exist")

@router.put("/api/todos/{id}", response_model=Todo)
async def update_todo(id: str, data: TodoBody):
  todo = jsonable_encoder(data)
  updated_todo = await db_update_todo(id, todo)
  if updated_todo:
    return updated_todo
  raise HTTPException(status_code=404, detail="Update task failed")