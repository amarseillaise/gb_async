from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response

from bson import ObjectId
import motor.motor_asyncio
from pymongo import ReturnDocument
from fst_api2.models import TaskModel, UpdateTaskModel, TaskCollection

MONGO_DB_URL = 'mongodb://localhost:27017/'

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DB_URL)
db = client.tasks
task_collection = db.get_collection("tasks")




@app.post(
    "/tasks/",
    response_description="Add new task",
    response_model=TaskModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_task(task: TaskModel = Body(...)):
    new_task = await task_collection.insert_one(
        task.model_dump(by_alias=True, exclude=["id"])
    )
    created_student = await task_collection.find_one(
        {"_id": new_task.inserted_id}
    )
    return created_student


@app.get(
    "/tasks/",
    response_description="List all tasks",
    response_model=TaskCollection,
    response_model_by_alias=False,
)
async def list_tasks():
    return TaskCollection(tasks=await task_collection.find().to_list(1000))


@app.get(
    "/tasks/{id}",
    response_description="Get a single task",
    response_model=TaskModel,
    response_model_by_alias=False,
)
async def show_task(id: str):
    if (
        student := await task_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return student

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@app.put(
    "/tasks/{id}",
    response_description="Update a task",
    response_model=TaskModel,
    response_model_by_alias=False,
)
async def update_task(id: str, task: UpdateTaskModel = Body(...)):
    task = {
        k: v for k, v in task.model_dump(by_alias=True).items() if v is not None
    }

    if len(task) >= 1:
        update_result = await task_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": task},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Task {id} not found")

    if (existing_student := await task_collection.find_one({"_id": id})) is not None:
        return existing_student

    raise HTTPException(status_code=404, detail=f"Task {id} not found")


@app.delete("/tasks/{id}", response_description="Delete a task")
async def delete_task(id: str):
    """
    Remove a single student record from the database.
    """
    delete_result = await task_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Task {id} not found")