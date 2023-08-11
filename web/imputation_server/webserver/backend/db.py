from tortoise import Tortoise, run_async

async def do_stuff():
    """关闭数据库"""
    await Tortoise.close_connections()


async def init():
    """创建数据库"""
    await Tortoise.init(
        db_url='mysql://root:e8c87vb2@118.195.223.193:3306/imputationcomputed',
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas()

if __name__ == '__main__':
    run_async(init())  # 创建数据库
    run_async(do_stuff())  # 清理数据库连接