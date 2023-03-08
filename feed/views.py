from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib import messages

from followers.models import Follower
from .models import Post


class HomePage(TemplateView):
    http_method_names = ["get"]
    template_name = "feed/homepage.html"

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
           # following = list(
           #     Follower.objects.filter(
           #         followed_by=self.request.user).values_list('following', flat=True)
           # )
            # if not following:
            #    # show the default 30
            posts = Post.objects.all().order_by('-id')[0:30]
           # else:
           #     posts = Post.objects.filter(
           #         author__in=following).order_by('-id')[0:60]
        else:
            posts = Post.objects.all().order_by('-id')[0:30]
            # posts = 'Login to be able to see posts'
        context['posts'] = posts
        return context


class FriendsPostView(TemplateView):
    http_method_names = ["get"]
    template_name = "feed/friends_posts_view.html"

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            following = list(
                Follower.objects.filter(
                    followed_by=self.request.user).values_list('following', flat=True)
            )
            if not following:
                # friend_posts = 'You do not follow any friend!'
                friend_posts = Post.objects.all().order_by('-id')[0:0]
            else:
                friend_posts = Post.objects.filter(
                    author__in=following).order_by('-id')[0:60]
        else:
            friend_posts = Post.objects.all().order_by('-id')[0:30]
            #friend_posts = 'Login to be able to see posts'
        context['friend_posts'] = friend_posts
        return context


class MyPostView(TemplateView):
    http_method_names = ["get"]
    template_name = "feed/my_posts.html"

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            my_posts = Post.objects.filter(
                author=self.request.user).order_by('-id')[0:60]
        else:
            my_posts = Post.objects.all().order_by('-id')[0:0]
            context['messages'] = messages.success(
                'You do not have any posts!')
        context['my_posts'] = my_posts
        return context


class PostDetailView(DetailView):
    http_method_name = ["get"]
    template_name = "feed/detail.html"
    model = Post
    context_object_name = "post"


class CreateNewPost(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "feed/create.html"
    fields = ['text']
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        post = Post.objects.create(
            text=request.POST.get("text"),
            author=request.user,
        )
        return render(
            request,
            "includes/post.html",
            {
                "post": post,
                "show_detail_link": True,
            },
            content_type="application/html"
        )
