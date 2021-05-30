from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login as auth_login, get_user_model, authenticate
from django.contrib.auth.views import LoginView, logout_then_login
from django.contrib.auth.decorators import login_required
from django.template import engines
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from .forms import CommentForm
from django.db.models import Count
from django.db.models import Q
from django.views import generic

User = get_user_model()

@login_required
def index(request):
    if request.method == 'GET':
        return HttpResponse("<pre> Hello 🥱 <pre>")

@login_required
def post_list(request, tag_slug=None):
    posts = Post.published.all() 
    # search
    query = request.GET.get("q")
    if query:
        posts=Post.published.filter(Q(title__icontains=query)).distinct()
        django_engine = engines['django']
        template = django_engine.from_string('Sorry, we can\'t find this:' + query)
        return HttpResponse(template.render(None, request))
            
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)    
    return render(request,'post_list.html',{'posts':posts, page:'pages'})

@login_required
def post_detail(request, post):
    post=get_object_or_404(Post,slug=post,status='published')
    comments = post.comments.all()
    new_comment = None
    
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect(post.get_absolute_url()+'#'+str(new_comment.id))
    else:
        comment_form = CommentForm()

    return render(request, 'post_detail.html',{'post':post,'comments': comments,'comment_form':comment_form})

class RegistrationLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        if 'username' not in form.cleaned_data or 'password' not in form.cleaned_data:
            return self.form_invalid(form)
        if User.objects.filter(username=form.cleaned_data['username']).exists():
            return self.form_invalid(form)
        user = User.objects.create_user(form.cleaned_data['username'], None, form.cleaned_data['password'])
        authenticate(user)
        auth_login(request, user)
        return HttpResponseRedirect(self.get_success_url())