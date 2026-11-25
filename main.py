from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Todo API")


# Todo model
class Todo(BaseModel):
    title: str
    completed: bool = False


# Temporary in-memory storage
todos = []


# Home route
@app.get("/")
def home():
    return {
        "message": "Todo API is running"
    }


# Get all todos
@app.get("/todos")
def get_todos():
    return todos


# Get a single todo
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):

    if todo_id < 0 or todo_id >= len(todos):
        raise HTTPException(status_code=404, detail="Todo not found")

    return todos[todo_id]


# Create a new todo
@app.post("/todos")
def create_todo(todo: Todo):

    new_todo = {
        "id": len(todos),
        "title": todo.title,
        "completed": todo.completed
    }

    todos.append(new_todo)

    return new_todo


# Update a todo
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: Todo):

    if todo_id < 0 or todo_id >= len(todos):
        raise HTTPException(status_code=404, detail="Todo not found")

    todos[todo_id] = {
        "id": todo_id,
        "title": todo.title,
        "completed": todo.completed
    }

    return todos[todo_id]


# Delete a todo
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):

    if todo_id < 0 or todo_id >= len(todos):
        raise HTTPException(status_code=404, detail="Todo not found")

    deleted_todo = todos.pop(todo_id)

    return {
        "message": "Todo deleted successfully",
        "todo": deleted_todo
    }


# Health check
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }