from django.db import models


# Create your models here.


class T_reader_emails(models.Model):
    email = models.EmailField(verbose_name='用户邮箱')
    username = models.CharField(verbose_name='用户姓名', default='匿名', max_length=20)
    email_post_time = models.TextField(verbose_name='邮箱记录创建时间', null=True, max_length=20)
