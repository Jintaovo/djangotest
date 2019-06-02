from django.db import models
# Create your models here.
# 出版社表
class Publisher(models.Model):
    # 自增的ID主键
    id = models.AutoField(primary_key=True)
    # 创建一个varchar(64)的唯一的不为空的字段，且不能为空，且不重复
    name = models.CharField(max_length=64, null=False, unique=True)

# 书籍表
class Book(models.Model):
    # 自增的ID主键
    id = models.AutoField(primary_key=True)
    # 创建一个varchar(64)的唯一的不为空的字段，且不能为空，且不重复
    title = models.CharField(max_length=64, null=False, unique=True)
    # 告诉ORM我这张表和Publisher表是关联关系，ORM自动帮我创建关联ID （publisher_id）字段
    publisher = models.ForeignKey(to="Publisher")

# 作者表
class Author(models.Model):
    # 自增的ID主键
    id = models.AutoField(primary_key=True)
    # 创建一个varchar(64)的唯一的不为空的字段，且不能为空，且不重复
    name = models.CharField(max_length=16, null=False, unique=True)
    # 告诉ORM 我这张表和book表是多对多的关联关系，ORM自动帮我生成了第三张表
    book = models.ManyToManyField(to="Book")