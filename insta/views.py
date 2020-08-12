from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse
from .forms import PostForm
from .models import Post
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
)
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.
class PostListView(ListView):
    template_name = "insta/post_list.html"
    queryset = Post.objects.all().filter(created_date__lte=timezone.now()).order_by('-created_date')
    context_object_name = 'posts'

class PostCreateView(CreateView):
    template_name = 'insta/post_create.html'
    form_class = PostForm
    queryset = Post.objects.all()
    success_url = '/'

    def form_valid(self, form):
        print(form.cleaned_data)
        form.instance.author = self.request.user
        return super().form_valid(form)


def register(request):
    if request.method == 'POST':
        print("This shit is working bro.")
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            print(username,"This shit is working")
            messages.success(request, f'Account created for {username} successfully!')
            return redirect('/')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'users/profile.html')

class Profile(DetailView):
    template_name = 'users/profile.html'
    queryset = User.objects.all()
    success_url = '/'

    def get_object(self):
        id_ = self.kwargs.get("username")
        user = get_object_or_404(User, username=id_)
        return user 
        
    def get_context_data(self, *args, **kwargs):
        context = super(Profile,self).get_context_data(*args, **kwargs)
        user = self.get_object()
        context.update({
            'posts' : user.posts.all().filter(created_date__lte=timezone.now()).order_by('-created_date')
        })
        return context 
    def add_follow(self, request):
        user = self.get_object() 
        user.profile.followed_by.add(request.user.profile) 
