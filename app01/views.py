from django.shortcuts import render, redirect, HttpResponse
    from app01 import models
    # Create your views here.

# 展示出版社列表
def publisher_list(request):
    # 去数据库查出所有的出版社，填充到HTML中，给用户返回
    ret = models.Publisher.objects.all().order_by("id")
    return render(request, 'publisher_list.html', {"publisher": ret})

# 添加新的出版社
def add_publisher(request):
    error = ""
    # 如果是POST请求，我就取到用户填写的数据
    if request.method == "POST":
        add_publisher = request.POST.get("add_name")
        if add_publisher:
            # 从数据库中获取所以的出版社
            all_publisher = models.Publisher.objects.all()
            # 循环判断新添加的出版社名字是否已经存在
            for i in all_publisher:
                # 如果存在返回错误提示
                if i.name == add_publisher:
                    error = "%s 已经存在" % (add_publisher)
                    return render(request,'add_publisher.html', {"error": error})
            # 通过ORM去数据库里创建一条记录
            models.Publisher.objects.create(name=add_publisher)
            # 引导用户访问出版社列表页，查看是否添加成功 ———> 跳转
            return redirect("/publisher_list/")
        else:
            error = "error：出版社名字不能为空 ！"
    # 用户第一次来，我给他返回一个用来填写的HTML页面
    return render(request,'add_publisher.html', {"error": error})

# 删除出版社
def delete_publisher(request):
    # 删除指定的数据
    # 1. 从GET请求的参数里面拿到将要删除的ID值
    del_id = request.GET.get("id") # 字典取值，取不到默认为None
    # 如果取到id值
    if del_id:
        # 去数据库删除当前的id值的数据
        # 1.根据id值查找到数据并进行删除
        models.Publisher.objects.get(id=del_id).delete()
        # 上面这句删除还可以用这种方式如下：
        # del_obj = models.Publisher.objects.get(id=del_id)
        # del_obj.delete()
        # 返回删除后的页面，跳转到出版社的列表页，查看删除是否成功
        return redirect("/publisher_list/")
    else:
        return HttpResponse('<h1 style="color: red">ERROR : 删除的出版社不存在 !</h1>')

# 编辑出版社
def edit_publisher(request):
    # 用户修改完出版社的名字，点击提交按钮，给我发来新的出版社名字
    if request.method == "POST":
        # 取新出版社的名字
        edit_id = request.POST.get("id")
        edit_newname = request.POST.get("name")
        # 更新出版社（数据库）
        edit_publisher = models.Publisher.objects.get(id=edit_id)
        edit_publisher.name = edit_newname
        edit_publisher.save()  # 把修改提交到数据库
        # 跳转到出版社列表页，查看是否修改成功
        return redirect("/publisher_list/")
        # 根据id取到编辑的是哪个出版社
    # 从GET请求的URL中取到id参数
    edit_id = request.GET.get("id")
    if edit_id:
        # 获取到当前编辑的出版社对象
        edit_obj = models.Publisher.objects.get(id=edit_id)
        return render(request, "edit_publisher.html", {"publisher": edit_obj})
    else:
        return HttpResponse('<h1 style="color: red">ERROR : 编辑的出版社不存在 !</h1>')

# 展示书籍
def book_list(request):
    # 去数据库中查询所有的书籍
    all_book = models.Book.objects.all().order_by("id")
    # 在HTML页面完成字符串替换(渲染书籍)
    return render(request, "book_list.html", {"all_book": all_book})

# 添加书籍
def add_book(request):
    error = ""
    if request.method == "POST":
        # 获取新书的名字
        add_name = request.POST.get("book_name")
        # 获取新书的出版社
        publisher = request.POST.get("publisher_id")
        if add_name:
            # 创建新书对象, 自动提交   (创建方法一)
            models.Book.objects.create(title=add_name, publisher_id=publisher)
            # 返回到书籍列表页
            return redirect("/book_list/")
        else:
            error = "error：书名不能为空！"
    # 取到所有的出版社
    ret = models.Publisher.objects.all()
    return render(request, "add_book.html", {"publisher_list": ret, "error": error})

