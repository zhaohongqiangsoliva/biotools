from fastapi import APIRouter, Depends,FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from models import User
from core import verify_password, create_access_token, deps
from scheams import (
    UserIn_Pydantic,
    Response400,
    ResponseToken,
    Response200,
    User_Pydantic,
)

login = APIRouter(tags=["认证相关"])


@login.post("/login", summary="登录")
async def user_login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    if user := await User.get(username=form_data.username):
        if verify_password(form_data.password, user.password):
            token = create_access_token({"sub": user.username})
            # s
            # await request.app.state.redis.set(user.username, token, 180)
            #return ResponseToken(data={"token": f"bearer {token}"}, access_token=token)
    return Response400(msg="请求失败.")




@login.get("/login", summary="登录2" )
async def user_login2(username,password):
    return JSONResponse(content={"code": 0, "message": "Custom Code 0","msg":"接口调用成功","token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXNzd29yZCI6IjYwMDU1NDU1ODlmZmI2MDdiYzdmOWY5MGNlNDRlMzFkIiwiZXhwIjoxNjg2MDQzNjg5LCJlbWFpbCI6IjE1MTEwMTUxMzAxQDE2My5jb20ifQ.13xDnibXFe1JI7zhrC-BDtWmxEmpbdaJqZ-LRAKmcZU"})
    #if user := await User.get(username=form_data.username):
        # if verify_password(form_data.password, user.password):
        #     token = create_access_token({"sub": user.username})
        #     # s
        #     # await request.app.state.redis.set(user.username, token, 180)
        #     return ResponseToken(data={"token": f"bearer {token}"}, access_token=token)
    #return Response400(msg="请求失败.")

@login.put("/logout", summary="注销")
async def user_logout(request: Request, user: User = Depends(deps.get_current_user)):
    request.app.state.redis.delete(user.username)
    return Response200()


@login.post("/user", summary="用户新增")
async def user_create(user: UserIn_Pydantic):
    if await User.filter(username=user.username):
        return Response400(msg="用户已存在.")
    return Response200(
        data=await User_Pydantic.from_tortoise_orm(await User.create(**user.dict()))
    )
