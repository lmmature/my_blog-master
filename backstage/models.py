from django.db import models


# Create your models here.


class T_title(models.Model):
    # id = models.AutoField(verbose_name='唯一标识', primary_key=True, )
    title = models.TextField(verbose_name='标题')
    type_id = models.IntegerField(verbose_name='类型编码', null=False)
    time = models.CharField(max_length=20, verbose_name='录入时间')
    description = models.TextField(verbose_name="内容简述", null=True)
    img = models.FileField(upload_to='article/image/', default='article/image/default.jpg')
    show = models.CharField(max_length=1, verbose_name="是否展示", default=1, null=True)


class T_content(models.Model):
    t_id = models.IntegerField(verbose_name="标题id")
    content = models.TextField(verbose_name="html文本内容", max_length=50000)
    markdown_text = models.TextField(verbose_name="md文本", max_length=50000, null=True)


class T_type(models.Model):
    id = models.AutoField(verbose_name="文章类型", primary_key=True)
    type = models.CharField(max_length=20, verbose_name="类型名称")
    type_id = models.IntegerField(verbose_name='类型id')


class T_day_visit_flow(models.Model):
    visit_time = models.TimeField(verbose_name='访问时间')
    visit_num = models.IntegerField(verbose_name='访问数量')


class T_everyday_visit(models.Model):
    date = models.DateTimeField(verbose_name='访问日期')
    visit_num = models.IntegerField(verbose_name='访问量')


class T_article_images(models.Model):
    belong = models.IntegerField(verbose_name='关联文章的id', null=True)
    filename = models.CharField(max_length=20, verbose_name="图片名称", null=True)
    img = models.FileField(upload_to='article/image/')
    upload_time = models.TimeField(verbose_name='上传时间', auto_now=True)
