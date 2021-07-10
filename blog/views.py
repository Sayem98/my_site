from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date
from .models import Post, Tag
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .form import CommentForm
from .models import CommentModel
from django.urls import reverse


# Create your views here.


class index(ListView):
    template_name = 'blog/index.html'
    model = Post
    ordering = ['-date']

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


class all_posts(ListView):
    model = Post
    # paginate_by = 2
    template_name = 'blog/all_posts.html'

    # posts = Post.objects.all()
    # return render(request, 'blog/all_posts.html', {
    #     'all_posts': posts
    # })


class view_a_post(View):
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        saved_posts = request.session.get('stored_posts')
        if post.id in saved_posts:
            saved_for_letter = True
        else:
            saved_for_letter = False
        return render(request, 'blog/post_details.html', {
            'post': post,
            'post_tags': post.tags.all(),
            'comments': post.comments.all().order_by('-id'),
            'comment_form': CommentForm(),
            'saved_for_letter': saved_for_letter
        })

    def post(self, request, slug):
        comment = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        if comment.is_valid():
            comment = comment.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('post-a-page', args=[slug]))
        return render(request, 'blog/post_details.html', {
            'post': post,
            'post_tags': post.tags.all(),
            'comments': post.comments.all().order_by('-id'),
            'comment_form': CommentForm()
        })

    # model = Post
    # template_name = 'blog/post_details.html'
    #
    # # post = Post.objects.get(slug=slug)
    # # post = get_object_or_404(Post, slug=slug)
    # # return render(request, 'blog/post_details.html', {
    # #     'post': post,
    # #     'post_tags': post.tags.all()
    # # })
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['post_tags'] = self.object.tags.all()
    #     context['comment_form'] = CommentForm()
    #     return context


class SavedPosts(View):
    def get(self, request):
        stored_posts = request.session.get('stored_posts')
        # print(stored_posts)
        if stored_posts is None or len(stored_posts) == 0:
            posts = []
            has_posts = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            has_posts = True
        return render(request, 'blog/saved_posts.html', {
            'posts': posts,
            'has_posts': has_posts
        })

        # post_id = request.session['saved']
        # print(post_id)
        # post = Post.objects.filter(pk=post_id)
        # print(post[0])

    def post(self, request):
        stored_posts = request.session.get('stored_posts')
        if stored_posts is None:
            stored_posts = []
        if int(request.POST['post_id']) not in stored_posts:
            stored_posts.append(int(request.POST['post_id']))
            request.session['stored_posts'] = stored_posts
        return HttpResponseRedirect(reverse('posts-page'))

        # post_id = request.POST['post']
        # post = Post.objects.get(pk=post_id)
        # print(post)
        # # saved_posts.append(post.slug)
        # request.session['saved'] = post.id
        # return HttpResponseRedirect('posts')


class ClearSavedPosts(View):
    def post(self, request):
        request.session['stored_posts'] = []
        return HttpResponseRedirect(reverse('saved'))