# 删除书籍
def delete_book(request):
    delete_id = request.GET.get("id")
    if delete_id:
        # 去删除数据库中删除指定id的数据
        models.Book.objects.get(id=delete_id).delete()
        # 返回书籍列表页面，查看是否删除成功
        return redirect("/book_list")
    else:
        return HttpResponse('<h1 style="color: red">ERROR : 删除的书籍不存在 !</h1>')

# 编辑书籍
def edit_book(request):
    # 从URL里面获取要删除的书籍的id值
    if request.method == "POST":
        edit_id = request.POST.get("id")
        if edit_id:
            # 从提交的数据里面取，书名和书名关联的出版社
            new_publisher_id = request.POST.get("publisher")
            new_name = request.POST.get("book_name")
            # 更新
            edit_book_obj = models.Book.objects.get(id=edit_id)
            edit_book_obj.title = new_name   # 更新书名
            edit_book_obj.publisher_id = new_publisher_id   # 更新书籍关联的出版社
            # 将修改提交到数据库
            edit_book_obj.save()
            # 返回书籍列表页，查看是否编辑成功
            return redirect("/book_list/")
    # 取到编辑的书的id值
    edit_id = request.GET.get("id")
    if edit_id:
        publisher_list = models.Publisher.objects.all()
        edit_obj = models.Book.objects.get(id=edit_id)
        # 返回一个页面，让用户编辑书籍信息
        return render(request, "edit_book.html", {"book_obj": edit_obj, "publisher_list": publisher_list})
    else:
        return HttpResponse('<h1 style="color: red">ERROR : 编辑的书籍不存在 !</h1>')

# 作者列表
def author_list(request):
    # 查询所有的作者
    author_obj = models.Author.objects.get(id=1)
    print(author_obj)
    all_author = models.Author.objects.all().order_by("id")
    return render(request, "author_list.html", {"author_list":all_author})

# 添加作者
def add_author(request):
    error = ""
    if request.method == "POST":
        # 取到提交的数据
        new_author_name = request.POST.get("author_name")
        if new_author_name:
            # post提交的数据是多个值的时候，一定要用getlist ， 如多选的checkbox和多选的select
            books = request.POST.getlist("books")
            # 创建作者
            new_author_obj = models.Author.objects.create(name=new_author_name)
            # 把新作者和书籍建立对应关系,自动提交
            new_author_obj.book.set(books)
            # 跳转到作者列表页面，查看是否添加成功
            return redirect("/author_list/")
        else:
            error = "error：作者不能为空！"
    # 查询所有的书籍
    ret = models.Book.objects.all()
    return render(request, "add_author.html", {"book_list": ret, "error": error})

# 删除作者
def delete_author(request):
    # 从URl中获取需要删除的作者的ID值
    delete_id = request.GET.get("id")
    if delete_id:
        # 如果获取到值，那么进行删除
        models.Author.objects.get(id=delete_id).delete()
        # 跳转到作者列表页，查看是否删除成功
        return redirect("/author_list/")
    else:
        return HttpResponse('<h1 style="color: red">ERROR : 删除的作者不存在 !</h1>')

# 编辑作者
def edit_author(request):
    # 如果编辑完提交数据过来
    if request.method == "POST":
        # 拿到提交过来的编辑后的数据
        edit_author_id = request.POST.get("author_id")
        new_author_name = request.POST.get("author_name")
        # 拿到编辑后作者关联的书籍信息
        new_books = request.POST.getlist("books")
        # 根据ID找到当前编辑的作者对象
        edit_author_obj = models.Author.objects.get(id=edit_author_id)
        # 更新作者的名字
        edit_author_obj.name = new_author_name
        # 更新作者关联的书的对应关系
        edit_author_obj.book.set(new_books)
        # 将修改提交到数据库
        edit_author_obj.save()
        # 返回作者列表页,查看是否编辑成功
        return redirect("/author_list/")
    # 从URL里面取要编辑的作者的id信息
    edit_id = request.GET.get("id")
    # 找到要编辑的作者对象
    edit_author_obj = models.Author.objects.get(id=edit_id)
    # 查询所有的书籍对象
    ret = models.Book.objects.all()
    return render(request, "edit_author.html", {"book_list": ret, "author": edit_author_obj})

views.py