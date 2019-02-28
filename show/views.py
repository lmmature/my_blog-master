from django.shortcuts import render, HttpResponse, redirect
from backstage import models as bacstage_models
from .models import T_reader_emails
from django.core.mail import send_mail
import time


# Create your views here.


def ValidateEmail(email):  # 邮箱验证
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def index(request, ):
    if request.method == 'POST':  # 读者邮箱保存
        email = request.POST['reader-email']
        print(ValidateEmail(email))
        if ValidateEmail(email):
            if T_reader_emails.objects.filter(email=email).exists():
                return HttpResponse("您已提交过该邮箱")
            T_reader_emails.objects.create(email=email,
                                           email_post_time=time.strftime('%Y-%m-%d', time.localtime(time.time())))
        else:
            return HttpResponse("邮箱格式有误")
        return HttpResponse("感谢您的支持")
    # 展示数据获取
    passages = bacstage_models.T_title.objects.all().order_by('-time')[0:10]
    result1 = []
    result2 = []
    result3 = []
    for indx, var in enumerate(passages):
        itm = {}
        if var.show == '1':
            itm["id"] = var.id
            itm["title"] = var.title
            itm["description"] = var.description
            itm["time"] = var.time
            itm["url"] = var.img.url
            if indx <= 2:
                result1.append(itm)
                continue
            if indx <= 5:
                result2.append(itm)
                continue
            if indx <= 8:
                result3.append(itm)
    latest = bacstage_models.T_title.objects.filter(show='1').order_by('-time')[0:3]  # 最新文章
    label = bacstage_models.T_type.objects.all()  # 获取标签
    return render(request, 'show/index.html', locals())


def single(request, paper):
    passage = bacstage_models.T_title.objects.get(id=paper)
    title = passage.title
    content = bacstage_models.T_content.objects.get(id=paper).content
    latest = bacstage_models.T_title.objects.all().order_by('time')[0:3]  # 最新文章
    label = bacstage_models.T_type.objects.all()  # 获取标签
    return render(request, 'show/single.html', locals())


def blog(request, get_type=None):
    if get_type:
        get_type_id = bacstage_models.T_type.objects.get(type=get_type).type_id
        passages = bacstage_models.T_title.objects.filter(type_id=get_type_id).order_by('-time')[0:9]
        result1 = []
        result2 = []
        result3 = []
        for indx, var in enumerate(passages):
            itm = {}
            itm["id"] = var.id
            itm["title"] = var.title
            itm["description"] = var.description
            itm["time"] = var.time
            itm["url"] = var.img.url
            if indx <= 2:
                result1.append(itm)
                continue
            if indx <= 5:
                result2.append(itm)
                continue
            if indx <= 8:
                result3.append(itm)
        return render(request, 'show/blog.html', locals())
    return redirect('show_index')


def contact(request, ):
    send = False
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        # 第三方 SMTP 服务
        try:
            print("okokoko")
            send_mail(subject, message, email, ['1043213248@qq.com'], fail_silently=False)
            print("success")
            send = True
        except:
            failed = False
        return render(request, 'show/contact.html', locals())
    return render(request, 'show/contact.html', locals())


def about(request, ):
    return HttpResponse("about")
