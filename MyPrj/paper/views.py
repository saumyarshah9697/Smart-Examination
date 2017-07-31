import random
from django.shortcuts import render
from . import forms
from . import models
import os
from django.http import HttpResponse
from django.utils.encoding import *
import os.path
import xlrd,xlwt
import numpy as np
from .ansChq import Marks1,Marks2

adminkey='imbatman'



# Demo Ans checking script Redirection
def trypage(request):
    return render(request,'paper/try.html',{'message':"",'correct':"Correct Answer",'attempt':"Attempted Ans"})

# Demo Ans checking script
def anschecking(request):
    message='error'
    form=forms.TryForm(request.POST)
    if form.is_valid():
        trueans=form.cleaned_data['trueans']
        ans=form.cleaned_data['ans']
        m1=int(Marks1(trueans,ans)*100)/100.00
        m2=int(Marks2(trueans,ans)*100)/100.00
        message="marks by Normal Plagarism = "+str(m1)+"  and Marks by Advanced Method = "+str(m2)
    return render(request,'paper/try.html',{'message':message,'correct':trueans,'attempt':ans})


# HOMEPAGE RIDIRECTING IF ALREADY LOGGED IN
def index(request):
    message=''
    if(models.User.objects.filter(user_id=request.session['user'])):
        user=models.User.objects.get(user_id=request.session['user'])

        #teacher
        if user.role==1:
            qbs=user.qbank_set.all()
            tests=[]
            for x in qbs:
                tests+=x.test_set.all()
            uploadform=forms.uploadQb()
            return render(request,'paper/teacher.html',{'user':user,'tests':tests,'qbs':qbs,'message1':'','message2':'','message3':'','message4':'','uploadform':uploadform})

        #admin
        elif user.role==2:
            return render(request,'paper/admin.html',{'user':user,'message':''})

            #student
        elif user.role==3:
            return render(request,'paper/student.html',{'user':user,'message':''})
    else:
        return render(request,'paper/index.html',{'registermessage':message,'loginmessage':message})


# REMOVAL OF SESSION
def logout(request):
    request.session['user']=''
    return render(request,'paper/index.html',{'registermessage':"",'loginmessage':""})


# USER REGISTRATION
def register(request):
    Logform=forms.LoginForm()
    Regform=forms.RegisterForm(request.POST)
    message=''
    if Regform.is_valid():
        user=Regform.cleaned_data['user_id']
        role=Regform.cleaned_data['role']
        password=Regform.cleaned_data['password']
        admin=Regform.cleaned_data['admin']
        newUser=models.User.objects.filter(user_id=user)

        if(admin==adminkey):
            if(newUser):
                message='user id already exists'
            else:
                newUser=models.User(user_id=user,role=role,password=password)
                newUser.save()
                # os.mkdir('paper/'+user)
                message=user+' Registered :)'
        else:
            message='contact admin for guidence'
    return render(request,'paper/index.html',{'loginmessage':'','registermessage':message})

# USER LOGIN
def login(request):
    Regform=forms.RegisterForm()
    Logform=forms.LoginForm(request.POST)
    message=''
    if Logform.is_valid():
        user=Logform.cleaned_data['user_id']
        password=Logform.cleaned_data['password']
        if models.User.objects.filter(user_id=user):
            newUser1=models.User.objects.get(user_id=user)
            if newUser1.password == password:
                request.session['user']=newUser1.user_id
                user=models.User.objects.get(user_id=request.session['user'])

                #teacher
                if newUser1.role==1:
                    qbs=user.qbank_set.all()
                    tests=[]
                    for x in qbs:
                        tests+=x.test_set.all()
                    uploadform=forms.uploadQb()
                    return render(request,'paper/teacher.html',{'user':user,'tests':tests,'qbs':qbs,'message1':'','message2':'','message3':'','message4':'','uploadform':uploadform})

                #admin
                elif newUser1.role==2:
                    return render(request,'paper/admin.html',{'user':user,'message':''})

                #student
                elif newUser1.role==3:
                    return render(request,'paper/student.html',{'user':user,'message':''})

        message='invalid user or password'
        return render(request,'paper/index.html',{'loginmessage':message,'registermessage':''})
    else:
        message=''
        return render(request,'paper/index.html',{'registermessage':message,'loginmessage':message})

