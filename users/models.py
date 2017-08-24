from django.db import models
from django.contrib.auth.models import User



# 找回密码创建
class User_ex(models.Model):
    """User models ex"""
    user = models.ForeignKey(User)   #和User关联的外键
    valid_code = models.CharField(max_length = 24)   #验证码
    valid_time = models.DateTimeField(auto_now = True) #验证码有效时间
 
    def __str__(self):
        return u'%s' % (self.valid_code)
