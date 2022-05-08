from typing import List
from fastapi import Body, FastAPI
from database import app_start_up_handler
from models import Task
from schemas import TasksSchema, NewTaskSchema, TaskCompleteSchema  

def get_application():

    app = FastAPI()

    app.add_event_handler("startup", app_start_up_handler(app))

    return app

app = get_application()


@app.get("/", response_model=List[TasksSchema])
async def allTasks() -> List:
    """Returns all tasks from the DB"""
    return await Task.all()


@app.get("/task/", response_model=TasksSchema)
async def getTask(title: str):
    """Returns a specific task using the title as a query param"""
    return await Task.get(title=title)


@app.get("/tasks/completed/", response_model=List[TaskCompleteSchema])
async def getTask():
    """Returns all the completed tasks in the DB"""
    taskz = await Task.all()
    return [task for task in taskz if task.completed == True]


@app.post("/new-task/", response_model=TasksSchema)
async def createTask(data: NewTaskSchema):
    """Creates a new task and saves to the DB"""
    new_task = await Task.create(
        **data.dict()
    )
    return new_task


@app.put("/task/", response_model=TaskCompleteSchema)
async def updateTask(title: str = Body(..., embed=True)):
    """Updates the status of a task to completed"""
    task = await Task.get(title=title)
    task.completed = True
    await task.save()
    return task
    