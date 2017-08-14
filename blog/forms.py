from django import forms

from .models import Topic,Entry
from DjangoUeditor.models import UEditorField

class TopicForm(forms.ModelForm):
    class Meta:
        model=Topic
        fields=['text']
        labels={'text':''}  #作用，不要为字段text生成标签


class EntryForm(forms.ModelForm):
    class Meta:
        model=Entry
        fields=['topic','title','text']
        labels={'text':''}
        # widgets={'text':forms.Textarea(attrs={'cols':80})}