
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .form import PostForm, LogInForm, SignUpForm, ProfileEditForm, CommentForm 
from .models import Post, User,Comment
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, authenticate, logout 




def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(parent__isnull=True, post=post).all()
    new_comment = None
    if request.method == 'POST':
        parent_id = request.POST.get('parent_id', None)
        if parent_id:
            c_obj = Comment.objects.filter(id=parent_id).last()
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.parent = c_obj
                new_comment.save()
        else:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.save()
       
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})       

def category(request, slug):
    post = get_object_or_404(Post, slug=slug)
    posts = Post.objects.filter(category = post.category)

    return render(request, 'blog/category.html', {'posts': posts})

def tag(request,slug):  
    post = get_object_or_404(Post, slug=slug)
    posts = Post.objects.filter(id=12)
    return render(request, 'blog/tag.html', {'posts': posts})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            # post.tag = form.cleaned_data("tag")
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('log_in')
    else:
        form = SignUpForm()   
    return render(request, 'blog/signup.html', {'form': form})


def log_in(request):
    form = LogInForm()
    error = False
    if request.user.is_authenticated:
        return redirect("post_list")
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                 login(request, user)  
                return redirect('post_list')
            else:
                form = LogInForm()

    return render(request, 'blog/login.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('post_list')

def profile(request, username):

    user = get_user_model().objects.filter(username=username).first()
    if user:
        form = UpdateProfile(instance=user)
        
    if form.is_valid():
            user_form = form.save()

            messages.success(request, f'{user_form}, Your profile has been updated!')
            return redirect('blog/profile.html', user_form.username)

    else:
       for error in list(form.errors.values()):
               messages.error(request, error)
   
                                                     
               return render(request, 'profile.html', context)


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'blog/profile.html', {'user': user})

def profile_edit(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == "POST":
        user_form = ProfileEditForm(request.POST, instance=user)
        if user_form.is_valid():
            
            user_form.save()
            return redirect(profile_view, user.username)
    else:
        user_form = ProfileEditForm(instance=user)
    return render(request, 'blog/profile_edit.html', {'form': user_form})

