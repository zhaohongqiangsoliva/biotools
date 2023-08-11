from tortoise.contrib.pydantic import pydantic_model_creator

from models import Task

Task_Pydantic = pydantic_model_creator(Task, name="Task")
TaskIn_Pydantic = pydantic_model_creator(Task, name="TaskIn", exclude_readonly=True)