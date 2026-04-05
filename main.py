from fastapi import FastAPI, HTTPException
from typing import List
from schemas import Task, TaskCreate

app = FastAPI()

# Збереження даних в пам'яті
tasks = {}
task_id_counter = 1


@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return list(tasks.values())


@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    global task_id_counter
    new_task = Task(id=task_id_counter, **task.model_dump())
    tasks[task_id_counter] = new_task
    task_id_counter += 1
    return new_task


@app.put("/tasks/{id}", response_model=Task)
def update_task(id: int, updated_task: TaskCreate):
    if id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    task = Task(id=id, **updated_task.model_dump())
    tasks[id] = task
    return task


@app.delete("/tasks/{id}")
def delete_task(id: int):
    if id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    del tasks[id]
    return {"message": "Task deleted"}