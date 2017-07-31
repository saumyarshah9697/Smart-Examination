from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^$',views.index,name='index'),

    url(r'^register/',views.register,name='register'),
    url(r'^login/',views.login,name='login'),

    url(r'^logout/',views.logout,name='logout'),

    url(r'^removeUser/',views.removeUser,name='removeUser'),
    url(r'^evalTest/',views.testEval,name='evalTest'),

    url(r'^reqCheck/',views.reqCheck,name='reqCheck'),
    url(r'^ScoreSheet',views.ScoreSheet,name='ScoreSheet'),
    url(r'^createTest/',views.createTest,name='createTest'),
    url(r'^delqb/',views.delQbank,name='delqb'),
    url(r'^uploadQb/',views.uploadQbank,name='uploadQb'),
    url(r'^downloadQb/',views.dnloadQbank,name='downloadQb'),
    url(r'^downloadAns/',views.dnloadAns,name='downloadAns'),

    url(r'^try/',views.trypage,name='try'),
    url(r'^anschecking/',views.anschecking,name='anschecking'),

    url(r'^giveTest/',views.giveTest,name='giveTest'),
    url(r'^checkMarks/',views.checkMarks,name='checkMarks'),

    url(r'^saveAns/',views.saveAns,name='saveAns'),
    url(r'^goToQuestion/',views.goToQuestion,name='goToQuestion'),
    url(r'^submitPaper/',views.submitPaper,name='submitPaper'),


    ]
