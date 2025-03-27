from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import Post, Comment, Tag
from .forms import PostForm, CommentForm
from django.db.models import Q
from django.urls import reverse_lazy


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile after successful update
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'blog/profile.html', {'form': form})

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-create_at']


class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/post_list.html' 
    context_object_name = 'posts'
    ordering = ['-create_at']

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        tag = get_object_or_404(Tag, slug=tag_slug)
        return Post.objects.filter(tags__in=[tag])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs.get('tag_slug')
        context['tag'] = get_object_or_404(Tag, slug=tag_slug)
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'posts'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('posts-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
def post_search(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(tags__name__icontains=query)
        ).distinct()

    return render(request, 'blog/search_results.html', {'results': results, 'query': query})
    

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs['post_id']})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})