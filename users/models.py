from django.db import models
from django.contrib.auth.models import User

from types import MethodType #类动态绑定方法
import os

AVATAR_ROOT = 'avatar'
AVATAR_DEFAULT = os.path.join(AVATAR_ROOT, 'default.jpg')

# 找回密码创建
class User_ex(models.Model):
    """User models ex"""
    user = models.ForeignKey(User)   #和User关联的外键
    valid_code = models.CharField(max_length = 24)   #验证码
    valid_time = models.DateTimeField(auto_now = True) #验证码有效时间
 
    def __str__(self):
        return u'%s' % (self.valid_code)

class User_Avatar(models.Model):
    """user avatar"""
    user = models.ForeignKey(User)
    avatar = models.ImageField(upload_to='avatar/')

#动态绑定头像相关的方法
def get_avatar_url(self):
    try:
        avatar = User_Avatar.objects.get(user=self.id)
        return avatar.avatar
    except Exception as e:
        return AVATAR_DEFAULT

#动态绑定方法
User.get_avatar_url = MethodType(get_avatar_url, User)