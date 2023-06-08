from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Post, Comment
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    posts = reversed(list(Post.objects.all()))
    return render(request, 'index.html', {
      'posts': posts
    })

def register(request):
  if request.method == 'GET':
     return render(request, 'register.html')
  if request.POST['password'] == request.POST['password2']:
    try:
      user = User.objects.create_user(
        username=request.POST['username'],
        password=request.POST['password']
      )
      user.save()
      login(request, user)
      return redirect('home')
    except IntegrityError:
      return render(request, 'register.html', {
        'error': 'User already exists'
      })
  else:
    return render(request, 'register.html', {
      'error': 'Passwords do not match'
    })
  
def signin(request):
  if request.method == 'GET':
    return render(request, 'login.html')
  
  user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
  
  if user is None:
    return render(request, 'register.html', {
      'error': 'Please check your username and password'
    })
  else:
    login(request, user)
    return redirect('/dashboard')

def post_details(request, id):
  post = get_object_or_404(Post, id=id)
  comments = Comment.objects.filter(post_id=id)

  count = len(comments)

  if comments:
    print('Comments found')
    return render(request, 'post_details.html', {
    'post': post,
    'comments': comments,
    'count': count
    })
  else:
    return render(request, 'post_details.html', {
      'post': post,
      'count': 0
    })

@login_required
def create_comment(request, id):
  if request.method == 'POST':
    post = Post.objects.get(id=id)
    comment = Comment.objects.create(description=request.POST['description'], user=request.user, post=post)
    comment.save()
    return redirect('/posts/%s' % id)
  else:
    return redirect('/posts/%s' % id)
  
@login_required
def signout(request):
  logout(request)
  return redirect('/login')

@login_required
def dashboard(request):
  posts = Post.objects.filter(user=request.user)
  posts = reversed(list(Post.objects.filter(user=request.user))[:5])
  return render(request, 'dashboard.html', {
    'posts': posts
  })

@login_required
def create_post(request):
  if request.method == 'GET':
    return render(request, 'create_form.html', {
      'title': 'Create a new post'
    })
  else:
    post = Post.objects.create(title=request.POST['title'], content=request.POST['content'], image=request.POST['image'], user=request.user)
    post.save()

    return redirect('/posts/%s' % post.id)
  
@login_required
def update_post(request, id):
  if request.method == 'GET':
    post = Post.objects.get(id=id, user=request.user)
    return render(request, 'create_form.html', {
      'post': post,
      'title': 'Update post'
    })
  else:
    post = Post.objects.get(id=id, user=request.user)
    post.title = request.POST['title']
    post.content = request.POST['content']
    post.image = request.POST['image']
    post.save()

    return redirect('/posts/%s' % post.id)
  
@login_required
def delete_post(request, id):
  if request.method == 'POST':
    post = Post.objects.get(id=id, user=request.user)
    post.delete()
    return redirect('/dashboard')
  else:
    return redirect('/dashboard')