# ADMIN TO REMOVE ANY USER HE WISHES
def removeUser(request):
    form=forms.LoginForm(request.POST)
    if form.is_valid():
        user_id=form.cleaned_data['user_id']
        password=form.cleaned_data['password']
        User=models.User.objects.get(user_id=request.session['user'])
        if (User.password==password and user_id!=User.user_id):
            models.User.objects.filter(user_id=user_id).delete()
            # os.rmdir('paper/'+User.user_id)
            return render(request,'paper/admin.html',{'user':models.User.objects.get(user_id=request.session['user']),'message':user_id+' deleted'})
        else:
            return render(request,'paper/admin.html',{'user':models.User.objects.get(user_id=request.session['user']),'message':'invalid details'})

# ADMIN TO START ANSWER CHECKING SCRIPT
def testEval(request):
    pass


# for student giving test
class Test():
    test_id=""
    qno=[]
    questions=[]
    ans=[]
    marks=[]

# STUDENT GIVE TEST
def giveTest(request,template='paper/test.html'):
    User=models.User.objects.get(user_id=request.session['user'])
    form=forms.GiveTest(request.POST)
    message='error'
    if form.is_valid():
        test_id=form.cleaned_data['test_id']
        user_pass=form.cleaned_data['user_pass']
        admin_pass=form.cleaned_data['admin_pass']
        if User.password==user_pass and models.Test.objects.filter(test_id=test_id):
            test=models.Test.objects.get(test_id=test_id)
            if test.test_pass==admin_pass:
                if test.checked==0:
                    t=Test()
                    t.test_id=test_id
                    # extract data from test file
                    workbook=xlrd.open_workbook(test_id+'.xls')
                    worksheet=workbook.sheet_by_index(0)
                    rows=worksheet.nrows
                    models.Temp.objects.filter(sessionid=User.user_id).delete()
                    for no in range(1,rows):
                        obj=models.Temp(sessionid=User.user_id,qno=no,marks=worksheet.cell(no,2).value,ques=worksheet.cell(no,1).value,ans=" ")
                        t.qno.append(no)
                        t.questions.append(worksheet.cell(no,1).value)
                        t.marks.append(worksheet.cell(no,2).value)
                        t.ans.append(" ")
                        obj.save()


                    response=render(request,template,{'user':User,'test':t,'qno':1,'qnow':t.questions[0],'anow':t.ans[0],'marks':t.marks[0]})
                    response.set_cookie(key='test_id',value=test_id)
                    return response
                else:
                    message='test cannot be given'
            else:
                message='invalid password for test'
    return render(request,'paper/student.html',{'user':User,'message':message})



def saveAns(request):
    User=models.User.objects.get(user_id=request.session['user'])
    test_id=request.COOKIES.get("test_id")  #str(request.COOKIES.get('test_id'))
    paper=models.Temp.objects.filter(sessionid=User.user_id)
    t=Test()
    t.test_id=test_id
    form=forms.Ans(request.POST)
    qno=1
    if form.is_valid():
        # for no in range(1,rows):
        #     t.questions.append(worksheet.cell(no,0).value)
        t.questions=[]
        t.ans=[]
        t.marks=[]
        no=1
        for ques in paper:
            t.questions.append(ques.ques)
            t.ans.append(ques.ans)
            t.marks.append(ques.marks)
            no+=1

        qno=int(t.questions.index(form.cleaned_data['qno']))
        ans=form.cleaned_data['ans']
        a=models.Temp.objects.get(sessionid=User.user_id,qno=qno+1)
        a.ans=ans
        a.save()

    t.questions=[]
    t.ans=[]
    t.marks=[]
    no=1
    for ques in paper:
        t.questions.append(ques.ques)
        t.ans.append(ques.ans)
        t.marks.append(ques.marks)
        no+=1

    myvar=(models.Temp.objects.all())
    for x in myvar:
        print(x.qno,x.ans)
    responce=render(request,'paper/test.html',{'user':User,'test':t,'qnow':t.questions[qno],'anow':t.ans[qno],'marks':t.marks[qno]})
    responce.set_cookie(key='test_id',value=test_id)
    return responce

