from django.db import models
from django.contrib.postgres.fields import ArrayField

class User(models.Model):
    user_id=models.CharField(unique=True,max_length=50)
    password=models.CharField(max_length=50)
    role=models.IntegerField(blank=False)
    def __str__(self):
        return self.user_id


class Qbank(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    qbank_id=models.CharField(unique=True,max_length=50,blank=False)
    # subject_id=models.CharField(max_length=50)
    qbank_file=models.FileField(upload_to= 'qbs/',blank=False)
    ans_file=models.FileField(upload_to= 'ans/',blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.qbank_id



class Test(models.Model):
    qbank=models.ForeignKey(Qbank,on_delete=models.CASCADE)
    test_id=models.CharField(unique=True,max_length=50)
    request=models.IntegerField(default=0)
    checked=models.IntegerField(default=0)
    marks=models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    test_pass=models.CharField(max_length=50,default="imbatman")
    # test_file=models.FileField(upload_to= 'tests/',blank=False)
    # true if send and checked respt
    def __str__(self):
        return self.test_id

class Temp(models.Model):
    sessionid=models.CharField(max_length=150,default="Empty")
    qno=models.IntegerField(default=0)
    marks=models.IntegerField(default=0)
    ques=models.CharField(max_length=150,default="Empty")
    ans=models.CharField(max_length=1500,default="Empty")

class Score(models.Model):
    user=models.CharField(max_length=50)
    test=models.CharField(max_length=50)
    score=models.PositiveIntegerField()

class TestLog(models.Model):
    test_id=models.CharField(max_length=50)
    file_name=models.CharField(max_length=101)
    user_id=models.CharField(max_length=50)
    score=models.CharField(max_length=50,default="not checked")
