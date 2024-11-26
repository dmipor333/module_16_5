from fastapi import FastAPI, status, Body, HTTPException, Request, Form, Path
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates
from typing import Annotated, List

app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)
templates = Jinja2Templates(directory="Lesson16/templates")

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/")
async def main_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/user/{user_id")
async def get_users(request: Request, user_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse("users.html", {"request": request, "user": users[user_id - 1]})
    except IndexError:
        raise HTTPException(status_code=404, detail="User not found")


@app.post("/user/{username}/{age}")
async def old_users(user: User, username: str, age: int) -> str:
    if users:
        current_index = max(user.id for user in users) + 1
    else:
        current_index = 1
    user.id = current_index
    user.username = username
    user.age = age
    users.append(user)
    return f'User {current_index} is registered.'


@app.put("/user/{user_id}/{username}/{age}")
async def put_user(user_id: int, username: str, age: int) -> str:
    for i in users:
        if i.id == user_id:
            try:
                i.username = username
                i.age = age
                return f'User {user_id} has been updated.'
            except IndexError:
                raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def delete_user(user_id: int) -> str:
    for index, i in enumerate(users):
        if i.id == user_id:
            users.pop(index)
            return f'User ID {user_id} deleted'
        raise HTTPException(status_code=404, detail='User was not found.')

#  python -m uvicorn Lesson16.module_16_5:app
#  uvicorn Lesson16.module_16_5:app --reload