def goToQuestion(request):
    User=models.User.objects.get(user_id=request.session['user'])
    paper=models.Temp.objects.filter(sessionid=User.user_id)

    test_id=request.COOKIES.get("test_id")          #str(request.COOKIES.get('test_id'))

    t=Test()
    t.test_id=test_id
    t.questions=[]
    t.marks=[]
    t.ans=[]
    no=0
    for ques in paper:
        t.questions.append(ques.ques)
        t.marks.append(ques.marks)
        t.ans.append(ques.ans)
        no+=1

    qno=0
    form=forms.jumpQues(request.POST)
    if form.is_valid():
        qno=int(t.questions.index(form.cleaned_data['qno']))
        #qno=form.cleaned_data['qno']

    print(models.Temp.objects.all())
    responce=render(request,'paper/test.html',{'user':User,'test':t,'qnow':t.questions[qno],'anow':t.ans[qno],'marks':t.marks[qno]})
    responce.set_cookie(key='test_id',value=test_id)
    return responce



def submitPaper(request):
    User=models.User.objects.get(user_id=request.session['user'])
    test_id=str(request.COOKIES.get('test_id'))
    test_file=xlwt.Workbook()
    sheet=test_file.add_sheet('sheet_1',cell_overwrite_ok=True)
    sheet.write(0,0,"qno")
    sheet.write(0,1,"ans")
    sheet.write(0,2,"Max marks")
    # sheet.write(0,3,"Scored")
    paper=models.Temp.objects.filter(sessionid=User.user_id)
    no=1
    for questions in paper:
        sheet.write(no,0,questions.ques)
        sheet.write(no,1,questions.ans)
        sheet.write(no,2,questions.marks)
        no+=1
    file_name=test_id+'-'+User.user_id+'.xls'
    test_file.save(file_name)
    tlnew=models.TestLog(test_id=test_id,file_name=file_name,user_id=User.user_id)
    tlnew.save()

    models.Temp.objects.filter(sessionid=User.user_id).delete()
    response=render(request,'paper/student.html',{'user':User,'message':'Test completed'})
    response.set_cookie(key='test_id',value=" ")
    return response


# STUDENT CHECK MARKS (REUSE FOR TEACHER)
def checkMarks(request):
    pass

# TEACHER DELETE EXISTING QBANK
def delQbank(request):
    User=models.User.objects.get(user_id=request.session['user'])
    form=forms.selectQb(request.POST)
    message4='error'
    if form.is_valid():
        qb=form.cleaned_data['qb']
        if User.qbank_set.filter(qbank_id=qb):
            User.qbank_set.get(qbank_id=qb).delete()
            message4='deleted'
    qbs=User.qbank_set.all()
    tests=[]
    for x in qbs:
        tests+=x.test_set.all()
    uploadform=forms.uploadQb()
    return render(request,'paper/teacher.html',{'user':User,'tests':tests,'qbs':qbs,'message1':'','message2':'','message3':'','message4':message4,'uploadform':uploadform})

# TEACHER UPLOAD QBANK
def uploadQbank(request):
    User=models.User.objects.get(user_id=request.session['user'])
    form=forms.uploadQb(request.POST,request.FILES)
    message3='error'

    if form.is_valid():
        # form.save()
        # fs=request.FILES
        User.qbank_set.create(qbank_id=form.cleaned_data['qbank_id'],qbank_file=request.FILES['qbank_file'],ans_file=request.FILES['ans_file'])
        User.save()
        message3='uploaded'

    qbs=User.qbank_set.all()
    tests=[]
    for x in qbs:
        tests += x.test_set.all()
    return render(request,'paper/teacher.html',{'user':User,'tests':tests,'qbs':qbs,'message1':'','message2':'','message3':message3,'message4':'','uploadform':form})

