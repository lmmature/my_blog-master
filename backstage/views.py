from django.shortcuts import render, HttpResponse, redirect
from .models import T_title, T_content, T_type, T_article_images
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import time
import json


# Create your views here.


@csrf_exempt
# @login_required
def add_markdown(request, ):
    if not request.user.is_authenticated:
        if request.method == "POST":
            get_json = request.POST
            title = get_json['title']
            if T_title.objects.filter(title__exact=title):
                return HttpResponse("标题已经存在")
            article_type = get_json['type']
            time = get_json['time']
            content = get_json['content']
            get_md = get_json['md']
            if get_json['description']:  # 有写简述就直接存简述，否则截断内容的前五十个字符来进行填充
                description = get_json['description']
            else:
                description = content[0:50]
            typeid = T_type.objects.filter(type=article_type)[0].type_id  # 取类型编码
            p = T_article_images.objects.filter(belong=None)  # 获取所有没有归属的图片
            if p:
                t = T_title(title=title, time=time, type_id=typeid, description=description, img=p[0].img)
            else:
                t = T_title(title=title, time=time, type_id=typeid, description=description)
            # 保存title表
            t.save()
            t_id = T_title.objects.filter(title=title)[0].id  # 取title_id号码
            t = T_content(t_id=t_id, content=content, markdown_text=get_md)  # 存内容表
            t.save()
            if p:
                p.update(belong=t_id)  # 建立图片和文章的关系
            return HttpResponse("保存成功")
        types = T_type.objects.values('type')  # 获取类型填充select
        return render(request, "backstage/markdown.html", {"types": list(types)})


# @login_required
@csrf_exempt
def add_text(request, ):
    if not request.user.is_authenticated:
        if request.method == "POST":
            get_json = request.POST
            title = get_json['title']
            if T_title.objects.filter(title__exact=title):
                return HttpResponse("标题已经存在")
            article_type = get_json['type']
            time = get_json['time']
            content = get_json['content']
            if get_json['description']:  # 有写简述就直接存简述，否则截断内容的前五十个字符来进行填充
                description = get_json['description']
            else:
                description = content[0:50]
            typeid = T_type.objects.filter(type=article_type)[0].type_id  # 取类型编码
            t = T_title(title=title, time=time, type_id=typeid, description=description)
            # 保存title表
            t.save()
            t_id = T_title.objects.filter(title=title)[0].id  # 取title_id号码
            t = T_content(t_id=t_id, content=content)  # 存内容表
            t.save()
            return HttpResponse("保存成功")
        types = T_type.objects.values('type')  # 获取类型填充select
        return render(request, 'backstage/add.html', {"types": list(types)})


# @login_required
def index(request, ):
    if not request.user.is_authenticated:
        return render(request, 'backstage/index.html')


# @login_required
@csrf_exempt
def manage(request, ):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            get_id = request.POST.get('id')  # 获取参数时要用键值关系
            get_num = request.POST.get('num')  # 获取翻页
            get_all = request.POST.get('all')  # 获取批量删除
            get_statue = request.POST.get('statue')  # 获取展示命令
            if get_statue is not None:
                T_title.objects.filter(id=get_id).update(show=get_statue)
                return HttpResponse("修改成功")
            if get_id:  # 单一删除
                try:
                    T_content.objects.get(id=get_id).delete()
                    T_title.objects.get(id=get_id).delete()
                    if T_article_images.objects.filter(belong=get_id).exists():  # 有图片则删除
                        imgs = T_article_images.objects.filter(belong=get_id)
                        for var in imgs:  # 先删除本地文件
                            var.img.delete(save=True)
                        imgs.delete()  # 删除记录
                    return HttpResponse(status=200)
                except:
                    return HttpResponse(status=500)
            elif get_num:  # 获取翻页
                content = list(T_title.objects.filter(show='1')[9 * (int(get_num) - 1):int(get_num) * 9])
                result = []
                for var in content:
                    itm = {}
                    itm["id"] = var.id
                    itm["title"] = var.title
                    itm["description"] = var.description
                    itm["time"] = var.time
                    itm['url'] = T_article_images.objects.get(belong=var.id).img.url[0]
                    result.append(itm)
                return HttpResponse(json.dumps(result))
            elif get_all:  # 批量删除
                try:
                    for var in json.loads(get_all):
                        T_content.objects.get(id=var).delete()
                        T_title.objects.get(id=var).delete()
                        if T_article_images.objects.filter(belong=var).exists():
                            imgs = T_article_images.objects.filter(belong=var)
                            for vars in imgs:  # 先删除本地文件
                                vars.img.delete(save=True)
                            imgs.delete()  # 删除数据库记录
                    return HttpResponse(status=200)
                except:
                    return HttpResponse(status=500)
        content = list(T_title.objects.filter(show='1')[:9])  # 首页
        total = T_title.objects.filter(show='1').count()
        if total % 9 == 0:
            length = total / 9  # 获取页数
        else:
            length = total / 9 + 1
        statue = 1
        return render(request, 'backstage/manage.html',
                      {'statue': statue, 'content': content, "length": range(0, int(length))})


