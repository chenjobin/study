#coding:utf-8
from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate #验证密码是否正确

#注册表单
class RegisterForm(forms.Form,UserCreationForm):
    email = forms.EmailField()
    # mobile = forms.CharField(label='手机号', max_length=11)
    # qq = forms.CharField(label='QQ号', max_length=16)
    # type = forms.ChoiceField(label='注册类型', choices=(('buyer','买家'),('saler','商家')))
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError('所有项都为必填项')
        else:
            cleaned_data = super().clean()
        return cleaned_data


class ChangeNickForm(forms.Form):
    """change the nick name form"""
    #旧昵称，hidden类型，用于判断是否有修改
    old_nickname = forms.CharField(widget=forms.HiddenInput(attrs={'id':'old_nickname'}))
    #新昵称
    nickname = forms.CharField(label=u'新的昵称', max_length=20,
        widget=forms.TextInput(attrs={'class':'form-control', 'id':'nickname', 'placeholder':u"请输入您的昵称"}),
        error_messages={'required':u'昵称不能为空'})

    #nickname验证方法
    def clean_nickname(self):
        old_nickname = self.cleaned_data.get('old_nickname')
        nickname = self.cleaned_data.get('nickname')
        #此处可以被参考，用在邮箱验证，确保一个邮箱只能注册一个账号
        is_exist = User.objects.filter(first_name=nickname).count()>0

        if is_exist:
            #用事先写入hidden的昵称判断是否是自己的昵称
            if old_nickname == nickname:
                raise ValidationError(u'您当前的昵称就是“%s”，写一个新的吧' % nickname)
            else:
                raise ValidationError(u'“%s”已被使用，请重新输入' % nickname)
        else:
            return nickname

class ChangePwdForm(forms.Form):
    """change the password form"""
    username = forms.CharField(widget=forms.HiddenInput())
    pwd_old = forms.CharField(label=u'旧的密码', max_length=36,
        widget=forms.PasswordInput(
            attrs={'class':'form-control', 'id':'pwd_old','placeholder':u'请输入旧密码，验真身'}))
    pwd_1 = forms.CharField(label=u'新的密码', max_length=36,
        widget=forms.PasswordInput(
            attrs={'class':'form-control', 'id':'pwd_1','placeholder':u'请输入至少8位的密码'}))
    pwd_2 = forms.CharField(label=u'再输一遍', max_length=36,
        widget=forms.PasswordInput(
            attrs={'class':'form-control', 'id':'pwd_2','placeholder':u'重复新的密码确保正确'}))

    #验证两个新密码是否一致
    def clean_pwd_2(self):
        pwd_1 = self.cleaned_data.get('pwd_1')
        pwd_2 = self.cleaned_data.get('pwd_2')

        if pwd_1 != pwd_2:
            raise ValidationError(u'两次输入的密码不一致，再输入一次吧')
        if len(pwd_2) < 6 or len(pwd_2) > 36:
            raise ValidationError(u'密码长度需要在6-36之间')
        return pwd_2

    #验证旧密码是否正确
    def clean_pwd_old(self):
        username = self.cleaned_data.get('username')
        pwd_old = self.cleaned_data.get('pwd_old')
        user = authenticate(username=username, password=pwd_old)

        if user is None:
            raise ValidationError(u'旧密码不正确，验真身失败')
        return pwd_old