# TEACHER DOWNLOAD UPLOADED QBANK
def dnloadQbank(request):
    User=models.User.objects.get(user_id=request.session['user'])
    form=forms.selectQb(request.POST)
    message4='error'
    if form.is_valid():
        qb=form.cleaned_data['qb']
        if User.qbank_set.filter(qbank_id=qb):
            qb_select=User.qbank_set.get(qbank_id=qb)
            qb_filename=qb_select.qbank_file
            path_to_file='media/qbs'
            response = HttpResponse(content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(qb_filename)
            response['X-Sendfile'] = smart_str(path_to_file)
            return response
            message4=''
    qbs=User.qbank_set.all()
    tests=[]
    for x in qbs:
        tests+=x.test_set.all()
    uploadform=forms.uploadQb()
    return render(request,'paper/teacher.html',{'user':User,'tests':tests,'qbs':qbs,'message1':'','message2':'','message3':'','message4':message4,'uploadform':uploadform})

# TEACHER DOWNLOAD ANS QBANK
def dnloadAns(request):
    User=models.User.objects.get(user_id=request.session['user'])
    form=forms.selectQb(request.POST)
    message4='error'
    if form.is_valid():
        qb=form.cleaned_data['qb']
        if User.qbank_set.filter(qbank_id=qb):
            qb_select=User.qbank_set.get(qbank_id=qb)
            qb_filename=qb_select.ans_file
            path_to_file='media/ans'
            response = HttpResponse(content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(qb_filename)
            response['X-Sendfile'] = smart_str(path_to_file)
            return response
            message4=''
    qbs=User.qbank_set.all()
    tests=[]
    for x in qbs:
        tests+=x.test_set.all()
    uploadform=forms.uploadQb()
    return render(request,'paper/teacher.html',{'user':User,'tests':tests,'qbs':qbs,'message1':'','message2':'','message3':'','message4':message4,'uploadform':uploadform})

# TEACHER CREATE TEST
def createTest(request):
    User=models.User.objects.get(user_id=request.session['user'])
    form=forms.TestGenerate(request.POST)
    message1='error'
    if form.is_valid():
        qb=form.cleaned_data['qb']
        if User.qbank_set.filter(qbank_id=qb):
            mark3=int(form.cleaned_data['mark3'])
            mark4=int(form.cleaned_data['mark4'])
            mark7=int(form.cleaned_data['mark7'])
            test_id=form.cleaned_data['test_id']
            test_pass=form.cleaned_data['test_pass']
            # if True:
            if not models.Test.objects.filter(test_id=test_id):
                qb_select=User.qbank_set.get(qbank_id=qb)
                workbook=xlrd.open_workbook('C:\\Users\\Rushabh\\Desktop\\project\\MyPrj\\'+qb_select.qbank_file.url)
                worksheet=workbook.sheet_by_index(0)
                # message1=worksheet.cell(0,0).value
                # message1='its working'
                mark3qnos=[]
                mark4qnos=[]
                mark7qnos=[]
                rows=worksheet.nrows
                for no in range(1,rows):
                    cell=worksheet.cell(no,2).value
                    if '3'==str(int(cell)):
                        mark3qnos.append(str(no))
                        print(3,no)
                    elif '4'==(str(int(cell))):
                        mark4qnos.append(str(no))
                        print(4,no)
                    elif '7'==(str(int(cell))):
                        mark7qnos.append(str(no))
                        print(7,no)
                    else:
                        break
                    no+=1

                if(mark3<=len(mark3qnos) or mark4<=len(mark4qnos) or mark7<=len(mark7qnos)):
                    while mark3!=len(mark3qnos):
                        del(mark3qnos[random.randint(0,len(mark3qnos)-1)])
                    while mark4!=len(mark4qnos):
                        del(mark4qnos[random.randint(0,len(mark4qnos)-1)])
                    while mark7!=len(mark7qnos):
                        del(mark7qnos[random.randint(0,len(mark7qnos)-1)])

                    print('\n3 '+str(len(mark3qnos)))
                    print('4 '+str(len(mark4qnos)))
                    print('7 '+str(len(mark7qnos)))
                    test_file=xlwt.Workbook()
                    # test_file.save('C:\\Users\\Rushabh\\Desktop\\project\\MyPrj\\tests\\'+test_id+'.xls')
                    sheet=test_file.add_sheet('sheet_1',cell_overwrite_ok=True)
                    sheet.write(0,0,"qno")
                    sheet.write(0,1,"question")
                    sheet.write(0,2,"marks")

                    for x in range(0,mark3):
                        sheet.write(x+1,0,(mark3qnos[x]))
                        sheet.write(x+1,1,(worksheet.cell(int(mark3qnos[x]),1).value))
                        sheet.write(x+1,2,3)

                    for x in range(0,mark4):
                        sheet.write(mark3+x+1,0,str(mark4qnos[x]))
                        sheet.write(mark3+x+1,1,(worksheet.cell(int(mark4qnos[x]),1).value))
                        sheet.write(mark3+x+1,2,4)

                    for x in range(0,mark7):
                        sheet.write(mark3+mark4+1+x,0,str(mark7qnos[x]))
                        sheet.write(mark3+mark4+x+1,1,(worksheet.cell(int(mark7qnos[x]),1).value))
                        sheet.write(mark3+mark4+1+x,2,7)

                    test_file.save(test_id+'.xls')
                    message1="test created"
                    qb_select.test_set.create(test_pass=test_pass,test_id=test_id,marks=((3*mark3)+(4*mark4)+(7*mark7)))

                else:
                    message1="invalid no of questions "+str(mark3qnos[0])
            else:
                message1=test_id+" already exist use different test id"

    qbs=User.qbank_set.all()
    tests=[]
    for x in qbs:
        tests+=x.test_set.all()
    uploadform=forms.uploadQb()
    return render(request,'paper/teacher.html',{'user':User,'tests':tests,'qbs':qbs,'message1':message1,'message2':'','message3':'','message4':'','uploadform':uploadform})


# TEACHER REQUESTING CHECK FOR TEST
def reqCheck(request):
    User=models.User.objects.get(user_id=request.session['user'])
    form=forms.selectTesr(request.POST)
    message2='error'
    if form.is_valid():
        test_id=form.cleaned_data['test']
        if models.Test.objects.filter(test_id=test_id):
            test=models.Test.objects.get(test_id=test_id)
            test.request=1
            test.save()
            message2="Resquest sent for evaluation"
    qbs=User.qbank_set.all()
    tests=[]
    for x in qbs:
        tests+=x.test_set.all()
    uploadform=forms.uploadQb()
    return render(request,'paper/teacher.html',{'user':User,'tests':tests,'qbs':qbs,'message1':'','message2':message2,'message3':'','message4':'','uploadform':uploadform})



# TEACHER SCORE SHEET FOR TEST unfinished
def ScoreSheet(request):
    User=models.User.objects.get(user_id=request.session['user'])
    form=forms.selectTesr(request.POST)
    message2='error'
    if form.is_valid():
        test_id=form.cleaned_data['test']
        if models.Test.objects.filter(test_id=test_id):
            test=models.Test.objects.get(test_id=test_id)
            max_marks =test.marks
            objs=models.TestLog.objects.filter(test_id=test_id)

            test_file=xlwt.Workbook()
            sheet=test_file.add_sheet('sheet_1',cell_overwrite_ok=True)
            sheet.write(0,0,"Test id")
            sheet.write(0,1,test_id)
            sheet.write(1,2,"Max marks")
            sheet.write(1,3,max_marks)

            sheet.write(2,0,"Student id")
            sheet.write(2,1,"Marks achieved")

            line_no=3
            for x in objs:
                sheet.write(line_no,0,x.user_id)
                sheet.write(line_no,1,x.score)

            test_file.save(test_id+"score.xls")
            #path_to_file='media/ans'
            response = HttpResponse(content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(test_id+"score.xls")
            # response['X-Sendfile'] = smart_str(path_to_file)





            message2='working'
    qbs=User.qbank_set.all()
    tests=[]
    for x in qbs:
        tests+=x.test_set.all()
    uploadform=forms.uploadQb()
    return render(request,'paper/teacher.html',{'user':User,'tests':tests,'qbs':qbs,'message1':'','message2':message2,'message3':'','message4':'','uploadform':uploadform})