# @login_required()
@csrf_exempt
def manage_hide(request, ):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            get_id = request.POST.get('id')  # 获取参数时要用键值关系
            get_num = request.POST.get('num')  # 获取翻页
            get_all = request.POST.get('all')  # 获取批量删除
            get_statue = request.POST.get('statue')  # 获取展示命令
            if get_statue is not None:
                T_title.objects.filter(id=get_id).update(show=get_statue)
                return HttpResponse("修改成功")
            if get_id:  # 单一删除
                try:
                    T_content.objects.get(id=get_id).delete()
                    T_title.objects.get(id=get_id).delete()
                    if T_article_images.objects.filter(belong=get_id).exists():  # 有图片则删除
                        imgs = T_article_images.objects.filter(belong=get_id)
                        for var in imgs:  # 先删除本地文件
                            var.img.delete(save=True)
                        imgs.delete()  # 删除记录
                    return HttpResponse(status=200)
                except:
                    return HttpResponse(status=500)
            elif get_num:  # 获取翻页
                content = list(T_title.objects.filter(show='0')[9 * (int(get_num) - 1):int(get_num) * 9])
                result = []
                for var in content:
                    itm = {}
                    itm["id"] = var.id
                    itm["title"] = var.title
                    itm["description"] = var.description
                    itm["time"] = var.time
                    itm['url'] = T_article_images.objects.get(belong=var.id).img.url[0]
                    result.append(itm)
                return HttpResponse(json.dumps(result))
            elif get_all:  # 批量删除
                try:
                    for var in json.loads(get_all):
                        T_content.objects.get(id=var).delete()
                        T_title.objects.get(id=var).delete()
                        if T_article_images.objects.filter(belong=var).exists():
                            imgs = T_article_images.objects.filter(belong=var)
                            for vars in imgs:  # 先删除本地文件
                                vars.img.delete(save=True)
                            imgs.delete()  # 删除数据库记录
                    return HttpResponse(status=200)
                except:
                    return HttpResponse(status=500)
        content = list(T_title.objects.filter(show='0')[:9])  # 首页
        total = T_title.objects.filter(show='0').count()
        if total % 9 == 0:
            length = total / 9  # 获取页数
        else:
            length = total / 9 + 1
        statue = 0
        return render(request, 'backstage/manage.html',
                      {'statue': statue, 'content': content, "length": range(0, int(length))})


# @login_required
def article_sum(request, ):
    if not request.user.is_authenticated:
        types = T_type.objects.values('type')  # 获取类型填充select
        return render(request, 'backstage/wenzhangtongji.html', {"types": list(types), "num": len(list(types))})


# @login_required
@csrf_exempt
def edit(request, get_id):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            get_json = request.POST
            title = get_json['title']
            article_type = get_json['type']
            time = get_json['time']
            description = get_json['description']
            content = get_json['content']
            get_md = get_json['md']
            type_id = T_type.objects.filter(type__exact=article_type)[0].type_id  # 拿类型编码
            T_title.objects.filter(id=get_id).update(type_id=type_id, time=time, title=title,
                                                     description=description)  # 更新内容
            T_content.objects.filter(t_id=get_id).update(content=content, markdown_text=get_md)
            return HttpResponse("已更新, 刷新生效")
        title = T_title.objects.filter(id=get_id)[0]  # 展示内容
        c = T_content.objects.filter(t_id=title.id)[0]
        type = T_type.objects.filter(type_id=title.type_id)[0].type
        types = list(T_type.objects.values("type"))
        flag = True  # 默认为普通文本
        content = c.content
        if c.markdown_text:
            content = c.markdown_text
            flag = False
        return render(request, "backstage/edit.html", locals())


def out(request, ):
    if not request.user.is_authenticated:
        return redirect("cas_ng_logout")
    # return HttpResponse("您未登录")


@csrf_exempt
def upload(request, ):
    if not request.user.is_authenticated:
        if request.method == "GET":
            return render(request, "backstage/index.html")
        # upload_time = time.strftime('%Y/%m/%d/%H/%M', time.localtime(time.time()))
        filename = request.FILES.get("editormd-image-file").__str__()
        msgs = {}
        check = T_article_images.objects.filter(filename=filename)
        if check.exists():  # 已经存在
            msgs["message"] = '文件已经存在'
            msgs["success"] = 1
            url = check[0].img.url
            msgs["url"] = url
            return HttpResponse(str(msgs).replace("'", '"'))
        T_article_images.objects.create(filename=filename, img=request.FILES.get("editormd-image-file"))
        msgs["message"] = '上传成功'
        msgs["success"] = 1
        url = T_article_images.objects.get(filename=filename).img.url
        msgs["url"] = url
        return HttpResponse(str(msgs).replace("'", '"'))
    else:
        mesg = {"message": '用户未登录，上传失败', "success": 0}
        return HttpResponse(str(mesg).replace("'", '"'))
