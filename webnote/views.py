from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, PostForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post

@login_required
def index(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request,'index.html', {'posts': posts})

@login_required
def special(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request,'registration.html',
                          {'user_form':user_form,
                           'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'login.html', {})

@login_required
def post_new(request):
    if request.method == 'POST':    # если пользователь отправляет форму
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('index')  # redirect('name of view function')
    else:   # если только зашел на страницу и еще ничего не отправил
        form = PostForm()
    return render(request,'post_edit.html', {'form': form})

@login_required
def post_detail(request,pk):
    post = get_object_or_404(Post, pk=pk)  # получаем нужный нам пост из базы, используя его первичный ключ
                                           # если такого нет - 404
    return render(request,'post_detail.html',{'post':post})

@login_required
def post_remove(request,pk):
    post = get_object_or_404(Post,pk=pk)  # получаем, если пост с таким pk существует
    post.delete()  # удаляем объект из бд
    return redirect('index')

@login_required
def post_edit(request,pk):
    post = get_object_or_404(Post, pk=pk)
    title = post.title
    if request.method == 'POST':    # если пользователь отправляет форму
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('index')  # redirect('name of view function')
    else:   # если только зашел на страницу и еще ничего не отправил
        form = PostForm(instance=post)
    return render(request,'post_edit.html', {'form': form, 'title':title})