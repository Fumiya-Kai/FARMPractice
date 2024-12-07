from decouple import config
from typing import Union
import motor.motor_asyncio

MONG_API_KEY = config('MONGO_API_KEY')

client = motor.motor_asyncio.AsyncIOMotorClient(MONG_API_KEY)
database = client.API_DB
collection_user = database.user
collection_todo = database.todo

def todo_serializer(todo) -> dict:
  return {
    "id": str(todo["_id"]),
    "title": todo["title"],
    "description": todo["description"]
  }

async def db_create_todo(data: dict) -> Union [dict, bool]:
  todo = await collection_todo.insert_one(data)
  new_todo = await collection_todo.find_one({"_id": todo.inserted_id})
  if new_todo:
    return todo_serializer(new_todo)
  return False