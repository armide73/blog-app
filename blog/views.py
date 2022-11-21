from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from blog.forms import BlogForm, CommentForm, UserRegisterForm
from .models import Post, Comment

User = get_user_model()

class RegisterUser(generic.CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'user/register.html'


def logout_view(request):
    logout(request)
    return redirect('login')
    # Redirect to a success page.

@login_required
def create_blog(request):
    form = BlogForm()
    context = {
        "form": form,
    }
    if request.method == 'POST':
        blog_form = BlogForm(request.POST)
        if blog_form.is_valid():
            blog_post = blog_form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('home')
        else:
            context = {
                "form": blog_form,
                "errors": blog_form.errors,
            }
            return render(request, 'blog/create-post.html', context)
    return render(request, 'blog/create-post.html', context)


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog/index.html'

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blog/post-detail.html'
    def get(self, request, *args, **kwargs):
        try:
            object=Post.objects.get(slug=kwargs.get('slug'))
            # total_likes = object.total_likes()
            comments = Comment.objects.filter(blog=object)
            form=CommentForm()
            context={
                "object": object,
                "form": form,
                "comments": comments,
            }
            return render(request, self.template_name, context)
        except Post.DoesNotExist:
            pass
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            blog_comment = form.save(commit=False)
            blog_comment.user = request.user
            blog_comment.blog = Post.objects.get(slug=kwargs.get('slug'))
            blog_comment.save()
            return HttpResponseRedirect(reverse('post_detail', args=[str(kwargs.get('slug'))]))
        else:
            context = {
                "form": form,
                "errors": form.errors,
            }
            return render(request, self.template_name, context)
            

class PostDelete(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy('home')
    template_name = 'blog/delete-post.html'

class PostEdit(LoginRequiredMixin, generic.UpdateView):
    form_class = BlogForm
    queryset = Post.objects.all()
    success_url = reverse_lazy('home')
    template_name = 'blog/edit-post.html'


def likeView(request, slug):
    post = get_object_or_404(Post, slug=request.POST.get('post_slug'))
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_detail', args=[str(slug)]))