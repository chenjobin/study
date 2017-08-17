#coding:utf-8
from django import forms
from django.contrib.auth.forms import UserCreationForm

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

