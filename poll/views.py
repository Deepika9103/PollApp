from django.shortcuts import render,redirect
from .models import Poll
from django.http import HttpResponse
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages 
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login')
def create(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        newPoll = Poll(question=question,option1=option1,option2=option2,option3=option3)
        newPoll.save()
    return render (request,'poll/create.html')

@login_required(login_url='login')
def allPoll(request):
    polls = Poll.objects.all()
    return render (request, 'poll/poll.html',{'polls':polls})

@login_required(login_url='login')
def vote(request,id):
    poll = Poll.objects.get(pk=id)

    if request.method == 'POST':

        selected_option = request.POST.get('poll')
        if selected_option == 'option1':
            poll.option1_count += 1
        elif selected_option == 'option2':
            poll.option2_count += 1
        elif selected_option == 'option3':
            poll.option3_count += 1
        else:
            return HttpResponse(400, 'Invalid form')

        poll.save()

        return redirect('results', poll.id)
        #return HttpResponse('valid form')

    return render(request, 'poll/vote.html', {'poll' : poll})

@login_required(login_url='login')
def results(request,id):
    poll = Poll.objects.get(pk=id)
    option1per = (poll.option1_count / (poll.option1_count+poll.option2_count+poll.option3_count))*100
    option2per = (poll.option2_count/ (poll.option1_count+poll.option2_count+poll.option3_count))*100
    option3per = (poll.option3_count/ (poll.option1_count+poll.option2_count+poll.option3_count))*100
    content ={
        'poll' : poll,
        'option1per' : option1per,
        'option2per' : option2per,
        'option3per' : option3per
    }
    return render(request, 'poll/results.html', content )


def loginuser(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username+password)
        user = authenticate(request,username=username,password=password)
        print(user)
        print("hello4")
        if user is not None:
            print("hello1")
            login(request,user)
            print('hello2')
            return redirect('create/')
        else:
            messages.info(request, 'Email or password is incorrect')
    return render(request,'poll/login.html')

#logout the user
def logoutUser(request):
    logout(request)
    return redirect('login')



def register(request):
    form = CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            #to get a field from the form 
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created '+user)

            return redirect('login/')
    context = {'form':form}
    return render(request,'poll/register.html',context)