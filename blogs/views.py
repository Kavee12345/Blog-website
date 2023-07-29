from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic
from .forms import BlogForm
from .models import Blog
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.


def error_404_view(request, exception):
    return render(request, "404.html")


def error_500_view(request):
    return render(request, "500.html")


def home(request):
    return render(request, 'home.html')


class BlogList(generic.ListView):
    model = Blog
    context_object_name = 'blog'
    template_name = 'blog/blog_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(
                Q(title__icontains=query) | Q(ingredients__icontains=query))
        else:
            object_list = self.model.objects.all()
        return object_list


class BlogDetail(generic.DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'
    slug_url_kwarg = 'the_slug'


class BlogCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = BlogForm
    template_name = "blog/create.html"
    success_url = '/my_blog'
    login_url = '/auth/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin,
                       generic.DeleteView):
    model = Blog
    template_name = 'blog/blog_delete.html'
    success_url = '/my_blog'
    slug_url_kwarg = 'the_slug'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


class BlogEditView(LoginRequiredMixin, generic.UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = "blog/edit.html"
    success_url = '/my_blog'
    slug_url_kwarg = 'the_slug'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@login_required()
def my_blog(request):
    user_blog = []
    user_blog = Blog.objects.filter(author=request.user)
    return render(request=request,
                  template_name='blog/blog_user_list.html',
                  context={
                      'user': request.user,
                      'blog': user_blog
                  })
