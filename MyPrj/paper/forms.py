from django import forms
from .models import *
class RegisterForm(forms.Form):
    user_id=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)
    role=forms.ChoiceField(widget=forms.RadioSelect,choices=(('1','teacher'),('2','admin'),('3','student')))
    admin=forms.CharField(widget=forms.PasswordInput)

class LoginForm(forms.Form):
    user_id=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

class uploadQb(forms.ModelForm):
    class Meta:
        model=Qbank
        fields=('qbank_id','qbank_file','ans_file',)

class selectQb(forms.Form):
    qb=forms.CharField()

class selectTesr(forms.Form):
    test=forms.CharField()

class generateTest(forms.Form):
    role=forms.CharField()

class TestGenerate(forms.Form):
    qb=forms.CharField()
    mark3=forms.CharField()
    mark4=forms.CharField()
    mark7=forms.CharField()
    test_id=forms.CharField()
    test_pass=forms.CharField()

class TryForm(forms.Form):
    trueans=forms.CharField(widget=forms.Textarea)
    ans=forms.CharField(widget=forms.Textarea)

class GiveTest(forms.Form):
    test_id=forms.CharField()
    user_pass=forms.CharField(widget=forms.PasswordInput)
    admin_pass=forms.CharField(widget=forms.PasswordInput)

class SelectQ(forms.Form):
    qno=forms.CharField()

class Ans(forms.Form):
    qno=forms.CharField()
    ans=forms.CharField(widget=forms.Textarea)

class jumpQues(forms.Form):
    qno=forms.CharField()
