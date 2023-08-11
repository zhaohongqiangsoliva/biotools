"""
# 存储数据库相关的操作
"""
from app import db
from werkzeug.security import  generate_password_hash, check_password_hash
from datetime import  datetime



# 用户和任务的关系: 一对多， 用户是一， 任务是多，
# 用户和分类的关系:
class User(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(30), unique=True)
    add_time = db.Column(db.DateTime, default=datetime.now()) # 账户创建时间
    # 1).  User添加属性todos; 2). Todo添加属性user;
    todos = db.relationship('Todo', backref="user")
    categories = db.relationship('Category', backref='user')

    @property
    def password(self):
        """u.password"""
        raise  AttributeError("密码属性不可以读取")

    @password.setter
    def password(self, password):
        """u.password = xxxxx """
        self.password_hash = generate_password_hash(password)


    def verify_password(self, password):
        """验证密码是否正确"""
        return  check_password_hash(self.password_hash, password)

    def __repr__(self):
        return  "<User %s>" %(self.username)

# 任务和分类的关系： 一对多
# 分类是一， 任务是多, 外键写在多的一端
class Todo(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    content = db.Column(db.String(100)) # 任务内容
    status = db.Column(db.Boolean, default=False) # 任务的状态
    add_time = db.Column(db.DateTime, default=datetime.now())  # 任务创建时间
    # 任务的类型,关联另外一个表的id
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    # 任务所属用户;
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return  "<Todo %s>" %(self.content[:6])


class Category(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    add_time = db.Column(db.DateTime, default=datetime.now())  # 任务创建时间
    # 1). Category添加一个属性todos, 2). Todo添加属性category；
    todos = db.relationship('Todo', backref='category')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return  "<Category %s>" %(self.name)

# 初始化，用于测试数据库，实际代码不用写，因为把初始化数据库写在models.py文件中更为方便
def init():
    db.drop_all()
    db.create_all()
    u = User(username='admin',email='admin@qq.com')
    u.password='admin'
    db.session.add(u)
    db.session.commit()
    print('用户%s创建成功' %(u.username))
    c = Category(name='学习',user_id=1)
    db.session.add(c)
    print('分类%s创建成功' %(c.name))

    t = Todo(content='学习flask',category_id=1,user_id=1)
    db.session.add(t)
    print('任务%s添加成功' %(t.content))

    db.session.commit()


if __name__ == '__main__':
    init()
