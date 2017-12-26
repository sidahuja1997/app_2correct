
from django.http import HttpResponse,  HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import Question,  Choice
from django.urls import reverse
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import connection
from django.contrib.auth import hashers as hash
import re
#from django.template import loader
# temporary class to get work done!!!

class OBJ():
    def __init__(self):
        self.id=0
        self.title=''
        self.message=''

#def index(request):
 #   return HttpResponse("Hello world! you are at the polls index")
# Create your views here.
def index(request,user_name):
    user1=User.objects.get(username=user_name)
    login(request,user1)
    latest_question_list = Question.objects.order_by('-pub_date')#[:5]
   # template=loader.get_template('polls/index.html'
    context={'latest_question_list':latest_question_list}
    return render(request,'polls/index.html',context)


def detail(request, question_id):
    #return HttpResponse("You're looking at question %s." % question_id)

    question=get_object_or_404(Question,pk=question_id)

    return render(request, 'polls/detail.html', {'question': question})
def results(request, question_id):

    question=get_object_or_404(Question,pk=question_id)
    return render(request,'polls/results.html',{'question':question})

def vote(request, question_id):
    print('something happened!')
    question=get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError):
        return render(request,'polls/detail.html',{'question':question,
                                                   'error_message':'you didn\'t select a choice'})
    else:
        selected_choice.votes+=1
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def dlogin(request):
    return render(request,'polls/login.html')

def register(request,context={}):
    return render(request,'polls/register.html',context)


def user_login(request):

    c=connection.cursor()
    password=''
    username=''
    if request.method == 'POST':
          username = (request.POST['username'])
          password = (request.POST['password'])
          #print([username,password])
    username=check(username)
    password=check(password)

    password=ret_pass(password)

    print('new password is ',password)
    passs=c.execute('select password from auth_user where username= \'%s\''%(username))
    try:
        passs=passs.fetchone()[0]

        print(hash.check_password(password,passs))
        if(hash.check_password(password,passs)):
            password=passs
            print(password)

    except:
        pass
    print(password)
    print(username)
    a=c.execute('select * from auth_user where username = \'%s\' and password = \'%s\''%(username,password)).fetchall()
    print(len(a))
    if(len(a)>0):
        return HttpResponseRedirect('/login/polls/%s'%(username))
    else :
        return HttpResponseRedirect('/login/')

def ret_pass(a):
    a=a[:len(a)//2]
    b=''
    for i in a:

        if(i=='_'):
            b+=i
        elif(i in ['1','2','3','4','5','6','7','8','9','!','@','#']):
            b+=i;
        else:
            b+=chr(ord(i)-5)
    return(b)





def check(s):
    s = s.split(" ")
    l = ['select', 'drop', 'insert', 'or', '--', ';', 'xp_cmdshell']
    while ('\'' in s):
        s[s.index('\'')] += '\''

    for i in l:
        if (i in s):
            s.remove(i)
    sc = ""
    for i in s:
        sc += i
        sc += " "
    sc=sc.rstrip()
    return sc


def poster(request,context={}):
    return render(request,'polls/poster.html',context)

def poster_submit(request):
    title=request.POST['title']
    message=request.POST['message']
    if(xss_check(title)or xss_check(message)):
        return poster(request,context={'error_message':'XSS attack failed!!'})
    else:

        c=connection.cursor()
        #a=c.execute('select * from polls_question')
        qry='INSERT INTO poster (user_id,title,message) VALUES (%s,\'%s\',\'%s\')'%(request.user.id,title,message)
        c.execute(qry)
        post_list = c.execute('SELECT * FROM poster')


        objects = []
        for i in post_list:
            s = OBJ()
            s.id = i[0]
            s.title = i[1]
            s.message = i[2]
            objects += [s]
        objects.reverse()

        context={'objects':objects}
        return poster(request,context)
    #c.execute('INSERT INTO poster (user_id,title,message) VALUES (%s,\'%s\',\'%s\')'%(request.user.id,title,message))
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def xss_check(a):
    if(re.search(r'<[A-Za-z]*\d?>[a-zA-Z]*<\/[A-Za-z]*\d?',a)):
        return True
    else:
        return False



def passnum(a):
    flag=0
    for i in range(10):
        if(str(i) in a):
            flag=1
    if(flag==1):
        return True
    else:
        return False
def passcap(a):
    flag=0
    for i in a:
        if(ord(i) in range(65,91)):
            flag=1
    if(flag==1):
        return True
    else:
        return False


def user_register(request):

    a=(request.POST['username'])
    password=request.POST['password']
    if(len(a)>30):
        return render(request,'polls/register.html',context=
        {'error_message':'Username is greater than 30 characters. TRY AGAIN!!'})
    elif (not passnum(password)):
        return render(request, 'polls/register.html',
                      context={'error_message':
                                   'Password does not contain a number. TRY AGAIN!!'})
    elif(not passcap(password)):
        return render(request,'polls/register.html',
                      context={'error_message':'Password does not contain a capital letter.TRY AGAIN'})
    else:
        try:
            user=User.objects.get(username=request.POST['username'])
            print(user)
        except:

            User.objects.create_user(username=request.POST['username'],password=request.POST['password'],
            first_name=request.POST['first_name'],last_name=request.POST['last_name'])
            return HttpResponseRedirect('/login/')
        else:
            return render(request,'polls/register.html',
                          context={'error_message':'This username is already taken! Try some other'})


