from typing import List, Any, Union

from fastapi import APIRouter, Depends , Cookie

from core import deps
from models import Task
from models import User
from scheams import Task_Pydantic, TaskIn_Pydantic, Response200, Response400


jobs = APIRouter(tags=["JOBS"])


# @jobs.get("/jobs", summary="JOBlist", response_model=Union[Response200, Response400])
# async def jobs_list(limit: int = 10, page: int = 1):
#     skip = (page - 1) * limit
#     data = {
#         "total": await Task.all().count(),
#         "Tasks": await Task_Pydantic.from_queryset(Task.all().offset(skip).limit(limit).order_by('-id'))
#     }
#     return Response200(data=data)

@jobs.get("/jobs/query", summary="JOBlist", response_model=Union[Response200, Response400])
async def jobs_list(userName):
    # skip = (page - 1) * limit

    print(userName)
    user =  await User.filter(userName=userName).first()

    data = {
        
        "Tasks": await Task_Pydantic.from_queryset(Task.filter(userId=user.userId).order_by('-id')) #.offset(skip).limit(limit)
    }
    return Response200(data=data)


@jobs.post("/jobs", summary="submitJOBS")
async def jobs_create(Task_form: TaskIn_Pydantic, token: Any = Depends(deps.get_current_user)):
    return Response200(data=await Task_Pydantic.from_tortoise_orm(await Task.create(**Task_form.dict())))


@jobs.put("/jobs/{pk}", summary="编辑电影")
async def jobs_update(pk: int, Task_form: TaskIn_Pydantic, token: Any = Depends(deps.get_current_user)):
    if await Task.filter(pk=pk).update(**Task_form.dict()):
        return Response200()
    return Response400(msg="更新失败")


@jobs.delete("/jobs/{pk}", summary="removeJOBS")
async def jobs_delete(pk: int, token: Any = Depends(deps.get_current_user)):
    if await Task.filter(pk=pk).delete():
        return Response200()
    return Response400(msg="删除失败")
